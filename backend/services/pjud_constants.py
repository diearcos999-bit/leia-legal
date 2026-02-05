"""
Constantes y códigos del Poder Judicial de Chile.
Basado en la documentación oficial de APIs de Estadísticas del PJUD.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


# ==================== CORTES DE APELACIONES ====================

CORTES_APELACIONES: Dict[int, str] = {
    0: "Todo el País",
    10: "Corte de Apelaciones de Arica",
    11: "Corte de Apelaciones de Iquique",
    15: "Corte de Apelaciones de Antofagasta",
    20: "Corte de Apelaciones de Copiapó",
    25: "Corte de Apelaciones de La Serena",
    30: "Corte de Apelaciones de Valparaíso",
    35: "Corte de Apelaciones de Rancagua",
    40: "Corte de Apelaciones de Talca",
    45: "Corte de Apelaciones de Chillán",
    46: "Corte de Apelaciones de Concepción",
    50: "Corte de Apelaciones de Temuco",
    55: "Corte de Apelaciones de Valdivia",
    56: "Corte de Apelaciones de Puerto Montt",
    60: "Corte de Apelaciones de Coyhaique",
    61: "Corte de Apelaciones de Punta Arenas",
    90: "Corte de Apelaciones de Santiago",
    91: "Corte de Apelaciones de San Miguel",
}

# Mapeo inverso: nombre corto -> código
CORTES_POR_NOMBRE: Dict[str, int] = {
    "arica": 10,
    "iquique": 11,
    "antofagasta": 15,
    "copiapo": 20,
    "copiapó": 20,
    "la serena": 25,
    "serena": 25,
    "valparaiso": 30,
    "valparaíso": 30,
    "rancagua": 35,
    "talca": 40,
    "chillan": 45,
    "chillán": 45,
    "concepcion": 46,
    "concepción": 46,
    "temuco": 50,
    "valdivia": 55,
    "puerto montt": 56,
    "coyhaique": 60,
    "punta arenas": 61,
    "santiago": 90,
    "san miguel": 91,
}


# ==================== COMPETENCIAS ====================

COMPETENCIAS = {
    "Civil": "Civil",
    "Cobranza": "Cobranza",
    "Familia": "Familia",
    "Laboral": "Laboral",
    "Penal": "Penal",
    "Garantia": "Garantía",
    "Top": "Tribunal Oral en lo Penal",
}


# ==================== TRIBUNALES POR COMPETENCIA ====================

# Tribunales Civiles
TRIBUNALES_CIVIL: Dict[int, str] = {
    988: "1° Juzgado Civil de Santiago",
    989: "2° Juzgado Civil de Santiago",
    990: "3° Juzgado Civil de Santiago",
    991: "4° Juzgado Civil de Santiago",
    992: "5° Juzgado Civil de Santiago",
    993: "6° Juzgado Civil de Santiago",
    994: "7° Juzgado Civil de Santiago",
    995: "8° Juzgado Civil de Santiago",
    996: "9° Juzgado Civil de Santiago",
    997: "10° Juzgado Civil de Santiago",
    998: "11° Juzgado Civil de Santiago",
    999: "12° Juzgado Civil de Santiago",
    1000: "13° Juzgado Civil de Santiago",
    1001: "14° Juzgado Civil de Santiago",
    1002: "15° Juzgado Civil de Santiago",
    1003: "16° Juzgado Civil de Santiago",
    1004: "17° Juzgado Civil de Santiago",
    1005: "18° Juzgado Civil de Santiago",
    1006: "19° Juzgado Civil de Santiago",
    1007: "20° Juzgado Civil de Santiago",
    1008: "21° Juzgado Civil de Santiago",
    1009: "22° Juzgado Civil de Santiago",
    1010: "23° Juzgado Civil de Santiago",
    1011: "24° Juzgado Civil de Santiago",
    1012: "25° Juzgado Civil de Santiago",
    1013: "26° Juzgado Civil de Santiago",
    1014: "27° Juzgado Civil de Santiago",
    1015: "28° Juzgado Civil de Santiago",
    1016: "29° Juzgado Civil de Santiago",
    1017: "30° Juzgado Civil de Santiago",
    # Otros tribunales civiles principales
    1018: "1° Juzgado Civil de Valparaíso",
    1019: "2° Juzgado Civil de Valparaíso",
    1020: "3° Juzgado Civil de Valparaíso",
    1021: "4° Juzgado Civil de Valparaíso",
    1022: "1° Juzgado Civil de Concepción",
    1023: "2° Juzgado Civil de Concepción",
    1024: "3° Juzgado Civil de Concepción",
}

# Tribunales de Cobranza
TRIBUNALES_COBRANZA: Dict[int, str] = {
    1070: "1° Juzgado de Cobranza Laboral y Previsional de Santiago",
    1071: "2° Juzgado de Cobranza Laboral y Previsional de Santiago",
    1072: "3° Juzgado de Cobranza Laboral y Previsional de Santiago",
    1073: "4° Juzgado de Cobranza Laboral y Previsional de Santiago",
}

# Tribunales de Familia
TRIBUNALES_FAMILIA: Dict[int, str] = {
    1100: "1° Juzgado de Familia de Santiago",
    1101: "2° Juzgado de Familia de Santiago",
    1102: "3° Juzgado de Familia de Santiago",
    1103: "4° Juzgado de Familia de Santiago",
    1104: "Juzgado de Familia de Pudahuel",
    1105: "Juzgado de Familia de Puente Alto",
    1106: "Juzgado de Familia de Colina",
    1107: "Juzgado de Familia de Maipú",
    1108: "Juzgado de Familia de San Bernardo",
    1109: "Juzgado de Familia de Peñalolén",
    1110: "Juzgado de Familia de Valparaíso",
    1111: "Juzgado de Familia de Viña del Mar",
    1112: "Juzgado de Familia de Concepción",
}

# Tribunales Laborales
TRIBUNALES_LABORAL: Dict[int, str] = {
    1200: "1° Juzgado de Letras del Trabajo de Santiago",
    1201: "2° Juzgado de Letras del Trabajo de Santiago",
    1202: "Juzgado de Letras del Trabajo de Valparaíso",
    1203: "Juzgado de Letras del Trabajo de Viña del Mar",
    1204: "Juzgado de Letras del Trabajo de Concepción",
    1205: "Juzgado de Letras del Trabajo de Temuco",
    1206: "Juzgado de Letras del Trabajo de Puerto Montt",
    1207: "Juzgado de Letras del Trabajo de Antofagasta",
    1208: "Juzgado de Letras del Trabajo de Iquique",
    1209: "Juzgado de Letras del Trabajo de La Serena",
    1210: "Juzgado de Letras del Trabajo de Rancagua",
    1211: "Juzgado de Letras del Trabajo de Talca",
}

# Juzgados de Garantía
TRIBUNALES_GARANTIA: Dict[int, str] = {
    1300: "1° Juzgado de Garantía de Santiago",
    1301: "2° Juzgado de Garantía de Santiago",
    1302: "3° Juzgado de Garantía de Santiago",
    1303: "4° Juzgado de Garantía de Santiago",
    1304: "5° Juzgado de Garantía de Santiago",
    1305: "6° Juzgado de Garantía de Santiago",
    1306: "7° Juzgado de Garantía de Santiago",
    1307: "8° Juzgado de Garantía de Santiago",
    1308: "9° Juzgado de Garantía de Santiago",
    1309: "10° Juzgado de Garantía de Santiago",
    1310: "11° Juzgado de Garantía de Santiago",
    1311: "12° Juzgado de Garantía de Santiago",
    1312: "13° Juzgado de Garantía de Santiago",
    1313: "14° Juzgado de Garantía de Santiago",
    1314: "15° Juzgado de Garantía de Santiago",
    1315: "Juzgado de Garantía de Puente Alto",
    1316: "Juzgado de Garantía de San Bernardo",
    1317: "Juzgado de Garantía de Colina",
    1318: "Juzgado de Garantía de Valparaíso",
    1319: "Juzgado de Garantía de Viña del Mar",
    1320: "Juzgado de Garantía de Concepción",
}

# Tribunales Orales en lo Penal
TRIBUNALES_TOP: Dict[int, str] = {
    1400: "1° Tribunal Oral en lo Penal de Santiago",
    1401: "2° Tribunal Oral en lo Penal de Santiago",
    1402: "3° Tribunal Oral en lo Penal de Santiago",
    1403: "4° Tribunal Oral en lo Penal de Santiago",
    1404: "5° Tribunal Oral en lo Penal de Santiago",
    1405: "6° Tribunal Oral en lo Penal de Santiago",
    1406: "7° Tribunal Oral en lo Penal de Santiago",
    1407: "Tribunal Oral en lo Penal de Puente Alto",
    1408: "Tribunal Oral en lo Penal de San Bernardo",
    1409: "Tribunal Oral en lo Penal de Valparaíso",
    1410: "Tribunal Oral en lo Penal de Viña del Mar",
    1411: "Tribunal Oral en lo Penal de Concepción",
}

# Diccionario consolidado de todos los tribunales
TODOS_TRIBUNALES: Dict[int, str] = {
    **TRIBUNALES_CIVIL,
    **TRIBUNALES_COBRANZA,
    **TRIBUNALES_FAMILIA,
    **TRIBUNALES_LABORAL,
    **TRIBUNALES_GARANTIA,
    **TRIBUNALES_TOP,
}


# ==================== FUNCIONES AUXILIARES ====================

def get_corte_nombre(codigo: int) -> str:
    """Obtiene el nombre de una Corte de Apelaciones por su código."""
    return CORTES_APELACIONES.get(codigo, f"Corte desconocida ({codigo})")


def get_tribunal_nombre(codigo: int) -> str:
    """Obtiene el nombre de un tribunal por su código."""
    return TODOS_TRIBUNALES.get(codigo, f"Tribunal desconocido ({codigo})")


def get_corte_codigo(nombre: str) -> Optional[int]:
    """Obtiene el código de una Corte de Apelaciones por su nombre."""
    nombre_lower = nombre.lower().strip()
    return CORTES_POR_NOMBRE.get(nombre_lower)


def detectar_competencia(texto: str) -> Optional[str]:
    """
    Detecta la competencia basándose en texto (RIT, nombre de tribunal, etc.).
    """
    texto_lower = texto.lower()

    if any(x in texto_lower for x in ["civil", "c-"]):
        return "Civil"
    elif any(x in texto_lower for x in ["cobranza", "cobro"]):
        return "Cobranza"
    elif any(x in texto_lower for x in ["familia", "f-", "alimentos", "visitas", "cuidado personal"]):
        return "Familia"
    elif any(x in texto_lower for x in ["laboral", "trabajo", "t-", "despido"]):
        return "Laboral"
    elif any(x in texto_lower for x in ["garantía", "garantia", "g-", "rpa", "rit"]):
        return "Garantia"
    elif any(x in texto_lower for x in ["oral penal", "top", "o-"]):
        return "Top"
    elif any(x in texto_lower for x in ["penal"]):
        return "Penal"

    return None


def extraer_info_rit(rit: str) -> Dict[str, Optional[str]]:
    """
    Extrae información del RIT (Rol Interno del Tribunal).
    Formato típico: C-1234-2024 (Tipo-Número-Año)
    """
    import re

    match = re.match(r'^([A-Z])-(\d+)-(\d{4})$', rit.upper().strip())

    if not match:
        return {"tipo": None, "numero": None, "año": None, "competencia": None}

    tipo, numero, año = match.groups()

    # Mapeo de letras a competencias
    tipo_competencia = {
        "C": "Civil",
        "T": "Laboral",
        "F": "Familia",
        "O": "Tribunal Oral Penal",
        "G": "Garantía",
        "P": "Penal",
        "V": "Violencia Intrafamiliar",
        "M": "Medidas de Protección",
    }

    return {
        "tipo": tipo,
        "numero": numero,
        "año": año,
        "competencia": tipo_competencia.get(tipo, "Desconocida"),
    }


# ==================== TIPOS DE CAUSAS ====================

TIPOS_CAUSA = {
    "C": "Causa Civil",
    "T": "Causa Laboral",
    "F": "Causa de Familia",
    "O": "Causa Tribunal Oral Penal",
    "G": "Causa de Garantía",
    "P": "Causa Penal",
    "V": "Violencia Intrafamiliar",
    "M": "Medidas de Protección",
    "E": "Causa Ejecutiva",
    "A": "Recurso de Apelación",
    "R": "Recurso",
}


# ==================== ESTADOS DE CAUSA ====================

ESTADOS_CAUSA = [
    "En Tramitación",
    "Con Sentencia",
    "Terminada",
    "En Acuerdo",
    "Archivada",
    "Suspendida",
    "Paralizada",
]


# ==================== MATERIAS COMUNES ====================

MATERIAS_COMUNES = {
    "civil": [
        "Cobro de Pesos",
        "Indemnización de Perjuicios",
        "Cumplimiento de Contrato",
        "Arrendamiento",
        "Reivindicación",
        "Precario",
        "Servidumbre",
        "Tercería",
        "Juicio Ejecutivo",
        "Gestión Preparatoria",
    ],
    "familia": [
        "Alimentos Mayores",
        "Alimentos Menores",
        "Cuidado Personal",
        "Relación Directa y Regular",
        "Divorcio",
        "Adopción",
        "Violencia Intrafamiliar",
        "Medidas de Protección",
        "Autorización Salida del País",
        "Filiación",
    ],
    "laboral": [
        "Despido Injustificado",
        "Cobro de Prestaciones",
        "Accidente del Trabajo",
        "Enfermedad Profesional",
        "Tutela Laboral",
        "Práctica Antisindical",
        "Nulidad de Despido",
        "Declarativa de Relación Laboral",
    ],
    "penal": [
        "Robo",
        "Hurto",
        "Estafa",
        "Lesiones",
        "Amenazas",
        "Tráfico de Drogas",
        "Homicidio",
        "Delitos Sexuales",
        "Violencia Intrafamiliar",
        "Cuasidelito",
    ],
}
