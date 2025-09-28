# Release Notes v0.1.15

## 🔧 Corrección Crítica: Configuración Dinámica de Variables

Esta versión `v0.1.15` incluye una corrección crítica que resuelve el problema donde las variables de configuración no se actualizaban correctamente después de llamar a `update_config()`.

### 🐛 Problema Resuelto

- **Resuelto: Variables de configuración no se actualizaban dinámicamente**
  - **Causa**: Las variables de configuración se importaban estáticamente con `from .config import *` al inicio del archivo `app.py`, antes de que `update_config()` pudiera modificar los valores.
  - **Solución**: Cambiado a importaciones dinámicas de las variables de configuración en cada función que las necesita.

### ✨ Mejoras Técnicas

- **Importaciones Dinámicas**: Todas las variables de configuración ahora se importan dinámicamente cuando se necesitan:
  - `INSTALL` - Para controlar el modo de instalación
  - `PORT` - Para la configuración del puerto
  - `DEBUG` - Para el modo de depuración
  - `LOG` - Para el logging
  - `DATABASE_URL` - Para la conexión a la base de datos
  - `ENTITIES_PATH` - Para la ruta de entidades YAML
  - `AUTH`, `JWT_*` - Para configuración de autenticación
  - `INITIAL_USERS` - Para usuarios iniciales
  - `CUSTOM_ROUTES` - Para rutas personalizadas

### 🎯 Comportamiento Corregido

**Antes (v0.1.14 y anteriores):**
```python
# ❌ INSTALL siempre era True por importación estática
from .config import INSTALL  # Se importa al inicio del módulo
update_config(INSTALL=False)  # No tiene efecto
# El backend siempre reiniciaba la base de datos
```

**Después (v0.1.15):**
```python
# ✅ INSTALL se lee dinámicamente después de update_config()
from .config import INSTALL  # Se importa cuando se necesita
update_config(INSTALL=False)  # Sí tiene efecto
# El backend respeta la configuración y NO reinicia la base de datos
```

### 📝 Cambios Técnicos Detallados

1. **Eliminada importación estática**: `from .config import *` → `from .config import update_config`
2. **Importaciones dinámicas agregadas** en:
   - `BackendGenerator.__init__()`: Para `DEBUG`, `JWT_*`
   - `BackendGenerator.initialize()`: Para `INSTALL`, `DATABASE_URL`, `ENTITIES_PATH`, `CUSTOM_ROUTES`
   - `BackendGenerator._create_initial_users()`: Para `AUTH`, `INITIAL_USERS`
   - `BackendGenerator.run()`: Para `PORT`, `DEBUG`
   - `run_backend()`: Para `PORT`

### ✅ Estado Actual

Con esta corrección, el backend ahora:
- ✅ Respeta correctamente `INSTALL=False` (no reinicia la base de datos)
- ✅ Respeta correctamente `PORT` configurado
- ✅ Respeta correctamente todas las configuraciones de `update_config()`
- ✅ Mantiene compatibilidad total con versiones anteriores
- ✅ Funciona correctamente en modo desarrollo y producción

### 🧪 Verificación

Para verificar que funciona correctamente:

```python
from yaml_to_backend import update_config, get_run_backend

# Configurar para NO reiniciar la base de datos
update_config(INSTALL=False, PORT=8001)

# Ejecutar el backend
run_backend = get_run_backend()
run_backend()  # No reiniciará la base de datos, puerto 8001
```

## 📦 Instalación y Actualización

Para instalar esta versión:
```bash
pip install yaml-to-backend==0.1.15
```

Para actualizar:
```bash
pip install --upgrade yaml-to-backend
```

## 🔄 Migración

Esta versión es completamente retrocompatible. No se requieren cambios en el código existente.
