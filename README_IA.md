# README_IA - Contexto Completo del Proyecto YAML-to-Backend

## 🎯 Propósito de este Documento

Este README_IA está diseñado para proporcionar contexto completo a una IA sobre el proyecto **YAML-to-Backend**. Contiene toda la información relevante, preguntas del usuario, respuestas, decisiones tomadas y contexto técnico para que una IA pueda entender y trabajar efectivamente con este proyecto.

## 📋 Información del Proyecto

### **Nombre**: YAML-to-Backend
### **Versión Actual**: 0.1.12
### **Repositorio**: https://github.com/cxmjg/yaml-to-backend
### **Autor**: IPAS Team
### **Licencia**: MIT

## 🎯 Objetivo del Proyecto

**YAML-to-Backend** es una librería Python que genera automáticamente backends completos con FastAPI, SQLAlchemy y SQLModel a partir de definiciones YAML. Es ideal para startups y desarrolladores que necesitan prototipar rápidamente APIs RESTful sin escribir código repetitivo.

### **Metodología de Trabajo**
- Los usuarios definen modelos con archivos YAML
- La librería genera automáticamente modelos ORM, endpoints CRUD y documentación
- Sistema de permisos basado en roles con soporte "yo" (self-access)
- Autenticación JWT integrada
- Validación automática de datos

## 🔧 Características Principales

- **Generación automática de modelos**: Crea modelos SQLModel y Pydantic automáticamente
- **CRUD automático**: Genera endpoints CRUD completos para cada entidad
- **Autenticación integrada**: Sistema de autenticación JWT incluido
- **Validación automática**: Validación de datos basada en las definiciones YAML
- **Documentación automática**: Swagger/OpenAPI generado automáticamente
- **Soporte para relaciones**: Claves foráneas y relaciones entre entidades
- **Sistema de permisos**: Control de acceso basado en roles con soporte "yo"
- **Borrado lógico**: Soporte para soft delete configurable

## 🏗️ Arquitectura del Sistema

### **Componentes Principales**

1. **EntityParser** (`yaml_to_backend.core.entity_parser`)
   - Carga y parsea archivos YAML de entidades
   - Valida estructura de entidades

2. **ModelGenerator** (`yaml_to_backend.core.model_generator`)
   - Genera modelos SQLModel y Pydantic
   - Crea diccionario centralizado PYDANTIC_MODELS
   - Escribe archivos de modelos generados

3. **AuthManager** (`yaml_to_backend.security.auth`)
   - Maneja autenticación JWT
   - Verifica permisos de usuarios
   - Gestiona tokens de acceso

4. **DatabaseManager** (`yaml_to_backend.db.connection`)
   - Gestiona conexiones MySQL asíncronas
   - Maneja sesiones de base de datos
   - Inicializa y resetea base de datos

5. **BackendGenerator** (`yaml_to_backend.app`)
   - Orquesta la generación completa del backend
   - Crea aplicación FastAPI
   - Genera endpoints CRUD

6. **CRUDGenerator** (`yaml_to_backend.api.crud_generator`)
   - Genera endpoints CRUD automáticamente
   - Aplica sistema de permisos
   - Maneja validaciones

## 📁 Estructura del Proyecto

```
yaml-to-backend/
├── yaml_to_backend/          # Código fuente de la librería
│   ├── __init__.py
│   ├── app.py               # Aplicación principal
│   ├── config.py            # Configuración
│   ├── cli.py               # Interfaz de línea de comandos
│   ├── api/                 # Generadores de API
│   │   ├── __init__.py
│   │   ├── auth_routes.py   # Rutas de autenticación
│   │   └── crud_generator.py # Generador de CRUD
│   ├── core/                # Lógica principal
│   │   ├── __init__.py
│   │   ├── entity_parser.py # Parser de YAML
│   │   └── model_generator.py # Generador de modelos
│   ├── db/                  # Base de datos
│   │   ├── __init__.py
│   │   ├── connection.py    # Gestión de conexiones
│   │   ├── models.py        # Modelos base generados
│   │   └── generated_models.py # Modelos Pydantic generados
│   └── security/            # Autenticación y seguridad
│       ├── __init__.py
│       └── auth.py          # Gestor de autenticación
├── tests/                   # Pruebas y ejemplos
│   ├── entidades/           # Archivos YAML de ejemplo
│   ├── main.py              # Script de prueba
│   ├── pruebas_curl.sh      # Pruebas de endpoints
│   └── ORM Tests/           # Pruebas de modelos ORM
├── pyproject.toml           # Configuración del proyecto
├── MANIFEST.in              # Archivos del paquete
└── README.md                # Documentación principal
```

## 🔑 Conceptos Clave

### **Sistema de Permisos "Yo"**
- Permite que usuarios solo accedan a registros donde un campo específico coincida con su ID
- Configuración: `yo: { campo_usuario: id }`
- Ejemplo: Usuario solo puede ver/editar contenedores donde `usuario = su_id`

### **Borrado Lógico**
- Soporte para soft delete configurable
- Campo configurable: `columna_borrado: 'habilitado'`
- Tipo configurable: `borrado_logico: 'boolean'` o `'timestamp'`

### **Diccionario PYDANTIC_MODELS**
- Diccionario centralizado con todos los modelos Pydantic generados
- Estructura: `{entidad: {accion: clase_modelo}}`
- Acciones: `create`, `update`, `response`
- Funciones utilitarias: `get_pydantic_model()`, `get_all_entities()`, etc.

## 📝 Formato YAML de Entidades

### **Estructura Básica**
```yaml
entidad: NombreEntidad
tabla: nombre_tabla
descripcion: Descripción de la entidad
campos:
  id:
    tipo: integer
    pk: true
  campo1:
    tipo: string
    max: 100
    required: true
    ejemplo: "valor ejemplo"
  campo2:
    tipo: integer
    fk: otra_entidad.id
    required: true
permisos:
  admin: [r, w, d]
  usuario:
    yo:
      campo_usuario: id
```

### **Tipos de Datos Soportados**
- `integer`: Números enteros
- `string`: Cadenas de texto
- `boolean`: Valores booleanos
- `datetime`: Fechas y horas
- `date`: Solo fechas
- `time`: Solo horas
- `float`: Números decimales
- `text`: Texto largo
- `json`: Datos JSON

### **Relaciones**
- `fk: entidad.campo`: Clave foránea
- `pk: true`: Clave primaria

## 🔧 Configuración

### **Configuración Básica**
```python
from yaml_to_backend import update_config, get_run_backend

update_config(
    ENTITIES_PATH='./entidades/',
    DB_HOST='localhost',
    DB_USER='root',
    DB_PASSWORD='1234',
    DB_NAME='mi_base',
    DB_PORT=3306,
    PORT=8000,
    INSTALL=True,
    DEBUG=True,
    LOG=True
)
```

### **Configuración de Autenticación**
```python
AUTH = {
    'tabla': 'usuarios',
    'columna_usuario': 'nombre',
    'columna_password': 'password',
    'superusuario': 'admin',
    'password_default': 'admin123',
    'columna_borrado': 'habilitado',
    'borrado_logico': 'boolean'
}
```

### **Usuarios Iniciales**
```python
INITIAL_USERS = [
    {'nombre': 'admin', 'password': 'admin123', 'rol': 'admin', 'habilitado': True},
    {'nombre': 'usuario1', 'password': 'user123', 'rol': 'usuario', 'habilitado': True}
]
```

## 🧪 Testing

### **Pruebas de Endpoints**
- Script: `tests/pruebas_curl.sh`
- Prueba todas las operaciones CRUD
- Verifica autenticación y permisos

### **Pruebas de Modelos ORM**
- Directorio: `tests/ORM Tests/`
- Framework: Pytest
- Prueba operaciones directas en modelos

### **Ejecución de Pruebas**
```bash
# Pruebas de endpoints
cd tests
./pruebas_curl.sh

# Pruebas de modelos ORM
pytest "ORM Tests/"
```

## 🔍 Preguntas y Respuestas del Usuario

### **Pregunta 1**: "¿Esto significa que un usuario con rol 'usuario' solo puede ver/editar registros donde el campo id coincida con su propio ID?"
**Respuesta**: Sí, exactamente. El rol puede llamarse "usuario" o cualquier otro nombre definido en el YAML.

### **Pregunta 2**: "¿Los roles se definen en los YAML?"
**Respuesta**: Sí, excepto por el rol "admin" que es un rol por defecto y siempre tendrá permisos completos.

### **Pregunta 3**: "¿Esos campos se deben configurar en los YAML?"
**Respuesta**: Sí, esos campos se deben configurar en los YAML.

### **Pregunta 4**: "¿Los YAML de ejemplo tienen nombre?"
**Respuesta**: Sí, el auth espera que se le indique qué columna corresponderá al username y password.

### **Pregunta 5**: "¿Los tests son manuales?"
**Respuesta**: En este momento son manuales, aunque es una buena idea que se ejecuten automáticamente en CI/CD.

### **Pregunta 6**: "¿Te gustaría incluir despliegue con Docker?"
**Respuesta**: Sí, sería una funcionalidad futura deseable.

## 🚀 Estado Actual del Proyecto

### **Versión Funcional**
- ✅ Backend funcionando en puerto 8007
- ✅ Autenticación JWT operativa
- ✅ Usuario admin creado correctamente (admin/admin123)
- ✅ Todas las pruebas CRUD pasando
- ✅ 5 entidades con operaciones completas
- ✅ Sistema de permisos "yo" funcionando
- ✅ Documentación completa actualizada

### **Problemas Resueltos**
- ❌ Puerto 8006 con problemas de conectividad → ✅ Puerto 8007 funcionando
- ❌ Login admin fallando → ✅ Login admin exitoso
- ❌ Event loop issues → ✅ Refactorizado autenticación
- ❌ Configuración AUTH incorrecta → ✅ Configuración corregida

### **Archivos de Prueba**
- `tests/entidades/`: 9 archivos YAML de ejemplo
- `tests/main.py`: Script de configuración y ejecución
- `tests/pruebas_curl.sh`: Pruebas automatizadas de endpoints
- `tests/ORM Tests/`: Pruebas de modelos ORM con Pytest

## 📚 Dependencias

### **Dependencias Principales**
- `fastapi>=0.104.0`: Framework web
- `uvicorn[standard]>=0.24.0`: Servidor ASGI
- `sqlalchemy>=2.0.0`: ORM
- `sqlmodel>=0.0.8`: Integración SQLAlchemy + Pydantic
- `pydantic>=2.0.0`: Validación de datos
- `pyyaml>=6.0`: Parsing YAML
- `bcrypt>=4.0.0`: Hashing de contraseñas
- `python-jose[cryptography]>=3.3.0`: Tokens JWT
- `asyncmy>=0.2.8`: Driver MySQL asíncrono
- `inflection>=0.5.0`: Transformación de strings
- `passlib[bcrypt]>=1.7.0`: Utilidades de hashing

### **Dependencias de Desarrollo**
- `pytest>=7.0.0`: Framework de testing
- `pytest-asyncio>=0.21.0`: Soporte async para pytest
- `httpx>=0.24.0`: Cliente HTTP para testing

## 🔮 Funcionalidades Futuras (No Implementadas)

1. **Sistema de migraciones**: Para manejar cambios en YAML
2. **Docker deployment**: Para facilitar despliegue
3. **Manejo de errores mejorado**: Para mayor robustez
4. **Validaciones personalizadas**: Más tipos de validación
5. **Tipos de datos adicionales**: UUID, decimal, enum
6. **CI/CD automatizado**: Para tests automáticos

## 🎯 Casos de Uso Típicos

### **Startup Necesitando API Rápida**
1. Definir entidades en YAML
2. Configurar base de datos
3. Ejecutar `python main.py`
4. API RESTful lista con documentación Swagger

### **Desarrollador Prototipando**
1. Crear archivos YAML con estructura de datos
2. Generar backend automáticamente
3. Probar endpoints con curl
4. Iterar rápidamente sobre cambios

### **Proyecto con Permisos Complejos**
1. Definir roles en YAML
2. Configurar permisos "yo" para acceso personal
3. Usar sistema de autenticación integrado
4. Control granular de acceso

## 🔧 Comandos Importantes

### **Instalación**
```bash
pip install yaml-to-backend
```

### **Ejecución**
```bash
cd tests
python main.py
```

### **Pruebas**
```bash
cd tests
./pruebas_curl.sh
pytest "ORM Tests/"
```

### **CLI**
```bash
yaml-to-backend --config entidades/ --port 8000
yaml-to-backend --validate entidades/
```

## 📖 Ejemplos de Uso

### **Acceso a Modelos Pydantic**
```python
from yaml_to_backend.db.generated_models import (
    PYDANTIC_MODELS,
    get_pydantic_model,
    get_all_entities
)

# Obtener modelo de creación
UsuarioCreate = get_pydantic_model("Usuario", "create")

# Listar entidades
entities = get_all_entities()  # ["Usuario", "Tarea", ...]
```

### **Uso de Endpoints**
```bash
# Login
curl -X POST "http://localhost:8007/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Crear entidad
curl -X POST "http://localhost:8007/api/roles/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"rol":"desarrollador"}'
```

## 🚨 Consideraciones Importantes

1. **No hay sistema de migraciones**: Si los YAML cambian, se debe recrear la base de datos
2. **Puerto 8007**: El puerto 8006 tiene problemas, usar 8007
3. **Entorno virtual**: Siempre activar `.venv` antes de ejecutar
4. **Directorio tests**: Ejecutar desde `tests/` para usar archivos de ejemplo
5. **Usuario admin**: Credenciales por defecto: admin/admin123
6. **Borrado lógico**: Configurado para campo 'habilitado' tipo boolean

## 📞 Información de Contacto

- **Autor**: IPAS Team
- **Email**: info@ipas.com
- **Repositorio**: https://github.com/cxmjg/yaml-to-backend
- **Licencia**: MIT

---

**Nota para IA**: Este documento contiene todo el contexto necesario para entender y trabajar con el proyecto YAML-to-Backend. Incluye la metodología, arquitectura, problemas resueltos, configuración y ejemplos de uso. Usar esta información como referencia completa para cualquier tarea relacionada con el proyecto. 