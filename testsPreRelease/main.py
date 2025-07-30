#!/usr/bin/env python3
"""
Test Pre-Release - YAML-to-Backend

Este archivo permite probar la librería antes de generar un release
para verificar que todo funcione correctamente.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from yaml_to_backend import update_config, get_run_backend

# =============================================================================
# CONFIGURACIÓN DE PRUEBA
# =============================================================================

# Configuración de base de datos de prueba
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

# =============================================================================
# EJECUCIÓN DE PRUEBA
# =============================================================================

if __name__ == "__main__":
    print("🧪 Iniciando prueba pre-release de yaml-to-backend...")
    print("📁 Directorio de entidades: testsPreRelease/entidades/")
    print("🔧 Configuración AUTH:")
    print("   - columna_usuario: nombre")
    print("   - columna_borrado: habilitado")
    print("   - borrado_logico: boolean")
    print("🌐 Puerto: 8005")
    print("🗄️  Base de datos: mi_base")
    print("=" * 60)
    
    try:
        # Ejecutar el backend
        run_backend = get_run_backend()
        run_backend()
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        print("🔍 Verificar:")
        print("   1. Que el modelo Usuario tenga el campo 'nombre'")
        print("   2. Que el modelo Usuario tenga el campo 'habilitado'")
        print("   3. Que no haya errores de importación")
        print("   4. Que la configuración AUTH se aplique correctamente")
        raise 