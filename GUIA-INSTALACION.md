# 🚀 GUÍA DE INSTALACIÓN Y USO - JusticiaAI MVP

## ✅ LO QUE SE CREÓ

Tu MVP de JusticiaAI está completo con:

✅ **Frontend (Next.js + TypeScript)**
- Landing page profesional
- Chat IA funcional
- UI components (shadcn/ui)
- Responsive design

✅ **Backend (FastAPI + Claude)**
- API REST completa
- Chatbot IA con Claude 3.5 Sonnet
- System prompt especializado en leyes chilenas
- CORS configurado

✅ **Documentación**
- README completo
- Ejemplos de .env
- Esta guía de instalación

---

## ⚡ INSTALACIÓN RÁPIDA (15 minutos)

### Paso 1: Prerequisitos

Asegúrate de tener instalado:
- ✅ Node.js 20+ ([descargar](https://nodejs.org/))
- ✅ Python 3.11+ ([descargar](https://www.python.org/))
- ✅ API Key de Anthropic ([obtener gratis](https://console.anthropic.com/))

**Verificar versiones:**
```bash
node --version  # debe ser v20+
python3 --version  # debe ser 3.11+
```

---

### Paso 2: Configurar Backend (5 min)

```bash
# 1. Navegar a la carpeta backend
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend

# 2. Crear entorno virtual de Python
python3 -m venv venv

# 3. Activar el entorno virtual
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate  # En Windows

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env

# 6. Editar .env con tu API key
nano .env  # o usa cualquier editor de texto
```

**En el archivo .env, cambia:**
```env
ANTHROPIC_API_KEY=tu-api-key-real-aqui
```

**💡 ¿Dónde conseguir la API key de Anthropic?**
1. Ve a: https://console.anthropic.com/
2. Crea cuenta (gratis)
3. En "API Keys", copia tu key
4. Pégala en el `.env`

**7. Iniciar el backend:**
```bash
uvicorn main:app --reload
```

✅ **Backend corriendo en:** http://localhost:8000
✅ **API Docs:** http://localhost:8000/docs

---

### Paso 3: Configurar Frontend (5 min)

**Abre una NUEVA terminal** (deja el backend corriendo):

```bash
# 1. Navegar a la carpeta frontend
cd /Users/RobertoArcos/suite/justiciaai-mvp/frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env.local

# 4. Iniciar el frontend
npm run dev
```

✅ **Frontend corriendo en:** http://localhost:3000

---

### Paso 4: Probar el Chatbot (2 min)

1. Abre tu navegador en: **http://localhost:3000**
2. Click en el botón **"Comenzar Gratis"** o **"Hablar con IA Legal"**
3. Verás el chat con el asistente IA
4. Prueba preguntando: **"Me despidieron sin finiquito, ¿qué hago?"**

✅ **Si ves una respuesta de la IA, ¡TODO FUNCIONA!** 🎉

---

## 🐛 TROUBLESHOOTING

### Error: "ANTHROPIC_API_KEY not set"

**Problema:** No configuraste la API key en el backend.

**Solución:**
```bash
cd backend
nano .env  # edita y agrega tu key real
```

Luego reinicia el backend (Ctrl+C y vuelve a correr `uvicorn main:app --reload`)

---

### Error: "Module not found"

**Problema:** Dependencias no instaladas correctamente.

**Solución Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Solución Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### Error: "Port 3000 already in use"

**Problema:** Otro proceso está usando el puerto.

**Solución:**
```bash
# Matar el proceso en el puerto 3000
lsof -ti:3000 | xargs kill -9

# O usa otro puerto
npm run dev -- -p 3001
```

---

### Error de CORS en el chat

**Problema:** Frontend y Backend no se pueden comunicar.

**Solución:**
1. Verifica que ambos estén corriendo:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000

2. Si usas otro puerto, actualiza `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

---

## 📂 ESTRUCTURA DEL PROYECTO

```
justiciaai-mvp/
├── frontend/
│   ├── app/
│   │   ├── page.tsx          ← Landing page
│   │   ├── chat/
│   │   │   └── page.tsx      ← Chatbot IA
│   │   ├── layout.tsx        ← Layout principal
│   │   └── globals.css       ← Estilos globales
│   ├── components/
│   │   └── ui/               ← Componentes UI
│   ├── lib/
│   │   └── utils.ts          ← Utilidades
│   ├── package.json
│   └── .env.local            ← Config frontend
│
├── backend/
│   ├── main.py               ← API principal
│   ├── requirements.txt      ← Dependencias Python
│   └── .env                  ← Config backend (API keys)
│
└── README.md                 ← Documentación general
```

---

## 🎯 PRÓXIMOS PASOS

### Ahora que tienes el MVP funcionando:

**1. Personaliza el contenido:**
- Edita `frontend/app/page.tsx` para cambiar textos de la landing
- Modifica `backend/main.py` para ajustar el system prompt del asistente

**2. Agrega más features:**
- [ ] Auth (login/registro)
- [ ] Base de datos (guardar conversaciones)
- [ ] Marketplace de abogados
- [ ] Dashboard de usuario

**3. Deploy a producción:**
- **Frontend:** Deploy en Vercel (gratis)
- **Backend:** Deploy en Railway o Render (gratis tier disponible)

---

## 🚀 DEPLOY A PRODUCCIÓN

### Opción A: Vercel (Frontend) + Railway (Backend)

**Frontend en Vercel:**
```bash
cd frontend
npm install -g vercel
vercel
```

**Backend en Railway:**
1. Ve a railway.app
2. Crea cuenta
3. "New Project" → "Deploy from GitHub repo"
4. Conecta tu repo
5. Agrega variable: `ANTHROPIC_API_KEY=tu-key`

### Opción B: Todo en un VPS (DigitalOcean, AWS, etc.)

Ver guía detallada en: `docs/deployment.md` (crear después)

---

## 📊 TESTING

### Probar el backend directamente:

```bash
# Con curl:
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, tengo una consulta legal"}'

# O visita la documentación interactiva:
open http://localhost:8000/docs
```

### Probar el frontend:

```bash
cd frontend
npm run build  # Verifica que compila sin errores
npm start      # Corre la versión de producción
```

---

## 🔐 SEGURIDAD

**IMPORTANTE - Antes de deploy a producción:**

1. ✅ Nunca subas `.env` a Git
2. ✅ Usa variables de entorno en producción
3. ✅ Agrega rate limiting al API
4. ✅ Implementa autenticación
5. ✅ Usa HTTPS en producción

---

## 🆘 SOPORTE

**Si tienes problemas:**

1. **Revisa los logs:**
   - Backend: La terminal donde corre `uvicorn`
   - Frontend: La terminal donde corre `npm run dev`
   - Browser console: F12 → Console tab

2. **Verifica que todo esté corriendo:**
   ```bash
   # Backend health check
   curl http://localhost:8000/health

   # Frontend (abre en navegador)
   open http://localhost:3000
   ```

3. **Si nada funciona:**
   - Reinicia ambos servidores (Ctrl+C y vuelve a iniciar)
   - Verifica que las dependencias estén instaladas
   - Revisa que los puertos 3000 y 8000 estén libres

---

## 📝 COMANDOS ÚTILES

```bash
# === BACKEND ===
cd backend
source venv/bin/activate       # Activar entorno virtual
uvicorn main:app --reload      # Iniciar servidor dev
uvicorn main:app --host 0.0.0.0 --port 8000  # Producción
python -m pytest               # Correr tests (cuando existan)

# === FRONTEND ===
cd frontend
npm run dev                    # Desarrollo
npm run build                  # Build para producción
npm start                      # Correr producción
npm run lint                   # Linter
npm test                       # Tests (cuando existan)

# === AMBOS ===
# Terminal 1:
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de considerar el MVP completo:

**Backend:**
- [ ] Backend corre en http://localhost:8000
- [ ] Puedes ver docs en http://localhost:8000/docs
- [ ] Health check responde: http://localhost:8000/health
- [ ] Chat endpoint funciona con curl/Postman

**Frontend:**
- [ ] Frontend corre en http://localhost:3000
- [ ] Landing page se ve correctamente
- [ ] Puedes navegar a /chat
- [ ] El chat envía y recibe mensajes
- [ ] Los mensajes de la IA aparecen correctamente

**Integración:**
- [ ] El frontend se conecta al backend sin errores CORS
- [ ] El chatbot responde con contenido relevante
- [ ] Las respuestas son sobre leyes chilenas
- [ ] El asistente recomienda consultar con un abogado

---

## 🎉 ¡LISTO!

Tu MVP de JusticiaAI está funcionando. Ahora puedes:

1. **Mostrarlo a potenciales inversionistas**
2. **Hacer demos con usuarios reales**
3. **Iterar según feedback**
4. **Agregar más features**

**Próximos features recomendados:**
- Auth y perfiles de usuario
- Guardar conversaciones en DB
- Marketplace de abogados (listado)
- Sistema de match IA → Abogado
- Dashboard

---

**¿Preguntas? ¿Problemas? ¿Necesitas ayuda?**

Documentación completa en: `/README.md`

**Built with ❤️ for JusticiaAI**
