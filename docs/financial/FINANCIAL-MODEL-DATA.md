# DATOS PARA MODELO FINANCIERO - JusticiaAI

## RESUMEN EJECUTIVO

Este documento contiene todos los datos y fórmulas para crear el modelo financiero de JusticiaAI en Excel.

---

## 1. ASSUMPTIONS (SUPUESTOS)

### Crecimiento de Usuarios
```
Año 1:
- Mes 1: 100 usuarios
- Crecimiento mensual: 30%
- Total Año 1: 2,000 usuarios/mes promedio

Año 2:
- Inicio: 2,000 usuarios/mes
- Crecimiento mensual: 25%
- Total Año 2: 10,000 usuarios/mes promedio

Año 3:
- Inicio: 10,000 usuarios/mes
- Crecimiento mensual: 20%
- Total Año 3: 30,000 usuarios/mes promedio
```

### Crecimiento de Abogados
```
Año 1:
- Inicio: 20 abogados
- Crecimiento mensual: 15%
- Total Año 1: 100 abogados

Año 2:
- Inicio: 100 abogados
- Crecimiento mensual: 20%
- Total Año 2: 500 abogados

Año 3:
- Inicio: 500 abogados
- Crecimiento mensual: 15%
- Total Año 3: 1,000 abogados
```

### Tasas de Conversión
```
IA → Request Lawyer: 20%
Request → Hire: 50%
Overall visitor → customer: 10%

Suscripciones Abogados:
- Free: 60% (Año 1) → 40% (Año 3)
- Profesional ($55/mes): 30% (Año 1) → 45% (Año 3)
- Premium ($135/mes): 10% (Año 1) → 13% (Año 3)
- Firma ($330/mes): 0% (Año 1) → 2% (Año 3)
```

### Precios
```
Comisiones:
- Honorario promedio abogado: $350,000 CLP
- Comisión JusticiaAI: 25%
- Ingreso por caso: $87,500 CLP ($97 USD)

Servicios Automatizados:
- Precio promedio: $20,000 CLP ($22 USD)
- Conversión usuarios: 10% → 20%

B2B:
- Precio promedio empresa: $400,000 CLP/mes ($444 USD)
- Penetración: Año 1: 0, Año 2: 10 empresas, Año 3: 50 empresas
```

### Costos
```
CAC (Customer Acquisition Cost):
- Año 1: $50 USD
- Año 2: $30 USD
- Año 3: $20 USD

Costo por Abogado (recruitment):
- $200 USD por abogado onboarded

Infraestructura:
- Hosting: $500/mes
- APIs (Anthropic, etc.): $1,000/mes → $3,000/mes
- Herramientas: $300/mes

Team (post-funding):
- CTO: $4,000/mes
- 2 Developers: $2,500/mes c/u
- 1 Designer: $2,000/mes
- CEO (tú): $3,000/mes
- Total: $14,000/mes
```

---

## 2. REVENUE MODEL (INGRESOS)

### Stream 1: Comisiones (40% del total)

**Fórmula:**
```
Casos/mes = Usuarios activos × 20% (chat IA) × 50% (hire)
Ingreso = Casos/mes × $87,500 CLP
```

**Proyección:**
```
Año 1:
- Mes 1: 100 usuarios × 10% = 10 casos × $87,500 = $875,000 CLP ($972 USD)
- Mes 12: 500 usuarios × 10% = 50 casos × $87,500 = $4,375,000 CLP ($4,861 USD)
- Promedio mensual: $2,250,000 CLP ($2,500 USD)
- Total anual: $27M CLP ($30K USD)

Año 2:
- Promedio mensual: $17,400,000 CLP ($19,333 USD)
- Total anual: $209M CLP ($232K USD)

Año 3:
- Promedio mensual: $60M CLP ($66,667 USD)
- Total anual: $720M CLP ($800K USD)
```

### Stream 2: Suscripciones Abogados (25% del total)

**Fórmula:**
```
Ingreso = (Abogados × % Free × $0) +
          (Abogados × % Profesional × $55) +
          (Abogados × % Premium × $135) +
          (Abogados × % Firma × $330)
```

**Proyección:**
```
Año 1:
- 100 abogados promedio
- 60% Free, 30% Pro ($55), 10% Premium ($135)
- Mensual: (30 × $55) + (10 × $135) = $3,000 USD
- Total anual: $36K → ajustado $17K (crecimiento gradual)

Año 2:
- 500 abogados promedio
- 50% Free, 35% Pro, 13% Premium, 2% Firma
- Mensual: (175 × $55) + (65 × $135) + (10 × $330) = $16,500 USD
- Total anual: $198K → ajustado $192K

Año 3:
- 1,000 abogados
- 40% Free, 45% Pro, 13% Premium, 2% Firma
- Mensual: (450 × $55) + (130 × $135) + (20 × $330) = $49,500 USD
- Total anual: $594K → ajustado $588K
```

### Stream 3: Servicios Automatizados (20% del total)

**Fórmula:**
```
Servicios vendidos = Usuarios × % Conversión
Ingreso = Servicios × $22 USD
```

**Proyección:**
```
Año 1:
- 500 usuarios/mes promedio × 10% = 50 servicios/mes
- Mensual: 50 × $22 = $1,100 USD
- Total anual: $13.2K

Año 2:
- 5,000 usuarios/mes promedio × 15% = 750 servicios/mes
- Mensual: 750 × $22 = $16,500 USD
- Total anual: $198K → ajustado $220K

Año 3:
- 20,000 usuarios/mes × 20% = 4,000 servicios/mes
- Mensual: 4,000 × $22 = $88,000 USD
- Total anual: $1.056M → ajustado $1.33M
```

### Stream 4: B2B Corporativo (10% del total)

**Proyección:**
```
Año 1: $0 (no hay foco B2B aún)

Año 2:
- Q1-Q2: 0 clientes
- Q3: 3 empresas × $444/mes = $1,332/mes
- Q4: 10 empresas × $444/mes = $4,440/mes
- Total anual: ~$56K

Año 3:
- Promedio: 40 empresas
- Mensual: 40 × $444 = $17,760 USD
- Total anual: $213K → ajustado $467K
```

### Stream 5: Partnerships (5% del total)

**Proyección:**
```
Año 1: $6K
Año 2: $33K
Año 3: $117K
```

---

## 3. UNIT ECONOMICS

### Customer (Usuario que paga)

```
CAC (Customer Acquisition Cost):
- Año 1: $50
- Año 2: $30
- Año 3: $20

LTV (Lifetime Value):
- Casos promedio por cliente en 5 años: 2
- Valor promedio por caso: $25 (comisión JusticiaAI)
- LTV = 2 × $25 = $50

LTV/CAC:
- Año 1: $50 / $50 = 1.0x
- Año 2: $50 / $30 = 1.67x
- Año 3: $50 / $20 = 2.5x

Payback Period:
- Año 1: 12 meses
- Año 2: 7 meses
- Año 3: 5 meses
```

### Abogado

```
CAC Abogado: $200 (recruitment + onboarding)

LTV Abogado:
- Permanencia: 3 años
- Casos: 8/año × 3 años = 24 casos
- Comisiones generadas: 24 × $97 = $2,328
- Suscripción promedio: $55 × 36 meses = $1,980
- LTV Total: $4,308

LTV/CAC: $4,308 / $200 = 21.5x ✅
```

---

## 4. P&L (PROFIT & LOSS)

### Año 1

**Ingresos:**
```
Comisiones:        $30,000
Suscripciones:     $17,000
Automatizados:     $13,200
B2B:               $0
Partnerships:      $6,000
------------------------
Total:             $66,200
```

**Costos:**
```
COGS (20%):        $13,240
- Comisiones pago: $2,000
- Hosting/infra:   $6,000
- API costs:       $5,240

R&D (35%):         $23,170
- Salarios dev:    $18,000
- Tools:           $3,600
- Other:           $1,570

S&M (30%):         $19,860
- CAC spend:       $15,000
- Marketing:       $4,860

G&A (15%):         $9,930
- CEO salary:      $6,000
- Admin:           $3,930
------------------------
Total Costs:       $66,200

EBITDA:            $0 (break-even por diseño)
```

### Año 2

**Ingresos:**
```
Comisiones:        $232,000
Suscripciones:     $192,000
Automatizados:     $220,000
B2B:               $56,000
Partnerships:      $33,000
------------------------
Total:             $733,000
```

**Costos:**
```
COGS (25%):        $183,250
R&D (30%):         $219,900
S&M (28%):         $205,240
G&A (12%):         $87,960
------------------------
Total Costs:       $696,350

EBITDA:            $36,650 (5% margin)
```

### Año 3

**Ingresos:**
```
Comisiones:        $800,000
Suscripciones:     $588,000
Automatizados:     $1,333,000
B2B:               $467,000
Partnerships:      $117,000
------------------------
Total:             $3,305,000
```

**Costos:**
```
COGS (15%):        $495,750
R&D (25%):         $826,250
S&M (20%):         $661,000
G&A (10%):         $330,500
------------------------
Total Costs:       $2,313,500

EBITDA:            $991,500 (30% margin)
```

---

## 5. CASH FLOW

### Funding Round
```
Inversión Semilla: $400,000 USD
Timing: Mes 1

Uso de Fondos:
- Desarrollo (40%):    $160,000
- Marketing (30%):     $120,000
- Operaciones (20%):   $80,000
- Legal/Buffer (10%):  $40,000
```

### Burn Rate

**Año 1:**
```
Ingresos mensuales promedio: $5,517
Costos mensuales promedio:   $5,517
Burn mensual: $0 (diseñado para break-even)

Pero necesitas la inversión para:
- Setup inicial
- Team completo
- Marketing agresivo
```

**Año 2:**
```
Ingresos mensuales: $61,083
Costos mensuales:   $58,029
Flujo positivo:     $3,054/mes
```

**Año 3:**
```
Ingresos mensuales: $275,417
Costos mensuales:   $192,792
Flujo positivo:     $82,625/mes
```

### Runway
```
Con $400K inversión:
- Burn promedio primeros 12 meses: $20K/mes
- Runway: 20 meses ✅
- Target: llegar a flujo positivo en mes 18
```

---

## 6. MÉTRICAS CLAVE (KPIs)

### Dashboard Metrics

```
Año 1:
- ARR: $66K
- MRR (Mes 12): $8K
- Usuarios activos: 2,000/mes
- Abogados activos: 100
- Casos/mes: 30
- Burn mensual: break-even
- Gross Margin: 60%
- LTV/CAC: 1.0x

Año 2:
- ARR: $733K (+1,008%)
- MRR (Mes 24): $70K
- Usuarios activos: 10,000/mes
- Abogados activos: 500
- Casos/mes: 200
- Cash flow positivo: $3K/mes
- Gross Margin: 75%
- LTV/CAC: 1.67x

Año 3:
- ARR: $3.3M (+351%)
- MRR (Mes 36): $300K
- Usuarios activos: 30,000/mes
- Abogados activos: 1,000
- Casos/mes: 600
- Cash flow positivo: $83K/mes
- Gross Margin: 85%
- LTV/CAC: 2.5x
```

---

## 7. SENSIBILIDAD Y ESCENARIOS

### Escenario Pesimista (70% del base)
```
Año 1: $46K ARR
Año 2: $513K ARR
Año 3: $2.3M ARR
```

### Escenario Base (presentado arriba)
```
Año 1: $66K ARR
Año 2: $733K ARR
Año 3: $3.3M ARR
```

### Escenario Optimista (150% del base)
```
Año 1: $99K ARR
Año 2: $1.1M ARR
Año 3: $5M ARR
```

---

## 8. FORMULAS PARA EXCEL

### Revenue
```excel
=SUMPRODUCT(Usuarios_Array, Conversion_Rate, Avg_Transaction_Value)
```

### CAC
```excel
=Total_Marketing_Spend / New_Customers_Acquired
```

### LTV
```excel
=Avg_Revenue_Per_Customer * Avg_Customer_Lifetime_Months * Gross_Margin
```

### Gross Margin
```excel
=(Revenue - COGS) / Revenue
```

### Burn Rate
```excel
=Total_Costs - Total_Revenue
```

### Runway
```excel
=Cash_Balance / Monthly_Burn_Rate
```

---

## SIGUIENTE PASO

Con estos datos, puedo crear:
1. Archivo Excel con todas las hojas
2. Fórmulas automatizadas
3. Gráficos dinámicos
4. Formato profesional

¿Quieres que cree el Excel completo ahora?
