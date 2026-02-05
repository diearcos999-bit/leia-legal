"""
Vector Store - Maneja almacenamiento y búsqueda en Pinecone

Pinecone Free Tier:
- 100,000 vectores gratis
- 1 índice
- 1GB storage
- Perfecto para MVP
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import os
from dotenv import load_dotenv

try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("⚠️  Pinecone no instalado. Instala con: pip install pinecone-client")

load_dotenv()


class VectorStore:
    """Maneja almacenamiento y búsqueda de vectores en Pinecone"""

    def __init__(
        self,
        index_name: str = "leia-legal",
        dimension: int = 1536,
        metric: str = "cosine"
    ):
        """
        Args:
            index_name: Nombre del índice en Pinecone
            dimension: Dimensiones de los vectores (1536 para OpenAI)
            metric: Métrica de similitud (cosine, euclidean, dotproduct)
        """
        if not PINECONE_AVAILABLE:
            raise ImportError("Pinecone no instalado. pip install pinecone-client")

        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric

        # Obtener API key
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "PINECONE_API_KEY no configurada. "
                "Agrégala a .env o ve a: https://app.pinecone.io"
            )

        # Inicializar cliente Pinecone
        self.pc = Pinecone(api_key=self.api_key)

        # Inicializar o conectar al índice
        self.index = None
        self._initialize_index()

    def _initialize_index(self):
        """Crea o conecta al índice de Pinecone"""
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            print(f"📝 Creando nuevo índice: {self.index_name}")

            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Región free tier
                )
            )

            print(f"✅ Índice '{self.index_name}' creado exitosamente")
        else:
            print(f"✅ Conectado a índice existente: {self.index_name}")

        self.index = self.pc.Index(self.index_name)

    def upsert_vectors(self, vectors: List[Tuple[str, List[float], Dict]]) -> Dict:
        """
        Inserta o actualiza vectores en Pinecone

        Args:
            vectors: Lista de tuplas (id, vector, metadata)

        Returns:
            Resumen de la operación
        """
        if not vectors:
            return {"upserted_count": 0}

        print(f"📤 Subiendo {len(vectors)} vectores a Pinecone...")

        # Pinecone acepta batches de hasta 100 vectores
        batch_size = 100
        total_upserted = 0

        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]

            try:
                response = self.index.upsert(vectors=batch)
                total_upserted += response.upserted_count
                print(f"   ✅ Batch {i // batch_size + 1}: {response.upserted_count} vectores")
            except Exception as e:
                print(f"   ❌ Error en batch {i // batch_size + 1}: {e}")

        print(f"✅ Total vectores subidos: {total_upserted}")

        return {"upserted_count": total_upserted}

    def load_from_embeddings_file(self, embeddings_file: Path) -> Dict:
        """
        Carga vectores desde un archivo de embeddings y los sube a Pinecone

        Args:
            embeddings_file: Archivo JSON con chunks y embeddings

        Returns:
            Resumen de la carga
        """
        print(f"\n📥 Cargando embeddings desde: {embeddings_file.name}")

        with open(embeddings_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        # Preparar vectores para Pinecone
        vectors = []

        for chunk in chunks:
            if "embedding" not in chunk:
                print(f"⚠️  Chunk sin embedding: {chunk.get('chunk_id', 'unknown')}")
                continue

            # ID único
            vector_id = chunk["chunk_id"]

            # Vector de embeddings
            vector = chunk["embedding"]

            # Metadata (Pinecone tiene límites: solo strings, numbers, bools, lists)
            metadata = {
                "text": chunk["text"][:1000],  # Primeros 1000 chars (límite Pinecone)
                "source": chunk["metadata"].get("source", "unknown"),
                "law_name": chunk["metadata"].get("law_name", "unknown"),
                "category": chunk["metadata"].get("category", "general"),
                "chunk_number": chunk.get("chunk_number", 0),
                "total_chunks": chunk.get("total_chunks", 0),
                "url": chunk["metadata"].get("url", ""),
            }

            # Agregar article_number si existe
            if chunk["metadata"].get("article_number"):
                metadata["article_number"] = str(chunk["metadata"]["article_number"])

            vectors.append((vector_id, vector, metadata))

        # Subir a Pinecone
        result = self.upsert_vectors(vectors)

        return {
            "file": str(embeddings_file),
            "total_chunks": len(chunks),
            "vectors_upserted": result["upserted_count"]
        }

    def load_all_embeddings(self, embeddings_dir: Path) -> List[Dict]:
        """
        Carga todos los archivos de embeddings de un directorio

        Args:
            embeddings_dir: Directorio con archivos *_embedded.json

        Returns:
            Lista de resúmenes de carga
        """
        embedding_files = list(embeddings_dir.glob("*_embedded.json"))

        if not embedding_files:
            print(f"⚠️  No se encontraron archivos de embeddings en {embeddings_dir}")
            return []

        print(f"\n🚀 Cargando {len(embedding_files)} archivos a Pinecone...\n")

        summaries = []

        for emb_file in embedding_files:
            try:
                summary = self.load_from_embeddings_file(emb_file)
                summaries.append(summary)
            except Exception as e:
                print(f"❌ Error cargando {emb_file.name}: {e}")

        return summaries

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Busca vectores similares en Pinecone

        Args:
            query_vector: Vector de la consulta
            top_k: Número de resultados a devolver
            filter: Filtros de metadata (ej: {"category": "laboral"})

        Returns:
            Lista de resultados con scores y metadata
        """
        try:
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter,
                include_metadata=True
            )

            # Formatear resultados
            matches = []
            for match in results.matches:
                matches.append({
                    "id": match.id,
                    "score": match.score,
                    "text": match.metadata.get("text", ""),
                    "source": match.metadata.get("source", ""),
                    "law_name": match.metadata.get("law_name", ""),
                    "category": match.metadata.get("category", ""),
                    "url": match.metadata.get("url", ""),
                    "article_number": match.metadata.get("article_number")
                })

            return matches

        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []

    def get_stats(self) -> Dict:
        """Obtiene estadísticas del índice"""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}


def main():
    """Script principal para cargar vectores a Pinecone"""
    print("=" * 60)
    print("PINECONE VECTOR STORE - LEIA")
    print("=" * 60)

    # Verificar API key
    if not os.getenv("PINECONE_API_KEY"):
        print("\n❌ ERROR: PINECONE_API_KEY no configurada")
        print("\nPara configurar:")
        print("1. Ve a: https://app.pinecone.io")
        print("2. Crea cuenta gratuita")
        print("3. Crea API key en Settings")
        print("4. Agrégala a backend/.env:")
        print("   PINECONE_API_KEY=tu-api-key")
        print("\n" + "=" * 60)
        return

    if not PINECONE_AVAILABLE:
        print("\n❌ ERROR: Pinecone no instalado")
        print("\nPara instalar:")
        print("   pip install pinecone-client")
        print("\n" + "=" * 60)
        return

    try:
        # Inicializar vector store
        vector_store = VectorStore()

        # Cargar todos los embeddings
        embeddings_dir = Path("data/embeddings")

        if not embeddings_dir.exists():
            print(f"\n❌ Directorio no encontrado: {embeddings_dir}")
            print("Primero ejecuta embedder.py para generar embeddings")
            return

        summaries = vector_store.load_all_embeddings(embeddings_dir)

        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)

        total_chunks = sum(s["total_chunks"] for s in summaries)
        total_upserted = sum(s["vectors_upserted"] for s in summaries)

        print(f"Total chunks procesados: {total_chunks}")
        print(f"Vectores subidos a Pinecone: {total_upserted}")

        print(f"\nArchivos cargados:")
        for summary in summaries:
            print(f"  • {Path(summary['file']).name}: {summary['vectors_upserted']} vectores")

        # Estadísticas del índice
        stats = vector_store.get_stats()
        if stats:
            print(f"\n📈 Estadísticas del índice:")
            print(f"  • Total vectores: {stats['total_vectors']}")
            print(f"  • Dimensiones: {stats['dimension']}")
            print(f"  • Capacidad usada: {stats['index_fullness'] * 100:.2f}%")

        print("\n✅ Vector store listo para búsquedas!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n❌ {e}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("=" * 60)


if __name__ == "__main__":
    main()
