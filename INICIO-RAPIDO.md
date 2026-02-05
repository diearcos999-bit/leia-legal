# 🚀 INICIO RÁPIDO - JusticiaAI MVP

## ✅ BACKEND YA ESTÁ INSTALADO

El backend está listo. Ahora solo necesitas:

### 1. Conseguir API Key de Anthropic (5 min - GRATIS)

1. Ve a: **https://console.anthropic.com/**
2. Crea cuenta (gratis, no necesitas tarjeta)
3. Click en **"Get API Keys"**
4. Click **"Create Key"**
5. Copia la key (empieza con `sk-ant-...`)

### 2. Configurar el Backend (1 min)

Edita el archivo `.env`:

```bash
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend
nano .env
```

Cambia esta línea:
```
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

Por:
```
ANTHROPIC_API_KEY=sk-ant-tu-key-real-aqui
```

Guarda: `Ctrl+O`, Enter, `Ctrl+X`

### 3. Iniciar Backend (1 min)

**Opción A - Script rápido:**
```bash
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend
./start.sh
```

**Opción B - Manual:**
```bash
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend
source venv/bin/activate
python main_simple.py
```

✅ Verás: `🚀 Iniciando JusticiaAI Backend...`
✅ Backend en: **http://localhost:8000**

**DEJA ESTA TERMINAL ABIERTA**

---

## 📱 INSTALAR FRONTEND

**Abre una NUEVA terminal** (Cmd+T) y ejecuta:

```bash
cd /Users/RobertoArcos/suite/justiciaai-mvp/frontend
npm install
```

Esto tomará 2-3 minutos.

Luego:

```bash
cp .env.example .env.local
npm run dev
```

✅ Frontend en: **http://localhost:3000**

---

## 🎉 PROBAR EL CHATBOT

1. Abre http://localhost:3000
2. Click en **"Comenzar Gratis"**
3. Pregunta: **"Me despidieron sin finiquito, ¿qué hago?"**

Si ves una respuesta de la IA → **¡FUNCIONA!** 🎉

---

## ❌ SI NO TIENES LA API KEY AÚN

El backend arrancará pero el chat no funcionará. Verás un mensaje de error.

**Solución:**
1. Consigue la key en https://console.anthropic.com/
2. Agrégala al `.env`
3. Reinicia el backend (Ctrl+C y vuelve a correr)

---

## 🆘 PROBLEMAS COMUNES

**"Port 8000 already in use"**
```bash
lsof -ti:8000 | xargs kill -9
```

**"Module not found"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements-simple.txt
```

---

## 📝 RESUMEN DE COMANDOS

```bash
# Terminal 1 - Backend
cd /Users/RobertoArcos/suite/justiciaai-mvp/backend
source venv/bin/activate
python main_simple.py

# Terminal 2 - Frontend
cd /Users/RobertoArcos/suite/justiciaai-mvp/frontend
npm install
npm run dev
```

---

**¡Listo! Tu MVP de JusticiaAI está funcionando!** 🚀
