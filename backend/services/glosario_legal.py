"""
Glosario Legal de Chile.
Basado en el glosario oficial del Poder Judicial de Chile.

Este módulo proporciona definiciones de términos legales para que
LEIA pueda explicar conceptos jurídicos a los usuarios.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import re


# ==================== DATACLASS ====================

@dataclass
class TerminoLegal:
    """Representa un término del glosario legal."""
    termino: str
    definicion: str
    categoria: Optional[str] = None
    sinonimos: Optional[List[str]] = None
    ejemplos: Optional[List[str]] = None


# ==================== SIGLAS Y ABREVIATURAS ====================

SIGLAS: Dict[str, str] = {
    "RIT": "Rol Interno del Tribunal. Número único asignado a cada causa dentro de un tribunal específico. Formato típico: C-1234-2024 (Tipo-Número-Año).",
    "ROL": "Número de identificación de una causa. Puede referirse al RIT o al ROL de la causa ante tribunales superiores.",
    "RUC": "Rol Único de Causa. Identificador único nacional para causas penales que permite seguir el caso a través de todo el sistema judicial.",
    "RUN": "Rol Único Nacional. Número de identificación de las personas naturales en Chile (equivalente al RUT para personas).",
    "RUT": "Rol Único Tributario. Número de identificación tributaria en Chile.",
    "MP": "Ministerio Público. Organismo autónomo encargado de dirigir la investigación de los delitos y ejercer la acción penal pública.",
    "TOP": "Tribunal Oral en lo Penal. Tribunal colegiado que conoce el juicio oral en materia penal.",
    "JG": "Juzgado de Garantía. Tribunal unipersonal que controla la investigación y protege los derechos del imputado.",
    "CA": "Corte de Apelaciones. Tribunal superior que conoce recursos contra resoluciones de tribunales inferiores.",
    "CS": "Corte Suprema. Máximo tribunal del país.",
    "DPP": "Defensoría Penal Pública. Servicio que proporciona defensa penal gratuita a quienes no pueden costearla.",
    "CAJ": "Corporación de Asistencia Judicial. Organismo que brinda asistencia jurídica gratuita en materias no penales.",
    "SML": "Servicio Médico Legal. Organismo auxiliar de la administración de justicia.",
    "PDI": "Policía de Investigaciones de Chile.",
    "VIF": "Violencia Intrafamiliar.",
    "RAF": "Registro de Alimentarios. Sistema donde se inscriben las personas que adeudan pensiones de alimentos.",
    "LBPA": "Ley de Bases de los Procedimientos Administrativos.",
    "CPP": "Código Procesal Penal.",
    "CPC": "Código de Procedimiento Civil.",
    "CT": "Código del Trabajo.",
    "CC": "Código Civil.",
    "CP": "Código Penal.",
}


# ==================== GLOSARIO PRINCIPAL ====================

GLOSARIO: Dict[str, TerminoLegal] = {
    # === A ===
    "abandono del procedimiento": TerminoLegal(
        termino="Abandono del Procedimiento",
        definicion="Sanción procesal que pone término al juicio cuando el demandante no realiza actuaciones durante un tiempo determinado (generalmente 6 meses). El juicio termina, pero el demandante puede iniciar una nueva demanda.",
        categoria="Procesal Civil"
    ),
    "acción": TerminoLegal(
        termino="Acción",
        definicion="Derecho de toda persona de acudir a los tribunales para hacer valer una pretensión. Es el mecanismo para poner en movimiento la actividad jurisdiccional.",
        categoria="General"
    ),
    "acta": TerminoLegal(
        termino="Acta",
        definicion="Documento oficial que da cuenta de lo ocurrido en una actuación judicial, audiencia o diligencia. Debe ser firmada por los intervinientes.",
        categoria="General"
    ),
    "actuación judicial": TerminoLegal(
        termino="Actuación Judicial",
        definicion="Cualquier actividad que realiza el tribunal en el ejercicio de sus funciones: resoluciones, audiencias, notificaciones, etc.",
        categoria="General"
    ),
    "acuerdo": TerminoLegal(
        termino="Acuerdo",
        definicion="Convenio entre las partes para resolver un conflicto. También se refiere al proceso de deliberación de un tribunal colegiado para dictar sentencia.",
        categoria="General"
    ),
    "acusación": TerminoLegal(
        termino="Acusación",
        definicion="Acto procesal mediante el cual el Ministerio Público o el querellante formulan cargos formales contra el imputado, solicitando que sea llevado a juicio oral.",
        categoria="Penal"
    ),
    "alegato": TerminoLegal(
        termino="Alegato",
        definicion="Exposición oral que realizan los abogados ante el tribunal para defender los intereses de su parte. En tribunales superiores, los alegatos se realizan en audiencias públicas.",
        categoria="General"
    ),
    "alimentos": TerminoLegal(
        termino="Alimentos",
        definicion="Prestación económica que una persona debe dar a otra para su subsistencia. Incluye comida, habitación, vestuario, salud, educación y recreación. Se deben a los hijos, cónyuge, padres y otros familiares según la ley.",
        categoria="Familia",
        ejemplos=["Pensión de alimentos para hijos menores", "Alimentos para cónyuge"]
    ),
    "apelación": TerminoLegal(
        termino="Apelación",
        definicion="Recurso procesal que permite a la parte agraviada solicitar a un tribunal superior que revise y modifique una resolución del tribunal inferior. Es el recurso más común.",
        categoria="Recursos",
        sinonimos=["Recurso de apelación"]
    ),
    "apercibimiento": TerminoLegal(
        termino="Apercibimiento",
        definicion="Advertencia que hace el tribunal sobre las consecuencias negativas que tendrá para una parte si no cumple con una orden o requerimiento judicial.",
        categoria="General"
    ),
    "árbitro": TerminoLegal(
        termino="Árbitro",
        definicion="Juez privado designado por las partes o por la justicia para resolver un conflicto específico. Existen árbitros de derecho, arbitradores y mixtos.",
        categoria="General"
    ),
    "arraigo": TerminoLegal(
        termino="Arraigo",
        definicion="Medida cautelar que prohíbe a una persona salir del país mientras dura un proceso judicial.",
        categoria="Cautelares"
    ),
    "arresto": TerminoLegal(
        termino="Arresto",
        definicion="Medida de apremio que consiste en privar de libertad a una persona por un tiempo breve, generalmente para obligarla a cumplir una resolución judicial.",
        categoria="General"
    ),
    "audiencia": TerminoLegal(
        termino="Audiencia",
        definicion="Sesión en que el tribunal escucha a las partes y sus abogados. Puede ser pública o privada, y en ella se rinden pruebas, se dictan resoluciones o se realizan alegatos.",
        categoria="General"
    ),
    "auto": TerminoLegal(
        termino="Auto",
        definicion="Resolución judicial que resuelve incidentes o cuestiones accesorias del proceso que requieren fundamentación, pero no son sentencias definitivas.",
        categoria="Resoluciones"
    ),
    "avenimiento": TerminoLegal(
        termino="Avenimiento",
        definicion="Acuerdo alcanzado directamente entre las partes de un juicio, que pone fin al conflicto. Debe ser aprobado por el tribunal y tiene valor de sentencia ejecutoriada.",
        categoria="Términos del proceso"
    ),

    # === C ===
    "carátula": TerminoLegal(
        termino="Carátula",
        definicion="Nombre con que se identifica una causa judicial, generalmente usando los apellidos de las partes (ej: 'Pérez con González'). También se llama caratulado.",
        categoria="General",
        sinonimos=["Caratulado"]
    ),
    "casación": TerminoLegal(
        termino="Casación",
        definicion="Recurso extraordinario ante la Corte Suprema para anular sentencias que contengan errores de derecho (casación en el fondo) o vicios de procedimiento (casación en la forma).",
        categoria="Recursos"
    ),
    "caución": TerminoLegal(
        termino="Caución",
        definicion="Garantía que debe entregar una persona para asegurar el cumplimiento de una obligación. Puede ser real (dinero, bienes) o personal (fiador).",
        categoria="Garantías"
    ),
    "comparecencia": TerminoLegal(
        termino="Comparecencia",
        definicion="Acto de presentarse ante el tribunal, ya sea personalmente o representado por un abogado.",
        categoria="General"
    ),
    "conciliación": TerminoLegal(
        termino="Conciliación",
        definicion="Trámite obligatorio en muchos juicios donde el juez propone bases de acuerdo a las partes para terminar el conflicto de manera amigable.",
        categoria="General"
    ),
    "condena": TerminoLegal(
        termino="Condena",
        definicion="Decisión judicial que declara la responsabilidad de una persona y le impone una sanción o la obligación de realizar o pagar algo.",
        categoria="Sentencias"
    ),
    "contestación de la demanda": TerminoLegal(
        termino="Contestación de la Demanda",
        definicion="Escrito mediante el cual el demandado responde a la demanda, exponiendo sus defensas y excepciones. Es el acto procesal que traba la litis.",
        categoria="Procesal Civil"
    ),
    "costas": TerminoLegal(
        termino="Costas",
        definicion="Gastos del juicio que debe pagar la parte vencida, incluyendo honorarios de abogados, tasas judiciales y otros gastos procesales.",
        categoria="General"
    ),
    "curador": TerminoLegal(
        termino="Curador",
        definicion="Persona designada por el tribunal para representar y proteger los intereses de alguien que no puede hacerlo por sí mismo (incapaz, ausente, herencia yacente).",
        categoria="Familia"
    ),
    "cuidado personal": TerminoLegal(
        termino="Cuidado Personal",
        definicion="Derecho y deber de un padre o madre de tener a su hijo viviendo consigo y responsabilizarse de su crianza y educación. Antes se llamaba 'tuición'.",
        categoria="Familia",
        sinonimos=["Tuición", "Custodia"]
    ),

    # === D ===
    "decreto": TerminoLegal(
        termino="Decreto",
        definicion="Resolución judicial simple que ordena trámites necesarios para dar curso al proceso, sin resolver cuestiones debatidas entre las partes.",
        categoria="Resoluciones",
        sinonimos=["Providencia", "Proveído"]
    ),
    "demanda": TerminoLegal(
        termino="Demanda",
        definicion="Escrito mediante el cual una persona (demandante) solicita al tribunal que reconozca un derecho o condene a otra persona (demandado) a realizar o pagar algo.",
        categoria="Procesal Civil"
    ),
    "demandante": TerminoLegal(
        termino="Demandante",
        definicion="Persona que inicia un juicio civil presentando una demanda. También se le llama actor.",
        categoria="Partes",
        sinonimos=["Actor"]
    ),
    "demandado": TerminoLegal(
        termino="Demandado",
        definicion="Persona contra quien se dirige la demanda en un juicio civil.",
        categoria="Partes"
    ),
    "desistimiento": TerminoLegal(
        termino="Desistimiento",
        definicion="Acto por el cual el demandante renuncia a continuar el juicio. Si el demandado ya contestó, requiere su consentimiento. Impide iniciar un nuevo juicio por la misma causa.",
        categoria="Términos del proceso"
    ),
    "despido injustificado": TerminoLegal(
        termino="Despido Injustificado",
        definicion="Término del contrato de trabajo por decisión unilateral del empleador sin que exista una causal legal que lo justifique. Da derecho al trabajador a indemnizaciones.",
        categoria="Laboral"
    ),

    # === E ===
    "embargo": TerminoLegal(
        termino="Embargo",
        definicion="Medida judicial que afecta bienes del deudor, prohibiendo que disponga de ellos, para asegurar el pago de una deuda. Los bienes embargados pueden ser rematados.",
        categoria="Cautelares"
    ),
    "emplazamiento": TerminoLegal(
        termino="Emplazamiento",
        definicion="Acto de comunicar al demandado que se ha iniciado un juicio en su contra, dándole un plazo para defenderse.",
        categoria="Notificaciones"
    ),
    "escritura pública": TerminoLegal(
        termino="Escritura Pública",
        definicion="Documento otorgado ante notario público que da plena fe de los hechos y acuerdos que contiene. Es obligatoria para ciertos actos como compraventa de inmuebles.",
        categoria="Documentos"
    ),
    "exhorto": TerminoLegal(
        termino="Exhorto",
        definicion="Comunicación oficial entre tribunales de distinta jurisdicción para solicitar que se practique una diligencia en el territorio del tribunal requerido.",
        categoria="General"
    ),

    # === F ===
    "fianza": TerminoLegal(
        termino="Fianza",
        definicion="Garantía personal donde un tercero (fiador) se compromete a pagar una deuda si el deudor principal no lo hace.",
        categoria="Garantías"
    ),
    "fiscalía": TerminoLegal(
        termino="Fiscalía",
        definicion="Oficina del Ministerio Público donde trabajan los fiscales que investigan delitos y ejercen la acción penal.",
        categoria="Penal"
    ),
    "formalización": TerminoLegal(
        termino="Formalización",
        definicion="Acto procesal en que el fiscal comunica al imputado, en presencia del juez de garantía, que desarrolla una investigación en su contra por un delito determinado.",
        categoria="Penal"
    ),

    # === I ===
    "imputado": TerminoLegal(
        termino="Imputado",
        definicion="Persona a quien se atribuye participación en un hecho punible. Tiene derechos fundamentales como la presunción de inocencia y el derecho a defensa.",
        categoria="Penal"
    ),
    "incidente": TerminoLegal(
        termino="Incidente",
        definicion="Cuestión accesoria que se promueve durante el juicio y que requiere pronunciamiento especial del tribunal. Puede o no suspender el proceso principal.",
        categoria="Procesal"
    ),
    "indemnización": TerminoLegal(
        termino="Indemnización",
        definicion="Compensación económica que debe pagar quien ha causado un daño a otra persona. Puede ser por daño emergente, lucro cesante o daño moral.",
        categoria="General"
    ),

    # === J ===
    "juicio ejecutivo": TerminoLegal(
        termino="Juicio Ejecutivo",
        definicion="Procedimiento judicial para cobrar deudas que constan en un título ejecutivo (pagaré, cheque, sentencia, etc.). Es más rápido que el juicio ordinario.",
        categoria="Procesal Civil"
    ),
    "juicio ordinario": TerminoLegal(
        termino="Juicio Ordinario",
        definicion="Procedimiento civil de aplicación general, con etapas de discusión, prueba y sentencia. Se usa cuando la ley no señala un procedimiento especial.",
        categoria="Procesal Civil"
    ),
    "jurisdicción": TerminoLegal(
        termino="Jurisdicción",
        definicion="Potestad de los tribunales para conocer y resolver conflictos jurídicos, hacer ejecutar lo juzgado y velar por el cumplimiento de la ley.",
        categoria="General"
    ),

    # === L ===
    "legitimación": TerminoLegal(
        termino="Legitimación",
        definicion="Calidad que debe tener una persona para ser parte en un juicio específico. Implica tener un interés actual en el resultado del proceso.",
        categoria="Procesal"
    ),
    "litisconsorcio": TerminoLegal(
        termino="Litisconsorcio",
        definicion="Situación procesal en que hay pluralidad de demandantes (activo) o demandados (pasivo) en un mismo juicio.",
        categoria="Procesal"
    ),

    # === M ===
    "mandato judicial": TerminoLegal(
        termino="Mandato Judicial",
        definicion="Poder que una persona otorga a un abogado para que la represente en juicio. Debe constar por escrito y puede ser general o especial.",
        categoria="General"
    ),
    "medida cautelar": TerminoLegal(
        termino="Medida Cautelar",
        definicion="Resolución judicial que busca asegurar el resultado del juicio, impidiendo que el demandado oculte o enajene bienes. Incluye embargos, retenciones, prohibiciones.",
        categoria="Cautelares"
    ),
    "medida de protección": TerminoLegal(
        termino="Medida de Protección",
        definicion="Resolución judicial que protege a una persona en situación de riesgo, especialmente en casos de violencia intrafamiliar o vulneración de derechos de niños.",
        categoria="Familia"
    ),

    # === N ===
    "notificación": TerminoLegal(
        termino="Notificación",
        definicion="Acto mediante el cual se comunica oficialmente a las partes las resoluciones del tribunal. Puede ser personal, por cédula, por estado diario o por avisos.",
        categoria="Notificaciones"
    ),
    "nulidad": TerminoLegal(
        termino="Nulidad",
        definicion="Sanción que priva de efectos a un acto procesal que no cumple con los requisitos legales. Puede ser absoluta o relativa.",
        categoria="Procesal"
    ),

    # === P ===
    "patrocinio": TerminoLegal(
        termino="Patrocinio",
        definicion="Actuación de un abogado habilitado que asume la defensa técnica de una parte en juicio. Es obligatorio en la mayoría de los procedimientos.",
        categoria="General"
    ),
    "pensión de alimentos": TerminoLegal(
        termino="Pensión de Alimentos",
        definicion="Monto de dinero que periódicamente debe pagar el alimentante al alimentario para cubrir sus necesidades de subsistencia.",
        categoria="Familia"
    ),
    "perito": TerminoLegal(
        termino="Perito",
        definicion="Experto en una ciencia, arte o técnica que es llamado a declarar en juicio para ilustrar al tribunal sobre materias que requieren conocimientos especializados.",
        categoria="Prueba"
    ),
    "plazo": TerminoLegal(
        termino="Plazo",
        definicion="Período de tiempo fijado por la ley o el tribunal para realizar una actuación procesal. Pueden ser fatales (se extinguen por el solo transcurso) o no fatales.",
        categoria="General"
    ),
    "preclusión": TerminoLegal(
        termino="Preclusión",
        definicion="Pérdida de la facultad de realizar un acto procesal por no haberlo ejercido oportunamente o por haber realizado un acto incompatible.",
        categoria="Procesal"
    ),
    "prescripción": TerminoLegal(
        termino="Prescripción",
        definicion="Extinción de un derecho o acción por el transcurso del tiempo. Puede ser adquisitiva (se adquiere un derecho) o extintiva (se pierde un derecho).",
        categoria="General"
    ),
    "presunción de inocencia": TerminoLegal(
        termino="Presunción de Inocencia",
        definicion="Derecho fundamental que garantiza que toda persona es considerada inocente hasta que se demuestre su culpabilidad mediante sentencia condenatoria firme.",
        categoria="Penal"
    ),
    "prisión preventiva": TerminoLegal(
        termino="Prisión Preventiva",
        definicion="Medida cautelar personal que priva de libertad al imputado durante la investigación, cuando hay peligro de fuga, obstaculización de la investigación o peligro para la víctima.",
        categoria="Penal"
    ),
    "procedimiento abreviado": TerminoLegal(
        termino="Procedimiento Abreviado",
        definicion="Procedimiento penal simplificado donde el imputado acepta los hechos y la pena propuesta por el fiscal, renunciando al juicio oral.",
        categoria="Penal"
    ),
    "prueba": TerminoLegal(
        termino="Prueba",
        definicion="Medios que utilizan las partes para demostrar los hechos que fundan sus pretensiones. Incluye documentos, testigos, peritos, confesión, inspección personal.",
        categoria="Prueba"
    ),

    # === Q ===
    "querella": TerminoLegal(
        termino="Querella",
        definicion="Acción penal ejercida por la víctima o su representante para perseguir la responsabilidad del imputado. Permite participar activamente en el proceso penal.",
        categoria="Penal"
    ),

    # === R ===
    "rebeldía": TerminoLegal(
        termino="Rebeldía",
        definicion="Situación procesal del demandado que no contesta la demanda dentro del plazo legal. El juicio continúa en su ausencia.",
        categoria="Procesal"
    ),
    "recurso": TerminoLegal(
        termino="Recurso",
        definicion="Medio de impugnación que permite a las partes solicitar la revisión de una resolución judicial. Los más comunes son apelación, casación y queja.",
        categoria="Recursos"
    ),
    "recurso de protección": TerminoLegal(
        termino="Recurso de Protección",
        definicion="Acción constitucional ante la Corte de Apelaciones para restablecer el imperio del derecho cuando existe una acción u omisión arbitraria o ilegal que afecta garantías constitucionales.",
        categoria="Recursos"
    ),
    "relación directa y regular": TerminoLegal(
        termino="Relación Directa y Regular",
        definicion="Derecho del padre o madre que no tiene el cuidado personal del hijo de mantener contacto con él. Antes se llamaba 'visitas'. Incluye días, fines de semana y vacaciones.",
        categoria="Familia",
        sinonimos=["Visitas", "Régimen de visitas"]
    ),
    "remate": TerminoLegal(
        termino="Remate",
        definicion="Venta pública de bienes embargados al mejor postor, para pagar con el producto al acreedor.",
        categoria="Ejecución"
    ),
    "réplica": TerminoLegal(
        termino="Réplica",
        definicion="Escrito del demandante que responde a la contestación de la demanda, reforzando sus argumentos y contradiciendo las defensas del demandado.",
        categoria="Procesal Civil"
    ),
    "resolución": TerminoLegal(
        termino="Resolución",
        definicion="Pronunciamiento del tribunal sobre las peticiones de las partes o cuestiones del proceso. Incluye decretos, autos, sentencias interlocutorias y definitivas.",
        categoria="Resoluciones"
    ),

    # === S ===
    "sentencia": TerminoLegal(
        termino="Sentencia",
        definicion="Resolución judicial que pone fin al juicio, pronunciándose sobre las pretensiones de las partes. Puede ser condenatoria, absolutoria o declarativa.",
        categoria="Sentencias"
    ),
    "sentencia definitiva": TerminoLegal(
        termino="Sentencia Definitiva",
        definicion="Resolución que pone fin al juicio, decidiendo las cuestiones controvertidas. Una vez firme, produce efecto de cosa juzgada.",
        categoria="Sentencias"
    ),
    "sentencia ejecutoriada": TerminoLegal(
        termino="Sentencia Ejecutoriada",
        definicion="Sentencia firme contra la cual no proceden recursos, ya sea porque se agotaron o porque venció el plazo para interponerlos. Produce efecto de cosa juzgada.",
        categoria="Sentencias",
        sinonimos=["Sentencia firme"]
    ),
    "sobreseimiento": TerminoLegal(
        termino="Sobreseimiento",
        definicion="Resolución que pone término al proceso penal antes de la sentencia. Puede ser definitivo (equivale a absolución) o temporal (suspende el proceso).",
        categoria="Penal"
    ),
    "suspensión condicional": TerminoLegal(
        termino="Suspensión Condicional del Procedimiento",
        definicion="Salida alternativa en proceso penal donde el imputado acepta condiciones durante un período, tras el cual se sobresee definitivamente la causa.",
        categoria="Penal"
    ),

    # === T ===
    "tercería": TerminoLegal(
        termino="Tercería",
        definicion="Intervención de un tercero en un juicio para defender sus derechos. Puede ser de dominio, posesión, prelación o pago.",
        categoria="Procesal"
    ),
    "testigo": TerminoLegal(
        termino="Testigo",
        definicion="Persona que declara en juicio sobre hechos que conoce por haberlos presenciado o por referencia de terceros.",
        categoria="Prueba"
    ),
    "título ejecutivo": TerminoLegal(
        termino="Título Ejecutivo",
        definicion="Documento que permite iniciar directamente un juicio ejecutivo por contener una obligación líquida, actualmente exigible e indubitada (ej: pagaré, cheque, sentencia).",
        categoria="Ejecución"
    ),
    "tramitación electrónica": TerminoLegal(
        termino="Tramitación Electrónica",
        definicion="Sistema de gestión judicial donde las actuaciones se realizan digitalmente a través de la Oficina Judicial Virtual, sin necesidad de expedientes físicos.",
        categoria="General"
    ),
    "tribunal": TerminoLegal(
        termino="Tribunal",
        definicion="Órgano público encargado de ejercer la función jurisdiccional, conociendo y resolviendo conflictos conforme a derecho.",
        categoria="General"
    ),
    "tutela laboral": TerminoLegal(
        termino="Tutela Laboral",
        definicion="Procedimiento especial para proteger los derechos fundamentales de los trabajadores cuando son vulnerados por el empleador.",
        categoria="Laboral"
    ),

    # === V ===
    "víctima": TerminoLegal(
        termino="Víctima",
        definicion="Persona ofendida por el delito. Tiene derecho a ser informada, protegida, escuchada y a obtener reparación.",
        categoria="Penal"
    ),
    "violencia intrafamiliar": TerminoLegal(
        termino="Violencia Intrafamiliar",
        definicion="Maltrato que afecta la vida, integridad física o psíquica de quien tenga o haya tenido la calidad de cónyuge, conviviente o pariente.",
        categoria="Familia",
        sinonimos=["VIF"]
    ),
}


# ==================== FRASES LATINAS ====================

FRASES_LATINAS: Dict[str, str] = {
    "ad hoc": "Para este caso específico. Ej: perito ad hoc, abogado ad hoc.",
    "de facto": "De hecho, en la práctica, aunque no sea legal.",
    "de iure": "De derecho, conforme a la ley.",
    "erga omnes": "Respecto de todos, con efectos generales.",
    "ex officio": "De oficio, por iniciativa del tribunal sin petición de parte.",
    "habeas corpus": "Acción para proteger la libertad personal de quien está detenido ilegalmente.",
    "in dubio pro reo": "En caso de duda, a favor del acusado.",
    "in fraganti": "En el acto, mientras se comete el delito.",
    "inter partes": "Entre las partes, con efectos solo para quienes participaron en el juicio.",
    "ius cogens": "Derecho imperativo que no admite acuerdo en contrario.",
    "litis": "Litigio, controversia judicial.",
    "modus operandi": "Modo de operar, forma de actuar.",
    "non bis in idem": "No dos veces por lo mismo. Prohíbe juzgar dos veces por el mismo hecho.",
    "nulla poena sine lege": "No hay pena sin ley previa que la establezca.",
    "onus probandi": "Carga de la prueba. Obligación de probar los hechos alegados.",
    "prima facie": "A primera vista, según aparece inicialmente.",
    "pro bono": "Por el bien público, sin cobrar honorarios.",
    "res judicata": "Cosa juzgada. Lo decidido en sentencia firme no puede volver a discutirse.",
    "sine die": "Sin fecha determinada.",
    "ultra petita": "Más allá de lo pedido. Vicio de sentencia que otorga más de lo solicitado.",
}


# ==================== FUNCIONES DE BÚSQUEDA ====================

def buscar_termino(consulta: str) -> Optional[TerminoLegal]:
    """
    Busca un término en el glosario.

    Args:
        consulta: Término a buscar

    Returns:
        TerminoLegal si se encuentra, None si no existe
    """
    consulta_lower = consulta.lower().strip()

    # Búsqueda exacta
    if consulta_lower in GLOSARIO:
        return GLOSARIO[consulta_lower]

    # Búsqueda por sinónimos
    for termino in GLOSARIO.values():
        if termino.sinonimos:
            for sinonimo in termino.sinonimos:
                if sinonimo.lower() == consulta_lower:
                    return termino

    return None


def buscar_sigla(sigla: str) -> Optional[str]:
    """
    Busca el significado de una sigla.

    Args:
        sigla: Sigla a buscar

    Returns:
        Definición si se encuentra, None si no existe
    """
    sigla_upper = sigla.upper().strip()
    return SIGLAS.get(sigla_upper)


def buscar_frase_latina(frase: str) -> Optional[str]:
    """
    Busca el significado de una frase latina.

    Args:
        frase: Frase latina a buscar

    Returns:
        Significado si se encuentra, None si no existe
    """
    frase_lower = frase.lower().strip()
    return FRASES_LATINAS.get(frase_lower)


def buscar_en_todo(consulta: str) -> Dict[str, Any]:
    """
    Busca en todo el glosario (términos, siglas, frases latinas).

    Args:
        consulta: Texto a buscar

    Returns:
        Dict con resultados encontrados
    """
    resultado = {
        "consulta": consulta,
        "encontrado": False,
        "tipo": None,
        "definicion": None,
        "termino_completo": None,
    }

    # Buscar en términos
    termino = buscar_termino(consulta)
    if termino:
        resultado["encontrado"] = True
        resultado["tipo"] = "termino"
        resultado["definicion"] = termino.definicion
        resultado["termino_completo"] = termino
        resultado["categoria"] = termino.categoria
        return resultado

    # Buscar en siglas
    sigla_def = buscar_sigla(consulta)
    if sigla_def:
        resultado["encontrado"] = True
        resultado["tipo"] = "sigla"
        resultado["definicion"] = sigla_def
        return resultado

    # Buscar en frases latinas
    latina_def = buscar_frase_latina(consulta)
    if latina_def:
        resultado["encontrado"] = True
        resultado["tipo"] = "frase_latina"
        resultado["definicion"] = latina_def
        return resultado

    return resultado


def buscar_terminos_por_categoria(categoria: str) -> List[TerminoLegal]:
    """
    Obtiene todos los términos de una categoría.

    Args:
        categoria: Categoría a buscar (ej: "Familia", "Penal", "Laboral")

    Returns:
        Lista de términos de esa categoría
    """
    categoria_lower = categoria.lower()
    return [
        t for t in GLOSARIO.values()
        if t.categoria and t.categoria.lower() == categoria_lower
    ]


def obtener_todas_categorias() -> List[str]:
    """Obtiene lista de todas las categorías disponibles."""
    categorias = set()
    for termino in GLOSARIO.values():
        if termino.categoria:
            categorias.add(termino.categoria)
    return sorted(list(categorias))


def obtener_estadisticas_glosario() -> Dict[str, int]:
    """Obtiene estadísticas del glosario."""
    return {
        "total_terminos": len(GLOSARIO),
        "total_siglas": len(SIGLAS),
        "total_frases_latinas": len(FRASES_LATINAS),
        "categorias": len(obtener_todas_categorias()),
    }


# ==================== FUNCIÓN PARA LEIA ====================

def explicar_para_usuario(termino: str) -> str:
    """
    Genera una explicación amigable de un término legal para el usuario.
    Diseñada para ser usada por LEIA.

    Args:
        termino: Término a explicar

    Returns:
        Explicación en lenguaje sencillo
    """
    resultado = buscar_en_todo(termino)

    if not resultado["encontrado"]:
        return f"No encontré el término '{termino}' en mi glosario legal. ¿Podrías escribirlo de otra forma o dar más contexto?"

    if resultado["tipo"] == "sigla":
        return f"**{termino.upper()}** significa: {resultado['definicion']}"

    if resultado["tipo"] == "frase_latina":
        return f"**{termino}** es una expresión latina que significa: {resultado['definicion']}"

    # Es un término completo
    termino_obj = resultado["termino_completo"]
    explicacion = f"**{termino_obj.termino}**\n\n{termino_obj.definicion}"

    if termino_obj.categoria:
        explicacion += f"\n\n📁 *Área: {termino_obj.categoria}*"

    if termino_obj.sinonimos:
        explicacion += f"\n\n🔄 *También conocido como: {', '.join(termino_obj.sinonimos)}*"

    if termino_obj.ejemplos:
        explicacion += f"\n\n📝 *Ejemplos:*\n" + "\n".join(f"- {ej}" for ej in termino_obj.ejemplos)

    return explicacion
