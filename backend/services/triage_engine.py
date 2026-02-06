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
    DIRECT_LAWYER_REQUEST = "direct_lawyer_request"  # Usuario pide abogado directamente, responder breve


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

    # Frases que indican solicitud DIRECTA de abogado (respuesta breve + botón)
    DIRECT_LAWYER_REQUEST_PATTERNS = [
        r"^s[ií]$",  # Solo "sí" o "si"
        r"^s[ií],?\s*(por favor|porfavor)?$",  # "sí, por favor"
        r"^dale$",
        r"^ok(ay)?$",
        r"^claro$",
        r"^bueno$",
        r"^ya$",
        r"^listo$",
        # Patrones con "sí/si" + solicitud de abogado
        r"s[ií],?\s*(quiero|dame|necesito|busco)",
        r"s[ií],?\s*conect[ae]me",
        r"s[ií],?\s*me interesa",
        # Solicitudes directas de abogado (pueden aparecer en cualquier parte)
        r"dame (un )?abogado",
        r"deme (un )?abogado",
        r"puedes darme (un )?abogado",
        r"puede darme (un )?abogado",
        r"pásame (un )?abogado",
        r"pasame (un )?abogado",
        r"conéctame con (un )?abogado",
        r"conectame con (un )?abogado",
        r"muéstrame (los )?abogados",
        r"muestrame (los )?abogados",
        r"ver (los )?abogados",
        r"quiero ver (los )?abogados",
        r"quiero (un )?abogado",
        r"necesito (un )?abogado",
        r"busco (un )?abogado",
        # Confirmaciones después de oferta
        r"me interesa",
        r"conéctame",
        r"conectame",
        r"derívame",
        r"derivame",
    ]

    # Frases que indican que el usuario pide asesoría formal (requiere orientación primero)
    ADVICE_REQUEST_PATTERNS = [
        r"qué (debo|debería|tengo que) hacer",
        r"cómo (demando|denuncio|me defiendo)",
        r"puedo demandar",
        r"quiero (demandar|denunciar|apelar)",
        r"quiero (contactar|hablar|consultar).*abogado",
        r"contactar(me)? con (un )?abogado",
        r"hablar con (un )?abogado",
        r"represéntame",
        r"asesórame",
        r"qué me recomiendas hacer"
    ]

    # Problemas legales concretos que sugieren necesidad de abogado
    CONCRETE_LEGAL_PROBLEMS = [
        # Arriendos y propiedades
        r"problema(s)? (con|de|del) (el |mi |un )?arriend",
        r"no me paga(n)?", r"no paga(n)? (el |la |los |las )?arriendo",
        r"deb(e|en) (plata|dinero|meses)", r"moroso", r"meses de arriendo",
        r"no devuelve(n)? (la )?garantía", r"no devuelve(n)? el mes",
        r"quiere(n)? echar(me|nos)?", r"me quiere(n)? sacar",
        r"terminó el contrato", r"venció el contrato",
        r"arrendatario", r"arrendador",
        # Laboral
        r"no me paga(n)?( el)? sueldo", r"me deben (sueldo|plata|dinero)",
        r"me despidieron", r"me echaron", r"me botaron",
        r"no me dieron finiquito", r"finiquito (mal|incorrecto)",
        r"horas extra no pagadas",
        # Familia
        r"no paga(n)? (la )?pensión", r"no paga(n)? alimentos",
        r"no cumple(n)? (con )?visitas", r"no deja(n)? ver",
        r"se llevó a (mi |los )?hijo",
        # Deudas
        r"me demandaron", r"me llegó (una )?demanda",
        r"me van a embargar", r"me embargaron",
        r"no puedo pagar", r"deuda impagable",
        # General
        r"incumpl(ió|ieron|e|en)", r"no cumpl(ió|ieron|e|en)",
        r"estafa(ron|do)?", r"me engaña(ron)?", r"fraude"
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
        query_lower = user_query.lower().strip()

        # 0. PRIMERO: Detectar solicitud DIRECTA de abogado (respuesta breve + botón)
        # Esto tiene prioridad porque el usuario ya decidió que quiere un abogado
        if self._is_direct_lawyer_request(query_lower, conversation_history):
            # Detectar especialidades del historial si el mensaje es muy corto
            specialties = self._detect_specialties_from_history(query_lower, conversation_history)
            return TriageResult(
                decision=TriageDecision.DIRECT_LAWYER_REQUEST,
                confidence=0.95,
                reason="Usuario solicitó abogado directamente",
                suggested_response=self._get_direct_lawyer_response(specialties),
                suggested_specialties=specialties
            )

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

        # 4. Detectar problemas legales concretos (no me pagan, me despidieron, etc.)
        if self._has_concrete_legal_problem(query_lower):
            specialties = self._detect_specialties(query_lower)
            return TriageResult(
                decision=TriageDecision.REQUIRES_LAWYER,
                confidence=0.80,
                reason="Detecté un problema legal concreto que puede requerir asistencia profesional",
                suggested_response=self._get_concrete_problem_response(specialties),
                suggested_specialties=specialties
            )

        # 5. Evaluar resultados RAG
        return self._evaluate_rag_results(user_query, rag_results)

    def _is_direct_lawyer_request(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> bool:
        """
        Detecta si el usuario está pidiendo directamente un abogado.
        Esto incluye respuestas cortas afirmativas cuando ya se ofreció un abogado.
        """
        # Verificar patrones directos
        for pattern in self.DIRECT_LAWYER_REQUEST_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True

        # Si el mensaje es muy corto y afirmativo, verificar si en el historial
        # LEIA ya ofreció conectar con un abogado
        short_affirmatives = ["sí", "si", "dale", "ok", "okay", "claro", "bueno", "ya", "listo", "porfa", "por favor"]
        if query.lower().strip().rstrip(".,!") in short_affirmatives and conversation_history:
            # Buscar en los últimos mensajes de LEIA si ofreció abogado
            for msg in reversed(conversation_history[-4:]):  # Últimos 4 mensajes
                if msg.get("role") == "assistant":
                    content_lower = msg.get("content", "").lower()
                    if any(phrase in content_lower for phrase in [
                        "conectarte con un abogado",
                        "abogado de leia",
                        "abogados de leia",
                        "te muestro abogados",
                        "ver abogados",
                        "te conecto con",
                        "derivación",
                        "especialista en"
                    ]):
                        return True

        return False

    def _detect_specialties_from_history(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> List[str]:
        """
        Detecta especialidades combinando el query actual y el historial.
        Útil cuando el mensaje actual es muy corto (ej: "sí").
        """
        # Primero intentar detectar del query actual
        specialties = self._detect_specialties(query)

        # Si no encontró nada específico y hay historial
        if specialties == ["Civil y Contratos"] and conversation_history:
            # Buscar primero en la última respuesta de LEIA si mencionó una especialidad
            specialty_mentions = {
                "Penal": ["derecho penal", "penalista", "delito", "lesiones", "querella criminal"],
                "Laboral": ["derecho laboral", "laboralista", "despido", "finiquito"],
                "Familia": ["derecho de familia", "familiarista", "pensión alimenticia", "divorcio", "custodia"],
                "Seguros": ["derecho de seguros", "seguro", "póliza", "siniestro", "aseguradora"],
                "Civil y Contratos": ["derecho civil", "civilista", "contrato"],
                "Consumidor": ["derecho del consumidor", "consumidor", "sernac"],
                "Arriendos": ["arriendos", "arrendamiento", "desahucio"],
                "Deudas y Cobranza": ["deudas", "cobranza", "embargo"],
                "Migración": ["migración", "extranjería", "visa"],
                "Herencias": ["herencias", "sucesión", "testamento"],
            }

            # Revisar las últimas respuestas de LEIA
            for msg in reversed(conversation_history[-4:]):
                if msg.get("role") == "assistant":
                    content_lower = msg.get("content", "").lower()
                    for specialty, keywords in specialty_mentions.items():
                        if any(kw in content_lower for kw in keywords):
                            return [specialty]

            # Si no encontró en LEIA, buscar en mensajes del usuario
            all_user_text = " ".join([
                msg.get("content", "")
                for msg in conversation_history
                if msg.get("role") == "user"
            ])
            specialties = self._detect_specialties(all_user_text.lower())

        return specialties

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

    def _has_concrete_legal_problem(self, query: str) -> bool:
        """Detecta si hay un problema legal concreto que amerita abogado"""
        return any(
            re.search(pattern, query, re.IGNORECASE)
            for pattern in self.CONCRETE_LEGAL_PROBLEMS
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

        # Mapeo de categorías con palabras clave expandidas
        specialty_keywords = {
            "Laboral": [
                "trabajo", "laboral", "despid", "finiquito", "sueldo",
                "contrato de trabajo", "empleador", "trabajador", "indemniza",
                "vacaciones", "horas extra", "sindicato", "patron", "jefe",
                "desvincula", "echaron", "botaron", "renunci", "liquidacion",
                "afp", "isapre", "prevision", "cotizacion", "tutela",
                "autodespido", "nulidad del despido", "accidente laboral"
            ],
            "Familia": [
                "divorcio", "pensión", "pension", "alimento", "custodia", "visita",
                "matrimonio", "separación", "separacion", "hijo", "padre", "madre",
                "tuición", "tuicion", "cuidado personal", "relación directa",
                "relacion directa", "familia", "pareja", "conviviente", "manutención",
                "manutencion", "ex esposa", "ex esposo", "ex marido", "ex mujer",
                "violencia intrafamiliar", "vif", "adopcion", "adopción"
            ],
            "Civil y Contratos": [
                "contrato", "incumplimiento", "indemnización", "perjuicio",
                "responsabilidad civil", "promesa", "compraventa"
            ],
            "Arriendos": [
                "arriend", "desahucio", "garantía", "garantia", "departamento",
                "casa", "inmueble", "propiedad", "copropiedad", "gastos comunes",
                "administración", "condominio", "corredora"
            ],
            "Deudas y Cobranza": [
                "deuda", "cobro", "pagare", "pagaré", "cheque", "letra",
                "embargo", "dicom", "prescripción", "prescripcion", "moroso",
                "cobranza", "ejecutivo", "retención", "retencion"
            ],
            "Consumidor": [
                "sernac", "consumidor", "garantía legal", "reclamo",
                "producto", "servicio", "devolución", "devolucion",
                "publicidad engañosa", "tienda", "compra", "vendedor",
                "retracto", "falabella", "ripley", "paris", "lider",
                "telecomunicacion", "pasaje", "aerolínea", "aerolinea"
            ],
            "Penal": [
                "delito", "denuncia", "querella", "imputado", "fiscal",
                "defensor", "penal", "crimen", "robo", "hurto", "estafa",
                "golpe", "amenaza", "carcel", "cárcel", "preso", "detenido",
                "citación", "citacion"
            ],
            "Migración": [
                "visa", "extranjería", "extranjeria", "migración", "migracion",
                "permanencia", "prórroga", "prorroga", "rechazo", "deportación",
                "deportacion", "residencia", "pdi", "extranjero"
            ],
            "Tributario": [
                "sii", "impuesto", "tributario", "iva", "boleta", "factura",
                "fiscalización", "fiscalizacion", "liquidación", "liquidacion",
                "giro", "tta", "renta"
            ],
            "Herencias": [
                "herencia", "testamento", "posesión efectiva", "posesion efectiva",
                "heredero", "sucesión", "sucesion", "partición", "particion",
                "fallecido", "bienes"
            ],
            "Bancario": [
                "banco", "crédito", "credito", "préstamo", "prestamo",
                "hipoteca", "tarjeta", "fraude", "clonación", "clonacion",
                "transferencia", "cuenta"
            ],
            "Seguros": [
                "seguro", "póliza", "poliza", "siniestro", "cobertura",
                "aseguradora", "peritaje"
            ]
        }

        for specialty, keywords in specialty_keywords.items():
            if any(kw in query for kw in keywords):
                specialties.append(specialty)

        return specialties if specialties else ["Civil y Contratos"]

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

    def _get_direct_lawyer_response(self, specialties: List[str]) -> str:
        """
        Respuesta BREVE cuando el usuario pide directamente un abogado.
        El botón de "Ver abogados" se mostrará automáticamente.
        """
        specialty = specialties[0] if specialties else "tu caso"
        return f"Perfecto, te conecto con abogados especializados en {specialty}."

    def _get_lawyer_suggestion_response(self) -> str:
        """Respuesta cuando el usuario pide asesoría formal"""
        return """Entiendo que necesitas asesoría legal profesional.

LEIA es una herramienta de orientación, pero para casos que requieren acción legal, lo mejor es hablar con un abogado.

Puedo ayudarte a encontrar el abogado adecuado según:
- Tu ubicación
- El área legal de tu caso
- Tu presupuesto

¿Te muestro abogados verificados que pueden ayudarte?"""

    def _get_concrete_problem_response(self, specialties: List[str]) -> str:
        """Respuesta cuando hay un problema legal concreto"""
        specialty = specialties[0] if specialties else "tu caso"
        return f"""Entiendo tu situación. Este tipo de problema puede tener solución legal.

Te he dado orientación general, pero para tomar acciones concretas (como enviar una carta, iniciar un procedimiento o demandar), es recomendable que un abogado especialista en {specialty} revise tu caso específico.

Puedo conectarte con abogados verificados de LEIA que se especializan en este tipo de casos."""

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
