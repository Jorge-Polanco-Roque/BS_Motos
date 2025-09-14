#!/bin/bash
# setup.sh - Script de configuración inicial Docker-First

echo "🏍️  BS Motos - Setup Inicial Docker-First"
echo "=========================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "💡 Inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

echo "✅ Docker está ejecutándose"

# Verificar Docker Compose
if ! docker-compose --version > /dev/null 2>&1; then
    echo "❌ Error: Docker Compose no está disponible"
    echo "💡 Instala Docker Desktop que incluye Docker Compose"
    exit 1
fi

echo "✅ Docker Compose está disponible"

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p inputs
mkdir -p outputs

# Configurar archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📋 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env y configura tu OPENAI_API_KEY"
    echo "💡 Obtén tu API key en: https://platform.openai.com"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar archivos de datos
echo "📊 Verificando archivos de datos..."
if [ -f "inputs/tabla_test.csv" ]; then
    echo "✅ Archivo de prueba encontrado: inputs/tabla_test.csv"
else
    echo "⚠️  Archivo de prueba no encontrado: inputs/tabla_test.csv"
    echo "💡 Asegúrate de tener archivos CSV en el directorio inputs/"
fi

# Hacer ejecutables los scripts
echo "🔧 Configurando permisos de scripts..."
chmod +x scripts/*.sh

# Construir imagen Docker
echo "🐳 Construyendo imagen Docker..."
echo "⏱️  Esto puede tomar unos minutos la primera vez..."
docker-compose build

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Setup completado exitosamente!"
    echo "=========================================="
    echo ""
    echo "📋 Próximos pasos:"
    echo "1. Configurar API key: nano .env"
    echo "2. Ejecutar dashboard: ./scripts/run.sh"
    echo "3. O procesar datos: ./scripts/pipeline.sh"
    echo ""
    echo "🚀 Comandos disponibles:"
    echo "   ./scripts/run.sh        - Dashboard en producción"
    echo "   ./scripts/dev.sh        - Desarrollo con recarga automática"
    echo "   ./scripts/pipeline.sh   - Procesar datos con OpenAI"
    echo "   ./scripts/clean.sh      - Limpiar contenedores"
    echo ""
    echo "💡 URLs:"
    echo "   Dashboard: http://localhost:8501"
    echo "   Desarrollo: http://localhost:8502"
    echo ""
else
    echo ""
    echo "❌ Error durante la construcción de la imagen"
    echo "🔍 Revisa los logs arriba para más detalles"
    exit 1
fi