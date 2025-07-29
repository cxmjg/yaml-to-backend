#!/usr/bin/env python3
"""
Script de prueba para YAML-to-Backend
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from yaml_to_backend import update_config
    print("✅ Configuración importada correctamente")
    
    # Probar la configuración
    update_config(PORT=8001, DB_HOST='localhost')
    print("✅ Configuración actualizada correctamente")
    
    # Probar importar run_backend
    from yaml_to_backend import get_run_backend
    run_backend = get_run_backend()
    print("✅ run_backend importado correctamente")
    
    print("\n🎉 ¡YAML-to-Backend funciona correctamente!")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1) 