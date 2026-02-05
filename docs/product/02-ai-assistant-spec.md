# Especificación: Asistente Legal con IA

## 1. Resumen

**Nombre**: JusticiaBot
**Propósito**: Chatbot conversacional especializado en leyes chilenas que ofrece orientación legal inicial gratuita y recomienda abogados cuando necesario.
**Tecnología**: Anthropic Claude 3.5 Sonnet + RAG (Retrieval-Augmented Generation)

## 2. User Stories

### US-001: Como usuario, quiero consultar si tengo un caso legal
**Given**: Usuario describe su problema
**When**: Chatbot analiza la situación
**Then**: Recibe orientación clara sobre si requiere asesoría legal

### US-002: Como usuario, quiero entender mis derechos
**Given**: Usuario en situación legal específica
**When**: Hace preguntas sobre sus derechos
**Then**: Recibe información clara en lenguaje simple

### US-003: Como usuario, quiero saber próximos pasos
**Given**: Usuario confirma necesitar abogado
**When**: Finaliza conversación con IA
**Then**: Recibe informe con resumen, derechos, opciones y recomendación de abogados

## 3. Funcionalidades Core

### 3.1 Triage de Consultas

**Input**: Descripción del problema del usuario
**Proceso**:
```
1. Usuario describe situación
2. IA hace preguntas aclaratorias (máx 5)
3. Clasifica:
   - Área legal (familia, laboral, civil, etc.)
   - Urgencia (alta, media, baja)
   - Complejidad (simple, media, compleja)
   - ¿Requiere abogado? (sí/no/tal vez)
```
**Output**: Clasificación + explicación

### 3.2 Explicación de Derechos

**Corpus Legal**:
- Leyes chilenas (embeddings en Pinecone)
- Código Civil, Laboral, Familia, etc.
- Jurisprudencia relevante
- FAQs legales

**Proceso (RAG)**:
```
1. Pregunta usuario → Embedding
2. Búsqueda semántica en Pinecone (top 5 chunks relevantes)
3. Claude genera respuesta con contexto legal
4. Cita fuentes (artículos de ley)
```

**Ejemplo**:
```
Usuario: "Me despidieron sin previo aviso, ¿es legal?"
IA: "En Chile, según el Código del Trabajo (artículo 161), el empleador
puede terminar el contrato sin previo aviso solo por causales específicas
llamadas 'necesidades de la empresa' (artículo 161). Sin embargo, debe
pagarte:
- Indemnización por años de servicio
- Indemnización sustitutiva de aviso previo (1 mes)

¿Quieres que calculemos tu indemnización aproximada?"
```

### 3.3 Generación de Informe Preliminar

**Trigger**: Usuario termina conversación o pide "ver resumen"

**Contenido del Informe (PDF)**:
```
┌─────────────────────────────────────────────┐
│      INFORME LEGAL PRELIMINAR               │
│         JusticiaAI                          │
└─────────────────────────────────────────────┘

1. RESUMEN DE TU SITUACIÓN
   [Resumen generado por IA basado en conversación]

2. ÁREA LEGAL
   Laboral - Despido

3. TUS DERECHOS
   • Derecho a indemnización por años de servicio
   • Derecho a indemnización sustitutiva de aviso previo
   • Derecho a reclamar si despido es injustificado

   Base Legal: Código del Trabajo, artículos 161, 162, 163

4. OPCIONES DISPONIBLES
   • Negociar finiquito con empleador
   • Presentar reclamo ante Inspección del Trabajo
   • Demandar ante Tribunales Laborales

5. PRÓXIMOS PASOS RECOMENDADOS
   1. Reunir documentación (contrato, finiquito, emails)
   2. Consultar con abogado laboral especializado
   3. Actuar dentro de 60 días desde despido

6. ABOGADOS RECOMENDADOS
   [3 perfiles de abogados matched]

   📞 ¿Quieres conectar con un abogado ahora?
   [Botón: Ver Abogados] [Botón: Descargar Informe]

────────────────────────────────────────────
Este informe es solo orientación general. No
constituye asesoría legal formal. Para análisis
específico de tu caso, consulta un abogado.
```

### 3.4 Matching Inteligente

**Proceso**:
```
1. Área legal detectada → Filtrar abogados por especialidad
2. Aplicar algoritmo de matching (ver spec separada)
3. Seleccionar top 3
4. Mostrar en informe
```

## 4. Arquitectura Técnica

### 4.1 Components

```
┌─────────────────────────────────────────────────┐
│              FRONTEND                           │
│  Chat Interface (React)                         │
│  - Input field + Send button                    │
│  - Message history                              │
│  - Typing indicator                             │
│  - Quick replies (buttons)                      │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│              API GATEWAY                        │
│  POST /api/chat                                 │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│           AI SERVICE (Python/FastAPI)           │
│                                                 │
│  1. Receive message                             │
│  2. Retrieve context (RAG)                      │
│  3. Call Anthropic Claude API                   │
│  4. Process response                            │
│  5. Save conversation                           │
│  6. Return response                             │
└─────────────────────────────────────────────────┘
            ▼                    ▼
┌──────────────────┐  ┌─────────────────────────┐
│   PINECONE       │  │  ANTHROPIC CLAUDE       │
│ (Vector Search)  │  │  (LLM API)              │
│ - Legal corpus   │  │  - claude-3-5-sonnet    │
│ - Jurisprudence  │  │  - 200K context window  │
└──────────────────┘  └─────────────────────────┘
            ▼
┌─────────────────────────────────────────────────┐
│         DATABASE (PostgreSQL)                   │
│  - conversations                                │
│  - messages                                     │
│  - classifications                              │
└─────────────────────────────────────────────────┘
```

### 4.2 API Endpoints

#### POST /api/chat
```typescript
Request:
{
  "conversation_id": "uuid" | null, // null para nueva conversación
  "message": "Me despidieron sin aviso",
  "user_id": "uuid" | null // null si anónimo
}

Response:
{
  "conversation_id": "uuid",
  "response": {
    "text": "Entiendo tu situación. Para ayudarte mejor...",
    "type": "question" | "answer" | "summary",
    "quick_replies": ["Sí", "No", "No estoy seguro"] | null
  },
  "classification": {
    "area": "laboral" | "familia" | ...,
    "urgency": "high" | "medium" | "low",
    "needs_lawyer": boolean,
    "confidence": 0.85
  } | null, // null si aún no clasificado
  "metadata": {
    "tokens_used": 1250,
    "response_time_ms": 850
  }
}
```

#### POST /api/chat/summary
```typescript
Request:
{
  "conversation_id": "uuid"
}

Response:
{
  "summary": {
    "situation": "Descripción generada...",
    "area": "laboral",
    "rights": ["Derecho a indemnización...", ...],
    "options": ["Negociar finiquito...", ...],
    "next_steps": ["Reunir documentación...", ...]
  },
  "matched_lawyers": [
    {
      "id": "uuid",
      "name": "María González",
      "specialty": "Derecho Laboral",
      "rating": 4.8,
      "cases_won": 45,
      "price_range": "$300-500K",
      "match_score": 0.92
    },
    // ... 2 más
  ],
  "pdf_url": "https://justiciaai.cl/reports/uuid.pdf"
}
```

### 4.3 RAG Implementation

**Pipeline**:
```python
def generate_response(user_message: str, conversation_history: list):
    # 1. Generar embedding de la pregunta
    question_embedding = generate_embedding(user_message)

    # 2. Buscar en Pinecone
    relevant_chunks = pinecone_index.query(
        vector=question_embedding,
        top_k=5,
        include_metadata=True
    )

    # 3. Construir contexto
    context = "\n\n".join([
        f"Fuente: {chunk.metadata['source']}\n{chunk.metadata['text']}"
        for chunk in relevant_chunks
    ])

    # 4. Construir prompt
    prompt = f"""
    Eres JusticiaBot, un asistente legal especializado en leyes de Chile.

    Contexto Legal:
    {context}

    Historial de Conversación:
    {format_conversation_history(conversation_history)}

    Usuario: {user_message}

    Instrucciones:
    - Responde en español chileno, lenguaje simple
    - Cita artículos de ley cuando relevantes
    - Si no estás seguro, dilo claramente
    - Sugiere consultar abogado para casos complejos
    - Máximo 150 palabras

    Respuesta:
    """

    # 5. Llamar a Claude
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
```

### 4.4 Corpus Legal (Pinecone)

**Contenido**:
- Código Civil (8,000 chunks)
- Código del Trabajo (3,000 chunks)
- Código de Familia (2,000 chunks)
- Leyes especiales (5,000 chunks)
- Jurisprudencia relevante (10,000 chunks)
- FAQs legales (1,000 chunks)

**Total**: ~29,000 chunks

**Chunk Size**: 500 tokens con overlap de 50

**Metadata por Chunk**:
```json
{
  "text": "Artículo 161. El contrato de trabajo...",
  "source": "Código del Trabajo",
  "article": "161",
  "area": "laboral",
  "topic": "despidos",
  "url": "https://www.bcn.cl/leychile/..."
}
```

## 5. Prompt Engineering

### 5.1 System Prompt

```
Eres JusticiaBot, un asistente legal especializado en las leyes de Chile.

TU ROL:
- Orientar a ciudadanos sobre sus derechos y opciones legales
- Explicar conceptos legales en lenguaje simple
- Hacer triaje de consultas legales
- Recomendar cuándo consultar un abogado

LO QUE DEBES HACER:
✓ Usar lenguaje simple, evitar jerga legal innecesaria
✓ Hacer preguntas aclaratorias cuando sea necesario
✓ Citar leyes y artículos específicos cuando aplique
✓ Ser empático y comprensivo
✓ Explicar paso a paso
✓ Recomendar próximos pasos concretos

LO QUE NO DEBES HACER:
✗ Dar asesoría legal específica (no eres abogado)
✗ Garantizar resultados de casos
✗ Asumir información no proporcionada
✗ Usar lenguaje técnico sin explicar
✗ Ser ambiguo sobre limitaciones

FORMATO DE RESPUESTAS:
- Párrafos cortos (2-3 líneas máximo)
- Listas con bullets cuando enumeras opciones
- Citas legales en formato: "según [Ley], artículo [X]"
- Preguntas al final si necesitas aclarar

LIMITACIONES (siempre menciona cuando relevante):
"Esta es orientación general. Para tu caso específico,
recomiendo consultar con un abogado especializado."
```

### 5.2 Few-Shot Examples

**Ejemplo 1: Pregunta simple**
```
User: "¿Puedo despedir a un trabajador sin motivo?"
Assistant: "En Chile NO puedes despedir sin motivo justificado.
Según el Código del Trabajo, existen dos tipos de despido válidos:

1. **Con causa justificada** (Art. 160): Faltas graves del trabajador
2. **Necesidades de la empresa** (Art. 161): Razones económicas

En ambos casos debes:
• Dar aviso por escrito
• Especificar la causal
• Pagar indemnizaciones correspondientes

Despedir "sin motivo" puede considerarse **despido injustificado**
y el trabajador puede demandarte.

¿Tienes una situación específica con un trabajador?"
```

**Ejemplo 2: Caso complejo → Derivar**
```
User: "Quiero demandar a mi empleador por acoso laboral y obtener
indemnización. ¿Cuánto me corresponde?"
Assistant: "Entiendo que estás en una situación muy difícil.
El acoso laboral es un tema serio protegido por ley en Chile.

Sobre la indemnización, depende de múltiples factores:
• Gravedad del acoso
• Duración y frecuencia
• Daños causados (psicológicos, económicos)
• Pruebas disponibles

**Este es un caso complejo que requiere análisis profesional.**

Te recomiendo:
1. Documentar todos los incidentes (fechas, testigos, emails)
2. Consultar con un abogado laboralista especializado en acoso
3. Considerar denuncia ante Inspección del Trabajo

¿Quieres que te conecte con abogados especializados en este tema?"
```

## 6. Clasificación de Consultas

### 6.1 Áreas Legales (Taxonomy)

```typescript
enum AreaLegal {
  FAMILIA = "familia",              // Divorcio, pensiones, visitas
  LABORAL = "laboral",              // Despidos, finiquitos, acoso
  CIVIL = "civil",                  // Contratos, arriendos, disputas
  PENAL = "penal",                  // Delitos, denuncias
  CONSUMIDOR = "consumidor",        // Reclamos, garantías
  DEUDAS = "deudas",                // Cobranzas, negociación
  HERENCIAS = "herencias",          // Sucesiones, testamentos
  INMOBILIARIO = "inmobiliario",    // Compraventa, hipotecas
  COMERCIAL = "comercial",          // Contratos, sociedades
  OTRO = "otro"
}
```

### 6.2 Urgencia

```typescript
enum Urgency {
  HIGH = "high",      // <7 días (plazo legal inminente)
  MEDIUM = "medium",  // 7-30 días
  LOW = "low"         // >30 días o sin plazo crítico
}
```

### 6.3 Clasificador con Claude

```python
async def classify_case(conversation: list) -> Classification:
    summary = summarize_conversation(conversation)

    prompt = f"""
    Analiza esta consulta legal y clasifícala:

    Consulta: {summary}

    Responde en JSON:
    {{
      "area": "familia" | "laboral" | ...,
      "urgency": "high" | "medium" | "low",
      "needs_lawyer": true | false,
      "complexity": "simple" | "medium" | "complex",
      "reasoning": "breve explicación"
    }}
    """

    response = await anthropic_client.complete(prompt)
    return parse_json(response)
```

## 7. UX/UI Considerations

### 7.1 Chat Interface

**Design Principles**:
- Conversacional, no formulario
- Typing indicators (IA "pensando")
- Quick replies para opciones comunes
- Scroll automático a último mensaje
- Avatar de JusticiaBot

**Example Flow**:
```
[JusticiaBot]: ¡Hola! 👋 Soy JusticiaBot. Cuéntame, ¿en qué puedo ayudarte hoy?

[Usuario]: Me despidieron del trabajo

[JusticiaBot]: Entiendo, lamento escuchar eso. Para ayudarte mejor,
¿podrías contarme un poco más?

[Quick Replies]:
[Me despidieron hoy] [Fue hace semanas] [Aún no me despiden]

[Usuario]: *clicks "Me despidieron hoy"*

[JusticiaBot]: ¿Te entregaron una carta de despido o finiquito?

[Quick Replies]:
[Sí, tengo carta] [No me dieron nada] [Solo verbal]

...
```

### 7.2 Mobile Considerations

- Teclado no debe ocultar últimos mensajes
- Quick replies en horizontal scroll
- Botón "enviar" grande (thumb-friendly)
- Voice input (futuro)

### 7.3 Accessibility

- Screen reader compatible
- Alt text para íconos
- Sufficient color contrast
- Keyboard navigation
- Font size adjustable

## 8. Guardrails & Safety

### 8.1 Disclaimer Automático

Mostrar al iniciar conversación:
```
⚠️ Importante: JusticiaBot ofrece orientación legal general.
No reemplaza la asesoría de un abogado. Para decisiones
legales importantes, consulta un profesional.
```

### 8.2 Content Moderation

**Detectar y bloquear**:
- Solicitudes de asesoría médica
- Contenido violento/ilegal
- Spam comercial
- Abuso/insultos

**Respuesta Genérica**:
```
"Lo siento, no puedo ayudarte con eso. Si tienes una
consulta legal, estaré encantado de orientarte."
```

### 8.3 Rate Limiting

- Usuarios anónimos: 5 conversaciones/día
- Usuarios registrados: 20 conversaciones/día
- Bloqueo temporal si abuso detectado

## 9. Métricas de Éxito

### 9.1 Product Metrics

- **Engagement**: Mensajes por conversación (target: 8+)
- **Completion Rate**: % conversaciones que llegan a informe (target: 70%)
- **Conversion Rate**: % que solicitan abogado después de IA (target: 30%)
- **Time to Classification**: Mensajes hasta clasificar caso (target: <5)

### 9.2 Quality Metrics

- **Accuracy**: % respuestas correctas (eval manual, target: 95%+)
- **Helpfulness**: Rating usuarios (1-5, target: 4.2+)
- **Lawyer Confidence**: % abogados confiados en clasificación de IA (target: 85%+)

### 9.3 Technical Metrics

- **Latency**: Response time (target: <2s p95)
- **Token Usage**: Promedio tokens/mensaje (target: <1,500)
- **Error Rate**: % llamadas fallidas (target: <1%)
- **Cost per Conversation**: USD/conversación (target: <$0.50)

## 10. Testing Strategy

### 10.1 Unit Tests

- Test prompt generation
- Test RAG retrieval (mock Pinecone)
- Test classification logic
- Test conversation summarization

### 10.2 Integration Tests

- Test full chat flow end-to-end
- Test Anthropic API integration
- Test Pinecone search
- Test PDF generation

### 10.3 Quality Eval

**Dataset de Test**: 100 consultas legales reales

**Eval Criteria**:
- ¿Respuesta correcta? (Sí/No)
- ¿Cita leyes relevantes? (Sí/No)
- ¿Lenguaje comprensible? (1-5)
- ¿Recomienda abogado cuando debe? (Sí/No)

**Threshold**: 90% aprobación

### 10.4 Load Testing

- Simular 100 conversaciones concurrentes
- Verificar latency < 3s bajo carga
- Verificar no rate limits de Anthropic

## 11. Roadmap de Mejoras

### Fase 1 (MVP)
- ✅ Chat básico con Claude
- ✅ RAG con corpus legal
- ✅ Clasificación de casos
- ✅ Generación de informe PDF

### Fase 2 (Mes 4-6)
- 📄 Análisis de documentos (upload PDF)
- 🧠 Memoria entre sesiones
- 📊 Análisis predictivo (probabilidad éxito)
- 🗣️ Voice input (speech-to-text)

### Fase 3 (Mes 7-12)
- 🧬 Fine-tuning modelo propio con casos reales
- 🌐 Multi-idioma (inglés para extranjeros)
- 📞 Integración con videollamadas
- 🎓 Modo educativo (aprender sobre leyes)

---

**Owner**: AI Team
**Priority**: P0 (Core Feature)
**Status**: Spec Completo → Ready for Development
