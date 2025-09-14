# 🔐 Guía de Seguridad - BS Motos

## 🎯 Gestión Segura de OpenAI API Key

### **🚨 NUNCA HAGAS ESTO:**
```bash
❌ export OPENAI_API_KEY="sk-1234..." && git add . && git commit
❌ echo "OPENAI_API_KEY=sk-real-key" > config.py
❌ Compartir .env por email/chat
❌ Hardcodear API key en archivos Python
```

### **✅ MÉTODOS SEGUROS:**

#### **🥇 Opción 1: Variable de entorno del sistema (RECOMENDADO)**
```bash
# Setup automático
./scripts/setup-secure.sh

# O manual - agregar a ~/.zshrc o ~/.bashrc
export OPENAI_API_KEY="sk-tu_api_key_aqui"
source ~/.zshrc

# Verificar
echo $OPENAI_API_KEY
```

#### **🥈 Opción 2: Archivo .env local**
```bash
# Setup automático
./scripts/setup-secure.sh

# O manual
cp .env.example .env
nano .env  # Editar API key
chmod 600 .env  # Permisos seguros
```

#### **🥉 Opción 3: Docker secrets (Producción avanzada)**
```bash
# Para producción en servidores
echo "sk-tu_api_key" | docker secret create openai_api_key -
```

---

## 🛡️ Verificación de Seguridad

### **Verificar que .env está protegido:**
```bash
# Debe estar en .gitignore
grep -n "\.env" .gitignore

# Debe tener permisos restrictivos
ls -la .env  # Debería mostrar -rw-------
```

### **Verificar que no hay keys en código:**
```bash
# Buscar keys accidentalmente commiteadas
git grep -n "sk-" 
git grep -n "OPENAI_API_KEY.*=" -- "*.py"

# No debería encontrar nada
```

### **Audit log de Docker:**
```bash
# Ver que no se loguea la API key
docker-compose logs | grep -i "api"
# No debería mostrar keys reales
```

---

## 🚨 Si tu API Key se compromete:

### **Pasos inmediatos:**
1. **Ir a OpenAI Dashboard**: https://platform.openai.com/api-keys
2. **Revocar la key comprometida** inmediatamente  
3. **Crear nueva API key**
4. **Actualizar tu configuración**:
   ```bash
   # Método sistema
   nano ~/.zshrc  # Actualizar export OPENAI_API_KEY="nueva_key"
   
   # Método .env
   nano .env      # Actualizar OPENAI_API_KEY=nueva_key
   ```
5. **Verificar billing** para actividad no autorizada

---

## 🔒 Configuración Recomendada por Entorno

### **Desarrollo Local:**
```bash
# Usar .env con permisos restrictivos
chmod 600 .env
./scripts/run.sh
```

### **CI/CD (GitHub Actions):**
```yaml
# En GitHub: Settings > Secrets > Actions
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### **Servidor de Producción:**
```bash
# Variable de entorno del sistema
export OPENAI_API_KEY="sk-production-key"
docker-compose up -d
```

### **Docker Swarm/Kubernetes:**
```bash
# Docker secrets
echo "sk-prod-key" | docker secret create openai_key -
```

---

## 📊 Monitoreo de Uso

### **Verificar consumo de API:**
```bash
# Comando para verificar uso aproximado
echo "Revisa tu usage en: https://platform.openai.com/usage"
```

### **Logs de costo por dataset:**
```bash
# Ver logs del pipeline para estimar costos
docker-compose logs bs-motos-pipeline | grep -E "(Total|Cost|Tokens)"
```

---

## 🎯 Quick Security Checklist

- [ ] ✅ API key NO está en código Python
- [ ] ✅ `.env` está en `.gitignore`
- [ ] ✅ `.env` tiene permisos 600 (`-rw-------`)
- [ ] ✅ Variable de entorno del sistema configurada
- [ ] ✅ No hay keys en commits (`git grep "sk-"`)
- [ ] ✅ Billing alerts configurados en OpenAI
- [ ] ✅ Keys rotadas cada 90 días (buena práctica)

---

## 🚀 Setup Recomendado (Seguro y Rápido)

```bash
# 1. Configuración segura automática
./scripts/setup-secure.sh

# 2. Verificar configuración
echo $OPENAI_API_KEY | head -c 8  # Debería mostrar "sk-..."

# 3. Probar funcionamiento
./scripts/dashboard-only.sh  # Dashboard sin API (OK)
./scripts/pipeline.sh inputs/tabla_test.csv outputs/test.csv  # Con API

# 4. Verificar seguridad
grep -r "sk-" . --exclude-dir=.git --exclude="*.md" || echo "✅ No keys in code"
```

---

*Mantén tu API key segura. Es tu responsabilidad.* 🔐