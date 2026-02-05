"""
Herramientas legales para los agentes de LEIA.

Proporciona acceso al glosario legal chileno, siglas,
frases latinas y funciones de búsqueda de términos.
"""

from typing import List, Dict, Any, Optional

from langchain_core.tools import tool

# Importar el glosario legal existente
from services.glosario_legal import (
    buscar_termino,
    buscar_sigla as _buscar_sigla,
    buscar_frase_latina,
    buscar_en_todo,
    buscar_terminos_por_categoria,
    obtener_todas_categorias,
    explicar_para_usuario,
    obtener_estadisticas_glosario,
    GLOSARIO,
    SIGLAS,
    FRASES_LATINAS,
)


@tool
def glosario_lookup(termino: str) -> Dict[str, Any]:
    """
    Busca la definición de un término legal en el glosario de LEIA.

    Esta herramienta consulta el glosario legal chileno para encontrar
    definiciones, sinónimos y explicaciones de términos jurídicos.
    Útil cuando el usuario pregunta "¿Qué significa X?" o usa
    terminología legal que necesita explicación.

    Args:
        termino: El término legal a buscar (ej: "sentencia ejecutoriada",
                 "cuidado personal", "despido injustificado")

    Returns:
        Dict con la definición, categoría, sinónimos y ejemplos del término
    """
    resultado = buscar_en_todo(termino)

    if not resultado["encontrado"]:
        # Intentar búsqueda parcial
        termino_lower = termino.lower()
        posibles = []
        for key, term in GLOSARIO.items():
            if termino_lower in key or termino_lower in term.termino.lower():
                posibles.append({
                    "termino": term.termino,
                    "categoria": term.categoria,
                })
            elif term.sinonimos:
                for sin in term.sinonimos:
                    if termino_lower in sin.lower():
                        posibles.append({
                            "termino": term.termino,
                            "categoria": term.categoria,
                        })
                        break

        return {
            "encontrado": False,
            "termino_buscado": termino,
            "mensaje": f"No encontré el término '{termino}' exactamente en el glosario.",
            "sugerencias": posibles[:5] if posibles else [],
        }

    # Preparar respuesta según el tipo
    response = {
        "encontrado": True,
        "termino_buscado": termino,
        "tipo": resultado["tipo"],
        "definicion": resultado["definicion"],
    }

    if resultado["tipo"] == "termino" and resultado.get("termino_completo"):
        term_obj = resultado["termino_completo"]
        response["termino_formal"] = term_obj.termino
        response["categoria"] = term_obj.categoria
        response["sinonimos"] = term_obj.sinonimos or []
        response["ejemplos"] = term_obj.ejemplos or []

    elif resultado["tipo"] == "sigla":
        response["sigla"] = termino.upper()

    elif resultado["tipo"] == "frase_latina":
        response["frase"] = termino.lower()

    # Agregar explicación amigable
    response["explicacion_usuario"] = explicar_para_usuario(termino)

    return response


@tool
def buscar_sigla(sigla: str) -> Dict[str, Any]:
    """
    Busca el significado de una sigla legal chilena.

    Útil para explicar abreviaturas como RIT, RUC, ROL, VIF, etc.

    Args:
        sigla: La sigla a buscar (ej: "RIT", "RUC", "VIF")

    Returns:
        Dict con el significado de la sigla
    """
    significado = _buscar_sigla(sigla)

    if not significado:
        # Buscar siglas similares
        sigla_upper = sigla.upper()
        similares = [s for s in SIGLAS.keys() if sigla_upper in s or s in sigla_upper]

        return {
            "encontrado": False,
            "sigla": sigla.upper(),
            "mensaje": f"No encontré la sigla '{sigla.upper()}' en el glosario.",
            "siglas_disponibles": similares[:5] if similares else list(SIGLAS.keys())[:10],
        }

    return {
        "encontrado": True,
        "sigla": sigla.upper(),
        "significado": significado,
    }


@tool
def buscar_categoria(categoria: str) -> Dict[str, Any]:
    """
    Lista todos los términos legales de una categoría específica.

    Útil para explorar términos relacionados a un área del derecho.

    Args:
        categoria: La categoría a buscar (ej: "Familia", "Laboral", "Penal", "Civil")

    Returns:
        Dict con la lista de términos de esa categoría
    """
    terminos = buscar_terminos_por_categoria(categoria)

    if not terminos:
        categorias_disponibles = obtener_todas_categorias()
        return {
            "encontrado": False,
            "categoria": categoria,
            "mensaje": f"No encontré términos en la categoría '{categoria}'.",
            "categorias_disponibles": categorias_disponibles,
        }

    return {
        "encontrado": True,
        "categoria": categoria,
        "total_terminos": len(terminos),
        "terminos": [
            {
                "termino": t.termino,
                "definicion_corta": t.definicion[:150] + "..." if len(t.definicion) > 150 else t.definicion,
            }
            for t in terminos
        ],
    }


@tool
def obtener_categorias_legales() -> Dict[str, Any]:
    """
    Lista todas las categorías disponibles en el glosario legal.

    Útil para saber qué áreas del derecho están cubiertas.

    Returns:
        Dict con la lista de categorías y estadísticas
    """
    categorias = obtener_todas_categorias()
    stats = obtener_estadisticas_glosario()

    return {
        "categorias": categorias,
        "estadisticas": stats,
    }


@tool
def buscar_frase_legal(frase: str) -> Dict[str, Any]:
    """
    Busca el significado de una frase o expresión latina legal.

    Útil para explicar términos como "habeas corpus", "in dubio pro reo", etc.

    Args:
        frase: La frase latina a buscar

    Returns:
        Dict con el significado de la frase
    """
    significado = buscar_frase_latina(frase)

    if not significado:
        frases_similares = [f for f in FRASES_LATINAS.keys() if frase.lower() in f]

        return {
            "encontrado": False,
            "frase": frase,
            "mensaje": f"No encontré la frase '{frase}' en el glosario de expresiones latinas.",
            "frases_disponibles": frases_similares if frases_similares else list(FRASES_LATINAS.keys())[:10],
        }

    return {
        "encontrado": True,
        "frase": frase.lower(),
        "significado": significado,
    }


def get_legal_tools() -> List:
    """
    Retorna todas las herramientas legales para usar con LangGraph.

    Returns:
        Lista de herramientas legales
    """
    return [
        glosario_lookup,
        buscar_sigla,
        buscar_categoria,
        obtener_categorias_legales,
        buscar_frase_legal,
    ]


def explain_legal_term(termino: str) -> str:
    """
    Función auxiliar para obtener una explicación amigable de un término.

    Args:
        termino: Término a explicar

    Returns:
        Explicación en lenguaje sencillo
    """
    return explicar_para_usuario(termino)
