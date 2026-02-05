"""
Herramientas de documentos para los agentes de LEIA.

Proporciona funciones para cargar plantillas, llenar formularios
y generar documentos PDF legales.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import os
import re

from langchain_core.tools import tool

# Directorio de plantillas
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "legal"


def _format_rut(rut: str) -> str:
    """Formatea un RUT chileno."""
    # Remover puntos y guiones existentes
    rut_clean = re.sub(r'[.\-]', '', rut.upper())
    if len(rut_clean) < 2:
        return rut

    # Separar cuerpo y dígito verificador
    body = rut_clean[:-1]
    dv = rut_clean[-1]

    # Formatear con puntos
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
            # Intentar varios formatos
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


def _get_available_templates() -> List[Dict[str, str]]:
    """Lista las plantillas disponibles."""
    templates = []

    if not TEMPLATES_DIR.exists():
        return templates

    for template_file in TEMPLATES_DIR.glob("*.jinja2"):
        template_name = template_file.stem
        templates.append({
            "name": template_name,
            "path": str(template_file),
            "description": _get_template_description(template_name),
        })

    return templates


def _get_template_description(name: str) -> str:
    """Obtiene la descripción de una plantilla."""
    descriptions = {
        "finiquito": "Documento de término de relación laboral",
        "demanda_laboral": "Demanda ante tribunales del trabajo",
        "carta_reclamo": "Carta de reclamo formal ante empresas/SERNAC",
        "contrato_arriendo": "Contrato de arrendamiento de inmueble",
        "poder_simple": "Poder simple para trámites",
        "carta_despido": "Carta de aviso de término de contrato",
    }
    return descriptions.get(name, "Documento legal")


@tool
def load_template(template_name: str) -> Dict[str, Any]:
    """
    Carga una plantilla de documento legal.

    Esta herramienta obtiene la estructura y campos requeridos
    de una plantilla para generar documentos legales.

    Args:
        template_name: Nombre de la plantilla (ej: "finiquito", "carta_reclamo")

    Returns:
        Dict con la plantilla cargada y los campos requeridos
    """
    template_path = TEMPLATES_DIR / f"{template_name}.jinja2"

    if not template_path.exists():
        available = _get_available_templates()
        return {
            "success": False,
            "error": f"Plantilla '{template_name}' no encontrada",
            "available_templates": available,
        }

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Extraer variables del template (patrón {{ variable }})
        variables = set(re.findall(r'\{\{\s*(\w+)\s*\}\}', template_content))

        # Obtener campos requeridos de metadata si existe
        required_fields = _get_template_required_fields(template_name)

        return {
            "success": True,
            "template_name": template_name,
            "description": _get_template_description(template_name),
            "variables": list(variables),
            "required_fields": required_fields,
            "template_content": template_content,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def _get_template_required_fields(template_name: str) -> List[Dict[str, str]]:
    """Obtiene los campos requeridos para cada plantilla."""
    fields_map = {
        "finiquito": [
            {"name": "empleador_nombre", "type": "string", "description": "Nombre o razón social del empleador"},
            {"name": "empleador_rut", "type": "rut", "description": "RUT del empleador"},
            {"name": "trabajador_nombre", "type": "string", "description": "Nombre completo del trabajador"},
            {"name": "trabajador_rut", "type": "rut", "description": "RUT del trabajador"},
            {"name": "fecha_inicio", "type": "date", "description": "Fecha de inicio de la relación laboral"},
            {"name": "fecha_termino", "type": "date", "description": "Fecha de término"},
            {"name": "causal_termino", "type": "string", "description": "Causal de término (art. del Código del Trabajo)"},
            {"name": "ultimo_sueldo", "type": "money", "description": "Último sueldo bruto mensual"},
            {"name": "dias_vacaciones", "type": "number", "description": "Días de vacaciones pendientes"},
            {"name": "anos_servicio", "type": "number", "description": "Años de servicio para indemnización"},
        ],
        "carta_reclamo": [
            {"name": "destinatario_nombre", "type": "string", "description": "Nombre de la empresa/institución"},
            {"name": "destinatario_direccion", "type": "string", "description": "Dirección del destinatario"},
            {"name": "remitente_nombre", "type": "string", "description": "Nombre del reclamante"},
            {"name": "remitente_rut", "type": "rut", "description": "RUT del reclamante"},
            {"name": "remitente_direccion", "type": "string", "description": "Dirección del reclamante"},
            {"name": "remitente_email", "type": "email", "description": "Email de contacto"},
            {"name": "fecha_compra", "type": "date", "description": "Fecha de la compra/servicio"},
            {"name": "descripcion_problema", "type": "text", "description": "Descripción detallada del problema"},
            {"name": "solucion_solicitada", "type": "text", "description": "Solución que solicita"},
        ],
        "demanda_laboral": [
            {"name": "tribunal", "type": "string", "description": "Tribunal del Trabajo correspondiente"},
            {"name": "demandante_nombre", "type": "string", "description": "Nombre del trabajador demandante"},
            {"name": "demandante_rut", "type": "rut", "description": "RUT del demandante"},
            {"name": "demandante_direccion", "type": "string", "description": "Dirección del demandante"},
            {"name": "demandado_nombre", "type": "string", "description": "Nombre/razón social del empleador"},
            {"name": "demandado_rut", "type": "rut", "description": "RUT del demandado"},
            {"name": "demandado_direccion", "type": "string", "description": "Dirección del demandado"},
            {"name": "fecha_ingreso", "type": "date", "description": "Fecha de inicio de la relación laboral"},
            {"name": "fecha_despido", "type": "date", "description": "Fecha del despido"},
            {"name": "ultimo_sueldo", "type": "money", "description": "Último sueldo mensual"},
            {"name": "hechos", "type": "text", "description": "Relato de los hechos"},
            {"name": "pretensiones", "type": "text", "description": "Lo que se solicita al tribunal"},
        ],
    }
    return fields_map.get(template_name, [])


@tool
def fill_template(
    template_name: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Llena una plantilla con los datos proporcionados.

    Esta herramienta genera el contenido del documento legal
    usando la plantilla y los datos del usuario.

    Args:
        template_name: Nombre de la plantilla a usar
        data: Diccionario con los valores para cada campo

    Returns:
        Dict con el documento generado
    """
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape

        # Cargar plantilla
        template_result = load_template.invoke({"template_name": template_name})
        if not template_result.get("success"):
            return template_result

        # Configurar Jinja2
        env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(['html', 'xml']),
        )

        # Agregar filtros personalizados
        env.filters['format_rut'] = _format_rut
        env.filters['format_money'] = _format_money
        env.filters['format_date'] = _format_date

        # Cargar y renderizar template
        template = env.get_template(f"{template_name}.jinja2")

        # Agregar fecha actual si no está en los datos
        if 'fecha_documento' not in data:
            data['fecha_documento'] = datetime.now().strftime("%Y-%m-%d")

        # Formatear datos según tipo
        required_fields = _get_template_required_fields(template_name)
        for field in required_fields:
            field_name = field["name"]
            if field_name in data:
                if field["type"] == "rut":
                    data[field_name] = _format_rut(str(data[field_name]))
                elif field["type"] == "money":
                    data[field_name] = _format_money(int(data[field_name]))
                elif field["type"] == "date":
                    data[field_name] = _format_date(str(data[field_name]))

        # Renderizar
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


@tool
def generate_pdf(
    content: str,
    filename: str,
    title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Genera un archivo PDF a partir del contenido del documento.

    Esta herramienta convierte el documento generado a formato PDF
    para su descarga o impresión.

    Args:
        content: Contenido del documento (texto o HTML)
        filename: Nombre del archivo de salida (sin extensión)
        title: Título opcional para el documento

    Returns:
        Dict con la ruta del PDF generado
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

        # Directorio de salida
        output_dir = Path(__file__).parent.parent.parent / "data" / "generated_documents"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = re.sub(r'[^\w\-]', '_', filename)
        output_path = output_dir / f"{safe_filename}_{timestamp}.pdf"

        # Crear documento
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Justify',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=11,
            leading=14,
        ))
        styles.add(ParagraphStyle(
            name='Title_Custom',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=16,
            spaceAfter=30,
        ))

        # Construir contenido
        story = []

        if title:
            story.append(Paragraph(title, styles['Title_Custom']))
            story.append(Spacer(1, 0.25 * inch))

        # Procesar contenido (dividir en párrafos)
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Limpiar HTML básico si existe
                clean_para = re.sub(r'<[^>]+>', '', para)
                story.append(Paragraph(clean_para, styles['Justify']))
                story.append(Spacer(1, 0.15 * inch))

        # Generar PDF
        doc.build(story)

        return {
            "success": True,
            "pdf_path": str(output_path),
            "filename": output_path.name,
            "generated_at": datetime.now().isoformat(),
        }

    except ImportError:
        return {
            "success": False,
            "error": "ReportLab no está instalado. Ejecute: pip install reportlab",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@tool
def list_templates() -> Dict[str, Any]:
    """
    Lista todas las plantillas de documentos legales disponibles.

    Returns:
        Dict con la lista de plantillas y sus descripciones
    """
    templates = _get_available_templates()

    if not templates:
        return {
            "success": True,
            "templates": [],
            "message": "No hay plantillas disponibles. Las plantillas deben estar en el directorio templates/legal/",
        }

    return {
        "success": True,
        "templates": templates,
        "total": len(templates),
    }


def get_document_tools() -> List:
    """
    Retorna todas las herramientas de documentos para usar con LangGraph.

    Returns:
        Lista de herramientas de documentos
    """
    return [
        load_template,
        fill_template,
        generate_pdf,
        list_templates,
    ]
