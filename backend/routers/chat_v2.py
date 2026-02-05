"""
LEIA - Router de Chat V2

Chat mejorado con:
- Motor de triage anti-alucinación
- Integración con sistema de casos
- Derivación inteligente a abogados
- Citación obligatoria de fuentes
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import anthropic
import os
import json

from database import get_db
from auth import get_current_user, get_current_user_optional
from models import User, Conversation, ChatMessage
from services.triage_engine import get_triage_engine, TriageDecision, TriageResult
from prompts.leia_system_prompt import build_system_prompt

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v2/chat", tags=["chat-v2"])


# ============================================================
# SCHEMAS
# ============================================================

class MessageV2(BaseModel):
    """Mensaje en la conversación"""
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=5000)


class ChatRequestV2(BaseModel):
    """Solicitud de chat mejorada"""
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[int] = None
    conversation_history: Optional[List[MessageV2]] = Field(default=[])


class SourceInfo(BaseModel):
    """Información de fuente citada"""
    source: str
    section: Optional[str] = None
    page: Optional[str] = None
    similarity: float


class ReferralSuggestion(BaseModel):
    """Sugerencia de derivación"""
    should_refer: bool
    urgency: str  # none, low, medium, high, urgent
    reason: str
    specialties: List[str]


class ChatResponseV2(BaseModel):
    """Respuesta de chat mejorada"""
    response: str
    sources: List[SourceInfo]
    has_sufficient_info: bool
    referral: Optional[ReferralSuggestion]
    tokens_used: Optional[int] = None
    conversation_id: Optional[int] = None


# ============================================================
# CLIENTE ANTHROPIC
# ============================================================

def get_anthropic_client():
    """Obtiene el cliente de Anthropic"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY no configurada"
        )
    return anthropic.Anthropic(api_key=api_key)


# ============================================================
# RAG ENGINE
# ============================================================

def get_rag_results(query: str) -> List[Dict[str, Any]]:
    """
    Obtiene resultados del RAG.

    Retorna lista de documentos con scores de similitud.
    """
    try:
        from rag.rag_engine import create_rag_engine

        engine = create_rag_engine()
        if not engine:
            return []

        results = engine.retrieve_context(query)
        return results or []

    except ImportError:
        # RAG no disponible
        return []
    except Exception as e:
        print(f"Error en RAG: {e}")
        return []


def format_rag_context(results: List[Dict[str, Any]]) -> str:
    """
    Formatea los resultados RAG como contexto para Claude.
    """
    if not results:
        return ""

    context_parts = []

    for i, doc in enumerate(results, 1):
        metadata = doc.get("metadata", {})
        content = doc.get("content", doc.get("text", ""))
        source = metadata.get("source", "Apunte sin título")
        section = metadata.get("section", "")
        page = metadata.get("page", "")
        score = doc.get("score", 0)

        header = f"### Fuente {i}: {source}"
        if section:
            header += f" - {section}"
        if page:
            header += f" (pág. {page})"
        header += f" [Relevancia: {score:.0%}]"

        context_parts.append(f"{header}\n\n{content}")

    return "\n\n---\n\n".join(context_parts)


# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@router.post("/", response_model=ChatResponseV2)
@limiter.limit("30/minute")
async def chat_v2(
    request: Request,
    chat_request: ChatRequestV2,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Chat con LEIA v2.

    Mejoras sobre v1:
    - Motor de triage anti-alucinación
    - Citación obligatoria de fuentes
    - Detección automática de derivación
    - Respuestas honestas cuando no hay info
    """
    client = get_anthropic_client()
    triage = get_triage_engine()

    # 1. Buscar en RAG
    rag_results = get_rag_results(chat_request.message)

    # 2. Analizar con motor de triage
    triage_result = triage.analyze(
        user_query=chat_request.message,
        rag_results=rag_results,
        conversation_history=[
            {"role": m.role, "content": m.content}
            for m in chat_request.conversation_history
        ] if chat_request.conversation_history else None
    )

    # 3. Determinar si hay info suficiente
    has_sufficient_info = triage_result.decision == TriageDecision.RESPOND_WITH_SOURCES

    # 4. Construir prompt del sistema
    rag_context = format_rag_context(triage_result.sources_found) if has_sufficient_info else ""
    system_prompt = build_system_prompt(
        rag_context=rag_context,
        has_relevant_sources=has_sufficient_info
    )

    # 5. Agregar instrucciones según el triage
    if triage_result.decision == TriageDecision.NO_INFO_AVAILABLE:
        system_prompt += f"""

## INSTRUCCIÓN ESPECIAL PARA ESTA RESPUESTA

{triage_result.reason}

Debes responder honestamente que no tienes información sobre este tema.
Usa el formato de respuesta para "cuando no hay info".
Sugiere consultar con un abogado especializado en: {', '.join(triage_result.suggested_specialties)}
"""

    elif triage_result.decision in [TriageDecision.URGENT_MATTER, TriageDecision.SENSITIVE_TOPIC]:
        system_prompt += f"""

## INSTRUCCIÓN ESPECIAL: DERIVACIÓN URGENTE

{triage_result.reason}

Este caso requiere atención profesional inmediata.
Después de una breve orientación, ofrece conectar con un abogado.
Especialidades sugeridas: {', '.join(triage_result.suggested_specialties)}
"""

    elif triage_result.decision == TriageDecision.REQUIRES_LAWYER:
        system_prompt += f"""

## INSTRUCCIÓN ESPECIAL: DERIVACIÓN

El usuario necesita asesoría legal profesional.
Después de orientar brevemente, ofrece la derivación.
Especialidades sugeridas: {', '.join(triage_result.suggested_specialties)}
"""

    # 6. Construir mensajes para Claude
    messages = []

    for msg in chat_request.conversation_history or []:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    messages.append({
        "role": "user",
        "content": chat_request.message
    })

    # 7. Llamar a Claude
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            system=system_prompt,
            messages=messages
        )

        assistant_message = response.content[0].text

    except anthropic.APIError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de API: {str(e)}"
        )

    # 8. Guardar en base de datos si hay usuario
    conversation_id = chat_request.conversation_id

    if current_user:
        # Crear o actualizar conversación
        if not conversation_id:
            conversation = Conversation(
                user_id=current_user.id,
                title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            conversation_id = conversation.id
        else:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            ).first()

            if not conversation:
                raise HTTPException(
                    status_code=404,
                    detail="Conversación no encontrada"
                )

        # Guardar mensajes
        user_msg = ChatMessage(
            conversation_id=conversation_id,
            role="user",
            content=chat_request.message
        )
        db.add(user_msg)

        assistant_msg = ChatMessage(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_message,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens
        )
        db.add(assistant_msg)

        db.commit()

    # 9. Preparar fuentes para la respuesta
    sources = []
    if triage_result.sources_found:
        for doc in triage_result.sources_found:
            metadata = doc.get("metadata", {})
            sources.append(SourceInfo(
                source=metadata.get("source", "Apunte"),
                section=metadata.get("section"),
                page=metadata.get("page"),
                similarity=doc.get("score", 0)
            ))

    # 10. Preparar sugerencia de derivación
    referral = None
    if triage_result.decision in [
        TriageDecision.URGENT_MATTER,
        TriageDecision.SENSITIVE_TOPIC,
        TriageDecision.REQUIRES_LAWYER,
        TriageDecision.NO_INFO_AVAILABLE
    ]:
        urgency_map = {
            TriageDecision.URGENT_MATTER: "urgent",
            TriageDecision.SENSITIVE_TOPIC: "high",
            TriageDecision.REQUIRES_LAWYER: "medium",
            TriageDecision.NO_INFO_AVAILABLE: "low"
        }

        referral = ReferralSuggestion(
            should_refer=True,
            urgency=urgency_map.get(triage_result.decision, "low"),
            reason=triage_result.reason,
            specialties=triage_result.suggested_specialties
        )

    return ChatResponseV2(
        response=assistant_message,
        sources=sources,
        has_sufficient_info=has_sufficient_info,
        referral=referral,
        tokens_used=response.usage.input_tokens + response.usage.output_tokens,
        conversation_id=conversation_id
    )


# ============================================================
# ENDPOINT DE MATCHING RÁPIDO
# ============================================================

@router.post("/suggest-lawyers")
async def suggest_lawyers_from_chat(
    request: Request,
    message: str = "",
    legal_area: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Sugiere abogados basado en el contexto del chat.

    Usa el mensaje del usuario para detectar área legal y ubicación.
    """
    from models import Lawyer

    triage = get_triage_engine()

    # Detectar especialidades desde el mensaje
    if not legal_area and message:
        specialties = triage._detect_specialties(message.lower())
        legal_area = specialties[0] if specialties else "Derecho General"

    # Buscar abogados
    query = db.query(Lawyer).filter(Lawyer.is_verified == True)

    if legal_area and legal_area != "Derecho General":
        # Mapear áreas a especialidades de la BD
        area_mapping = {
            "Derecho Laboral": ["Laboral", "Derecho Laboral", "Trabajo"],
            "Derecho de Familia": ["Familia", "Derecho de Familia"],
            "Derecho Civil": ["Civil", "Derecho Civil", "Contratos"],
            "Derecho Penal": ["Penal", "Derecho Penal", "Criminal"],
            "Derecho del Consumidor": ["Consumidor", "SERNAC"]
        }

        search_terms = area_mapping.get(legal_area, [legal_area])
        from sqlalchemy import or_
        query = query.filter(
            or_(*[Lawyer.specialty.ilike(f"%{term}%") for term in search_terms])
        )

    if region:
        query = query.filter(Lawyer.location.ilike(f"%{region}%"))

    # Ordenar por rating
    lawyers = query.order_by(Lawyer.rating.desc()).limit(5).all()

    return {
        "detected_area": legal_area,
        "lawyers": [
            {
                "id": l.id,
                "name": l.name,
                "specialty": l.specialty,
                "rating": l.rating or 0,
                "reviews_count": l.reviews or 0,
                "location": l.location,
                "price_display": f"${l.price_min:,} - ${l.price_max:,}".replace(",", ".") if l.price_min and l.price_max else None,
                "is_verified": l.is_verified
            }
            for l in lawyers
        ]
    }


# ============================================================
# ENDPOINT PARA CREAR CASO DESDE CHAT
# ============================================================

@router.post("/create-case")
async def create_case_from_chat(
    request: Request,
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un caso a partir de una conversación existente.

    1. Genera resumen automático
    2. Extrae hechos y fechas
    3. Detecta área legal
    4. Prepara para transferencia
    """
    from models_extended import Case, CaseEvent, CaseStatus, CasePriority, generate_case_number

    # Verificar conversación
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversación no encontrada"
        )

    # Verificar que no exista ya un caso
    existing_case = db.query(Case).filter(
        Case.conversation_id == conversation_id
    ).first()

    if existing_case:
        return {
            "status": "exists",
            "case_id": existing_case.id,
            "case_number": existing_case.case_number,
            "message": "Ya existe un caso para esta conversación"
        }

    # Obtener mensajes
    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.created_at).all()

    if not messages:
        raise HTTPException(
            status_code=400,
            detail="La conversación no tiene mensajes"
        )

    # Construir texto de conversación
    conversation_text = "\n".join([
        f"{'Usuario' if m.role == 'user' else 'LEIA'}: {m.content}"
        for m in messages
    ])

    # Generar resumen con Claude
    client = get_anthropic_client()

    from prompts.leia_system_prompt import build_case_summary_prompt
    summary_prompt = build_case_summary_prompt(conversation_text)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": summary_prompt}]
    )

    # Parsear respuesta
    try:
        summary_data = json.loads(response.content[0].text)
    except json.JSONDecodeError:
        # Fallback si no se puede parsear
        summary_data = {
            "summary": conversation.title or "Caso legal",
            "legal_area": "Por determinar"
        }

    # Crear caso
    case_number = generate_case_number(db)

    # Mapear urgencia a prioridad
    urgency_to_priority = {
        "low": CasePriority.LOW,
        "medium": CasePriority.MEDIUM,
        "high": CasePriority.HIGH,
        "urgent": CasePriority.URGENT
    }

    new_case = Case(
        user_id=current_user.id,
        conversation_id=conversation_id,
        case_number=case_number,
        title=summary_data.get("summary", "")[:255] or conversation.title or "Caso legal",
        summary=summary_data.get("summary"),
        legal_area=summary_data.get("legal_area"),
        sub_area=summary_data.get("sub_area"),
        priority=urgency_to_priority.get(
            summary_data.get("urgency", "medium"),
            CasePriority.MEDIUM
        ),
        status=CaseStatus.READY_TO_TRANSFER,
        region=summary_data.get("region"),
        city=summary_data.get("city"),
        risk_level=summary_data.get("risk_level"),
        risk_factors=summary_data.get("risk_factors"),
        extracted_facts=summary_data.get("facts"),
        extracted_dates=summary_data.get("dates"),
        pending_questions=summary_data.get("pending_questions")
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # Registrar evento
    event = CaseEvent(
        case_id=new_case.id,
        actor_id=current_user.id,
        event_type="created",
        description=f"Caso {case_number} creado desde conversación"
    )
    db.add(event)
    db.commit()

    return {
        "status": "created",
        "case_id": new_case.id,
        "case_number": new_case.case_number,
        "summary": new_case.summary,
        "legal_area": new_case.legal_area,
        "risk_level": new_case.risk_level,
        "pending_questions": new_case.pending_questions,
        "message": "Caso creado exitosamente. Ahora puedes transferirlo a un abogado."
    }
