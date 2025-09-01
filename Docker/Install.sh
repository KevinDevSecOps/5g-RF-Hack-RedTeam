#!/bin/bash
# Script de instalación rápida para 5G RF RedTeam Toolkit

echo "🚀 Instalando 5G RF RedTeam Toolkit..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Crear directorios necesarios
mkdir -p data logs tmp

# Construir la imagen Docker
echo "📦 Construyendo imagen Docker..."
docker-compose -f docker/docker-compose.yml build

if [ $? -eq 0 ]; then
    echo "✅ Imagen Docker construida exitosamente"
else
    echo "❌ Error construyendo la imagen Docker"
    exit 1
fi

# Iniciar el contenedor
echo "🐳 Iniciando contenedor..."
docker-compose -f docker/docker-compose.yml up -d

if [ $? -eq 0 ]; then
    echo "✅ Contenedor iniciado exitosamente"
    echo "🌐 Dashboard disponible en: http://localhost:5000"
    echo "📊 Accede al panel de control para comenzar el scanning"
else
    echo "❌ Error iniciando el contenedor"
    exit 1
fi

echo "🎉 Instalación completada!"
echo "Para ver los logs: docker-compose -f docker/docker-compose.yml logs -f"
echo "Para detener: docker-compose -f docker/docker-compose.yml down"