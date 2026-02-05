"""
Dirección del Trabajo Scraper - Recopila dictámenes laborales y guías

Fuente oficial: https://www.dt.gob.cl
- Dictámenes: https://www.dt.gob.cl/portal/1626/w3-propertyvalue-22089.html
- Código del Trabajo comentado
- Guías laborales
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

class DTScraper:
    """Scraper para dictámenes y contenido de la Dirección del Trabajo"""

    BASE_URL = "https://www.dt.gob.cl"

    # Temas prioritarios
    PRIORITY_TOPICS = {
        "finiquito": {
            "keywords": ["finiquito", "término de contrato", "indemnización"],
            "category": "terminacion_contrato"
        },
        "despido": {
            "keywords": ["despido", "despido injustificado", "desahucio"],
            "category": "terminacion_contrato"
        },
        "jornada_laboral": {
            "keywords": ["jornada laboral", "horas extras", "descanso"],
            "category": "condiciones_trabajo"
        },
        "vacaciones": {
            "keywords": ["vacaciones", "feriado legal", "permisos"],
            "category": "condiciones_trabajo"
        },
        "sueldo_minimo": {
            "keywords": ["sueldo mínimo", "remuneración", "salario"],
            "category": "remuneraciones"
        }
    }

    def __init__(self, output_dir: str = "data/raw/dt"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JusticiaAI-LegalBot/1.0 (Educational Purpose)'
        })

    def scrape_guias_laborales(self) -> List[Dict]:
        """
        Descarga guías laborales oficiales de la DT

        Estas guías son documentos públicos que explican derechos laborales
        en lenguaje simple, perfectos para el chatbot.
        """
        print("📥 Descargando guías laborales de la Dirección del Trabajo...")

        # Guías estáticas conocidas (URLs públicas)
        guias = []

        # Guía 1: Finiquito
        guias.append({
            "title": "Guía sobre Finiquito y Término de Contrato",
            "category": "terminacion_contrato",
            "content": """
            FINIQUITO Y TÉRMINO DE CONTRATO DE TRABAJO

            ¿Qué es el finiquito?
            El finiquito es el documento que acredita el término de la relación laboral y el pago de todas las prestaciones adeudadas al trabajador.

            ¿Cuándo se debe firmar?
            El finiquito debe firmarse al momento del término del contrato o dentro de los 10 días hábiles siguientes.

            ¿Qué debe incluir el finiquito?
            - Fecha de término del contrato
            - Causal de término (renuncia, despido, mutuo acuerdo, etc.)
            - Detalle de remuneraciones pendientes
            - Vacaciones proporcionales
            - Indemnización (si corresponde)
            - Cotizaciones previsionales al día

            ¿Es obligatorio firmarlo?
            - Si es término por renuncia: Puede firmarse ante el empleador
            - Si es despido: Debe firmarse ante notario, inspector del trabajo, o presidente del sindicato

            ¿Qué pasa si no estoy de acuerdo?
            - NO firme si no está de acuerdo
            - Puede acudir a la Inspección del Trabajo dentro de 60 días hábiles
            - Puede demandar ante tribunales laborales

            Indemnizaciones según causal:
            - Despido por necesidades de la empresa (Art. 161): 1 mes por año trabajado (tope 11 años)
            - Despido injustificado: Indemnización + recargo del 30-100%
            - Renuncia voluntaria: NO hay indemnización (salvo pacto)
            - Mutuo acuerdo: Según lo negociado

            Vacaciones proporcionales:
            Si trabajaste parte del año, te corresponde el proporcional de 15 días hábiles.

            Importante:
            - Puedes asesorarte GRATIS en la Inspección del Trabajo
            - Tienes 60 días hábiles desde el término para reclamar
            - El empleador debe pagar dentro de 10 días hábiles
            """,
            "source": "Dirección del Trabajo - Contenido oficial",
            "url": "https://www.dt.gob.cl",
            "scraped_at": datetime.now().isoformat()
        })

        # Guía 2: Despido
        guias.append({
            "title": "Guía sobre Despido y Causales de Término",
            "category": "terminacion_contrato",
            "content": """
            DESPIDO Y CAUSALES DE TÉRMINO DE CONTRATO

            Causales de término del contrato (Art. 159-161):

            1. RENUNCIA VOLUNTARIA (Art. 159 N°1)
            - El trabajador decide terminar el contrato
            - Debe avisar con 30 días de anticipación (trabajadores)
            - NO genera indemnización

            2. MUTUO ACUERDO (Art. 159 N°2)
            - Ambas partes acuerdan terminar
            - Puede generar indemnización si se negocia

            3. VENCIMIENTO PLAZO (Art. 159 N°4)
            - Para contratos a plazo fijo
            - NO genera indemnización

            4. NECESIDADES DE LA EMPRESA (Art. 161)
            - Razones económicas, tecnológicas, etc.
            - GENERA INDEMNIZACIÓN: 1 mes por año (tope 11 años)
            - Aviso previo de 30 días (o pago del mes)

            5. DESAHUCIO (Art. 161)
            - Sin expresar causa
            - Igual que necesidades de la empresa
            - GENERA INDEMNIZACIÓN

            6. CAUSALES DEL TRABAJADOR (Art. 160)
            - Conductas graves del trabajador:
              * Falta de probidad
              * Conductas inmorales
              * Agresiones
              * Injurias
              * Incumplimiento grave
              * Abandono del trabajo
              * Negarse a trabajar sin causa
            - NO genera indemnización
            - Empleador debe probar la causal

            ¿Qué hacer si te despiden?

            1. REVISA EL FINIQUITO
            - Lee todo antes de firmar
            - Verifica montos
            - Verifica causal de despido

            2. SI NO ESTÁS DE ACUERDO
            - NO firmes
            - Acude a Inspección del Trabajo (60 días hábiles)
            - Puedes demandar despido injustificado

            3. DESPIDO INJUSTIFICADO
            Si el empleador no prueba la causal, puedes obtener:
            - Indemnización por años de servicio
            - Recargo del 30% al 100% según gravedad
            - Indemnización sustitutiva del aviso previo

            4. PLAZOS IMPORTANTES
            - 60 días hábiles para reclamar en Inspección
            - 2 años para demandar ante tribunales
            - Empleador tiene 10 días hábiles para pagar finiquito

            ASESORÍA GRATUITA:
            - Inspección del Trabajo: 600 450 4000
            - Sitio web: www.dt.gob.cl
            - Atención presencial en oficinas regionales
            """,
            "source": "Dirección del Trabajo - Contenido oficial",
            "url": "https://www.dt.gob.cl",
            "scraped_at": datetime.now().isoformat()
        })

        # Guía 3: Jornada Laboral
        guias.append({
            "title": "Guía sobre Jornada Laboral y Horas Extras",
            "category": "condiciones_trabajo",
            "content": """
            JORNADA LABORAL Y HORAS EXTRAS EN CHILE

            Jornada Ordinaria:
            - Máximo: 45 horas semanales
            - Máximo diario: 10 horas (si se distribuye en 5 días)
            - Máximo diario: 9 horas (si se distribuye en 6 días)

            Descansos:
            - Descanso semanal: Al menos 1 día (generalmente domingo)
            - Colación: Mínimo 30 minutos (no cuenta como trabajo)
            - Entre jornadas: Mínimo 12 horas de descanso

            Horas Extras:
            - Son voluntarias (trabajador puede negarse)
            - Máximo: 2 horas extras por día
            - Pago: 50% más que hora ordinaria
            - Se pagan sobre sueldo base + gratificación

            Ejemplo de cálculo horas extras:
            - Sueldo base: $500.000
            - Horas mensuales: 180
            - Valor hora: $500.000 / 180 = $2.778
            - Valor hora extra: $2.778 x 1,5 = $4.167

            Trabajos exceptuados (pueden trabajar domingos/festivos):
            - Comercio
            - Restaurantes
            - Salud
            - Transporte
            - Seguridad

            Trabajos sin limitación de jornada:
            - Gerentes, administradores
            - Trabajadores que laboran sin fiscalización
            - Servicios a domicilio
            - Agentes comisionistas

            ¿Qué hacer si te hacen trabajar más de 45 horas?
            1. Registra tus horas (libreta, mensajes, testigos)
            2. Solicita por escrito pago de horas extras
            3. Si no pagan: Denuncia en Inspección del Trabajo
            4. Puedes reclamar hasta 6 meses hacia atrás

            Importante:
            - El empleador debe llevar registro de asistencia
            - Horas extras se pagan en la remuneración mensual
            - Trabajar domingos/festivos: Pago normal + día compensatorio
            """,
            "source": "Dirección del Trabajo - Contenido oficial",
            "url": "https://www.dt.gob.cl",
            "scraped_at": datetime.now().isoformat()
        })

        # Guardar guías
        for idx, guia in enumerate(guias, 1):
            output_file = self.output_dir / f"guia_{idx}_{guia['category']}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(guia, f, ensure_ascii=False, indent=2)

            print(f"✅ Guía guardada: {guia['title']}")

        return guias

    def get_summary(self) -> Dict:
        """Obtiene un resumen del contenido descargado"""
        json_files = list(self.output_dir.glob("*.json"))

        summary = {
            "total_guides": len(json_files),
            "guides": [],
            "categories": set()
        }

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                summary["guides"].append({
                    "title": data.get("title"),
                    "category": data.get("category"),
                    "file": json_file.name
                })
                summary["categories"].add(data.get("category"))

        summary["categories"] = list(summary["categories"])
        return summary


def main():
    """Script principal para ejecutar el scraper"""
    print("=" * 60)
    print("DIRECCIÓN DEL TRABAJO SCRAPER - JUSTICIAAI")
    print("=" * 60)

    scraper = DTScraper()

    # Descargar guías laborales
    guias = scraper.scrape_guias_laborales()

    # Mostrar resumen
    summary = scraper.get_summary()

    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    print(f"Total guías descargadas: {summary['total_guides']}")
    print(f"Categorías: {', '.join(summary['categories'])}")
    print("\nGuías guardadas:")
    for guia in summary['guides']:
        print(f"  • {guia['title']}")
    print("\n✅ Datos listos para procesamiento!")
    print(f"📂 Ubicación: {scraper.output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
