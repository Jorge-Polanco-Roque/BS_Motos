#!/bin/bash
# run.sh - Script para ejecutar dashboard en producción

echo "🏍️  BS Motos - Dashboard Producción"
echo "===================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "💡 Inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

# Cargar variables de entorno si existe .env
if [ -f ".env" ]; then
    echo "📋 Cargando variables de entorno desde .env"
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

# Verificar API key (opcional para dashboard)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY no está configurada"
    echo "💡 Soluciones:"
    echo "   1. Crear archivo .env: ./scripts/setup-secure.sh"
    echo "   2. Export manual: export OPENAI_API_KEY='tu_api_key'"
    echo ""
    read -p "¿Continuar sin API key? (dashboard funcionará en modo solo-visualización) (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ OpenAI API Key configurada (${OPENAI_API_KEY:0:8}...)"
fi

# Verificar si hay datos
if [ ! -f "output_final.csv" ]; then
    echo "⚠️  No se encontró output_final.csv"
    echo "💡 Ejecuta primero: ./scripts/pipeline.sh"
    echo "💡 O el dashboard permitirá subir archivos manualmente"
fi

echo "🚀 Iniciando dashboard..."
echo "📱 URL: http://localhost:8501"
echo "🛑 Para detener: Ctrl+C"
echo "===================================="

# Ejecutar dashboard principal
docker-compose up --build bs-motos-dashboard