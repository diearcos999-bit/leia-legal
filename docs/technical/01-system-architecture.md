# Arquitectura del Sistema - JusticiaAI

## 1. Resumen Ejecutivo

JusticiaAI se construye sobre una **arquitectura de microservicios cloud-native** diseñada para:
- **Escalabilidad**: Soportar crecimiento de 100 a 100,000+ usuarios
- **Confiabilidad**: 99.9% uptime SLA
- **Seguridad**: Cumplimiento Ley 21.719, cifrado end-to-end
- **Performance**: <2s respuesta API, <500ms IA
- **Mantenibilidad**: Despliegues independientes, testing automatizado

## 2. Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIOS                                 │
│  Web App  │  Mobile iOS  │  Mobile Android  │  Admin Dashboard │
└─────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CDN + WAF                                 │
│                   (CloudFlare)                                   │
└─────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY                                   │
│         (Kong / AWS API Gateway)                                 │
│  - Autenticación        - Rate Limiting                          │
│  - Routing              - Logging                                │
└─────────────────────────────────────────────────────────────────┘
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                   MICROSERVICIOS                               │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│ Auth Service │ User Service │Lawyer Service│ Case Service    │
├──────────────┼──────────────┼──────────────┼─────────────────┤
│ AI Service   │ Match Service│Document Gen  │ Payment Service │
├──────────────┼──────────────┼──────────────┼─────────────────┤
│ Notification │ Analytics    │ Integration  │ Admin Service   │
│ Service      │ Service      │ Service (OJV)│                 │
└───────────────────────────────────────────────────────────────┘
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│ PostgreSQL   │ MongoDB      │ Redis        │ S3              │
│ (relacional) │ (documentos) │ (cache/queue)│ (archivos)      │
└──────────────┴──────────────┴──────────────┴─────────────────┘
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                  SERVICIOS EXTERNOS                            │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│ OpenAI/      │ Transbank    │ SII          │ ClaveÚnica      │
│ Anthropic    │ (pagos)      │ (facturación)│ (auth)          │
├──────────────┼──────────────┼──────────────┼─────────────────┤
│ SendGrid     │ Twilio       │ AWS          │ Pinecone        │
│ (email)      │ (SMS/WA)     │ (infra)      │ (vector DB)     │
└──────────────┴──────────────┴──────────────┴─────────────────┘
```

## 3. Componentes del Frontend

### 3.1 Web Application

**Framework**: Next.js 14+ (React)

**Características**:
- SSR (Server-Side Rendering) para SEO
- App Router para routing moderno
- TypeScript para type-safety
- Tailwind CSS + shadcn/ui para UI
- React Query para state management
- Zod para validación

**Páginas Principales**:
- Landing page
- Chatbot IA (interfaz conversacional)
- Marketplace de abogados
- Perfil de usuario/abogado
- Dashboard (usuario/abogado)
- Sistema de mensajería
- Gestión de casos
- Pagos y facturación
- Admin panel

**Performance**:
- Lazy loading de componentes
- Image optimization (Next/Image)
- Code splitting automático
- Service Worker para offline

### 3.2 Mobile Applications

**Framework**: React Native + Expo

**Ventajas**:
- Código compartido iOS/Android (90%+)
- Hot reload para desarrollo rápido
- Acceso a APIs nativas
- Over-the-air updates

**Features Móviles**:
- Push notifications
- Biometric auth (FaceID/TouchID)
- Camera para upload documentos
- Deep linking
- Offline mode (básico)

### 3.3 Admin Dashboard

**Framework**: React + Vite

**Usuarios**:
- Team interno (ops, soporte)
- Moderación (verificación abogados)
- Analytics

**Features**:
- Gestión usuarios/abogados
- Moderación de perfiles y reviews
- Analytics y reportes
- Gestión de contenido
- Config de sistema

## 4. Backend - Microservicios

### 4.1 Auth Service

**Responsabilidad**: Autenticación y autorización

**Tecnología**: Node.js + Express + JWT

**Funcionalidades**:
- Registro/login usuarios y abogados
- Integración ClaveÚnica (OAuth)
- Social login (Google, LinkedIn)
- Email verification
- Password reset
- JWT generation/validation
- Role-based access control (RBAC)
- Session management

**Base de Datos**: PostgreSQL
- Tabla `users`
- Tabla `refresh_tokens`
- Tabla `oauth_credentials`

### 4.2 User Service

**Responsabilidad**: Gestión de perfiles de usuarios (clientes)

**Tecnología**: Node.js + Express

**Funcionalidades**:
- CRUD de perfiles
- Preferencias y configuración
- Historial de casos
- Favoritos (abogados)
- Reviews y ratings

**Base de Datos**: PostgreSQL
- Tabla `user_profiles`
- Tabla `user_preferences`
- Tabla `reviews`

### 4.3 Lawyer Service

**Responsabilidad**: Gestión de perfiles de abogados

**Tecnología**: Node.js + Express

**Funcionalidades**:
- Onboarding de abogados
- Verificación de credenciales (automática + manual)
- Gestión de especialidades
- Disponibilidad y calendario
- Pricing y paquetes
- Estadísticas y analytics
- Subscription management

**Base de Datos**: PostgreSQL
- Tabla `lawyer_profiles`
- Tabla `lawyer_credentials`
- Tabla `lawyer_specialties`
- Tabla `lawyer_availability`
- Tabla `lawyer_subscriptions`

**Integración Externa**:
- Búsqueda en registro Poder Judicial
- Verificación título universidad
- Verificación RUT (SII)

### 4.4 AI Service

**Responsabilidad**: Inteligencia artificial para chatbot y análisis

**Tecnología**: Python + FastAPI

**Funcionalidades**:
- Chatbot conversacional
- Triaje de consultas
- Análisis de documentos
- Generación de resúmenes
- Extracción de entidades legales
- Clasificación de casos
- Sentiment analysis

**IA/ML Stack**:
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Fine-tuning**: Con corpus legal chileno
- **Vector DB**: Pinecone (embeddings de leyes y jurisprudencia)
- **RAG**: Retrieval-Augmented Generation para precisión

**Base de Datos**:
- PostgreSQL: Historial de conversaciones
- Pinecone: Embeddings de contenido legal
- Redis: Cache de respuestas comunes

**APIs**:
- `POST /chat`: Enviar mensaje, recibir respuesta IA
- `POST /analyze-document`: Analizar contrato/documento
- `POST /classify-case`: Clasificar tipo de caso legal
- `POST /extract-entities`: Extraer fechas, montos, partes

### 4.5 Match Service

**Responsabilidad**: Matching inteligente usuario-abogado

**Tecnología**: Node.js + Express

**Algoritmo de Matching**:
```python
score = (
    specialization_match * 0.35 +
    availability_match * 0.15 +
    price_range_match * 0.20 +
    location_match * 0.10 +
    rating_score * 0.15 +
    success_rate * 0.05
)
```

**Funcionalidades**:
- Calcular match score
- Filtrar por criterios
- Ordenar por relevancia
- Recommend similar lawyers

**Base de Datos**: PostgreSQL + Redis cache

### 4.6 Case Service

**Responsabilidad**: Gestión del ciclo de vida de casos

**Tecnología**: Node.js + Express

**Estados de Caso**:
```
Inquiry → Matched → Negotiation → Agreed → Active →
Resolved → Closed
```

**Funcionalidades**:
- Crear caso desde chatbot
- Asignar abogado
- Gestionar documentos del caso
- Timeline de eventos
- Notas y comunicación
- Estado y progreso
- Finalización y review

**Base de Datos**: PostgreSQL + MongoDB
- PostgreSQL: Datos estructurados (metadata)
- MongoDB: Documentos, notas, comunicación

### 4.7 Document Generation Service

**Responsabilidad**: Generación automatizada de documentos

**Tecnología**: Python + FastAPI

**Funcionalidades**:
- Templates legales (Jinja2)
- Fill de formularios con datos usuario
- Generación PDF (WeasyPrint/ReportLab)
- Watermarking
- Versioning

**Templates**:
- Contratos (trabajo, arriendo, servicios)
- Poderes
- Demandas estándar
- Finiquitos
- Cartas legales

**Base de Datos**:
- S3: Templates y documentos generados
- PostgreSQL: Metadata

### 4.8 Payment Service

**Responsabilidad**: Procesamiento de pagos y comisiones

**Tecnología**: Node.js + Express

**Funcionalidades**:
- Integración Transbank/Flow
- Procesamiento de pagos
- Cálculo de comisiones
- Payout a abogados
- Facturación electrónica (SII)
- Gestión de suscripciones (Stripe-like)
- Reconciliación

**Base de Datos**: PostgreSQL
- Tabla `transactions`
- Tabla `commissions`
- Tabla `payouts`
- Tabla `invoices`

**Flujo de Pago**:
```
Cliente paga $100 →
  Platform retiene $25 (comisión) →
    Abogado recibe $75 (payout)
```

**Integraciones**:
- Transbank WebPay Plus
- Flow (alternativa)
- SII (facturación electrónica)
- Bancos (payouts)

### 4.9 Notification Service

**Responsabilidad**: Notificaciones multi-canal

**Tecnología**: Node.js + Bull (queue)

**Canales**:
- Email (SendGrid)
- SMS (Twilio)
- WhatsApp (Twilio Business)
- Push notifications (Firebase)
- In-app notifications

**Tipos de Notificaciones**:
- Nuevo mensaje
- Match con abogado
- Cambio estado de caso
- Recordatorios de pago
- Actualizaciones judiciales (OJV)
- Marketing (con opt-in)

**Base de Datos**:
- Redis: Cola de mensajes
- PostgreSQL: Historial y preferencias

### 4.10 Integration Service (OJV)

**Responsabilidad**: Integración con Oficina Judicial Virtual

**Tecnología**: Python + Selenium/Playwright

**Funcionalidades**:
- Scraping legal de OJV (sin API oficial)
- Login automatizado con ClaveÚnica
- Consulta de causas
- Detección de cambios
- Alertas automáticas
- Descarga de documentos judiciales

**Desafíos**:
- OJV sin API pública → scraping
- CAPTCHAs y anti-bot
- Cambios frecuentes de UI

**Mitigación**:
- Scraping respetuoso (rate limiting)
- Retry logic robusto
- Monitoreo de cambios en OJV
- Plan B: consulta manual con alertas

**Base de Datos**:
- MongoDB: Causas y actualizaciones
- PostgreSQL: Jobs y estado

### 4.11 Analytics Service

**Responsabilidad**: Analytics y reportes

**Tecnología**: Python + FastAPI

**Funcionalidades**:
- Tracking de eventos
- Dashboards de métricas
- Reportes automatizados
- A/B testing
- Cohort analysis
- Funnel analysis

**Stack de Analytics**:
- Mixpanel / Amplitude (product analytics)
- Google Analytics (web analytics)
- Custom dashboards (Metabase/Superset)

**Métricas Clave**:
- Usuarios activos (DAU/MAU)
- Conversion rate
- Churn
- LTV/CAC
- Net Revenue Retention

### 4.12 Admin Service

**Responsabilidad**: Operaciones internas y moderación

**Tecnología**: Node.js + Express

**Funcionalidades**:
- Verificación manual de abogados
- Moderación de reviews
- Soporte (ticketing)
- Gestión de contenido
- Feature flags
- System configuration

## 5. Data Layer

### 5.1 PostgreSQL (Relacional)

**Uso**: Datos transaccionales y estructurados

**Tablas Principales**:
- `users`
- `lawyers`
- `cases`
- `transactions`
- `reviews`
- `messages`
- `notifications`

**Características**:
- ACID compliance
- Replicación master-slave
- Backups diarios automáticos
- Point-in-time recovery

### 5.2 MongoDB (Documentos)

**Uso**: Datos no estructurados y semi-estructurados

**Colecciones**:
- `case_documents`
- `chat_history`
- `ojv_data`
- `legal_research`

**Características**:
- Flexible schema
- Horizontal scaling (sharding)
- Full-text search

### 5.3 Redis (Cache & Queue)

**Uso**: Caching, sessions, message queues

**Casos de Uso**:
- Session storage
- API response cache
- Rate limiting
- Real-time data
- Job queues (Bull)

### 5.4 S3 (Object Storage)

**Uso**: Archivos y documentos

**Buckets**:
- `justiciaai-documents` (documentos de casos)
- `justiciaai-generated` (documentos generados)
- `justiciaai-templates` (templates)
- `justiciaai-public` (imágenes, logos)

**Características**:
- Versioning
- Encryption at rest
- Lifecycle policies
- CDN integration

### 5.5 Pinecone (Vector Database)

**Uso**: Embeddings para RAG (IA)

**Contenido**:
- Leyes de Chile (embeddings)
- Jurisprudencia (sentencias)
- Doctrina legal
- FAQs legales

**Función**:
- Semantic search para chatbot
- Retrieval para contexto de IA

## 6. Infraestructura y DevOps

### 6.1 Cloud Provider

**Elección**: AWS (Amazon Web Services)

**Razones**:
- Cobertura en LATAM (São Paulo)
- Servicios maduros
- Compliance (ISO 27001, SOC 2)
- Ecosistema de herramientas

**Servicios AWS Utilizados**:
- EC2 / ECS Fargate (compute)
- RDS (PostgreSQL managed)
- ElastiCache (Redis managed)
- S3 (object storage)
- CloudFront (CDN)
- Route 53 (DNS)
- Certificate Manager (SSL)
- CloudWatch (monitoring)
- Secrets Manager (secrets)
- SES (email backup)

### 6.2 Containerización

**Docker**:
- Cada microservicio en container
- Multi-stage builds para optimización
- Alpine Linux base images

**Orchestration**:
- Kubernetes (EKS) para producción
- Docker Compose para desarrollo local

### 6.3 CI/CD

**Pipeline**:
```
Git Push → GitHub Actions →
  Linting & Testing →
    Build Docker Image →
      Push to ECR →
        Deploy to EKS (staging) →
          E2E Tests →
            Deploy to EKS (prod)
```

**Herramientas**:
- GitHub Actions (CI/CD)
- Jest (unit tests)
- Cypress (E2E tests)
- SonarQube (code quality)
- Snyk (security scanning)

### 6.4 Monitoreo y Logging

**Application Monitoring**:
- Sentry (error tracking)
- New Relic / Datadog (APM)
- Prometheus + Grafana (metrics)

**Logging**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Structured logging (JSON)
- Log retention: 90 días

**Alerting**:
- PagerDuty (on-call)
- Slack integration
- Email alerts

## 7. Seguridad

### 7.1 Autenticación y Autorización

**Auth**:
- JWT tokens (access + refresh)
- OAuth 2.0 para integraciones
- ClaveÚnica para verificación identidad

**RBAC (Role-Based Access Control)**:
- Roles: User, Lawyer, Admin, Moderator
- Permisos granulares por recurso

### 7.2 Cifrado

**En Tránsito**:
- TLS 1.3 obligatorio
- HTTPS everywhere
- Certificate pinning (móvil)

**En Reposo**:
- Database encryption (AWS KMS)
- S3 encryption (AES-256)
- Backups cifrados

### 7.3 Protección de Datos (Ley 21.719)

**Principios**:
- Data minimization
- Purpose limitation
- Consent management
- Right to erasure
- Data portability

**Implementación**:
- Consent flags en DB
- Data export API
- Data deletion API
- Audit logs de accesos
- Privacy policy y T&C claros

### 7.4 Seguridad Aplicación

**Protecciones**:
- Input validation (Zod, Joi)
- SQL injection prevention (ORMs)
- XSS prevention (sanitization)
- CSRF tokens
- Rate limiting (prevención DDoS)
- Content Security Policy
- Security headers

**Auditorías**:
- Pentesting anual
- Vulnerability scanning (Snyk)
- Dependency updates automatizadas

## 8. Escalabilidad

### 8.1 Horizontal Scaling

**Servicios Stateless**:
- Fácilmente replicables
- Load balancing (AWS ALB)
- Auto-scaling basado en CPU/memoria

**Ejemplo**:
```
Traffic aumenta →
  Kubernetes escala pods →
    2 → 10 instancias de API Service
```

### 8.2 Database Scaling

**PostgreSQL**:
- Read replicas para queries pesadas
- Connection pooling (PgBouncer)
- Sharding por usuario (futuro, si necesario)

**MongoDB**:
- Sharding nativo
- Indexes optimizados

**Redis**:
- Redis Cluster para alta disponibilidad

### 8.3 Caching Strategy

**Capas de Cache**:
1. CDN (CloudFront) - assets estáticos
2. Application cache (Redis) - API responses
3. Database query cache

**Invalidación**:
- TTL-based para datos no críticos
- Event-based para datos críticos

### 8.4 Async Processing

**Casos de Uso**:
- Envío de notificaciones
- Generación de documentos
- Scraping OJV
- Analytics processing

**Herramienta**: Bull (Redis-backed queue)

**Ventaja**: Desacoplar y escalar workers independientemente

## 9. Disaster Recovery & Business Continuity

### 9.1 Backups

**Databases**:
- Backups automáticos diarios
- Retención: 30 días
- Point-in-time recovery (7 días)
- Cross-region replication

**Archivos (S3)**:
- Versioning habilitado
- Replicación a bucket secundario

### 9.2 High Availability

**Diseño**:
- Multi-AZ deployment
- Redundancia en todos los servicios críticos
- Health checks y auto-healing

**SLA Target**: 99.9% uptime (8.76 horas downtime/año)

### 9.3 Disaster Recovery Plan

**RTO (Recovery Time Objective)**: 4 horas
**RPO (Recovery Point Objective)**: 1 hora

**Procedimiento**:
1. Detectar incidente
2. Activar equipo on-call
3. Evaluar impacto
4. Activar backup en región secundaria
5. Redirigir tráfico
6. Comunicar a usuarios

## 10. Roadmap Técnico

### Fase 1: MVP (Meses 1-3)

**Servicios Mínimos**:
- Auth Service
- User Service
- Lawyer Service
- AI Service (básico)
- Case Service (básico)
- Payment Service (básico)

**Frontend**:
- Web app con chatbot IA
- Marketplace básico
- Perfiles y dashboard simple

**Infraestructura**:
- Monolito modular (más rápido que microservicios desde inicio)
- PostgreSQL + Redis
- Deployment en Heroku/Railway (speed)

### Fase 2: Escalamiento (Meses 4-6)

**Servicios Adicionales**:
- Document Generation
- Notification Service
- Match Service (algoritmo mejorado)
- Integration Service (OJV)

**Frontend**:
- Apps móviles (React Native)
- Mensajería en tiempo real
- Admin dashboard

**Infraestructura**:
- Migración a AWS
- Separación en microservicios
- CI/CD automatizado

### Fase 3: Optimización (Meses 7-12)

**Servicios Avanzados**:
- Analytics Service
- IA avanzada (fine-tuning)
- ODR (dispute resolution)

**Frontend**:
- Offline mode
- PWA
- Performance optimization

**Infraestructura**:
- Kubernetes en producción
- Multi-region (si necesario)
- Monitoring avanzado

### Fase 4: Expansión (Año 2+)

**Servicios**:
- B2B API
- White-label platform
- Integración con más servicios externos

**Infraestructura**:
- Global CDN
- Edge computing (Cloudflare Workers)
- ML infrastructure (para entrenar modelos propios)

## 11. Decisiones Técnicas Clave

### 11.1 Monolito vs Microservicios

**Decisión**: Empezar con monolito modular, evolucionar a microservicios

**Razón**:
- Velocidad de desarrollo inicial (MVP en 3 meses)
- Menos complejidad operacional al inicio
- Más fácil de debugear
- Transición a microservicios cuando equipo y escala lo requieran

### 11.2 SQL vs NoSQL

**Decisión**: PostgreSQL principal + MongoDB complementario

**Razón**:
- Datos transaccionales (casos, pagos) requieren ACID
- PostgreSQL maduro y confiable
- MongoDB para flexibilidad en documentos/chat

### 11.3 Build vs Buy (IA)

**Decisión**: Usar APIs de OpenAI/Anthropic, fine-tune cuando necesario

**Razón**:
- Velocidad (no entrenar desde cero)
- Calidad (modelos state-of-the-art)
- Costo inicial bajo
- Migrar a modelo propio cuando escala lo justifique

### 11.4 On-Premise vs Cloud

**Decisión**: Cloud-first (AWS)

**Razón**:
- Velocidad de deployment
- Escalabilidad elástica
- Menor capex
- Compliance y seguridad gestionados

## 12. Estimación de Costos Técnicos

### Año 1 (MVP, 100 usuarios/día)

| Recurso | Costo Mensual |
|---------|---------------|
| AWS Compute (EC2/ECS) | $200 |
| AWS RDS (PostgreSQL) | $100 |
| AWS ElastiCache (Redis) | $50 |
| AWS S3 + CloudFront | $30 |
| OpenAI API | $300 |
| Herramientas (Sentry, SendGrid, etc.) | $150 |
| **Total Mensual** | **$830** |
| **Total Anual** | **$10K** |

### Año 2 (Crecimiento, 5,000 usuarios/día)

| Recurso | Costo Mensual |
|---------|---------------|
| AWS Infrastructure | $1,500 |
| OpenAI API | $1,500 |
| Monitoring & Tools | $500 |
| **Total Mensual** | **$3,500** |
| **Total Anual** | **$42K** |

### Año 3 (Escala, 20,000 usuarios/día)

| Recurso | Costo Mensual |
|---------|---------------|
| AWS Infrastructure | $5,000 |
| OpenAI API (o modelo propio) | $3,000 |
| Monitoring & Tools | $1,000 |
| **Total Mensual** | **$9,000** |
| **Total Anual** | **$108K** |

**Nota**: Costos técnicos son ~3-5% de ingresos en Año 3 (saludable para SaaS)

---

**Próximo**: Ver stack detallado, esquemas de base de datos, y APIs en documentos técnicos adicionales.
