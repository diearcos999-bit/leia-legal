# JusticiaAI MVP

Plataforma legaltech que democratiza el acceso a justicia en Chile mediante IA + Marketplace de abogados.

## 🏗️ Arquitectura

```
justiciaai-mvp/
├── frontend/          # Next.js 14 + TypeScript (Web App)
├── backend/           # FastAPI (AI Service + API Gateway)
├── shared/            # Tipos compartidos, utils
├── docs/              # Documentación técnica
└── docker/            # Docker configs para deployment
```

## 🚀 Quick Start

### Prerequisitos

- Node.js 20+ LTS
- Python 3.11+
- PostgreSQL 15+ (o Docker)
- API Key de Anthropic Claude (para IA)

### 1. Frontend (Next.js)

```bash
cd frontend
npm install
cp .env.example .env.local
# Edita .env.local con tus keys
npm run dev
```

Frontend disponible en: http://localhost:3000

### 2. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus keys
uvicorn main:app --reload
```

Backend disponible en: http://localhost:8000
API Docs: http://localhost:8000/docs

### 3. Base de Datos

```bash
cd frontend
npx prisma migrate dev
npx prisma generate
npx prisma studio  # Para explorar la DB visualmente
```

## 🎯 Features del MVP

### ✅ Fase 1 (Semanas 1-2) - CURRENT
- [x] Setup proyecto
- [x] Chatbot IA conversacional
- [x] Landing page
- [ ] Auth básico (email/password)
- [ ] Perfil de usuario

### 🚧 Fase 2 (Semanas 3-4)
- [ ] Marketplace de abogados (listado)
- [ ] Perfil de abogado
- [ ] Sistema de match IA → Abogado
- [ ] Mensajería básica

### 📋 Fase 3 (Semanas 5-6)
- [ ] Pagos (Transbank)
- [ ] Dashboard usuario
- [ ] Dashboard abogado
- [ ] Gestión de casos

## 🔧 Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **UI:** Tailwind CSS + shadcn/ui
- **State:** Zustand + React Query
- **Forms:** React Hook Form + Zod

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11
- **IA:** Anthropic Claude 3.5 Sonnet
- **DB:** PostgreSQL + Prisma
- **Cache:** Redis (opcional)

### Infrastructure
- **Hosting:** Vercel (Frontend) + Railway (Backend)
- **DB:** Supabase / Railway PostgreSQL
- **Storage:** AWS S3 / Cloudflare R2
- **CDN:** Cloudflare

## 📚 Documentación

- [Arquitectura del Sistema](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Guía de Deployment](./docs/deployment.md)
- [Contribuir](./docs/contributing.md)

## 🔐 Variables de Entorno

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@localhost:5432/justiciaai
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

### Backend (.env)
```env
ANTHROPIC_API_KEY=your-anthropic-key
DATABASE_URL=postgresql://user:password@localhost:5432/justiciaai
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

## 🚀 Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel --prod
```

### Railway (Backend)
```bash
cd backend
railway up
```

Ver [Guía de Deployment](./docs/deployment.md) para más detalles.

## 🧪 Testing

### Frontend
```bash
cd frontend
npm test              # Unit tests
npm run test:e2e      # E2E tests (Playwright)
```

### Backend
```bash
cd backend
pytest                # Run all tests
pytest --cov          # With coverage
```

## 📦 Scripts Útiles

```bash
# Desarrollo
npm run dev                    # Start frontend dev server
uvicorn main:app --reload      # Start backend dev server

# Build
npm run build                  # Build frontend para producción
docker-compose build           # Build Docker images

# Base de Datos
npx prisma studio              # Visual DB editor
npx prisma migrate dev         # Run migrations
npx prisma db seed             # Seed data

# Linting
npm run lint                   # Lint frontend
ruff check .                   # Lint backend (Python)
```

## 🤝 Contribuir

1. Fork el repo
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 License

Copyright © 2025 JusticiaAI. All rights reserved.

## 👥 Equipo

- **Roberto Arcos** - Founder & CEO - [@robertoarcos](https://linkedin.com/in/robertoarcos)

## 🔗 Links

- **Landing:** [justiciaai.cl](https://justiciaai.cl)
- **Pitch Deck:** [Ver Deck](../legaltech-chile-project/presentations/)
- **Docs:** [Documentación Completa](./docs/)

---

**🚀 Built with ❤️ in Chile**
