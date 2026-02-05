"""
Research Agent - Agente Investigador Legal de LEIA.

Este agente está especializado en investigar legislación chilena,
jurisprudencia y responder consultas legales usando RAG y el glosario.
"""

from typing import Dict, Any, List, Optional, Literal

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agents.base import BaseAgent, AgentState
from agents.tools.rag_tools import rag_search, format_rag_context
from agents.tools.legal_tools import (
    glosario_lookup,
    buscar_sigla,
    buscar_categoria,
    buscar_frase_legal,
)


class ResearchAgent(BaseAgent):
    """
    Agente investigador especializado en derecho chileno.

    Capacidades:
    - Buscar en la base de conocimiento legal (RAG)
    - Consultar el glosario de términos legales
    - Explicar siglas y frases latinas
    - Sintetizar información de múltiples fuentes
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        super().__init__(model, temperature, max_tokens)

        # Herramientas disponibles para este agente
        self.tools = [
            rag_search,
            glosario_lookup,
            buscar_sigla,
            buscar_frase_legal,
        ]

        # Vincular herramientas al LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Construir el grafo
        self.graph = self.build_graph()

    @property
    def system_prompt(self) -> str:
        return """Eres el Agente Investigador Legal de LEIA, especializado en derecho chileno.

Tu rol es investigar y proporcionar información legal precisa sobre el sistema jurídico chileno.

CAPACIDADES:
1. rag_search: Buscar legislación y documentos legales en la base de conocimiento
2. glosario_lookup: Buscar definiciones de términos legales
3. buscar_sigla: Explicar siglas legales (RIT, RUC, VIF, etc.)
4. buscar_frase_legal: Explicar frases latinas usadas en derecho

INSTRUCCIONES:
- SIEMPRE usa las herramientas disponibles para fundamentar tus respuestas
- Cita las fuentes específicas cuando uses información del RAG
- Explica los términos legales en lenguaje sencillo
- Si no encuentras información específica, indícalo claramente
- Recuerda que das ORIENTACIÓN general, no asesoría legal profesional
- SIEMPRE recomienda consultar con un abogado para casos específicos

ÁREAS DE ESPECIALIDAD:
- Derecho Laboral (despidos, finiquitos, indemnizaciones)
- Derecho de Familia (divorcios, pensiones, cuidado personal)
- Derecho del Consumidor
- Derecho Civil
- Derecho Penal básico

FORMATO DE RESPUESTA:
1. Responde la consulta principal
2. Cita las fuentes legales relevantes
3. Explica términos técnicos si es necesario
4. Sugiere pasos a seguir si aplica
5. Recomienda consultar con un abogado"""

    def _should_continue(self, state: AgentState) -> Literal["tools", "synthesize"]:
        """
        Decide si continuar usando herramientas o sintetizar la respuesta.
        """
        messages = state["messages"]
        last_message = messages[-1]

        # Si el LLM hizo una llamada a herramienta, ejecutarla
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        # Si no hay llamadas a herramientas, sintetizar
        return "synthesize"

    def _call_model(self, state: AgentState) -> Dict[str, Any]:
        """
        Llama al modelo con el estado actual.
        """
        messages = state["messages"]

        # Agregar el system prompt al inicio si es la primera llamada
        if len(messages) == 1:  # Solo tiene el mensaje del usuario
            system_message = SystemMessage(content=self.system_prompt)
            messages = [system_message] + messages

        response = self.llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def _use_tools(self, state: AgentState) -> Dict[str, Any]:
        """
        Ejecuta las herramientas y actualiza el estado.
        """
        messages = state["messages"]
        last_message = messages[-1]

        tool_calls = last_message.tool_calls
        tools_used = state.get("tools_used", [])
        sources = state.get("sources", [])
        context = state.get("context", "")

        # Crear el nodo de herramientas
        tool_node = ToolNode(self.tools)
        tool_results = tool_node.invoke({"messages": messages})

        # Actualizar herramientas usadas y fuentes
        for tc in tool_calls:
            tool_name = tc["name"]
            if tool_name not in tools_used:
                tools_used.append(tool_name)

            # Extraer fuentes de RAG si aplica
            if tool_name == "rag_search":
                for msg in tool_results.get("messages", []):
                    if hasattr(msg, "content"):
                        try:
                            import json
                            result = json.loads(msg.content) if isinstance(msg.content, str) else msg.content
                            if isinstance(result, dict) and result.get("documents"):
                                for doc in result["documents"]:
                                    sources.append({
                                        "type": "rag",
                                        "law_name": doc.get("law_name"),
                                        "article": doc.get("article"),
                                        "category": doc.get("category"),
                                    })
                                # Agregar contexto
                                if result.get("context"):
                                    context += "\n" + result["context"]
                        except (json.JSONDecodeError, TypeError):
                            pass

        return {
            "messages": tool_results.get("messages", []),
            "tools_used": tools_used,
            "sources": sources,
            "context": context,
        }

    def _synthesize(self, state: AgentState) -> Dict[str, Any]:
        """
        Sintetiza la respuesta final basada en toda la información recopilada.
        """
        messages = state["messages"]
        context = state.get("context", "")
        sources = state.get("sources", [])

        # Si ya tenemos una respuesta del modelo sin herramientas
        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and not hasattr(last_message, "tool_calls"):
            final_answer = last_message.content
        else:
            # Generar respuesta final con todo el contexto
            synthesis_prompt = f"""Basándote en la información recopilada, proporciona una respuesta
completa y bien estructurada a la consulta del usuario.

CONTEXTO RECOPILADO:
{context if context else "No se encontró contexto adicional."}

FUENTES UTILIZADAS:
{sources if sources else "Conocimiento general."}

Recuerda:
- Responder en español chileno
- Usar lenguaje accesible
- Citar fuentes específicas
- Recomendar consultar con un abogado"""

            messages_for_synthesis = messages + [HumanMessage(content=synthesis_prompt)]
            response = self.llm.invoke(messages_for_synthesis)
            final_answer = response.content

        return {
            "final_answer": final_answer,
            "metadata": {
                **state.get("metadata", {}),
                "sources_count": len(sources),
                "tools_used_count": len(state.get("tools_used", [])),
            }
        }

    def build_graph(self) -> StateGraph:
        """
        Construye el grafo de estados del agente investigador.

        Flujo:
        1. call_model: Analiza la consulta y decide qué herramientas usar
        2. tools: Ejecuta las herramientas seleccionadas
        3. synthesize: Sintetiza la respuesta final

        El agente puede iterar entre call_model y tools múltiples veces
        hasta tener suficiente información.
        """
        # Crear el grafo
        workflow = StateGraph(AgentState)

        # Agregar nodos
        workflow.add_node("call_model", self._call_model)
        workflow.add_node("tools", self._use_tools)
        workflow.add_node("synthesize", self._synthesize)

        # Definir el punto de entrada
        workflow.set_entry_point("call_model")

        # Agregar transiciones condicionales
        workflow.add_conditional_edges(
            "call_model",
            self._should_continue,
            {
                "tools": "tools",
                "synthesize": "synthesize",
            }
        )

        # Después de usar herramientas, volver al modelo
        workflow.add_edge("tools", "call_model")

        # Synthesize es el nodo final
        workflow.add_edge("synthesize", END)

        return workflow


async def run_research_query(query: str) -> Dict[str, Any]:
    """
    Función auxiliar para ejecutar una consulta con el agente investigador.

    Args:
        query: La consulta legal a investigar

    Returns:
        Dict con la respuesta y metadata
    """
    agent = ResearchAgent()
    return await agent.run(query)
