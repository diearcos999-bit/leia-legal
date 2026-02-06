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

# Importar prompts de LEIA
try:
    from prompts.leia_system_prompt import build_system_prompt, LEIA_SYSTEM_PROMPT
    USE_LEIA_PROMPTS = True
except ImportError:
    USE_LEIA_PROMPTS = False

# Importar base de datos y routers extendidos
try:
    from database import engine, Base, get_db
    from routers import chat_v2, lawyers_extended, auth, pjud, notifications, cases, direct_chat, categories, oauth
    EXTENDED_ROUTERS = True
except ImportError as e:
    print(f"ℹ️  Routers extendidos no disponibles: {e}")
    EXTENDED_ROUTERS = False

# Intentar cargar RAG Engine
try:
    from rag.rag_engine import create_rag_engine
    rag_engine = create_rag_engine()
    RAG_ENABLED = rag_engine is not None
    if RAG_ENABLED:
        print("✅ RAG HABILITADO - Usando apuntes de Pinecone")
    else:
        print("⚠️ RAG engine creado pero es None")
except Exception as e:
    import traceback
    print(f"ℹ️  RAG no disponible: {e}")
    print(f"   Traceback: {traceback.format_exc()}")
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

# Incluir routers extendidos si están disponibles
if EXTENDED_ROUTERS:
    app.include_router(auth.router)
    app.include_router(oauth.router)
    app.include_router(chat_v2.router)
    app.include_router(lawyers_extended.router)
    app.include_router(pjud.router)
    app.include_router(notifications.router)
    app.include_router(cases.router)
    app.include_router(direct_chat.router)
    app.include_router(categories.router)
    print("✅ Routers cargados (auth, oauth, chat_v2, lawyers_extended, pjud, notifications, cases, direct_chat, categories)")

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
if USE_LEIA_PROMPTS:
    SYSTEM_PROMPT = LEIA_SYSTEM_PROMPT
    print("✅ Usando prompts mejorados de LEIA")
else:
    SYSTEM_PROMPT = """Eres LEIA, un asistente legal especializado en leyes chilenas. Tu misión es orientar y educar sobre temas legales.

- Proporciona orientación legal general en lenguaje simple
- Especializada en derecho chileno
- SIEMPRE recomienda consultar con un abogado para casos específicos
- Cuando no tengas información completa, responde lo que puedas y haz preguntas
- Deriva a un abogado cuando el caso lo requiera"""

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
        "rag_engine_exists": rag_engine is not None,
        "message": "Backend is running" if ANTHROPIC_API_KEY else "Configure ANTHROPIC_API_KEY in .env"
    }

@app.get("/debug/rag")
async def debug_rag():
    """Endpoint temporal de debug para RAG"""
    return {
        "RAG_ENABLED": RAG_ENABLED,
        "rag_engine": str(rag_engine),
        "rag_engine_type": type(rag_engine).__name__ if rag_engine else None,
        "has_vector_store": hasattr(rag_engine, 'vector_store') and rag_engine.vector_store is not None if rag_engine else False
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
        print(f"🔍 DEBUG: RAG_ENABLED={RAG_ENABLED}, rag_engine={rag_engine}")
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

# Importar utilidades de feriados
try:
    from utils.feriados_chile import (
        calcular_plazo_dias_habiles,
        listar_feriados_año,
        es_feriado,
        es_dia_habil_judicial
    )
    from datetime import date
    FERIADOS_DISPONIBLE = True
    print("✅ Módulo de feriados chilenos cargado")
except ImportError as e:
    print(f"⚠️ Módulo de feriados no disponible: {e}")
    FERIADOS_DISPONIBLE = False


@app.post("/api/calcular-plazo")
async def calcular_plazo(request: dict):
    """
    Calcula el vencimiento de un plazo legal.

    Acepta:
    {
        "fecha_inicio": "2026-02-05",
        "dias": 10,
        "tipo": "judicial_civil" | "corridos"
    }

    Retorna:
    {
        "fecha_vencimiento": "2026-02-17",
        "fecha_inicio": "2026-02-05",
        "dias": 10,
        "tipo": "judicial_civil",
        "detalle": [...]
    }
    """
    if not FERIADOS_DISPONIBLE:
        raise HTTPException(status_code=500, detail="Módulo de feriados no disponible")

    try:
        fecha_str = request.get("fecha_inicio")
        dias = request.get("dias", 10)
        tipo = request.get("tipo", "judicial_civil")

        # Parsear fecha
        partes = fecha_str.split("-")
        fecha_inicio = date(int(partes[0]), int(partes[1]), int(partes[2]))

        resultado = calcular_plazo_dias_habiles(fecha_inicio, dias, tipo)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculando plazo: {str(e)}")


@app.get("/api/feriados/{year}")
async def obtener_feriados(year: int):
    """
    Obtiene los feriados de Chile para un año específico.
    """
    if not FERIADOS_DISPONIBLE:
        raise HTTPException(status_code=500, detail="Módulo de feriados no disponible")

    try:
        feriados = listar_feriados_año(year)
        return {
            "year": year,
            "total": len(feriados),
            "feriados": feriados
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error obteniendo feriados: {str(e)}")


@app.get("/api/es-habil/{fecha}")
async def verificar_dia_habil(fecha: str):
    """
    Verifica si una fecha es día hábil judicial en Chile.

    Formato fecha: YYYY-MM-DD
    """
    if not FERIADOS_DISPONIBLE:
        raise HTTPException(status_code=500, detail="Módulo de feriados no disponible")

    try:
        partes = fecha.split("-")
        fecha_obj = date(int(partes[0]), int(partes[1]), int(partes[2]))

        es_habil = es_dia_habil_judicial(fecha_obj)
        es_fer = es_feriado(fecha_obj)
        dia_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][fecha_obj.weekday()]

        return {
            "fecha": fecha,
            "dia_semana": dia_semana,
            "es_habil_judicial": es_habil,
            "es_feriado": es_fer,
            "razon_no_habil": None if es_habil else ("feriado" if es_fer else "domingo")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verificando fecha: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Iniciando LEIA Backend...")
    print("📍 API: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
