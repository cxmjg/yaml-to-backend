#!/usr/bin/env python3
"""
Script para probar que todos los archivos YAML son válidos y compatibles con yaml-to-backend
"""

import yaml
import os
from pathlib import Path

def test_yaml_files():
    """Prueba todos los archivos YAML en el directorio entidades"""
    
    entidades_path = Path("entidades")
    if not entidades_path.exists():
        print("❌ Directorio 'entidades' no encontrado")
        return False
    
    yaml_files = list(entidades_path.glob("*.yaml"))
    if not yaml_files:
        print("❌ No se encontraron archivos YAML en el directorio 'entidades'")
        return False
    
    print(f"📁 Encontrados {len(yaml_files)} archivos YAML:")
    
    all_valid = True
    
    for yaml_file in yaml_files:
        print(f"\n🔍 Probando: {yaml_file.name}")
        
        try:
            # Cargar el archivo YAML
            with open(yaml_file, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if not data:
                print(f"  ❌ Archivo vacío o inválido")
                all_valid = False
                continue
            
            # Verificar campos requeridos
            required_fields = ['entidad', 'tabla', 'campos']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"  ❌ Campos faltantes: {missing_fields}")
                all_valid = False
                continue
            
            # Verificar que hay campos definidos
            if not data['campos']:
                print(f"  ❌ No hay campos definidos")
                all_valid = False
                continue
            
            # Verificar tipos de datos soportados
            supported_types = ['integer', 'int', 'string', 'text', 'boolean', 'bool', 
                             'datetime', 'date', 'float', 'decimal', 'json']
            
            invalid_types = []
            for field_name, field_config in data['campos'].items():
                field_type = field_config.get('tipo', 'string').lower()
                if field_type not in supported_types:
                    invalid_types.append(f"{field_name}: {field_type}")
            
            if invalid_types:
                print(f"  ❌ Tipos no soportados: {invalid_types}")
                all_valid = False
                continue
            
            # Verificar foreign keys
            for field_name, field_config in data['campos'].items():
                if 'fk' in field_config:
                    fk_value = field_config['fk']
                    if '.' not in fk_value:
                        print(f"  ❌ FK inválida en {field_name}: {fk_value}")
                        all_valid = False
            
            print(f"  ✅ Archivo válido - Entidad: {data['entidad']}")
            
        except yaml.YAMLError as e:
            print(f"  ❌ Error de sintaxis YAML: {e}")
            all_valid = False
        except Exception as e:
            print(f"  ❌ Error inesperado: {e}")
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    print("🧪 Probando archivos YAML para yaml-to-backend")
    print("=" * 50)
    
    if test_yaml_files():
        print("\n🎉 ¡Todos los archivos YAML son válidos!")
        print("✅ Los archivos están listos para usar con yaml-to-backend")
    else:
        print("\n❌ Algunos archivos YAML tienen problemas")
        print("🔧 Revisa los errores anteriores y corrígelos") 