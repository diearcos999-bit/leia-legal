# LEIA - Instrucciones para Claude Code

## MCPs Disponibles

### Context7 (Documentacion Actualizada)
Proporciona documentacion actualizada de librerias. Usar cuando necesites informacion sobre APIs recientes.

**Uso:**
```
use context7
Muestra la documentacion de FastAPI para dependency injection
```

**Librerias soportadas:** FastAPI, Next.js 14, React, LangChain, LangGraph, Playwright, Tailwind CSS, Anthropic SDK, y 1000+ mas.

### Next Devtools
Acceso a errores de build, runtime y tipos de Next.js. Se activa automaticamente al trabajar con el frontend.

### Playwright
Testing E2E y automatizacion de browser. Util para debugging del scraper de PJUD.

---

## Stack del Proyecto

### Frontend (`/frontend`)
- **Framework:** Next.js 14.2.0 (App Router)
- **UI:** React 18.3 + TypeScript 5
- **Styling:** Tailwind CSS 3.4 + Radix UI
- **State:** Zustand + React Query
- **Forms:** React Hook Form + Zod
- **Testing:** Jest + Playwright

### Backend (`/backend`)
- **Framework:** FastAPI 0.110+
- **Runtime:** Python 3.11 + Uvicorn
- **ORM:** SQLAlchemy 2.0
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **IA:** Anthropic Claude SDK 0.41+
- **Agentes:** LangChain + LangGraph
- **RAG:** OpenAI Embeddings + Pinecone
- **Scraping:** Playwright (PJUD)

---

## Comandos de Desarrollo

### Frontend
```bash
cd frontend
npm run dev          # Servidor de desarrollo (puerto 3000)
npm run build        # Build de produccion
npm run test         # Tests unitarios
npm run test:e2e     # Tests E2E con Playwright
npm run lint         # Linting
```

### Backend
```bash
cd backend
source venv/bin/activate
python main_simple.py           # Servidor simplificado (puerto 8000)
uvicorn main:app --reload       # Servidor completo con hot reload
pytest                          # Tests
```

---

## Estructura de Carpetas

```
leia/
├── frontend/              # Next.js App
│   ├── app/              # App Router pages
│   ├── components/       # React components
│   └── lib/              # Utilities
├── backend/              # FastAPI Server
│   ├── routers/          # API endpoints
│   ├── agents/           # IA agents (LangGraph)
│   ├── rag/              # RAG system
│   ├── services/         # Business logic
│   └── data/             # Data files
└── docs/                 # Documentacion de negocio
    ├── business/         # Analisis de mercado
    ├── technical/        # Arquitectura
    └── presentations/    # Pitch deck
```

---

## APIs Externas

| API | Variable de Entorno | Uso |
|-----|-------------------|-----|
| Anthropic Claude | `ANTHROPIC_API_KEY` | Chatbot LEIA, agentes IA |
| OpenAI | `OPENAI_API_KEY` | Embeddings para RAG |
| Pinecone | `PINECONE_API_KEY` | Vector database |

---

## Notas Importantes

1. **PJUD Scraper:** El archivo `/backend/services/pjud_scraper.py` usa Playwright para scraping del Poder Judicial. Requiere autenticacion con ClaveUnica.

2. **Base de Datos:** SQLite en desarrollo (`leia.db`), PostgreSQL en produccion.

3. **Rate Limiting:** Los endpoints tienen limite de tasa con slowapi.

4. **Autenticacion:** JWT con expiracion de 7 dias.
