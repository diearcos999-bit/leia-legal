from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from sqlalchemy.orm import Session
import anthropic
import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# RAG imports
try:
    from rag.rag_engine import create_rag_engine
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("ℹ️  RAG module not available")

# Rate limiting imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

# Import database and auth modules
from database import get_db, init_db
from auth import (
    UserCreate, UserLogin, UserResponse, Token, ProfessionalCreate,
    create_user, authenticate_user, get_user_by_email, create_professional,
    create_access_token, get_current_user, get_current_user_optional,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import User, Lawyer, Consultation, PJUDConnection, CausaJudicial, ProfessionalType

# Import routers
from routers import pjud as pjud_router
from routers import estadisticas as estadisticas_router
from routers import agents as agents_router
from routers import cases as cases_router
from routers import lawyers_extended as lawyers_ext_router
from routers import chat_v2 as chat_v2_router
from routers import messages as messages_router
from routers import notifications as notifications_router
from routers import calls as calls_router
from routers import oauth as oauth_router

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="LEIA API",
    description="Backend API para LEIA - Asistente Legal con IA para Chile",
    version="0.1.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(pjud_router.router)
app.include_router(estadisticas_router.router)
app.include_router(agents_router.router)
app.include_router(cases_router.router)
app.include_router(lawyers_ext_router.router)
app.include_router(chat_v2_router.router)
app.include_router(messages_router.router)
app.include_router(notifications_router.router)
app.include_router(calls_router.router)
app.include_router(oauth_router.router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ Database initialized")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Anthropic Client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("⚠️  WARNING: ANTHROPIC_API_KEY not set. Chat will not work.")
    client = None
else:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# RAG Engine - Para respuestas con legislación chilena real
rag_engine = None
if RAG_AVAILABLE:
    rag_engine = create_rag_engine()
    if rag_engine:
        print("✅ RAG Engine initialized - Chat will use Chilean legal knowledge")
    else:
        print("ℹ️  RAG Engine not configured - Chat will use base Claude knowledge")

# Validation constants
MAX_MESSAGE_LENGTH = 5000
MAX_HISTORY_MESSAGES = 50
MAX_FEEDBACK_LENGTH = 10000
MAX_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 2000
MAX_PHONE_LENGTH = 20

def sanitize_string(value: str) -> str:
    """Remove potentially dangerous characters from strings."""
    if not value:
        return value
    # Remove control characters and null bytes
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value.strip()


# Pydantic Models
class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LENGTH)

    @field_validator('content')
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        return sanitize_string(v)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LENGTH)
    conversation_history: Optional[List[Message]] = Field(default=[], max_length=MAX_HISTORY_MESSAGES)

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = sanitize_string(v)
        if not v:
            raise ValueError('El mensaje no puede estar vacío')
        return v


class ChatResponse(BaseModel):
    response: str
    tokens_used: Optional[int] = None


class FeedbackRequest(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=100)
    user_question: str = Field(..., max_length=MAX_MESSAGE_LENGTH)
    ai_response: str = Field(..., max_length=MAX_FEEDBACK_LENGTH)
    feedback: str = Field(..., pattern="^(helpful|not_helpful)$")
    correction: Optional[str] = Field(None, max_length=MAX_DESCRIPTION_LENGTH)
    timestamp: Optional[str] = None

    @field_validator('feedback')
    @classmethod
    def validate_feedback(cls, v: str) -> str:
        if v not in ['helpful', 'not_helpful']:
            raise ValueError('El feedback debe ser "helpful" o "not_helpful"')
        return v

    @field_validator('correction')
    @classmethod
    def sanitize_correction(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return sanitize_string(v)
        return v


# Pydantic Models for Lawyers
class LawyerResponse(BaseModel):
    id: int
    name: str
    professional_type: Optional[str] = "abogado"
    specialty: str
    experience: Optional[str] = None
    rating: float
    reviews: int
    location: Optional[str] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    price: Optional[str] = None  # Formatted price string
    image: Optional[str] = None
    cases: int
    success_rate: Optional[float] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    is_verified: bool

    class Config:
        from_attributes = True


class LawyerListResponse(BaseModel):
    lawyers: List[LawyerResponse]
    total: int
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)


class ConsultationCreate(BaseModel):
    lawyer_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=MAX_NAME_LENGTH)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    phone: Optional[str] = Field(None, max_length=MAX_PHONE_LENGTH)
    description: str = Field(..., min_length=10, max_length=MAX_DESCRIPTION_LENGTH)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = sanitize_string(v)
        if len(v) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        v = sanitize_string(v)
        if len(v) < 10:
            raise ValueError('La descripción debe tener al menos 10 caracteres')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = sanitize_string(v)
            # Remove non-numeric characters except + for country code
            cleaned = re.sub(r'[^\d+]', '', v)
            if len(cleaned) < 8 or len(cleaned) > 15:
                raise ValueError('El teléfono debe tener entre 8 y 15 dígitos')
            return cleaned
        return v


class ConsultationResponse(BaseModel):
    id: int
    lawyer_id: int
    name: str
    email: str
    phone: Optional[str] = None
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# System Prompt para el Asistente Legal
SYSTEM_PROMPT = """Eres LEIA, un asistente legal especializado en leyes chilenas. Tu nombre significa Legal IA y tu misión es democratizar el acceso a justicia en Chile.

TU ROL:
- Proporcionar orientación legal GENERAL en lenguaje simple y accesible
- Especializado en el sistema legal chileno
- Ayudar a los usuarios a entender sus derechos y opciones
- Explicar términos legales en lenguaje comprensible
- Ser empático y profesional

IMPORTANTE - LIMITACIONES:
- NO eres un abogado y NO proporcionas asesoría legal formal
- NO puedes representar legalmente a nadie
- SIEMPRE recomienda consultar con un abogado para casos específicos
- NO des consejos que puedan interpretarse como asesoría legal profesional

ÁREAS DE ESPECIALIDAD:
- Derecho Laboral (despidos, finiquitos, indemnizaciones)
- Derecho de Familia (divorcios, pensiones alimenticias, cuidado personal)
- Deudas y Cobranzas
- Arriendos y desalojos
- Derecho del Consumidor
- Herencias básicas
- Causas judiciales y trámites en tribunales

CONOCIMIENTO DEL SISTEMA JUDICIAL CHILENO:
- Conoces los tipos de causas: Civil (C-), Laboral (T-), Familia (F-), Penal (O-/G-)
- Conoces las Cortes de Apelaciones de Chile (Arica, Iquique, Antofagasta, Copiapó, La Serena, Valparaíso, Rancagua, Talca, Chillán, Concepción, Temuco, Valdivia, Puerto Montt, Coyhaique, Punta Arenas, Santiago, San Miguel)
- Conoces los tipos de tribunales: Civiles, de Familia, del Trabajo, de Garantía, Orales en lo Penal, de Cobranza
- Puedes explicar el significado de RIT (Rol Interno del Tribunal), RUC (Rol Único de Causa), ROL, etc.

GLOSARIO LEGAL INTEGRADO:
Cuando el usuario pregunte por un término legal, explícalo en lenguaje sencillo. Conoces términos como:
- Alimentos: Pensión para subsistencia de hijos u otros familiares
- Cuidado Personal: Antes llamado "tuición", es el derecho de tener al hijo viviendo consigo
- Relación Directa y Regular: Antes llamado "visitas", derecho del padre que no tiene cuidado personal
- Despido Injustificado: Término del contrato sin causal legal válida
- Sentencia Ejecutoriada: Sentencia firme que no admite recursos
- Medida Cautelar: Resolución para asegurar el resultado del juicio
- Embargo: Afectar bienes del deudor para garantizar el pago
- Apelación: Recurso para que un tribunal superior revise una resolución
- Y muchos más términos del derecho chileno

FORMATO DE RESPUESTA:
1. Muestra empatía con la situación
2. Explica el concepto legal en lenguaje simple
3. Si hay términos técnicos, explícalos brevemente
4. Menciona los derechos del usuario
5. Sugiere pasos generales a seguir
6. SIEMPRE recomienda consultar con un abogado para el caso específico
7. Si es relevante, ofrece conectar con abogados verificados de nuestra red

TONO: Profesional, empático, accesible, educativo.

Recuerda: Tu objetivo es ORIENTAR y EDUCAR, no dar asesoría legal formal."""

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "LEIA API - Asistente Legal con IA",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "me": "/api/auth/me"
            },
            "chat": "/api/chat",
            "feedback": "/api/feedback",
            "feedback_stats": "/api/feedback/stats",
            "quick_questions": "/api/quick-questions",
            "lawyers": {
                "list": "/api/lawyers",
                "detail": "/api/lawyers/{id}"
            },
            "consultations": "/api/consultations",
            "pjud": {
                "status": "/api/pjud/status",
                "connect": "/api/pjud/connect",
                "sync": "/api/pjud/sync",
                "causas": "/api/pjud/causas"
            },
            "estadisticas": {
                "cortes": "/api/cortes",
                "competencias": "/api/competencias",
                "tribunales": "/api/tribunales",
                "ingresos": "/api/estadisticas/ingresos",
                "resumen": "/api/estadisticas/resumen"
            },
            "glosario": {
                "buscar": "/api/glosario/buscar",
                "explicar": "/api/glosario/explicar",
                "categorias": "/api/glosario/categorias",
                "siglas": "/api/glosario/siglas",
                "latinas": "/api/glosario/latinas"
            },
            "agents": {
                "status": "/api/agents/status",
                "research": "/api/agents/research",
                "generate_document": "/api/agents/generate-document",
                "templates": "/api/agents/templates",
                "chat": "/api/agents/chat",
                "categories": "/api/agents/categories"
            },
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "anthropic_configured": ANTHROPIC_API_KEY is not None
    }


# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/register", response_model=Token)
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.

    - Verifica que el email no esté ya registrado
    - Hashea la contraseña
    - Crea el usuario en la base de datos
    - Retorna un token JWT para autenticación inmediata
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Password validation is now handled by Pydantic validators in auth.py
    # Create user
    user = create_user(db, user_data)

    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


class ProfessionalResponse(BaseModel):
    """Response for professional registration."""
    access_token: str
    token_type: str
    user: UserResponse
    professional_type: str
    lawyer_id: int


@app.post("/api/auth/register/professional", response_model=ProfessionalResponse)
@limiter.limit("5/minute")
async def register_professional(request: Request, professional_data: ProfessionalCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo profesional legal (abogado, procurador, o estudio jurídico).

    - Verifica que el email no esté ya registrado
    - Crea el usuario con rol 'lawyer'
    - Crea el perfil de abogado/profesional asociado
    - Retorna un token JWT para autenticación inmediata
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, professional_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Create professional (user + lawyer profile)
    user, lawyer = create_professional(db, professional_data)

    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return ProfessionalResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
        professional_type=professional_data.professional_type,
        lawyer_id=lawyer.id
    )


class LoginResponse(BaseModel):
    """Extended login response that includes professional_type for lawyers."""
    access_token: str
    token_type: str
    user: UserResponse
    professional_type: Optional[str] = None
    lawyer_id: Optional[int] = None


@app.post("/api/auth/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica un usuario y retorna un token JWT.

    - Verifica las credenciales (email y contraseña)
    - Retorna un token JWT válido por 7 días
    - Para profesionales, incluye professional_type y lawyer_id
    """
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Get professional_type if user is a lawyer
    professional_type = None
    lawyer_id = None
    if user.role == "lawyer":
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == user.id).first()
        if lawyer:
            professional_type = lawyer.professional_type.value if lawyer.professional_type else "abogado"
            lawyer_id = lawyer.id

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
        professional_type=professional_type,
        lawyer_id=lawyer_id
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Retorna la información del usuario autenticado actual.

    Requiere un token JWT válido en el header Authorization.
    """
    return UserResponse.model_validate(current_user)


@app.put("/api/auth/me", response_model=UserResponse)
async def update_current_user(
    full_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza la información del usuario autenticado.
    """
    if full_name is not None:
        current_user.full_name = full_name
        db.commit()
        db.refresh(current_user)

    return UserResponse.model_validate(current_user)


# ==================== CHAT ENDPOINTS ====================

@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat(request: Request, chat_request: ChatRequest):
    """
    Endpoint principal del chatbot legal con IA.

    Recibe un mensaje del usuario y el historial de conversación,
    y devuelve una respuesta generada por Claude.

    Si RAG está configurado, enriquece las respuestas con legislación chilena real.
    """
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Anthropic API no está configurada. Por favor configura ANTHROPIC_API_KEY en el archivo .env"
        )

    try:
        # Construir el historial de mensajes para Claude
        messages = []

        # Agregar historial previo
        for msg in chat_request.conversation_history:
            if msg.role in ['user', 'assistant']:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Agregar el mensaje actual del usuario
        messages.append({
            "role": "user",
            "content": chat_request.message
        })

        # Usar RAG si está disponible para enriquecer la respuesta
        enhanced_system_prompt = SYSTEM_PROMPT
        rag_sources = []

        if rag_engine:
            try:
                # Buscar contexto legal relevante
                relevant_docs = rag_engine.retrieve_context(chat_request.message)

                if relevant_docs:
                    # Construir contexto con los documentos encontrados
                    context = rag_engine.build_context_prompt(relevant_docs)

                    # Enriquecer el prompt con el contexto legal
                    enhanced_system_prompt = f"""{SYSTEM_PROMPT}

{context}

INSTRUCCIONES ESPECIALES RAG:
- USA la información del CONTEXTO LEGAL RELEVANTE proporcionado arriba para responder con precisión
- CITA las fuentes específicas cuando uses información del contexto (ej: "Según el Código del Trabajo, Artículo X...")
- Si el contexto no cubre completamente la pregunta, indícalo claramente
- SIEMPRE prioriza la información del contexto sobre tu conocimiento general
- Si hay contradicciones, usa el contexto como fuente de verdad
"""
                    # Guardar fuentes para metadata
                    rag_sources = [
                        {
                            "law_name": doc.get("law_name"),
                            "article": doc.get("article_number"),
                            "category": doc.get("category"),
                            "similarity": doc.get("score")
                        }
                        for doc in relevant_docs
                    ]
            except Exception as rag_error:
                # Si RAG falla, continuar sin él
                print(f"⚠️  RAG error (continuing without): {rag_error}")

        # Llamar a Claude API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=enhanced_system_prompt,
            messages=messages
        )

        # Extraer la respuesta
        assistant_message = response.content[0].text

        return ChatResponse(
            response=assistant_message,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens
        )

    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Error de Anthropic API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/api/quick-questions")
async def get_quick_questions():
    """
    Devuelve preguntas rápidas sugeridas para el usuario.
    """
    return {
        "questions": [
            "Me despidieron sin finiquito, ¿qué hago?",
            "Quiero divorciarme, ¿cuáles son los pasos?",
            "Tengo deudas que no puedo pagar",
            "Mi arrendador no me devuelve el depósito",
            "¿Cómo calcular la indemnización por años de servicio?",
            "¿Qué es la pensión alimenticia y cómo se calcula?"
        ]
    }

# Directorio para almacenar feedbacks
FEEDBACK_DIR = Path(__file__).parent / "data" / "feedbacks"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/api/feedback")
@limiter.limit("30/minute")
async def save_feedback(request: Request, feedback: FeedbackRequest):
    """
    Guarda feedback del usuario sobre las respuestas del AI.

    El feedback se guarda en un archivo JSON para análisis posterior
    y mejora continua del sistema.
    """
    try:
        feedback_file = FEEDBACK_DIR / "feedbacks.json"

        # Preparar datos del feedback
        feedback_data = {
            "message_id": feedback.message_id,
            "user_question": feedback.user_question,
            "ai_response": feedback.ai_response,
            "feedback": feedback.feedback,
            "correction": feedback.correction,
            "timestamp": feedback.timestamp or datetime.now().isoformat(),
            "saved_at": datetime.now().isoformat()
        }

        # Leer feedbacks existentes o crear lista vacía
        existing_feedbacks = []
        if feedback_file.exists():
            try:
                with open(feedback_file, "r", encoding="utf-8") as f:
                    existing_feedbacks = json.load(f)
            except (json.JSONDecodeError, IOError):
                existing_feedbacks = []

        # Agregar nuevo feedback
        existing_feedbacks.append(feedback_data)

        # Guardar todos los feedbacks
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(existing_feedbacks, f, ensure_ascii=False, indent=2)

        return {
            "status": "saved",
            "message": "Feedback guardado exitosamente. ¡Gracias por ayudarnos a mejorar!"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar feedback: {str(e)}"
        )

@app.get("/api/feedback/stats")
async def get_feedback_stats():
    """
    Devuelve estadísticas básicas del feedback recibido.
    """
    try:
        feedback_file = FEEDBACK_DIR / "feedbacks.json"

        if not feedback_file.exists():
            return {
                "total": 0,
                "helpful": 0,
                "not_helpful": 0,
                "with_corrections": 0
            }

        with open(feedback_file, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)

        helpful = sum(1 for f in feedbacks if f.get("feedback") == "helpful")
        not_helpful = sum(1 for f in feedbacks if f.get("feedback") == "not_helpful")
        with_corrections = sum(1 for f in feedbacks if f.get("correction"))

        return {
            "total": len(feedbacks),
            "helpful": helpful,
            "not_helpful": not_helpful,
            "with_corrections": with_corrections,
            "helpful_rate": round(helpful / len(feedbacks) * 100, 1) if feedbacks else 0
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


# ==================== LAWYERS ENDPOINTS ====================

@app.get("/api/lawyers", response_model=LawyerListResponse)
@limiter.limit("60/minute")
async def list_lawyers(
    request: Request,
    specialty: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    Lista abogados con filtros opcionales.

    - specialty: Filtrar por especialidad
    - location: Filtrar por ubicación
    - search: Buscar por nombre
    - page: Número de página (default: 1)
    - page_size: Tamaño de página (default: 10)
    """
    query = db.query(Lawyer)

    # Apply filters
    if specialty and specialty != "Todas las especialidades":
        query = query.filter(Lawyer.specialty == specialty)

    if location and location != "Todas las ubicaciones":
        query = query.filter(Lawyer.location == location)

    if search:
        query = query.filter(Lawyer.name.ilike(f"%{search}%"))

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    lawyers = query.offset(offset).limit(page_size).all()

    # Format response
    lawyer_responses = []
    for lawyer in lawyers:
        price = None
        if lawyer.price_min and lawyer.price_max:
            price = f"${lawyer.price_min:,} - ${lawyer.price_max:,}".replace(",", ".")

        # Get professional_type value
        prof_type = lawyer.professional_type.value if lawyer.professional_type else "abogado"

        lawyer_responses.append(LawyerResponse(
            id=lawyer.id,
            name=lawyer.name,
            professional_type=prof_type,
            specialty=lawyer.specialty,
            experience=lawyer.experience,
            rating=lawyer.rating or 0,
            reviews=lawyer.reviews or 0,
            location=lawyer.location,
            price_min=lawyer.price_min,
            price_max=lawyer.price_max,
            price=price,
            image=lawyer.image,
            cases=lawyer.cases or 0,
            success_rate=lawyer.success_rate,
            description=lawyer.description,
            phone=lawyer.phone,
            is_verified=lawyer.is_verified
        ))

    return LawyerListResponse(
        lawyers=lawyer_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@app.get("/api/lawyers/{lawyer_id}", response_model=LawyerResponse)
@limiter.limit("60/minute")
async def get_lawyer(request: Request, lawyer_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de un abogado específico.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    price = None
    if lawyer.price_min and lawyer.price_max:
        price = f"${lawyer.price_min:,} - ${lawyer.price_max:,}".replace(",", ".")

    prof_type = lawyer.professional_type.value if lawyer.professional_type else "abogado"

    return LawyerResponse(
        id=lawyer.id,
        name=lawyer.name,
        professional_type=prof_type,
        specialty=lawyer.specialty,
        experience=lawyer.experience,
        rating=lawyer.rating or 0,
        reviews=lawyer.reviews or 0,
        location=lawyer.location,
        price_min=lawyer.price_min,
        price_max=lawyer.price_max,
        price=price,
        image=lawyer.image,
        cases=lawyer.cases or 0,
        success_rate=lawyer.success_rate,
        description=lawyer.description,
        phone=lawyer.phone,
        is_verified=lawyer.is_verified
    )


@app.get("/api/auth/me/professional", response_model=LawyerResponse)
async def get_current_professional_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna el perfil profesional del usuario autenticado.
    Solo funciona para usuarios con rol 'lawyer'.
    """
    if current_user.role != "lawyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no es un profesional legal"
        )

    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil profesional no encontrado"
        )

    price = None
    if lawyer.price_min and lawyer.price_max:
        price = f"${lawyer.price_min:,} - ${lawyer.price_max:,}".replace(",", ".")

    prof_type = lawyer.professional_type.value if lawyer.professional_type else "abogado"

    return LawyerResponse(
        id=lawyer.id,
        name=lawyer.name,
        professional_type=prof_type,
        specialty=lawyer.specialty,
        experience=lawyer.experience,
        rating=lawyer.rating or 0,
        reviews=lawyer.reviews or 0,
        location=lawyer.location,
        price_min=lawyer.price_min,
        price_max=lawyer.price_max,
        price=price,
        image=lawyer.image,
        cases=lawyer.cases or 0,
        success_rate=lawyer.success_rate,
        description=lawyer.description,
        phone=lawyer.phone,
        is_verified=lawyer.is_verified
    )


# ==================== CONSULTATIONS ENDPOINTS ====================

@app.post("/api/consultations", response_model=ConsultationResponse)
@limiter.limit("10/minute")
async def create_consultation(
    request: Request,
    consultation: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Crea una solicitud de consulta con un abogado.

    Valida que el abogado exista y guarda la solicitud.
    """
    # Verify lawyer exists
    lawyer = db.query(Lawyer).filter(Lawyer.id == consultation.lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    # Create consultation
    new_consultation = Consultation(
        lawyer_id=consultation.lawyer_id,
        user_id=current_user.id if current_user else None,
        name=consultation.name,
        email=consultation.email,
        phone=consultation.phone,
        description=consultation.description,
        status="pending"
    )

    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)

    return ConsultationResponse(
        id=new_consultation.id,
        lawyer_id=new_consultation.lawyer_id,
        name=new_consultation.name,
        email=new_consultation.email,
        phone=new_consultation.phone,
        description=new_consultation.description,
        status=new_consultation.status,
        created_at=new_consultation.created_at
    )


@app.get("/api/consultations", response_model=List[ConsultationResponse])
@limiter.limit("30/minute")
async def list_user_consultations(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista las consultas del usuario autenticado.
    """
    consultations = db.query(Consultation).filter(
        Consultation.user_id == current_user.id
    ).order_by(Consultation.created_at.desc()).all()

    return [
        ConsultationResponse(
            id=c.id,
            lawyer_id=c.lawyer_id,
            name=c.name,
            email=c.email,
            phone=c.phone,
            description=c.description,
            status=c.status,
            created_at=c.created_at
        )
        for c in consultations
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
