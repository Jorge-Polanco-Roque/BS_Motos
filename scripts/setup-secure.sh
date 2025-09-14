#!/bin/bash
# setup-secure.sh - Configuración segura de API key

echo "🔐 BS Motos - Configuración Segura de API Key"
echo "=============================================="

echo "Métodos disponibles:"
echo "1. 🥇 Variable de entorno del sistema (MÁS SEGURO)"
echo "2. 🥈 Archivo .env local (SEGURO para desarrollo)" 
echo "3. 🥉 Configuración manual"
echo ""

read -p "Selecciona método (1-3): " method

case $method in
    1)
        echo ""
        echo "🥇 Configurando variable de entorno del sistema..."
        echo ""
        read -p "Ingresa tu OpenAI API Key: " -s api_key
        echo ""
        
        # Detectar shell
        if [[ $SHELL == *"zsh"* ]]; then
            shell_config="$HOME/.zshrc"
        else
            shell_config="$HOME/.bashrc"
        fi
        
        echo "# BS Motos OpenAI API Key" >> "$shell_config"
        echo "export OPENAI_API_KEY=\"$api_key\"" >> "$shell_config"
        
        echo "✅ API key agregada a $shell_config"
        echo "💡 Ejecuta: source $shell_config"
        echo "💡 O reinicia tu terminal"
        ;;
        
    2) 
        echo ""
        echo "🥈 Configurando archivo .env local..."
        echo ""
        read -p "Ingresa tu OpenAI API Key: " -s api_key
        echo ""
        
        # Crear archivo .env
        cat > .env << EOF
# BS Motos - Variables de entorno
# NUNCA commitear este archivo

# OpenAI API Key (requerido para pipeline)
OPENAI_API_KEY=$api_key

# Configuración opcional de Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
EOF

        chmod 600 .env  # Solo el propietario puede leer
        echo "✅ Archivo .env creado con permisos seguros"
        ;;
        
    3)
        echo ""
        echo "🥉 Configuración manual..."
        echo "Copia .env.example a .env y edita manualmente:"
        echo "  cp .env.example .env"
        echo "  nano .env"
        ;;
        
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "🔒 RECORDATORIOS DE SEGURIDAD:"
echo "• NUNCA commitees tu API key al repositorio"
echo "• NUNCA compartas tu .env en chats/emails"
echo "• Si la key se compromete, regenerala en OpenAI"
echo "• El archivo .env ya está en .gitignore"
echo ""
echo "✅ Configuración completada. Ahora puedes ejecutar:"
echo "  ./scripts/run.sh"