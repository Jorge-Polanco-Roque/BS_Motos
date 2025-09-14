#!/usr/bin/env python3
"""
3_building_output.py - BS Motos Survey Response Generator

Este script ejecuta los prompts generados por 2_building_prompt.py y genera respuestas
usando OpenAI GPT-3.5-turbo. Crea columnas individuales para cada pregunta con las
respuestas en formato JSON estructurado.

Basado en ref.py como referencia para integración con OpenAI API.

Usage:
    python 3_building_output.py input_file.csv output_file.csv

Author: Jorge Polanco Roque
Email: jorge.polanco.roque@gmail.com
"""

import pandas as pd
import os
import sys
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

class SurveyResponseGenerator:
    """
    Clase para generar respuestas de encuestas usando prompts predefinidos
    """
    
    def __init__(self):
        """
        Inicializa el generador con configuración de OpenAI
        """
        # Cargar variables de entorno
        load_dotenv()
        
        # Inicializar cliente OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY no encontrada en variables de entorno")
            print("💡 Para Docker: docker run -e OPENAI_API_KEY=tu_api_key ...")
            print("💡 Para desarrollo: crea archivo .env con OPENAI_API_KEY=tu_api_key")
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")
        
        self.client = OpenAI(api_key=api_key)
        
        # Configuración del modelo
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 200
        self.temperature = 0.1  # Baja temperatura para respuestas más consistentes
        
    def execute_prompt(self, prompt_text, question_number, total_questions, record_index=None):
        """
        Ejecuta un prompt individual usando OpenAI API
        
        Args:
            prompt_text (str): El texto del prompt a ejecutar
            question_number (int): Número de pregunta actual
            total_questions (int): Total de preguntas
            record_index (int): Índice del registro actual
            
        Returns:
            str: Respuesta del modelo en formato JSON
        """
        try:
            # Mostrar progreso
            if record_index is not None:
                print(f"[Registro {record_index+1}] Pregunta {question_number}/{total_questions}: Procesando...")
            
            # Configurar el prompt del sistema para garantizar formato JSON
            system_prompt = """Eres un buyer persona que responde preguntas de investigación de mercado sobre motocicletas. 
            DEBES responder ÚNICAMENTE en formato JSON válido con la estructura exacta:
            {
                "respuesta_elegida": "Letra de la opción elegida (A, B, C, D o E)",
                "opcion_completa": "Texto completo de la opción seleccionada",
                "confianza": "Alta" o "Media" o "Baja",
                "razonamiento": "Una o dos frases explicando por qué elegiste esta opción"
            }
            
            NO agregues texto adicional fuera del JSON. NO uses markdown. Solo JSON puro."""
            
            # Realizar llamada a OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_text}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            result = response.choices[0].message.content.strip()
            
            # Validar que la respuesta es JSON válido
            try:
                parsed_json = json.loads(result)
                # Verificar estructura requerida
                required_keys = ["respuesta_elegida", "opcion_completa", "confianza", "razonamiento"]
                if all(key in parsed_json for key in required_keys):
                    print(f"    ✅ Respuesta: {parsed_json['respuesta_elegida']} - {parsed_json['opcion_completa'][:30]}... (Confianza: {parsed_json['confianza']})")
                    return result
                else:
                    print(f"    ⚠️  JSON incompleto, usando respuesta por defecto")
                    return self._get_default_response()
            except json.JSONDecodeError:
                print(f"    ⚠️  Respuesta no es JSON válido, usando respuesta por defecto")
                return self._get_default_response()
                
        except Exception as e:
            print(f"    ❌ Error ejecutando prompt: {e}")
            return self._get_default_response()
    
    def _get_default_response(self):
        """
        Genera una respuesta por defecto en caso de error
        
        Returns:
            str: JSON por defecto
        """
        default_response = {
            "respuesta_elegida": "A",
            "opcion_completa": "Opción no determinada",
            "confianza": "Baja", 
            "razonamiento": "No pude determinar una respuesta clara basada en mi perfil"
        }
        return json.dumps(default_response, ensure_ascii=False)
    
    def process_csv(self, input_file, output_file):
        """
        Procesa el archivo CSV con prompts y genera respuestas
        
        Args:
            input_file (str): Ruta del archivo CSV de entrada
            output_file (str): Ruta del archivo CSV de salida
        """
        try:
            # Leer archivo CSV
            print(f"📖 Leyendo archivo: {input_file}")
            df = pd.read_csv(input_file, encoding='utf-8')
            print(f"Total registros: {len(df)}")
            print(f"Columnas encontradas: {df.columns.tolist()}")
            
            # Identificar columnas de prompts
            prompt_columns = [col for col in df.columns if col.startswith('prompt_pregunta_')]
            prompt_columns.sort()  # Ordenar para procesamiento secuencial
            
            if not prompt_columns:
                raise ValueError("No se encontraron columnas con prompts (prompt_pregunta_*)")
            
            print(f"Columnas de prompts encontradas: {len(prompt_columns)}")
            for i, col in enumerate(prompt_columns, 1):
                print(f"  {i}. {col}")
            
            # Crear columnas de respuesta
            response_columns = []
            for prompt_col in prompt_columns:
                response_col = prompt_col.replace('prompt_pregunta_', 'respuesta_pregunta_')
                response_columns.append(response_col)
                df[response_col] = ""
            
            print(f"\n🚀 Iniciando procesamiento de {len(df)} registros...")
            print(f"Se procesarán {len(prompt_columns)} preguntas por registro")
            print(f"Total de llamadas a API: {len(df) * len(prompt_columns)}")
            
            # Mostrar vista previa
            if len(df) > 0:
                print("\n📋 Vista previa del primer registro:")
                print(f"JSON: {str(df.iloc[0]['json'])[:100]}...")
                if prompt_columns:
                    print(f"Primera pregunta: {str(df.iloc[0][prompt_columns[0]])[:100]}...")
            
            # Confirmar procesamiento
            confirm = input("\n¿Continuar con el procesamiento? (s/N): ").lower().strip()
            if confirm != 's':
                print("❌ Procesamiento cancelado por el usuario")
                return
            
            start_time = time.time()
            total_prompts = len(df) * len(prompt_columns)
            processed_prompts = 0
            
            # Procesar cada registro
            for record_index, row in df.iterrows():
                print(f"\n📝 Procesando registro {record_index + 1}/{len(df)}")
                
                # Procesar cada pregunta del registro
                for question_index, prompt_col in enumerate(prompt_columns):
                    prompt_text = row[prompt_col]
                    response_col = prompt_col.replace('prompt_pregunta_', 'respuesta_pregunta_')
                    
                    if pd.isna(prompt_text) or prompt_text.strip() == "":
                        print(f"  ⏭️  Pregunta {question_index + 1}: Prompt vacío, saltando...")
                        df.at[record_index, response_col] = self._get_default_response()
                    else:
                        # Ejecutar prompt
                        response = self.execute_prompt(
                            prompt_text, 
                            question_index + 1, 
                            len(prompt_columns),
                            record_index
                        )
                        df.at[record_index, response_col] = response
                    
                    processed_prompts += 1
                    
                    # Mostrar progreso general
                    progress = (processed_prompts / total_prompts) * 100
                    elapsed_time = time.time() - start_time
                    
                    if processed_prompts > 0:
                        estimated_total = (elapsed_time / processed_prompts) * total_prompts
                        remaining_time = estimated_total - elapsed_time
                        print(f"  📊 Progreso general: {progress:.1f}% - Tiempo restante: {remaining_time/60:.1f} min")
                    else:
                        print(f"  📊 Progreso general: {progress:.1f}% - Iniciando...")
                    
                    # Pequeña pausa para evitar rate limiting
                    time.sleep(0.1)
            
            # Guardar resultados
            print(f"\n💾 Guardando resultados en: {output_file}")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            # Mostrar estadísticas finales
            total_time = time.time() - start_time
            print(f"\n🎉 ¡Procesamiento completado exitosamente!")
            print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
            print(f"📊 Estadísticas:")
            print(f"   • Registros procesados: {len(df)}")
            print(f"   • Preguntas por registro: {len(prompt_columns)}")
            print(f"   • Total respuestas generadas: {processed_prompts}")
            print(f"   • Archivo de salida: {output_file}")
            
            # Mostrar vista previa de resultados
            print(f"\n📋 Vista previa de resultados:")
            if response_columns:
                sample_response = df.iloc[0][response_columns[0]]
                try:
                    parsed_sample = json.loads(sample_response)
                    print(f"   Ejemplo respuesta pregunta 1:")
                    print(f"   • Respuesta elegida: {parsed_sample.get('respuesta_elegida', 'N/A')}")
                    print(f"   • Opción: {parsed_sample.get('opcion_completa', 'N/A')}")
                    print(f"   • Confianza: {parsed_sample.get('confianza', 'N/A')}")
                    print(f"   • Razonamiento: {parsed_sample.get('razonamiento', 'N/A')}")
                except:
                    print(f"   Primera respuesta: {sample_response}")
            
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            raise

def main():
    """
    Función principal del script
    """
    if len(sys.argv) != 3:
        print("❌ Error: Número incorrecto de argumentos")
        print("📖 Uso: python 3_building_output.py <archivo_entrada.csv> <archivo_salida.csv>")
        print("📝 Ejemplo: python 3_building_output.py 2_output_dicotomic.csv 3_output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Verificar archivo de entrada
    if not os.path.exists(input_file):
        print(f"❌ Error: Archivo de entrada no encontrado: {input_file}")
        sys.exit(1)
    
    # Permitir que el archivo de entrada y salida sean el mismo (para pipeline unificado)
    if input_file == output_file:
        print(f"📄 Modo pipeline unificado: actualizando el mismo archivo ({input_file})")
    
    print("🏍️  BS Motos - Survey Response Generator")
    print("=" * 50)
    print(f"📥 Archivo de entrada: {input_file}")
    print(f"📤 Archivo de salida: {output_file}")
    print("=" * 50)
    
    try:
        # Crear generador y procesar
        generator = SurveyResponseGenerator()
        generator.process_csv(input_file, output_file)
        
    except Exception as e:
        print(f"\n❌ Error ejecutando el script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()