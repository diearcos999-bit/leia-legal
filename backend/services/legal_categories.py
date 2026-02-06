"""
Categorías legales para LEIA.
Define las áreas de práctica, subcategorías y criterios de derivación.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class LegalCategory(str, Enum):
    """Categorías principales de práctica legal."""
    LABORAL = "laboral"
    FAMILIA = "familia"
    CIVIL = "civil"
    ARRIENDOS = "arriendos"
    DEUDAS = "deudas"
    CONSUMIDOR = "consumidor"
    PENAL = "penal"
    MIGRACION = "migracion"
    ADMINISTRATIVO = "administrativo"
    TRIBUTARIO = "tributario"
    SOCIETARIO = "societario"
    PROPIEDAD_INTELECTUAL = "propiedad_intelectual"
    NOTARIAL = "notarial"
    SUCESIONES = "sucesiones"
    BANCARIO = "bancario"
    SEGUROS = "seguros"


@dataclass
class CategoryInfo:
    """Información completa de una categoría legal."""
    id: str
    name: str
    description: str
    icon: str
    subcategories: List[str]
    referral_triggers: List[str]  # Cuándo derivar a abogado
    keywords: List[str]  # Palabras clave para detección


# Definición completa de categorías
LEGAL_CATEGORIES: Dict[str, CategoryInfo] = {
    "laboral": CategoryInfo(
        id="laboral",
        name="Laboral",
        description="Conflictos entre trabajadores y empleadores",
        icon="Briefcase",
        subcategories=[
            "Despido",
            "Finiquito",
            "Autodespido",
            "Nulidad del despido",
            "Tutela laboral",
            "Accidentes del trabajo",
            "Licencias médicas",
            "Remuneraciones y horas extra"
        ],
        referral_triggers=[
            "Carta de despido recibida",
            "Cálculo de finiquito disputado",
            "Plazos legales corriendo",
            "Citación a comparendo",
            "Demanda o mediación en curso"
        ],
        keywords=[
            "despido", "finiquito", "trabajo", "empleador", "sueldo",
            "contrato laboral", "horas extra", "vacaciones", "licencia",
            "accidente laboral", "indemnización", "tutela", "autodespido"
        ]
    ),

    "familia": CategoryInfo(
        id="familia",
        name="Familia",
        description="Asuntos familiares y de menores",
        icon="Users",
        subcategories=[
            "Pensión de alimentos",
            "Relación directa y regular",
            "Cuidado personal",
            "Divorcio",
            "Compensación económica",
            "Violencia intrafamiliar",
            "Adopción"
        ],
        referral_triggers=[
            "Medidas cautelares vigentes",
            "Violencia intrafamiliar (VIF)",
            "Niños involucrados",
            "Audiencia programada",
            "Incumplimiento reiterado de pensión"
        ],
        keywords=[
            "divorcio", "pensión", "alimentos", "custodia", "visitas",
            "hijo", "hija", "matrimonio", "separación", "violencia",
            "VIF", "familia", "cuidado personal", "régimen"
        ]
    ),

    "civil": CategoryInfo(
        id="civil",
        name="Civil y Contratos",
        description="Contratos, responsabilidad civil e indemnizaciones",
        icon="FileText",
        subcategories=[
            "Incumplimiento contractual",
            "Indemnización de perjuicios",
            "Cobro de pesos",
            "Responsabilidad civil",
            "Promesas y compraventas",
            "Servicios"
        ],
        referral_triggers=[
            "Montos altos en disputa",
            "Contrato complejo",
            "Amenaza de demanda",
            "Necesidad de negociar formalmente"
        ],
        keywords=[
            "contrato", "incumplimiento", "indemnización", "daños",
            "perjuicios", "cobro", "deuda", "promesa", "compraventa",
            "responsabilidad", "reparación"
        ]
    ),

    "arriendos": CategoryInfo(
        id="arriendos",
        name="Arriendos e Inmobiliario",
        description="Contratos de arriendo y propiedad inmueble",
        icon="Home",
        subcategories=[
            "Término de arriendo",
            "Desahucio",
            "No pago de arriendo",
            "Garantía y mes de garantía",
            "Daños a la propiedad",
            "Copropiedad y administración",
            "Compraventa de inmuebles"
        ],
        referral_triggers=[
            "Desalojo en curso",
            "Juicio monitorio o ejecutivo",
            "Notificación judicial recibida",
            "Conflicto con administración de edificio"
        ],
        keywords=[
            "arriendo", "arrendador", "arrendatario", "desahucio",
            "garantía", "departamento", "casa", "inmueble", "propiedad",
            "condominio", "gastos comunes", "corredora"
        ]
    ),

    "deudas": CategoryInfo(
        id="deudas",
        name="Deudas y Cobranza",
        description="Cobranzas, embargos y juicios ejecutivos",
        icon="CreditCard",
        subcategories=[
            "Pagaré, letra y cheque",
            "Embargo",
            "Prescripción de deudas",
            "Repactaciones",
            "Cobranza extrajudicial",
            "DICOM y boletín comercial"
        ],
        referral_triggers=[
            "Notificación judicial recibida",
            "Embargo o retención de bienes",
            "Demanda ejecutiva",
            "Documentos firmados (pagaré, letra)"
        ],
        keywords=[
            "deuda", "cobro", "pagaré", "cheque", "embargo", "DICOM",
            "cobranza", "prescripción", "ejecutivo", "retención",
            "repactación", "morosidad"
        ]
    ),

    "consumidor": CategoryInfo(
        id="consumidor",
        name="Consumidor y SERNAC",
        description="Derechos del consumidor y reclamos comerciales",
        icon="ShoppingBag",
        subcategories=[
            "Garantía legal",
            "Derecho a retracto",
            "Incumplimiento de compra o servicio",
            "Estafas comerciales",
            "Pasajes y viajes",
            "Telecomunicaciones",
            "Reclamos SERNAC"
        ],
        referral_triggers=[
            "Necesidad de demanda en JPL",
            "Montos relevantes",
            "Proveedor no responde",
            "Casos repetidos o sistemáticos"
        ],
        keywords=[
            "SERNAC", "garantía", "devolución", "producto", "servicio",
            "reclamo", "consumidor", "tienda", "compra", "retracto",
            "telecomunicaciones", "aerolínea", "viaje"
        ]
    ),

    "penal": CategoryInfo(
        id="penal",
        name="Penal",
        description="Delitos, denuncias y defensa penal",
        icon="Shield",
        subcategories=[
            "Denuncias",
            "Querellas",
            "Citaciones",
            "Medidas cautelares",
            "Delitos económicos simples"
        ],
        referral_triggers=[
            "Citación a declarar",
            "Detención previa",
            "Amenazas recibidas",
            "Violencia intrafamiliar",
            "Riesgo inmediato"
        ],
        keywords=[
            "denuncia", "querella", "delito", "robo", "estafa", "amenaza",
            "fiscalía", "carabineros", "PDI", "detención", "imputado",
            "víctima", "penal"
        ]
    ),

    "migracion": CategoryInfo(
        id="migracion",
        name="Migración y Extranjería",
        description="Visas, permisos y trámites migratorios",
        icon="Globe",
        subcategories=[
            "Visas",
            "Prórrogas",
            "Permanencia definitiva",
            "Rechazos migratorios",
            "Recursos administrativos y judiciales"
        ],
        referral_triggers=[
            "Rechazo de visa o solicitud",
            "Plazos para recurso",
            "Orden de abandono del país",
            "Causal migratoria compleja"
        ],
        keywords=[
            "visa", "extranjería", "migración", "permanencia", "prórroga",
            "rechazo", "deportación", "residencia", "PDI", "extranjero"
        ]
    ),

    "administrativo": CategoryInfo(
        id="administrativo",
        name="Administrativo y Estado",
        description="Trámites con el Estado y municipalidades",
        icon="Building",
        subcategories=[
            "Municipalidades",
            "Sumarios administrativos",
            "Permisos",
            "Sanciones",
            "Reclamos ante servicios públicos",
            "Recursos administrativos"
        ],
        referral_triggers=[
            "Acto administrativo notificado",
            "Multas altas",
            "Plazos de reposición o jerárquico"
        ],
        keywords=[
            "municipalidad", "sumario", "permiso", "sanción", "multa",
            "servicio público", "funcionario", "reposición", "jerárquico",
            "contraloría"
        ]
    ),

    "tributario": CategoryInfo(
        id="tributario",
        name="Tributario",
        description="Impuestos, SII y fiscalizaciones",
        icon="Calculator",
        subcategories=[
            "SII y fiscalizaciones",
            "RAV (Revisión de Actuación Fiscalizadora)",
            "Reposición administrativa",
            "Reclamación en TTA",
            "Multas tributarias",
            "IVA y boletas"
        ],
        referral_triggers=[
            "Citación del SII",
            "Liquidación o giro emitido",
            "Plazos tributarios corriendo",
            "Necesidad de defensa formal"
        ],
        keywords=[
            "SII", "impuesto", "tributario", "IVA", "boleta", "factura",
            "fiscalización", "liquidación", "giro", "TTA", "renta"
        ]
    ),

    "societario": CategoryInfo(
        id="societario",
        name="Societario y Emprendimiento",
        description="Sociedades, contratos comerciales y startups",
        icon="Users",
        subcategories=[
            "Constitución de sociedades",
            "Pactos de socios",
            "Contratos comerciales",
            "Términos y condiciones",
            "Políticas de privacidad",
            "Marcas (básico)"
        ],
        referral_triggers=[
            "Inversión en juego",
            "Conflicto entre socios",
            "Contrato relevante",
            "Riesgo reputacional"
        ],
        keywords=[
            "sociedad", "empresa", "socio", "SPA", "SpA", "LTDA", "startup",
            "emprendimiento", "contrato comercial", "términos", "privacidad"
        ]
    ),

    "propiedad_intelectual": CategoryInfo(
        id="propiedad_intelectual",
        name="Propiedad Intelectual",
        description="Marcas, patentes y derechos de autor",
        icon="Lightbulb",
        subcategories=[
            "Registro de marca",
            "Oposición a marca",
            "Infracciones",
            "Uso indebido",
            "Licencias"
        ],
        referral_triggers=[
            "Oposición o demanda recibida",
            "Uso no autorizado de marca",
            "Negociación con terceros"
        ],
        keywords=[
            "marca", "patente", "INAPI", "propiedad intelectual", "copyright",
            "derechos de autor", "registro", "oposición", "licencia"
        ]
    ),

    "notarial": CategoryInfo(
        id="notarial",
        name="Notarial y Trámites",
        description="Escrituras, poderes y trámites notariales",
        icon="Stamp",
        subcategories=[
            "Escrituras simples",
            "Poderes",
            "Autorizaciones",
            "Herencias simples",
            "Posesión efectiva"
        ],
        referral_triggers=[
            "Necesita paso a paso con documentos",
            "Trámite complejo o urgente"
        ],
        keywords=[
            "notaría", "escritura", "poder", "autorización", "certificado",
            "legalización", "apostilla", "trámite"
        ]
    ),

    "sucesiones": CategoryInfo(
        id="sucesiones",
        name="Sucesiones y Herencias",
        description="Herencias, testamentos y partición de bienes",
        icon="Scroll",
        subcategories=[
            "Posesión efectiva",
            "Partición de bienes",
            "Testamentos",
            "Deudas hereditarias"
        ],
        referral_triggers=[
            "Bienes relevantes en juego",
            "Conflicto familiar",
            "Herencia con deudas"
        ],
        keywords=[
            "herencia", "testamento", "posesión efectiva", "heredero",
            "sucesión", "partición", "fallecido", "bienes"
        ]
    ),

    "bancario": CategoryInfo(
        id="bancario",
        name="Bancario y Financiero",
        description="Créditos, bancos y productos financieros",
        icon="Landmark",
        subcategories=[
            "Créditos",
            "Cláusulas abusivas",
            "Renegociación de deudas",
            "Fraudes bancarios",
            "Seguros asociados"
        ],
        referral_triggers=[
            "Fraude con montos altos",
            "Cobranza judicial",
            "Contrato bancario complejo"
        ],
        keywords=[
            "banco", "crédito", "préstamo", "hipoteca", "tarjeta", "fraude",
            "clonación", "transferencia", "cuenta", "financiero"
        ]
    ),

    "seguros": CategoryInfo(
        id="seguros",
        name="Seguros",
        description="Pólizas, siniestros y coberturas",
        icon="Umbrella",
        subcategories=[
            "Rechazo de cobertura",
            "Siniestros",
            "Seguros de auto",
            "Seguros de salud",
            "Seguros de vida"
        ],
        referral_triggers=[
            "Aseguradora rechaza formalmente",
            "Disputa de peritaje"
        ],
        keywords=[
            "seguro", "póliza", "siniestro", "cobertura", "aseguradora",
            "indemnización", "peritaje", "ISAPRE", "salud"
        ]
    )
}


def get_category(category_id: str) -> Optional[CategoryInfo]:
    """Obtiene información de una categoría por su ID."""
    return LEGAL_CATEGORIES.get(category_id)


def get_all_categories() -> List[Dict]:
    """Retorna todas las categorías en formato para API."""
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "icon": cat.icon,
            "subcategories": cat.subcategories
        }
        for cat in LEGAL_CATEGORIES.values()
    ]


def get_category_by_keyword(text: str) -> Optional[str]:
    """
    Detecta la categoría más probable basándose en palabras clave.
    Retorna el ID de la categoría o None.
    """
    text_lower = text.lower()
    best_match = None
    best_score = 0

    for cat_id, cat_info in LEGAL_CATEGORIES.items():
        score = sum(1 for kw in cat_info.keywords if kw in text_lower)
        if score > best_score:
            best_score = score
            best_match = cat_id

    return best_match if best_score > 0 else None


def should_refer_to_lawyer(category_id: str, context: str) -> bool:
    """
    Determina si se debe derivar a un abogado basándose en triggers.
    """
    category = get_category(category_id)
    if not category:
        return False

    context_lower = context.lower()

    # Palabras de urgencia general
    urgency_words = [
        "citación", "notificación", "demanda", "audiencia", "plazo",
        "urgente", "mañana", "hoy", "embargo", "detención"
    ]

    if any(word in context_lower for word in urgency_words):
        return True

    return False


# Lista de especialidades válidas (para validación en BD)
VALID_SPECIALTIES = [cat.name for cat in LEGAL_CATEGORIES.values()]

# Mapeo de nombres alternativos a IDs de categoría
SPECIALTY_ALIASES = {
    "Derecho Laboral": "laboral",
    "Derecho de Familia": "familia",
    "Derecho Civil": "civil",
    "Derecho Penal": "penal",
    "Derecho Tributario": "tributario",
    "Derecho Migratorio": "migracion",
    "Derecho Inmobiliario": "arriendos",
    "Cobranza": "deudas",
    "Derecho del Consumidor": "consumidor",
    "Derecho Comercial": "societario",
    "Marcas y Patentes": "propiedad_intelectual",
}
