# Criterios de Aceptación: Generador de Backends a partir de YAML

## 🔎 Historia de Usuario

Como desarrollador, quiero definir entidades y permisos en archivos YAML y generar automáticamente un backend asincrónico en Python con endpoints RESTful CRUD, autenticación y autorización basada en roles, para poder desplegar soluciones rápidas, seguras y personalizables con pruebas automáticas y configuraciones centralizadas.

---

## ⚖️ Criterios de Aceptación

### Ὅ5 Estructura del Proyecto

```
mi_proyecto/
├── main.py                  # Levanta y ejecuta el backend
├── config.py                # Configuraciones generales del backend
├── requirements.txt         # Dependencias del proyecto
├── backend/                 # Código fuente principal
│   ├── core/                # Lógica base, autenticación, utilidades
│   ├── db/                  # Conexión y modelos ORM
│   ├── api/                 # Endpoints auto-generados
│   ├── security/            # Middleware y autorización
│   └── tests/               # Tests unitarios
```

> La carpeta `entidades/` puede ubicarse en cualquier ruta, especificada por `ENTITIES_PATH` en `config.py`.

---

### 🔹 Configuración (config.py)

```python
ENTITIES_PATH = './entidades/'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'mi_base'
DEBUG = True
PORT = 8000
INSTALL = True
LOG = True

# Config de usuarios
AUTH = {
    'tabla': 'usuarios',
    'columna_usuario': 'username',
    'columna_password': 'password',
    'superusuario': 'admin',
    'password_default': 'admin123',
    'columna_borrado': 'deleted_at',  # puede ser 'is_deleted' (boolean) o 'deleted_at' (timestamp)
    'borrado_logico': 'timestamp'     # 'boolean' o 'timestamp'
}
```

---

### 📋 Ejemplo de Archivo YAML de Entidad

```yaml
entidad: Usuario
tabla: usuarios
campos:
  id:
    tipo: integer
    pk: true
  username:
    tipo: string
    max: 50
  password:
    tipo: string
    max: 200
  rol:
    tipo: string
permisos:
  admin: [r, w, d]
  usuario: [yo]
```

```yaml
entidad: Tarea
tabla: tareas
campos:
  id:
    tipo: integer
    pk: true
  titulo:
    tipo: string
  descripcion:
    tipo: string
  usuario_id:
    tipo: integer
    fk: usuarios.id
permisos:
  admin: [r, w, d]
  usuario:
    yo:
      campo_usuario: usuario_id
```

---

### 🔐 Autenticación

* Se genera por defecto un endpoint `POST /api/auth/login` que devuelve un JWT si las credenciales son válidas.
* Se utiliza `username` y `password` (configurable en `AUTH`).
* Las contraseñas se almacenan en la base de datos usando hashing seguro.

---

### 🔒 Autorización y Roles

* Cada entidad define los permisos por rol: `r` (read), `w` (write), `d` (delete), o `yo` (filtro por usuario).
* `yo` significa:

  * Si la entidad es el usuario logueado: solo puede acceder a sus propios datos (`usuarios.id = <id_actual>`).
  * Si es una entidad relacionada: solo accede a datos vinculados mediante FK, por ejemplo `tareas.usuario_id = <id_actual>`.

---

### 🚧 Instalación y Reinicialización de Base

* Si `INSTALL = True`, al levantar `main.py` se:

  1. Conecta a la base de datos.
  2. Borra todas las tablas.
  3. Regenera las tablas desde los YAML.
  4. Inserta usuarios iniciales definidos en `config.py`.

---

### ⚖️ Endpoints Generados

Todos los endpoints están bajo el prefijo `/api/`.

Ejemplo:

```http
GET /api/usuarios
POST /api/usuarios
GET /api/usuarios/{id}
PUT /api/usuarios/{id}
DELETE /api/usuarios/{id}
```

Para permisos tipo `yo`, también se genera:

```http
GET /api/usuarios/yo
```

---

### ⚙️ Tecnologías y Librerías

* Python >= 3.10
* FastAPI (async endpoints)
* SQLAlchemy (ORM)
* pydantic (validación de datos)
* PyYAML (lectura de archivos YAML)
* bcrypt (hash de contraseñas)
* python-dotenv (opcional)
* pytest + httpx (tests)

---

### 🔮 Tests Automáticos

* Generados automáticamente al crear los endpoints.
* Verifican:

  * Autenticación
  * CRUD por rol y permisos
  * Filtros `yo`
* Se ejecutan al finalizar la generación, si falla una prueba, se corrige y se reintenta hasta que pasen.
* Los tests viven en `tests/`.

---

### 🔄 Flujo de Ejecución

1. `main.py` importa `config.py`
2. Lee los YAML desde `ENTITIES_PATH`
3. Genera modelos ORM y rutas
4. Crea o reinicia la base si `INSTALL = True`
5. Inicia el backend en `localhost:<PORT>`

---

### 🔄 Futuras extensiones

* Soporte para relaciones ManyToMany.
* Exportación OpenAPI documentada.
* Soporte para filtros, ordenamientos y paginación en los endpoints.
* Soporte para otros motores como PostgreSQL, SQLite o MongoDB.

---

✅ **Este criterio de aceptación es el punto de partida para la generación de la librería y motor de backend automático.**
