# PLAN DE ACCIÓN: Pitch Deck JusticiaAI
## Meta: Deck listo en 2-3 sesiones (8-12 horas total)

---

## SESIÓN 1: Setup + Slides 1-5 (3-4 horas)

### ANTES DE EMPEZAR ✅
- [ ] Crear cuenta Figma (figma.com)
- [ ] Preparar logo o idea de logo (puede ser texto estilizado por ahora)
- [ ] Tener foto profesional tuya (para slide de equipo)
- [ ] Decidir información personal: email, teléfono, LinkedIn

---

### PASO 1: Setup Inicial en Figma (30 min)

1. **Crear Proyecto**
   - Ir a figma.com → "New design file"
   - Nombrar: "JusticiaAI Pitch Deck"

2. **Crear Frame Base**
   - Presiona `F` (Frame tool)
   - Selecciona "Presentation" → "1920 × 1080"
   - Nombrar: "Slide 1 - Cover"

3. **Instalar Plugins Esenciales**
   - Menu → Plugins → Browse
   - Instalar:
     - **Iconify** (íconos gratis)
     - **Unsplash** (fotos stock)
     - **Charts** (gráficos)
     - **Content Reel** (placeholder)

---

### PASO 2: Design System (45 min)

#### Colores

1. Click en rectángulo tool `R`
2. Crear 10 rectángulos pequeños (100x100)
3. Para cada uno:
   - Seleccionar → Panel derecho → Fill
   - Ingresar color
   - Click en color swatch → "+" → "Create style"
   - Nombrar

**Colores a crear:**
```
Primary/Blue-800:  #1E40AF
Primary/Blue-600:  #2563EB
Primary/Blue-100:  #DBEAFE

Secondary/Green-500: #10B981
Secondary/Amber-500: #F59E0B

Text/Gray-900:     #111827
Text/Gray-600:     #4B5563

Background/Gray-50: #F9FAFB
Background/White:   #FFFFFF

Border/Gray-300:    #D1D5DB
```

#### Tipografía

1. Presiona `T` (Text tool)
2. Escribir "Heading 1"
3. Configurar:
   - Font: Inter (búscala en dropdown)
   - Weight: Bold
   - Size: 64
   - Line height: 120%
   - Color: Gray-900
4. Seleccionar texto → Panel derecho → "..." → "Create style"
5. Nombrar: "Heading 1"

**Repetir para:**
- **Heading 2**: Inter SemiBold, 48px, 120%, Gray-900
- **Heading 3**: Inter SemiBold, 32px, 130%, Gray-900
- **Body Large**: Inter Regular, 24px, 150%, Gray-600
- **Body**: Inter Regular, 20px, 150%, Gray-600
- **Caption**: Inter Regular, 16px, 140%, Gray-500

---

### PASO 3: Slide 1 - Cover (30 min)

**Layout:**
```
┌─────────────────────────────┐
│                             │
│      [Logo JusticiaAI]      │
│                             │
│   Democratizando el acceso  │
│   a justicia en Chile con IA│
│                             │
│      [Ilustración]          │
│                             │
│   Roberto Arcos             │
│   Founder & CEO             │
│   [tu-email@justiciaai.cl]  │
│                             │
│   Buscando $400K USD        │
│   Ronda Semilla • Enero 2025│
└─────────────────────────────┘
```

**Paso a paso:**

1. **Background gradient**
   - Selecciona frame
   - Fill → Gradient → Linear
   - Stop 1: #EFF6FF (top)
   - Stop 2: #FFFFFF (bottom)

2. **Logo placeholder** (mientras no tengas logo)
   - Text tool `T`
   - Escribe "JusticiaAI"
   - Font: Inter Bold, 72px
   - Color: Blue-800
   - Centrar horizontalmente (panel derecho → Align horizontal center)

3. **Tagline**
   - Text tool `T`
   - Escribe: "Democratizando el acceso a justicia en Chile con IA"
   - Apply style: "Heading 2"
   - Centrar

4. **Ilustración**
   - Plugins → Unsplash
   - Buscar: "legal consultation" o "justice technology"
   - Arrastrar imagen al canvas
   - Resize: 600px width
   - Centrar

5. **Tu información**
   - Text tool, escribe:
     ```
     Roberto Arcos
     Founder & CEO
     [tu-email]
     ```
   - Style: Body
   - Centrar

6. **Funding ask**
   - Text tool:
     ```
     Buscando $400K USD
     Ronda Semilla • Enero 2025
     ```
   - Style: Body Large
   - Color: Blue-600
   - Centrar

7. **Espaciado**
   - Selecciona todos los elementos (Cmd+A o arrastra)
   - Panel derecho → Auto layout (Shift+A)
   - Spacing: 48px
   - Alignment: Center

---

### PASO 4: Slide 2 - Problem (45 min)

**Datos exactos a usar:**
- 70% de chilenos no puede acceder a justicia
- $500K+ cuesta un divorcio simple
- 79% no entiende el sistema judicial
- 400+ días toman procesos promedio
- 1.5M personas con problemas sin resolver anualmente

**Layout:**
```
┌─────────────────────────────┐
│ El Problema                 │
│                             │
│ 70% de los chilenos         │
│ no puede acceder a justicia │
│                             │
│ [4 problemas en grid 2x2]   │
│                             │
│ = 1.5M personas sin ayuda   │
└─────────────────────────────┘
```

**Paso a paso:**

1. **Duplicar slide**
   - Click derecho en Frame 1 → Duplicate
   - Nombrar: "Slide 2 - Problem"
   - Borrar todo el contenido

2. **Título**
   - Text `T`: "El Problema"
   - Style: Heading 1
   - Posición: Top-left (64px margin)

3. **Hero stat**
   - Text: "70% de los chilenos no puede acceder a justicia"
   - Font: Inter Bold, 56px
   - Color: Blue-600
   - Centrar horizontalmente
   - Posición Y: ~200px

4. **Grid de problemas** (4 cards)

   Para cada card:
   - Rectangle `R`: 400×200px
   - Fill: White
   - Border: 1px Gray-300
   - Corner radius: 16px
   - Shadow: 0 4px 6px rgba(0,0,0,0.05)

   **Card 1: Costos**
   - Plugins → Iconify → Buscar "dollar-sign"
   - Insertar ícono, color Blue-600, size 48px
   - Text: "Costos Prohibitivos" (Heading 3)
   - Text: "$500K+ por divorcio simple" (Body)
   - Agrupar todo → Auto layout vertical, spacing 12px

   **Card 2: Complejidad**
   - Ícono: "help-circle"
   - "Complejidad"
   - "79% no entiende el sistema"

   **Card 3: Demoras**
   - Ícono: "clock"
   - "Demoras"
   - "400+ días procesos promedio"

   **Card 4: Información**
   - Ícono: "info"
   - "Desinformación"
   - "No conocen sus derechos"

5. **Posicionar grid**
   - Seleccionar las 4 cards
   - Auto layout (Shift+A)
   - Direction: Horizontal wrap
   - Spacing: 32px
   - Centrar en slide

6. **Stat final**
   - Text: "= 1.5M personas con problemas sin resolver anualmente"
   - Font: Inter Bold, 32px
   - Color: Amber-500
   - Posición: Bottom center

---

### PASO 5: Slide 3 - Solution (45 min)

**Datos exactos:**
- IA Legal 24/7 en leyes chilenas
- Marketplace con abogados verificados
- Automatización de documentos e integraciones

**Layout:**
```
┌─────────────────────────────┐
│ La Solución                 │
│                             │
│ [Phone mockup]  [3 features]│
│  con chatbot       vertical │
│                             │
│ = LawConnect para LATAM     │
└─────────────────────────────┘
```

**Paso a paso:**

1. **Duplicar slide anterior**
   - Nombrar: "Slide 3 - Solution"
   - Limpiar contenido

2. **Título**
   - "La Solución" (Heading 1)

3. **Phone mockup** (Left side)

   Opción A - Con plugin:
   - Plugins → "Mockuuups Studio"
   - Seleccionar iPhone
   - Insertar screenshot de chatbot (ver SLIDE-DATA-GUIDE.md)

   Opción B - Manual:
   - Frame `F`: 375×812px (iPhone size)
   - Fill: White
   - Border: 4px black
   - Corner radius: 48px
   - Dentro: Crear simulación de chat
     - Burbujas azules (mensajes bot)
     - Burbujas grises (mensajes user)
   - Shadow: 0 20px 25px rgba(0,0,0,0.15)

4. **3 Features** (Right side)

   **Feature 1:**
   - Ícono: "bot" (Iconify)
   - Title: "IA Legal Gratuita" (Heading 3)
   - Text: "Orientación 24/7 en leyes chilenas, lenguaje simple" (Body)

   **Feature 2:**
   - Ícono: "users"
   - Title: "Marketplace Verificado"
   - Text: "Abogados con reviews, precios transparentes, match inteligente"

   **Feature 3:**
   - Ícono: "zap"
   - Title: "Automatización"
   - Text: "Documentos legales, integración tribunales, seguimiento"

   Agrupar cada feature → Auto layout vertical

5. **Posicionamiento**
   - Phone: Left, 25% del ancho
   - Features: Right, 65% del ancho
   - Centrar verticalmente

6. **Bottom tagline**
   - "= LawConnect + LegalZoom para LATAM"
   - Body Large, Blue-600
   - Bottom center

---

### PASO 6: Slide 4 - Market Opportunity (30 min)

**Datos exactos:**
- TAM: $2,000M (mercado legal Chile)
- SAM: $450M (digitalizable)
- SOM (Año 3): $10-15M (2-3% captura)

**Visual: Círculos concéntricos**

**Paso a paso:**

1. **Título**
   - "Oportunidad de Mercado" (Heading 1)

2. **Círculos concéntricos**

   - Circle tool `O`
   - Círculo 1: 500px diameter
     - Fill: Blue-100, opacity 60%
     - Label: "TAM: $2,000M"

   - Círculo 2: 350px diameter (centrado en círculo 1)
     - Fill: Blue-300, opacity 60%
     - Label: "SAM: $450M"

   - Círculo 3: 200px diameter (centrado)
     - Fill: Blue-600
     - Label: "SOM (Y3): $10-15M"

3. **Labels con líneas**
   - Line tool `L`
   - Desde borde de cada círculo hacia afuera
   - Text al final de línea con nombres y cifras

4. **Bottom stat**
   - "Capturar 2-3% del mercado = $3.3M ARR en Año 3"
   - Heading 3, Green-500

---

### PASO 7: Slide 5 - Business Model (30 min)

**Datos exactos:**
- 5 fuentes de ingreso
- Comisiones 25% (40% de ingresos)
- Suscripciones $55-135/mes (25%)
- Automatizados $10-50 (20%)
- B2B $200-1K/mes (10%)
- Partnerships (5%)
- LTV/CAC: 2.5x en Año 3

**Paso a paso:**

1. **Título**
   - "Modelo de Negocio" (Heading 1)

2. **Subtítulo**
   - "5 Fuentes de Ingreso Escalables"
   - Heading 2

3. **5 Revenue streams** (vertical list)

   Para cada stream (usar icons de Iconify):
   - Rectangle 800×100px
   - Auto layout horizontal
   - Spacing 24px
   - Contenido:
     - Ícono (48px)
     - Nombre (Heading 3)
     - % ingreso (Body, Blue-600)
     - Detalles (Caption)

   **Stream 1:**
   - Ícono: percentage
   - "Comisiones" | 40% | "20-30% sobre honorarios"

   **Stream 2:**
   - Ícono: repeat
   - "Suscripciones" | 25% | "$55-135/mes por abogado"

   **Stream 3:**
   - Ícono: file-text
   - "Automatizados" | 20% | "$10-50 por documento"

   **Stream 4:**
   - Ícono: briefcase
   - "B2B Corporativo" | 10% | "$200-1K/mes empresas"

   **Stream 5:**
   - Ícono: handshake
   - "Partnerships" | 5% | "Seguros, alianzas"

4. **Unit Economics destacado**
   - Rectangle grande, background Green-50
   - "LTV/CAC: 2.5x (Año 3)"
   - Font: Inter Bold, 40px
   - Color: Green-500
   - Bottom center

---

## CHECKPOINT SESIÓN 1 ✅

Has completado:
- ✅ Setup completo de Figma
- ✅ Design system (colores + tipografía)
- ✅ 5 slides fundamentales

**Resultado:** Ya tienes 35% del deck completo (5 de 14 slides).

**Próxima sesión:** Slides 6-10 (traction, competition, GTM, team, financials)

---

## SESIÓN 2: Slides 6-10 (3-4 horas)

### PASO 8: Slide 6 - Traction (30 min)

**Elegir versión según tu estado:**

#### Opción A: Pre-Launch

**Datos a mostrar:**
- Waiting list: [X] personas (si tienes)
- Abogados comprometidos: [X]
- LOIs/partnerships: [X]
- Roadmap: MVP (1-3), Beta (4-6), Scale (7-12)

**Layout: 3 stat boxes + Timeline**

1. **Stat boxes** (horizontal)
   - 3 rectangles: 300×200px cada uno
   - Background: White
   - Border: 2px Blue-600
   - Corner radius: 16px

   Box 1:
   - Number: "[X]" (72px Bold, Blue-600)
   - Label: "Waiting List" (Body)

   Box 2:
   - Number: "[X]"
   - Label: "Abogados Interesados"

   Box 3:
   - Number: "[X]"
   - Label: "LOIs Partners"

2. **Timeline visual**
   - Line tool: horizontal 800px
   - 3 puntos marcados
   - Text arriba de cada punto:
     - "Mes 1-3: MVP"
     - "Mes 4-6: Beta (100 casos)"
     - "Mes 7-12: $50K MRR"

#### Opción B: Post-Launch

(Si ya lanzaste, usar métricas reales)

**Datos:**
- Usuarios: [X]
- Abogados: [X]
- Casos completados: [X]
- MRR: $[X]K

**Layout similar pero con gráfico de crecimiento:**
- Usar plugin "Charts"
- Line chart mostrando MRR growth
- Gradient fill bajo la línea

---

### PASO 9: Slide 7 - Competition (30 min)

**Datos:**
- Única plataforma con IA legal en Chile
- Total Abogados: sin IA, red cerrada
- Marketplaces: pequeños, sin diferenciación

**Layout: Tabla comparativa**

1. **Título**
   - "Landscape Competitivo" (Heading 1)

2. **Subtítulo**
   - "Única con IA Legal Avanzada" (Heading 2, Blue-600)

3. **Tabla** (manual)

   Headers:
   - Crear rectangles para celdas: 180px width
   - Background: Blue-600 para header row
   - Text: White, Body, Bold

   Columnas:
   - [Blank] | IA | Marketplace | Auto | B2B

   Filas:
   - JusticiaAI | ✅ | ✅ | ✅ | ✅
   - Total Abogados | ❌ | ❌ | ⚠️ | ❌
   - Marketplaces | ❌ | ✅ | ❌ | ❌
   - CAJ | ❌ | ❌ | ❌ | ❌

   **Tip:** Copy-paste emojis (✅ ❌ ⚠️)

4. **Highlight JusticiaAI row**
   - Background: Blue-50

5. **Bottom moat**
   - "Ventaja: 6-12 meses antes que competencia construya IA"
   - Body Large, Amber-500

---

### PASO 10: Slide 8 - Go-to-Market (30 min)

**Datos:**
- Funnel: 100K visitors → 3% conversion → 3K customers
- Canales: SEO, SEM, Social, Partners

**Layout: Funnel visual**

1. **Título**
   - "Estrategia de Lanzamiento"

2. **Funnel** (trapezoid shapes)

   Crear 5 trapezoides apilados (más ancho arriba):

   **Level 1:**
   - Rectangle 800px width, 80px height
   - "100K Visitors"

   **Level 2:**
   - 700px width
   - "5K Registered (5% CTR)"

   **Level 3:**
   - 600px width
   - "1K Chat IA (20%)"

   **Level 4:**
   - 500px width
   - "200 Request Lawyer (20%)"

   **Level 5:**
   - 400px width
   - "100 Customers (50%)"

   **Gradiente de color:** Blue-100 arriba → Blue-600 abajo

3. **Arrows entre levels**
   - Line tool con flecha
   - Label con % conversión

4. **Canales** (bottom)
   - 4 íconos horizontales
   - Iconify: "search", "megaphone", "users", "handshake"
   - Labels: SEO, SEM, Social, Partners

---

### PASO 11: Slide 9 - Team (45 min)

**Datos:**
- Tu perfil: Roberto Arcos, Founder & CEO
- Tu experiencia: [agregar]
- CTO: [si ya tienes]
- Asesores: [si ya tienes]
- Hiring: AI/ML Engineer, 2 Developers

**Layout: Profile cards**

1. **Título**
   - "Equipo" (Heading 1)

2. **Tu profile card**

   Rectangle 900×200px:
   - Background: White
   - Border: 1px Gray-300
   - Corner radius: 16px
   - Auto layout horizontal, spacing 32px

   Contenido:
   - **Foto** (left):
     - Circle 150×150px
     - Insertar tu foto
     - O placeholder de UI Faces (Google: "UI faces generator")

   - **Info** (right):
     - "Roberto Arcos" (Heading 2)
     - "Founder & CEO" (Body, Gray-600)
     - Bullets (Body):
       - "• [Tu experiencia relevante]"
       - "• [Logro destacado]"
       - "• [Skills: producto, legal-tech, fundraising]"

3. **CTO card** (si aplica)
   - Similar layout
   - Placeholder si no tienes aún:
     - "CTO - En búsqueda"
     - Skills deseados

4. **Asesores** (smaller)
   - Texto simple:
     - "Asesores:"
     - "[Nombre] - [Cargo] en [Empresa]"
     - "[Nombre] - [Expertise]"

5. **Hiring**
   - Rectangle con background Blue-50
   - "Buscando: AI/ML Engineer, 2 Full-Stack Developers"
   - Body Large

---

### PASO 12: Slide 10 - Financials (45 min)

**Datos exactos:**
- Año 1: $66K ARR
- Año 2: $734K ARR
- Año 3: $3.3M ARR
- Gross Margin: 60% → 85%
- LTV/CAC: 1.0x → 2.5x

**Layout: Bar chart + metrics**

1. **Título**
   - "Proyecciones Financieras" (Heading 1)

2. **Subtítulo**
   - "Path to $3M+ ARR en 3 años" (Heading 2, Blue-600)

3. **Bar chart**

   Manual:
   - Rectangle tool para cada barra
   - Heights proporcionales:
     - Y1: 60px ($66K)
     - Y2: 660px ($734K)
     - Y3: 3000px ($3.3M) ← ajustar para fit
   - Width: 200px cada una
   - Spacing: 80px
   - Color: Blue-600

   Labels arriba de cada barra:
   - "$66K" (Y1)
   - "$734K" (Y2)
   - "$3.3M" (Y3)
   - Font: Inter Bold, 36px

   Arrows entre barras:
   - "+1,012%" (Y1→Y2)
   - "+349%" (Y2→Y3)
   - Caption, Green-500

4. **Metrics** (bottom)

   3 bullets:
   - "• Gross Margin: 60% → 85%"
   - "• LTV/CAC: 1.0x → 2.5x"
   - "• Break-even: Q4 Año 2"
   - Body Large

---

## CHECKPOINT SESIÓN 2 ✅

Has completado:
- ✅ 10 slides totales (70% del deck)
- ✅ Todos los slides de contenido core

**Próxima sesión:** Últimos 4 slides + polish final

---

## SESIÓN 3: Slides 11-14 + Polish (2-3 horas)

### PASO 13: Slide 11 - Funding Ask (30 min)

**Datos:**
- Buscando: $300-500K USD (proponer $400K)
- Equity: 15-20%
- Uso: 40% Dev, 30% Marketing, 20% Ops, 10% Legal
- Milestones: MVP (3m), 100 casos (6m), $50K MRR (12m)
- Runway: 18 meses

**Layout: Pie chart + milestones**

1. **Título principal**
   - "Buscamos $400K USD"
   - Font: Inter Bold, 64px, Blue-600
   - Centrar top

2. **Subtítulo**
   - "Ronda Semilla • 15-20% equity"
   - Body Large, Gray-600

3. **Pie chart**

   Opción A - Plugin "Charts":
   - Insert → Plugins → Charts
   - Pie chart
   - Data:
     - Desarrollo: 40%
     - Marketing: 30%
     - Operaciones: 20%
     - Legal: 10%
   - Colors: Shades of blue

   Opción B - Manual (si plugin no funciona):
   - 4 rectangles verticales proporcionales
   - Bar chart simple

4. **Legend** (right side)
   - 40% Desarrollo → $160K
   - 30% Marketing → $120K
   - 20% Operaciones → $80K
   - 10% Legal → $40K
   - Body

5. **Milestones** (bottom)

   3 checkmarks:
   - "✓ MVP en 3 meses"
   - "✓ 100 casos en 6 meses"
   - "✓ $50K MRR en 12 meses"
   - Heading 3, Green-500

6. **Runway**
   - "Runway: 18 meses"
   - Body Large, bottom right

---

### PASO 14: Slide 12 - Why Now (30 min)

**Datos:**
- Ventana tecnológica: Claude 3.5 hace IA legal viable
- Ventana competitiva: 6-12 meses de ventaja
- Regulación: Ley 21.719, Poder Judicial adopta IA
- Post-COVID: Digitalización permanente

**Layout: 4 reasons vertical**

1. **Título**
   - "¿Por Qué Ahora?" (Heading 1)

2. **4 Reasons** (vertical stack)

   Card template:
   - Rectangle 900×150px
   - Background: White
   - Border: 1px Gray-300
   - Corner radius: 12px
   - Auto layout horizontal, spacing 24px

   **Reason 1: Tecnología**
   - Ícono: "zap" (Iconify, 56px, Amber-500)
   - Title: "Ventana Tecnológica" (Heading 3)
   - Bullets:
     - "Claude 3.5 hace viable IA legal"
     - "First-mover advantage"

   **Reason 2: Competencia**
   - Ícono: "trophy" (56px, Blue-600)
   - Title: "Ventana Competitiva"
   - Bullets:
     - "Total Abogados sin IA aún"
     - "6-12 meses para adelantarnos"

   **Reason 3: Regulación**
   - Ícono: "trending-up" (56px, Green-500)
   - Title: "Momentum Regulatorio"
   - Bullets:
     - "Ley 21.719 impulsa legaltech"
     - "Poder Judicial adopta IA 2025"

   **Reason 4: Mercado**
   - Ícono: "globe" (56px, Blue-600)
   - Title: "Post-COVID"
   - Bullets:
     - "Digitalización acelerada"
     - "Usuarios listos para legal online"

3. **Spacing**
   - 32px entre cada card
   - Centrar verticalmente

---

### PASO 15: Slide 13 - Vision (30 min)

**Datos:**
- Año 1-2: Dominar Chile (50K users, 1K abogados)
- Año 3+: Expandir LATAM (Perú, Colombia, Argentina)
- Impacto: 100K+ personas, 5K+ abogados, millones ahorrados

**Layout: Mapa + milestones**

1. **Título**
   - "Visión" (Heading 1)

2. **Mapa de LATAM**

   Opción A - Imagen:
   - Google: "Latin America map vector"
   - Descargar PNG simple
   - Insertar en Figma
   - Resize: 500px height

   Opción B - Simplificado:
   - Usar shapes para representar Chile, Perú, Colombia, Argentina
   - Chile: Blue-600 (bright)
   - Otros: Blue-300 (dimmed)

3. **Pins en mapa**
   - Circle 24px
   - Fill: Blue-600 para Chile
   - Fill: Blue-300 para otros países

4. **Timeline** (right side)

   **Año 1-2:**
   - "Dominamos Chile"
   - Bullets:
     - "#1 marketplace legal"
     - "50K+ usuarios"
     - "1,000+ abogados"

   **Año 3+:**
   - "Expandimos LATAM"
   - Bullets:
     - "Perú, Colombia, Argentina"
     - "200M+ personas alcanzadas"

5. **Impacto** (bottom)

   3 stats horizontales:
   - "100K+ personas con acceso a justicia"
   - "5K+ abogados empoderados"
   - "Millones ahorrados en costos"
   - Font: Inter Bold, 24px, Green-500

6. **Tagline final**
   - "Tecnología al servicio de la justicia"
   - Heading 2, Center

---

### PASO 16: Slide 14 - Contact (20 min)

**Datos:**
- Tu nombre
- Email: [tu-email@justiciaai.cl]
- Teléfono: [+56 9 XXXX XXXX]
- LinkedIn: [tu-perfil]

**Layout: Clean, centrado**

1. **Background**
   - Gradient sutil (como Slide 1)
   - Blue-50 → White

2. **CTA headline** (top)
   - "¿Listos para democratizar la justicia en Chile?"
   - Heading 1
   - Centrar

3. **Logo** (center)
   - Si tienes logo, usar
   - Si no: "JusticiaAI" texto (72px)

4. **Tu info** (center)
   - "Roberto Arcos"
   - "Founder & CEO"
   - Blank line
   - "📧 [email]"
   - "📱 [teléfono]"
   - "💼 [LinkedIn URL]"
   - Body Large, spacing 16px

5. **QR Code** (bottom)
   - Plugins → "QR Code Generator"
   - URL: Link a Google Drive con deck + docs
   - Size: 200×200px
   - Caption: "Pitch deck + Data room"

6. **Spacing**
   - Todo centrado vertical y horizontal
   - 64px entre secciones

---

### PASO 17: Polish Final (60 min)

#### 1. Slide Numbers (10 min)

Para cada slide:
- Text tool
- Bottom right corner (32px margin)
- "[número] / 14"
- Caption style
- Color: Gray-500

**Tip:** Crear component y reusarlo

#### 2. Consistencia Visual (20 min)

Revisar TODOS los slides:

**Spacing:**
- Margins consistentes: 64px top/bottom, 80px left/right
- Between elements: 48px (major), 24px (minor)

**Alignment:**
- Títulos: Left aligned, 64px from top
- Contenido: Centrado o left aligned consistentemente
- Bottom elements: 64px from bottom

**Colors:**
- Solo usar colors de tu palette (no hardcoded)
- Blue-600 para highlights
- Green-500 para success/growth
- Amber-500 para urgency

**Typography:**
- Verificar que uses text styles (no custom)
- Sizes consistentes

**Tip:** Usa la herramienta de Figma "Design Lint" (plugin) para detectar inconsistencias

#### 3. Transiciones (10 min)

En Figma:
- Prototype tab (panel derecho)
- Conectar slides con flechas
- Interaction: "On click"
- Animation: "Instant" o "Dissolve" (200ms)

#### 4. Animaciones Sutiles (20 min) [OPCIONAL]

Si quieres impresionar:

Para elementos que aparecen:
- Seleccionar elemento
- Prototype tab
- "After delay" → "Fade in"
- Duration: 300ms

**Usar con moderación:**
- Stat boxes (fade in)
- Charts (fade in)
- Icons (fade in)

**NO animar:**
- Títulos
- Texto body
- Backgrounds

#### 5. Test Run (10 min)

1. Present mode: `Cmd + Enter`
2. Revisar TODO el deck
3. Verificar:
   - ¿Se lee todo desde 2 metros?
   - ¿Colores consistentes?
   - ¿Sin typos?
   - ¿Flujo lógico?
   - ¿Timing: ~1 min/slide?

---

### PASO 18: Export Final (15 min)

#### 1. PDF para Email

1. File → Export
2. Format: PDF
3. Settings:
   - Pages: All
   - Quality: High
4. Save as: "JusticiaAI-PitchDeck-[Fecha].pdf"

#### 2. PNG para Backup

1. Seleccionar todos los frames
2. Export → PNG
3. Scale: 2x (high res)
4. Save all

#### 3. Figma Link

1. Click "Share" (top right)
2. "Get link"
3. Settings:
   - "Anyone with the link can view"
   - Enable "Allow copying"
4. Copy link

#### 4. Versión para Presentar

**Opción A - Figma (recomendado):**
- Present mode: `Cmd + Enter`
- Full screen, clean
- Navegar con flechas

**Opción B - Google Slides/Keynote:**
- Importar PDF
- Agregar speaker notes
- Más seguro para entorno corporativo

---

## FINAL CHECKLIST ✅

Antes de enviar/presentar:

### Visual
- [ ] Todos los textos legibles desde 3 metros
- [ ] Colores consistentes (palette, no hardcoded)
- [ ] Spacing uniforme (64px margins, 48px between)
- [ ] Imágenes high-res (no pixeladas)
- [ ] Sin lorem ipsum o placeholders

### Contenido
- [ ] Todos los números correctos y actualizados
- [ ] Tu información de contacto correcta
- [ ] Sin typos (spell check)
- [ ] Datos consistentes entre slides
- [ ] Storytelling fluye lógicamente

### Técnico
- [ ] PDF exporta correctamente
- [ ] Slide numbers en todos (1/14 ... 14/14)
- [ ] Figma link funciona (test en incógnito)
- [ ] QR code funciona
- [ ] Backup en USB + cloud

### Presentación
- [ ] Practicado 3+ veces
- [ ] Timing: 8-10 minutos
- [ ] Responses a objeciones preparadas
- [ ] Demo lista (si aplica)
- [ ] Follow-up email template listo

---

## ENTREGABLES FINALES 📦

Al completar este plan tendrás:

1. **Figma file** completo y editable
2. **PDF** para enviar pre-meeting
3. **PNGs** de slides individuales
4. **Figma link** para compartir
5. **Presenter notes** (si usas Keynote/Slides)

---

## TIEMPO TOTAL ESTIMADO

- Sesión 1 (Setup + 5 slides): 3-4 horas
- Sesión 2 (5 slides): 3-4 horas
- Sesión 3 (4 slides + polish): 2-3 horas

**TOTAL: 8-12 horas** distribuidas en 2-3 días

---

## TIPS PRO 💡

1. **Trabaja en bloques:** 90 min trabajo, 15 min break
2. **Guarda frecuentemente:** Figma auto-save pero por las dudas
3. **Versiona:** Duplicate file antes de cambios grandes
4. **Feedback temprano:** Muestra Slide 1-3 a amigo/mentor ASAP
5. **No te cases con el diseño:** Si algo no funciona, iterar rápido
6. **Menos es más:** Si duda si agregar algo, no lo agregues
7. **Practica en voz alta:** Deck hermoso pero mal presentado = falla

---

## SIGUIENTES PASOS POST-DECK 🚀

1. **Crear data room** (Google Drive):
   - Pitch deck (PDF)
   - Financial model (Excel)
   - Business plan completo
   - Arquitectura técnica
   - Team bios

2. **Lista de inversionistas:**
   - Angels tech-savvy en Chile
   - VCs early-stage LATAM
   - Family offices con thesis en legal/social impact

3. **Emails personalizados:**
   - Subject: "JusticiaAI - Democratizando acceso a justicia en Chile con IA"
   - Body: Hook + 3 bullets + ask
   - Adjuntar deck

4. **Warm intros:**
   - LinkedIn para ver conexiones
   - Pedir intros a tu red

---

## RECURSOS ÚTILES 🔗

**Inspiration:**
- Airbnb original pitch deck
- Uber Series A deck
- Facebook pitch deck

**Tools:**
- Figma: figma.com
- Unsplash: unsplash.com
- Iconify: iconify.design
- UI Faces: uifaces.co

**Tutorials:**
- YouTube: "How to design pitch deck Figma"
- Figma Learn: learn.figma.com

---

## ¿TIENES DUDAS? 🤔

Consulta estos documentos adicionales:
- `SLIDE-DATA-GUIDE.md` → Datos exactos por slide
- `GRAPHICS-SPECS.md` → Especificaciones de gráficos
- `pitch-deck-outline.md` → Contenido detallado
- `figma-pitch-deck-guide.md` → Guía visual completa

---

**¡Estás listo para crear un pitch deck world-class! 🎨🚀**

**Meta clara:** Deck terminado en 2-3 sesiones → Empezar a contactar inversionistas ESTA SEMANA.

**Remember:** Un deck perfecto que nunca muestras vale $0. Un deck bueno que muestras a 50 inversionistas puede valer $400K.

**¡Manos a la obra, Roberto! 💪**
