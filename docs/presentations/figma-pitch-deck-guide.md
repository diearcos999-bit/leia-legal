# Guía: Crear Pitch Deck Visual en Figma - JusticiaAI

## Setup Inicial

### 1. Crear Cuenta y Proyecto
1. Ir a figma.com
2. Sign up (free para 3 proyectos)
3. "Create new design file" → "JusticiaAI Pitch Deck"

### 2. Configurar Canvas
- **Frame Size**: 1920 × 1080px (16:9 ratio, standard presentaciones)
- **Layout Grid**: 8px grid system
- **Columns**: 12 columns con 32px margin
- **Background**: Blanco (`#FFFFFF`)

---

## Design System Setup

### Color Palette

Crear **Color Styles** en Figma:

**Primary Colors**:
```
- Blue/800:  #1E40AF (Main brand)
- Blue/700:  #1D4ED8 (Hover states)
- Blue/600:  #2563EB (Buttons)
- Blue/100:  #DBEAFE (Backgrounds light)
- Blue/50:   #EFF6FF (Backgrounds lighter)
```

**Secondary Colors**:
```
- Emerald/500: #10B981 (Success, trust)
- Amber/500:   #F59E0B (Accent, highlights)
- Gray/900:    #111827 (Text primary)
- Gray/600:    #4B5563 (Text secondary)
- Gray/300:    #D1D5DB (Borders)
- Gray/50:     #F9FAFB (Backgrounds)
```

**Semantic Colors**:
```
- Success:  #22C55E
- Error:    #EF4444
- Warning:  #F97316
```

**Cómo crear color styles en Figma**:
1. Click icono de "selection" (V)
2. Crear rectangle con color
3. En panel derecho, click en color swatch
4. Click "+" en "Color styles"
5. Nombrar (ej: "Primary/Blue-800")
6. Repetir para todos los colores

---

### Typography

**Fuente**: Inter (Google Fonts, gratis en Figma)

Crear **Text Styles**:

1. **Heading 1** (Slide titles)
   - Font: Inter Bold
   - Size: 64px
   - Line height: 120%
   - Color: Gray-900

2. **Heading 2** (Section titles)
   - Font: Inter SemiBold
   - Size: 48px
   - Line height: 120%
   - Color: Gray-900

3. **Heading 3** (Subsections)
   - Font: Inter SemiBold
   - Size: 32px
   - Line height: 130%
   - Color: Gray-900

4. **Body Large** (Main content)
   - Font: Inter Regular
   - Size: 24px
   - Line height: 150%
   - Color: Gray-700

5. **Body** (Secondary content)
   - Font: Inter Regular
   - Size: 20px
   - Line height: 150%
   - Color: Gray-600

6. **Caption** (Small text, annotations)
   - Font: Inter Regular
   - Size: 16px
   - Line height: 140%
   - Color: Gray-500

**Cómo crear text styles**:
1. Crear text box (T)
2. Aplicar font, size, etc.
3. En panel derecho, click "..." next to "Text"
4. "Create style" → Nombrar

---

### Components Library

Crear components reusables:

**1. Button Primary**
```
Rectangle:
- Width: auto (min 200px)
- Height: 56px
- Fill: Blue-600
- Corner radius: 8px
- Shadow: 0 4px 6px rgba(0,0,0,0.1)

Text:
- Font: Inter SemiBold
- Size: 20px
- Color: White
- Center aligned
```

**2. Button Secondary**
```
Similar pero:
- Fill: White
- Border: 2px Blue-600
- Text color: Blue-600
```

**3. Card**
```
Rectangle:
- Auto layout (vertical, 24px gap)
- Padding: 32px
- Fill: White
- Border: 1px Gray-200
- Corner radius: 16px
- Shadow: 0 10px 15px rgba(0,0,0,0.05)
```

**4. Icon Circle**
```
Circle:
- Diameter: 80px
- Fill: Blue-50
- Icon inside (from Lucide/Iconify plugin)
- Color: Blue-600
```

---

## Slide by Slide Guide

### Slide 1: Cover

**Layout**:
```
┌─────────────────────────────────────────┐
│                                           │
│                                           │
│           [Logo JusticiaAI]              │
│                                           │
│          Democratizando el acceso        │
│          a justicia en Chile con IA      │
│                                           │
│           [Foto/Ilustración]             │
│                                           │
│         Roberto Arcos, Founder & CEO     │
│         roberto@justiciaai.cl            │
│                                           │
│         Buscando $300-500K USD           │
│         Ronda Semilla • Enero 2025       │
│                                           │
└─────────────────────────────────────────┘
```

**Elementos en Figma**:
1. **Background**: Gradient subtle (Blue-50 to White, top to bottom)
2. **Logo**: Placeholder circular o texto "JusticiaAI" (Inter Bold 72px)
3. **Tagline**: Heading 2 (48px)
4. **Imagen**: Ilustración (Undraw.co o Storyset.com - gratis)
5. **Tu info**: Body (20px)
6. **Funding ask**: Body Large (24px), color Blue-600

**Tips Visuales**:
- Centrar todo verticalmente
- Usar auto-layout para spacing consistente (48px entre elementos)
- Imagen/ilustración: Buscar "legal consultation" en Undraw

---

### Slide 2: Problem

**Layout**:
```
┌─────────────────────────────────────────┐
│ El Problema                               │
│                                           │
│ 70% de los chilenos no puede            │
│ acceder a servicios legales              │
│                                           │
│ [Icon] Costos Prohibitivos               │
│        $500K+ por divorcio simple        │
│                                           │
│ [Icon] Complejidad                       │
│        79% no entiende el sistema        │
│                                           │
│ [Icon] Demoras                           │
│        400+ días procesos promedio       │
│                                           │
│ [Icon] Información                       │
│        No saben sus derechos             │
│                                           │
│ → 1.5M personas sin resolver problemas  │
└─────────────────────────────────────────┘
```

**Elementos**:
1. **Title**: Top left, Heading 1 (64px)
2. **Hero stat**: Center-top, extra large (72px Bold), color Blue-600
3. **4 problems**: 2×2 grid
   - Icon (80×80px circle, Blue-50 background)
   - Title (Heading 3, 32px)
   - Description (Body, 20px)
   - Spacing: 40px between cards
4. **Bottom stat**: Large (36px), color Amber-500 for emphasis

**Íconos** (Plugin "Iconify"):
- Costos: `lucide:dollar-sign`
- Complejidad: `lucide:help-circle`
- Demoras: `lucide:clock`
- Información: `lucide:info`

---

### Slide 3: Solution

**Layout**:
```
┌─────────────────────────────────────────┐
│ La Solución                               │
│                                           │
│ [Screenshot Phone con Chatbot]           │
│                                           │
│ [Icon] IA Legal Gratuita                 │
│        Orientación 24/7 en leyes chile   │
│                                           │
│ [Icon] Marketplace Verificado            │
│        Precios transparentes, reviews    │
│                                           │
│ [Icon] Automatización                    │
│        Documentos, integraciones         │
│                                           │
│ = LawConnect + LegalZoom para LATAM     │
└─────────────────────────────────────────┘
```

**Elementos**:
1. **Title**: Heading 1
2. **Product screenshot**: Mockup de iPhone con chatbot (Frame phone en Figma)
   - Tamaño: ~600px height
   - Posición: Left side
   - Sombra elegante: 0 20px 25px rgba(0,0,0,0.15)
3. **3 features**: Right side, vertical stack
   - Similar layout a Slide 2
4. **Bottom comparison**: Body Large, color Blue-600

**Cómo crear phone mockup**:
1. Plugin "Mockuuups Studio" (free)
2. Or manual: Frame 375×812px (iPhone size)
3. Insertar screenshot de wireframe del chatbot

---

### Slide 4: Market Opportunity

**Layout**:
```
┌─────────────────────────────────────────┐
│ Oportunidad de Mercado                   │
│                                           │
│ [Gráfico: 3 círculos concéntricos]      │
│                                           │
│    TAM                                    │
│  $2,000M                                  │
│                                           │
│      SAM                                  │
│    $450M                                  │
│                                           │
│        SOM (Y3)                          │
│        $10-15M                            │
│                                           │
│ → 2-3% market share = $3.3M ARR          │
└─────────────────────────────────────────┘
```

**Cómo crear círculos**:
1. Circle tool (O)
2. 3 círculos: 600px, 400px, 200px diameter
3. Center aligned
4. Colors: Blue-100, Blue-300, Blue-600 (oscurece hacia adentro)
5. Opacity: 50% para ver overlap
6. Labels: Text con líneas apuntando a cada círculo

**Alternativa**: Bar chart
- Rectangle para cada barra (TAM, SAM, SOM)
- Width proporcional a tamaño
- Labels con números grandes arriba

---

### Slide 5: Business Model

**Layout**:
```
┌─────────────────────────────────────────┐
│ Modelo de Negocio                        │
│                                           │
│ [Diagrama de flujo circular]            │
│                                           │
│ 5 Fuentes de Ingreso                    │
│                                           │
│ [Icon] Comisiones    40% → 25% fee      │
│ [Icon] Suscripciones 25% → $0-135/mes   │
│ [Icon] Automatizados 20% → $10-50/doc   │
│ [Icon] B2B Corp      10% → $200-1K/mes  │
│ [Icon] Partnerships   5% → Variable      │
│                                           │
│ Unit Economics: LTV/CAC 7.5x (Year 3)   │
└─────────────────────────────────────────┘
```

**Diagrama central** (opcional):
- Flow: Usuario → Plataforma → Abogado
- Flechas con $ showing revenue streams
- Use Arrow connector tool en Figma

**5 Revenue streams**:
- Icon + Title + % + Details
- Layout en 2 columnas o vertical list
- Icons: `lucide:percentage`, `lucide:repeat`, `lucide:file-text`, `lucide:briefcase`, `lucide:handshake`

**Bottom stat**:
- Large (48px Bold)
- Color: Green/Emerald-500
- "LTV/CAC 7.5x" super destacado

---

### Slide 6: Traction

**Opción A: Pre-Launch**
```
┌─────────────────────────────────────────┐
│ Tracción Temprana                        │
│                                           │
│ ┌────────────┐ ┌────────────┐ ┌────────┐│
│ │    500     │ │     30     │ │   5    ││
│ │  Waiting   │ │  Abogados  │ │ LOIs   ││
│ │   List     │ │Comprometido│ │Partners││
│ └────────────┘ └────────────┘ └────────┘│
│                                           │
│ [Timeline visual]                         │
│ Mes 1-3: MVP                             │
│ Mes 4-6: Beta (100 casos)                │
│ Mes 7-12: Scale ($50K MRR)               │
└─────────────────────────────────────────┘
```

**Opción B: Post-Launch**
```
┌─────────────────────────────────────────┐
│ Momentum Fuerte                          │
│                                           │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────┐│
│ │ 2,000  │ │  100   │ │   50   │ │ $5K ││
│ │Usuarios│ │Abogados│ │ Casos  │ │ MRR ││
│ └────────┘ └────────┘ └────────┘ └─────┘│
│                                           │
│ [Gráfico de crecimiento MRR]            │
│ Mes 1: $1K → Mes 6: $5K                 │
│ +65% MoM growth                          │
│                                           │
│ NPS: 48 ⭐                                │
└─────────────────────────────────────────┘
```

**Stats boxes**: Card component con número grande, label pequeño

**Growth chart**:
1. Plugin "Charts" de Figma
2. O manual: Line chart con line tool
3. Data points marcados
4. Gradient fill bajo la línea (Blue-50)

---

### Slide 7: Competition

**Layout**:
```
┌─────────────────────────────────────────┐
│ Landscape Competitivo                    │
│                                           │
│ [Matriz 2×2 o Tabla]                     │
│                                           │
│          IA    Marketplace  Auto  B2B   │
│ Nosotros  ✅      ✅         ✅    ✅    │
│ Total Ab  ❌      ❌         ⚠️    ❌    │
│ Mktplace  ❌      ✅         ❌    ❌    │
│ CAJ       ❌      ❌         ❌    ❌    │
│                                           │
│ Ventaja: ÚNICA con IA legal avanzada    │
│ Moat: 6-12 meses ventana                 │
└─────────────────────────────────────────┘
```

**Tabla**:
- Headers: Bold, Blue-600
- Checkmarks/X: Green (✅) / Red (❌) / Yellow (⚠️)
- Highlight row "Nosotros": Background Blue-50

**Alternativa**: Quadrant chart (Innovation vs Market Share)
- X axis: Market Share
- Y axis: Technology/Innovation
- Bubbles para cada competitor
- Nosotros: Top-right (alta innovation, growing share)

---

### Slide 8: Go-to-Market

**Layout**:
```
┌─────────────────────────────────────────┐
│ Estrategia de Lanzamiento                │
│                                           │
│ [Funnel visual]                          │
│ 100K Visitors                            │
│    ↓ 5% CTR                              │
│ 5K Registered                            │
│    ↓ 20% Chat                            │
│ 1K Chat IA                               │
│    ↓ 20% Request                         │
│ 200 Request Lawyer                       │
│    ↓ 50% Hire                            │
│ 100 Paying Customers                     │
│                                           │
│ Channels: SEO • SEM • Social • Partners  │
└─────────────────────────────────────────┘
```

**Funnel**:
1. Trapezoid shapes apilados (más ancho arriba, angosto abajo)
2. Color gradient (Blue-100 top a Blue-600 bottom)
3. Numbers large dentro de cada level
4. Arrows con % conversion entre levels

**Channels row**:
- 4 icons con labels
- Icons: `lucide:search`, `lucide:megaphone`, `lucide:users`, `lucide:handshake`

---

### Slide 9: Team

**Layout**:
```
┌─────────────────────────────────────────┐
│ Equipo                                    │
│                                           │
│ ┌──────────────────────────────────────┐ │
│ │ [Foto]  Roberto Arcos, CEO            │ │
│ │         • [Previous role/company]     │ │
│ │         • [Key achievement]           │ │
│ │         • [Relevant skill]            │ │
│ └──────────────────────────────────────┘ │
│                                           │
│ ┌──────────────────────────────────────┐ │
│ │ [Foto]  [CTO Name], CTO               │ │
│ │         • [Experience]                │ │
│ │         • [Achievement]               │ │
│ └──────────────────────────────────────┘ │
│                                           │
│ Asesores: [Names con logos companies]   │
│                                           │
│ Buscando: AI/ML Eng, 2 Developers       │
└─────────────────────────────────────────┘
```

**Profile cards**:
- Photo: 120×120px circle (use placeholder from UI Faces o generador)
- Name + title: Heading 3
- Bullets: Body text
- Layout: Vertical stack or 2-column grid

**Advisors**: Smaller, just names + logos

---

### Slide 10: Financials

**Layout**:
```
┌─────────────────────────────────────────┐
│ Proyecciones Financieras                 │
│                                           │
│ [Chart: ARR Growth]                      │
│                                           │
│    $3.3M                                 │
│       ╱                                  │
│ $734K╱                                   │
│     ╱                                    │
│ $66K                                     │
│  │     │      │                          │
│  Y1    Y2     Y3                         │
│                                           │
│ • Gross Margin: 75% → 89%                │
│ • LTV/CAC: 2.3x → 7.5x                   │
│ • Path to profitability: Q4 Y3           │
└─────────────────────────────────────────┘
```

**Bar chart**:
1. 3 bars (Año 1, 2, 3)
2. Height proporcional ($66K, $734K, $3.3M)
3. Color: Blue-600
4. Labels con números grandes arriba de barra
5. Growth % entre barras

**Bottom metrics**:
- 3 bullets con números destacados
- Use Bold for numbers
- Icons para visual interest

---

### Slide 11: Funding Ask

**Layout**:
```
┌─────────────────────────────────────────┐
│ Buscamos $400K USD                       │
│ Ronda Semilla • 15-20% equity            │
│                                           │
│ [Pie chart: Uso de fondos]              │
│                                           │
│ 40% Desarrollo    $160K                  │
│ 30% Marketing     $120K                  │
│ 20% Operaciones   $80K                   │
│ 10% Legal         $40K                   │
│                                           │
│ Milestones:                              │
│ ✓ MVP en 3 meses                         │
│ ✓ 100 casos en 6 meses                   │
│ ✓ $50K MRR en 12 meses                   │
│                                           │
│ Runway: 18 meses                         │
└─────────────────────────────────────────┘
```

**Pie chart** (Plugin "Charts"):
- 4 segments con colores diferenciados
- Labels con % y $ fuera del chart
- Legend a la derecha

**Milestones**:
- Checkmark icons (green)
- Bold text para números
- Spacing: 16px entre items

---

### Slide 12: Why Now

**Layout**:
```
┌─────────────────────────────────────────┐
│ ¿Por Qué Ahora?                          │
│                                           │
│ [Icon] Ventana Tecnológica               │
│        Claude 3.5 hace viable IA legal   │
│        First-mover advantage             │
│                                           │
│ [Icon] Ventana Competitiva               │
│        Total Abogados sin IA aún         │
│        6-12 meses para adelantarnos      │
│                                           │
│ [Icon] Momentum Regulatorio              │
│        Ley 21.719 impulsa legaltech      │
│        Poder Judicial adopta IA 2025     │
│                                           │
│ [Icon] Post-COVID                        │
│        Digitalización acelerada          │
│        Usuarios listos                   │
└─────────────────────────────────────────┘
```

**4 reasons**: Vertical stack
- Icon + Title (bold) + 2 bullets
- Icons: `lucide:zap`, `lucide:trophy`, `lucide:trending-up`, `lucide:globe`

---

### Slide 13: Vision

**Layout**:
```
┌─────────────────────────────────────────┐
│ Visión                                    │
│                                           │
│ [Mapa de LATAM con pins]                │
│                                           │
│ Año 1-2: Dominamos Chile                │
│ #1 marketplace legal • 50K users         │
│                                           │
│ Año 3: Expandimos LATAM                 │
│ Perú, Colombia, Argentina                │
│                                           │
│ Impacto:                                 │
│ • 100K+ personas con acceso a justicia   │
│ • 5K+ abogados empowered                 │
│ • Millones ahorrados en costos           │
│                                           │
│ Tecnología al servicio de la justicia   │
└─────────────────────────────────────────┘
```

**Mapa**:
- Vector map de LATAM (buscar "Latin America map vector" en Google)
- Pins/markers en Chile (bright), Perú/Colombia/Argentina (dimmed)
- Color: Blue-600 para Chile, Blue-300 para expansión futura

**Impact stats**:
- Large numbers (48px Bold)
- Green color (Emerald-500) para positive impact

---

### Slide 14: Contact

**Layout**:
```
┌─────────────────────────────────────────┐
│                                           │
│                                           │
│          ¿Listos para democratizar       │
│          la justicia en Chile?           │
│                                           │
│          [Logo JusticiaAI]              │
│                                           │
│          Roberto Arcos                   │
│          Founder & CEO                   │
│                                           │
│          roberto@justiciaai.cl           │
│          +56 9 XXXX XXXX                 │
│          linkedin.com/in/robertoarcos    │
│                                           │
│          [QR Code al deck]               │
│                                           │
└─────────────────────────────────────────┘
```

**Clean, simple**:
- Centered todo
- Large spacing (64px between elements)
- QR code generado con plugin "QR Code Generator"
- Link to Google Drive con deck + docs

---

## Finishing Touches

### 1. Slide Numbers
- Bottom right corner
- Caption style (16px)
- Format: "5 / 14"

### 2. Consistent Footer (Optional)
- Company name left
- Slide number right
- Light gray bar (Gray-100)

### 3. Transitions Between Slides
En presentación:
- Fade (subtle)
- Duración: 0.3s
- Configurar en modo Present

### 4. Animations (Subtle)
- Fade in elements (no overkill)
- Use Figma's "Smart Animate" between frames
- Keep it professional (not PowerPoint'y)

---

## Export & Delivery

### For Pitch
1. **Present Mode**: Use Figma's present mode (Cmd+Enter)
2. **PDF Export**:
   - File → Export → PDF
   - Settings: All slides, high quality
   - Send 24-48h before meeting

### For Email
1. **PDF**: As attachment
2. **Figma Link**: Share with "view only" access
   - More impressive (shows you're tech-savvy)
   - They can zoom, explore

### For Demo Day / Public
1. **Export as PNG**: High res (2x or 3x)
2. Upload to Google Slides / Keynote for presenter notes

---

## Plugins Recomendados

**Must-Have**:
1. **Iconify** - Icons (gratis)
2. **Unsplash** - Stock photos (gratis)
3. **Charts** - Data visualization (gratis)
4. **Mockuuups Studio** - Device mockups (freemium)

**Nice-to-Have**:
5. **Content Reel** - Placeholder text/images (gratis)
6. **Blush** - Ilustraciones customizables ($)
7. **Remove BG** - Background removal (freemium)
8. **QR Code Generator** - Para slide final (gratis)

**Cómo instalar plugins**:
1. Menu → Plugins → Browse all plugins
2. Search by name → Install

---

## Timeline de Creación

**Day 1** (4 horas):
- Setup (colors, fonts, components)
- Slides 1-5

**Day 2** (4 horas):
- Slides 6-10
- Refinar layouts

**Day 3** (3 horas):
- Slides 11-14
- Polish (spacing, consistency)

**Day 4** (2 horas):
- Feedback de advisor/amigo
- Iteraciones
- Export final

**Total: 13 horas** para deck production-ready

---

## Quality Checklist

Antes de presentar, verificar:

**Visual**:
- [ ] Todos los textos son legibles desde 3 metros
- [ ] Colors consistentes (usa styles, no hardcoded)
- [ ] Spacing consistente (usa auto-layout)
- [ ] Imágenes son high-res (no pixeladas)
- [ ] Spelling checked (obvio pero importante!)

**Content**:
- [ ] Números actualizados y correctos
- [ ] Tu info de contacto correcta
- [ ] Links funcionan (QR code testear)
- [ ] No hay placeholder text ("Lorem ipsum...")

**Flow**:
- [ ] Historia fluye lógicamente
- [ ] No hay saltos bruscos
- [ ] Cada slide tiene mensaje claro (1 idea = 1 slide)
- [ ] 10 min pitch timing ≈ 1 min/slide promedio

**Technical**:
- [ ] PDF exporta correctamente
- [ ] Figma link está shared (view only)
- [ ] Tienes backup (USB, cloud)

---

## Presentation Tips

**Durante la presentación**:
1. **Usa Figma Present Mode**: Full screen, clean
2. **Usa Presenter View** (si disponible): Notas privadas
3. **Controla con teclado**:
   - Arrow keys: Navigate
   - Cmd+Enter: Enter/exit present
   - ESC: Exit
4. **Ten backup**:
   - PDF en laptop
   - PDF en USB
   - Link a Google Drive (si falla todo)

**Pro tip**: Practica con el deck al menos 3 veces antes del pitch real. Know exactly qué vas a decir en cada slide.

---

## Resources

**Inspiration** (Buscar en Google/Dribbble):
- "Pitch deck design"
- "SaaS pitch deck"
- "Marketplace pitch deck"

**Templates** (Si quieres empezar más rápido):
- Figma Community: "Pitch Deck Template"
- Filter por "free"
- Customizar con tu brand

**Tutorials**:
- YouTube: "How to design a pitch deck in Figma"
- Figma Learn (learn.figma.com)

---

## Próximo Paso

1. **Setup Figma** (30 min)
2. **Crear primeras 3 slides** (2 hours)
3. **Iterar** basado en feedback
4. **Completar deck** (total 13 horas over 3-4 días)

**Recuerda**: Un buen deck es 50% diseño, 50% contenido. Foca en claridad > belleza.

**¡Buena suerte! 🎨🚀**
