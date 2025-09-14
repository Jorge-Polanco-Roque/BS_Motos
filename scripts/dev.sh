#!/bin/bash
# dev.sh - Script para desarrollo Docker-First

echo "🏍️  BS Motos - Desarrollo Docker"
echo "================================="

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

# Verificar API key (opcional para desarrollo)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY no está configurada"
    echo "💡 Para desarrollo puedes continuar sin API key"
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ OpenAI API Key configurada (${OPENAI_API_KEY:0:8}...)"
fi

echo "🚀 Iniciando dashboard en modo desarrollo..."
echo "📱 URL: http://localhost:8502"
echo "🔄 Código se recarga automáticamente"
echo "🛑 Para detener: Ctrl+C"
echo "================================="

# Ejecutar en modo desarrollo con código en tiempo real
docker-compose --profile dev up --build bs-motos-dev