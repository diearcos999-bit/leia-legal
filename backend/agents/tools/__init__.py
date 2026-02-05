"""
Herramientas para los agentes de IA.

Este módulo contiene las herramientas que los agentes pueden usar
para realizar búsquedas RAG, consultas al glosario y generación de documentos.
"""

# Las herramientas se importan bajo demanda para evitar
# errores cuando langchain no está instalado
TOOLS_AVAILABLE = False

try:
    from agents.tools.rag_tools import rag_search, get_rag_tool
    from agents.tools.legal_tools import (
        glosario_lookup,
        buscar_sigla,
        buscar_categoria,
        get_legal_tools,
    )
    from agents.tools.document_tools import (
        load_template,
        fill_template,
        generate_pdf,
        get_document_tools,
    )
    TOOLS_AVAILABLE = True
except ImportError:
    # Definir placeholders cuando langchain no está disponible
    rag_search = None
    get_rag_tool = None
    glosario_lookup = None
    buscar_sigla = None
    buscar_categoria = None
    get_legal_tools = None
    load_template = None
    fill_template = None
    generate_pdf = None
    get_document_tools = None

__all__ = [
    "TOOLS_AVAILABLE",
    # RAG tools
    "rag_search",
    "get_rag_tool",
    # Legal tools
    "glosario_lookup",
    "buscar_sigla",
    "buscar_categoria",
    "get_legal_tools",
    # Document tools
    "load_template",
    "fill_template",
    "generate_pdf",
    "get_document_tools",
]
