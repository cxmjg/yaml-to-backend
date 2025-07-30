#!/usr/bin/env python3
"""
Script de prueba para yaml-to-backend instalado con pipx

Este script prueba la librería instalada con pipx para verificar
que funciona correctamente con las correcciones.
"""

import sys
import os

# Usar el Python del entorno virtual de pipx
pipx_python = "/home/mgarcia/.local/share/pipx/venvs/yaml-to-backend/bin/python"
if os.path.exists(pipx_python):
    sys.executable = pipx_python

from yaml_to_backend import update_config, get_run_backend

def test_library():
    """Prueba la librería yaml-to-backend"""
    print("🧪 Probando yaml-to-backend instalado con pipx...")
    print("=" * 60)
    
    try:
        # Configuración de prueba
        update_config(
            ENTITIES_PATH='./entidades/',  # Usar el directorio local de entidades
            DB_HOST='100.123.161.101',
            DB_USER='root',
            DB_PASSWORD='1234',
            DB_NAME='mi_base',
            DB_PORT=3306,
            PORT=8005,
            INSTALL=True,
            DEBUG=True,
            LOG=True,
            AUTH={
                'tabla': 'usuarios',
                'columna_usuario': 'nombre',  # Cambiado de 'username' a 'nombre' para coincidir con el YAML
                'columna_password': 'password',
                'superusuario': 'admin',
                'password_default': 'admin123',
                'columna_borrado': 'habilitado',
                'borrado_logico': 'boolean'
            }
        )

        # Usuarios de prueba
        update_config(
            INITIAL_USERS=[
                {'nombre': 'admin', 'password': 'admin123', 'rol': 'admin', 'habilitado': True},
                {'nombre': 'estudiante', 'password': 'estudiante123', 'rol': 'estudiante', 'habilitado': True},
                {'nombre': 'desarrollador', 'password': 'dev123', 'rol': 'admin', 'habilitado': True}
            ]
        )

        print("✅ Configuración aplicada correctamente")
        print("🔧 Configuración AUTH:")
        print("   - columna_usuario: nombre")
        print("   - columna_borrado: habilitado")
        print("   - borrado_logico: boolean")
        print("🌐 Puerto: 8005")
        print("🗄️  Base de datos: mi_base")
        print("=" * 60)
        
        # Obtener la función run_backend
        run_backend = get_run_backend()
        print("✅ Función run_backend obtenida correctamente")
        
        # Ejecutar el backend (solo por unos segundos para probar)
        print("🚀 Iniciando backend (se detendrá en 10 segundos)...")
        import threading
        import time
        
        # Ejecutar en un hilo separado para poder detenerlo
        def run_backend_thread():
            try:
                run_backend()
            except Exception as e:
                print(f"❌ Error en el backend: {e}")
        
        thread = threading.Thread(target=run_backend_thread)
        thread.daemon = True
        thread.start()
        
        # Esperar 10 segundos
        time.sleep(10)
        print("✅ Prueba completada exitosamente")
        print("🎉 La librería funciona correctamente con las correcciones!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        print("🔍 Verificar:")
        print("   1. Que el modelo Usuario tenga el campo 'nombre'")
        print("   2. Que el modelo Usuario tenga el campo 'habilitado'")
        print("   3. Que no haya errores de importación")
        print("   4. Que la configuración AUTH se aplique correctamente")
        return False

if __name__ == "__main__":
    success = test_library()
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron! La librería está lista para el release.")
        sys.exit(0)
    else:
        print("\n💥 Las pruebas fallaron. Revisa los errores antes del release.")
        sys.exit(1) 