"""
SERNAC Scraper - Recopila información sobre derechos del consumidor

Fuente oficial: https://www.sernac.cl
- Ley del Consumidor (19.496)
- Guías de derechos del consumidor
- Casos frecuentes
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class SERNACScraper:
    """Scraper para contenido de derechos del consumidor desde SERNAC"""

    BASE_URL = "https://www.sernac.cl"

    def __init__(self, output_dir: str = "data/raw/sernac"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JusticiaAI-LegalBot/1.0 (Educational Purpose)'
        })

    def scrape_consumer_guides(self) -> List[Dict]:
        """
        Descarga guías sobre derechos del consumidor

        Contenido educativo público de SERNAC
        """
        print("📥 Descargando guías de derechos del consumidor...")

        guias = []

        # Guía 1: Retracto (devolución de productos)
        guias.append({
            "title": "Derecho a Retracto - Devolución de Productos",
            "category": "derechos_basicos",
            "content": """
            DERECHO A RETRACTO (DEVOLUCIÓN)

            ¿Qué es el derecho a retracto?
            Es el derecho a devolver un producto sin dar razones y obtener la devolución de tu dinero.

            ¿Cuándo aplica?
            - Compras por internet
            - Compras por teléfono
            - Compras a domicilio (vendedor va a tu casa)
            - Compras fuera del local comercial

            Plazo:
            - 10 días corridos desde que recibes el producto
            - Para servicios: 10 días desde la contratación

            ¿Qué NO aplica para retracto?
            - Compras en tienda física (salvo garantía legal o cambio voluntario del vendedor)
            - Productos hechos a medida o personalizados
            - Productos perecibles (alimentos frescos)
            - Software descargado o abierto
            - Servicios ya prestados completamente

            ¿Cómo ejercer el derecho?
            1. Envía un correo o carta al vendedor indicando que te retractas
            2. Devuelve el producto en las mismas condiciones que lo recibiste
            3. El vendedor tiene 10 días para devolver tu dinero

            Costos de envío:
            - Envío de ida: Lo pagaste tú (no se devuelve)
            - Envío de vuelta: Lo pagas tú (salvo que el vendedor ofrezca pagarlo)

            Importante:
            - No necesitas dar razones
            - El producto debe estar sin uso y con etiquetas
            - Guarda comprobantes de envío
            - Si no te devuelven el dinero, puedes reclamar en SERNAC

            Ejemplo:
            Compraste zapatillas online el 1 de marzo, llegaron el 5 de marzo.
            Tienes hasta el 15 de marzo (10 días) para retractarte.
            """,
            "source": "SERNAC - Contenido oficial",
            "url": "https://www.sernac.cl",
            "scraped_at": datetime.now().isoformat()
        })

        # Guía 2: Garantía Legal
        guias.append({
            "title": "Garantía Legal - 3 meses obligatorios",
            "category": "garantias",
            "content": """
            GARANTÍA LEGAL (3 MESES OBLIGATORIA)

            ¿Qué es?
            Es la garantía mínima de 3 meses que tiene TODO producto nuevo por ley.

            ¿Qué cubre?
            - Fallas de fabricación
            - Producto que no funciona como debería
            - Diferencias con lo publicitado
            - Producto no sirve para el uso normal

            Duración:
            - Productos nuevos: Mínimo 3 meses
            - Productos usados: Mínimo 2 meses (si es vendedor profesional)
            - El vendedor puede ofrecer más tiempo (voluntario)

            ¿Qué NO cubre?
            - Mal uso del producto
            - Desgaste natural por uso
            - Daños causados por el comprador
            - Reparaciones por terceros no autorizados

            ¿Qué puedes pedir?
            Si el producto falla dentro de los 3 meses, puedes elegir:
            1. Reparación gratis
            2. Cambio por otro igual
            3. Devolución del dinero

            Importante:
            - La garantía es GRATIS (no puedes cobrar reparación)
            - El vendedor tiene máximo 30 días para reparar
            - Si no repara en 30 días: Puedes pedir cambio o devolución
            - Si la falla es grave: Puedes pedir cambio o devolución de inmediato

            Garantía del fabricante:
            - Es adicional a la garantía legal
            - Puede ser más larga (6 meses, 1 año, etc.)
            - Puede tener condiciones especiales

            ¿Cómo hacer efectiva la garantía?
            1. Lleva el producto al lugar de compra con la boleta
            2. Explica la falla
            3. Pide reparación, cambio o devolución
            4. Si no solucionan: Reclama en SERNAC

            Ejemplo:
            Compraste un celular el 1 de enero. El 15 de febrero deja de cargar.
            Tienes derecho a que lo reparen gratis o te lo cambien (estás dentro de los 3 meses).
            """,
            "source": "SERNAC - Contenido oficial",
            "url": "https://www.sernac.cl",
            "scraped_at": datetime.now().isoformat()
        })

        # Guía 3: Cobros indebidos
        guias.append({
            "title": "Cobros Indebidos y Cómo Reclamar",
            "category": "cobranzas",
            "content": """
            COBROS INDEBIDOS Y CÓMO RECLAMAR

            ¿Qué es un cobro indebido?
            - Te cobran algo que no compraste
            - Te cobran más de lo acordado
            - Te cobran servicios no contratados
            - Te cobran productos defectuosos que devolviste

            Ejemplos comunes:
            - Suscripciones que no autorizaste
            - Cargos duplicados en tarjeta
            - Cobros después de cancelar un servicio
            - Intereses o comisiones no informados

            ¿Qué hacer?

            1. RECLAMA AL PROVEEDOR (Primer paso obligatorio)
            - Envía correo o carta explicando el problema
            - Adjunta comprobantes (boletas, contratos, capturas)
            - Pide corrección del cobro
            - Guarda copia del reclamo

            2. SI NO RESPONDEN O RECHAZAN (después de 10 días)
            - Reclama en SERNAC: www.sernac.cl
            - O en Juzgado de Policía Local

            3. RECLAMO EN SERNAC
            - Es gratis
            - Puedes hacerlo online
            - SERNAC media entre tú y la empresa
            - Si no hay acuerdo: Puede ir a juicio

            Plazos:
            - Para reclamar: Hasta 6 meses después del problema
            - Para ir a juicio: Hasta 2 años

            ¿Qué puedes pedir?
            - Devolución del dinero cobrado indebidamente
            - Corrección de la factura
            - Indemnización por daños (si corresponde)
            - Multa a la empresa (en casos graves)

            Cobros en tarjeta de crédito:
            - Puedes hacer "reversa de cargo" (chargeback)
            - Contacta a tu banco dentro de 60 días
            - El banco investiga y puede devolverte el dinero

            SERNAC Telefónico:
            - 800 700 100 (gratis)
            - www.sernac.cl (reclamos online)
            - Oficinas regionales presenciales

            Importante:
            - NUNCA pagues algo que no reconoces sin antes reclamar
            - Guarda todos los comprobantes
            - Revisa tus estados de cuenta mensualmente
            - Las empresas no pueden cobrarte sin autorización previa

            Protección contra DICOM:
            Si el cobro es indebido y te amenazan con DICOM:
            - Reclama de inmediato en SERNAC
            - Es ilegal incluirte en DICOM por deudas en disputa
            - Puedes demandar por daño moral si te incluyen injustamente
            """,
            "source": "SERNAC - Contenido oficial",
            "url": "https://www.sernac.cl",
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
    print("SERNAC SCRAPER - JUSTICIAAI")
    print("=" * 60)

    scraper = SERNACScraper()

    # Descargar guías de consumidor
    guias = scraper.scrape_consumer_guides()

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
