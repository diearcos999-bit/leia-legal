# LEIA - Arquitectura Completa del Sistema

## Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Flujo UX Completo](#flujo-ux-completo)
4. [Reglas Anti-Alucinación](#reglas-anti-alucinación)
5. [Modelo de Datos](#modelo-de-datos)
6. [Endpoints API](#endpoints-api)
7. [Escalabilidad](#escalabilidad)

---

## Resumen Ejecutivo

LEIA es una plataforma LegalTech chilena que combina:
- **Asistente IA** basado en apuntes personales (RAG)
- **Motor de triage** anti-alucinación
- **Marketplace de abogados** con precios transparentes
- **Sistema de transferencia** de casos

### Principios Fundamentales

1. **Honestidad absoluta**: Solo responder con información de los apuntes
2. **Citación obligatoria**: Siempre mencionar la fuente
3. **Derivación inteligente**: Saber cuándo conectar con abogados
4. **Consentimiento explícito**: El usuario controla qué comparte

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js 14)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │    Chat     │  │  Abogados   │  │   Casos     │              │
│  │  Interface  │  │ Marketplace │  │  Dashboard  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   CAPA DE CHAT                           │    │
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────────────┐  │    │
│  │  │   RAG   │─▶│   TRIAGE    │─▶│  RESPUESTA/DERIVAR  │  │    │
│  │  │ Engine  │  │   Engine    │  │                     │  │    │
│  │  └─────────┘  └─────────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   CAPA DE CASOS                          │    │
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────────────┐  │    │
│  │  │ Crear   │─▶│ Generar     │─▶│  Transferir a       │  │    │
│  │  │ Caso    │  │ Resumen IA  │  │  Abogado            │  │    │
│  │  └─────────┘  └─────────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   CAPA DE ABOGADOS                       │    │
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────────────┐  │    │
│  │  │ Búsqueda│  │  Matching   │  │  Reseñas/Métricas   │  │    │
│  │  │ Filtros │  │ Inteligente │  │                     │  │    │
│  │  └─────────┘  └─────────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │   Claude    │ │  Pinecone   │ │  PostgreSQL │
      │   (LLM)     │ │  (Vectores) │ │    (BD)     │
      └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Flujo UX Completo

### Fase 1: Consulta Inicial

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USUARIO LLEGA A LEIA                                        │
│     └─▶ Landing page con chat prominente                        │
│                                                                  │
│  2. ESCRIBE SU CONSULTA                                         │
│     └─▶ "Me despidieron hace 2 meses sin pagar finiquito"       │
│                                                                  │
│  3. SISTEMA PROCESA                                             │
│     ├─▶ RAG busca en apuntes (similarity >= 0.75)               │
│     ├─▶ Triage evalúa: urgencia, sensibilidad, info disponible  │
│     └─▶ Decide: RESPONDER | NO_INFO | DERIVAR                   │
│                                                                  │
│  4. LEIA RESPONDE                                               │
│     ├─▶ Con fuentes citadas si hay info                         │
│     ├─▶ Honestamente si no hay info                             │
│     └─▶ Ofreciendo derivación si corresponde                    │
└─────────────────────────────────────────────────────────────────┘
```

### Fase 2: Derivación a Abogado

```
┌─────────────────────────────────────────────────────────────────┐
│  5. USUARIO ACEPTA DERIVACIÓN                                   │
│     └─▶ Click en "Ver abogados disponibles"                     │
│                                                                  │
│  6. SISTEMA MUESTRA ABOGADOS                                    │
│     └─▶ Filtrados por:                                          │
│         ├─ Área legal detectada (ej: Laboral)                   │
│         ├─ Región/Ciudad del usuario                            │
│         ├─ Rating y reputación                                  │
│         └─ Rango de precios                                     │
│                                                                  │
│  7. USUARIO VE PERFIL DE ABOGADO                                │
│     └─▶ Información visible:                                    │
│         ├─ Nombre, foto, verificación                           │
│         ├─ Especialidades, experiencia                          │
│         ├─ Rating + reseñas                                     │
│         ├─ PRECIOS CLAROS:                                      │
│         │   ├─ Consulta inicial: $30.000 (30 min)               │
│         │   ├─ Hora adicional: $50.000                          │
│         │   └─ Servicios específicos                            │
│         └─ Tiempo promedio de respuesta                         │
│                                                                  │
│  8. USUARIO SELECCIONA ABOGADO                                  │
│     └─▶ Click en "Consultar con este abogado"                   │
└─────────────────────────────────────────────────────────────────┘
```

### Fase 3: Transferencia de Caso

```
┌─────────────────────────────────────────────────────────────────┐
│  9. SISTEMA GENERA RESUMEN DEL CASO                             │
│     └─▶ Automáticamente con IA:                                 │
│         ├─ Hechos principales                                   │
│         ├─ Fechas relevantes                                    │
│         ├─ Área legal                                           │
│         ├─ Factores de riesgo                                   │
│         └─ Preguntas pendientes                                 │
│                                                                  │
│  10. USUARIO DA CONSENTIMIENTO                                  │
│      └─▶ Checkboxes obligatorios:                               │
│          ☐ Autorizo compartir el historial de chat              │
│          ☐ Autorizo compartir mis datos de contacto             │
│          ☐ Autorizo transferir mi caso al abogado               │
│          ☐ (Opcional) Autorizo compartir documentos             │
│                                                                  │
│  11. CASO SE TRANSFIERE                                         │
│      └─▶ El abogado recibe:                                     │
│          ├─ Número de caso (LEIA-2025-00001)                    │
│          ├─ Resumen estructurado                                │
│          ├─ Chat completo                                       │
│          ├─ Datos de contacto del usuario                       │
│          └─ Documentos (si autorizó)                            │
└─────────────────────────────────────────────────────────────────┘
```

### Fase 4: Seguimiento

```
┌─────────────────────────────────────────────────────────────────┐
│  12. ABOGADO RESPONDE                                           │
│      └─▶ Dentro de LEIA o contacto directo                      │
│                                                                  │
│  13. USUARIO VE ESTADO                                          │
│      └─▶ Dashboard con:                                         │
│          ├─ Estado del caso                                     │
│          ├─ Mensajes del abogado                                │
│          └─ Timeline de eventos                                 │
│                                                                  │
│  14. CASO SE COMPLETA                                           │
│      └─▶ Usuario puede:                                         │
│          ├─ Dejar reseña (1-5 estrellas + comentario)           │
│          └─ Recomendar abogado                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Reglas Anti-Alucinación

### Umbral de Similitud

```python
SIMILARITY_THRESHOLD = 0.75  # Mínimo para considerar info relevante
MIN_SOURCES = 2              # Ideal para respuesta confiable
```

### Matriz de Decisiones

| Score RAG | Fuentes | Urgencia | Decisión |
|-----------|---------|----------|----------|
| >= 0.75   | >= 2    | Baja     | RESPONDER con citas |
| >= 0.75   | 1       | Baja     | RESPONDER + disclaimer |
| 0.50-0.74 | -       | -        | NO_INFO + derivar |
| < 0.50    | -       | -        | NO_INFO + derivar |
| -         | -       | Alta     | DERIVAR inmediato |
| -         | -       | Penal    | DERIVAR siempre |

### Palabras Clave de Urgencia

```python
URGENT_KEYWORDS = [
    "urgente", "emergencia", "plazo vence",
    "detención", "detenido", "violencia",
    "desahucio", "embargo", "remate"
]
```

### Temas Sensibles (Siempre Derivar)

```python
SENSITIVE_TOPICS = [
    # Penal
    "delito", "imputado", "querella criminal",
    "violación", "homicidio",
    # Familia sensible
    "violencia intrafamiliar", "maltrato",
    # Laboral grave
    "acoso laboral", "acoso sexual"
]
```

---

## Modelo de Datos

### Diagrama ER Simplificado

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │────▶│   Case      │────▶│  Consent    │
│             │     │             │     │             │
│ - email     │     │ - number    │     │ - type      │
│ - role      │     │ - status    │     │ - granted   │
│ - verified  │     │ - legal_area│     │ - timestamp │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │
      │                   ▼
      │             ┌─────────────┐
      │             │CaseTransfer │
      │             │             │
      │             │ - status    │
      │             │ - message   │
      │             └─────────────┘
      │                   │
      ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Lawyer    │◀────│             │────▶│   Review    │
│             │     │             │     │             │
│ - name      │     │             │     │ - rating    │
│ - specialty │     │             │     │ - content   │
│ - verified  │     │             │     │ - approved  │
│ - rating    │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
      │
      ▼
┌─────────────┐
│LawyerService│
│             │
│ - name      │
│ - price     │
│ - type      │
└─────────────┘
```

### Entidades Principales

| Entidad | Propósito |
|---------|-----------|
| User | Usuarios del sistema |
| Lawyer | Perfiles de abogados |
| LawyerService | Servicios con precios |
| Case | Casos legales |
| CaseTransfer | Transferencias a abogados |
| Consent | Consentimientos del usuario |
| Review | Reseñas de abogados |
| LawyerMetrics | Métricas de rendimiento |

---

## Endpoints API

### Chat V2 (Nuevo)

```
POST /api/v2/chat
├─ Request: { message, conversation_history }
└─ Response: { response, sources, has_sufficient_info, referral }

POST /api/v2/chat/suggest-lawyers
├─ Request: { message, legal_area?, region? }
└─ Response: { detected_area, lawyers[] }

POST /api/v2/chat/create-case
├─ Request: { conversation_id }
└─ Response: { case_id, case_number, summary }
```

### Casos

```
POST   /api/cases              → Crear caso
GET    /api/cases              → Listar mis casos
GET    /api/cases/{id}         → Detalle de caso
PUT    /api/cases/{id}         → Actualizar caso
POST   /api/cases/{id}/summary → Generar resumen IA
POST   /api/cases/{id}/consent → Otorgar consentimiento
POST   /api/cases/{id}/transfer → Transferir a abogado
GET    /api/cases/{id}/timeline → Ver eventos
```

### Abogados (Extendido)

```
GET    /api/lawyers/search     → Búsqueda avanzada
POST   /api/lawyers/match      → Matching inteligente
GET    /api/lawyers/{id}/full  → Perfil completo
GET    /api/lawyers/{id}/services → Servicios y precios
GET    /api/lawyers/{id}/reviews → Reseñas
POST   /api/lawyers/{id}/reviews → Crear reseña
```

---

## Escalabilidad

### Fase Actual (MVP)

```
┌─────────────────────────────────────────────────────┐
│  ACTUAL                                             │
│  ├─ SQLite/PostgreSQL                               │
│  ├─ Pinecone Free (100K vectores)                   │
│  ├─ Claude Sonnet (pay-per-use)                     │
│  └─ Servidor único                                  │
└─────────────────────────────────────────────────────┘
```

### Fase 2: Crecimiento (1,000+ usuarios)

```
┌─────────────────────────────────────────────────────┐
│  CRECIMIENTO                                        │
│  ├─ PostgreSQL managed (Railway/Supabase)           │
│  ├─ Pinecone Standard (1M vectores)                 │
│  ├─ Redis para caché de sesiones                    │
│  ├─ Celery para tareas async (resúmenes, emails)    │
│  └─ Load balancer + 2 instancias                    │
└─────────────────────────────────────────────────────┘
```

### Fase 3: Escala (10,000+ usuarios)

```
┌─────────────────────────────────────────────────────┐
│  ESCALA                                             │
│  ├─ PostgreSQL cluster (read replicas)              │
│  ├─ Pinecone Enterprise                             │
│  ├─ Redis cluster                                   │
│  ├─ Kubernetes (auto-scaling)                       │
│  ├─ CDN para assets                                 │
│  └─ Monitoring (Datadog/Sentry)                     │
└─────────────────────────────────────────────────────┘
```

### Agregando Más Fuentes RAG

Para agregar corpus legal oficial en el futuro:

```python
# 1. Crear índice separado
rag_apuntes = RAGEngine(index="leia-apuntes")      # Tus apuntes
rag_legal = RAGEngine(index="leia-corpus-legal")    # Corpus oficial

# 2. Modificar búsqueda
def retrieve_context(query):
    # Buscar en apuntes primero
    results_apuntes = rag_apuntes.search(query)

    # Si no hay suficiente, buscar en corpus legal
    if not results_apuntes or results_apuntes[0].score < 0.75:
        results_legal = rag_legal.search(query)
        return results_apuntes + results_legal

    return results_apuntes

# 3. Diferenciar en respuesta
# "Según mis apuntes..." vs "Según el Código del Trabajo..."
```

### Agregando Notificaciones

```python
# Backend
from celery import Celery

celery = Celery('leia')

@celery.task
def notify_lawyer_new_case(case_id, lawyer_id):
    # Email
    send_email(lawyer.email, template="new_case", case=case)
    # Push (si hay app móvil)
    send_push(lawyer.user_id, message=f"Nuevo caso: {case.number}")
    # WebSocket (si está conectado)
    emit_to_user(lawyer.user_id, event="new_case", data=case)
```

---

## Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| `services/triage_engine.py` | Motor anti-alucinación |
| `models_extended.py` | Modelos de casos, transferencias, reseñas |
| `routers/cases.py` | Endpoints de gestión de casos |
| `routers/lawyers_extended.py` | Endpoints de abogados con precios |
| `routers/chat_v2.py` | Chat mejorado con triage |
| `prompts/leia_system_prompt.py` | Prompts del asistente |

---

## Próximos Pasos de Implementación

### Inmediato (Esta Semana)

1. **Crear tablas nuevas**
   ```bash
   cd backend
   python -c "from models_extended import *; from database import engine, Base; Base.metadata.create_all(engine)"
   ```

2. **Registrar routers en main.py**
   ```python
   from routers import cases, lawyers_extended, chat_v2
   app.include_router(cases.router)
   app.include_router(lawyers_extended.router)
   app.include_router(chat_v2.router)
   ```

3. **Subir apuntes a Pinecone**
   - Procesar PDFs/Word con embeddings
   - Incluir metadata (source, section, page)

### Corto Plazo (2 Semanas)

4. **Frontend de casos**
   - Pantalla de creación de caso
   - Flujo de consentimiento
   - Selección de abogado

5. **Frontend de abogados**
   - Perfiles con precios
   - Filtros de búsqueda
   - Sistema de reseñas

### Mediano Plazo (1 Mes)

6. **Dashboard de abogado**
   - Ver casos recibidos
   - Responder a usuarios
   - Gestionar servicios/precios

7. **Notificaciones**
   - Emails transaccionales
   - Alertas en plataforma

---

**Documento creado para LEIA - leia.cl**
**Fecha: Febrero 2025**
