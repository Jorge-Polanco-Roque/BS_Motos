# 🏍️ BS Motos - Sistema de Análisis de Encuestas

**Enfoque Docker-First**: Sistema completo de procesamiento y análisis de encuestas de motocicletas usando OpenAI API y visualización interactiva con Streamlit.

## 🎯 ¿Qué hace este proyecto?

1. **Procesa datos de encuestas** de CSV a formato estructurado
2. **Genera respuestas inteligentes** usando OpenAI GPT-3.5-turbo con 10 preguntas categóricas
3. **Visualiza resultados** en un dashboard profesional e interactivo
4. **Todo funciona con Docker** - sin instalaciones locales de Python

---

## 🚀 Inicio Súper Rápido (Docker-First)

### **Setup inicial (una sola vez):**
```bash
# 1. Clonar y navegar
git clone [repo-url]
cd BS_Motos

# 2. Setup automático
./scripts/setup.sh

# 3. Configurar API key
nano .env  # Editar OPENAI_API_KEY=tu_api_key_aqui
```

### **Uso diario:**
```bash
# Dashboard para visualización
./scripts/run.sh
# → http://localhost:8501

# Procesamiento de datos
./scripts/pipeline.sh
# → Genera output_final.csv

# Desarrollo con recarga automática
./scripts/dev.sh
# → http://localhost:8502
```

---

## 📋 Requisitos Mínimos

- **Docker Desktop** instalado y corriendo
- **OpenAI API Key** - [Obtener aquí](https://platform.openai.com) (solo para procesamiento)
- **Archivos CSV** en directorio `inputs/`

**¡Eso es todo!** Cero instalaciones de Python, pip, dependencias locales.

---

## 🐳 Servicios Docker Disponibles

### **1. Dashboard Principal** (`./scripts/run.sh`)
- **Puerto**: 8501
- **Uso**: Visualización y análisis de datos
- **Comando**: `docker-compose up bs-motos-dashboard`

### **2. Pipeline de Procesamiento** (`./scripts/pipeline.sh`)
- **Función**: Procesa CSV → JSON → Prompts → Respuestas OpenAI
- **Comando**: `docker-compose --profile pipeline run bs-motos-pipeline`

### **3. Desarrollo** (`./scripts/dev.sh`)  
- **Puerto**: 8502
- **Función**: Recarga automática de código
- **Comando**: `docker-compose --profile dev up bs-motos-dev`

---

## 📁 Estructura del Proyecto

```
BS_Motos/                    # 🐳 Docker-First Architecture
├── 🔧 DOCKER
│   ├── Dockerfile           # Imagen principal Python + deps
│   ├── docker-compose.yml   # 3 servicios: dashboard, pipeline, dev
│   ├── start.sh            # Script inicialización contenedor
│   └── requirements.txt     # Dependencias Python únicas
│
├── 📊 PIPELINE
│   ├── pipeline.py         # Script principal unificado
│   ├── 1_building_json.py  # CSV → JSON
│   ├── 2_building_prompt.py # JSON → Prompts personalizados  
│   └── 3_building_output.py # Prompts → Respuestas OpenAI
│
├── 📈 DASHBOARD
│   └── dashboard.py        # Streamlit app principal (Docker-only)
│
├── 🛠️ SCRIPTS
│   ├── setup.sh           # Configuración inicial
│   ├── run.sh             # Dashboard producción
│   ├── dev.sh             # Desarrollo con hot-reload
│   ├── pipeline.sh        # Procesamiento de datos
│   └── clean.sh           # Limpieza Docker
│
└── 📄 DATOS
    ├── inputs/             # CSV de entrada (tabla_test.csv, tabla_1.csv)
    ├── outputs/            # Resultados procesados por pipeline  
    ├── output_final.csv    # Dataset activo para dashboard
    └── .env               # Variables de entorno (API keys)
```

---

## 🎮 Casos de Uso Docker-First

### **Demo rápida** (sin procesamiento):
```bash
./scripts/run.sh  # Dashboard con datos existentes
```

### **Análisis completo** (con OpenAI):
```bash
./scripts/pipeline.sh inputs/tabla_test.csv outputs/resultado.csv
./scripts/run.sh
```

### **Desarrollo** (modificar código):
```bash
./scripts/dev.sh  # Auto-recarga al cambiar archivos
```

### **Producción** (servidor):
```bash
export OPENAI_API_KEY="sk-..."
docker-compose up -d bs-motos-dashboard
# → Ejecuta en background
```

---

## 📊 Funcionalidades del Sistema

### **🔄 Pipeline de Procesamiento**
1. **CSV → JSON**: Convierte datos de encuesta a estructura JSON
2. **Prompts personalizados**: Usa TODOS los datos por persona
3. **OpenAI Integration**: 10 preguntas categóricas sobre motocicletas:
   - Influencia Digital | Canal de Compra | Comunidad de Marca
   - Personalización | Promociones | Fuentes de Información  
   - Imagen y Estatus | Servicios | Endorsements | Conciencia Ambiental

### **📈 Dashboard Interactivo**
- **Análisis Demográfico**: Edad, género, educación, marcas
- **Análisis de Respuestas**: Distribución, confianza, razonamientos
- **Filtros Avanzados**: Por pregunta, nivel de confianza
- **Métricas en Tiempo Real**: 500+ estadísticas automatizadas

---

## 🐛 Solución de Problemas Docker-First

### **Error: "Docker not running"**
```bash
# Iniciar Docker Desktop
open -a Docker  # macOS
# o iniciar Docker Desktop manualmente
```

### **Error: "API Key not found"**
```bash
# Verificar configuración
cat .env | grep OPENAI_API_KEY

# Configurar correctamente
echo "OPENAI_API_KEY=sk-tu_api_key" >> .env
```

### **Error: "Puerto en uso"**
```bash
# Ver procesos
lsof -i :8501

# Usar script de limpieza
./scripts/clean.sh
```

### **Limpieza completa**
```bash
./scripts/clean.sh  # Elimina contenedores/imágenes sin usar
```

---

## 📈 Rendimiento y Costos

### **Procesamiento con OpenAI API**
- **Dataset pequeño** (20 registros): 2-3 minutos | ~$0.05
- **Dataset completo** (535 registros): 45-60 minutos | ~$0.25
- **Modelo usado**: GPT-3.5-turbo (optimizado para costo/calidad)

### **Recursos Docker**
- **RAM**: ~512MB por contenedor
- **CPU**: Mínimo 1 core
- **Disco**: ~2GB para imagen + datos

---

## 🔒 Seguridad Docker-First

### **Variables de entorno protegidas**
```bash
# ✅ Correcto - usando .env
OPENAI_API_KEY=sk-real-key

# ❌ Incorrecto - nunca en código
OPENAI_API_KEY="sk-real-key"  # en archivos .py
```

### **Contenedores aislados**
- Cada servicio en contenedor separado
- Network aislado `bs-motos-network`
- Volúmenes controlados para datos

---

## 🚀 Comandos de Referencia Rápida

### **Scripts automatizados (recomendado):**
```bash
# 🔧 SETUP
./scripts/setup.sh              # Configuración inicial
nano .env                       # Configurar API key

# 🎯 USO DIARIO
./scripts/dashboard-only.sh     # Solo visualización (sin API key)
./scripts/run.sh                # Dashboard completo
./scripts/pipeline.sh           # Procesar datos nuevos
./scripts/dev.sh                # Desarrollo con hot-reload

# 🧹 MANTENIMIENTO  
./scripts/clean.sh              # Limpiar Docker
```

### **Docker directo (avanzado):**
```bash
# Dashboard sin API key
docker run -p 8501:8501 -v $(pwd)/output_final.csv:/app/output_final.csv:ro bs-motos-analytics

# Pipeline completo  
export OPENAI_API_KEY="sk-tu_key"
docker-compose --profile pipeline run bs-motos-pipeline python pipeline.py inputs/tabla_test.csv outputs/resultado.csv

# Debug y monitoreo
docker-compose logs -f          # Ver logs
docker exec -it bs_motos_dashboard bash  # Acceder al contenedor
docker-compose ps               # Estado servicios
```

### **Gestión de datos:**
```bash
# Cambiar dataset activo
cp outputs/mi_archivo.csv output_final.csv
./scripts/run.sh

# Procesar múltiples archivos
./scripts/pipeline.sh inputs/dataset_A.csv outputs/resultado_A.csv
./scripts/pipeline.sh inputs/dataset_B.csv outputs/resultado_B.csv
```

---

## 🎉 Ventajas Docker-First

### **Para Desarrolladores**
- ✅ **Cero setup local** - Solo Docker
- ✅ **Entorno reproducible** - Funciona igual en cualquier máquina
- ✅ **Desarrollo aislado** - Sin contaminar sistema local
- ✅ **Hot-reload** - Cambios en vivo

### **Para Producción** 
- ✅ **Despliegue simple** - Una imagen, cualquier servidor
- ✅ **Escalabilidad** - Múltiples réplicas fácil
- ✅ **Monitoreo** - Logs centralizados
- ✅ **Rollback rápido** - Versiones de imagen

### **Para Demos/Clientes**
- ✅ **Instalación en 1 comando** - `./scripts/setup.sh`
- ✅ **Sin dependencias** - Solo Docker
- ✅ **Portable** - Funciona en Mac, Windows, Linux

---

## 📞 Soporte y Contacto

**Desarrollado por**: Jorge Polanco Roque  
**Arquitectura**: Docker-First BS Motos Survey Analytics

### **Para reportar problemas:**
```bash
# Incluir información del sistema
docker --version
docker-compose --version
docker system info
docker-compose logs bs-motos-dashboard
```

---

## 🏃‍♂️ **¡Comenzar AHORA!**

```bash
# ========================================
# SETUP INICIAL (solo una vez)
# ========================================

# 1. Clonar y navegar
git clone [repo-url] && cd BS_Motos

# 2. Setup automático
./scripts/setup.sh

# 3. Configurar API key
./scripts/setup-secure.sh  # Opción 2: archivo .env

# ========================================
# GENERAR DATOS (cuando tengas datos nuevos)
# ========================================

# 4. Generar output_final.csv con datos de prueba
./scripts/pipeline.sh inputs/tabla_test.csv outputs/test_result.csv
cp outputs/test_result.csv output_final.csv

# ========================================
# DASHBOARD (las veces que quieras)
# ========================================

# 5. Lanzar dashboard
./scripts/dashboard-only.sh

# 6. Abrir navegador
# http://localhost:8501

# ✅ ¡LISTO! Dashboard funcionando con tus datos
```

---

## 📝 **Comandos de Verificación**

### **Verificar que todo funciona:**
```bash
# Docker funcionando
docker --version

# API key configurada
echo $OPENAI_API_KEY | head -c 8  # Debería mostrar "sk-..."

# Archivos necesarios
ls inputs/tabla_test.csv output_final.csv

# Estado de contenedores
docker-compose ps
```

### **Si algo falla:**
```bash
# Ver logs
docker-compose logs -f

# Limpiar y reiniciar
./scripts/clean.sh
./scripts/setup.sh

# Debug - acceder al contenedor
docker exec -it bs_motos_dashboard bash
```

---

## ⏱️ **Tiempos Esperados**

- **Setup inicial**: 2-3 minutos
- **Pipeline con tabla_test.csv (20 registros)**: 2-3 minutos
- **Pipeline con tabla_1.csv (535 registros)**: 45-60 minutos  
- **Dashboard**: 10-15 segundos para arrancar

---

## 💡 **Tips**

### **Para desarrollo:**
- Usa `tabla_test.csv` para pruebas rápidas
- Usa `./scripts/dev.sh` para modificar código
- Mantén varios archivos procesados en `outputs/`

### **Para producción:**
- Usa `tabla_1.csv` para dataset completo
- Usa `./scripts/run.sh` para dashboard estable
- Haz backup de `output_final.csv`

### **Para demos:**
- Usa `./scripts/dashboard-only.sh` (no necesita API key)
- Sube archivos desde la interfaz web si no tienes datos

**¡Siguiendo estos pasos tendrás tu sistema BS Motos funcionando perfectamente!** 🏍️✨

---

*BS Motos v2.0 - Docker-First Architecture | Powered by OpenAI API + Streamlit*