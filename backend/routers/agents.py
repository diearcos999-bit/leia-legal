"""
Router de Agentes de IA para JusticiaAI.

Este módulo expone los endpoints para interactuar con los agentes
de investigación legal y generación de documentos.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

# Importar agentes
try:
    from agents.research_agent import ResearchAgent
    from agents.document_agent import DocumentAgent
    AGENTS_AVAILABLE = True
except ImportError as e:
    AGENTS_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Inicializar el limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/agents", tags=["Agents"])


# ==================== MODELOS PYDANTIC ====================

class ResearchRequest(BaseModel):
    """Solicitud de investigación legal."""
    query: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="La consulta o pregunta legal a investigar"
    )
    category: Optional[str] = Field(
        None,
        description="Categoría opcional: laboral, familia, civil, penal, consumidor"
    )


class ResearchResponse(BaseModel):
    """Respuesta del agente de investigación."""
    success: bool
    answer: Optional[str] = None
    sources: List[Dict[str, Any]] = []
    tools_used: List[str] = []
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class DocumentRequest(BaseModel):
    """Solicitud de generación de documento."""
    document_type: str = Field(
        ...,
        description="Tipo de documento: finiquito, carta_reclamo, demanda_laboral"
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Datos para llenar el documento"
    )
    generate_pdf: bool = Field(
        True,
        description="Si debe generar el PDF además del contenido"
    )


class DocumentResponse(BaseModel):
    """Respuesta del agente de documentos."""
    success: bool
    document_type: Optional[str] = None
    content: Optional[str] = None
    pdf_path: Optional[str] = None
    pdf_filename: Optional[str] = None
    missing_fields: Optional[List[Dict[str, str]]] = None
    error: Optional[str] = None
    generated_at: Optional[str] = None


class ChatWithAgentRequest(BaseModel):
    """Solicitud de chat con un agente."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="El mensaje para el agente"
    )
    agent_type: str = Field(
        "research",
        description="Tipo de agente: research o document"
    )


class TemplateInfo(BaseModel):
    """Información de una plantilla de documento."""
    name: str
    description: str
    required_fields: List[Dict[str, str]]


class TemplatesListResponse(BaseModel):
    """Lista de plantillas disponibles."""
    success: bool
    templates: List[TemplateInfo] = []
    error: Optional[str] = None


# ==================== ENDPOINTS ====================

@router.get("/status")
async def agents_status():
    """
    Verifica el estado de los agentes de IA.

    Returns:
        Dict con el estado de disponibilidad de los agentes
    """
    if not AGENTS_AVAILABLE:
        return {
            "available": False,
            "error": f"Los agentes no están disponibles: {IMPORT_ERROR}",
            "required_packages": ["langgraph", "langchain-anthropic"],
        }

    return {
        "available": True,
        "agents": {
            "research_agent": {
                "name": "Agente Investigador Legal",
                "description": "Investiga legislación chilena y responde consultas legales",
                "endpoint": "/api/agents/research",
            },
            "document_agent": {
                "name": "Agente de Documentos",
                "description": "Genera documentos legales chilenos",
                "endpoint": "/api/agents/generate-document",
            },
        },
        "templates_endpoint": "/api/agents/templates",
    }


@router.post("/research", response_model=ResearchResponse)
@limiter.limit("10/minute")
async def research(request: Request, research_request: ResearchRequest):
    """
    Ejecuta una investigación legal usando el agente investigador.

    El agente:
    - Busca en la base de conocimiento legal (RAG)
    - Consulta el glosario de términos
    - Sintetiza una respuesta con fuentes

    Args:
        research_request: Consulta a investigar

    Returns:
        Respuesta con la información legal encontrada
    """
    if not AGENTS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Los agentes de IA no están disponibles. Instale: pip install langgraph langchain-anthropic"
        )

    try:
        agent = ResearchAgent()
        result = await agent.run(research_request.query)

        return ResearchResponse(
            success=result.get("success", False),
            answer=result.get("answer"),
            sources=result.get("sources", []),
            tools_used=result.get("tools_used", []),
            error=result.get("error"),
            metadata=result.get("metadata", {}),
        )

    except Exception as e:
        return ResearchResponse(
            success=False,
            error=str(e),
            metadata={"error_time": datetime.now().isoformat()},
        )


@router.post("/generate-document", response_model=DocumentResponse)
@limiter.limit("5/minute")
async def generate_document(request: Request, doc_request: DocumentRequest):
    """
    Genera un documento legal usando el agente de documentos.

    Documentos disponibles:
    - finiquito: Documento de término de relación laboral
    - carta_reclamo: Carta de reclamo formal (SERNAC)
    - demanda_laboral: Demanda ante tribunales del trabajo

    Args:
        doc_request: Tipo de documento y datos para llenarlo

    Returns:
        Documento generado con opción de PDF
    """
    if not AGENTS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Los agentes de IA no están disponibles. Instale: pip install langgraph langchain-anthropic"
        )

    # Validar tipo de documento
    valid_types = ["finiquito", "carta_reclamo", "demanda_laboral"]
    if doc_request.document_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de documento inválido. Opciones: {', '.join(valid_types)}"
        )

    try:
        agent = DocumentAgent()
        result = await agent.generate_document(
            document_type=doc_request.document_type,
            data=doc_request.data,
            generate_pdf=doc_request.generate_pdf,
        )

        return DocumentResponse(
            success=result.get("success", False),
            document_type=result.get("document_type"),
            content=result.get("content"),
            pdf_path=result.get("pdf_path"),
            pdf_filename=result.get("pdf_filename"),
            missing_fields=result.get("missing_fields"),
            error=result.get("error"),
            generated_at=result.get("generated_at"),
        )

    except Exception as e:
        return DocumentResponse(
            success=False,
            error=str(e),
        )


@router.get("/templates", response_model=TemplatesListResponse)
async def list_document_templates():
    """
    Lista las plantillas de documentos disponibles.

    Returns:
        Lista de plantillas con sus campos requeridos
    """
    if not AGENTS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Los agentes de IA no están disponibles"
        )

    try:
        from agents.tools.document_tools import list_templates, load_template

        # Obtener lista de plantillas
        templates_result = list_templates.invoke({})

        if not templates_result.get("success"):
            return TemplatesListResponse(
                success=False,
                error=templates_result.get("message", "No hay plantillas disponibles"),
            )

        # Obtener detalles de cada plantilla
        detailed_templates = []
        for template in templates_result.get("templates", []):
            template_detail = load_template.invoke({"template_name": template["name"]})
            if template_detail.get("success"):
                detailed_templates.append(TemplateInfo(
                    name=template["name"],
                    description=template_detail.get("description", template["description"]),
                    required_fields=template_detail.get("required_fields", []),
                ))

        return TemplatesListResponse(
            success=True,
            templates=detailed_templates,
        )

    except Exception as e:
        return TemplatesListResponse(
            success=False,
            error=str(e),
        )


@router.get("/templates/{template_name}")
async def get_template_details(template_name: str):
    """
    Obtiene los detalles de una plantilla específica.

    Args:
        template_name: Nombre de la plantilla

    Returns:
        Detalles de la plantilla incluyendo campos requeridos
    """
    if not AGENTS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Los agentes de IA no están disponibles"
        )

    try:
        from agents.tools.document_tools import load_template

        result = load_template.invoke({"template_name": template_name})

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get("error", f"Plantilla '{template_name}' no encontrada")
            )

        return {
            "success": True,
            "template_name": result.get("template_name"),
            "description": result.get("description"),
            "required_fields": result.get("required_fields", []),
            "variables": result.get("variables", []),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/chat")
@limiter.limit("15/minute")
async def chat_with_agent(request: Request, chat_request: ChatWithAgentRequest):
    """
    Endpoint de chat conversacional con los agentes.

    Permite interactuar de forma más natural con los agentes,
    haciendo preguntas o solicitando documentos.

    Args:
        chat_request: Mensaje y tipo de agente

    Returns:
        Respuesta del agente
    """
    if not AGENTS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Los agentes de IA no están disponibles"
        )

    try:
        if chat_request.agent_type == "research":
            agent = ResearchAgent()
        elif chat_request.agent_type == "document":
            agent = DocumentAgent()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de agente inválido. Opciones: research, document"
            )

        result = await agent.run(chat_request.message)

        return {
            "success": result.get("success", False),
            "response": result.get("answer") or result.get("final_answer"),
            "sources": result.get("sources", []),
            "tools_used": result.get("tools_used", []),
            "error": result.get("error"),
            "metadata": result.get("metadata", {}),
        }

    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None,
        }


# ==================== ENDPOINTS DE UTILIDAD ====================

@router.get("/categories")
async def get_legal_categories():
    """
    Lista las categorías legales disponibles para filtrar búsquedas.

    Returns:
        Lista de categorías con descripciones
    """
    return {
        "categories": [
            {
                "id": "laboral",
                "name": "Derecho Laboral",
                "description": "Despidos, finiquitos, indemnizaciones, contratos de trabajo",
                "keywords": ["despido", "finiquito", "indemnización", "contrato", "sueldo"],
            },
            {
                "id": "familia",
                "name": "Derecho de Familia",
                "description": "Divorcios, pensiones alimenticias, cuidado personal, visitas",
                "keywords": ["divorcio", "pensión", "alimentos", "custodia", "cuidado personal"],
            },
            {
                "id": "civil",
                "name": "Derecho Civil",
                "description": "Contratos, arriendos, deudas, herencias",
                "keywords": ["arriendo", "deuda", "contrato", "herencia", "demanda"],
            },
            {
                "id": "consumidor",
                "name": "Derecho del Consumidor",
                "description": "Reclamos, garantías, SERNAC, publicidad engañosa",
                "keywords": ["reclamo", "garantía", "SERNAC", "devolución", "producto"],
            },
            {
                "id": "penal",
                "name": "Derecho Penal",
                "description": "Delitos, querellas, defensa penal",
                "keywords": ["delito", "querella", "denuncia", "fiscalía", "defensa"],
            },
        ]
    }
