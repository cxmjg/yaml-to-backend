#!/usr/bin/env python3
"""
Script de prueba pre-release para yaml-to-backend

Este script permite probar la librería localmente antes de generar un release
para verificar que todo funcione correctamente.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def test_pre_release():
    """Prueba la librería antes del release"""
    print("🧪 Iniciando pruebas pre-release de yaml-to-backend...")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("yaml_to_backend"):
        print("❌ Error: No se encontró el directorio yaml_to_backend")
        print("   Ejecuta este script desde el directorio raíz del proyecto")
        return False
    
    # Verificar que estamos en un entorno virtual
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Advertencia: No parece estar en un entorno virtual")
        print("   Se recomienda usar un entorno virtual para las pruebas")
    
    # Crear directorio temporal para pruebas
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Directorio temporal de prueba: {temp_dir}")
        
        # Copiar archivos de prueba
        test_dir = Path(temp_dir) / "test_project"
        test_dir.mkdir()
        
        # Copiar entidades
        entities_dir = test_dir / "entidades"
        entities_dir.mkdir()
        
        if os.path.exists("testsPreRelease/entidades"):
            for yaml_file in Path("testsPreRelease/entidades").glob("*.yaml"):
                shutil.copy2(yaml_file, entities_dir)
            print(f"✅ Copiadas entidades de prueba: {list(entities_dir.glob('*.yaml'))}")
        else:
            print("⚠️  No se encontró testsPreRelease/entidades, usando entidades por defecto")
            # Copiar entidades por defecto
            if os.path.exists("entidades"):
                for yaml_file in Path("entidades").glob("*.yaml"):
                    shutil.copy2(yaml_file, entities_dir)
                print(f"✅ Copiadas entidades por defecto: {list(entities_dir.glob('*.yaml'))}")
        
        # Copiar main.py de prueba
        if os.path.exists("testsPreRelease/main.py"):
            shutil.copy2("testsPreRelease/main.py", test_dir)
            main_file = test_dir / "main.py"
        else:
            print("❌ No se encontró testsPreRelease/main.py")
            return False
        
        # Usar el Python del entorno virtual actual
        python_exe = sys.executable
        print(f"🐍 Usando Python del entorno virtual actual: {python_exe}")
        
        # Verificar que la librería está instalada
        try:
            import yaml_to_backend
            print(f"✅ Librería yaml-to-backend instalada (versión: {yaml_to_backend.__version__})")
        except ImportError:
            print("❌ La librería yaml-to-backend no está instalada")
            print("   Ejecuta: pip install -e .")
            return False
        
        # Ejecutar prueba
        print("🚀 Ejecutando prueba...")
        try:
            # Configurar el path para que encuentre las entidades
            env = os.environ.copy()
            env['ENTITIES_PATH'] = str(entities_dir)
            
            result = subprocess.run([python_exe, "main.py"], 
                                  cwd=test_dir, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30,
                                  env=env)
            
            if result.returncode == 0:
                print("✅ Prueba exitosa!")
                print("📋 Salida:")
                print(result.stdout)
                return True
            else:
                print("❌ Prueba falló!")
                print("📋 Error:")
                print(result.stderr)
                print("📋 Salida:")
                print(result.stdout)
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Prueba excedió el tiempo límite (30 segundos)")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando prueba: {e}")
            return False

def main():
    """Función principal"""
    print("🔧 Herramienta de prueba pre-release para yaml-to-backend")
    print("=" * 60)
    
    success = test_pre_release()
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron! La librería está lista para el release.")
        return 0
    else:
        print("\n💥 Las pruebas fallaron. Revisa los errores antes del release.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 