"""
Herramientas RAG para los agentes de LEIA.

Proporciona funciones para buscar en la base de conocimiento legal
usando el sistema RAG existente (Pinecone + OpenAI embeddings).
"""

from typing import List, Dict, Any, Optional
import os

from langchain_core.tools import tool

# Importar el sistema RAG existente
try:
    from rag.rag_engine import RAGEngine, create_rag_engine
    from rag.vector_store import VectorStore
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# Singleton para el RAG engine
_rag_engine: Optional["RAGEngine"] = None


def get_rag_engine() -> Optional["RAGEngine"]:
    """
    Obtiene la instancia singleton del RAG engine.

    Returns:
        RAGEngine si está disponible, None si no está configurado
    """
    global _rag_engine

    if _rag_engine is not None:
        return _rag_engine

    if not RAG_AVAILABLE:
        return None

    _rag_engine = create_rag_engine()
    return _rag_engine


@tool
def rag_search(
    query: str,
    category: Optional[str] = None,
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    Busca información legal relevante en la base de conocimiento RAG.

    Esta herramienta consulta la base de datos vectorial para encontrar
    legislación chilena, artículos y documentos legales relevantes
    para responder la consulta del usuario.

    Args:
        query: La consulta o pregunta a buscar
        category: Categoría opcional para filtrar (laboral, familia, civil, etc.)
        top_k: Número de resultados a retornar (default: 3)

    Returns:
        Dict con los documentos encontrados y sus metadatos
    """
    engine = get_rag_engine()

    if engine is None:
        return {
            "success": False,
            "error": "Sistema RAG no disponible",
            "documents": [],
            "context": "",
        }

    try:
        # Construir filtro si se especifica categoría
        filter_dict = None
        if category:
            filter_dict = {"category": category.lower()}

        # Buscar documentos relevantes
        documents = engine.retrieve_context(query, filter=filter_dict)

        if not documents:
            return {
                "success": True,
                "documents": [],
                "context": "",
                "message": "No se encontraron documentos relevantes para esta consulta.",
            }

        # Construir contexto formateado
        context = engine.build_context_prompt(documents)

        # Formatear resultados
        formatted_docs = []
        for doc in documents:
            formatted_docs.append({
                "law_name": doc.get("law_name", "Fuente desconocida"),
                "article": doc.get("article_number"),
                "category": doc.get("category", "general"),
                "text": doc.get("text", "")[:500] + "..." if len(doc.get("text", "")) > 500 else doc.get("text", ""),
                "url": doc.get("url"),
                "similarity_score": doc.get("score", 0),
            })

        return {
            "success": True,
            "documents": formatted_docs,
            "context": context,
            "total_found": len(documents),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "documents": [],
            "context": "",
        }


def search_legal_documents(
    query: str,
    category: Optional[str] = None,
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Función auxiliar para buscar documentos legales sin el decorador @tool.

    Args:
        query: La consulta a buscar
        category: Categoría opcional para filtrar
        top_k: Número de resultados

    Returns:
        Lista de documentos encontrados
    """
    result = rag_search.invoke({
        "query": query,
        "category": category,
        "top_k": top_k,
    })
    return result.get("documents", [])


def get_rag_tool():
    """
    Retorna la herramienta RAG para usar con LangGraph.

    Returns:
        La herramienta rag_search configurada
    """
    return rag_search


def format_rag_context(documents: List[Dict[str, Any]]) -> str:
    """
    Formatea una lista de documentos RAG en un contexto legible.

    Args:
        documents: Lista de documentos recuperados

    Returns:
        String formateado con el contexto
    """
    if not documents:
        return ""

    context_parts = ["INFORMACIÓN LEGAL RELEVANTE:\n"]

    for idx, doc in enumerate(documents, 1):
        context_parts.append(f"\n[Fuente {idx}]")
        context_parts.append(f"Ley: {doc.get('law_name', 'Desconocida')}")

        if doc.get("article"):
            context_parts.append(f"Artículo: {doc['article']}")

        context_parts.append(f"Categoría: {doc.get('category', 'General')}")
        context_parts.append(f"\nContenido:\n{doc.get('text', '')}")

        if doc.get("url"):
            context_parts.append(f"URL: {doc['url']}")

        context_parts.append("-" * 60)

    return "\n".join(context_parts)
