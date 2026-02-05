# ESPECIFICACIONES DE GRÁFICOS - JusticiaAI Pitch Deck
## Guía visual detallada para cada gráfico y visualización

---

## TABLA DE CONTENIDOS

1. [Slide 2: Problem Icons & Stats](#slide-2-problem)
2. [Slide 3: Phone Mockup Chatbot](#slide-3-chatbot)
3. [Slide 4: TAM/SAM/SOM Circles](#slide-4-market)
4. [Slide 5: Revenue Streams Icons](#slide-5-revenue)
5. [Slide 6: Timeline/Growth Chart](#slide-6-traction)
6. [Slide 7: Competitive Matrix](#slide-7-competition)
7. [Slide 8: Conversion Funnel](#slide-8-funnel)
8. [Slide 10: Financial Bar Chart](#slide-10-financials)
9. [Slide 11: Use of Funds Pie Chart](#slide-11-funding)
10. [Slide 13: LATAM Map](#slide-13-vision)

---

## SLIDE 2: PROBLEM

### Visual Overview
4 cards en grid 2×2, cada uno con ícono + título + descripción

### Card Specifications

**Dimensions:**
- Card: 400px (W) × 200px (H)
- Spacing: 32px between cards
- Total grid: 832px (W) × 432px (H)

**Card Structure:**
```
┌─────────────────────────────┐
│   [Icon Circle]             │  ← 80×80px circle
│                             │
│   Título del Problema       │  ← Heading 3 (32px)
│   Descripción detallada     │  ← Body (20px)
└─────────────────────────────┘
```

**Card Styling:**
- Background: `#FFFFFF` (White)
- Border: `1px solid #D1D5DB` (Gray-300)
- Corner radius: `16px`
- Shadow: `0 4px 6px rgba(0, 0, 0, 0.05)`
- Padding: `32px`
- Auto layout: Vertical, spacing `16px`, center aligned

### Icon Circles

**Circle:**
- Diameter: `80px`
- Fill: `#DBEAFE` (Blue-100)
- No border

**Icon inside:**
- From Iconify plugin
- Size: `40px`
- Color: `#2563EB` (Blue-600)
- Centered in circle

**Icons to use:**
1. **Costos**: `lucide:dollar-sign`
2. **Complejidad**: `lucide:help-circle`
3. **Demoras**: `lucide:clock`
4. **Información**: `lucide:info`

### Step-by-Step en Figma

1. **Crear card base:**
   ```
   Rectangle (R) → 400×200px
   Fill: White
   Border: 1px Gray-300
   Corner radius: 16px
   Add shadow (Effects → Drop shadow)
   ```

2. **Agregar ícono:**
   ```
   Plugins → Iconify → Buscar ícono
   Resize a 40×40px
   Color: Blue-600

   Ellipse (O) → 80×80px
   Fill: Blue-100
   Center icon inside circle
   Group (Cmd+G)
   ```

3. **Agregar texto:**
   ```
   Text (T) → Título
   Apply "Heading 3" style

   Text (T) → Descripción
   Apply "Body" style
   Max width: 336px
   ```

4. **Auto layout:**
   ```
   Select all elements in card
   Shift+A (Auto layout)
   Direction: Vertical
   Spacing: 16px
   Padding: 32px all sides
   Alignment: Center horizontally
   ```

5. **Duplicar y posicionar:**
   ```
   Duplicate card 3 veces (Cmd+D)
   Cambiar iconos y textos
   Select all 4 cards
   Shift+A (Auto layout)
   Direction: Horizontal wrap
   Spacing: 32px
   Max width: 832px
   ```

---

## SLIDE 3: CHATBOT

### Phone Mockup Specifications

**Phone Frame:**
- Dimensions: `375px (W) × 812px (H)` (iPhone X size)
- Corner radius: `48px`
- Border: `4px solid #111827` (para simular bezel)
- Shadow: `0 20px 25px rgba(0, 0, 0, 0.15)`

**Screen Inside:**
- Dimensions: `367px (W) × 804px (H)`
- Background: `#F9FAFB` (Gray-50)
- Position: Centered in frame (4px offset from edges)

### Chat UI Elements

**Header:**
```
┌─────────────────────────────┐
│ [←] JusticiaAI  [•••]      │  ← 64px height
│                             │     Background: Blue-600
└─────────────────────────────┘
```
- Height: `64px`
- Background: `#2563EB` (Blue-600)
- Text: "JusticiaAI" - White, 18px SemiBold
- Back arrow icon (left)
- Menu dots icon (right)

**Chat Messages:**

User message (right-aligned):
```
┌─────────────────────────────┐
│                 ┌─────────┐ │
│                 │ Mensaje │ │
│                 │ usuario │ │
│                 └─────────┘ │
└─────────────────────────────┘
```
- Max width: `260px`
- Background: `#DBEAFE` (Blue-100)
- Border radius: `16px 16px 4px 16px`
- Padding: `12px 16px`
- Text: Body (16px), Gray-900
- Align: Right, margin-right `16px`

Bot message (left-aligned):
```
┌─────────────────────────────┐
│ ┌─────────┐                 │
│ │ Mensaje │                 │
│ │   bot   │                 │
│ └─────────┘                 │
└─────────────────────────────┘
```
- Max width: `280px`
- Background: `#FFFFFF` (White)
- Border: `1px solid #D1D5DB`
- Border radius: `16px 16px 16px 4px`
- Padding: `12px 16px`
- Text: Body (16px), Gray-900
- Align: Left, margin-left `16px`

**Ejemplo de conversación:**

```
[User - right]
"Me despidieron sin finiquito, ¿qué hago?"

[Bot - left]
"Entiendo tu situación. En Chile, el empleador
DEBE pagarte finiquito dentro de 10 días hábiles.

Incluye:
• Sueldo proporcional
• Vacaciones pendientes
• Indemnización (si aplica)

¿Te despidieron con o sin causa?"

[Buttons - center]
┌─────────────┐ ┌─────────────┐
│  Con causa  │ │  Sin causa  │
└─────────────┘ └─────────────┘
```

**Button specs:**
- Width: `150px`
- Height: `40px`
- Background: `#2563EB` (Blue-600)
- Border radius: `8px`
- Text: White, 14px SemiBold
- Spacing: `12px` between buttons

### Alternative: Plugin Method

**Using Mockuuups Studio:**
1. Plugins → Mockuuups Studio → Free
2. Select device: iPhone 13/14
3. Insert screenshot/design
4. Export

**If creating mockup screenshot elsewhere:**
- Take screenshot of actual chat interface
- Or use Figma to design full chat, then screenshot
- Import as image into phone frame

---

## SLIDE 4: MARKET

### TAM/SAM/SOM Concentric Circles

**Visual:**
```
        ┌──────────────────┐
        │                  │  ← TAM (largest)
        │   ┌──────────┐   │
        │   │          │   │  ← SAM (medium)
        │   │  ┌────┐  │   │
        │   │  │SOM │  │   │  ← SOM (smallest)
        │   │  └────┘  │   │
        │   └──────────┘   │
        └──────────────────┘
```

**Circle Dimensions:**
- TAM: `600px` diameter
- SAM: `400px` diameter
- SOM: `220px` diameter

**Circle Styling:**

TAM (outer):
```
Fill: #DBEAFE (Blue-100)
Opacity: 50%
No border
```

SAM (middle):
```
Fill: #93C5FD (Blue-300)
Opacity: 60%
No border
```

SOM (inner):
```
Fill: #2563EB (Blue-600)
Opacity: 80%
No border
```

**Labels with Lines:**

Each circle needs label with connector line:

```
       Circle  ─────────→  ┌──────────────┐
                          │ TAM: $2,000M │
                          │ Mercado total│
                          └──────────────┘
```

**Label Box:**
- Rectangle: Auto width × `80px` height
- Background: White
- Border: `2px solid` matching circle color
- Corner radius: `12px`
- Padding: `16px`
- Shadow: `0 2px 4px rgba(0,0,0,0.1)`

**Connector Line:**
- Width: `2px`
- Color: Same as circle
- Length: `100-150px`
- Use Line tool (L)

**Text in Labels:**
- Title: Heading 3 (32px Bold), matching circle color
- Subtitle: Body (20px), Gray-600

**Positioning:**
```
TAM label: Right side, 45° angle
SAM label: Top right, 30° angle
SOM label: Centered or slight right
```

### Step-by-Step:

1. **Create circles:**
   ```
   Ellipse (O) → 600×600px (TAM)
   Fill: Blue-100, opacity 50%
   Center on canvas

   Ellipse (O) → 400×400px (SAM)
   Center on TAM circle

   Ellipse (O) → 220×220px (SOM)
   Center on SAM circle
   ```

2. **Add labels:**
   ```
   For each circle:
   - Rectangle (R) → auto × 80px
   - Auto layout, padding 16px
   - Add text (Title + subtitle)
   - Position outside circle
   ```

3. **Connect with lines:**
   ```
   Line tool (L)
   From circle edge to label
   Width: 2px
   Color: Match circle
   ```

### Alternative: Bar Chart

If circles are complex, use horizontal bar chart:

```
┌────────────────────────────────────────┐ $2,000M - TAM
├─────────────────────┐                  │
│                     │ $450M - SAM      │
│  ┌──────┐           │                  │
│  │      │ $15M     │                  │
└──┴──────┴───────────┴──────────────────┘
   SOM    SAM         TAM
```

---

## SLIDE 5: REVENUE

### Revenue Stream Icons

Each stream needs icon + text in horizontal layout

**Layout per stream:**
```
┌────────────────────────────────────────┐
│ [Icon]  Nombre Stream  40%  Detalles  │
│  48px   Heading 3    Color  Caption   │
└────────────────────────────────────────┘
```

**Container:**
- Width: `800px`
- Height: `100px`
- Auto layout: Horizontal
- Spacing: `24px`
- Padding: `16px 24px`
- Background: `#F9FAFB` (Gray-50) or transparent
- Border: `1px solid #E5E7EB` (optional)
- Corner radius: `12px`
- Alignment: Center vertically

**Icon Specs:**
- Size: `48×48px`
- Color: `#2563EB` (Blue-600)
- From Iconify

**Text Specs:**
- Stream name: Heading 3 (32px SemiBold), Gray-900
- Percentage: Body Large (24px Bold), Blue-600
- Details: Caption (16px), Gray-600

**Icons to use:**
1. **Comisiones**: `lucide:percentage`
2. **Suscripciones**: `lucide:repeat`
3. **Automatizados**: `lucide:file-text`
4. **B2B**: `lucide:briefcase`
5. **Partnerships**: `lucide:handshake`

### Unit Economics Box

**Dimensions:**
- Width: `600px`
- Height: `200px`
- Background: `#D1FAE5` (Green-50)
- Border: `3px solid #10B981` (Green-500)
- Corner radius: `16px`
- Padding: `32px`

**Content:**
```
┌────────────────────────────────┐
│                                │
│     LTV/CAC: 2.5x              │  ← 56px Bold
│                                │     Green-500
│     (Año 3)                    │  ← 20px
│                                │     Gray-600
└────────────────────────────────┘
```

---

## SLIDE 6: TRACTION

### Option A: Timeline (Pre-Launch)

**Visual:**
```
────●────────●────────●────
   Mes 1-3   Mes 4-6  Mes 7-12

     MVP       Beta     Scale
```

**Horizontal Line:**
- Width: `800px`
- Height: `4px`
- Color: `#2563EB` (Blue-600)

**Milestones (dots):**
- Circle: `24px` diameter
- Fill: `#2563EB` (Blue-600)
- Border: `4px solid #DBEAFE` (Blue-100)
- Position: On line, evenly spaced (200px apart)

**Labels:**
- Above dot: "Mes 1-3" (Body, Gray-900)
- Below dot: "MVP" (Heading 3, Blue-600)
- Below that: Brief description (Caption, Gray-600)

**Card for details:**
```
┌─────────────────────┐
│ MES 1-3             │
│ MVP                 │
│                     │
│ • Chatbot IA        │
│ • Marketplace basic │
│ • 30 casos target   │
└─────────────────────┘
```
- Width: `240px`
- Height: Auto
- Background: White
- Border: `1px solid #D1D5DB`
- Corner radius: `12px`
- Padding: `20px`

### Option B: Growth Chart (Post-Launch)

**Line Chart:**

Using Figma Charts plugin:
1. Plugins → Charts → Line Chart
2. Data points:
   ```
   Month 1: $1,000
   Month 2: $1,500
   Month 3: $2,500
   Month 4: $3,800
   Month 5: $5,000
   ```
3. Settings:
   - Line color: `#2563EB` (Blue-600)
   - Line width: `3px`
   - Data point markers: Circle, 8px
   - Grid: Light gray
   - Fill under line: Gradient Blue-100 to transparent

**Manual method:**

1. **Create axis:**
   ```
   Y-axis: 0 to $5K (vertical, left)
   X-axis: Jan to Jun (horizontal, bottom)
   ```

2. **Plot points:**
   ```
   Connect with pen tool (P)
   Smooth curves between points
   ```

3. **Style line:**
   ```
   Stroke: 3px, Blue-600
   Join: Round
   ```

4. **Fill under curve:**
   ```
   Duplicate line
   Close path to X-axis
   Fill: Linear gradient
     Top: Blue-100 (40% opacity)
     Bottom: Transparent
   ```

---

## SLIDE 7: COMPETITION

### Competitive Matrix Table

**Table Structure:**

```
┌─────────────┬─────┬────────────┬──────┬─────┐
│             │ IA  │ Marketplace│ Auto │ B2B │
├─────────────┼─────┼────────────┼──────┼─────┤
│ JusticiaAI  │ ✅  │     ✅     │  ✅  │ ✅  │
├─────────────┼─────┼────────────┼──────┼─────┤
│ Total Abog. │ ❌  │     ❌     │  ⚠️  │ ❌  │
├─────────────┼─────┼────────────┼──────┼─────┤
│ Marketplaces│ ❌  │     ✅     │  ❌  │ ❌  │
├─────────────┼─────┼────────────┼──────┼─────┤
│ CAJ         │ ❌  │     ❌     │  ❌  │ ❌  │
└─────────────┴─────┴────────────┴──────┴─────┘
```

**Cell Dimensions:**
- Header row: `180px (W) × 60px (H)`
- Data cells: `180px (W) × 80px (H)`
- Total table: `900px (W) × 380px (H)`

**Styling:**

Header row:
```
Background: #2563EB (Blue-600)
Text: White, Body Large (24px Bold)
Padding: 16px
Border: 1px solid White
```

First column (company names):
```
Background: #F9FAFB (Gray-50)
Text: Gray-900, Body (20px SemiBold)
Padding: 16px
Border: 1px solid #D1D5DB
Align: Left
```

JusticiaAI row (highlight):
```
Background: #DBEAFE (Blue-100)
Border: 2px solid #2563EB (Blue-600)
```

Other data cells:
```
Background: White
Border: 1px solid #D1D5DB
Padding: 16px
Align: Center
```

**Emoji/Icons:**
- ✅ Size: 32px, use emoji or `lucide:check-circle` (Green-500)
- ❌ Size: 32px, use emoji or `lucide:x-circle` (Red-500)
- ⚠️ Size: 32px, use emoji or `lucide:alert-triangle` (Amber-500)

### Step-by-Step:

1. **Create header row:**
   ```
   Rectangle (R) → 180×60px
   Duplicate 4 times (5 columns total)
   Arrange horizontally, no gap
   Fill: Blue-600
   Group all
   ```

2. **Create data rows:**
   ```
   Rectangle (R) → 180×80px
   Duplicate 4 times (5 columns)
   Arrange horizontally, no gap
   Fill: White, border Gray-300
   Group
   Duplicate group 4 times (4 rows)
   Stack vertically
   ```

3. **Add JusticiaAI row highlight:**
   ```
   Select row 1 (JusticiaAI)
   Fill: Blue-100
   Border: 2px Blue-600
   ```

4. **Add text:**
   ```
   For each cell:
   Text tool (T)
   Type content or paste emoji
   Center in cell
   ```

5. **Assemble:**
   ```
   Position header row above data rows
   Align all
   Group entire table
   ```

---

## SLIDE 8: FUNNEL

### Conversion Funnel

**Visual:**
```
┌────────────────────────────┐  100K Visitors
│                            │
└────────────────────────────┘
          ↓ 5%
  ┌──────────────────────┐      5K Registered
  │                      │
  └──────────────────────┘
          ↓ 20%
    ┌────────────────┐          1K Chat IA
    │                │
    └────────────────┘
          ↓ 20%
      ┌──────────┐              200 Request
      │          │
      └──────────┘
          ↓ 50%
        ┌────┐                  100 Customers
        └────┘
```

**Trapezoid Dimensions:**

Level 1 (top):
```
Width: 800px
Height: 80px
```

Level 2:
```
Width: 700px
Height: 80px
```

Level 3:
```
Width: 600px
Height: 80px
```

Level 4:
```
Width: 500px
Height: 80px
```

Level 5 (bottom):
```
Width: 400px
Height: 80px
```

**Styling:**

Gradient fill (top to bottom):
```
Level 1: #DBEAFE (Blue-100)
Level 2: #93C5FD (Blue-300)
Level 3: #60A5FA (Blue-400)
Level 4: #3B82F6 (Blue-500)
Level 5: #2563EB (Blue-600)
```

**Text inside each level:**
- Number: 48px Bold, White (for darker levels) or Gray-900 (for light levels)
- Label: 20px, same color as number
- Centered

**Arrows between levels:**
- Line with arrow: Width `4px`, color Gray-600
- Length: `40px`
- Label next to arrow: "5% CTR" (Body, Gray-900)

### Creating Trapezoids:

Method 1 - Rectangle + Skew:
```
1. Rectangle (R) → 800×80px
2. Select left-bottom and right-bottom corners
3. Move inward symmetrically to create angle
```

Method 2 - Pen Tool:
```
1. Pen tool (P)
2. Draw 4 points:
   - Top-left: (0, 0)
   - Top-right: (800, 0)
   - Bottom-right: (750, 80)
   - Bottom-left: (50, 80)
3. Close path
```

### Step-by-Step:

1. **Create all trapezoids:**
   ```
   Create 5 trapezoids with dimensions above
   Fill with gradient colors
   Center align horizontally
   ```

2. **Stack vertically:**
   ```
   Spacing: 60px between (for arrows)
   Center aligned
   ```

3. **Add text:**
   ```
   For each level:
   - Number (48px Bold)
   - Label (20px)
   - Center in trapezoid
   ```

4. **Add arrows:**
   ```
   Line tool (L) with arrow
   Between each level
   Label: "X% conversion"
   ```

5. **Group:**
   ```
   Select all
   Cmd+G
   ```

---

## SLIDE 10: FINANCIALS

### Bar Chart

**Visual:**
```
    $3.3M ┐
          │     ███
          │     ███
          │     ███
          │     ███
  $734K   │ ███ ███
          │ ███ ███
          │ ███ ███
   $66K   │ ███ ███ ███
          └─────────────
           Y1  Y2  Y3
```

**Bar Dimensions:**

To make heights proportional to values:

```
Y1 ($66K):    Height = 60px
Y2 ($734K):   Height = 660px  (11.1x Y1)
Y3 ($3.3M):   Height = 3000px (scaled to 300px for fit)
```

**Actual implementation (scaled to fit):**
```
Y1: 60px height
Y2: 220px height
Y3: 340px height
```

**Bar Styling:**
- Width: `180px` each
- Spacing: `80px` between bars
- Fill: `#2563EB` (Blue-600)
- Corner radius: `8px 8px 0 0` (rounded top only)

**Labels above bars:**
- Value: 48px Bold, Blue-600
- "$66K", "$734K", "$3.3M"
- Position: 16px above bar

**Growth arrows:**
```
Between Y1-Y2:  "+1,012% ↗"
Between Y2-Y3:  "+349% ↗"
```
- Font: 20px SemiBold
- Color: `#10B981` (Green-500)
- Arrow icon: `lucide:trending-up`

**X-axis labels:**
- "Año 1", "Año 2", "Año 3"
- Font: Body (20px), Gray-600
- Position: Below bars, centered

### Step-by-Step:

1. **Create bars:**
   ```
   Rectangle (R):
   - Y1: 180×60px
   - Y2: 180×220px
   - Y3: 180×340px

   Fill: Blue-600
   Corner radius: 8px (top corners only)
   ```

2. **Align bars:**
   ```
   Align bottom edges (baseline)
   Space horizontally: 80px between
   ```

3. **Add value labels:**
   ```
   Text (T): "$66K", "$734K", "$3.3M"
   Font: 48px Bold, Blue-600
   Position above each bar (16px gap)
   Center horizontally with bar
   ```

4. **Add growth labels:**
   ```
   Text: "+1,012%"
   Icon: trending-up (20px)
   Color: Green-500
   Position between Y1 and Y2 bars
   Repeat for Y2-Y3
   ```

5. **Add axis labels:**
   ```
   Text: "Año 1", "Año 2", "Año 3"
   Font: Body, Gray-600
   Position below bars
   ```

6. **Group:**
   ```
   Select all elements
   Cmd+G
   ```

---

## SLIDE 11: FUNDING

### Pie Chart (Use of Funds)

**Data:**
- Desarrollo: 40% ($160K)
- Marketing: 30% ($120K)
- Operaciones: 20% ($80K)
- Legal: 10% ($40K)

**Using Charts Plugin:**

1. Plugins → Charts → Pie Chart
2. Input data:
   ```
   Desarrollo: 40
   Marketing: 30
   Operaciones: 20
   Legal: 10
   ```
3. Colors:
   ```
   Desarrollo: #2563EB (Blue-600)
   Marketing: #10B981 (Green-500)
   Operaciones: #F59E0B (Amber-500)
   Legal: #6B7280 (Gray-500)
   ```
4. Size: `400px` diameter
5. Show percentages on slices

**Manual Method (if plugin fails):**

Alternative: Horizontal bar chart

```
┌────────────────────────────────────┐ 40% Desarrollo ($160K)
├─────────────────────────────┐      │
│                             │      │ 30% Marketing ($120K)
├──────────────────┐          │      │
│                  │          │      │ 20% Operaciones ($80K)
├──────────┐       │          │      │
│          │       │          │      │ 10% Legal ($40K)
└──────────┴───────┴──────────┴──────┘
```

**Bar specs:**
- Total width: `600px`
- Height per bar: `60px`
- Spacing: `12px` between bars
- Colors: Same as pie chart
- Labels: Inside bar (white text) + outside (amount)

---

## SLIDE 13: VISION

### LATAM Map

**Option 1: Vector Map**

1. **Find vector map:**
   - Google: "Latin America map vector SVG free"
   - Download SVG
   - Import to Figma: File → Place Image

2. **Styling:**
   - Chile: Fill `#2563EB` (Blue-600), Opacity 100%
   - Perú: Fill `#93C5FD` (Blue-300), Opacity 60%
   - Colombia: Fill `#93C5FD` (Blue-300), Opacity 60%
   - Argentina: Fill `#93C5FD` (Blue-300), Opacity 60%
   - Rest of LATAM: Fill `#E5E7EB` (Gray-200), Opacity 40%

3. **Add location pins:**
   ```
   Circle: 32×32px
   Fill: Solid color matching country
   Border: 4px white
   Shadow: 0 2px 4px rgba(0,0,0,0.2)

   Place on capital cities:
   - Santiago (Chile)
   - Lima (Perú)
   - Bogotá (Colombia)
   - Buenos Aires (Argentina)
   ```

**Option 2: Simplified Shapes**

If can't find good vector:

1. **Create simplified country shapes:**
   ```
   Pen tool (P)
   Trace rough outlines of:
   - Chile (long vertical)
   - Perú (above Chile)
   - Colombia (top)
   - Argentina (right of Chile)
   ```

2. **Style same as Option 1**

3. **Add labels:**
   ```
   Text next to each country
   Body (20px), Gray-900
   ```

**Map dimensions:**
- Width: `400-500px`
- Height: Proportional to width
- Position: Center or left of slide

---

## GENERAL DESIGN PRINCIPLES

### Consistency Checklist

**Colors:**
- Only use palette colors (no hardcoded hex)
- Blue-600 for primary actions/highlights
- Green-500 for success/growth
- Amber-500 for warnings/urgency
- Gray-900 for primary text
- Gray-600 for secondary text

**Spacing:**
- Major sections: 64px
- Between elements: 48px
- Within components: 24px
- Tight spacing: 12px
- Margins: 64-80px from edges

**Typography:**
- Always use text styles (no custom)
- Heading 1: 64px Bold (slide titles)
- Heading 2: 48px SemiBold (subtitles)
- Heading 3: 32px SemiBold (section headers)
- Body Large: 24px Regular (important text)
- Body: 20px Regular (standard text)
- Caption: 16px Regular (small text)

**Borders & Shadows:**
- Subtle borders: 1px Gray-300
- Emphasis borders: 2px Blue-600
- Card shadows: 0 4px 6px rgba(0,0,0,0.05)
- Elevated shadows: 0 10px 15px rgba(0,0,0,0.1)
- Phone/device shadows: 0 20px 25px rgba(0,0,0,0.15)

**Corner Radius:**
- Small elements: 8px
- Cards: 12-16px
- Large containers: 16-24px
- Buttons: 8px
- Phone mockup: 48px

---

## EXPORT SPECIFICATIONS

### For PDF Export:
```
File → Export → PDF
Settings:
- Pages: All
- Quality: High
- Color profile: sRGB
```

### For PNG Export:
```
Select all frames
Export → PNG
Settings:
- Scale: 2x (high resolution)
- Format: PNG
- Background: Include
```

### For Presentation:
```
Figma Present Mode:
- Cmd+Enter
- Fullscreen
- Navigate with arrow keys
- ESC to exit
```

---

## TROUBLESHOOTING

**If icons don't load:**
- Use emojis instead
- Or download SVG icons from heroicons.com

**If charts plugin fails:**
- Create bars/circles manually
- Follow manual methods in this guide

**If colors look different:**
- Check display color profile (sRGB)
- Verify Figma color mode (RGB)

**If export is pixelated:**
- Increase export scale to 2x or 3x
- Ensure all images are high-res (min 2x original size)

---

**¡Con estas especificaciones puedes crear TODOS los gráficos del pitch deck!** 📊✅
