#!/usr/bin/env python3
"""
Backend IPAS - Punto de entrada principal

Este archivo permite personalizar la configuración del backend
y ejecutar la aplicación de forma simple.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from yaml_to_backend import update_config, run_backend

# =============================================================================
# CONFIGURACIÓN PERSONALIZADA
# =============================================================================
# Aquí puedes modificar cualquier valor de configuración por defecto
# Descomenta y modifica las líneas que necesites:

# Ejemplo: Cambiar el puerto del servidor
# update_config(PORT=8002)

# Ejemplo: Cambiar configuración de base de datos
update_config(
    DB_HOST='192.168.1.100',
    DB_USER='root',
    DB_PASSWORD='1234',
    DB_NAME='mi_db',
    DB_PORT=3306,
    PORT=8001
)

# Ejemplo: Agregar un usuario adicional
# update_config(
#     INITIAL_USERS=[
#         {'username': 'admin', 'password': 'admin123', 'rol': 'admin'},
#         {'username': 'usuario1', 'password': 'usuario123', 'rol': 'usuario'},
#         {'username': 'desarrollador', 'password': 'dev123', 'rol': 'admin'}
#     ]
# )

# =============================================================================
# EJECUCIÓN DEL BACKEND
# =============================================================================

if __name__ == "__main__":

    # Ejecutar el backend
    run_backend() 