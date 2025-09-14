#!/bin/bash
# clean.sh - Script para limpiar contenedores y volúmenes Docker

echo "🏍️  BS Motos - Limpieza Docker"
echo "==============================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "💡 Inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

echo "🧹 Deteniendo servicios BS Motos..."
docker-compose down

echo "🗑️  Limpiando contenedores detenidos..."
docker container prune -f

echo "🗑️  Limpiando imágenes sin usar..."
docker image prune -f

echo "🗑️  Limpiando volúmenes sin usar..."
docker volume prune -f

echo "🗑️  Limpiando networks sin usar..."
docker network prune -f

# Opción para limpieza completa
read -p "¿Realizar limpieza completa? (elimina TODAS las imágenes sin usar) (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Realizando limpieza completa..."
    docker system prune -a -f
    echo "✅ Limpieza completa terminada"
else
    echo "✅ Limpieza básica terminada"
fi

# Mostrar uso actual de espacio
echo ""
echo "📊 Uso actual de espacio Docker:"
docker system df

echo ""
echo "💡 Para reconstruir las imágenes BS Motos:"
echo "   ./scripts/run.sh"