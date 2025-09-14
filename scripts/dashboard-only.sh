#!/bin/bash
# dashboard-only.sh - Solo dashboard, sin procesar datos

echo "🏍️  BS Motos - Dashboard (Solo Visualización)"
echo "=============================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "💡 Inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

echo "📊 Modo: Solo visualización de datos existentes"
echo "💡 Este script NO procesa datos nuevos"
echo ""

# Verificar si hay datos existentes
if [ -f "output_final.csv" ]; then
    echo "✅ Datos encontrados: output_final.csv"
    lines=$(wc -l < output_final.csv)
    echo "📄 Registros: $(($lines - 1)) personas encuestadas"
else
    echo "⚠️  No se encontró output_final.csv"
    echo ""
    echo "🔄 Para generar datos ejecuta:"
    echo "   ./scripts/pipeline.sh inputs/tabla_test.csv outputs/output_final.csv"
    echo ""
    echo "📤 O puedes subir archivos manualmente desde el dashboard"
fi

echo ""
echo "🚀 Lanzando dashboard..."
echo "📱 URL: http://localhost:8501"
echo "📤 Puedes subir archivos CSV desde la interfaz web"
echo "🛑 Para detener: Ctrl+C"
echo "=============================================="

# Ejecutar solo dashboard (sin API key requerida para visualización)
docker-compose up --build bs-motos-dashboard