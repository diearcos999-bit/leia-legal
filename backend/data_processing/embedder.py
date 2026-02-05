"""
Embedder - Genera embeddings vectoriales de textos legales usando OpenAI

Utiliza el modelo text-embedding-3-small de OpenAI:
- Dimensiones: 1536
- Costo: ~$0.02 por 1M tokens
- Alta calidad para búsqueda semántica
"""

import openai
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    """Generador de embeddings para textos legales"""

    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        """
        Args:
            model: Modelo de OpenAI para embeddings
            api_key: API key de OpenAI (si no está en .env)
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OpenAI API key no configurada. "
                "Agrega OPENAI_API_KEY a .env o pásala como parámetro"
            )

        # Configurar cliente OpenAI
        openai.api_key = self.api_key

        self.embedding_dim = 1536  # Dimensiones de text-embedding-3-small
        self.batch_size = 100  # Procesar hasta 100 textos por batch

    def generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding para un texto individual

        Args:
            text: Texto a vectorizar

        Returns:
            Vector de embeddings (lista de floats)
        """
        try:
            response = openai.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Error generando embedding: {e}")
            return None

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings para múltiples textos en un batch

        Args:
            texts: Lista de textos a vectorizar

        Returns:
            Lista de vectores de embeddings
        """
        if not texts:
            return []

        try:
            response = openai.embeddings.create(
                model=self.model,
                input=texts
            )

            # Ordenar embeddings según el índice original
            embeddings = [None] * len(texts)
            for item in response.data:
                embeddings[item.index] = item.embedding

            return embeddings

        except Exception as e:
            print(f"❌ Error generando batch de embeddings: {e}")
            return [None] * len(texts)

    def process_chunks_file(self, input_file: Path, output_file: Path) -> Dict:
        """
        Procesa un archivo de chunks y genera embeddings

        Args:
            input_file: Archivo JSON con chunks procesados
            output_file: Archivo donde guardar chunks con embeddings

        Returns:
            Resumen del procesamiento
        """
        print(f"\n📥 Cargando chunks desde: {input_file.name}")

        with open(input_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        total_chunks = len(chunks)
        print(f"📊 Total chunks a procesar: {total_chunks}")

        # Procesar en batches
        chunks_with_embeddings = []
        failed_chunks = 0

        for i in range(0, total_chunks, self.batch_size):
            batch = chunks[i:i + self.batch_size]
            batch_texts = [chunk["text"] for chunk in batch]

            print(f"🔄 Procesando batch {i // self.batch_size + 1} ({len(batch)} chunks)...")

            embeddings = self.generate_embeddings_batch(batch_texts)

            # Agregar embeddings a chunks
            for chunk, embedding in zip(batch, embeddings):
                if embedding:
                    chunk["embedding"] = embedding
                    chunk["embedding_model"] = self.model
                    chunk["embedding_dim"] = self.embedding_dim
                    chunk["embedded_at"] = datetime.now().isoformat()
                    chunks_with_embeddings.append(chunk)
                else:
                    failed_chunks += 1
                    print(f"   ⚠️  Falló chunk: {chunk.get('chunk_id', 'unknown')}")

            # Rate limiting: pequeña pausa entre batches
            if i + self.batch_size < total_chunks:
                time.sleep(0.5)

        # Guardar chunks con embeddings
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_with_embeddings, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Embeddings generados: {len(chunks_with_embeddings)}")
        if failed_chunks > 0:
            print(f"❌ Chunks fallidos: {failed_chunks}")
        print(f"💾 Guardados en: {output_file}")

        # Resumen
        summary = {
            "input_file": str(input_file),
            "output_file": str(output_file),
            "total_chunks": total_chunks,
            "successful_embeddings": len(chunks_with_embeddings),
            "failed_chunks": failed_chunks,
            "model": self.model,
            "embedding_dim": self.embedding_dim,
            "processed_at": datetime.now().isoformat()
        }

        return summary

    def process_all_chunk_files(self, input_dir: Path, output_dir: Path) -> List[Dict]:
        """
        Procesa todos los archivos de chunks en un directorio

        Args:
            input_dir: Directorio con archivos *_chunks.json
            output_dir: Directorio donde guardar chunks con embeddings

        Returns:
            Lista de resúmenes de procesamiento
        """
        chunk_files = list(input_dir.glob("*_chunks.json"))

        if not chunk_files:
            print(f"⚠️  No se encontraron archivos de chunks en {input_dir}")
            return []

        print(f"\n🚀 Iniciando generación de embeddings para {len(chunk_files)} archivos...\n")

        summaries = []

        for chunk_file in chunk_files:
            output_file = output_dir / f"{chunk_file.stem}_embedded.json"

            try:
                summary = self.process_chunks_file(chunk_file, output_file)
                summaries.append(summary)
            except Exception as e:
                print(f"❌ Error procesando {chunk_file.name}: {e}")

        return summaries


def estimate_cost(total_tokens: int) -> float:
    """
    Estima el costo de generar embeddings

    Args:
        total_tokens: Número total de tokens a procesar

    Returns:
        Costo estimado en USD
    """
    # text-embedding-3-small: $0.02 por 1M tokens
    cost_per_million = 0.02
    return (total_tokens / 1_000_000) * cost_per_million


def main():
    """Script principal para generar embeddings"""
    print("=" * 60)
    print("EMBEDDINGS GENERATOR - LEIA")
    print("=" * 60)

    # Verificar API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY no configurada")
        print("\nPara configurar:")
        print("1. Ve a: https://platform.openai.com/api-keys")
        print("2. Crea una API key")
        print("3. Agrégala a backend/.env:")
        print("   OPENAI_API_KEY=sk-...")
        print("\n" + "=" * 60)
        return

    try:
        embedder = Embedder()

        input_dir = Path("data/processed")
        output_dir = Path("data/embeddings")

        # Procesar todos los archivos
        summaries = embedder.process_all_chunk_files(input_dir, output_dir)

        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)

        total_chunks = sum(s["total_chunks"] for s in summaries)
        total_successful = sum(s["successful_embeddings"] for s in summaries)
        total_failed = sum(s["failed_chunks"] for s in summaries)

        print(f"Total chunks procesados: {total_chunks}")
        print(f"Embeddings exitosos: {total_successful}")
        if total_failed > 0:
            print(f"Fallos: {total_failed}")

        print(f"\nArchivos generados:")
        for summary in summaries:
            print(f"  • {Path(summary['output_file']).name}: {summary['successful_embeddings']} embeddings")

        # Estimación de costo (aproximada)
        # Asumimos ~300 tokens por chunk en promedio
        estimated_tokens = total_successful * 300
        estimated_cost = estimate_cost(estimated_tokens)

        print(f"\n💰 Costo estimado: ${estimated_cost:.4f} USD")
        print(f"   (basado en ~{estimated_tokens:,} tokens)")

        print("\n✅ Embeddings listos para Pinecone!")
        print(f"📂 Ubicación: {output_dir.absolute()}")
        print("=" * 60)

    except ValueError as e:
        print(f"\n❌ {e}")
        print("=" * 60)


if __name__ == "__main__":
    main()
