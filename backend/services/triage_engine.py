"""
LEIA - Motor de Triage y Anti-Alucinación

Este módulo implementa las reglas para:
1. Detectar cuándo NO hay información suficiente en los apuntes
2. Detectar cuándo se debe derivar a un abogado
3. Generar respuestas honestas sin alucinaciones
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any
import re


class TriageDecision(Enum):
    """Decisiones posibles del triage"""
    RESPOND_WITH_SOURCES = "respond_with_sources"  # Hay info, responder con citas
    NO_INFO_AVAILABLE = "no_info_available"        # No hay info, ser honesto
    REQUIRES_LAWYER = "requires_lawyer"            # Requiere derivación
    URGENT_MATTER = "urgent_matter"                # Urgente, derivar YA
    SENSITIVE_TOPIC = "sensitive_topic"            # Tema sensible, sugerir abogado


@dataclass
class TriageResult:
    """Resultado del análisis de triage"""
    decision: TriageDecision
    confidence: float  # 0-1
    reason: str
    suggested_response: Optional[str] = None
    suggested_specialties: List[str] = None
    sources_found: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.suggested_specialties is None:
            self.suggested_specialties = []
        if self.sources_found is None:
            self.sources_found = []


class TriageEngine:
    """
    Motor de triage para LEIA.

    Reglas fundamentales:
    1. NUNCA inventar información
    2. SIEMPRE citar fuentes cuando existan
    3. SIEMPRE admitir cuando NO hay información
    4. SIEMPRE derivar casos urgentes/sensibles
    """

    # Umbral de similitud para considerar que hay información relevante
    SIMILARITY_THRESHOLD = 0.75

    # Umbral mínimo para considerar que la info es "suficiente"
    MIN_SOURCES_FOR_CONFIDENCE = 2

    # Palabras clave que indican urgencia
    URGENT_KEYWORDS = [
        "urgente", "emergencia", "inmediato", "ahora mismo",
        "hoy", "mañana", "plazo vence", "audiencia",
        "detención", "detenido", "arrestado", "cárcel",
        "violencia", "golpes", "amenaza", "peligro",
        "desahucio", "desalojo", "lanzamiento",
        "embargo", "remate", "subasta"
    ]

    # Temas que SIEMPRE requieren abogado
    SENSITIVE_TOPICS = [
        # Penal
        "delito", "crimen", "imputado", "acusado", "querella criminal",
        "violación", "abuso", "homicidio", "robo", "hurto",
        # Familia sensible
        "violencia intrafamiliar", "vif", "maltrato", "abuso infantil",
        "sustracción de menor", "custodia urgente",
        # Laboral grave
        "acoso laboral", "acoso sexual", "discriminación",
        # Otros
        "quiebra", "insolvencia", "concurso",
        "representación legal", "ir a juicio", "apelar"
    ]

    # Frases que indican que el usuario pide asesoría formal
    ADVICE_REQUEST_PATTERNS = [
        r"qué (debo|debería|tengo que) hacer",
        r"cómo (demando|denuncio|me defiendo)",
        r"puedo demandar",
        r"necesito un abogado",
        r"quiero (demandar|denunciar|apelar)",
        r"represéntame",
        r"asesórame",
        r"qué me recomiendas hacer"
    ]

    # Respuestas predefinidas para casos sin información
    NO_INFO_RESPONSES = {
        "default": """No tengo información sobre este tema en mis apuntes.

Esto no significa que tu consulta no tenga solución - simplemente no cuento con material de estudio que cubra este caso específico.

Te recomiendo:
1. Consultar directamente con un abogado especializado
2. Revisar fuentes oficiales como la Biblioteca del Congreso Nacional (bcn.cl)

¿Te gustaría que te conecte con un abogado verificado?""",

        "partial": """Encontré información parcial sobre tu consulta, pero no es suficiente para darte una respuesta completa.

{partial_info}

Para una respuesta más precisa sobre tu caso específico, te recomiendo consultar con un abogado.

¿Te gustaría ver abogados especializados en {specialty}?"""
    }

    def __init__(self):
        pass

    def analyze(
        self,
        user_query: str,
        rag_results: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> TriageResult:
        """
        Analiza la consulta del usuario y los resultados RAG
        para decidir cómo responder.

        Args:
            user_query: Pregunta del usuario
            rag_results: Resultados de la búsqueda RAG (con scores)
            conversation_history: Historial de la conversación

        Returns:
            TriageResult con la decisión y sugerencias
        """
        query_lower = user_query.lower()

        # 1. Detectar si es un tema urgente
        if self._is_urgent(query_lower):
            return TriageResult(
                decision=TriageDecision.URGENT_MATTER,
                confidence=0.95,
                reason="Detecté palabras clave de urgencia en tu consulta",
                suggested_response=self._get_urgent_response(query_lower),
                suggested_specialties=self._detect_specialties(query_lower)
            )

        # 2. Detectar si es un tema sensible que requiere abogado
        if self._is_sensitive(query_lower):
            return TriageResult(
                decision=TriageDecision.SENSITIVE_TOPIC,
                confidence=0.90,
                reason="Este tema requiere asesoría legal profesional",
                suggested_response=self._get_sensitive_response(query_lower),
                suggested_specialties=self._detect_specialties(query_lower)
            )

        # 3. Detectar si el usuario pide asesoría formal
        if self._requests_formal_advice(query_lower):
            return TriageResult(
                decision=TriageDecision.REQUIRES_LAWYER,
                confidence=0.85,
                reason="Detecté que necesitas asesoría legal formal",
                suggested_response=self._get_lawyer_suggestion_response(),
                suggested_specialties=self._detect_specialties(query_lower)
            )

        # 4. Evaluar resultados RAG
        return self._evaluate_rag_results(user_query, rag_results)

    def _is_urgent(self, query: str) -> bool:
        """Detecta si la consulta es urgente"""
        return any(kw in query for kw in self.URGENT_KEYWORDS)

    def _is_sensitive(self, query: str) -> bool:
        """Detecta si el tema es sensible"""
        return any(topic in query for topic in self.SENSITIVE_TOPICS)

    def _requests_formal_advice(self, query: str) -> bool:
        """Detecta si el usuario pide asesoría formal"""
        return any(
            re.search(pattern, query)
            for pattern in self.ADVICE_REQUEST_PATTERNS
        )

    def _evaluate_rag_results(
        self,
        query: str,
        rag_results: List[Dict[str, Any]]
    ) -> TriageResult:
        """
        Evalúa los resultados RAG para decidir si hay suficiente información.
        """
        if not rag_results:
            return TriageResult(
                decision=TriageDecision.NO_INFO_AVAILABLE,
                confidence=1.0,
                reason="No encontré información relevante en mis apuntes",
                suggested_response=self.NO_INFO_RESPONSES["default"],
                suggested_specialties=self._detect_specialties(query.lower())
            )

        # Filtrar por umbral de similitud
        relevant_results = [
            r for r in rag_results
            if r.get("score", 0) >= self.SIMILARITY_THRESHOLD
        ]

        if not relevant_results:
            # Hay resultados pero ninguno pasa el umbral
            best_score = max(r.get("score", 0) for r in rag_results)

            if best_score >= 0.5:  # Información parcial
                return TriageResult(
                    decision=TriageDecision.NO_INFO_AVAILABLE,
                    confidence=0.7,
                    reason=f"La información encontrada es parcial (similitud: {best_score:.0%})",
                    suggested_response=self._get_partial_info_response(rag_results[0]),
                    sources_found=rag_results[:1],
                    suggested_specialties=self._detect_specialties(query.lower())
                )
            else:
                return TriageResult(
                    decision=TriageDecision.NO_INFO_AVAILABLE,
                    confidence=1.0,
                    reason="No encontré información relevante en mis apuntes",
                    suggested_response=self.NO_INFO_RESPONSES["default"],
                    suggested_specialties=self._detect_specialties(query.lower())
                )

        # Hay información relevante
        confidence = min(relevant_results[0].get("score", 0.75), 0.95)

        return TriageResult(
            decision=TriageDecision.RESPOND_WITH_SOURCES,
            confidence=confidence,
            reason=f"Encontré {len(relevant_results)} fuente(s) relevante(s)",
            sources_found=relevant_results,
            suggested_specialties=self._detect_specialties(query.lower())
        )

    def _detect_specialties(self, query: str) -> List[str]:
        """Detecta especialidades legales relevantes para la consulta"""
        specialties = []

        specialty_keywords = {
            "Derecho Laboral": [
                "trabajo", "laboral", "despid", "finiquito", "sueldo",
                "contrato de trabajo", "empleador", "trabajador", "indemniza",
                "vacaciones", "horas extra", "sindicato", "patron", "jefe",
                "desvincula", "echaron", "botaron", "renunci", "liquidacion",
                "afp", "isapre", "prevision", "cotizacion"
            ],
            "Derecho de Familia": [
                "divorcio", "pensión", "pension", "alimento", "custodia", "visita",
                "matrimonio", "separación", "separacion", "hijo", "padre", "madre",
                "tuición", "tuicion", "cuidado personal", "relación directa",
                "relacion directa", "familia", "pareja", "conviviente", "manutención",
                "manutencion", "ex esposa", "ex esposo", "ex marido", "ex mujer"
            ],
            "Derecho Civil": [
                "contrato", "arriend", "deuda", "cobro", "debo", "pagar",
                "garantía", "garantia", "propiedad", "inmueble", "herencia",
                "sucesión", "sucesion", "casa", "departamento", "hipoteca",
                "prestamo", "préstamo", "moroso", "dicom"
            ],
            "Derecho Penal": [
                "delito", "denuncia", "querella", "imputado", "fiscal",
                "defensor", "penal", "crimen", "robo", "hurto", "estafa",
                "golpe", "amenaza", "carcel", "cárcel", "preso", "detenido"
            ],
            "Derecho del Consumidor": [
                "sernac", "consumidor", "garantía", "garantia", "reclamo",
                "producto", "servicio", "devolución", "devolucion",
                "publicidad engañosa", "tienda", "compra", "vendedor"
            ]
        }

        for specialty, keywords in specialty_keywords.items():
            if any(kw in query for kw in keywords):
                specialties.append(specialty)

        return specialties if specialties else ["Derecho General"]

    def _get_urgent_response(self, query: str) -> str:
        """Genera respuesta para casos urgentes"""
        specialties = self._detect_specialties(query)
        specialty_text = specialties[0] if specialties else "tu caso"

        return f"""Entiendo que tu situación es urgente.

Dada la naturaleza de tu consulta, te recomiendo contactar inmediatamente con un abogado especializado en {specialty_text}.

En LEIA tenemos abogados verificados disponibles que pueden atenderte hoy.

¿Te muestro los abogados disponibles ahora?"""

    def _get_sensitive_response(self, query: str) -> str:
        """Genera respuesta para temas sensibles"""
        specialties = self._detect_specialties(query)

        return f"""Este tipo de consulta requiere la atención de un profesional del derecho.

Por la naturaleza del tema, no sería responsable de mi parte darte orientación general - necesitas asesoría legal especializada.

Puedo conectarte con abogados verificados especializados en {', '.join(specialties)}.

¿Te gustaría ver las opciones disponibles?"""

    def _get_lawyer_suggestion_response(self) -> str:
        """Respuesta cuando el usuario pide asesoría formal"""
        return """Entiendo que necesitas asesoría legal profesional.

LEIA es una herramienta de orientación, pero para casos que requieren acción legal, lo mejor es hablar con un abogado.

Puedo ayudarte a encontrar el abogado adecuado según:
- Tu ubicación
- El área legal de tu caso
- Tu presupuesto

¿Te muestro abogados verificados que pueden ayudarte?"""

    def _get_partial_info_response(self, best_result: Dict[str, Any]) -> str:
        """Respuesta cuando hay información parcial"""
        source = best_result.get("metadata", {}).get("source", "mis apuntes")
        return f"""Encontré información relacionada pero no es suficiente para responder completamente.

La fuente más cercana es: {source}

Para una respuesta precisa sobre tu caso específico, te sugiero consultar con un abogado.

¿Te gustaría ver abogados especializados?"""

    def format_sources_for_response(
        self,
        sources: List[Dict[str, Any]]
    ) -> str:
        """
        Formatea las fuentes encontradas para incluir en la respuesta.
        """
        if not sources:
            return ""

        formatted = "\n\n---\n**Fuentes consultadas:**\n"

        for i, source in enumerate(sources, 1):
            metadata = source.get("metadata", {})
            source_name = metadata.get("source", "Apunte sin título")
            section = metadata.get("section", "")
            page = metadata.get("page", "")

            formatted += f"\n{i}. {source_name}"
            if section:
                formatted += f" - {section}"
            if page:
                formatted += f" (pág. {page})"

        return formatted


# Singleton para uso global
_triage_engine = None

def get_triage_engine() -> TriageEngine:
    """Obtiene la instancia del motor de triage"""
    global _triage_engine
    if _triage_engine is None:
        _triage_engine = TriageEngine()
    return _triage_engine
