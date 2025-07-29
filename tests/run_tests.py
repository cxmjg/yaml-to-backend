#!/usr/bin/env python3
"""
Ejecutor de pruebas para el backend generador
Este archivo permite ejecutar las pruebas de endpoints de manera organizada
"""

import subprocess
import sys
import time
import argparse
import signal
import os
from pathlib import Path

def check_backend_ready(base_url: str = "http://localhost:8000", max_retries: int = 30) -> bool:
    """Verifica que el backend esté listo para recibir requests"""
    import httpx
    
    print("⏳ Esperando que el backend esté listo...")
    
    for i in range(max_retries):
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{base_url}/docs")
                if response.status_code == 200:
                    print("✅ Backend está listo!")
                    return True
        except:
            pass
        
        print(f"   Intento {i+1}/{max_retries}...")
        time.sleep(2)
    
    print("❌ Backend no está respondiendo después de varios intentos")
    return False

def start_backend():
    """Inicia el backend en segundo plano"""
    print("🚀 Iniciando el backend...")
    
    # Verificar que main.py existe
    if not Path("main.py").exists():
        print("❌ Error: main.py no encontrado")
        return None
    
    try:
        # Ejecutar el backend con logs visibles
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"✅ Backend iniciado con PID: {process.pid}")
        
        # Esperar un poco y verificar si hay errores
        time.sleep(5)
        if process.poll() is not None:
            # El proceso terminó, obtener los logs
            stdout, stderr = process.communicate()
            print("❌ Backend terminó prematuramente")
            if stderr:
                print(f"Error: {stderr}")
            if stdout:
                print(f"Output: {stdout}")
            return None
        
        # Mostrar logs recientes si el proceso sigue ejecutándose
        try:
            # Intentar leer logs sin bloquear
            import select
            if select.select([process.stderr], [], [], 0.1)[0]:
                stderr_line = process.stderr.readline()
                if stderr_line:
                    print(f"Backend log: {stderr_line.strip()}")
        except:
            pass
        
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando el backend: {e}")
        return None

def stop_backend(process):
    """Detiene el proceso del backend"""
    if process:
        print(f"\n🛑 Deteniendo el backend (PID: {process.pid})...")
        try:
            process.terminate()
            process.wait(timeout=5)
            print("✅ Backend detenido correctamente")
        except subprocess.TimeoutExpired:
            print("⚠️  Forzando cierre del backend...")
            process.kill()
            process.wait()
        except Exception as e:
            print(f"⚠️  Error deteniendo el backend: {e}")

def run_pytest_command(args, start_backend_auto=False):
    """Ejecuta pytest con los argumentos especificados"""
    cmd = [sys.executable, "-m", "pytest"] + args
    
    print(f"🧪 Ejecutando: {' '.join(cmd)}")
    print("=" * 60)
    
    backend_process = None
    
    try:
        # Si se solicita iniciar el backend automáticamente
        if start_backend_auto:
            backend_process = start_backend()
            if not backend_process:
                print("❌ No se pudo iniciar el backend")
                return False
            
            # Esperar a que el backend esté listo
            if not check_backend_ready():
                print("❌ Backend no está respondiendo")
                return False
        
        # Ejecutar pytest
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando pytest: {e}")
        return False
    finally:
        # Limpiar el proceso del backend si se inició automáticamente
        if start_backend_auto and backend_process:
            stop_backend(backend_process)

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🎯 Ejecutando todas las pruebas del backend")
    return run_pytest_command(["tests/", "-v"], start_backend_auto=True)

def run_integration_tests():
    """Ejecuta solo las pruebas de integración"""
    print("🔗 Ejecutando pruebas de integración")
    return run_pytest_command(["tests/", "-m", "integration", "-v"], start_backend_auto=True)

def run_unit_tests():
    """Ejecuta solo las pruebas unitarias"""
    print("🔧 Ejecutando pruebas unitarias")
    return run_pytest_command(["tests/", "-m", "not integration", "-v"])

def run_auth_tests():
    """Ejecuta solo las pruebas de autenticación"""
    print("🔐 Ejecutando pruebas de autenticación")
    return run_pytest_command(["tests/test_auth.py", "-v"])

def run_parser_tests():
    """Ejecuta solo las pruebas del parser"""
    print("📝 Ejecutando pruebas del parser de entidades")
    return run_pytest_command(["tests/test_entity_parser.py", "-v"])

def run_endpoints_tests():
    """Ejecuta solo las pruebas de endpoints"""
    print("📡 Ejecutando pruebas de endpoints")
    return run_pytest_command(["tests/test_endpoints.py", "-v"], start_backend_auto=True)

def run_with_coverage():
    """Ejecuta las pruebas con cobertura"""
    print("📊 Ejecutando pruebas con cobertura")
    return run_pytest_command([
        "tests/", 
        "--cov=backend", 
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v"
    ], start_backend_auto=True)

def run_specific_test(test_path):
    """Ejecuta una prueba específica"""
    print(f"🎯 Ejecutando prueba específica: {test_path}")
    return run_pytest_command([test_path, "-v"])

def show_help():
    """Muestra la ayuda del ejecutor"""
    print("""
🧪 Ejecutor de Pruebas del Backend Generador

Uso:
  python tests/run_tests.py [opción]

Opciones:
  all              Ejecutar todas las pruebas (inicia backend automáticamente)
  integration      Solo pruebas de integración (inicia backend automáticamente)
  unit             Solo pruebas unitarias
  auth             Solo pruebas de autenticación
  parser           Solo pruebas del parser
  endpoints        Solo pruebas de endpoints (inicia backend automáticamente)
  coverage         Pruebas con cobertura (inicia backend automáticamente)
  help             Mostrar esta ayuda

Ejemplos:
  # Ejecutar todas las pruebas (backend automático)
  python tests/run_tests.py all
  
  # Solo pruebas de integración (backend automático)
  python tests/run_tests.py integration
  
  # Solo pruebas unitarias
  python tests/run_tests.py unit
  
  # Pruebas con cobertura (backend automático)
  python tests/run_tests.py coverage
  
  # Solo pruebas de autenticación
  python tests/run_tests.py auth

Características:
  ✅ Inicio automático del backend para pruebas de integración
  ✅ Espera automática hasta que el backend esté listo
  ✅ Limpieza automática del backend al finalizar
  ✅ Manejo robusto de errores y timeouts
""")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    option = sys.argv[1].lower()
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: Debes ejecutar este script desde la raíz del proyecto")
        print("   cd /ruta/al/proyecto/IPAS")
        return 1
    
    success = False
    
    if option == "all":
        success = run_all_tests()
    elif option == "integration":
        success = run_integration_tests()
    elif option == "unit":
        success = run_unit_tests()
    elif option == "auth":
        success = run_auth_tests()
    elif option == "parser":
        success = run_parser_tests()
    elif option == "endpoints":
        success = run_endpoints_tests()
    elif option == "coverage":
        success = run_with_coverage()
    elif option == "help":
        show_help()
        return 0
    else:
        print(f"❌ Opción desconocida: {option}")
        show_help()
        return 1
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 