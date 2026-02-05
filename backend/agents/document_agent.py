"""
Document Agent - Agente Generador de Documentos de LEIA.

Este agente está especializado en generar documentos legales chilenos
usando plantillas predefinidas y los datos proporcionados por el usuario.
"""

from typing import Dict, Any, List, Optional, Literal

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agents.base import BaseAgent, AgentState
from agents.tools.document_tools import (
    load_template,
    fill_template,
    generate_pdf,
    list_templates,
)
from agents.tools.legal_tools import glosario_lookup


class DocumentAgent(BaseAgent):
    """
    Agente generador de documentos legales.

    Capacidades:
    - Listar plantillas disponibles
    - Guiar al usuario en la recopilación de datos
    - Llenar plantillas con datos validados
    - Generar documentos PDF
    """

    def __init__(
        self,
        model: str = "claude-3-haiku-20240307",
        temperature: float = 0.2,  # Más bajo para mayor precisión
        max_tokens: int = 4096,
    ):
        super().__init__(model, temperature, max_tokens)

        # Herramientas disponibles para este agente
        self.tools = [
            list_templates,
            load_template,
            fill_template,
            generate_pdf,
            glosario_lookup,  # Para explicar términos si el usuario pregunta
        ]

        # Vincular herramientas al LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Construir el grafo
        self.graph = self.build_graph()

    @property
    def system_prompt(self) -> str:
        return """Eres el Agente de Documentos de LEIA, especializado en documentos legales chilenos.

Tu rol es ayudar a los usuarios a generar documentos legales chilenos de forma guiada y precisa.

CAPACIDADES:
1. list_templates: Listar las plantillas de documentos disponibles
2. load_template: Cargar una plantilla específica y ver sus campos requeridos
3. fill_template: Llenar una plantilla con los datos del usuario
4. generate_pdf: Generar el documento en formato PDF
5. glosario_lookup: Explicar términos legales si el usuario tiene dudas

DOCUMENTOS DISPONIBLES:
- Finiquito de trabajo
- Carta de reclamo (SERNAC)
- Demanda laboral

PROCESO DE GENERACIÓN:
1. Identificar qué tipo de documento necesita el usuario
2. Cargar la plantilla correspondiente
3. Solicitar los datos requeridos de forma clara
4. Validar que los datos estén completos
5. Generar el documento
6. Ofrecer descargarlo en PDF

INSTRUCCIONES IMPORTANTES:
- Sé PRECISO con los datos legales (RUT, fechas, montos)
- Explica cada campo que solicites al usuario
- Valida que los RUT tengan formato correcto (XX.XXX.XXX-X)
- Valida que las fechas estén en formato correcto
- Si faltan datos obligatorios, solicítalos antes de generar
- SIEMPRE advierte que el documento debe ser revisado por un abogado
- El finiquito DEBE ser ratificado ante un ministro de fe

FORMATO DE RUT CHILENO:
- Personas: XX.XXX.XXX-X (ej: 12.345.678-9)
- Empresas: XX.XXX.XXX-X (ej: 76.123.456-7)

FORMATO DE MONTOS:
- Siempre en pesos chilenos
- Sin decimales (ej: 500000, no 500.000)

ADVERTENCIAS OBLIGATORIAS:
- El finiquito debe ratificarse ante: Inspección del Trabajo, Notario, o Registro Civil
- La demanda laboral requiere patrocinio de abogado para ser presentada
- Los documentos generados son BORRADORES que deben ser revisados"""

    def _should_continue(self, state: AgentState) -> Literal["tools", "respond"]:
        """
        Decide si continuar usando herramientas o responder al usuario.
        """
        messages = state["messages"]
        last_message = messages[-1]

        # Si el LLM hizo una llamada a herramienta, ejecutarla
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        return "respond"

    def _call_model(self, state: AgentState) -> Dict[str, Any]:
        """
        Llama al modelo con el estado actual.
        """
        messages = state["messages"]

        # Agregar el system prompt al inicio si es la primera llamada
        if len(messages) == 1:
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
        metadata = state.get("metadata", {})

        # Crear el nodo de herramientas
        tool_node = ToolNode(self.tools)
        tool_results = tool_node.invoke({"messages": messages})

        # Actualizar herramientas usadas
        for tc in tool_calls:
            tool_name = tc["name"]
            if tool_name not in tools_used:
                tools_used.append(tool_name)

            # Guardar información del documento generado
            if tool_name == "fill_template":
                metadata["template_used"] = tc.get("args", {}).get("template_name")

            if tool_name == "generate_pdf":
                for msg in tool_results.get("messages", []):
                    if hasattr(msg, "content"):
                        try:
                            import json
                            result = json.loads(msg.content) if isinstance(msg.content, str) else msg.content
                            if isinstance(result, dict) and result.get("success"):
                                metadata["pdf_path"] = result.get("pdf_path")
                                metadata["pdf_filename"] = result.get("filename")
                        except (json.JSONDecodeError, TypeError):
                            pass

        return {
            "messages": tool_results.get("messages", []),
            "tools_used": tools_used,
            "metadata": metadata,
        }

    def _respond(self, state: AgentState) -> Dict[str, Any]:
        """
        Genera la respuesta final para el usuario.
        """
        messages = state["messages"]
        last_message = messages[-1]

        if isinstance(last_message, AIMessage):
            final_answer = last_message.content
        else:
            final_answer = "Lo siento, hubo un error procesando tu solicitud."

        return {
            "final_answer": final_answer,
        }

    def build_graph(self) -> StateGraph:
        """
        Construye el grafo de estados del agente de documentos.

        Flujo:
        1. call_model: Analiza la solicitud y decide qué hacer
        2. tools: Ejecuta las herramientas necesarias
        3. respond: Genera la respuesta final

        El agente puede iterar entre call_model y tools para
        recopilar datos y generar el documento.
        """
        # Crear el grafo
        workflow = StateGraph(AgentState)

        # Agregar nodos
        workflow.add_node("call_model", self._call_model)
        workflow.add_node("tools", self._use_tools)
        workflow.add_node("respond", self._respond)

        # Definir el punto de entrada
        workflow.set_entry_point("call_model")

        # Agregar transiciones condicionales
        workflow.add_conditional_edges(
            "call_model",
            self._should_continue,
            {
                "tools": "tools",
                "respond": "respond",
            }
        )

        # Después de usar herramientas, volver al modelo
        workflow.add_edge("tools", "call_model")

        # respond es el nodo final
        workflow.add_edge("respond", END)

        return workflow

    async def generate_document(
        self,
        document_type: str,
        data: Dict[str, Any],
        generate_pdf: bool = True,
    ) -> Dict[str, Any]:
        """
        Método directo para generar un documento con datos ya conocidos.

        Args:
            document_type: Tipo de documento (finiquito, carta_reclamo, demanda_laboral)
            data: Diccionario con todos los datos requeridos
            generate_pdf: Si debe generar también el PDF

        Returns:
            Dict con el documento generado y metadata
        """
        # Cargar la plantilla
        template_result = load_template.invoke({"template_name": document_type})
        if not template_result.get("success"):
            return {
                "success": False,
                "error": template_result.get("error", "Error cargando plantilla"),
            }

        # Verificar campos requeridos
        required_fields = template_result.get("required_fields", [])
        missing_fields = []
        for field in required_fields:
            if field["name"] not in data:
                missing_fields.append(field)

        if missing_fields:
            return {
                "success": False,
                "error": "Faltan campos requeridos",
                "missing_fields": missing_fields,
            }

        # Llenar la plantilla
        fill_result = fill_template.invoke({
            "template_name": document_type,
            "data": data,
        })

        if not fill_result.get("success"):
            return fill_result

        result = {
            "success": True,
            "document_type": document_type,
            "content": fill_result.get("content"),
            "generated_at": fill_result.get("generated_at"),
        }

        # Generar PDF si se solicita
        if generate_pdf:
            from agents.tools.document_tools import generate_pdf as gen_pdf
            pdf_result = gen_pdf.invoke({
                "content": fill_result["content"],
                "filename": f"{document_type}_{data.get('trabajador_rut', 'documento')}",
                "title": f"Documento Legal - {document_type.replace('_', ' ').title()}",
            })

            if pdf_result.get("success"):
                result["pdf_path"] = pdf_result.get("pdf_path")
                result["pdf_filename"] = pdf_result.get("filename")

        return result


async def run_document_generation(query: str) -> Dict[str, Any]:
    """
    Función auxiliar para ejecutar una solicitud de documento.

    Args:
        query: La solicitud del usuario

    Returns:
        Dict con la respuesta y metadata
    """
    agent = DocumentAgent()
    return await agent.run(query)
