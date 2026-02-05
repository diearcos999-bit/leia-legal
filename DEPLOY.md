# LEIA - Guia de Deploy a Produccion

## Arquitectura

```
[Vercel - Frontend]  <-->  [Railway - Backend + PostgreSQL]
     Next.js                    FastAPI + SQLite/PostgreSQL
```

---

## PASO 1: Deploy Backend en Railway

### 1.1 Crear cuenta y proyecto

1. Ve a [railway.app](https://railway.app)
2. Inicia sesion con GitHub
3. Click en **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Conecta tu repositorio y selecciona la carpeta `backend`

### 1.2 Configurar variables de entorno

En Railway Dashboard > Variables, agrega:

| Variable | Valor | Requerido |
|----------|-------|-----------|
| `ANTHROPIC_API_KEY` | tu-api-key | Si |
| `CORS_ORIGINS` | https://tu-app.vercel.app | Si |
| `ENVIRONMENT` | production | Si |
| `OPENAI_API_KEY` | tu-api-key | No (para RAG) |
| `PINECONE_API_KEY` | tu-api-key | No (para RAG) |

### 1.3 Configurar el servicio

1. En Settings > Build:
   - Root Directory: `/backend`
   - Build Command: (dejar vacio, usa nixpacks)
   - Start Command: `uvicorn main_simple:app --host 0.0.0.0 --port $PORT`

2. En Settings > Networking:
   - Click "Generate Domain" para obtener URL publica

### 1.4 Agregar PostgreSQL (Opcional pero recomendado)

1. En tu proyecto Railway, click **"+ New"**
2. Selecciona **"Database" > "PostgreSQL"**
3. Railway agregara automaticamente `DATABASE_URL`

### 1.5 Verificar deploy

Visita: `https://tu-app.railway.app/health`

Deberia mostrar:
```json
{"status": "healthy", "service": "leia-backend"}
```

---

## PASO 2: Deploy Frontend en Vercel

### 2.1 Conectar repositorio

1. Ve a [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Importa tu repositorio de GitHub
4. **IMPORTANTE**: En "Root Directory", selecciona `frontend`

### 2.2 Configurar variables de entorno

En Vercel > Settings > Environment Variables:

| Variable | Valor |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | https://tu-backend.railway.app |

### 2.3 Deploy

1. Click **"Deploy"**
2. Espera a que termine el build
3. Vercel te dara una URL como `https://leia-xxx.vercel.app`

### 2.4 Actualizar CORS en Railway

Vuelve a Railway y actualiza la variable `CORS_ORIGINS` con tu URL de Vercel:

```
CORS_ORIGINS=https://leia-xxx.vercel.app
```

---

## PASO 3: Dominio personalizado (Opcional)

### En Vercel (Frontend)
1. Settings > Domains
2. Agrega tu dominio (ej: `leia.cl`)
3. Configura DNS segun instrucciones de Vercel

### En Railway (Backend)
1. Settings > Networking > Custom Domain
2. Agrega subdominio (ej: `api.leia.cl`)
3. Configura DNS

Actualiza `CORS_ORIGINS` y `NEXT_PUBLIC_API_URL` con los nuevos dominios.

---

## Checklist Final

- [ ] Backend deployado en Railway
- [ ] `/health` responde correctamente
- [ ] Frontend deployado en Vercel
- [ ] Variables de entorno configuradas en ambos
- [ ] CORS configurado correctamente
- [ ] Chat funciona en produccion
- [ ] Login/Registro funciona
- [ ] Busqueda de abogados funciona

---

## Troubleshooting

### Error CORS
- Verifica que `CORS_ORIGINS` en Railway incluya tu URL de Vercel
- La URL debe ser exacta, sin trailing slash

### Chat no funciona
- Verifica `ANTHROPIC_API_KEY` en Railway
- Revisa logs en Railway Dashboard

### Base de datos
- Railway SQLite funciona pero se reinicia con deploys
- Para persistencia, agrega PostgreSQL

---

## Costos estimados

| Servicio | Plan Gratuito | Limite |
|----------|--------------|--------|
| Vercel | Hobby | 100GB bandwidth/mes |
| Railway | Trial | $5 creditos, luego $5/mes |

Para un MVP, ambos tiers gratuitos son suficientes.
