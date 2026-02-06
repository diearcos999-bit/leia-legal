"""
Feriados de Chile - Módulo para cálculo de plazos legales

Este módulo contiene los feriados legales de Chile según la Ley 2.977 y modificaciones.
Incluye feriados fijos y móviles calculados dinámicamente.
"""

from datetime import date, timedelta
from typing import List, Set

# Feriados FIJOS (misma fecha cada año)
FERIADOS_FIJOS = [
    (1, 1),    # Año Nuevo
    (5, 1),    # Día del Trabajo
    (5, 21),   # Día de las Glorias Navales
    (6, 20),   # Día Nacional de los Pueblos Indígenas (desde 2021)
    (6, 29),   # San Pedro y San Pablo (puede moverse)
    (7, 16),   # Día de la Virgen del Carmen
    (8, 15),   # Asunción de la Virgen
    (9, 18),   # Independencia Nacional
    (9, 19),   # Día de las Glorias del Ejército
    (10, 12),  # Encuentro de Dos Mundos (puede moverse)
    (10, 31),  # Día de las Iglesias Evangélicas y Protestantes
    (11, 1),   # Día de Todos los Santos
    (12, 8),   # Inmaculada Concepción
    (12, 25),  # Navidad
]

# Feriados que se mueven al lunes si caen entre martes y viernes
FERIADOS_MOVILES_LUNES = [
    (6, 29),   # San Pedro y San Pablo
    (10, 12),  # Encuentro de Dos Mundos
]


def calcular_pascua(year: int) -> date:
    """
    Calcula la fecha de Pascua de Resurrección usando el algoritmo de Gauss.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def mover_a_lunes(fecha: date) -> date:
    """
    Si la fecha cae entre martes y viernes, la mueve al lunes anterior.
    """
    dia_semana = fecha.weekday()  # 0=lunes, 1=martes, ... 6=domingo
    if 1 <= dia_semana <= 4:  # Martes a viernes
        return fecha - timedelta(days=dia_semana)  # Mover al lunes
    return fecha


def obtener_feriados_año(year: int) -> Set[date]:
    """
    Obtiene todos los feriados de un año específico.

    Retorna un set de fechas para búsqueda eficiente.
    """
    feriados = set()

    # 1. Agregar feriados fijos
    for mes, dia in FERIADOS_FIJOS:
        fecha = date(year, mes, dia)
        # Verificar si este feriado es móvil
        if (mes, dia) in FERIADOS_MOVILES_LUNES:
            fecha = mover_a_lunes(fecha)
        feriados.add(fecha)

    # 2. Feriados religiosos móviles basados en Pascua
    pascua = calcular_pascua(year)

    # Viernes Santo (2 días antes de Pascua)
    viernes_santo = pascua - timedelta(days=2)
    feriados.add(viernes_santo)

    # Sábado Santo (1 día antes de Pascua)
    sabado_santo = pascua - timedelta(days=1)
    feriados.add(sabado_santo)

    # 3. Feriado especial: si el 18 o 19 de septiembre caen martes o miércoles,
    #    también es feriado el lunes previo
    sep_18 = date(year, 9, 18)
    sep_19 = date(year, 9, 19)

    # Lunes 17 es feriado si el 18 cae martes
    if sep_18.weekday() == 1:  # Martes
        feriados.add(date(year, 9, 17))

    # Viernes 20 es feriado si el 19 cae jueves
    if sep_19.weekday() == 3:  # Jueves
        feriados.add(date(year, 9, 20))

    return feriados


def es_feriado(fecha: date) -> bool:
    """
    Verifica si una fecha específica es feriado en Chile.
    """
    feriados = obtener_feriados_año(fecha.year)
    return fecha in feriados


def es_dia_habil_judicial(fecha: date) -> bool:
    """
    Verifica si una fecha es día hábil JUDICIAL en Chile.

    En materia judicial civil:
    - NO son hábiles: domingos y feriados
    - SÍ son hábiles: lunes a sábado (incluyendo sábado)
    """
    # Domingo = 6 en weekday()
    if fecha.weekday() == 6:
        return False
    if es_feriado(fecha):
        return False
    return True


def calcular_plazo_dias_habiles(
    fecha_inicio: date,
    dias: int,
    tipo: str = "judicial_civil"
) -> dict:
    """
    Calcula el vencimiento de un plazo en días hábiles.

    Args:
        fecha_inicio: Fecha de notificación o inicio del plazo
        dias: Número de días hábiles
        tipo: "judicial_civil" (lunes-sábado sin feriados) o "corridos" (todos los días)

    Returns:
        dict con fecha_vencimiento, dias_contados, detalle

    Nota: El día de inicio NO se cuenta (se excluye).
    """
    fecha_actual = fecha_inicio
    dias_contados = 0
    detalle = []

    while dias_contados < dias:
        fecha_actual = fecha_actual + timedelta(days=1)

        if tipo == "corridos":
            # Días corridos: todos los días cuentan
            dias_contados += 1
            detalle.append({
                "fecha": fecha_actual.isoformat(),
                "dia_numero": dias_contados,
                "es_habil": True
            })
        else:
            # Días hábiles judiciales
            if es_dia_habil_judicial(fecha_actual):
                dias_contados += 1
                detalle.append({
                    "fecha": fecha_actual.isoformat(),
                    "dia_numero": dias_contados,
                    "es_habil": True
                })
            else:
                razon = "domingo" if fecha_actual.weekday() == 6 else "feriado"
                detalle.append({
                    "fecha": fecha_actual.isoformat(),
                    "dia_numero": None,
                    "es_habil": False,
                    "razon": razon
                })

    # Si el último día cae en feriado, se prorroga al siguiente hábil
    while not es_dia_habil_judicial(fecha_actual):
        fecha_actual = fecha_actual + timedelta(days=1)
        detalle.append({
            "fecha": fecha_actual.isoformat(),
            "dia_numero": dias_contados,
            "es_habil": True,
            "prorroga": True
        })

    return {
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_vencimiento": fecha_actual.isoformat(),
        "dias_solicitados": dias,
        "tipo_plazo": tipo,
        "detalle": detalle
    }


def listar_feriados_año(year: int) -> List[dict]:
    """
    Lista todos los feriados de un año con sus nombres.
    """
    nombres_feriados = {
        (1, 1): "Año Nuevo",
        (5, 1): "Día del Trabajo",
        (5, 21): "Día de las Glorias Navales",
        (6, 20): "Día Nacional de los Pueblos Indígenas",
        (6, 29): "San Pedro y San Pablo",
        (7, 16): "Día de la Virgen del Carmen",
        (8, 15): "Asunción de la Virgen",
        (9, 17): "Feriado puente Fiestas Patrias",
        (9, 18): "Independencia Nacional",
        (9, 19): "Día de las Glorias del Ejército",
        (9, 20): "Feriado puente Fiestas Patrias",
        (10, 12): "Encuentro de Dos Mundos",
        (10, 31): "Día de las Iglesias Evangélicas y Protestantes",
        (11, 1): "Día de Todos los Santos",
        (12, 8): "Inmaculada Concepción",
        (12, 25): "Navidad",
    }

    feriados = obtener_feriados_año(year)
    resultado = []

    for f in sorted(feriados):
        nombre = nombres_feriados.get((f.month, f.day), "Feriado religioso")
        if f.month == 3 or f.month == 4:  # Semana Santa
            dia_semana = f.weekday()
            if dia_semana == 4:  # Viernes
                nombre = "Viernes Santo"
            elif dia_semana == 5:  # Sábado
                nombre = "Sábado Santo"

        resultado.append({
            "fecha": f.isoformat(),
            "nombre": nombre,
            "dia_semana": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][f.weekday()]
        })

    return resultado


# Para uso rápido desde el chatbot
def calcular_vencimiento_texto(fecha_inicio_str: str, dias: int, tipo: str = "judicial_civil") -> str:
    """
    Función helper para el chatbot.

    Ejemplo: calcular_vencimiento_texto("2026-02-05", 10, "judicial_civil")
    """
    try:
        partes = fecha_inicio_str.split("-")
        fecha_inicio = date(int(partes[0]), int(partes[1]), int(partes[2]))

        resultado = calcular_plazo_dias_habiles(fecha_inicio, dias, tipo)

        return f"Plazo de {dias} días {tipo}: desde {fecha_inicio_str} vence el {resultado['fecha_vencimiento']}"
    except Exception as e:
        return f"Error calculando plazo: {e}"


if __name__ == "__main__":
    # Test
    print("Feriados 2026:")
    for f in listar_feriados_año(2026):
        print(f"  {f['fecha']} - {f['nombre']} ({f['dia_semana']})")

    print("\nCálculo de plazo:")
    resultado = calcular_plazo_dias_habiles(date(2026, 2, 5), 10, "judicial_civil")
    print(f"  10 días hábiles desde 2026-02-05: vence {resultado['fecha_vencimiento']}")
