#!/usr/bin/env python3
"""
dashboard.py - BS Motos Survey Analytics Dashboard

Dashboard profesional para visualizar los resultados del pipeline de encuestas
de motocicletas procesadas con OpenAI API.

Author: Jorge Polanco Roque
Email: jorge.polanco.roque@gmail.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
from collections import Counter
import sys
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="BS Motos - Survey Analytics",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para diseño profesional
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        text-transform: uppercase;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .question-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def load_data(file_path):
    """Carga y procesa los datos del archivo CSV"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Error cargando archivo: {e}")
        return None

def extract_demographics(df):
    """Extrae información demográfica del JSON"""
    demographics = []
    
    for idx, row in df.iterrows():
        try:
            json_data = json.loads(row['json'])
            demo = {
                'ID': json_data.get('ID', 'N/A'),
                'Plaza': json_data.get('Plaza', 'N/A'),
                'Sexo': json_data.get('Sexo', 'N/A'),
                'Edad': json_data.get('Edad', 'N/A'),
                'Estado_Civil': json_data.get('Cual_es_su_estado_conyugal_Respuesta_unica', 'N/A'),
                'Educacion': json_data.get('Nivel_educativo_terminado_Respuesta_unica', 'N/A'),
                'Situacion_Laboral': json_data.get('Situacion_laboral_Respuesta_unica', 'N/A'),
                'Marca_Actual': json_data.get('Cual_es_la_marca_de_su_moto_RU_y_espontanea_ultima_moto_adquirida', 'N/A'),
                'Satisfaccion': json_data.get('Que_tan_satisfecho_esta_actualmente_con_la_moto_que_posee_RU_asistida', 'N/A'),
                'Frecuencia_Uso': json_data.get('Con_que_frecuencia_utiliza_su_moto_RU_y_asistida', 'N/A'),
                'Presupuesto': json_data.get('Cuanto_estaria_dispuesto_a_pagar_por_una_nueva_moto_RU_y_asistida', 'N/A')
            }
            demographics.append(demo)
        except Exception as e:
            st.warning(f"Error procesando registro {idx}: {e}")
            
    return pd.DataFrame(demographics)

def extract_responses(df):
    """Extrae las respuestas elegidas de las 10 preguntas"""
    responses_data = []
    
    # Definir los nombres de las preguntas
    question_names = {
        'respuesta_pregunta_1': 'Influencia Digital',
        'respuesta_pregunta_2': 'Canal de Compra',
        'respuesta_pregunta_3': 'Comunidad de Marca',
        'respuesta_pregunta_4': 'Personalización',
        'respuesta_pregunta_5': 'Promociones y Incentivos',
        'respuesta_pregunta_6': 'Fuentes de Información',
        'respuesta_pregunta_7': 'Imagen y Estatus',
        'respuesta_pregunta_8': 'Servicios de Valor Agregado',
        'respuesta_pregunta_9': 'Endorsements e Influencia',
        'respuesta_pregunta_10': 'Conciencia Ambiental'
    }
    
    for idx, row in df.iterrows():
        user_responses = {'ID': idx + 1}
        
        for col_name, question_name in question_names.items():
            if col_name in df.columns:
                try:
                    resp_json = json.loads(row[col_name])
                    user_responses[question_name] = {
                        'respuesta_elegida': resp_json.get('respuesta_elegida', 'N/A'),
                        'opcion_completa': resp_json.get('opcion_completa', 'N/A'),
                        'confianza': resp_json.get('confianza', 'N/A'),
                        'razonamiento': resp_json.get('razonamiento', 'N/A')
                    }
                except:
                    user_responses[question_name] = {
                        'respuesta_elegida': 'N/A',
                        'opcion_completa': 'N/A',
                        'confianza': 'N/A',
                        'razonamiento': 'N/A'
                    }
        
        responses_data.append(user_responses)
    
    return responses_data, question_names

def create_demographics_dashboard(demo_df):
    """Crea el dashboard de demografía"""
    st.markdown('<div class="section-header">📊 Análisis Demográfico</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_respondents = len(demo_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_respondents}</div>
            <div class="metric-label">Total Encuestados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_age = demo_df['Edad'].apply(lambda x: int(x) if str(x).isdigit() else 0).mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">Edad Promedio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ciudades = demo_df['Plaza'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ciudades}</div>
            <div class="metric-label">Ciudades</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        marcas = demo_df['Marca_Actual'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{marcas}</div>
            <div class="metric-label">Marcas de Motos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos demográficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por género
        gender_counts = demo_df['Sexo'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values, 
            names=gender_counts.index,
            title="Distribución por Género",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_gender.update_layout(
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Distribución por educación
        edu_counts = demo_df['Educacion'].value_counts()
        fig_edu = px.bar(
            x=edu_counts.index, 
            y=edu_counts.values,
            title="Distribución por Nivel Educativo",
            color=edu_counts.values,
            color_continuous_scale="Blues"
        )
        fig_edu.update_layout(
            xaxis_title="Nivel Educativo",
            yaxis_title="Cantidad",
            font=dict(size=12),
            title_font_size=16,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_edu, use_container_width=True)
    
    # Fila adicional de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por situación laboral
        trabajo_counts = demo_df['Situacion_Laboral'].value_counts()
        fig_trabajo = px.bar(
            x=trabajo_counts.values,
            y=trabajo_counts.index,
            orientation='h',
            title="Distribución por Situación Laboral",
            color=trabajo_counts.values,
            color_continuous_scale="Greens"
        )
        fig_trabajo.update_layout(
            xaxis_title="Cantidad",
            yaxis_title="Situación Laboral",
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_trabajo, use_container_width=True)
    
    with col2:
        # Marcas de motos más populares
        marca_counts = demo_df['Marca_Actual'].value_counts().head(10)
        fig_marca = px.bar(
            x=marca_counts.index,
            y=marca_counts.values,
            title="Top Marcas de Motos",
            color=marca_counts.values,
            color_continuous_scale="Oranges"
        )
        fig_marca.update_layout(
            xaxis_title="Marca",
            yaxis_title="Cantidad",
            font=dict(size=12),
            title_font_size=16,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_marca, use_container_width=True)

def create_responses_dashboard(responses_data, question_names):
    """Crea el dashboard de respuestas"""
    st.markdown('<div class="section-header">🏍️ Análisis de Respuestas de Encuesta</div>', unsafe_allow_html=True)
    
    # Sidebar para filtros
    st.sidebar.markdown("### 🔍 Filtros")
    
    # Selector de pregunta
    selected_questions = st.sidebar.multiselect(
        "Seleccionar Preguntas:",
        list(question_names.values()),
        default=list(question_names.values())
    )
    
    # Filtro por confianza
    confidence_filter = st.sidebar.selectbox(
        "Filtrar por Confianza:",
        ["Todas", "Alta", "Media", "Baja"]
    )
    
    if not selected_questions:
        st.warning("⚠️ Por favor selecciona al menos una pregunta para visualizar.")
        return
    
    # Métricas de respuestas
    col1, col2, col3, col4 = st.columns(4)
    
    total_responses = len(responses_data) * len(selected_questions)
    high_confidence = 0
    unique_answers = set()
    total_reasoning_length = 0
    reasoning_count = 0
    
    for response in responses_data:
        for question in selected_questions:
            if question in response:
                if response[question]['confianza'] == 'Alta':
                    high_confidence += 1
                unique_answers.add(response[question]['respuesta_elegida'])
                # Calcular longitud promedio de razonamientos
                reasoning = response[question].get('razonamiento', '')
                if reasoning and reasoning != 'N/A':
                    total_reasoning_length += len(reasoning)
                    reasoning_count += 1
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_responses}</div>
            <div class="metric-label">Total Respuestas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence_rate = (high_confidence / total_responses * 100) if total_responses > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{confidence_rate:.1f}%</div>
            <div class="metric-label">Confianza Alta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(unique_answers)}</div>
            <div class="metric-label">Respuestas Únicas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_reasoning_length = (total_reasoning_length / reasoning_count) if reasoning_count > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_reasoning_length:.0f}</div>
            <div class="metric-label">Caracteres Promedio</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Crear visualizaciones para cada pregunta seleccionada
    for question in selected_questions:
        st.markdown(f'<div class="question-title">📋 {question}</div>', unsafe_allow_html=True)
        
        # Recopilar datos para esta pregunta
        question_responses = []
        question_confidence = []
        question_details = []
        
        for response in responses_data:
            if question in response:
                resp_data = response[question]
                if confidence_filter == "Todas" or resp_data['confianza'] == confidence_filter:
                    question_responses.append(resp_data['respuesta_elegida'])
                    question_confidence.append(resp_data['confianza'])
                    question_details.append({
                        'ID': response['ID'],
                        'Respuesta': resp_data['respuesta_elegida'],
                        'Opción': resp_data['opcion_completa'][:50] + "..." if len(resp_data['opcion_completa']) > 50 else resp_data['opcion_completa'],
                        'Confianza': resp_data['confianza'],
                        'Razonamiento': resp_data['razonamiento'][:100] + "..." if len(resp_data['razonamiento']) > 100 else resp_data['razonamiento']
                    })
        
        if question_responses:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de distribución de respuestas
                response_counts = Counter(question_responses)
                
                fig = px.bar(
                    x=list(response_counts.keys()),
                    y=list(response_counts.values()),
                    title=f"Distribución de Respuestas - {question}",
                    color=list(response_counts.values()),
                    color_continuous_scale="Viridis",
                    labels={'x': 'Respuesta Elegida', 'y': 'Cantidad'}
                )
                
                fig.update_layout(
                    font=dict(size=12),
                    title_font_size=14,
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de confianza
                confidence_counts = Counter(question_confidence)
                
                fig_conf = px.pie(
                    values=list(confidence_counts.values()),
                    names=list(confidence_counts.keys()),
                    title="Distribución de Confianza",
                    color_discrete_map={
                        'Alta': '#27AE60',
                        'Media': '#F39C12', 
                        'Baja': '#E74C3C'
                    }
                )
                
                fig_conf.update_layout(
                    font=dict(size=12),
                    title_font_size=14,
                    height=400
                )
                
                st.plotly_chart(fig_conf, use_container_width=True)
            
            # Tabla detallada
            details_df = pd.DataFrame(question_details)
            st.dataframe(
                details_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Sección expandible para razonamientos completos
            with st.expander(f"💭 Ver Razonamientos Completos - {question}", expanded=False):
                for i, response in enumerate([r for r in responses_data if question in r]):
                    if question in response:
                        resp_data = response[question]
                        if confidence_filter == "Todas" or resp_data['confianza'] == confidence_filter:
                            st.markdown(f"""
                            **👤 Encuestado {response['ID']} | Respuesta: {resp_data['respuesta_elegida']} | Confianza: {resp_data['confianza']}**
                            
                            📝 *{resp_data['opcion_completa']}*
                            
                            💭 **Razonamiento:** {resp_data['razonamiento']}
                            
                            ---
                            """)
        else:
            st.info(f"No hay datos disponibles para {question} con los filtros seleccionados.")
        
        st.markdown("---")

def main():
    """Función principal del dashboard"""
    # Título principal
    st.markdown('<div class="main-header">🏍️ BS Motos - Survey Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar para cargar archivo
    st.sidebar.markdown("### 📁 Cargar Datos")
    
    # Opción para seleccionar archivo
    file_option = st.sidebar.radio(
        "Seleccionar fuente de datos:",
        ["Usar archivo por defecto (output_final.csv)", "Subir archivo personalizado"]
    )
    
    df = None
    
    if file_option == "Usar archivo por defecto (output_final.csv)":
        if Path("output_final.csv").exists():
            df = load_data("output_final.csv")
            st.sidebar.success("✅ Archivo cargado correctamente")
        else:
            st.sidebar.error("❌ Archivo output_final.csv no encontrado")
            st.error("No se encontró el archivo output_final.csv. Ejecuta primero el pipeline.")
            return
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Subir archivo CSV",
            type=['csv'],
            help="Sube el archivo de salida del pipeline BS Motos"
        )
        
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            st.sidebar.success("✅ Archivo cargado correctamente")
    
    if df is not None:
        # Verificar estructura del archivo
        required_cols = ['json'] + [f'respuesta_pregunta_{i}' for i in range(1, 11)]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ El archivo no tiene la estructura esperada. Faltan columnas: {missing_cols}")
            return
        
        # Extraer datos
        demo_df = extract_demographics(df)
        responses_data, question_names = extract_responses(df)
        
        # Mostrar información del dataset
        st.sidebar.markdown("### 📊 Información del Dataset")
        st.sidebar.metric("Total Registros", len(df))
        st.sidebar.metric("Total Preguntas", len(question_names))
        st.sidebar.metric("Total Respuestas", len(df) * len(question_names))
        
        # Pestañas principales
        tab1, tab2 = st.tabs(["📊 Demografía", "🏍️ Respuestas de Encuesta"])
        
        with tab1:
            create_demographics_dashboard(demo_df)
        
        with tab2:
            create_responses_dashboard(responses_data, question_names)
        
        # Footer
        st.markdown("---")
        st.markdown(
            "**BS Motos Survey Analytics Dashboard** | "
            "Desarrollado por Jorge Polanco Roque | "
            f"Datos actualizados: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
        )
    
    else:
        st.info("👆 Por favor carga un archivo para comenzar el análisis.")

if __name__ == "__main__":
    main()