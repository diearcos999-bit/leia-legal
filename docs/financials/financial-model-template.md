# Modelo Financiero JusticiaAI - Template para Excel

## Instrucciones para Crear el Modelo en Excel

Este documento proporciona la estructura completa para crear el modelo financiero en Excel/Google Sheets.

---

## SHEET 1: Assumptions (Supuestos)

### A. Growth Assumptions

| Métrica | Año 1 | Año 2 | Año 3 | Notas |
|---------|-------|-------|-------|-------|
| **Usuarios Nuevos/Mes** | | | | |
| Q1 | 150 | 3,000 | 10,000 | Crecimiento acelerado |
| Q2 | 300 | 4,000 | 12,000 | |
| Q3 | 500 | 5,000 | 15,000 | |
| Q4 | 700 | 6,000 | 18,000 | |
| **Total Usuarios Nuevos/Año** | 1,650 | 18,000 | 55,000 | |
| **Usuarios Activos Fin de Año** | 2,000 | 15,000 | 50,000 | Con churn |

| **Abogados** | | | | |
| Nuevos/Mes (promedio) | 8 | 33 | 42 | |
| Total Abogados Fin de Año | 100 | 500 | 1,000 | |
| % Abogados Activos | 70% | 75% | 80% | Que reciben casos |

| **Conversion Rates** | | | | |
| Visitor → Usuario Registrado | 15% | 20% | 25% | Mejora con optimización |
| Usuario → Usa IA | 60% | 65% | 70% | |
| Usa IA → Solicita Abogado | 20% | 25% | 30% | |
| Solicita → Contrata (paga) | 50% | 55% | 60% | |
| **Overall Conversion** | 0.9% | 2.2% | 3.2% | Visitor → Customer |

### B. Pricing Assumptions

| Fuente de Ingreso | Año 1 | Año 2 | Año 3 |
|-------------------|-------|-------|-------|
| **Comisión Marketplace** | 25% | 25% | 25% |
| Honorario Promedio Caso | $300K | $350K | $400K |
| Comisión Promedio por Caso | $75K | $87K | $100K |

| **Suscripciones Abogados** | | | |
| Plan Gratis (% abogados) | 85% | 60% | 40% |
| Plan Profesional ($50K/mes) | 12% | 30% | 45% |
| Plan Premium ($120K/mes) | 3% | 9% | 13% |
| Plan Firma ($300K+/mes) | 0% | 1% | 2% |
| ARPA (Avg Rev per Abogado/mes) | $12.6K | $28.8K | $44.1K |

| **Servicios Automatizados** | | | |
| Precio Promedio | $20K | $22K | $25K |
| % Usuarios que Compran | 10% | 15% | 20% |
| Compras/Usuario/Año | 0.1 | 0.15 | 0.2 |

| **B2B Corporativo** | | | |
| Clientes B2B Fin de Año | 0 | 50 | 200 |
| ARPA Mensual B2B | N/A | $300K | $350K |

### C. Cost Assumptions

| **COGS (Cost of Goods Sold)** | Año 1 | Año 2 | Año 3 |
|--------------------------------|-------|-------|-------|
| Payment Processing Fee | 3.5% | 3.5% | 3.5% |
| AI API Cost per Conversation | $0.50 | $0.40 | $0.30 |
| Conversations/Usuario/Mes | 2 | 2.5 | 3 |
| Infrastructure (AWS) | $10K/mes | $40K/mes | $100K/mes |

| **Operating Expenses** | | | |
| Salarios (ver detalle abajo) | $700K | $1,500K | $2,500K |
| Marketing | $68K | $180K | $300K |
| Legal & Compliance | $40K | $50K | $60K |
| Office & Admin | $20K | $40K | $60K |
| Software & Tools | $24K | $48K | $72K |

| **CAC por Canal** | | | |
| Google Ads | $20 | $18 | $15 |
| Facebook/Instagram | $15 | $13 | $12 |
| Organic (SEO) | $3 | $2 | $1 |
| Partnerships | $10 | $8 | $6 |
| Weighted Average CAC | $15 | $12 | $10 |

### D. Headcount Assumptions

| Rol | Salary/Mes (CLP) | Año 1 | Año 2 | Año 3 |
|-----|------------------|-------|-------|-------|
| CEO/Founder | $0 | 1 | 1 | 1 |
| CTO | $2,500K | 1 | 1 | 1 |
| Developers | $1,800K | 2 → 4 | 6 | 10 |
| AI/ML Engineer | $2,000K | 1 | 2 | 3 |
| Product Designer | $1,500K | 0.5 → 1 | 2 | 3 |
| Product Manager | $1,800K | 0 | 1 | 2 |
| Marketing/Growth | $1,500K | 0.5 → 1 | 2 | 4 |
| Sales (B2B) | $1,500K | 0 | 2 | 6 |
| Customer Support | $800K | 0.5 → 1 | 3 | 6 |
| Legal/Compliance | $1,200K | 0.25 → 0.5 | 1 | 1 |
| Operations | $1,000K | 0 | 1 | 2 |
| Data Analyst | $1,500K | 0 | 1 | 2 |
| **Total Headcount** | | **6 → 10** | **23** | **41** |
| **Total Payroll/Mes** | | **$58M** | **$125M** | **$208M** |
| **Total Payroll/Año** | | **$700M** | **$1,500M** | **$2,500M** |

---

## SHEET 2: Revenue Model

### Monthly Revenue Breakdown (Año 1)

| Mes | Usuarios Activos | Casos Cerrados | Comisiones | Subs Abogados | Automatizados | B2B | Total MRR |
|-----|------------------|----------------|------------|---------------|---------------|-----|-----------|
| 1 | 100 | 5 | $0.4M | $0.5M | $0.1M | $0 | $1M |
| 2 | 150 | 10 | $0.8M | $0.7M | $0.2M | $0 | $1.7M |
| 3 | 250 | 15 | $1.1M | $1M | $0.3M | $0 | $2.4M |
| 4 | 400 | 20 | $1.5M | $1.3M | $0.4M | $0 | $3.2M |
| 5 | 600 | 25 | $1.9M | $1.7M | $0.6M | $0 | $4.2M |
| 6 | 850 | 30 | $2.3M | $2M | $0.8M | $0 | $5.1M |
| 7 | 1,200 | 35 | $2.6M | $2.5M | $1M | $0 | $6.1M |
| 8 | 1,500 | 40 | $3M | $3M | $1.2M | $0 | $7.2M |
| 9 | 1,800 | 45 | $3.4M | $3.5M | $1.4M | $0 | $8.3M |
| 10 | 2,000 | 50 | $3.8M | $4M | $1.6M | $0 | $9.4M |
| 11 | 2,000 | 50 | $3.8M | $4.5M | $1.6M | $0 | $9.9M |
| 12 | 2,000 | 50 | $3.8M | $5M | $1.6M | $0 | $10.4M |
| **Total Año 1** | | **360** | **$27M** | **$15M** | **$12M** | **$0** | **$59M CLP** |

**En USD**: $66K (TC: 900 CLP/USD)

### Annual Revenue Summary (3 Years)

| Fuente | Año 1 (CLP) | Año 1 (USD) | Año 2 (CLP) | Año 2 (USD) | Año 3 (CLP) | Año 3 (USD) |
|--------|-------------|-------------|-------------|-------------|-------------|-------------|
| **Comisiones** | $27M | $30K | $209M | $233K | $720M | $800K |
| **Suscripciones** | $15M | $17K | $173M | $192K | $529M | $588K |
| **Automatizados** | $12M | $13K | $198M | $220K | $1,200M | $1,333K |
| **B2B** | $0 | $0 | $50M | $56K | $420M | $467K |
| **Partnerships** | $5M | $6K | $30M | $33K | $105M | $117K |
| **Total Revenue** | **$59M** | **$66K** | **$660M** | **$734K** | **$2,974M** | **$3.3M** |

**Growth Rate**:
- Año 1→2: +1,018% (early stage hypergrowth)
- Año 2→3: +350%

---

## SHEET 3: Cost Structure

### COGS (Cost of Goods Sold)

| Item | Año 1 | Año 2 | Año 3 |
|------|-------|-------|-------|
| **Payment Processing** | $2M | $23M | $104M |
| (3.5% de revenue) | | | |
| **AI API Costs** | $8M | $50M | $120M |
| (Conversations × $0.40 avg) | | | |
| **Infrastructure (AWS)** | $5M | $16M | $108M |
| **Total COGS** | **$15M** | **$89M** | **$332M** |
| **Gross Profit** | **$44M** | **$571M** | **$2,642M** |
| **Gross Margin** | **75%** | **87%** | **89%** |

### Operating Expenses (OpEx)

| Categoría | Año 1 | Año 2 | Año 3 |
|-----------|-------|-------|-------|
| **Salarios** | $700M | $1,500M | $2,500M |
| **Marketing & Sales** | $68M | $180M | $300M |
| **Legal & Compliance** | $40M | $50M | $60M |
| **Office & Admin** | $20M | $40M | $60M |
| **Software & Tools** | $24M | $48M | $72M |
| **Total OpEx** | **$852M** | **$1,818M** | **$2,992M** |

### P&L Summary

| Línea | Año 1 | Año 2 | Año 3 |
|-------|-------|-------|-------|
| **Revenue** | $59M | $660M | $2,974M |
| **COGS** | ($15M) | ($89M) | ($332M) |
| **Gross Profit** | $44M | $571M | $2,642M |
| **Gross Margin** | 75% | 87% | 89% |
| **OpEx** | ($852M) | ($1,818M) | ($2,992M) |
| **EBITDA** | **($808M)** | **($1,247M)** | **($350M)** |
| **EBITDA Margin** | -1,369% | -189% | -12% |
| **Break-even** | | | **Q4 Año 3** |

**Conversión a USD**:
- Año 1 EBITDA: -$898K
- Año 2 EBITDA: -$1,386K
- Año 3 EBITDA: -$389K

**Path to Profitability**: Q2-Q3 Año 4 (proyectado)

---

## SHEET 4: Cash Flow & Funding

### Sources & Uses (Ronda Semilla: $400K USD)

**Sources**:
- Seed Round: $400,000 USD
- (Equivalente: $360M CLP a TC 900)

**Uses**:
| Categoría | Monto (USD) | % | Monto (CLP) |
|-----------|-------------|---|-------------|
| **Desarrollo** | $160K | 40% | $144M |
| - Salarios tech (6 meses) | $120K | | $108M |
| - Infrastructure & Tools | $40K | | $36M |
| **Marketing** | $120K | 30% | $108M |
| - Paid acquisition | $80K | | $72M |
| - Content & PR | $30K | | $27M |
| - Tools & events | $10K | | $9M |
| **Operaciones** | $80K | 20% | $72M |
| - Salarios non-tech | $50K | | $45M |
| - Office & admin | $20K | | $18M |
| - Recruitment | $10K | | $9M |
| **Legal & Contingencia** | $40K | 10% | $36M |
| - Setup legal | $15K | | $13.5M |
| - Seguros (1 año) | $15K | | $13.5M |
| - Contingencia | $10K | | $9M |
| **Total** | **$400K** | **100%** | **$360M** |

**Runway**: 18 meses con $400K (quema $22K/mes promedio)

### Monthly Cash Flow (Año 1)

| Mes | Revenue | COGS | OpEx | Net Cash Flow | Cumulative Cash |
|-----|---------|------|------|---------------|-----------------|
| 0 | $0 | $0 | $0 | **+$400K** | $400K |
| 1 | $1.1K | ($0.4K) | ($70K) | ($69K) | $331K |
| 2 | $1.9K | ($0.6K) | ($70K) | ($69K) | $262K |
| 3 | $2.7K | ($0.8K) | ($72K) | ($70K) | $192K |
| 4 | $3.6K | ($1K) | ($72K) | ($69K) | $123K |
| 5 | $4.7K | ($1.3K) | ($74K) | ($71K) | $52K |
| 6 | $5.7K | ($1.5K) | ($74K) | ($70K) | ($18K) |
| ... | | | | | |
| 12 | $11.6K | ($3K) | ($80K) | ($71K) | **($546K)** |

**Cash Need End of Year 1**: ~$546K adicionales
**Total Funding Required Año 1-2**: ~$900K USD

### Funding Strategy

| Ronda | Timing | Monto | Dilución | Valoración Post | Uso |
|-------|--------|-------|----------|-----------------|-----|
| **Seed** | Mes 0 | $400K | 15-20% | $2-2.5M | MVP + 18 meses |
| **Bridge** | Mes 12 | $300K | 5-8% | $4-5M | Extend runway 12 meses |
| **Series A** | Mes 24 | $2-3M | 20-25% | $10-12M | Scale to profitability |

---

## SHEET 5: Unit Economics

### Customer Unit Economics

| Métrica | Año 1 | Año 2 | Año 3 | Cálculo |
|---------|-------|-------|-------|---------|
| **CAC** | $20 | $15 | $12 | Marketing / New Users |
| **Avg Transaction Value** | $75 | $87 | $100 | Comisión por caso |
| **Purchase Frequency** | 0.2× | 0.25× | 0.3× | Casos/Usuario/Año |
| **Customer Lifespan** | 3 años | 3 años | 3 años | Estimado |
| **LTV** | $45 | $65 | $90 | ATV × Freq × Lifespan |
| **LTV/CAC** | **2.3x** | **4.3x** | **7.5x** | Target: >3x |
| **Payback Period** | 8 meses | 5 meses | 3 meses | CAC / (Monthly ARPU) |

**Healthy Target**: LTV/CAC > 3x, Payback < 12 meses ✅

### Lawyer Unit Economics

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| **CAC (Lawyer)** | $200 | $150 | $100 |
| **Avg Cases/Lawyer/Mes** | 2 | 3 | 4 |
| **Commission/Lawyer/Mes** | $150 | $261 | $400 |
| **Subscription/Lawyer/Mes** | $12.6K | $28.8K | $44.1K |
| **Total Rev/Lawyer/Mes** | $162.6K | $289.8K | $444.1K |
| **LTV (3 años)** | $5,854K | $10,433K | $15,988K |
| **LTV/CAC** | **29x** | **70x** | **160x** | Excelente |

**Insight**: Abogados tienen economics mucho mejores que usuarios finales. Priorizar retención de abogados.

---

## SHEET 6: Key Metrics Dashboard

### North Star Metric
**Casos Resueltos Exitosamente / Mes**

| | Q1 | Q2 | Q3 | Q4 | Total Año |
|-|----|----|----|----|-----------|
| **Año 1** | 30 | 75 | 120 | 150 | 375 |
| **Año 2** | 400 | 600 | 800 | 1,000 | 2,800 |
| **Año 3** | 1,500 | 1,800 | 2,000 | 2,200 | 7,500 |

### Acquisition Metrics

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| Website Visitors/Mes | 20K | 100K | 300K |
| Conversion to Registered | 15% | 20% | 25% |
| New Users/Mes (avg) | 150 | 1,500 | 5,000 |
| New Lawyers/Mes (avg) | 8 | 33 | 42 |
| CAC Users | $20 | $15 | $12 |
| CAC Lawyers | $200 | $150 | $100 |

### Engagement Metrics

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| DAU/MAU Ratio | 25% | 30% | 35% |
| IA Conversations/User | 2 | 2.5 | 3 |
| Time on Site (min) | 8 | 10 | 12 |
| % Users that Request Lawyer | 20% | 25% | 30% |

### Retention Metrics

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| Monthly Churn (Users) | 15% | 12% | 10% |
| Monthly Churn (Lawyers) | 10% | 8% | 5% |
| NPS | 45 | 50 | 55 |
| Repeat Usage Rate | 10% | 15% | 20% |

### Revenue Metrics

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| MRR (End of Year) | $10.4M | $60M | $270M |
| ARR | $59M | $660M | $2,974M |
| ARPU (Users) | $30K | $44K | $59K |
| ARPA (Lawyers) | $150K | $347K | $529K |
| Net Revenue Retention | N/A | 85% | 95% |

---

## SHEET 7: Sensitivity Analysis

### Scenario Planning

#### Base Case (Presentado arriba)
- Growth: Moderado (100% → 350%)
- CAC: $20 → $12
- Conversion: 0.9% → 3.2%

#### Optimistic Case (+30% all metrics)
| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| ARR | $86K | $954K | $4.3M |
| EBITDA | ($700K) | ($900K) | Break-even |
| Funding Needed | $350K | $600K | $0 |

#### Pessimistic Case (-30% growth, +30% costs)
| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| ARR | $46K | $514K | $2.3M |
| EBITDA | ($1.1M) | ($1.8M) | ($800K) |
| Funding Needed | $500K | $1.2M | $600K |

### Break-even Analysis

**Variables**:
- Fixed Costs/Mes: $150K (Año 3)
- Variable Cost/User: $5
- Avg Revenue/User/Mes: $60

**Break-even Volume**: 2,500 usuarios activos pagando

**Achievable**: Q4 Año 3 según proyección base

---

## SHEET 8: Comparables & Valuation

### Legaltech Comparables

| Company | ARR | Valuation | Multiple | Stage |
|---------|-----|-----------|----------|-------|
| **LegalZoom** | $500M | $1.5B | 3x | Public |
| **Rocket Lawyer** | $100M | $500M | 5x | Late Stage |
| **Clio** | $200M | $1.6B | 8x | Late Stage |
| **Total Abogados** | ~$2M | $10M | 5x | Early Stage |

**Average Multiple (Early Stage)**: 5-10x ARR

### JusticiaAI Valuation

**Seed Round** (Año 0):
- Pre-money: $1.6-2M
- Investment: $400K
- Post-money: $2-2.4M
- Dilución: 16-20%

**Series A** (Año 2, $660K ARR):
- Pre-money: $8-10M (12-15x ARR)
- Investment: $2-3M
- Post-money: $10-13M
- Dilución: 20-23%

**Exit Scenarios (Año 5, proyectado $15M ARR)**:

| Scenario | ARR | Multiple | Valuation | ROI (desde Seed) |
|----------|-----|----------|-----------|------------------|
| **Conservative** | $12M | 4x | $48M | **24x** |
| **Base** | $15M | 6x | $90M | **45x** |
| **Optimistic** | $20M | 8x | $160M | **80x** |

---

## Instrucciones para Implementar en Excel

### Setup

1. **Crear archivo nuevo**: "JusticiaAI-Financial-Model-v1.xlsx"
2. **Crear 8 sheets** según estructura arriba
3. **Color coding**:
   - Inputs (amarillo)
   - Calculations (blanco)
   - Outputs (verde claro)
4. **Formulas**: Linkar todo (no hardcodear números)

### Formulas Clave

**Revenue** (Sheet 2, Mes X):
```excel
=Casos_Cerrados * Honorario_Promedio * Comision_Rate
```

**CAC**:
```excel
=Marketing_Spend / New_Users
```

**LTV**:
```excel
=ARPU * 12 * Customer_Lifespan_Years * Gross_Margin
```

**Cash Balance**:
```excel
=Previous_Month_Cash + Revenue - COGS - OpEx
```

### Validaciones

- [ ] Todas las filas suman correctamente
- [ ] Año 1 total = suma de Q1-Q4
- [ ] CAC × Users = Marketing budget
- [ ] Payroll = Headcount × Salaries
- [ ] Cash balance tracks across months

### Gráficos Recomendados

1. **ARR Growth** (línea, 3 años)
2. **Revenue Mix** (stacked bar por fuente)
3. **Cash Balance** (línea con fundraising events)
4. **Unit Economics** (LTV/CAC por año)
5. **Path to Profitability** (EBITDA por quarter)

---

## Exportar para Inversionistas

### Versiones

1. **Full Model** (internal): Todas las sheets, editable
2. **Investor View** (external): Solo sheets 2, 4, 6, 7, 8 - protected
3. **PDF Summary**: 2 páginas con highlights + gráficos

### Presentación

- Enviar modelo 24-48h antes de meeting
- Estar preparado para defender supuestos
- Tener sensitivities listas (qué pasa si...)

---

**Próximo Paso**: Implementar este template en Excel/Google Sheets con todas las fórmulas linkeadas.

**Tiempo Estimado**: 3-4 horas para crear modelo completo funcional.
