# 🤖 Sistema RAG - JusticiaAI

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Instalación](#instalación)
4. [Uso Básico](#uso-básico)
5. [Pipeline Completo](#pipeline-completo)
6. [Configuración](#configuración)
7. [Fuentes de Datos](#fuentes-de-datos)
8. [Costos](#costos)
9. [Troubleshooting](#troubleshooting)
10. [Próximos Pasos](#próximos-pasos)

---

## 🎯 Visión General

El **Sistema RAG (Retrieval-Augmented Generation)** de JusticiaAI combina:

- **Búsqueda vectorial** (Pinecone): Encuentra información legal relevante
- **IA generativa** (Claude): Genera respuestas precisas usando contexto verificado
- **Fuentes oficiales chilenas**: BCN LeyChile, Dirección del Trabajo, SERNAC

### ¿Por qué RAG?

**Problema**: Claude solo conoce leyes hasta su fecha de entrenamiento (2024), y puede "alucinar" información legal incorrecta.

**Solución RAG**:
1. Usuario pregunta: *"¿Me pueden despedir sin finiquito?"*
2. Sistema busca en base de conocimiento → Encuentra Código del Trabajo, Art. 160-161
3. Claude recibe contexto legal → Responde con información verificada
4. Usuario obtiene respuesta precisa con fuentes citadas

### Beneficios

✅ **Precisión**: Respuestas basadas en leyes chilenas reales
✅ **Actualización**: Fácil agregar nuevas leyes/dictámenes
✅ **Trazabilidad**: Cada respuesta cita sus fuentes
✅ **Defensibilidad**: Data moat que crece con el uso
✅ **Confianza**: Usuarios ven fuentes oficiales

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     USUARIO                                   │
│                  "¿Qué es el finiquito?"                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 CHATBOT (FastAPI)                             │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ 1. Recibe pregunta                                     │   │
│  │ 2. Genera embedding de pregunta (OpenAI)              │   │
│  │ 3. Busca contexto relevante (Pinecone)                │   │
│  │ 4. Construye prompt con contexto + pregunta           │   │
│  │ 5. Envía a Claude                                      │   │
│  │ 6. Devuelve respuesta + fuentes                        │   │
│  └───────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴───────────┐
        ▼                        ▼
┌──────────────┐        ┌──────────────────┐
│   PINECONE   │        │     CLAUDE       │
│  Vector DB   │        │   (Anthropic)    │
│              │        │                  │
│ • 100K vecs  │        │ • Genera texto   │
│ • Búsqueda   │        │ • Usa contexto   │
│ • Similitud  │        │ • Cita fuentes   │
└──────────────┘        └──────────────────┘
```

### Componentes

1. **Data Collection** (`data_collection/`)
   - `bcn_scraper.py`: Descarga leyes desde BCN LeyChile
   - `dt_scraper.py`: Descarga guías de Dirección del Trabajo
   - `sernac_scraper.py`: Descarga info de derechos del consumidor

2. **Data Processing** (`data_processing/`)
   - `text_processor.py`: Limpia y divide textos en chunks
   - `embedder.py`: Genera embeddings vectoriales (OpenAI)

3. **RAG System** (`rag/`)
   - `vector_store.py`: Maneja almacenamiento en Pinecone
   - `rag_engine.py`: Motor principal de RAG

4. **API** (`main_simple.py`)
   - Endpoint `/api/chat` con RAG integrado

---

## 🚀 Instalación

### Paso 1: Requisitos

```bash
# Python 3.10+
python --version

# Instalar dependencias
cd backend
pip install -r requirements.txt

# Dependencias nuevas necesarias:
pip install openai pinecone-client beautifulsoup4 pyyaml
```

### Paso 2: Configurar API Keys

```bash
# Copiar template
cp .env.example .env

# Editar .env con tus keys
nano .env
```

Necesitas obtener:

1. **OpenAI API Key** (para embeddings)
   - Ve a: https://platform.openai.com/api-keys
   - Crea API key
   - Agrega a `.env`: `OPENAI_API_KEY=sk-...`

2. **Pinecone API Key** (para vector database)
   - Ve a: https://app.pinecone.io/
   - Crea cuenta gratuita
   - Settings → API Keys → Create API Key
   - Agrega a `.env`: `PINECONE_API_KEY=...`

3. **Anthropic API Key** (ya la tienes)
   - Ya está configurada: `ANTHROPIC_API_KEY=sk-ant-api03-...`

### Paso 3: Verificar Instalación

```bash
# Verificar que todo esté instalado
python -c "import openai, pinecone; print('✅ Librerías OK')"

# Verificar API keys
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI:', bool(os.getenv('OPENAI_API_KEY'))); print('Pinecone:', bool(os.getenv('PINECONE_API_KEY')))"
```

---

## 📖 Uso Básico

### Pipeline Completo (5 Pasos)

#### Paso 1: Recopilar Datos Legales

```bash
# Directorio: backend/

# Descargar leyes desde BCN
python data_collection/bcn_scraper.py

# Descargar guías laborales
python data_collection/dt_scraper.py

# Descargar info consumidor
python data_collection/sernac_scraper.py
```

**Salida**: Archivos JSON en `data/raw/bcn/`, `data/raw/dt/`, `data/raw/sernac/`

#### Paso 2: Procesar Textos

```bash
# Limpiar y dividir textos en chunks
python data_processing/text_processor.py
```

**Salida**: Archivos `*_chunks.json` en `data/processed/`

#### Paso 3: Generar Embeddings

```bash
# Generar vectores con OpenAI
python data_processing/embedder.py
```

**Salida**: Archivos `*_embedded.json` en `data/embeddings/`
**Costo**: ~$0.10 para 5K chunks

#### Paso 4: Subir a Pinecone

```bash
# Cargar vectores a Pinecone
python rag/vector_store.py
```

**Salida**: Índice `justiciaai-legal` en Pinecone con todos los vectores

#### Paso 5: Probar RAG

```bash
# Iniciar backend con RAG
python main_simple.py
```

Ve a: http://localhost:3001/chat

Haz una pregunta: *"¿Qué es el finiquito?"*

Verás que la respuesta:
- ✅ Usa información de la base de conocimiento
- ✅ Cita fuentes específicas
- ✅ Es más precisa que Claude solo

---

## ⚙️ Configuración

### config.yaml

Personaliza el comportamiento del RAG:

```yaml
rag:
  top_k: 3  # Número de documentos a recuperar (1-5)
  similarity_threshold: 0.7  # Umbral mínimo similitud (0-1)

text_processing:
  chunk_size: 1000  # Tamaño chunks (500-2000)
  chunk_overlap: 200  # Solapamiento (100-300)
```

### Ajustar Precisión vs Recall

- **Más precisión** (menos resultados, más relevantes):
  - `top_k: 2`
  - `similarity_threshold: 0.8`

- **Más recall** (más resultados, algunos menos relevantes):
  - `top_k: 5`
  - `similarity_threshold: 0.6`

---

## 📚 Fuentes de Datos

### Actuales

1. **BCN LeyChile** (Leyes oficiales)
   - Código del Trabajo
   - Código Civil
   - Ley del Consumidor (19.496)
   - Ley de Matrimonio Civil (19.947)
   - Pensión Alimenticia (14.908)

2. **Dirección del Trabajo** (Guías laborales)
   - Finiquito y término de contrato
   - Despido y causales
   - Jornada laboral y horas extras
   - Vacaciones y permisos
   - Sueldo mínimo y remuneraciones

3. **SERNAC** (Derechos del consumidor)
   - Derecho a retracto
   - Garantía legal
   - Cobros indebidos

### Próximas Fuentes (Roadmap)

- [ ] Dictámenes de Dirección del Trabajo (vía API/scraping)
- [ ] Sentencias del Poder Judicial (casos públicos)
- [ ] Artículos académicos (SciELO Chile)
- [ ] Datos de feedback positivo de usuarios

---

## 💰 Costos

### Fase Inicial (MVP)

| Servicio | Costo | Límites Free Tier |
|----------|-------|-------------------|
| **Pinecone** | $0/mes | 100K vectores, 1 índice |
| **OpenAI Embeddings** | ~$0.10 | Por 5K chunks (~$0.02/1M tokens) |
| **Claude (Haiku)** | ~$10-15/mes | 1000 consultas ($0.25 input, $1.25 output/1M tokens) |
| **Total** | **$10-20/mes** | Hasta 1000 usuarios/mes |

### Escalado (Post-Seed, 10K usuarios/mes)

| Servicio | Costo |
|----------|-------|
| **Pinecone** | $70/mes | Plan Standard (1M vectores) |
| **OpenAI** | $5/mes | Actualizaciones mensuales |
| **Claude** | $150/mes | 10K consultas |
| **Total** | **$225/mes** | (~0.5% de revenue proyectado) |

---

## 🐛 Troubleshooting

### Error: "Pinecone API key no configurada"

```bash
# Verifica que .env tenga la key
cat .env | grep PINECONE_API_KEY

# Si no existe, agrégala
echo "PINECONE_API_KEY=tu-api-key-aquí" >> .env
```

### Error: "Vector store no inicializado"

```bash
# Ejecuta el pipeline completo:
python data_collection/bcn_scraper.py
python data_processing/text_processor.py
python data_processing/embedder.py
python rag/vector_store.py
```

### Error: "No se encuentran archivos de chunks"

```bash
# Verifica que existan los directorios
ls data/raw/bcn
ls data/processed
ls data/embeddings

# Si faltan, ejecuta scrapers primero
python data_collection/bcn_scraper.py
```

### RAG no está funcionando en el chat

```bash
# Verifica health endpoint
curl http://localhost:8000/health

# Debe mostrar: "rag_enabled": true
```

Si dice `false`, revisa logs del backend al iniciar.

---

## 🔜 Próximos Pasos

### Corto Plazo (Post-Implementación)

1. **Monitoreo de Calidad**
   - Revisar feedbacks negativos
   - Identificar preguntas que RAG no responde bien
   - Agregar más contenido de esas áreas

2. **Actualización Regular**
   - Configurar cron job mensual para scrapers
   - Agregar nuevos dictámenes de DT
   - Actualizar cambios en leyes

3. **Optimización**
   - Ajustar `top_k` y `similarity_threshold` según feedback
   - Experimentar con chunk sizes
   - Probar reranking de resultados

### Mediano Plazo (Post-Seed)

4. **Fuentes Adicionales**
   - API de Dirección del Trabajo
   - Sentencias del Poder Judicial
   - Casos reales validados por abogados

5. **Features Avanzadas**
   - Filtros por categoría legal en búsqueda
   - Respuestas con múltiples fuentes citadas
   - Sugerencias de preguntas relacionadas

6. **Mejora Continua Automática**
   - Feedback positivo → Agrega a knowledge base
   - Feedback negativo → Identifica gaps
   - A/B testing de configuraciones RAG

---

## 📊 Métricas de Éxito

### KPIs a Monitorear

1. **Precisión**
   - % de respuestas que usan RAG exitosamente
   - Score de similitud promedio (debe ser >0.7)

2. **Satisfacción Usuario**
   - % de feedback positivo (meta: >80%)
   - % de respuestas con fuentes citadas

3. **Cobertura**
   - % de preguntas donde RAG encuentra contexto relevante
   - Temas sin cobertura (para agregar contenido)

4. **Performance**
   - Latencia de búsqueda vectorial (<200ms)
   - Tiempo total de respuesta (<3 segundos)

---

## 🎓 Recursos Adicionales

- **Pinecone Docs**: https://docs.pinecone.io/
- **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings
- **RAG Best Practices**: https://www.anthropic.com/index/contextual-retrieval
- **BCN LeyChile**: https://www.bcn.cl/leychile/
- **Dirección del Trabajo**: https://www.dt.gob.cl/
- **SERNAC**: https://www.sernac.cl/

---

## 💬 Preguntas Frecuentes

**P: ¿Por qué OpenAI para embeddings y no Claude?**
R: Actualmente Claude no tiene API de embeddings. OpenAI text-embedding-3-small es estado del arte, barato ($0.02/1M tokens) y rápido.

**P: ¿Puedo usar otro vector database en vez de Pinecone?**
R: Sí. El código está preparado para cambiar a Weaviate o Chroma. Pinecone es recomendado por su free tier generoso y facilidad de uso.

**P: ¿Qué pasa si el contexto no cubre la pregunta?**
R: El RAG tiene fallback a Claude sin contexto. El usuario igual recibe respuesta, pero sin fuentes citadas.

**P: ¿Cómo agrego mis propios documentos legales?**
R: Crea un JSON con formato similar a los scrapers, guárdalo en `data/raw/custom/`, y ejecuta el pipeline de procesamiento.

---

**✅ SISTEMA LISTO PARA USO**

Con este sistema RAG, JusticiaAI tiene:
- ✅ Respuestas legales precisas basadas en fuentes oficiales
- ✅ Trazabilidad y transparencia (fuentes citadas)
- ✅ Capacidad de mejora continua (agregar contenido fácilmente)
- ✅ Defensibilidad técnica (data moat)
- ✅ Costos bajos y escalables ($10-20/mes inicial)

**¡Tu chatbot legal está listo para dominar Chile!** 🇨🇱🚀
