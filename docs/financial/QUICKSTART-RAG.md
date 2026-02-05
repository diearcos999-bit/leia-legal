# 🚀 QUICKSTART - Sistema RAG en 10 Minutos

## ✅ Checklist Rápida

### Paso 1: Instalar Dependencias (2 min)

```bash
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend

pip install openai pinecone-client beautifulsoup4 pyyaml
```

### Paso 2: Configurar API Keys (3 min)

```bash
# Copiar template
cp .env.example .env

# Editar archivo
nano .env
```

**Agregar 2 nuevas keys:**

1. **OpenAI** (para embeddings)
   - Ve a: https://platform.openai.com/api-keys
   - Crea key → Copia
   - Pega en `.env`: `OPENAI_API_KEY=sk-...`

2. **Pinecone** (vector database gratis)
   - Ve a: https://app.pinecone.io/
   - Sign up → Settings → API Keys → Create
   - Pega en `.env`: `PINECONE_API_KEY=...`

### Paso 3: Ejecutar Pipeline Completo (5 min)

```bash
# Un solo comando hace todo:
python run_rag_pipeline.py
```

**Esto ejecuta automáticamente:**
- ✅ Descarga leyes chilenas (BCN, DT, SERNAC)
- ✅ Procesa y limpia textos
- ✅ Genera embeddings (OpenAI)
- ✅ Sube vectores a Pinecone
- ✅ Verifica que todo funciona

**Costo**: ~$0.10 USD

### Paso 4: Probar en Chat (1 min)

```bash
# Asegúrate que backend esté corriendo
python main_simple.py
```

1. Abre: http://localhost:3001/chat
2. Pregunta: **"¿Qué es el finiquito?"**
3. ✅ Verifica que cite fuentes oficiales

---

## 🎯 Cómo Saber que Funciona

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

**Debe mostrar:**
```json
{
  "rag_enabled": true
}
```

### Test 2: Respuesta con Fuentes

Pregunta en chat: *"¿Qué es el finiquito?"*

**Respuesta DEBE incluir:**
- ✅ "Según el Código del Trabajo..."
- ✅ "Artículo X..."
- ✅ Referencias a DT o leyes específicas

### Test 3: Logs del Backend

En consola del backend verás:

```
✅ RAG Engine inicializado correctamente
✅ Conectado a índice existente: justiciaai-legal
```

---

## ❓ Troubleshooting Rápido

### Error: "Pinecone API key no configurada"

```bash
# Verifica .env
cat .env | grep PINECONE_API_KEY

# Si está vacío, agrégala:
echo "PINECONE_API_KEY=tu-key-aquí" >> .env
```

### Error: "OpenAI API key no configurada"

```bash
# Verifica .env
cat .env | grep OPENAI_API_KEY

# Si está vacío, agrégala:
echo "OPENAI_API_KEY=sk-..." >> .env
```

### RAG no funciona en el chat

1. Revisa logs del backend al iniciar
2. Verifica: `curl http://localhost:8000/health`
3. Si `rag_enabled: false`, ejecuta pipeline de nuevo

---

## 📚 Documentación Completa

- **README-RAG.md**: Guía detallada (10 páginas)
- **SISTEMA-RAG-COMPLETADO.md**: Resumen ejecutivo
- **config.yaml**: Configuración del sistema

---

## ✨ ¡Listo!

En 10 minutos tienes un chatbot legal con RAG funcionando.

**Próximo paso**: Demostrar a inversionistas que tu chatbot usa IA avanzada con fuentes verificadas.

🚀🇨🇱
