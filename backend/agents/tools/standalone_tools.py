"""
Herramientas standalone para testing sin LangChain.

Este módulo proporciona versiones de las herramientas que funcionan
sin necesidad de tener LangChain instalado, útil para testing y desarrollo.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import re
import sys
import os

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Importar glosario legal
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

# Directorio de plantillas
TEMPLATES_DIR = backend_dir / "templates" / "legal"


# ==================== HERRAMIENTAS LEGALES ====================

def glosario_lookup_standalone(termino: str) -> Dict[str, Any]:
    """Versión standalone de glosario_lookup."""
    resultado = buscar_en_todo(termino)

    if not resultado["encontrado"]:
        termino_lower = termino.lower()
        posibles = []
        for key, term in GLOSARIO.items():
            if termino_lower in key or termino_lower in term.termino.lower():
                posibles.append({
                    "termino": term.termino,
                    "categoria": term.categoria,
                })

        return {
            "encontrado": False,
            "termino_buscado": termino,
            "mensaje": f"No encontré el término '{termino}' exactamente en el glosario.",
            "sugerencias": posibles[:5] if posibles else [],
        }

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

    response["explicacion_usuario"] = explicar_para_usuario(termino)
    return response


def buscar_sigla_standalone(sigla: str) -> Dict[str, Any]:
    """Versión standalone de buscar_sigla."""
    significado = _buscar_sigla(sigla)

    if not significado:
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


def buscar_categoria_standalone(categoria: str) -> Dict[str, Any]:
    """Versión standalone de buscar_categoria."""
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


# ==================== HERRAMIENTAS DE DOCUMENTOS ====================

def _format_rut(rut: str) -> str:
    """Formatea un RUT chileno."""
    rut_clean = re.sub(r'[.\-]', '', rut.upper())
    if len(rut_clean) < 2:
        return rut
    body = rut_clean[:-1]
    dv = rut_clean[-1]
    body_formatted = ""
    for i, char in enumerate(reversed(body)):
        if i > 0 and i % 3 == 0:
            body_formatted = "." + body_formatted
        body_formatted = char + body_formatted
    return f"{body_formatted}-{dv}"


def _format_money(amount: int) -> str:
    """Formatea un monto en pesos chilenos."""
    return f"${amount:,.0f}".replace(",", ".")


def _format_date(date_str: str) -> str:
    """Formatea una fecha al formato chileno."""
    try:
        if isinstance(date_str, datetime):
            date_obj = date_str
        else:
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                return date_str

        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return f"{date_obj.day} de {meses[date_obj.month - 1]} de {date_obj.year}"
    except Exception:
        return date_str


def list_templates_standalone() -> Dict[str, Any]:
    """Versión standalone de list_templates."""
    templates = []

    if not TEMPLATES_DIR.exists():
        return {
            "success": True,
            "templates": [],
            "message": "No hay plantillas disponibles.",
        }

    descriptions = {
        "finiquito": "Documento de término de relación laboral",
        "demanda_laboral": "Demanda ante tribunales del trabajo",
        "carta_reclamo": "Carta de reclamo formal ante empresas/SERNAC",
    }

    for template_file in TEMPLATES_DIR.glob("*.jinja2"):
        template_name = template_file.stem
        templates.append({
            "name": template_name,
            "path": str(template_file),
            "description": descriptions.get(template_name, "Documento legal"),
        })

    return {
        "success": True,
        "templates": templates,
        "total": len(templates),
    }


def load_template_standalone(template_name: str) -> Dict[str, Any]:
    """Versión standalone de load_template."""
    template_path = TEMPLATES_DIR / f"{template_name}.jinja2"

    if not template_path.exists():
        available = list_templates_standalone()
        return {
            "success": False,
            "error": f"Plantilla '{template_name}' no encontrada",
            "available_templates": available.get("templates", []),
        }

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        variables = set(re.findall(r'\{\{\s*(\w+)\s*\}\}', template_content))

        fields_map = {
            "finiquito": [
                {"name": "empleador_nombre", "type": "string", "description": "Nombre o razón social del empleador"},
                {"name": "empleador_rut", "type": "rut", "description": "RUT del empleador"},
                {"name": "trabajador_nombre", "type": "string", "description": "Nombre completo del trabajador"},
                {"name": "trabajador_rut", "type": "rut", "description": "RUT del trabajador"},
                {"name": "fecha_inicio", "type": "date", "description": "Fecha de inicio de la relación laboral"},
                {"name": "fecha_termino", "type": "date", "description": "Fecha de término"},
                {"name": "causal_termino", "type": "string", "description": "Causal de término"},
                {"name": "ultimo_sueldo", "type": "money", "description": "Último sueldo bruto mensual"},
            ],
            "carta_reclamo": [
                {"name": "destinatario_nombre", "type": "string", "description": "Nombre de la empresa"},
                {"name": "remitente_nombre", "type": "string", "description": "Nombre del reclamante"},
                {"name": "remitente_rut", "type": "rut", "description": "RUT del reclamante"},
                {"name": "descripcion_problema", "type": "text", "description": "Descripción del problema"},
                {"name": "solucion_solicitada", "type": "text", "description": "Solución que solicita"},
            ],
            "demanda_laboral": [
                {"name": "tribunal", "type": "string", "description": "Tribunal del Trabajo"},
                {"name": "demandante_nombre", "type": "string", "description": "Nombre del demandante"},
                {"name": "demandante_rut", "type": "rut", "description": "RUT del demandante"},
                {"name": "demandado_nombre", "type": "string", "description": "Nombre del demandado"},
                {"name": "demandado_rut", "type": "rut", "description": "RUT del demandado"},
                {"name": "hechos", "type": "text", "description": "Relato de los hechos"},
                {"name": "pretensiones", "type": "text", "description": "Lo que se solicita"},
            ],
        }

        descriptions = {
            "finiquito": "Documento de término de relación laboral",
            "demanda_laboral": "Demanda ante tribunales del trabajo",
            "carta_reclamo": "Carta de reclamo formal ante empresas/SERNAC",
        }

        return {
            "success": True,
            "template_name": template_name,
            "description": descriptions.get(template_name, "Documento legal"),
            "variables": list(variables),
            "required_fields": fields_map.get(template_name, []),
            "template_content": template_content,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def fill_template_standalone(template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Versión standalone de fill_template."""
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape

        template_result = load_template_standalone(template_name)
        if not template_result.get("success"):
            return template_result

        env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(['html', 'xml']),
        )

        env.filters['format_rut'] = _format_rut
        env.filters['format_money'] = _format_money
        env.filters['format_date'] = _format_date

        template = env.get_template(f"{template_name}.jinja2")

        if 'fecha_documento' not in data:
            data['fecha_documento'] = datetime.now().strftime("%Y-%m-%d")

        rendered_content = template.render(**data)

        return {
            "success": True,
            "template_name": template_name,
            "content": rendered_content,
            "data_used": data,
            "generated_at": datetime.now().isoformat(),
        }

    except ImportError:
        return {
            "success": False,
            "error": "Jinja2 no está instalado. Ejecute: pip install jinja2",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


if __name__ == "__main__":
    # Tests básicos
    print("=== Test Glosario ===")
    result = glosario_lookup_standalone("alimentos")
    print(f"Término 'alimentos': encontrado={result['encontrado']}")

    print("\n=== Test Siglas ===")
    result = buscar_sigla_standalone("RIT")
    print(f"Sigla 'RIT': encontrado={result['encontrado']}")

    print("\n=== Test Plantillas ===")
    result = list_templates_standalone()
    print(f"Plantillas: {result}")

    print("\n=== Test Cargar Finiquito ===")
    result = load_template_standalone("finiquito")
    print(f"Plantilla finiquito: success={result['success']}")
    print(f"Campos requeridos: {len(result.get('required_fields', []))}")
