"""
Base Agent - Clase base para todos los agentes de LEIA.

Este módulo define la estructura común que comparten todos los agentes,
incluyendo el estado, configuración del LLM y métodos de ejecución.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from abc import ABC, abstractmethod
import os
from datetime import datetime

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    """
    Estado compartido entre nodos del grafo de un agente.

    Attributes:
        messages: Lista de mensajes de la conversación
        context: Contexto adicional recuperado (RAG, glosario, etc.)
        tools_used: Lista de herramientas utilizadas durante la ejecución
        intermediate_steps: Pasos intermedios del razonamiento
        final_answer: Respuesta final generada
        sources: Fuentes utilizadas para la respuesta
        metadata: Metadatos adicionales (timestamps, tokens, etc.)
    """
    messages: Annotated[List[BaseMessage], add_messages]
    context: str
    tools_used: List[str]
    intermediate_steps: List[Dict[str, Any]]
    final_answer: Optional[str]
    sources: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class BaseAgent(ABC):
    """
    Clase base abstracta para todos los agentes de LEIA.

    Proporciona la configuración común del LLM, manejo de estado
    y métodos de ejecución que todos los agentes heredan.
    """

    def __init__(
        self,
        model: str = "claude-3-haiku-20240307",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        """
        Inicializa el agente base.

        Args:
            model: Modelo de Claude a utilizar
            temperature: Temperatura para la generación (0-1)
            max_tokens: Máximo de tokens en la respuesta
        """
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Inicializar el LLM
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no está configurada en el entorno")

        self.llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            anthropic_api_key=api_key,
        )

        # El grafo se construye en las subclases
        self.graph = None
        self.compiled_graph = None

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Prompt del sistema específico para cada agente."""
        pass

    @abstractmethod
    def build_graph(self) -> StateGraph:
        """
        Construye el grafo de estados del agente.

        Cada subclase implementa su propia lógica de grafo
        con nodos y transiciones específicas.

        Returns:
            StateGraph configurado para el agente
        """
        pass

    def _get_initial_state(self, query: str) -> AgentState:
        """
        Crea el estado inicial para una consulta.

        Args:
            query: Consulta del usuario

        Returns:
            AgentState inicializado
        """
        return AgentState(
            messages=[HumanMessage(content=query)],
            context="",
            tools_used=[],
            intermediate_steps=[],
            final_answer=None,
            sources=[],
            metadata={
                "start_time": datetime.now().isoformat(),
                "model": self.model_name,
                "query": query,
            }
        )

    def compile(self) -> None:
        """
        Compila el grafo del agente.

        Debe llamarse después de build_graph() para
        poder ejecutar el agente.
        """
        if self.graph is None:
            self.graph = self.build_graph()
        self.compiled_graph = self.graph.compile()

    async def run(self, query: str) -> Dict[str, Any]:
        """
        Ejecuta el agente con una consulta.

        Args:
            query: Consulta del usuario

        Returns:
            Dict con la respuesta, fuentes y metadata
        """
        if self.compiled_graph is None:
            self.compile()

        initial_state = self._get_initial_state(query)

        try:
            # Ejecutar el grafo
            final_state = await self.compiled_graph.ainvoke(initial_state)

            # Calcular metadata final
            end_time = datetime.now().isoformat()
            final_state["metadata"]["end_time"] = end_time

            return {
                "success": True,
                "answer": final_state.get("final_answer", ""),
                "sources": final_state.get("sources", []),
                "tools_used": final_state.get("tools_used", []),
                "metadata": final_state.get("metadata", {}),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": None,
                "sources": [],
                "tools_used": [],
                "metadata": {
                    "error_time": datetime.now().isoformat(),
                    "query": query,
                }
            }

    def run_sync(self, query: str) -> Dict[str, Any]:
        """
        Versión síncrona de run() para uso sin async.

        Args:
            query: Consulta del usuario

        Returns:
            Dict con la respuesta, fuentes y metadata
        """
        import asyncio

        # Obtener o crear event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si ya hay un loop corriendo, crear una tarea
                import nest_asyncio
                nest_asyncio.apply()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.run(query))


class AgentError(Exception):
    """Excepción base para errores de agentes."""
    pass


class AgentConfigError(AgentError):
    """Error de configuración del agente."""
    pass


class AgentExecutionError(AgentError):
    """Error durante la ejecución del agente."""
    pass
