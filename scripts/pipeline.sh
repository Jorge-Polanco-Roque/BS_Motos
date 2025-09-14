#!/bin/bash
# pipeline.sh - Script para ejecutar el pipeline de procesamiento

echo "🏍️  BS Motos - Pipeline de Procesamiento"
echo "========================================="

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

# Verificar API key (requerida para pipeline)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY es requerida para el pipeline"
    echo "💡 Soluciones:"
    echo "   1. Crear archivo .env: ./scripts/setup-secure.sh"
    echo "   2. Export manual: export OPENAI_API_KEY='tu_api_key'"
    echo "   3. Obtener key en: https://platform.openai.com/api-keys"
    exit 1
fi

echo "✅ OpenAI API Key configurada (${OPENAI_API_KEY:0:8}...)"

# Verificar archivo de entrada
INPUT_FILE="${1:-inputs/tabla_test.csv}"
OUTPUT_FILE="${2:-outputs/output_final.csv}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: Archivo de entrada no encontrado: $INPUT_FILE"
    echo "📁 Archivos disponibles en inputs/:"
    ls -la inputs/ 2>/dev/null || echo "   (directorio inputs/ no existe)"
    echo ""
    echo "💡 Uso: $0 [archivo_entrada] [archivo_salida]"
    echo "💡 Ejemplo: $0 inputs/tabla_test.csv outputs/resultado.csv"
    exit 1
fi

# Crear directorio de salida si no existe
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "📥 Archivo de entrada: $INPUT_FILE"
echo "📤 Archivo de salida: $OUTPUT_FILE"
echo "🔄 Procesando con OpenAI API..."
echo "⏱️  Esto puede tomar varios minutos..."
echo "========================================="

# Ejecutar pipeline
docker-compose --profile pipeline run --rm bs-motos-pipeline \
  python pipeline.py "$INPUT_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Pipeline completado exitosamente"
    echo "📄 Resultado guardado en: $OUTPUT_FILE"
    echo "🚀 Ahora puedes ejecutar: ./scripts/run.sh"
else
    echo ""
    echo "❌ Error en el pipeline"
    echo "🔍 Revisa los logs arriba para más detalles"
    exit 1
fi