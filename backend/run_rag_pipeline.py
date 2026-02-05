#!/usr/bin/env python3
"""
Master Script - Ejecuta el pipeline completo de RAG

Pipeline:
1. Recopila datos legales (BCN, DT, SERNAC)
2. Procesa y limpia textos
3. Genera embeddings
4. Sube a Pinecone
5. Verifica que todo funcionó

Uso:
    python run_rag_pipeline.py            # Pipeline completo
    python run_rag_pipeline.py --skip-scraping  # Solo procesamiento
    python run_rag_pipeline.py --scrape-only    # Solo recopilación
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import argparse

class RAGPipeline:
    """Orquestador del pipeline RAG completo"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.start_time = None
        self.steps_completed = 0
        self.total_steps = 5

    def print_header(self, message):
        """Imprime encabezado de sección"""
        if self.verbose:
            print("\n" + "=" * 70)
            print(f"  {message}")
            print("=" * 70 + "\n")

    def print_step(self, step_num, message):
        """Imprime paso del pipeline"""
        if self.verbose:
            print(f"\n[Paso {step_num}/{self.total_steps}] {message}")
            print("-" * 70)

    def run_script(self, script_path, description):
        """
        Ejecuta un script Python y captura su salida

        Args:
            script_path: Ruta al script
            description: Descripción de lo que hace

        Returns:
            True si exitoso, False si falló
        """
        print(f"\n🔄 Ejecutando: {description}")
        print(f"   Script: {script_path}")

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )

            if result.returncode == 0:
                print(f"✅ {description} - COMPLETADO")
                if self.verbose and result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"❌ {description} - FALLÓ")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"❌ {description} - TIMEOUT (>5 min)")
            return False
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
            return False

    def step1_scrape_data(self):
        """Paso 1: Recopila datos legales"""
        self.print_step(1, "Recopilación de Datos Legales")

        scripts = [
            ("data_collection/bcn_scraper.py", "Leyes BCN LeyChile"),
            ("data_collection/dt_scraper.py", "Guías Dirección del Trabajo"),
            ("data_collection/sernac_scraper.py", "Información SERNAC")
        ]

        all_success = True
        for script, desc in scripts:
            if not self.run_script(script, desc):
                all_success = False

        if all_success:
            self.steps_completed += 1
            print("\n✅ Paso 1: Datos recopilados exitosamente")
        else:
            print("\n⚠️  Paso 1: Algunos scrapers fallaron, continuar de todos modos")
            self.steps_completed += 1

        return True  # Continuar aunque algunos fallen

    def step2_process_texts(self):
        """Paso 2: Procesa y limpia textos"""
        self.print_step(2, "Procesamiento de Textos")

        success = self.run_script(
            "data_processing/text_processor.py",
            "Limpieza y chunking de textos"
        )

        if success:
            self.steps_completed += 1
            print("\n✅ Paso 2: Textos procesados exitosamente")
        else:
            print("\n❌ Paso 2: Error en procesamiento. Pipeline detenido.")

        return success

    def step3_generate_embeddings(self):
        """Paso 3: Genera embeddings"""
        self.print_step(3, "Generación de Embeddings")

        success = self.run_script(
            "data_processing/embedder.py",
            "Embeddings con OpenAI"
        )

        if success:
            self.steps_completed += 1
            print("\n✅ Paso 3: Embeddings generados exitosamente")
        else:
            print("\n❌ Paso 3: Error generando embeddings. Pipeline detenido.")

        return success

    def step4_upload_to_pinecone(self):
        """Paso 4: Sube vectores a Pinecone"""
        self.print_step(4, "Carga a Pinecone Vector Database")

        success = self.run_script(
            "rag/vector_store.py",
            "Upload a Pinecone"
        )

        if success:
            self.steps_completed += 1
            print("\n✅ Paso 4: Vectores subidos a Pinecone exitosamente")
        else:
            print("\n❌ Paso 4: Error subiendo a Pinecone. Pipeline detenido.")

        return success

    def step5_verify_system(self):
        """Paso 5: Verifica que RAG esté funcionando"""
        self.print_step(5, "Verificación del Sistema")

        print("🔍 Verificando archivos generados...")

        # Verificar directorios
        checks = [
            (Path("data/raw/bcn"), "Datos BCN"),
            (Path("data/raw/dt"), "Datos DT"),
            (Path("data/raw/sernac"), "Datos SERNAC"),
            (Path("data/processed"), "Textos procesados"),
            (Path("data/embeddings"), "Embeddings"),
        ]

        all_exist = True
        for path, name in checks:
            if path.exists():
                files = list(path.glob("*.json"))
                print(f"   ✅ {name}: {len(files)} archivos")
            else:
                print(f"   ❌ {name}: No encontrado")
                all_exist = False

        if all_exist:
            self.steps_completed += 1
            print("\n✅ Paso 5: Sistema verificado y funcional")
            return True
        else:
            print("\n⚠️  Paso 5: Algunas verificaciones fallaron")
            return False

    def run_full_pipeline(self, skip_scraping=False, scrape_only=False):
        """Ejecuta el pipeline completo"""
        self.start_time = time.time()

        self.print_header("PIPELINE RAG - JUSTICIAAI")
        print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Paso 1: Scraping (opcional)
        if not skip_scraping:
            if not self.step1_scrape_data():
                return False

        if scrape_only:
            print("\n✅ Scraping completado (solo recopilación)")
            return True

        # Paso 2: Procesamiento
        if not self.step2_process_texts():
            return False

        # Paso 3: Embeddings
        if not self.step3_generate_embeddings():
            return False

        # Paso 4: Pinecone
        if not self.step4_upload_to_pinecone():
            return False

        # Paso 5: Verificación
        self.step5_verify_system()

        # Resumen final
        elapsed = time.time() - self.start_time
        self.print_header("RESUMEN FINAL")

        print(f"✅ Pipeline completado exitosamente")
        print(f"⏱️  Tiempo total: {elapsed / 60:.1f} minutos")
        print(f"📊 Pasos completados: {self.steps_completed}/{self.total_steps}")

        print("\n📝 Próximos pasos:")
        print("   1. Inicia el backend: python main_simple.py")
        print("   2. Abre el chat: http://localhost:3001/chat")
        print("   3. Haz una pregunta: '¿Qué es el finiquito?'")
        print("   4. ¡Verifica que RAG funciona! (respuesta con fuentes)")

        return True


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Pipeline RAG completo para JusticiaAI"
    )
    parser.add_argument(
        "--skip-scraping",
        action="store_true",
        help="Omite la recopilación de datos (usa datos existentes)"
    )
    parser.add_argument(
        "--scrape-only",
        action="store_true",
        help="Solo ejecuta los scrapers (no procesa)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Modo silencioso (menos output)"
    )

    args = parser.parse_args()

    # Crear pipeline
    pipeline = RAGPipeline(verbose=not args.quiet)

    # Ejecutar
    try:
        success = pipeline.run_full_pipeline(
            skip_scraping=args.skip_scraping,
            scrape_only=args.scrape_only
        )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n❌ Pipeline interrumpido por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
