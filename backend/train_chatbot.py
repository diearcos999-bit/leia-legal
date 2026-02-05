#!/usr/bin/env python3
"""
Script de Entrenamiento del Chatbot LEIA
=========================================

Este script automatiza todo el proceso de entrenar el chatbot con legislación chilena:

1. RECOPILAR DATOS: Ejecuta scrapers de BCN, DT y SERNAC
2. PROCESAR TEXTOS: Divide en chunks apropiados para RAG
3. GENERAR EMBEDDINGS: Vectoriza textos con OpenAI
4. SUBIR A PINECONE: Almacena vectores para búsqueda

Requisitos:
- OPENAI_API_KEY en .env (para embeddings)
- PINECONE_API_KEY en .env (para vector store)

Uso:
    python train_chatbot.py              # Ejecutar todo el pipeline
    python train_chatbot.py --step 1     # Solo ejecutar paso 1 (scrapers)
    python train_chatbot.py --step 2     # Solo ejecutar paso 2 (procesamiento)
    python train_chatbot.py --step 3     # Solo ejecutar paso 3 (embeddings)
    python train_chatbot.py --step 4     # Solo ejecutar paso 4 (Pinecone)
    python train_chatbot.py --status     # Ver estado actual
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Imprime encabezado formateado"""
    print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")


def print_step(step: int, text: str):
    """Imprime paso del proceso"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[Paso {step}] {text}{Colors.END}")
    print("-" * 50)


def print_success(text: str):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text: str):
    """Imprime advertencia"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.END}")


def print_error(text: str):
    """Imprime error"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def check_requirements():
    """Verifica que estén configuradas las API keys necesarias"""
    print_header("VERIFICANDO REQUISITOS")

    errors = []
    warnings = []

    # Verificar OpenAI API Key
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY no configurada")
        print_error("OPENAI_API_KEY no configurada")
        print("   → Obtén una en: https://platform.openai.com/api-keys")
        print("   → Agrégala a backend/.env: OPENAI_API_KEY=sk-...")
    else:
        print_success("OPENAI_API_KEY configurada")

    # Verificar Pinecone API Key
    if not os.getenv("PINECONE_API_KEY"):
        warnings.append("PINECONE_API_KEY no configurada (necesaria para paso 4)")
        print_warning("PINECONE_API_KEY no configurada")
        print("   → Obtén una gratis en: https://app.pinecone.io")
        print("   → Agrégala a backend/.env: PINECONE_API_KEY=...")
    else:
        print_success("PINECONE_API_KEY configurada")

    # Verificar dependencias
    try:
        import openai
        print_success("OpenAI SDK instalado")
    except ImportError:
        errors.append("OpenAI SDK no instalado")
        print_error("OpenAI SDK no instalado. Ejecuta: pip install openai")

    try:
        from pinecone import Pinecone
        print_success("Pinecone SDK instalado")
    except ImportError:
        warnings.append("Pinecone SDK no instalado")
        print_warning("Pinecone SDK no instalado. Ejecuta: pip install pinecone-client")

    return len(errors) == 0, errors, warnings


def step1_scrape_data():
    """Paso 1: Ejecutar scrapers para recopilar datos legales"""
    print_step(1, "RECOPILANDO DATOS LEGALES")

    from data_collection.bcn_scraper import BCNScraper
    from data_collection.dt_scraper import DTScraper
    from data_collection.sernac_scraper import SERNACScraper
    from data_collection.document_loader import DocumentLoader

    results = []

    # Primero: Procesar apuntes del abogado (si existen)
    print("\n📚 Procesando apuntes legales personalizados...")
    try:
        loader = DocumentLoader()
        apuntes_summary = loader.process_all()
        if apuntes_summary["total_documents"] > 0:
            results.append({"source": "APUNTES", "items": apuntes_summary["total_documents"]})
            print_success(f"APUNTES: {apuntes_summary['total_documents']} documentos ({apuntes_summary['total_words']:,} palabras)")
        else:
            print_warning("No hay apuntes en data/raw/apuntes/")
            print("   → Copia tus PDFs/Word a las carpetas: civil, procesal, leyes, etc.")
    except Exception as e:
        print_error(f"Error procesando apuntes: {e}")

    # BCN - Leyes (Código del Trabajo, Civil, Consumidor)
    print("\n📜 Descargando leyes desde Biblioteca del Congreso Nacional...")
    try:
        bcn_scraper = BCNScraper()
        bcn_results = bcn_scraper.scrape_all_priority_laws()
        results.append({"source": "BCN", "items": len(bcn_results)})
        print_success(f"BCN: {len(bcn_results)} leyes descargadas")
    except Exception as e:
        print_error(f"Error en BCN Scraper: {e}")

    # DT - Guías laborales
    print("\n👷 Descargando guías de la Dirección del Trabajo...")
    try:
        dt_scraper = DTScraper()
        dt_results = dt_scraper.scrape_guias_laborales()
        results.append({"source": "DT", "items": len(dt_results)})
        print_success(f"DT: {len(dt_results)} guías descargadas")
    except Exception as e:
        print_error(f"Error en DT Scraper: {e}")

    # SERNAC - Derechos del consumidor
    print("\n🛒 Descargando guías de SERNAC...")
    try:
        sernac_scraper = SERNACScraper()
        sernac_results = sernac_scraper.scrape_consumer_guides()
        results.append({"source": "SERNAC", "items": len(sernac_results)})
        print_success(f"SERNAC: {len(sernac_results)} guías descargadas")
    except Exception as e:
        print_error(f"Error en SERNAC Scraper: {e}")

    print("\n" + "-" * 50)
    total = sum(r["items"] for r in results)
    print_success(f"Total documentos recopilados: {total}")

    return results


def step2_process_texts():
    """Paso 2: Procesar textos y dividir en chunks"""
    print_step(2, "PROCESANDO TEXTOS")

    from data_processing.text_processor import TextProcessor

    processor = TextProcessor(chunk_size=1000, chunk_overlap=200)

    base_dir = Path("data/raw")
    output_dir = Path("data/processed")

    # Fuentes estándar + carpetas de apuntes
    sources = ["bcn", "dt", "sernac"]
    apuntes_categories = ["todos", "civil", "procesal", "leyes", "laboral", "familia", "consumidor", "penal"]

    all_chunks = 0

    # Procesar fuentes estándar
    for source in sources:
        source_dir = base_dir / source
        if source_dir.exists() and list(source_dir.glob("*.json")):
            print(f"\n📄 Procesando {source.upper()}...")
            try:
                summary = processor.process_directory(source_dir, output_dir)
                all_chunks += summary["total_chunks"]
                print_success(f"{source.upper()}: {summary['total_chunks']} chunks generados")
            except Exception as e:
                print_error(f"Error procesando {source}: {e}")

    # Procesar apuntes personalizados
    apuntes_dir = base_dir / "apuntes"
    for category in apuntes_categories:
        category_dir = apuntes_dir / category
        if category_dir.exists() and list(category_dir.glob("*.json")):
            print(f"\n📚 Procesando apuntes de {category.upper()}...")
            try:
                summary = processor.process_directory(category_dir, output_dir)
                all_chunks += summary["total_chunks"]
                print_success(f"APUNTES {category.upper()}: {summary['total_chunks']} chunks generados")
            except Exception as e:
                print_error(f"Error procesando apuntes {category}: {e}")

    print("\n" + "-" * 50)
    print_success(f"Total chunks generados: {all_chunks}")

    return all_chunks


def step3_generate_embeddings():
    """Paso 3: Generar embeddings con OpenAI"""
    print_step(3, "GENERANDO EMBEDDINGS")

    if not os.getenv("OPENAI_API_KEY"):
        print_error("OPENAI_API_KEY no configurada. No se pueden generar embeddings.")
        print("   → Agrega tu API key a backend/.env")
        return 0

    from data_processing.embedder import Embedder

    try:
        embedder = Embedder()
    except ValueError as e:
        print_error(str(e))
        return 0

    input_dir = Path("data/processed")
    output_dir = Path("data/embeddings")

    chunk_files = list(input_dir.glob("*_chunks.json"))

    if not chunk_files:
        print_warning("No hay archivos de chunks para procesar.")
        print("   → Ejecuta primero el paso 2 (procesamiento)")
        return 0

    total_embeddings = 0

    for chunk_file in chunk_files:
        output_file = output_dir / f"{chunk_file.stem.replace('_chunks', '')}_embedded.json"
        print(f"\n🔄 Procesando {chunk_file.name}...")

        try:
            summary = embedder.process_chunks_file(chunk_file, output_file)
            total_embeddings += summary["successful_embeddings"]
            print_success(f"{summary['successful_embeddings']} embeddings generados")
        except Exception as e:
            print_error(f"Error generando embeddings: {e}")

    print("\n" + "-" * 50)
    print_success(f"Total embeddings generados: {total_embeddings}")

    # Estimar costo
    estimated_tokens = total_embeddings * 300  # ~300 tokens por chunk
    cost = (estimated_tokens / 1_000_000) * 0.02
    print(f"💰 Costo estimado: ${cost:.4f} USD")

    return total_embeddings


def step4_upload_to_pinecone():
    """Paso 4: Subir embeddings a Pinecone"""
    print_step(4, "SUBIENDO A PINECONE")

    if not os.getenv("PINECONE_API_KEY"):
        print_error("PINECONE_API_KEY no configurada.")
        print("   → Obtén una gratis en: https://app.pinecone.io")
        print("   → Agrega a backend/.env: PINECONE_API_KEY=...")
        return 0

    try:
        from rag.vector_store import VectorStore
    except ImportError as e:
        print_error(f"Error importando VectorStore: {e}")
        return 0

    embeddings_dir = Path("data/embeddings")
    embedding_files = list(embeddings_dir.glob("*_embedded.json"))

    if not embedding_files:
        print_warning("No hay archivos de embeddings para subir.")
        print("   → Ejecuta primero el paso 3 (embeddings)")
        return 0

    try:
        print("🔌 Conectando a Pinecone...")
        vector_store = VectorStore()

        summaries = vector_store.load_all_embeddings(embeddings_dir)

        total_upserted = sum(s["vectors_upserted"] for s in summaries)

        print("\n" + "-" * 50)
        print_success(f"Total vectores subidos: {total_upserted}")

        # Mostrar estadísticas
        stats = vector_store.get_stats()
        if stats:
            print(f"\n📊 Estadísticas del índice:")
            print(f"   • Total vectores: {stats['total_vectors']}")
            print(f"   • Capacidad usada: {stats['index_fullness']*100:.2f}%")

        return total_upserted

    except Exception as e:
        print_error(f"Error subiendo a Pinecone: {e}")
        return 0


def show_status():
    """Muestra el estado actual del sistema"""
    print_header("ESTADO DEL SISTEMA RAG")

    # Verificar datos raw
    print("\n📁 Datos recopilados (data/raw/):")
    raw_dir = Path("data/raw")
    for source in ["bcn", "dt", "sernac"]:
        source_dir = raw_dir / source
        if source_dir.exists():
            files = list(source_dir.glob("*.json"))
            print(f"   • {source.upper()}: {len(files)} archivos")
        else:
            print(f"   • {source.upper()}: No hay datos")

    # Verificar apuntes
    print("\n📚 Apuntes personalizados (data/raw/apuntes/):")
    apuntes_dir = raw_dir / "apuntes"
    categories = ["todos", "civil", "procesal", "leyes", "laboral", "familia", "consumidor", "penal"]
    total_apuntes = 0
    for cat in categories:
        cat_dir = apuntes_dir / cat
        if cat_dir.exists():
            # Contar todos los formatos
            files = list(cat_dir.glob("*.json")) + list(cat_dir.glob("*.pdf")) + \
                    list(cat_dir.glob("*.docx")) + list(cat_dir.glob("*.txt"))
            if files:
                print(f"   • {cat.upper()}: {len(files)} archivos")
                total_apuntes += len(files)
    if total_apuntes == 0:
        print("   • No hay apuntes cargados")
        print("   → Copia tus PDFs/Word a: data/raw/apuntes/{civil,procesal,leyes,...}")

    # Verificar chunks procesados
    print("\n📄 Chunks procesados (data/processed/):")
    processed_dir = Path("data/processed")
    if processed_dir.exists():
        files = list(processed_dir.glob("*_chunks.json"))
        for f in files:
            import json
            with open(f) as fp:
                chunks = json.load(fp)
            print(f"   • {f.name}: {len(chunks)} chunks")
    else:
        print("   • No hay chunks procesados")

    # Verificar embeddings
    print("\n🔢 Embeddings generados (data/embeddings/):")
    embeddings_dir = Path("data/embeddings")
    if embeddings_dir.exists():
        files = list(embeddings_dir.glob("*_embedded.json"))
        for f in files:
            import json
            with open(f) as fp:
                embeddings = json.load(fp)
            print(f"   • {f.name}: {len(embeddings)} embeddings")
    else:
        print("   • No hay embeddings generados")

    # Verificar Pinecone
    print("\n☁️  Pinecone:")
    if os.getenv("PINECONE_API_KEY"):
        try:
            from rag.vector_store import VectorStore
            vs = VectorStore()
            stats = vs.get_stats()
            print(f"   • Conectado: Sí")
            print(f"   • Total vectores: {stats.get('total_vectors', 0)}")
            print(f"   • Capacidad: {stats.get('index_fullness', 0)*100:.2f}%")
        except Exception as e:
            print(f"   • Error conectando: {e}")
    else:
        print("   • PINECONE_API_KEY no configurada")

    # Verificar RAG en main.py
    print("\n🤖 Integración RAG en Chat:")
    main_path = Path("main.py")
    if main_path.exists():
        content = main_path.read_text()
        if "rag_engine" in content.lower() or "RAGEngine" in content:
            print("   • RAG integrado en main.py: Sí")
        else:
            print("   • RAG integrado en main.py: No (ejecuta train_chatbot.py para integrar)")


def run_full_pipeline():
    """Ejecuta todo el pipeline de entrenamiento"""
    print_header("ENTRENAMIENTO DE LEIA - CHATBOT LEGAL")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Verificar requisitos
    ok, errors, warnings = check_requirements()

    if not ok:
        print_error("\n❌ Hay errores que impiden continuar.")
        print("   Por favor, corrige los errores y vuelve a ejecutar.")
        return

    if warnings:
        print_warning("\n⚠️  Hay advertencias, pero puedes continuar parcialmente.")

    # Paso 1: Recopilar datos
    step1_scrape_data()

    # Paso 2: Procesar textos
    step2_process_texts()

    # Paso 3: Generar embeddings
    if os.getenv("OPENAI_API_KEY"):
        step3_generate_embeddings()
    else:
        print_warning("\nSaltando paso 3 (embeddings) - OPENAI_API_KEY no configurada")

    # Paso 4: Subir a Pinecone
    if os.getenv("PINECONE_API_KEY"):
        step4_upload_to_pinecone()
    else:
        print_warning("\nSaltando paso 4 (Pinecone) - PINECONE_API_KEY no configurada")

    # Resumen final
    print_header("ENTRENAMIENTO COMPLETADO")
    show_status()

    print(f"\n{Colors.GREEN}{Colors.BOLD}¡LEIA está lista para responder con conocimiento legal chileno!{Colors.END}")
    print("\nPróximos pasos:")
    print("1. Ejecuta el backend: python main.py")
    print("2. El chatbot usará RAG automáticamente si está configurado")


def main():
    parser = argparse.ArgumentParser(description="Entrenar chatbot LEIA con legislación chilena")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4],
                       help="Ejecutar solo un paso específico")
    parser.add_argument("--status", action="store_true",
                       help="Mostrar estado actual del sistema")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.step == 1:
        check_requirements()
        step1_scrape_data()
    elif args.step == 2:
        check_requirements()
        step2_process_texts()
    elif args.step == 3:
        check_requirements()
        step3_generate_embeddings()
    elif args.step == 4:
        check_requirements()
        step4_upload_to_pinecone()
    else:
        run_full_pipeline()


if __name__ == "__main__":
    main()
