#!/usr/bin/env python3
"""
Script para convertir datos CSV a formato JSON.

Este script lee un archivo CSV con datos de encuestas sobre motos,
convierte cada fila en un objeto JSON y guarda el resultado en un CSV
donde cada fila contiene el JSON de una persona.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import chardet

import pandas as pd


class CSVToJSONConverter:
    """Conversor de CSV a JSON siguiendo buenas prácticas de desarrollo."""
    
    def __init__(self, input_file: str, output_file: str = "output_json.csv"):
        """
        Inicializa el conversor.
        
        Args:
            input_file: Ruta al archivo CSV de entrada
            output_file: Ruta al archivo CSV de salida
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self._validate_input_file()
    
    def _validate_input_file(self) -> None:
        """Valida que el archivo de entrada exista."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.input_file}")
        
        if not self.input_file.suffix.lower() == '.csv':
            raise ValueError("El archivo debe tener extensión .csv")
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia los nombres de las columnas removiendo caracteres especiales.
        
        Args:
            df: DataFrame con los datos
            
        Returns:
            DataFrame con nombres de columnas limpios
        """
        df_cleaned = df.copy()
        
        # Crear un mapeo de nombres originales a nombres limpios
        column_mapping = {}
        for col in df.columns:
            # Remover caracteres especiales y normalizar
            clean_name = (col.strip()
                         .replace('¿', '')
                         .replace('?', '')
                         .replace('ñ', 'n')
                         .replace('á', 'a')
                         .replace('é', 'e')
                         .replace('í', 'i')
                         .replace('ó', 'o')
                         .replace('ú', 'u')
                         .replace('Á', 'A')
                         .replace('É', 'E')
                         .replace('Í', 'I')
                         .replace('Ó', 'O')
                         .replace('Ú', 'U')
                         .replace('(', '_')
                         .replace(')', '_')
                         .replace('[', '_')
                         .replace(']', '_')
                         .replace('{', '_')
                         .replace('}', '_')
                         .replace(',', '_')
                         .replace(';', '_')
                         .replace(':', '_')
                         .replace(' ', '_')
                         .replace('__', '_')
                         .strip('_'))
            
            column_mapping[col] = clean_name
        
        # Renombrar columnas
        df_cleaned.rename(columns=column_mapping, inplace=True)
        
        return df_cleaned
    
    def _row_to_json(self, row: pd.Series) -> str:
        """
        Convierte una fila del DataFrame a formato JSON.
        
        Args:
            row: Serie de pandas representando una fila
            
        Returns:
            String JSON de la fila
        """
        # Convertir la fila a diccionario
        person_data = {}
        
        for column, value in row.items():
            # Manejar valores NaN
            if pd.isna(value):
                person_data[column] = None
            else:
                # Convertir a string y limpiar
                person_data[column] = str(value).strip()
        
        # Convertir a JSON compacto (sin espacios extra)
        return json.dumps(person_data, ensure_ascii=False, separators=(',', ':'))
    
    def _detect_encoding(self) -> str:
        """Detecta automáticamente la codificación del archivo."""
        with open(self.input_file, 'rb') as f:
            raw_data = f.read(10000)  # Lee los primeros 10KB
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            print(f"Codificación detectada: {encoding} (confianza: {confidence:.2f})")
            return encoding if encoding else 'utf-8'
    
    def convert(self) -> None:
        """
        Ejecuta la conversión completa del archivo.
        """
        try:
            print(f"Leyendo archivo: {self.input_file}")
            
            # Detectar y usar la codificación correcta
            encoding = self._detect_encoding()
            
            # Leer CSV
            df = pd.read_csv(self.input_file, encoding=encoding)
            print(f"Archivo leído correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            
            # ============================================================================
            # CONFIGURACIÓN PARA PRUEBAS - CAMBIAR AQUÍ PARA PROCESAR TODA LA TABLA
            # ============================================================================
            # Para procesar TODA la tabla, cambiar TEST_MODE = False
            # Para procesar solo las primeras 20 filas, mantener TEST_MODE = True
            TEST_MODE = True
            
            if TEST_MODE:
                df = df.head(20)  # Solo primeras 20 observaciones para pruebas
                print(f"⚠️  MODO PRUEBA ACTIVADO: Procesando solo las primeras 20 observaciones")
                print(f"   Para procesar toda la tabla ({len(pd.read_csv(self.input_file, encoding=encoding))} registros), cambiar TEST_MODE = False en línea 144")
            
            print(f"Procesando {len(df)} registros...")
            # ============================================================================
            
            # Limpiar nombres de columnas
            df_cleaned = self._clean_column_names(df)
            
            # Convertir cada fila a JSON
            json_data = []
            for idx, row in df_cleaned.iterrows():
                json_string = self._row_to_json(row)
                json_data.append(json_string)
            
            # Crear DataFrame de salida con una sola columna 'json'
            output_df = pd.DataFrame({'json': json_data})
            
            # Guardar el archivo de salida
            output_df.to_csv(self.output_file, index=False, encoding='utf-8')
            
            print(f"Conversión completada exitosamente.")
            print(f"Archivo de salida: {self.output_file}")
            print(f"Total de registros procesados: {len(json_data)}")
            
        except Exception as e:
            print(f"Error durante la conversión: {str(e)}", file=sys.stderr)
            raise
    
    def preview_sample(self, num_samples: int = 3) -> None:
        """
        Muestra una vista previa de los primeros registros convertidos.
        
        Args:
            num_samples: Número de muestras a mostrar
        """
        try:
            encoding = self._detect_encoding()
            df = pd.read_csv(self.input_file, encoding=encoding)
            df_cleaned = self._clean_column_names(df)
            
            print(f"\nVista previa de {min(num_samples, len(df))} registros:")
            print("-" * 80)
            
            for idx in range(min(num_samples, len(df))):
                row = df_cleaned.iloc[idx]
                json_string = self._row_to_json(row)
                
                # Formatear JSON para mejor legibilidad en preview
                parsed_json = json.loads(json_string)
                formatted_json = json.dumps(parsed_json, ensure_ascii=False, indent=2)
                
                print(f"\nRegistro {idx + 1}:")
                print(formatted_json)
                print("-" * 80)
                
        except Exception as e:
            print(f"Error al generar vista previa: {str(e)}", file=sys.stderr)


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("Uso: python building_json.py <archivo_csv> [archivo_salida.csv]")
        print("Ejemplo: python building_json.py inputs/tabla_1.csv output_motos.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_json.csv"
    
    try:
        # Crear instancia del conversor
        converter = CSVToJSONConverter(input_file, output_file)
        
        # Mostrar vista previa
        print("=== VISTA PREVIA ===")
        converter.preview_sample(2)
        
        # Ejecutar conversión
        print("\n=== INICIANDO CONVERSIÓN ===")
        converter.convert()
        
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()