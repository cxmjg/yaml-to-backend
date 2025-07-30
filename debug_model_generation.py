#!/usr/bin/env python3
"""
Script de debug para verificar la generación de modelos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yaml_to_backend.core.entity_parser import EntityParser
from yaml_to_backend.core.model_generator import ModelGenerator
from yaml_to_backend.config import update_config

def debug_model_generation():
    """Debug de la generación de modelos"""
    print("🔍 Debug de generación de modelos")
    print("=" * 50)
    
    # Configurar AUTH
    update_config(
        AUTH={
            'tabla': 'usuarios',
            'columna_usuario': 'nombre',
            'columna_password': 'password',
            'superusuario': 'admin',
            'password_default': 'admin123',
            'columna_borrado': 'habilitado',
            'borrado_logico': 'boolean'
        }
    )
    
    # Cargar entidades
    print("📁 Cargando entidades...")
    entity_parser = EntityParser('./testsPreRelease/entidades/')
    entities = entity_parser.load_entities()
    
    print(f"✅ Entidades cargadas: {list(entities.keys())}")
    
    # Verificar entidad Usuarios
    if 'Usuarios' in entities:
        print("\n📋 Entidad Usuarios:")
        usuarios_entity = entities['Usuarios']
        print(f"   Tabla: {usuarios_entity['tabla']}")
        print(f"   Campos: {list(usuarios_entity['campos'].keys())}")
        
        # Verificar campos específicos
        campos = usuarios_entity['campos']
        if 'nombre' in campos:
            print(f"   ✅ Campo 'nombre' encontrado: {campos['nombre']}")
        else:
            print(f"   ❌ Campo 'nombre' NO encontrado")
            
        if 'habilitado' in campos:
            print(f"   ✅ Campo 'habilitado' encontrado: {campos['habilitado']}")
        else:
            print(f"   ❌ Campo 'habilitado' NO encontrado")
    
    # Generar modelos
    print("\n🔧 Generando modelos...")
    model_generator = ModelGenerator()
    
    # Generar código para Usuarios específicamente
    if 'Usuarios' in entities:
        print("\n📝 Código generado para Usuarios:")
        model_code = model_generator.generate_model_code('Usuarios', entities['Usuarios'])
        print(model_code)
    
    # Generar todos los modelos
    print("\n🚀 Generando todos los modelos...")
    try:
        models_result = model_generator.generate_all_models(entities)
        print("✅ Modelos generados exitosamente")
        
        # Verificar modelo Usuario generado
        if 'Usuario' in model_generator.generated_models:
            usuario_model = model_generator.generated_models['Usuario']
            print(f"\n📋 Modelo Usuario generado:")
            print(f"   Tabla: {usuario_model.__tablename__}")
            print(f"   Campos: {list(usuario_model.__fields__.keys())}")
            
            # Verificar campos específicos
            fields = usuario_model.__fields__
            if 'nombre' in fields:
                print(f"   ✅ Campo 'nombre' en modelo: {fields['nombre']}")
            else:
                print(f"   ❌ Campo 'nombre' NO en modelo")
                
            if 'habilitado' in fields:
                print(f"   ✅ Campo 'habilitado' en modelo: {fields['habilitado']}")
            else:
                print(f"   ❌ Campo 'habilitado' NO en modelo")
                
            if 'username' in fields:
                print(f"   ⚠️  Campo 'username' en modelo (no debería estar): {fields['username']}")
                
            if 'deleted_at' in fields:
                print(f"   ⚠️  Campo 'deleted_at' en modelo (no debería estar): {fields['deleted_at']}")
        
    except Exception as e:
        print(f"❌ Error generando modelos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_model_generation() 