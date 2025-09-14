#!/bin/bash
# start.sh - Script de inicialización para contenedor BS Motos

echo "🏍️  Iniciando BS Motos Survey Analytics Container"
echo "================================================="

# Verificar variables de entorno (OpenAI API solo para pipeline)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY no está definida"
    echo "💡 Dashboard funcionará en modo solo-visualización"
    echo "💡 Para procesar datos: docker run -e OPENAI_API_KEY=tu_api_key ..."
    DASHBOARD_ONLY_MODE=true
else
    echo "✅ OpenAI API Key configurada"
    DASHBOARD_ONLY_MODE=false
fi

# Crear directorios necesarios si no existen
mkdir -p /app/inputs
mkdir -p /app/outputs

echo "✅ Directorios creados"

# Verificar archivos necesarios
if [ ! -f "/app/dashboard.py" ]; then
    echo "❌ Error: dashboard.py no encontrado"
    exit 1
fi

echo "✅ Archivos verificados"

# Verificar si existe archivo de datos
if [ -f "/app/output_final.csv" ]; then
    echo "✅ Archivo de datos encontrado: output_final.csv"
else
    echo "⚠️  Archivo output_final.csv no encontrado"
    echo "💡 El dashboard puede funcionar subiendo archivos manualmente"
fi

# Configurar Streamlit
export STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}
export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-true}
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=${STREAMLIT_BROWSER_GATHER_USAGE_STATS:-false}

echo "✅ Configuración de Streamlit aplicada"

# Verificar dependencias críticas
if [ "$DASHBOARD_ONLY_MODE" = true ]; then
    python -c "import streamlit, pandas, plotly" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Dependencias de visualización verificadas"
    else
        echo "❌ Error: Faltan dependencias críticas para dashboard"
        exit 1
    fi
else
    python -c "import streamlit, pandas, plotly, openai" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Todas las dependencias verificadas"
    else
        echo "❌ Error: Faltan dependencias críticas"
        exit 1
    fi
fi

echo "================================================="
echo "🚀 Lanzando Dashboard en puerto $STREAMLIT_SERVER_PORT"
echo "📱 Accede desde: http://localhost:$STREAMLIT_SERVER_PORT"
echo "🛑 Para detener: Ctrl+C"
echo "================================================="

# Lanzar el dashboard
exec streamlit run dashboard.py \
    --server.port=$STREAMLIT_SERVER_PORT \
    --server.address=$STREAMLIT_SERVER_ADDRESS \
    --server.headless=$STREAMLIT_SERVER_HEADLESS \
    --browser.gatherUsageStats=$STREAMLIT_BROWSER_GATHER_USAGE_STATS