#!/usr/bin/env python3
"""
Document Loader - Carga apuntes y documentos legales en múltiples formatos

Formatos soportados:
- PDF (.pdf)
- Word (.docx)
- Texto plano (.txt)
- Markdown (.md)

Uso:
    python document_loader.py                    # Procesar todos los documentos
    python document_loader.py --folder civil     # Solo carpeta civil
    python document_loader.py --file archivo.pdf # Solo un archivo
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Intentar importar dependencias opcionales
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class DocumentLoader:
    """Carga y procesa documentos legales de múltiples formatos"""

    def __init__(self, output_dir: str = "data/raw/apuntes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_pdf(self, file_path: Path) -> Dict:
        """
        Extrae texto de un archivo PDF
        """
        if not PDF_AVAILABLE:
            print("⚠️  PyPDF2 no instalado. Ejecuta: pip install PyPDF2")
            return None

        try:
            text_content = []

            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                print(f"   📄 {num_pages} páginas encontradas")

                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text:
                        text_content.append(text)

            full_text = "\n\n".join(text_content)

            return {
                "title": file_path.stem,
                "content": full_text,
                "format": "pdf",
                "pages": num_pages,
                "file_path": str(file_path),
                "loaded_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"   ❌ Error leyendo PDF: {e}")
            return None

    def load_docx(self, file_path: Path) -> Dict:
        """
        Extrae texto de un archivo Word (.docx)
        """
        if not DOCX_AVAILABLE:
            print("⚠️  python-docx no instalado. Ejecuta: pip install python-docx")
            return None

        try:
            doc = Document(file_path)
            paragraphs = []

            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)

            full_text = "\n\n".join(paragraphs)

            return {
                "title": file_path.stem,
                "content": full_text,
                "format": "docx",
                "paragraphs": len(paragraphs),
                "file_path": str(file_path),
                "loaded_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"   ❌ Error leyendo DOCX: {e}")
            return None

    def load_text(self, file_path: Path) -> Dict:
        """
        Carga un archivo de texto plano (.txt o .md)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "title": file_path.stem,
                "content": content,
                "format": file_path.suffix[1:],  # txt o md
                "characters": len(content),
                "file_path": str(file_path),
                "loaded_at": datetime.now().isoformat()
            }

        except UnicodeDecodeError:
            # Intentar con latin-1 si UTF-8 falla
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                return {
                    "title": file_path.stem,
                    "content": content,
                    "format": file_path.suffix[1:],
                    "characters": len(content),
                    "file_path": str(file_path),
                    "loaded_at": datetime.now().isoformat()
                }
            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")
                return None

    def load_file(self, file_path: Path, category: str = "general") -> Optional[Dict]:
        """
        Carga un archivo detectando su formato automáticamente
        """
        suffix = file_path.suffix.lower()

        print(f"📥 Cargando: {file_path.name}")

        if suffix == '.pdf':
            data = self.load_pdf(file_path)
        elif suffix == '.docx':
            data = self.load_docx(file_path)
        elif suffix in ['.txt', '.md']:
            data = self.load_text(file_path)
        else:
            print(f"   ⚠️  Formato no soportado: {suffix}")
            return None

        if data:
            data["category"] = category
            data["source"] = "apuntes_abogado"

            # Estadísticas
            content_length = len(data.get("content", ""))
            words = len(data.get("content", "").split())
            print(f"   ✅ {words:,} palabras extraídas")

        return data

    def process_folder(self, folder_path: Path, category: str) -> List[Dict]:
        """
        Procesa todos los archivos de una carpeta
        """
        documents = []

        # Buscar archivos soportados
        patterns = ['*.pdf', '*.docx', '*.txt', '*.md']
        files = []
        for pattern in patterns:
            files.extend(folder_path.glob(pattern))

        if not files:
            print(f"   ⚠️  No se encontraron documentos en {folder_path}")
            return documents

        print(f"\n📂 Procesando carpeta: {category.upper()}")
        print(f"   {len(files)} archivos encontrados")
        print("-" * 40)

        for file_path in sorted(files):
            doc = self.load_file(file_path, category)
            if doc:
                documents.append(doc)

                # Guardar JSON individual
                output_file = self.output_dir / category / f"{file_path.stem}.json"
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(doc, f, ensure_ascii=False, indent=2)

        return documents

    def process_all(self) -> Dict:
        """
        Procesa todas las carpetas de apuntes
        """
        base_dir = self.output_dir
        categories = ['todos', 'civil', 'procesal', 'leyes', 'laboral', 'familia', 'consumidor', 'penal']

        all_documents = []
        summary = {
            "total_documents": 0,
            "total_words": 0,
            "by_category": {}
        }

        for category in categories:
            folder = base_dir / category
            if folder.exists():
                docs = self.process_folder(folder, category)
                all_documents.extend(docs)

                if docs:
                    words = sum(len(d.get("content", "").split()) for d in docs)
                    summary["by_category"][category] = {
                        "documents": len(docs),
                        "words": words
                    }

        summary["total_documents"] = len(all_documents)
        summary["total_words"] = sum(
            len(d.get("content", "").split())
            for d in all_documents
        )

        return summary


def check_dependencies():
    """Verifica e instala dependencias necesarias"""
    missing = []

    if not PDF_AVAILABLE:
        missing.append("PyPDF2")
    if not DOCX_AVAILABLE:
        missing.append("python-docx")

    if missing:
        print("\n⚠️  Dependencias faltantes para procesar documentos:")
        for dep in missing:
            print(f"   • {dep}")
        print(f"\nInstalar con: pip install {' '.join(missing)}")
        return False

    return True


def main():
    print("=" * 60)
    print("DOCUMENT LOADER - APUNTES LEGALES")
    print("=" * 60)

    parser = argparse.ArgumentParser(description="Cargar documentos legales")
    parser.add_argument("--folder", type=str, help="Procesar solo una carpeta")
    parser.add_argument("--file", type=str, help="Procesar solo un archivo")
    parser.add_argument("--check", action="store_true", help="Verificar dependencias")

    args = parser.parse_args()

    if args.check:
        check_dependencies()
        return

    loader = DocumentLoader()

    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            doc = loader.load_file(file_path, "manual")
            if doc:
                print(f"\n✅ Documento cargado: {doc['title']}")
                print(f"   Palabras: {len(doc['content'].split()):,}")
        else:
            print(f"❌ Archivo no encontrado: {file_path}")

    elif args.folder:
        folder_path = Path(f"data/raw/apuntes/{args.folder}")
        if folder_path.exists():
            docs = loader.process_folder(folder_path, args.folder)
            print(f"\n✅ {len(docs)} documentos procesados")
        else:
            print(f"❌ Carpeta no encontrada: {folder_path}")

    else:
        # Procesar todo
        summary = loader.process_all()

        print("\n" + "=" * 60)
        print("📊 RESUMEN")
        print("=" * 60)
        print(f"Total documentos: {summary['total_documents']}")
        print(f"Total palabras: {summary['total_words']:,}")

        if summary['by_category']:
            print("\nPor categoría:")
            for cat, data in summary['by_category'].items():
                print(f"   • {cat.upper()}: {data['documents']} docs, {data['words']:,} palabras")

        print("\n✅ Documentos listos para procesamiento!")
        print("   Ejecuta: python train_chatbot.py --step 2")
        print("=" * 60)


if __name__ == "__main__":
    main()
