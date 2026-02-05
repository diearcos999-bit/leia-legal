"""
BCN LeyChile Scraper - Recopila leyes chilenas desde la Biblioteca del Congreso Nacional

Fuentes:
- Código del Trabajo: https://www.bcn.cl/leychile/navegar?idNorma=207436
- Código Civil: https://www.bcn.cl/leychile/navegar?idNorma=172986
- Ley del Consumidor: https://www.bcn.cl/leychile/navegar?idNorma=61438
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

class BCNScraper:
    """Scraper para leyes chilenas desde BCN LeyChile"""

    BASE_URL = "https://www.bcn.cl/leychile"

    # Leyes prioritarias para el asistente legal
    PRIORITY_LAWS = {
        "codigo_trabajo": {
            "id": "207436",
            "name": "Código del Trabajo",
            "category": "laboral",
            "url": "https://www.bcn.cl/leychile/navegar?idNorma=207436"
        },
        "codigo_civil": {
            "id": "172986",
            "name": "Código Civil",
            "category": "civil",
            "url": "https://www.bcn.cl/leychile/navegar?idNorma=172986"
        },
        "ley_consumidor": {
            "id": "61438",
            "name": "Ley del Consumidor (19.496)",
            "category": "consumidor",
            "url": "https://www.bcn.cl/leychile/navegar?idNorma=61438"
        },
        "codigo_familia": {
            "id": "229557",
            "name": "Ley de Matrimonio Civil (19.947)",
            "category": "familia",
            "url": "https://www.bcn.cl/leychile/navegar?idNorma=229557"
        },
        "pension_alimenticia": {
            "id": "229557",
            "name": "Ley sobre Pensión Alimenticia (14.908)",
            "category": "familia",
            "url": "https://www.bcn.cl/leychile/navegar?idNorma=28581"
        }
    }

    def __init__(self, output_dir: str = "data/raw/bcn"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JusticiaAI-LegalBot/1.0 (Educational Purpose)'
        })

    def fetch_law_html(self, law_id: str) -> Optional[str]:
        """Descarga el HTML de una ley específica"""
        url = f"{self.BASE_URL}/navegar?idNorma={law_id}"

        try:
            print(f"📥 Descargando ley ID {law_id}...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Error descargando ley {law_id}: {e}")
            return None

    def parse_law_content(self, html: str, law_info: Dict) -> Dict:
        """Extrae el contenido estructurado de una ley"""
        soup = BeautifulSoup(html, 'html.parser')

        # Extraer artículos
        articles = []

        # Buscar divs con clase 'art' o 'articulo'
        article_elements = soup.find_all(['div', 'p'], class_=re.compile(r'(art|articulo)', re.I))

        for idx, elem in enumerate(article_elements, 1):
            text = elem.get_text(strip=True)
            if text and len(text) > 20:  # Filtrar elementos vacíos
                articles.append({
                    "article_number": idx,
                    "content": text,
                    "html": str(elem)
                })

        # Si no encontramos artículos por clase, buscar por estructura
        if not articles:
            # Buscar por patrón "Artículo X"
            content_div = soup.find('div', id='textolei') or soup.find('div', class_='texto-norma')
            if content_div:
                text = content_div.get_text(separator='\n\n')
                # Dividir por "Artículo"
                parts = re.split(r'Artículo\s+(\d+[º°]?\.?-?)', text, flags=re.IGNORECASE)

                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        article_num = parts[i].strip()
                        article_text = parts[i + 1].strip()
                        articles.append({
                            "article_number": article_num,
                            "content": article_text,
                            "html": None
                        })

        return {
            "law_id": law_info.get("id"),
            "law_name": law_info.get("name"),
            "category": law_info.get("category"),
            "url": law_info.get("url"),
            "articles": articles,
            "total_articles": len(articles),
            "scraped_at": datetime.now().isoformat(),
            "source": "BCN LeyChile"
        }

    def scrape_law(self, law_key: str) -> Optional[Dict]:
        """Descarga y procesa una ley específica"""
        if law_key not in self.PRIORITY_LAWS:
            print(f"❌ Ley '{law_key}' no encontrada en lista prioritaria")
            return None

        law_info = self.PRIORITY_LAWS[law_key]

        # Descargar HTML
        html = self.fetch_law_html(law_info["id"])
        if not html:
            return None

        # Parsear contenido
        parsed_data = self.parse_law_content(html, law_info)

        # Guardar JSON
        output_file = self.output_dir / f"{law_key}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Ley '{law_info['name']}' guardada: {parsed_data['total_articles']} artículos")
        return parsed_data

    def scrape_all_priority_laws(self) -> List[Dict]:
        """Descarga todas las leyes prioritarias"""
        results = []

        print(f"\n🚀 Iniciando descarga de {len(self.PRIORITY_LAWS)} leyes prioritarias...\n")

        for idx, (law_key, law_info) in enumerate(self.PRIORITY_LAWS.items(), 1):
            print(f"[{idx}/{len(self.PRIORITY_LAWS)}] {law_info['name']}")

            result = self.scrape_law(law_key)
            if result:
                results.append(result)

            # Rate limiting: esperar entre requests
            if idx < len(self.PRIORITY_LAWS):
                time.sleep(2)  # 2 segundos entre requests

        print(f"\n✅ Descarga completada: {len(results)} leyes guardadas\n")
        return results

    def get_summary(self) -> Dict:
        """Obtiene un resumen de las leyes descargadas"""
        json_files = list(self.output_dir.glob("*.json"))

        summary = {
            "total_laws": len(json_files),
            "laws": [],
            "total_articles": 0
        }

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                summary["laws"].append({
                    "name": data.get("law_name"),
                    "category": data.get("category"),
                    "articles": data.get("total_articles", 0),
                    "file": json_file.name
                })
                summary["total_articles"] += data.get("total_articles", 0)

        return summary


def main():
    """Script principal para ejecutar el scraper"""
    print("=" * 60)
    print("BCN LEYCHILE SCRAPER - JUSTICIAAI")
    print("=" * 60)

    scraper = BCNScraper()

    # Descargar todas las leyes prioritarias
    results = scraper.scrape_all_priority_laws()

    # Mostrar resumen
    summary = scraper.get_summary()

    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    print(f"Total leyes descargadas: {summary['total_laws']}")
    print(f"Total artículos: {summary['total_articles']}")
    print("\nLeyes guardadas:")
    for law in summary['laws']:
        print(f"  • {law['name']}: {law['articles']} artículos ({law['category']})")
    print("\n✅ Datos listos para procesamiento!")
    print(f"📂 Ubicación: {scraper.output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
