# Estrategia de Compliance - JusticiaAI

## 1. Marco Regulatorio Aplicable

### 1.1 Protección de Datos

#### Ley 21.719 (Nueva Ley de Protección de Datos Personales)
**Entrada en Vigor**: 1 de diciembre de 2026

**Principios Clave**:
- Legalidad, lealtad y transparencia
- Limitación de finalidad
- Minimización de datos
- Exactitud
- Limitación del plazo de conservación
- Integridad y confidencialidad

**Derechos de los Titulares (ARCO Plus)**:
- Acceso
- Rectificación
- Cancelación
- Oposición
- Portabilidad (nuevo)
- Olvido (nuevo)

**Obligaciones para JusticiaAI**:
- ✅ Designar responsable de datos
- ✅ Registro de actividades de tratamiento
- ✅ Evaluación de Impacto (EIPDP) para tratamientos de alto riesgo
- ✅ Notificación de brechas de seguridad (72 horas)
- ✅ Obtener consentimiento explícito
- ✅ Política de privacidad clara

#### Ley 19.628 (Vigente hasta 2026)
**Aplicable hasta**: Diciembre 2026

**Cumplimiento Básico**:
- Informar sobre tratamiento de datos
- Permitir oposición al tratamiento
- Mantener datos exactos y actualizados

### 1.2 Firma Electrónica

#### Ley 19.799

**Aplicable a**:
- Contratos generados por la plataforma
- Acuerdos entre usuario y abogado
- Documentos legales

**Requisitos**:
- **Firma Electrónica Simple**: Válida para contratos privados
- **Firma Electrónica Avanzada (FEA)**: Requerida para documentos con efectos de instrumento público

**Implementación**:
- Fase 1: Firma simple (checkbox + IP + timestamp)
- Fase 2: Integración con proveedores FEA certificados (Mifiel, otros)

### 1.3 Defensa del Consumidor (Ley 19.496)

**Aplicable como**: Proveedor de servicios de intermediación

**Obligaciones**:
- ✅ Información veraz y oportuna
- ✅ Precios claros (incluyendo comisiones)
- ✅ Derecho a retracto (7 días) en servicios no iniciados
- ✅ No cláusulas abusivas en T&C
- ✅ Procedimiento de reclamos claro

**Riesgos**:
- Publicidad engañosa
- Falta de transparencia en precios
- Incumplimiento de servicios prometidos

### 1.4 Ejercicio de la Abogacía

**Situación Actual**:
- NO existe colegiatura obligatoria en Chile
- NO existe regulación específica para plataformas legales

**Restricciones para JusticiaAI**:
- ❌ NO podemos ejercer la abogacía (solo intermediamos)
- ❌ NO podemos dar asesoría legal (solo orientación general con IA)
- ❌ NO podemos representar clientes en tribunales

**Claridad en Comunicaciones**:
- "JusticiaAI conecta usuarios con abogados independientes"
- "No somos un despacho legal, somos una plataforma tecnológica"
- IA ofrece "orientación general, no asesoría legal"

### 1.5 Facturación Electrónica

#### Integración con SII

**Obligaciones**:
- Emitir facturas electrónicas por servicios
- Integración con sistema SII
- Certificado digital de la empresa
- Timbraje electrónico

**Implementación**:
- SDK: lib-sii (Node.js)
- Certificado: Obtener de autoridad certificadora
- Testing: Ambiente de certificación SII antes de producción

## 2. Plan de Compliance

### 2.1 Timeline de Implementación

#### Pre-Lanzamiento (Mes 1-2)
- [ ] Constitución de empresa (SpA)
- [ ] Obtención de RUT y certificado digital
- [ ] Drafting de Términos y Condiciones
- [ ] Drafting de Política de Privacidad
- [ ] Drafting de Contrato con Abogados
- [ ] Obtención de seguros (responsabilidad civil, ciberseguridad)

#### MVP (Mes 3)
- [ ] Implementar sistema de consentimiento
- [ ] Implementar mecanismo de ejercicio de derechos ARCO
- [ ] Configurar logs de auditoría
- [ ] Integración facturación SII (básica)
- [ ] Publicar documentos legales en sitio

#### Post-MVP (Mes 4-12)
- [ ] Evaluación de Impacto en Protección de Datos (EIPDP)
- [ ] Designación formal de Delegado de Protección de Datos
- [ ] Registro de actividades de tratamiento
- [ ] Auditoría de seguridad externa
- [ ] Plan de respuesta a brechas
- [ ] Capacitación de equipo en protección de datos

#### Pre-2026 (Año 2)
- [ ] Actualizar prácticas para Ley 21.719
- [ ] Implementar portabilidad de datos
- [ ] Implementar derecho al olvido
- [ ] Actualizar Política de Privacidad
- [ ] Notificar a Agencia de Protección de Datos

### 2.2 Documentos Legales Requeridos

#### Externos (Usuarios)
1. **Términos y Condiciones**
   - Definición de servicios
   - Responsabilidades y limitaciones
   - Propiedad intelectual
   - Resolución de disputas
   - Terminación de cuenta

2. **Política de Privacidad**
   - Datos recopilados
   - Finalidad del tratamiento
   - Derechos de los titulares
   - Medidas de seguridad
   - Uso de cookies

3. **Disclaimer IA**
   - IA no reemplaza abogado
   - Orientación general, no asesoría
   - Limitaciones del sistema

4. **Política de Cookies**
   - Tipos de cookies usadas
   - Opt-out mechanism

5. **Proceso de Reclamos**
   - Cómo presentar reclamo
   - Plazos de respuesta
   - Escalamiento

#### Internos
6. **Contrato con Abogados**
   - Relación independiente (no empleados)
   - Comisiones y pagos
   - Estándares de calidad
   - Uso de marca
   - Confidencialidad

7. **Acuerdo de Procesamiento de Datos (DPA)**
   - Para proveedores que manejan datos (AWS, SendGrid, etc.)

8. **Política Interna de Seguridad**
   - Controles de acceso
   - Gestión de credenciales
   - Procedimientos de backup
   - Plan de continuidad

9. **Código de Conducta**
   - Para equipo interno
   - Para abogados en la plataforma

### 2.3 Estructura Legal de la Empresa

#### Tipo de Sociedad Recomendado: SpA (Sociedad por Acciones)

**Ventajas**:
- Flexibilidad en estatutos
- Responsabilidad limitada
- Facilidad para captar inversión
- No requiere directorio (opcional)

**Requisitos de Constitución**:
- Escritura pública ante notario
- Inscripción Registro de Comercio
- Publicación Diario Oficial
- Obtención RUT empresa
- Inicio de actividades SII

**Capital Inicial**: Sin mínimo legal (sugerido: $1M CLP)

**Estatutos Clave**:
- Objeto: "Desarrollo y operación de plataforma tecnológica de servicios legales"
- Duración: Indefinida
- Administración: Gerente General (Fundador)
- Emisión de acciones: Clases A (fundadores), B (inversionistas)

#### Marcas y Propiedad Intelectual

**Registro de Marca**: "JusticiaAI"
- Ante INAPI (Instituto Nacional de Propiedad Industrial)
- Clases: 35 (servicios publicitarios y gestión), 42 (servicios tecnológicos)
- Costo: ~$250K CLP
- Plazo: 4-6 meses

**Copyright**:
- Código fuente: Propiedad de JusticiaAI SpA
- Contenido generado por IA: Atribuido a plataforma con disclaimer
- Acuerdos de asignación de IP con developers/contractors

#### Seguros

1. **Responsabilidad Civil Profesional**
   - Cobertura: Errores u omisiones de la plataforma
   - Monto: $100M-500M CLP
   - Costo estimado: $2M-5M CLP/año

2. **Ciberseguridad**
   - Cobertura: Brechas de datos, ataques cibernéticos
   - Monto: $500M CLP
   - Costo estimado: $5M-10M CLP/año

3. **Responsabilidad Civil General**
   - Cobertura: Daños a terceros
   - Monto: $100M CLP

## 3. Gestión de Datos Personales

### 3.1 Datos Recopilados

#### Usuarios (Clientes)
**Datos Básicos**:
- Nombre completo
- RUT
- Email
- Teléfono
- Dirección

**Datos de Cuenta**:
- Usuario/contraseña (hash)
- Preferencias
- Historial de navegación

**Datos de Casos**:
- Descripción de problema legal (potencialmente sensible)
- Documentos subidos
- Comunicaciones con abogados
- Resultados de casos

**Datos de Pago**:
- NO almacenamos datos de tarjetas (tokenizados por Transbank)
- Historial de transacciones

#### Abogados
**Datos Profesionales**:
- Nombre, RUT
- Título profesional y universidad
- Número de inscripción Poder Judicial
- Especialidades
- Experiencia

**Datos Financieros**:
- Cuenta bancaria para payouts
- Historial de transacciones

**Datos de Desempeño**:
- Casos ganados/perdidos
- Ratings y reviews
- Tiempos de respuesta

### 3.2 Finalidades del Tratamiento

1. **Prestación del Servicio**: Conectar usuarios con abogados
2. **Mejora de la Plataforma**: Analytics, ML training
3. **Comunicaciones**: Notificaciones de casos, marketing (con opt-in)
4. **Cumplimiento Legal**: Facturación, registros para autoridades
5. **Seguridad**: Prevención de fraude

### 3.3 Base Legal (Ley 21.719)

| Tratamiento | Base Legal |
|-------------|------------|
| Prestación servicio | Ejecución de contrato |
| Marketing directo | Consentimiento (opt-in) |
| Analytics | Interés legítimo |
| Compartir con abogados | Ejecución de contrato |
| Cumplimiento tributario | Obligación legal |

### 3.4 Retención de Datos

| Tipo de Dato | Período de Retención |
|--------------|---------------------|
| Datos de cuenta activa | Mientras cuenta activa |
| Casos cerrados | 5 años (plazo prescripción legal) |
| Facturas | 6 años (obligación SII) |
| Logs de auditoría | 2 años |
| Datos de marketing (opt-out) | Eliminados inmediatamente |

**Eliminación Automática**: Cron job mensual que elimina datos que cumplieron retención

### 3.5 Medidas de Seguridad

#### Técnicas
- ✅ Cifrado en tránsito (TLS 1.3)
- ✅ Cifrado en reposo (AES-256)
- ✅ Passwords hasheadas (bcrypt, work factor 12)
- ✅ Tokens JWT con expiración
- ✅ Rate limiting (prevención DDoS)
- ✅ WAF (Web Application Firewall)
- ✅ Backups cifrados (diarios)
- ✅ Network segmentation (VPC privada)

#### Organizacionales
- ✅ Control de acceso basado en roles
- ✅ Logs de auditoría (quién accedió a qué)
- ✅ Revisión de accesos trimestral
- ✅ Capacitación anual de equipo en seguridad
- ✅ NDA con todos los empleados/contractors
- ✅ Background checks para team con acceso a datos

#### Procedimentales
- ✅ Plan de respuesta a incidentes
- ✅ Pruebas de seguridad anuales (pentest)
- ✅ Vulnerability scanning automatizado
- ✅ Disaster recovery plan
- ✅ Business continuity plan

### 3.6 Ejercicio de Derechos ARCO

**Mecanismo**: Formulario web + email (privacidad@justiciaai.cl)

**Plazos de Respuesta**:
- Acceso: 10 días hábiles
- Rectificación: 5 días hábiles
- Cancelación: 10 días hábiles
- Portabilidad: 15 días hábiles

**Implementación Técnica**:
- Dashboard de privacidad en cuenta de usuario
- Opción "Descargar mis datos" (JSON/PDF)
- Opción "Eliminar mi cuenta" (soft delete, retención de logs por seguridad)

### 3.7 Notificación de Brechas

**Obligación (Ley 21.719)**: Notificar a Agencia y afectados dentro de 72 horas

**Plan de Respuesta**:
```
1. Detección de Brecha
   ↓
2. Contención (inmediata)
   ↓
3. Evaluación de Impacto (<4 horas)
   ↓
4. Notificación Interna (CEO, Legal)
   ↓
5. Notificación Agencia (<72 horas)
   ↓
6. Notificación Afectados (si alto riesgo)
   ↓
7. Remediación
   ↓
8. Post-Mortem
```

**Template de Notificación**: Pre-preparado

## 4. Relación con Abogados

### 4.1 Naturaleza de la Relación

**Modelo**: Contratistas Independientes (NO empleados)

**Razones**:
- Flexibilidad para abogados (horarios, casos)
- Menor carga laboral para plataforma
- Escalabilidad
- Abogados mantienen práctica independiente

**Riesgos de Clasificación Errónea**:
- Si Inspección del Trabajo determina que son empleados:
  - Multas
  - Pago retroactivo de cotizaciones previsionales
  - Indemnizaciones

**Mitigación**:
- Contrato claramente especifica independencia
- Abogados fijan sus propios honorarios
- No hay exclusividad
- No hay horario fijo
- Pueden rechazar casos

### 4.2 Contrato con Abogados (Outline)

**Cláusulas Clave**:

1. **Naturaleza del Acuerdo**: Independencia, no relación laboral
2. **Servicios**: Prestación de servicios legales a clientes de la plataforma
3. **Comisiones**: X% sobre honorarios, pago neto a 15 días
4. **Estándares de Calidad**:
   - Responder consultas en <24 horas
   - Mantener comunicación profesional
   - Cumplir ética profesional
5. **Propiedad Intelectual**: Contenido generado por abogado es suyo
6. **Confidencialidad**: No compartir información de clientes fuera de plataforma
7. **Uso de Marca**: Permiso limitado para decir "abogado en JusticiaAI"
8. **Terminación**: Cualquiera puede terminar con 30 días de aviso
9. **Responsabilidad**: Abogado responsable de su práctica profesional
10. **Jurisdicción**: Tribunales de Santiago, Chile

### 4.3 Verificación de Abogados

**Proceso**:
```
1. Registro y solicitud
2. Verificación Automática:
   - Búsqueda en registro Poder Judicial (web scraping)
   - Verificación RUT (SII API)
3. Verificación Manual:
   - Revisión de título profesional (PDF)
   - Verificación universidad (llamada/email)
   - Background check básico (optional)
4. Entrevista (video o presencial)
5. Aprobación o Rechazo
6. Onboarding
```

**Criterios de Aprobación**:
- Título válido de abogado
- Inscrito en lista de abogados Poder Judicial
- Sin antecedentes de sanciones éticas graves (manual search)
- Entrevista satisfactoria

**Rechazo si**:
- Título falso o no verificable
- No inscrito en Poder Judicial
- Antecedentes penales graves
- Mala conducta profesional conocida

## 5. Términos y Condiciones (Outline)

### 5.1 Para Usuarios

**Secciones**:

1. **Aceptación de Términos**: Al usar la plataforma, acepta T&C
2. **Descripción de Servicios**:
   - Plataforma de intermediación
   - IA ofrece orientación general
   - NO somos abogados, NO damos asesoría legal
3. **Registro de Cuenta**:
   - Información veraz
   - Responsabilidad por credenciales
   - Prohibido compartir cuenta
4. **Uso de la Plataforma**:
   - Uso legal y ético
   - Prohibiciones (spam, fraude, etc.)
5. **Servicios de IA**:
   - Orientación general, no asesoría legal
   - No garantizamos exactitud absoluta
   - Recomendamos verificar con abogado
6. **Relación con Abogados**:
   - Contrato independiente entre usuario y abogado
   - JusticiaAI solo intermedia
   - Abogados son profesionales independientes
7. **Pagos y Comisiones**:
   - Precios publicados por abogados
   - Comisión de plataforma (X%)
   - Política de reembolsos
8. **Propiedad Intelectual**:
   - JusticiaAI es marca registrada
   - Contenido de la plataforma protegido por copyright
9. **Limitación de Responsabilidad**:
   - NO responsables por actuación de abogados
   - NO garantizamos resultados de casos
   - Responsabilidad limitada a monto pagado
10. **Resolución de Disputas**:
    - Mediación primero
    - Arbitraje si mediación falla
    - Jurisdicción: Santiago, Chile
11. **Modificaciones**: Derecho a modificar T&C con aviso
12. **Terminación**: Podemos terminar cuenta por violación de T&C

### 5.2 Para Abogados

Similar a usuarios, con adiciones:
- Obligaciones profesionales
- Estándares de calidad
- Sistema de ratings
- Causales de suspensión/terminación
- Pagos y comisiones detalladas

## 6. Política de Privacidad (Outline)

**Secciones**:
1. Introducción
2. Datos que recopilamos
3. Cómo usamos los datos
4. Base legal del tratamiento
5. Compartir datos (con quién)
6. Retención de datos
7. Tus derechos (ARCO Plus)
8. Seguridad
9. Cookies
10. Cambios a esta política
11. Contacto (privacidad@justiciaai.cl)

**Lenguaje**: Simple, claro, sin jerga legal

## 7. Gestión de Riesgos

### 7.1 Matriz de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Brecha de datos | Media | Alto | Seguridad robusta, seguros |
| IA da mal consejo | Media | Alto | Disclaimers, supervisión humana |
| Abogado negligente | Media | Medio | Verificación, reviews, seguros |
| Demanda por mala práctica | Baja | Alto | T&C claros, seguro RC |
| Clasificación errónea abogados | Media | Alto | Contrato independiente claro |
| Cambio regulatorio adverso | Baja | Alto | Monitoreo, advocacy proactivo |

### 7.2 Seguros de Cobertura

1. **RC Profesional**: $500M CLP
2. **Ciberseguridad**: $500M CLP
3. **RC General**: $100M CLP
4. **D&O** (Directors & Officers): $200M CLP (cuando haya directorio)

**Costo Total Estimado**: $10-15M CLP/año

## 8. Compliance Continuo

### 8.1 Roles y Responsabilidades

**Delegado de Protección de Datos** (DPO):
- Monitorear cumplimiento Ley 21.719
- Asesorar en tratamientos de datos
- Punto de contacto con Agencia
- Capacitar equipo

**Legal Counsel**:
- Actualizar T&C y políticas
- Gestionar reclamos legales
- Relación con abogados de la plataforma

**CISO (Chief Information Security Officer)**:
- Seguridad técnica
- Plan de respuesta a incidentes
- Pentesting y auditorías

### 8.2 Auditorías y Revisiones

**Trimestral**:
- Revisión de accesos a datos
- Verificación de logs de auditoría

**Anual**:
- Auditoría de seguridad externa
- Revisión de T&C y políticas
- Capacitación de equipo en compliance

**Ad-hoc**:
- Ante cambios regulatorios
- Ante incidentes de seguridad

### 8.3 Capacitación

**Todo el Equipo** (anual):
- Protección de datos básica
- Seguridad de la información
- Ética y confidencialidad

**Equipo Técnico** (semestral):
- Secure coding practices
- OWASP Top 10
- Manejo de secretos

**Equipo de Soporte** (trimestral):
- Atención de solicitudes ARCO
- Manejo de información sensible

## 9. Costo Estimado de Compliance

### Setup Inicial (Una vez)
| Item | Costo (CLP) |
|------|-------------|
| Constitución SpA | $500K |
| Registro de marca | $250K |
| Drafting T&C/Políticas | $1M-2M |
| Consultoría legal inicial | $1M |
| **Total** | **$2.75M-3.75M** |

### Recurrente (Anual)
| Item | Costo (CLP/año) |
|------|-----------------|
| Seguros | $10M-15M |
| Legal counsel (part-time) | $12M |
| DPO (part-time inicialmente) | $8M |
| Auditorías seguridad | $5M |
| Software compliance (GRC tools) | $2M |
| Capacitaciones | $1M |
| **Total** | **$38M-43M/año** |

**Como % de Ingresos** (Año 3): ~1.5% (saludable)

---

**Conclusión**: Estrategia de compliance proactiva que balancea cumplimiento riguroso con velocidad de ejecución. Prioriza protección de datos y claridad en relación con abogados.
