# Release Notes v0.1.14

## 🔧 Mejoras en la Configuración del Puerto

Esta versión `v0.1.14` incluye una mejora importante en la función `run_backend()` que resuelve el problema de configuración del puerto del servidor.

### 🐛 Corrección de Error

- **Resuelto: Backend ignoraba la configuración del puerto**
  - **Causa**: La función `run_backend()` en `yaml_to_backend/app.py` no estaba respetando la configuración del puerto establecida con `update_config()`.
  - **Solución**: Modificada la función `run_backend()` para usar `uvicorn.run()` con el puerto configurado desde `config.PORT`.

### ✨ Mejoras

- **Configuración de Puerto Mejorada**: Ahora el backend respeta correctamente la configuración del puerto establecida en `update_config()`.
- **Patrón de Configuración Simplificado**: El archivo `main.py` ahora usa el patrón más limpio con `update_config()` y `get_run_backend()`.
- **Compatibilidad Mantenida**: Todos los cambios son retrocompatibles con la funcionalidad existente.

### 📝 Cambios Técnicos

```python
# Antes (no respetaba PORT)
def run_backend():
    backend = asyncio.run(main())
    backend.run()  # Usaba puerto por defecto

# Después (respeta PORT)
def run_backend():
    backend = asyncio.run(main())
    import uvicorn
    from .config import PORT
    uvicorn.run(backend.app, host="0.0.0.0", port=PORT)
```

### 🎯 Uso Simplificado

Ahora puedes configurar el puerto de forma simple:

```python
from yaml_to_backend import update_config, get_run_backend

# Configurar el puerto
update_config(PORT=8002)

# Ejecutar el backend
run_backend = get_run_backend()
run_backend()  # Se ejecutará en el puerto 8002
```

## ✅ Estado Actual

Con esta corrección, el backend ahora:
- ✅ Respeta la configuración del puerto establecida
- ✅ Mantiene toda la funcionalidad existente
- ✅ Usa el patrón de configuración más limpio
- ✅ Es completamente retrocompatible

## 📦 Instalación y Actualización

Para instalar esta versión:
```bash
pip install yaml-to-backend==0.1.14
```

Para actualizar:
```bash
pip install --upgrade yaml-to-backend
```
