#!/usr/bin/env python3
"""
Script para generar prompts basados en datos JSON de encuestas.

Este script toma el archivo de salida del script anterior (JSON en CSV),
crea una copia y agrega una nueva columna 'prompt' que combina un template
de prompt personalizado con los datos JSON de cada persona.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


class PromptBuilder:
    """Generador de prompts para análisis de datos de encuestas sobre motos."""
    
    def __init__(self, input_file: str, output_file: str = "2_output.csv"):
        """
        Inicializa el constructor de prompts.
        
        Args:
            input_file: Ruta al archivo CSV con datos JSON
            output_file: Ruta al archivo CSV de salida con prompts
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self._validate_input_file()
    
    def _validate_input_file(self) -> None:
        """Valida que el archivo de entrada exista y sea válido."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.input_file}")
        
        if not self.input_file.suffix.lower() == '.csv':
            raise ValueError("El archivo debe tener extensión .csv")
    
    def _get_strategic_questions(self) -> List[Dict[str, Any]]:
        """
        Define las 10 preguntas categóricas mejoradas para análisis de comportamiento del consumidor de motos.
        
        Returns:
            Lista de diccionarios con preguntas categóricas y opciones de respuesta definidas
        """
        return [
            {
                "pregunta": "¿Con qué frecuencia consultas redes sociales antes de tomar decisiones de compra de motos?",
                "tema": "Influencia Digital",
                "opciones": ["Siempre", "Frecuentemente", "Ocasionalmente", "Raramente", "Nunca"]
            },
            {
                "pregunta": "¿Qué tan importante es para ti pertenecer a una comunidad de propietarios de tu marca de moto?",
                "tema": "Comunidad de Marca",
                "opciones": ["Muy importante", "Importante", "Moderadamente importante", "Poco importante", "Nada importante"]
            },
            {
                "pregunta": "¿Cuál es tu nivel de interés en personalizar o modificar tu moto con accesorios oficiales?",
                "tema": "Personalización",
                "opciones": ["Muy alto interés", "Alto interés", "Interés moderado", "Bajo interés", "Sin interés"]
            },
            {
                "pregunta": "¿Qué tipo de promoción te motivaría más a elegir una marca específica de moto?",
                "tema": "Promociones y Incentivos", 
                "opciones": ["Descuentos directos en precio", "Regalos incluidos (casco, accesorios)", "Programas de puntos/lealtad", "Garantía extendida gratuita", "Financiamiento con 0% interés"]
            },
            {
                "pregunta": "¿En qué fuente confías más para obtener información sobre marcas de motos?",
                "tema": "Fuentes de Información",
                "opciones": ["Reseñas de otros usuarios en línea", "Recomendaciones de familiares/amigos", "Pruebas y reviews de expertos", "Publicidad oficial de la marca", "Experiencia personal previa"]
            },
            {
                "pregunta": "¿Qué factor de imagen de marca es más relevante para ti al elegir una moto?",
                "tema": "Imagen y Estatus",
                "opciones": ["Prestigio y reconocimiento", "País de origen (japonesa, europea, etc.)", "Asociación con deportes/competencias", "Sostenibilidad y responsabilidad ambiental", "Relación calidad-precio"]
            },
            {
                "pregunta": "¿Cuál de estos servicios adicionales considerarías más valioso al comprar una moto?",
                "tema": "Servicios de Valor Agregado",
                "opciones": ["Asistencia en carretera 24/7", "Mantenimiento a domicilio", "Seguro contra robo incluido", "Servicio de rastreo GPS", "Capacitación de manejo gratuita"]
            },
            {
                "pregunta": "¿Qué tipo de endorsement te influenciaría más en la decisión de compra de una moto?",
                "tema": "Endorsements e Influencia",
                "opciones": ["Pilotos profesionales famosos", "Influencers motociclistas", "Recomendación de mecánicos expertos", "Patrocinio en competencias", "Testimonios de usuarios reales"]
            },
            {
                "pregunta": "¿Cuál es tu nivel de preocupación por el impacto ambiental al elegir una marca de moto?",
                "tema": "Conciencia Ambiental",
                "opciones": ["Muy preocupado", "Preocupado", "Moderadamente preocupado", "Poco preocupado", "Nada preocupado"]
            },
            {
                "pregunta": "¿Cuál es tu canal de compra preferido para adquirir una moto nueva?",
                "tema": "Canal de Compra",
                "opciones": ["Concesionario físico tradicional", "Venta online con entrega a domicilio", "Ferias y eventos de motos", "Compra directa al fabricante", "Plataformas de comercio electrónico"]
            }
        ]
    
    def _create_prompt_template(self, persona_data: Dict[str, Any], question_data: Dict[str, Any]) -> str:
        """
        Crea un prompt personalizado basado en TODOS los datos de la persona y una pregunta categórica.
        
        Args:
            persona_data: Diccionario con datos de la persona encuestada
            question_data: Diccionario con pregunta categórica y opciones de respuesta
            
        Returns:
            String con el prompt generado
        """
        # Extraer información demográfica básica
        edad = persona_data.get('Edad', 'N/A')
        sexo = persona_data.get('Sexo', 'N/A')
        plaza = persona_data.get('Plaza', 'N/A')
        estado_civil = persona_data.get('Cual_es_su_estado_conyugal_Respuesta_unica', 'N/A')
        educacion = persona_data.get('Nivel_educativo_terminado_Respuesta_unica', 'N/A')
        situacion_laboral = persona_data.get('Situacion_laboral_Respuesta_unica', 'N/A')
        
        # Información sobre su moto actual
        marcas_conoce = persona_data.get('Podria_decirme_que_marcas_de_motos_conoce_o_recuerda_TOM_RU_y_espontanea', 'N/A')
        marca_actual = persona_data.get('Cual_es_la_marca_de_su_moto_RU_y_espontanea_ultima_moto_adquirida', 'N/A')
        razones_compra = persona_data.get('Por_que_razones_escogio_comprar_su_moto_de_la_marca…_mencionar_marca_actual_del_encuestado_…_RM_y_ESPONTANEA_marcar_opciones_acordes_a_la_mencion', 'N/A')
        satisfaccion = persona_data.get('Que_tan_satisfecho_esta_actualmente_con_la_moto_que_posee_RU_asistida', 'N/A')
        recomendacion = persona_data.get('Basado_en_tu_experiencia_con_su_moto_…._mencionar_la_marca_de_moto__que_tanto_recomendarias_comprar_esta_marca_a_un_familiar_o_amigo_en_una_escala_del_0_al_10_Donde_10_es_la_maxima_puntuacion_RU_espontanea', 'N/A')
        
        # Importancia de diferentes aspectos (1-5)
        imp_marca = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_1._Marca_reputacion_y_procedencia', 'N/A')
        imp_reventa = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_2._Valor_de_reventa', 'N/A')
        imp_diseno = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_3._Diseno', 'N/A')
        imp_garantia = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_4._Anos_de_garantia', 'N/A')
        imp_precio = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_7._Precio', 'N/A')
        imp_combustible = persona_data.get('De_los_siguientes_aspectos_en_una_escala_del_1_al_5_en_donde_1_es_"Nada_Importante"_y_5_es_"Muy_importante_Que_tan_importante_considera_…_RU_por_atributo_y_ASISTIDA_6._Rendimiento_del_combustible', 'N/A')
        
        # Comportamientos de uso y compra
        motivo_compra = persona_data.get('Por_que_motivo_compro_su_moto_RM_y_espontanea', 'N/A')
        frecuencia_uso = persona_data.get('Con_que_frecuencia_utiliza_su_moto_RU_y_asistida', 'N/A')
        factores_decision = persona_data.get('Cual_o_cuales_de_los_siguientes_factores_influyeron_en_su_decision_para_comprar_su_moto_RM_y_espontanea', 'N/A')
        planes_reventa = persona_data.get('Tiene_pensado_revender_su_moto_RU_y_asistida', 'N/A')
        presupuesto_nueva = persona_data.get('Cuanto_estaria_dispuesto_a_pagar_por_una_nueva_moto_RU_y_asistida', 'N/A')
        financiamiento = persona_data.get('Compraria_una_moto_financiada_RU_y_asistida', 'N/A')
        
        # Búsqueda de información y mantenimiento
        fuentes_info = persona_data.get('A_traves_de_que_medios_busca_informacion_de_las_ultimas_actualizaciones_en_motos_RM_y_espontanea', 'N/A')
        lugar_mantenimiento = persona_data.get('A_donde_lleva_su_moto_para_realizarle_el_mantenimiento_preventivo_RU_y_asistida', 'N/A')
        elementos_proteccion = persona_data.get('Que_elementos_de_proteccion_utiliza_RM_y_espontanea', 'N/A')
        
        # Obtener datos de la pregunta categórica
        tema = question_data['tema']
        pregunta = question_data['pregunta']
        opciones = question_data['opciones']
        
        # Generar listado de opciones con letras
        opciones_formateadas = ""
        for i, opcion in enumerate(opciones):
            letra = chr(65 + i)  # A, B, C, D, E
            opciones_formateadas += f"{letra}. {opcion}\n"
        
        # Template de prompt específico para pregunta categórica
        prompt = f"""Actúas como un buyer persona basado en datos reales de investigación de mercado de motocicletas. Tu perfil está definido por los datos de encuesta proporcionados, y debes responder desde la perspectiva de esta persona específica.

TU PERFIL COMPLETO COMO BUYER PERSONA:

📋 INFORMACIÓN DEMOGRÁFICA:
- Persona: {sexo}, {edad} años
- Ubicación: {plaza}  
- Estado civil: {estado_civil}
- Educación: {educacion}
- Situación laboral: {situacion_laboral}

🏍️ EXPERIENCIA ACTUAL CON MOTOS:
- Marcas que conoce: {marcas_conoce}
- Marca actual: {marca_actual}
- Razones de compra anterior: {razones_compra}
- Nivel de satisfacción: {satisfaccion}
- Recomendaría su marca (0-10): {recomendacion}

💰 COMPORTAMIENTO DE COMPRA:
- Motivo de compra: {motivo_compra}
- Frecuencia de uso: {frecuencia_uso}
- Factores de decisión: {factores_decision}
- Planes de reventa: {planes_reventa}
- Presupuesto nueva moto: {presupuesto_nueva}
- Financiamiento: {financiamiento}

⚖️ IMPORTANCIA DE ASPECTOS (escala 1-5):
- Marca/reputación: {imp_marca}
- Precio: {imp_precio}
- Valor de reventa: {imp_reventa}
- Diseño: {imp_diseno}
- Garantía: {imp_garantia}
- Rendimiento combustible: {imp_combustible}

🔍 INFORMACIÓN Y MANTENIMIENTO:
- Fuentes de información: {fuentes_info}
- Lugar de mantenimiento: {lugar_mantenimiento}
- Elementos de protección: {elementos_proteccion}

CONTEXTO ESPECÍFICO - {tema.upper()}:
Basándote en tu perfil completo (demográfico, socioeconómico, experiencia con motos, comportamientos de compra e importancia que das a diferentes aspectos), responde la siguiente pregunta de investigación de mercado.

PREGUNTA:
{pregunta}

OPCIONES DE RESPUESTA:
{opciones_formateadas}

INSTRUCCIONES PARA TU RESPUESTA:
1. Analiza la pregunta considerando TODA tu información personal detallada
2. Evalúa cómo tu experiencia actual con motos influye en tu decisión
3. Considera tus comportamientos de compra y preferencias específicas
4. Ten en cuenta la importancia que das a diferentes aspectos (precio, marca, etc.)
5. Piensa en tu situación económica actual y presupuesto disponible
6. Considera tu contexto geográfico (Piura, Perú) y social

CRITERIOS DE DECISIÓN ESPECÍFICOS:
- Usa tu satisfacción actual ({satisfaccion}) y recomendación ({recomendacion}/10) como referencia
- Considera tu presupuesto ({presupuesto_nueva}) y actitud hacia financiamiento ({financiamiento})
- Ten en cuenta qué aspectos valoras más: marca ({imp_marca}), precio ({imp_precio}), etc.
- Piensa en tus fuentes de información habituales: {fuentes_info}
- Considera tu frecuencia de uso actual: {frecuencia_uso}
- Mantén coherencia con tus razones de compra anteriores: {razones_compra}

FORMATO DE RESPUESTA OBLIGATORIO:
Responde EXACTAMENTE en este formato JSON:
{{
    "respuesta_elegida": "Letra de la opción elegida (A, B, C, D o E)",
    "opcion_completa": "Texto completo de la opción seleccionada",
    "confianza": "Alta/Media/Baja",
    "razonamiento": "Explica tu elección referenciando aspectos específicos de tu perfil (marca actual, satisfacción, presupuesto, importancia que das a diferentes aspectos, etc.)"
}}

IMPORTANTE: 
- Tu respuesta debe ser coherente con TODOS los datos de tu perfil
- Menciona en el razonamiento aspectos específicos como tu marca actual, nivel de satisfacción, o importancia que das a ciertos aspectos
- La respuesta debe reflejar una persona real con experiencias y preferencias específicas
- Sé consistente con tu personalidad a través de las 10 preguntas"""

        return prompt
    
    def _process_json_row(self, json_string: str) -> Dict[str, Any]:
        """
        Procesa una fila JSON y maneja posibles errores de formato.
        
        Args:
            json_string: String JSON de la fila
            
        Returns:
            Diccionario con los datos parseados
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error al procesar JSON: {e}")
            return {}
    
    def build_prompts(self) -> None:
        """
        Procesa el archivo de entrada y genera 10 columnas de prompts para cada registro.
        """
        try:
            print(f"Leyendo archivo: {self.input_file}")
            
            # Leer el archivo CSV con los datos JSON
            df = pd.read_csv(self.input_file, encoding='utf-8')
            
            if 'json' not in df.columns:
                raise ValueError("El archivo debe contener una columna 'json'")
            
            print(f"Archivo leído correctamente. Registros: {len(df)}")
            
            # Crear una copia del DataFrame original
            output_df = df.copy()
            
            # Obtener las preguntas estratégicas
            strategic_questions = self._get_strategic_questions()
            
            # Generar columnas de prompts para cada pregunta
            print("Generando 10 columnas de prompts...")
            
            for question_idx, question_data in enumerate(strategic_questions, 1):
                column_name = f"prompt_pregunta_{question_idx}"
                prompts_for_question = []
                
                print(f"Generando prompts para tema {question_idx}: {question_data['tema']}")
                
                for idx, row in df.iterrows():
                    json_string = row['json']
                    
                    # Parsear el JSON
                    persona_data = self._process_json_row(json_string)
                    
                    if persona_data:
                        # Generar prompt para esta persona y este tema específico
                        prompt = self._create_prompt_template(persona_data, question_data)
                        prompts_for_question.append(prompt)
                    else:
                        # Si hay error en el JSON, agregar mensaje de error
                        prompts_for_question.append("ERROR: No se pudo procesar el JSON de este registro")
                    
                    # Mostrar progreso cada 100 registros para cada pregunta
                    if (idx + 1) % 100 == 0:
                        print(f"  Procesados {idx + 1}/{len(df)} registros para pregunta {question_idx}...")
                
                # Agregar la columna de prompts al DataFrame
                output_df[column_name] = prompts_for_question
            
            # Guardar el archivo de salida
            output_df.to_csv(self.output_file, index=False, encoding='utf-8')
            
            print(f"\n✅ Prompts generados exitosamente!")
            print(f"Archivo de salida: {self.output_file}")
            print(f"Total de registros procesados: {len(df)}")
            print(f"Total de columnas de prompts: 10")
            print(f"Columnas en archivo final: {list(output_df.columns)}")
            
        except Exception as e:
            print(f"❌ Error durante el procesamiento: {str(e)}", file=sys.stderr)
            raise
    
    def preview_prompts(self, num_samples: int = 1) -> None:
        """
        Muestra una vista previa de los prompts generados para las 10 preguntas.
        
        Args:
            num_samples: Número de personas (registros) a mostrar como muestra
        """
        try:
            df = pd.read_csv(self.input_file, encoding='utf-8')
            strategic_questions = self._get_strategic_questions()
            
            print(f"\nVista previa de prompts para {min(num_samples, len(df))} registro(s):")
            print("=" * 120)
            
            for sample_idx in range(min(num_samples, len(df))):
                json_string = df.iloc[sample_idx]['json']
                persona_data = self._process_json_row(json_string)
                
                if persona_data:
                    edad = persona_data.get('Edad', 'N/A')
                    sexo = persona_data.get('Sexo', 'N/A')
                    plaza = persona_data.get('Plaza', 'N/A')
                    
                    print(f"\n🧑 BUYER PERSONA {sample_idx + 1}: {sexo}, {edad} años, {plaza}")
                    print("=" * 120)
                    
                    # Mostrar resumen de los 10 temas para esta persona
                    for q_idx, question_data in enumerate(strategic_questions, 1):
                        print(f"\n📋 PROMPT_PREGUNTA_{q_idx} - TEMA: {question_data['tema']}")
                        print(f"   Sub-preguntas: {len(question_data['sub_preguntas'])} preguntas dicotómicas")
                        print("-" * 80)
                        
                        # Generar y mostrar primeras líneas del prompt
                        prompt = self._create_prompt_template(persona_data, question_data)
                        
                        prompt_lines = prompt.split('\n')
                        # Mostrar las primeras 8 líneas como vista previa
                        for line in prompt_lines[:8]:
                            print(f"   {line}")
                        if len(prompt_lines) > 8:
                            print("   ... [prompt continúa con perfil completo y lineamientos] ...")
                        print()
                
        except Exception as e:
            print(f"Error al generar vista previa: {str(e)}", file=sys.stderr)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Genera estadísticas sobre los prompts que se van a crear.
        
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        try:
            df = pd.read_csv(self.input_file, encoding='utf-8')
            strategic_questions = self._get_strategic_questions()
            
            # Procesar algunos registros para obtener estadísticas
            sample_data = []
            for idx in range(min(10, len(df))):
                json_string = df.iloc[idx]['json']
                persona_data = self._process_json_row(json_string)
                if persona_data:
                    sample_data.append(persona_data)
            
            # Extraer estadísticas básicas
            stats = {
                "total_registros": len(df),
                "total_prompts_a_generar": len(df) * len(strategic_questions),
                "columnas_prompt_a_crear": len(strategic_questions),
                "registros_muestra": len(sample_data),
                "campos_promedio_por_persona": len(sample_data[0]) if sample_data else 0,
                "ubicaciones_encontradas": list(set([p.get('Plaza', 'N/A') for p in sample_data])),
                "marcas_encontradas": list(set([p.get('Cual_es_la_marca_de_su_moto_RU_y_espontanea_ultima_moto_adquirida', 'N/A') for p in sample_data])),
                "temas_preguntas": [q['tema'] for q in strategic_questions],
                "total_sub_preguntas": sum(len(q['sub_preguntas']) for q in strategic_questions)
            }
            
            return stats
            
        except Exception as e:
            print(f"Error al calcular estadísticas: {str(e)}", file=sys.stderr)
            return {}


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("Uso: python 2_building_prompt.py <archivo_json_csv> [archivo_salida.csv]")
        print("Ejemplo: python 2_building_prompt.py 1_output.csv 2_output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "2_output.csv"
    
    try:
        # Crear instancia del constructor de prompts
        prompt_builder = PromptBuilder(input_file, output_file)
        
        # Mostrar estadísticas
        print("=== ESTADÍSTICAS DEL DATASET ===")
        stats = prompt_builder.get_statistics()
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Mostrar vista previa
        print("\n=== VISTA PREVIA DE PROMPTS ===")
        prompt_builder.preview_prompts(1)
        
        # Generar prompts
        print("\n=== GENERANDO PROMPTS ===")
        prompt_builder.build_prompts()
        
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()