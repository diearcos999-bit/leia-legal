#!/bin/bash
# Script para iniciar el backend de JusticiaAI

cd "$(dirname "$0")"
source venv/bin/activate
echo "🚀 Iniciando JusticiaAI Backend..."
echo "📍 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
python main_simple.py
