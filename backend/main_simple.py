"""
Backend simplificado para LEIA - Compatible con Python 3.14
Sin Pydantic para evitar problemas de compilación
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

# Importar base de datos y routers extendidos
try:
    from database import engine, Base, get_db
    from routers import chat_v2, lawyers_extended, auth, pjud, notifications, cases, direct_chat
    EXTENDED_ROUTERS = True
except ImportError as e:
    print(f"ℹ️  Routers extendidos no disponibles: {e}")
    EXTENDED_ROUTERS = False

# Intentar cargar RAG Engine
try:
    from rag.rag_engine import create_rag_engine
    rag_engine = create_rag_engine()
    RAG_ENABLED = rag_engine is not None
except Exception as e:
    print(f"ℹ️  RAG no disponible: {e}")
    print("   Chatbot funcionará sin RAG (solo Claude)")
    rag_engine = None
    RAG_ENABLED = False

app = FastAPI(
    title="LEIA API",
    description="Backend API para LEIA - Asistente Legal con IA para Chile",
    version="0.1.0"
)

# CORS Configuration - Dynamic based on environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
origins = [origin.strip() for origin in CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for Railway/Render
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "leia-backend"}

# Incluir routers extendidos si están disponibles
if EXTENDED_ROUTERS:
    app.include_router(auth.router)
    app.include_router(chat_v2.router)
    app.include_router(lawyers_extended.router)
    app.include_router(pjud.router)
    app.include_router(notifications.router)
    app.include_router(cases.router)
    app.include_router(direct_chat.router)
    print("✅ Routers cargados (auth, chat_v2, lawyers_extended, pjud, notifications, cases, direct_chat)")

# Anthropic Client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("⚠️  WARNING: ANTHROPIC_API_KEY not set. Chat will not work.")
    print("   Get your key at: https://console.anthropic.com/")
    print("   Then add it to backend/.env file")
    client = None
else:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Anthropic API configured successfully!")

# System Prompt para el Asistente Legal
SYSTEM_PROMPT = """Eres LEIA, un asistente legal especializado en leyes chilenas. Tu nombre significa Legal IA y tu misión es democratizar el acceso a justicia en Chile.

TU ROL:
- Proporcionar orientación legal GENERAL en lenguaje simple y accesible
- Especializado en el sistema legal chileno
- Ayudar a los usuarios a entender sus derechos y opciones
- Ser empática y profesional

IMPORTANTE - LIMITACIONES:
- NO eres abogada y NO proporcionas asesoría legal formal
- NO puedes representar legalmente a nadie
- SIEMPRE recomienda consultar con un abogado para casos específicos
- NO des consejos que puedan interpretarse como asesoría legal profesional

ÁREAS DE ESPECIALIDAD:
- Derecho Laboral (despidos, finiquitos, indemnizaciones)
- Derecho de Familia (divorcios, pensiones alimenticias, custodia)
- Deudas y Cobranzas (prescripción, defensas, renegociación)
- Arriendos (contratos, desahucios, garantías)
- Derecho del Consumidor (SERNAC, garantías, devoluciones)
- Herencias básicas

FORMATO DE RESPUESTA:
1. Muestra empatía con la situación
2. Explica el concepto legal en lenguaje simple
3. Menciona los derechos del usuario
4. Sugiere pasos generales a seguir
5. SIEMPRE recomienda consultar con un abogado para el caso específico
6. Si es relevante, ofrece conectar con abogados verificados de nuestra red

TONO: Profesional, empática, accesible, educativo. Habla en primera persona como LEIA.

Recuerda: Tu objetivo es ORIENTAR y EDUCAR, no dar asesoría legal formal."""

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "LEIA API - Asistente Legal con IA",
        "version": "0.1.0",
        "status": "running",
        "python_version": "3.14+ compatible",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "anthropic_configured": ANTHROPIC_API_KEY is not None,
        "rag_enabled": RAG_ENABLED,
        "message": "Backend is running" if ANTHROPIC_API_KEY else "Configure ANTHROPIC_API_KEY in .env"
    }

@app.post("/api/chat")
async def chat(request: dict):
    """
    Endpoint principal del chatbot legal con IA.

    Acepta:
    {
        "message": "string",
        "conversation_history": [
            {"role": "user|assistant", "content": "string"}
        ]
    }

    Devuelve:
    {
        "response": "string",
        "tokens_used": int
    }
    """
    if not client:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Anthropic API no configurada",
                "message": "Por favor configura ANTHROPIC_API_KEY en el archivo .env",
                "instructions": "1. Ve a https://console.anthropic.com/ \n2. Crea cuenta gratis\n3. Copia tu API key\n4. Agrégala a backend/.env"
            }
        )

    try:
        # Extraer datos del request
        user_message = request.get("message", "")
        conversation_history = request.get("conversation_history", [])

        if not user_message:
            raise HTTPException(status_code=400, detail="El campo 'message' es requerido")

        # Si RAG está habilitado, usar RAG Engine
        if RAG_ENABLED and rag_engine:
            try:
                result = rag_engine.generate_response(
                    user_query=user_message,
                    conversation_history=conversation_history,
                    client=client,
                    system_prompt=SYSTEM_PROMPT
                )

                return {
                    "response": result["response"],
                    "tokens_used": result["tokens_used"],
                    "rag_enabled": True,
                    "sources_used": result["sources_used"],
                    "sources": result["sources"]
                }
            except Exception as rag_error:
                print(f"⚠️  Error en RAG, fallback a Claude: {rag_error}")
                # Si falla RAG, continuar con Claude normal

        # Fallback: Claude sin RAG
        messages = []

        # Agregar historial previo
        for msg in conversation_history:
            if isinstance(msg, dict) and msg.get("role") in ['user', 'assistant']:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Agregar el mensaje actual del usuario
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Llamar a Claude API con el modelo correcto
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Modelo más reciente
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        # Extraer la respuesta
        assistant_message = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        return {
            "response": assistant_message,
            "tokens_used": tokens_used,
            "rag_enabled": False
        }

    except anthropic.APIError as e:
        # Si el modelo no existe, intentar con claude-3-sonnet
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages
            )

            assistant_message = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            return {
                "response": assistant_message,
                "tokens_used": tokens_used
            }
        except Exception as fallback_error:
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

@app.post("/api/feedback")
async def save_feedback(request: dict):
    """
    Guarda feedback de usuarios sobre respuestas del chatbot.

    Acepta:
    {
        "message_id": "string",
        "user_question": "string",
        "ai_response": "string",
        "feedback": "helpful" | "not_helpful",
        "correction": "string" (optional),
        "timestamp": "string"
    }
    """
    import json
    from pathlib import Path
    from datetime import datetime

    # Por ahora guardamos en archivo JSON (en producción usarías una base de datos)
    feedbacks_file = Path("feedbacks.json")

    # Leer feedbacks existentes
    if feedbacks_file.exists():
        with open(feedbacks_file, 'r', encoding='utf-8') as f:
            try:
                feedbacks = json.load(f)
            except json.JSONDecodeError:
                feedbacks = []
    else:
        feedbacks = []

    # Agregar nuevo feedback
    feedback_data = {
        "message_id": request.get("message_id"),
        "user_question": request.get("user_question"),
        "ai_response": request.get("ai_response"),
        "feedback": request.get("feedback"),
        "correction": request.get("correction"),
        "timestamp": request.get("timestamp", datetime.now().isoformat())
    }

    feedbacks.append(feedback_data)

    # Guardar
    with open(feedbacks_file, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)

    print(f"\n📊 Nuevo feedback recibido: {feedback_data['feedback']}")
    if feedback_data['correction']:
        print(f"   Corrección: {feedback_data['correction'][:100]}...")

    return {
        "success": True,
        "message": "Feedback guardado correctamente"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Iniciando LEIA Backend...")
    print("📍 API: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
