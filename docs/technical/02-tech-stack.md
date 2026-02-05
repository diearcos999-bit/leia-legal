# Tech Stack Detallado - JusticiaAI

## 1. Frontend Stack

### 1.1 Web Application

#### Core Framework
```json
{
  "framework": "Next.js 14.2+",
  "reason": "SSR para SEO, App Router, React Server Components",
  "language": "TypeScript 5.0+",
  "runtime": "Node.js 20 LTS"
}
```

#### UI & Styling
```json
{
  "css": "Tailwind CSS 3.4+",
  "components": "shadcn/ui + Radix UI",
  "icons": "Lucide React",
  "animations": "Framer Motion",
  "fonts": "next/font (Google Fonts)",
  "reason": "Componentes accesibles, customizables, performantes"
}
```

#### State Management
```json
{
  "server-state": "TanStack Query (React Query) v5",
  "client-state": "Zustand",
  "forms": "React Hook Form + Zod",
  "reason": "Separación clara server/client state, type-safety"
}
```

#### Utilities
```json
{
  "http-client": "Axios",
  "date": "date-fns",
  "validation": "Zod",
  "utils": "clsx + tw-merge (cn utility)",
  "tables": "TanStack Table v8",
  "charts": "Recharts"
}
```

#### Testing
```json
{
  "unit": "Jest + React Testing Library",
  "e2e": "Playwright",
  "visual": "Chromatic (Storybook)",
  "coverage": "NYC/Istanbul"
}
```

### 1.2 Mobile Application

#### Core Framework
```json
{
  "framework": "React Native 0.73+",
  "tooling": "Expo SDK 50+",
  "language": "TypeScript",
  "reason": "Code sharing 90%+, OTA updates, mejor DX"
}
```

#### Libraries Nativas
```json
{
  "navigation": "React Navigation v6",
  "storage": "AsyncStorage + MMKV",
  "networking": "Axios + React Query",
  "push-notifications": "Expo Notifications",
  "camera": "Expo Camera",
  "biometrics": "Expo Local Authentication",
  "file-system": "Expo File System"
}
```

#### State & Forms
```json
{
  "state": "Zustand",
  "forms": "React Hook Form",
  "validation": "Zod"
}
```

### 1.3 Admin Dashboard

#### Core
```json
{
  "framework": "React 18 + Vite",
  "ui": "Ant Design / Material-UI",
  "routing": "React Router v6",
  "reason": "Admin-specific components out-of-the-box"
}
```

## 2. Backend Stack

### 2.1 API Services (Node.js)

#### Framework
```json
{
  "framework": "Express.js 4.18+",
  "language": "TypeScript",
  "runtime": "Node.js 20 LTS",
  "reason": "Maduro, ecosistema rico, performance adecuado"
}
```

#### Core Libraries
```json
{
  "validation": "Joi / Zod",
  "orm": "Prisma (TypeScript-first ORM)",
  "auth": "jsonwebtoken + bcrypt",
  "cors": "cors",
  "compression": "compression",
  "helmet": "helmet (security headers)",
  "rate-limiting": "express-rate-limit",
  "logging": "Winston + Morgan"
}
```

#### Testing
```json
{
  "unit": "Jest",
  "integration": "Supertest",
  "mocks": "nock",
  "factories": "Fishery"
}
```

### 2.2 AI/ML Services (Python)

#### Framework
```json
{
  "framework": "FastAPI 0.110+",
  "language": "Python 3.11+",
  "reason": "Async, type hints, auto-docs, fast"
}
```

#### AI/ML Libraries
```json
{
  "llm-sdk": "openai / anthropic",
  "embeddings": "sentence-transformers",
  "vector-search": "pinecone-client",
  "nlp": "spaCy (español)",
  "pdf": "PyPDF2 / pdfplumber",
  "docx": "python-docx",
  "templating": "Jinja2",
  "pdf-generation": "WeasyPrint / ReportLab"
}
```

#### Utilities
```json
{
  "validation": "Pydantic V2",
  "async": "asyncio + aiohttp",
  "celery": "Celery (background jobs)",
  "testing": "pytest + pytest-asyncio"
}
```

### 2.3 Integration/Scraping Services

#### Tools
```json
{
  "browser-automation": "Playwright (Python)",
  "alternative": "Selenium",
  "http": "aiohttp + requests",
  "html-parsing": "BeautifulSoup4 + lxml",
  "scheduling": "APScheduler",
  "reason": "OJV scraping legal robusto"
}
```

## 3. Database Stack

### 3.1 PostgreSQL

#### Version & Hosting
```json
{
  "version": "PostgreSQL 15+",
  "hosting": "AWS RDS",
  "connection-pooling": "PgBouncer",
  "orm": "Prisma (Node) / SQLAlchemy (Python)"
}
```

#### Extensions
```json
{
  "extensions": [
    "pg_trgm (fuzzy search)",
    "uuid-ossp (UUIDs)",
    "pgcrypto (encryption)",
    "pg_stat_statements (query analysis)"
  ]
}
```

#### Backup & HA
```json
{
  "backups": "Automated daily (AWS RDS)",
  "replication": "Multi-AZ (sync)",
  "read-replicas": "Yes (async)",
  "retention": "30 days"
}
```

### 3.2 MongoDB

#### Version & Hosting
```json
{
  "version": "MongoDB 7.0+",
  "hosting": "MongoDB Atlas",
  "driver": "mongoose (Node) / Motor (Python async)"
}
```

#### Features
```json
{
  "features": [
    "Flexible schema",
    "Full-text search",
    "Aggregation pipeline",
    "Change streams (real-time)"
  ]
}
```

### 3.3 Redis

#### Version & Hosting
```json
{
  "version": "Redis 7.2+",
  "hosting": "AWS ElastiCache",
  "client": "ioredis (Node) / redis-py (Python)"
}
```

#### Use Cases
```json
{
  "use-cases": [
    "Session store",
    "API cache",
    "Rate limiting",
    "Job queues (Bull)",
    "Real-time pub/sub"
  ]
}
```

### 3.4 Pinecone (Vector Database)

#### Config
```json
{
  "service": "Pinecone Managed",
  "index-type": "s1 (standard)",
  "dimensions": 1536,
  "metric": "cosine",
  "reason": "Semantic search para RAG en IA legal"
}
```

### 3.5 S3 (Object Storage)

#### Config
```json
{
  "provider": "AWS S3",
  "sdk": "aws-sdk-js v3 / boto3",
  "features": [
    "Versioning enabled",
    "Encryption (AES-256)",
    "Lifecycle policies",
    "CloudFront integration"
  ]
}
```

## 4. Infrastructure Stack

### 4.1 Cloud Provider: AWS

#### Compute
```json
{
  "containers": "ECS Fargate / EKS (Kubernetes)",
  "serverless": "Lambda (para tareas específicas)",
  "reason": "Escala automática, pay-per-use"
}
```

#### Networking
```json
{
  "vpc": "Custom VPC con subnets privadas/públicas",
  "load-balancer": "Application Load Balancer (ALB)",
  "cdn": "CloudFront",
  "dns": "Route 53",
  "waf": "AWS WAF + CloudFlare"
}
```

#### Storage & Database
```json
{
  "rds": "PostgreSQL Multi-AZ",
  "elasticache": "Redis Cluster",
  "s3": "Multiple buckets por environment",
  "efs": "Elastic File System (si necesario)"
}
```

#### Security & Monitoring
```json
{
  "secrets": "AWS Secrets Manager",
  "kms": "Key Management Service",
  "iam": "Fine-grained roles",
  "cloudwatch": "Logs & Metrics",
  "cloudtrail": "Audit trail"
}
```

### 4.2 Container Orchestration

#### Development
```json
{
  "tool": "Docker Compose",
  "purpose": "Local development environment",
  "services": "All microservices + databases"
}
```

#### Production
```json
{
  "orchestrator": "Kubernetes (AWS EKS)",
  "alternative": "ECS Fargate (si team pequeño)",
  "service-mesh": "Istio (futuro, si necesario)",
  "helm": "Para package management"
}
```

### 4.3 CI/CD

#### Pipeline
```json
{
  "ci": "GitHub Actions",
  "cd": "ArgoCD / Flux (GitOps)",
  "registry": "AWS ECR (Docker images)",
  "environments": ["dev", "staging", "production"]
}
```

#### Stages
```json
{
  "stages": [
    "Lint & Format (ESLint, Prettier, Black)",
    "Unit Tests (Jest, pytest)",
    "Build Docker Images",
    "Security Scan (Snyk, Trivy)",
    "Push to ECR",
    "Deploy to Staging",
    "E2E Tests (Playwright)",
    "Deploy to Production (manual approval)"
  ]
}
```

### 4.4 Monitoring & Observability

#### APM (Application Performance Monitoring)
```json
{
  "tool": "Datadog / New Relic",
  "metrics": "Custom + infrastructure",
  "traces": "Distributed tracing",
  "profiling": "Production profiling"
}
```

#### Error Tracking
```json
{
  "tool": "Sentry",
  "integrations": ["Frontend", "Backend", "Mobile"],
  "alerts": "Slack + PagerDuty"
}
```

#### Logging
```json
{
  "stack": "ELK (Elasticsearch, Logstash, Kibana)",
  "alternative": "AWS CloudWatch Insights",
  "format": "JSON structured logs",
  "retention": "90 days"
}
```

#### Metrics
```json
{
  "tool": "Prometheus + Grafana",
  "exporters": ["Node exporter", "Postgres exporter", "Custom app metrics"],
  "alerting": "Alertmanager → PagerDuty"
}
```

### 4.5 Security Tools

#### Code Security
```json
{
  "sast": "SonarQube",
  "dependency-scanning": "Snyk / Dependabot",
  "secrets-scanning": "GitGuardian",
  "container-scanning": "Trivy"
}
```

#### Runtime Security
```json
{
  "waf": "CloudFlare + AWS WAF",
  "ddos": "CloudFlare",
  "rate-limiting": "Kong API Gateway",
  "intrusion-detection": "AWS GuardDuty"
}
```

## 5. External Services & APIs

### 5.1 AI & ML
```json
{
  "llm": {
    "primary": "Anthropic Claude 3.5 Sonnet",
    "fallback": "OpenAI GPT-4 Turbo",
    "reason": "Claude mejor para textos largos (legal), GPT-4 como backup"
  },
  "embeddings": {
    "service": "OpenAI text-embedding-3-large",
    "dimensions": 1536
  },
  "vector-db": {
    "service": "Pinecone",
    "alternative": "Weaviate (self-hosted si escala)"
  }
}
```

### 5.2 Payments
```json
{
  "chile": {
    "primary": "Transbank WebPay Plus",
    "alternative": "Flow",
    "subscriptions": "Stripe (si internacional futuro)"
  },
  "fees": {
    "transbank": "~3.5% + $100 CLP",
    "flow": "~3% + IVA"
  }
}
```

### 5.3 Billing & Invoicing
```json
{
  "chile": {
    "sii": "API Facturación Electrónica SII",
    "library": "lib-sii (Node.js)",
    "certificates": "Certificado digital empresa"
  }
}
```

### 5.4 Authentication
```json
{
  "claveunica": {
    "protocol": "OAuth 2.0",
    "provider": "Gobierno de Chile",
    "use-case": "Verificación identidad usuarios chilenos"
  },
  "social": {
    "google": "Google OAuth",
    "linkedin": "LinkedIn OAuth (abogados)"
  }
}
```

### 5.5 Communications

#### Email
```json
{
  "transactional": "SendGrid",
  "alternative": "AWS SES",
  "templates": "MJML + Handlebars",
  "volume": "10K emails/mes (gratis SendGrid)"
}
```

#### SMS & WhatsApp
```json
{
  "provider": "Twilio",
  "sms": "Twilio SMS",
  "whatsapp": "Twilio Business API",
  "cost": "~$0.0075 USD/SMS en Chile"
}
```

#### Push Notifications
```json
{
  "service": "Firebase Cloud Messaging (FCM)",
  "platforms": ["iOS", "Android", "Web"],
  "free": "Yes (sin límites razonables)"
}
```

### 5.6 File Processing
```json
{
  "pdf": {
    "generation": "WeasyPrint / Puppeteer",
    "parsing": "pdfplumber / pdf.js"
  },
  "ocr": {
    "service": "AWS Textract",
    "alternative": "Tesseract (open-source)",
    "use-case": "Escaneo de documentos subidos"
  },
  "signatures": {
    "chile": "Integración con proveedores FEA",
    "providers": ["Mifiel", "DocuSign (internacional)"]
  }
}
```

### 5.7 Analytics & Product

#### Product Analytics
```json
{
  "tool": "Mixpanel",
  "alternative": "Amplitude / PostHog",
  "events": "Custom events + auto-capture",
  "cost": "Free hasta 100K MTUs"
}
```

#### Web Analytics
```json
{
  "tool": "Google Analytics 4",
  "privacy": "Anonymized IPs, cookie consent",
  "alternative": "Plausible (privacy-first)"
}
```

#### A/B Testing
```json
{
  "tool": "Mixpanel Experiments / GrowthBook",
  "integration": "Feature flags + analytics"
}
```

### 5.8 Customer Support
```json
{
  "helpdesk": {
    "tool": "Intercom / Zendesk",
    "features": ["Live chat", "Ticketing", "Knowledge base"],
    "integrations": "CRM + analytics"
  },
  "chatbot": {
    "simple-queries": "Custom chatbot con IA interna",
    "escalation": "A humano via Intercom"
  }
}
```

## 6. Development Tools

### 6.1 Version Control
```json
{
  "vcs": "Git",
  "hosting": "GitHub",
  "workflow": "Git Flow",
  "branch-protection": "Required reviews, CI passing"
}
```

### 6.2 Project Management
```json
{
  "agile": "Jira / Linear",
  "docs": "Notion / Confluence",
  "design": "Figma",
  "api-docs": "Swagger (OpenAPI 3.0)"
}
```

### 6.3 Code Quality

#### Linting & Formatting
```json
{
  "javascript": "ESLint + Prettier",
  "python": "Black + Flake8 + mypy",
  "pre-commit": "Husky + lint-staged",
  "editorconfig": "Yes"
}
```

#### Code Review
```json
{
  "tool": "GitHub Pull Requests",
  "required-reviewers": "1 min (2 para critical)",
  "automated-checks": "CI must pass"
}
```

### 6.4 Local Development

#### Requirements
```json
{
  "required": [
    "Docker Desktop",
    "Node.js 20",
    "Python 3.11",
    "Git"
  ],
  "recommended": [
    "VSCode + extensions",
    "Postman / Insomnia",
    "DBeaver (DB client)"
  ]
}
```

#### Environment Setup
```bash
# 1. Clone repo
git clone https://github.com/justiciaai/platform.git
cd platform

# 2. Install dependencies
npm install              # Frontend
cd backend && npm install # Backend Node services
cd ai-service && pip install -r requirements.txt

# 3. Setup environment variables
cp .env.example .env
# Editar .env con credenciales locales

# 4. Start services
docker-compose up -d     # Databases
npm run dev              # Frontend
cd backend && npm run dev # Backend
cd ai-service && uvicorn main:app --reload # AI service

# 5. Run migrations
npm run prisma:migrate

# 6. Seed database
npm run seed
```

## 7. Costs Breakdown (Monthly, Año 2)

### Development & Tools
```json
{
  "github": "$21 (Team)",
  "figma": "$45 (3 designers)",
  "notion": "$10 (Team)",
  "sentry": "$26 (Team)",
  "total": "$102"
}
```

### Infrastructure (AWS)
```json
{
  "compute": "$500 (ECS Fargate / EC2)",
  "rds": "$200 (db.t3.medium Multi-AZ)",
  "elasticache": "$50 (cache.t3.micro)",
  "s3-cloudfront": "$100",
  "data-transfer": "$150",
  "other": "$100",
  "total": "$1,100"
}
```

### External APIs
```json
{
  "openai-anthropic": "$1,000 (80K requests/mes)",
  "pinecone": "$70 (Starter plan)",
  "sendgrid": "$20 (50K emails)",
  "twilio": "$100 (SMS/WhatsApp)",
  "transbank-flow": "$0 (pay-per-transaction)",
  "total": "$1,190"
}
```

### Monitoring & Ops
```json
{
  "datadog": "$31 (Pro, 3 hosts)",
  "pagerduty": "$25 (Starter)",
  "total": "$56"
}
```

### **Total Monthly (Año 2): ~$2,450 USD**

## 8. Technology Decision Rationale

### Why Next.js?
- SSR crítico para SEO (landing pages)
- App Router con React Server Components (futuro-proof)
- Vercel edge functions (performance)
- Mejor DX y velocidad de desarrollo

### Why TypeScript Everywhere?
- Type safety reduce bugs 15%+
- Better tooling (autocomplete, refactoring)
- Self-documenting code
- Industry standard

### Why Microservices (eventually)?
- Escalabilidad independiente de servicios
- Aislamiento de fallos
- Teams pueden trabajar paralelamente
- **Pero**: Empezar con monolito para velocidad

### Why PostgreSQL + MongoDB?
- PostgreSQL: ACID para transacciones críticas
- MongoDB: Flexibilidad para documentos legales
- No forzar todo en un paradigma

### Why AWS over GCP/Azure?
- Mejor presencia LATAM (São Paulo)
- Ecosistema más maduro
- Más opciones de servicios
- Mejor compliance/certificaciones

### Why Anthropic Claude for AI?
- Mejor manejo de contextos largos (documentos legales)
- Menos alucinaciones que GPT-4 en pruebas
- API más simple
- Antropología enfocada en safety

## 9. Future Tech Considerations

### When to Build vs Buy

**Build**:
- Core IP (algoritmo matching, IA fine-tuned)
- Diferenciadores competitivos

**Buy/Use SaaS**:
- Commodities (email, SMS, pagos)
- No reinventar rueda

### When to Migrate/Optimize

**AI**:
- Año 1-2: OpenAI/Anthropic APIs
- Año 3+: Si volumen alto, fine-tune open-source models (Llama, Mistral)

**Infrastructure**:
- Año 1: Managed services (RDS, ElastiCache)
- Año 3+: Si costo alto, evaluar self-managed en EC2

**Search**:
- Año 1-2: Pinecone managed
- Año 3+: Si costo alto, Weaviate self-hosted en Kubernetes

---

**Conclusión**: Stack moderno, battle-tested, con balance entre velocidad de desarrollo y escalabilidad futura. Prioriza TypeScript, cloud-native, y servicios managed para minimizar overhead operacional en etapas tempranas.
