#!/usr/bin/env python3
"""
pipeline.py - BS Motos Complete Pipeline

Pipeline completo que ejecuta los 3 scripts en secuencia:
1. 1_building_json.py - Convierte CSV a JSON
2. 2_building_prompt.py - Genera prompts categóricos
3. 3_building_output.py - Ejecuta prompts con OpenAI API

El resultado final es un CSV con:
- Columna 'json': datos originales
- 10 columnas 'prompt_pregunta_X': prompts generados
- 10 columnas 'respuesta_pregunta_X': respuestas de OpenAI

"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class BSMotosPipeline:
    """
    Pipeline completo para procesamiento de encuestas de motos con OpenAI
    """
    
    def __init__(self, input_csv="inputs/tabla_1.csv", output_file="test_1_output.csv"):
        """
        Inicializa el pipeline
        
        Args:
            input_csv: Archivo CSV de entrada
            output_file: Archivo CSV único que se irá actualizando
        """
        self.input_csv = input_csv
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Un solo archivo que se actualiza en cada paso
        self.output_file = output_file
        
        self._validate_environment()
    
    def _validate_environment(self):
        """
        Valida que el entorno esté correctamente configurado
        """
        print("🔍 Validando entorno...")
        
        # Verificar archivo de entrada
        if not os.path.exists(self.input_csv):
            raise FileNotFoundError(f"❌ Archivo de entrada no encontrado: {self.input_csv}")
        
        # Verificar scripts principales
        scripts = ["1_building_json.py", "2_building_prompt.py", "3_building_output.py"]
        for script in scripts:
            if not os.path.exists(script):
                raise FileNotFoundError(f"❌ Script no encontrado: {script}")
        
        # Verificar y probar API key de OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY no encontrada en variables de entorno")
        
        print("✅ Archivos y dependencias validados")
        
        # PRUEBA REAL DE OPENAI API KEY
        print("🔑 Probando conexión con OpenAI API...")
        self._test_openai_connection(api_key)
        
        print("✅ Entorno completamente validado")
    
    def _test_openai_connection(self, api_key):
        """
        Prueba real de conexión con OpenAI API
        """
        try:
            import openai
            from openai import OpenAI
            
            print("   📡 Iniciando conexión...")
            print(f"   📦 OpenAI version: {openai.__version__}")
            try:
                client = OpenAI(api_key=api_key)
                print("   ✅ Cliente OpenAI creado exitosamente")
            except Exception as e:
                print(f"   ❌ Error creando cliente: {e}")
                raise
            
            print("   🧪 Enviando prompt de prueba...")
            # Prueba simple y rápida
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Responde únicamente 'OK' si entiendes este mensaje."},
                    {"role": "user", "content": "Test de conexión BS Motos Pipeline"}
                ],
                max_tokens=5,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip()
            print(f"   📝 Respuesta recibida: '{result}'")
            
            if response and response.choices:
                print(f"   ✅ API KEY VÁLIDA - Conexión exitosa")
                print(f"   📊 Modelo: gpt-3.5-turbo")
                print(f"   💰 Tokens usados: {response.usage.total_tokens}")
            else:
                raise ValueError("Respuesta vacía de OpenAI")
                
        except ImportError:
            raise ImportError("❌ Error: librería 'openai' no instalada. Ejecutar: pip install openai")
            
        except Exception as e:
            print(f"   ❌ Error probando OpenAI API: {e}")
            print(f"   🚫 VERIFICAR:")
            print(f"      • API key correcta en .env")
            print(f"      • Saldo suficiente en cuenta OpenAI") 
            print(f"      • Conexión a internet activa")
            raise ValueError(f"❌ OPENAI_API_KEY no funciona: {e}")
    
    def run_command_with_realtime_logs(self, command, description):
        """
        Ejecuta un comando del sistema mostrando logs en tiempo real
        
        Args:
            command: Lista con comando y argumentos
            description: Descripción del paso para logging
            
        Returns:
            bool: True si el comando fue exitoso
        """
        print(f"\n{'='*60}")
        print(f"🚀 {description}")
        print(f"📝 Ejecutando: {' '.join(command)}")
        print(f"{'='*60}")
        print("📊 Logs en tiempo real:")
        
        start_time = time.time()
        
        try:
            # Ejecutar proceso con salida en tiempo real
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Leer salida línea por línea en tiempo real
            output_lines = []
            while True:
                line = process.stdout.readline()
                if line:
                    print(f"   {line.rstrip()}")
                    output_lines.append(line.rstrip())
                elif process.poll() is not None:
                    break
            
            # Esperar a que termine el proceso
            return_code = process.wait()
            
            execution_time = time.time() - start_time
            
            if return_code == 0:
                print(f"✅ Completado en {execution_time:.2f} segundos")
                return True
            else:
                print(f"❌ Error: código de salida {return_code}")
                return False
            
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return False
    
    def step1_convert_csv_to_json(self):
        """
        Paso 1: Convierte CSV original a formato JSON
        """
        print(f"📄 Archivo actual: {self.output_file} (se creará con datos JSON)")
        command = ["python", "1_building_json.py", self.input_csv, self.output_file]
        return self.run_command_with_realtime_logs(command, "PASO 1: Conversión CSV → JSON")
    
    def step2_generate_prompts(self):
        """
        Paso 2: Genera prompts categóricos y actualiza el mismo archivo
        """
        print(f"📄 Archivo actual: {self.output_file} (se actualizará con 10 columnas de prompts)")
        command = ["python", "2_building_prompt.py", self.output_file, self.output_file]
        return self.run_command_with_realtime_logs(command, "PASO 2: Generación de Prompts Categóricos")
    
    def step3_execute_prompts(self):
        """
        Paso 3: Ejecuta prompts REALES con OpenAI API y actualiza el mismo archivo
        """
        print(f"📄 Archivo actual: {self.output_file} (se actualizará con 10 columnas de respuestas)")
        print(f"🔥 PROCESAMIENTO REAL CON OPENAI API - SIN SIMULACIÓN")
        print(f"⚠️  Este paso utilizará la API de OpenAI y puede tomar varios minutos")
        
        command = ["python", "3_building_output.py", self.output_file, self.output_file]
        
        # Ejecutar proceso con logs en tiempo real y auto-confirmación
        start_time = time.time()
        
        try:
            print(f"\n{'='*60}")
            print(f"🚀 PASO 3: Ejecución REAL de Prompts con OpenAI API")
            print(f"📝 Ejecutando: {' '.join(command)}")
            print(f"{'='*60}")
            print("📊 Logs REALES en tiempo real:")
            
            # Ejecutar proceso con salida en tiempo real y input automático
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Enviar 's' automáticamente para confirmar procesamiento
            process.stdin.write("s\n")
            process.stdin.flush()
            process.stdin.close()
            
            # Leer salida línea por línea en tiempo real
            while True:
                line = process.stdout.readline()
                if line:
                    # Resaltar líneas importantes
                    line_stripped = line.rstrip()
                    if "✅" in line_stripped or "Respuesta:" in line_stripped:
                        print(f"   🎯 {line_stripped}")
                    elif "❌" in line_stripped or "Error" in line_stripped:
                        print(f"   🚨 {line_stripped}")
                    elif "📊" in line_stripped or "Progreso" in line_stripped:
                        print(f"   📈 {line_stripped}")
                    else:
                        print(f"   {line_stripped}")
                elif process.poll() is not None:
                    break
            
            return_code = process.wait()
            execution_time = time.time() - start_time
            
            if return_code == 0:
                print(f"✅ PROCESAMIENTO REAL COMPLETADO en {execution_time/60:.2f} minutos")
                return True
            else:
                print(f"❌ Error en procesamiento real: código de salida {return_code}")
                return False
            
        except Exception as e:
            print(f"❌ Error ejecutando paso 3 real: {e}")
            return False
    
    def run_complete_pipeline(self):
        """
        Ejecuta el pipeline completo
        """
        print("🏍️  BS MOTOS - PIPELINE REAL CON OPENAI API")
        print("="*60)
        print(f"📥 Archivo de entrada: {self.input_csv}")
        print(f"📄 Archivo único de trabajo: {self.output_file}")
        print(f"🔥 PROCESAMIENTO: 100% REAL - SIN SIMULACIÓN")
        print(f"⚠️  USAR API REAL DE OPENAI - CONSUMIRÁ TOKENS")
        print(f"🕐 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        pipeline_start = time.time()
        
        # Ejecutar pasos secuencialmente
        steps = [
            ("Paso 1", self.step1_convert_csv_to_json),
            ("Paso 2", self.step2_generate_prompts), 
            ("Paso 3", self.step3_execute_prompts)
        ]
        
        for step_name, step_function in steps:
            print(f"\n🔄 Iniciando {step_name}...")
            if not step_function():
                print(f"\n❌ PIPELINE FALLÓ en {step_name}")
                print("🛑 Abortando ejecución...")
                return False
            
            # Mostrar estado del archivo después de cada paso
            if os.path.exists(self.output_file):
                import pandas as pd
                df = pd.read_csv(self.output_file, encoding='utf-8')
                print(f"📊 Estado actual del archivo {self.output_file}:")
                print(f"   • Registros: {len(df)}")
                print(f"   • Columnas: {len(df.columns)}")
                print(f"   • Columnas actuales: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
        
        # Pipeline completado exitosamente
        total_time = time.time() - pipeline_start
        
        print(f"\n{'='*60}")
        print("🎉 ¡PIPELINE REAL COMPLETADO EXITOSAMENTE!")
        print(f"🔥 PROCESAMIENTO 100% REAL CON OPENAI API")
        print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
        print(f"📄 Archivo final único: {self.output_file}")
        print("="*60)
        
        # Mostrar información del archivo final
        if os.path.exists(self.output_file):
            import pandas as pd
            df = pd.read_csv(self.output_file, encoding='utf-8')
            print(f"📈 Estadísticas del archivo final:")
            print(f"   • Registros procesados: {len(df)}")
            print(f"   • Columnas totales: {len(df.columns)}")
            
            # Contar columnas por tipo
            json_cols = [col for col in df.columns if col == 'json']
            prompt_cols = [col for col in df.columns if col.startswith('prompt_pregunta_')]
            response_cols = [col for col in df.columns if col.startswith('respuesta_pregunta_')]
            
            print(f"   • Columnas JSON: {len(json_cols)}")
            print(f"   • Columnas Prompts: {len(prompt_cols)}")
            print(f"   • Columnas Respuestas: {len(response_cols)}")
            
            print(f"\n📋 Estructura final del archivo:")
            print(f"   Columnas: {', '.join(df.columns)}")
        
        return True
    
    def cleanup_intermediate_files(self):
        """
        Ya no hay archivos intermedios, todo está en un solo archivo
        """
        print(f"\n✅ Solo hay un archivo de trabajo: {self.output_file}")
        print("📁 No hay archivos intermedios que limpiar")
        print(f"🎯 Resultado final disponible en: {self.output_file}")

def main():
    """
    Función principal
    """
    # Configuración por defecto
    input_file = "inputs/tabla_1.csv"
    output_file = "test_1_output.csv"
    
    # Permitir argumentos personalizados
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        # Crear y ejecutar pipeline
        pipeline = BSMotosPipeline(input_csv=input_file, output_file=output_file)
        
        if pipeline.run_complete_pipeline():
            # Mostrar resumen final
            pipeline.cleanup_intermediate_files()
        else:
            print("\n💥 El pipeline falló. Revisar errores arriba.")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error crítico en el pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()