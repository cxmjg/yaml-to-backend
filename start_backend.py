#!/usr/bin/env python3
"""
Script para ejecutar el backend generado desde YAML
"""

import sys
import os

# Configurar el path del entorno virtual
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'lib', 'python3.13', 'site-packages')
sys.path.insert(0, venv_path)

from yaml_to_backend import update_config, get_run_backend

def main():
    print("🚀 Iniciando backend generado desde YAML...")
    print("📁 Usando archivos YAML desde: entidades/")
    
    # Configurar el backend
    update_config(
        DB_HOST='192.168.1.100',
        DB_USER='root',
        DB_PASSWORD='1234',
        DB_NAME='mi_db',
        DB_PORT=3306,
        PORT=8001
    )
    
    print("✅ Configuración aplicada")
    
    # Obtener la función run_backend
    run_backend = get_run_backend()
    print("✅ Función run_backend obtenida")
    
    # Ejecutar el backend
    print("🌐 Iniciando servidor en http://localhost:8001")
    print("📚 Documentación disponible en http://localhost:8001/docs")
    print("🔐 Endpoints disponibles:")
    print("   - /api/usuarios")
    print("   - /api/roles")
    print("   - /api/sistemas-operativos")
    print("   - /api/aplicaciones")
    print("   - /api/imagenes")
    print("   - /api/contenedores")
    print("   - /api/perfiles")
    print("   - /api/aplicacion-imagen")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor")
    
    run_backend()

if __name__ == "__main__":
    main() 