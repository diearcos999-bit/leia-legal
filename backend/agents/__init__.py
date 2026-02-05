"""
Agentes de IA para LEIA.

Este módulo contiene los agentes especializados que procesan consultas legales,
generan documentos y analizan casos usando LangGraph + Claude.
"""

# Imports condicionales para cuando las dependencias no están instaladas
try:
    from agents.base import BaseAgent, AgentState
    from agents.research_agent import ResearchAgent
    from agents.document_agent import DocumentAgent
    AGENTS_AVAILABLE = True
except ImportError as e:
    AGENTS_AVAILABLE = False
    BaseAgent = None
    AgentState = None
    ResearchAgent = None
    DocumentAgent = None

__all__ = [
    "BaseAgent",
    "AgentState",
    "ResearchAgent",
    "DocumentAgent",
    "AGENTS_AVAILABLE",
]
