"""Modelos generados automáticamente desde entidades YAML"""

from typing import Optional, Dict, Type, Any
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime

# Importar modelos existentes
from yaml_to_backend.db.models import Usuarios, SistemasOperativos, Roles, Perfiles, Imagenes, Contenedores, Aplicaciones, AplicacionImagen


class UsuariosCreate(BaseModel):
    """Modelo para crear Usuarios - Gestión de usuarios del sistema"""
    nombre: str
    password: str
    creado: datetime
    acceso: datetime
    habilitado: bool
    rol: int

class UsuariosUpdate(BaseModel):
    """Modelo para actualizar Usuarios"""
    nombre: Optional[str]
    password: Optional[str]
    creado: Optional[datetime]
    acceso: Optional[datetime]
    habilitado: Optional[bool]

class UsuariosResponse(BaseModel):
    """Modelo para respuesta de Usuarios"""
    id: int
    nombre: str
    password: str
    creado: datetime
    acceso: datetime
    habilitado: bool
    rol: int

class SistemasOperativosCreate(BaseModel):
    """Modelo para crear SistemasOperativos - Gestión de sistemas operativos disponibles"""
    nombre: str
    logo: str

class SistemasOperativosUpdate(BaseModel):
    """Modelo para actualizar SistemasOperativos"""
    nombre: Optional[str]
    logo: Optional[str]

class SistemasOperativosResponse(BaseModel):
    """Modelo para respuesta de SistemasOperativos"""
    id: int
    nombre: str
    logo: str

class RolesCreate(BaseModel):
    """Modelo para crear Roles - Gestión de roles de usuario"""
    rol: str

class RolesUpdate(BaseModel):
    """Modelo para actualizar Roles"""
    rol: Optional[str]

class RolesResponse(BaseModel):
    """Modelo para respuesta de Roles"""
    id: int
    rol: str

class PerfilesCreate(BaseModel):
    """Modelo para crear Perfiles - Gestión de perfiles de usuario"""
    nombre: str
    apellido: str
    email: str
    imagen: str
    usuario: int

class PerfilesUpdate(BaseModel):
    """Modelo para actualizar Perfiles"""
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[str]
    imagen: Optional[str]

class PerfilesResponse(BaseModel):
    """Modelo para respuesta de Perfiles"""
    id: int
    nombre: str
    apellido: str
    email: str
    imagen: str
    usuario: int

class ImagenesCreate(BaseModel):
    """Modelo para crear Imagenes - Gestión de imágenes de contenedores"""
    ubicacion: str
    nombre: str
    comandos: str
    logo: str
    sistemaOperativo: int

class ImagenesUpdate(BaseModel):
    """Modelo para actualizar Imagenes"""
    ubicacion: Optional[str]
    nombre: Optional[str]
    comandos: Optional[str]
    logo: Optional[str]

class ImagenesResponse(BaseModel):
    """Modelo para respuesta de Imagenes"""
    id: int
    ubicacion: str
    nombre: str
    comandos: str
    logo: str
    sistemaOperativo: int

class ContenedoresCreate(BaseModel):
    """Modelo para crear Contenedores - Gestión de contenedores de usuarios"""
    nombre: str
    http: int
    https: int
    puertos: str
    redes: str
    variables: str
    volumenes: str
    imagen: int
    usuario: int

class ContenedoresUpdate(BaseModel):
    """Modelo para actualizar Contenedores"""
    nombre: Optional[str]
    http: Optional[int]
    https: Optional[int]
    puertos: Optional[str]
    redes: Optional[str]
    variables: Optional[str]
    volumenes: Optional[str]

class ContenedoresResponse(BaseModel):
    """Modelo para respuesta de Contenedores"""
    id: int
    nombre: str
    http: int
    https: int
    puertos: str
    redes: str
    variables: str
    volumenes: str
    imagen: int
    usuario: int

class AplicacionesCreate(BaseModel):
    """Modelo para crear Aplicaciones - Gestión de aplicaciones disponibles"""
    nombre: str
    comando: str
    sistemaOperativo: int

class AplicacionesUpdate(BaseModel):
    """Modelo para actualizar Aplicaciones"""
    nombre: Optional[str]
    comando: Optional[str]

class AplicacionesResponse(BaseModel):
    """Modelo para respuesta de Aplicaciones"""
    id: int
    nombre: str
    comando: str
    sistemaOperativo: int

class AplicacionImagenCreate(BaseModel):
    """Modelo para crear AplicacionImagen - Relación entre aplicaciones e imágenes"""
    aplicacion: int
    imagen: int

class AplicacionImagenUpdate(BaseModel):
    """Modelo para actualizar AplicacionImagen"""

class AplicacionImagenResponse(BaseModel):
    """Modelo para respuesta de AplicacionImagen"""
    id: int
    aplicacion: int
    imagen: int



# =============================================================================
# DICCIONARIO CENTRALIZADO DE MODELOS PYDANTIC
# =============================================================================
# Este diccionario facilita el acceso programático a todos los modelos generados
# Estructura: {entidad: {accion: clase_modelo}}

PYDANTIC_MODELS: Dict[str, Dict[str, Type[BaseModel]]] = {
    "Usuarios": {
        "create": UsuariosCreate,
        "update": UsuariosUpdate,
        "response": UsuariosResponse
    },
    "SistemasOperativos": {
        "create": SistemasOperativosCreate,
        "update": SistemasOperativosUpdate,
        "response": SistemasOperativosResponse
    },
    "Roles": {
        "create": RolesCreate,
        "update": RolesUpdate,
        "response": RolesResponse
    },
    "Perfiles": {
        "create": PerfilesCreate,
        "update": PerfilesUpdate,
        "response": PerfilesResponse
    },
    "Imagenes": {
        "create": ImagenesCreate,
        "update": ImagenesUpdate,
        "response": ImagenesResponse
    },
    "Contenedores": {
        "create": ContenedoresCreate,
        "update": ContenedoresUpdate,
        "response": ContenedoresResponse
    },
    "Aplicaciones": {
        "create": AplicacionesCreate,
        "update": AplicacionesUpdate,
        "response": AplicacionesResponse
    },
    "AplicacionImagen": {
        "create": AplicacionImagenCreate,
        "update": AplicacionImagenUpdate,
        "response": AplicacionImagenResponse
    },
}

# =============================================================================
# FUNCIONES UTILITARIAS PARA ACCESO A MODELOS
# =============================================================================

def get_pydantic_model(entity_name: str, action: str) -> Type[BaseModel]:
    """
    Obtiene un modelo Pydantic específico por entidad y acción.
    
    Args:
        entity_name: Nombre de la entidad (ej: "Usuario", "Tarea")
        action: Acción del modelo ("create", "update", "response")
    
    Returns:
        Clase del modelo Pydantic solicitado
        
    Raises:
        KeyError: Si la entidad o acción no existe
    """
    try:
        return PYDANTIC_MODELS[entity_name][action]
    except KeyError:
        available_entities = list(PYDANTIC_MODELS.keys())
        available_actions = list(PYDANTIC_MODELS.get(entity_name, {}).keys())
        raise KeyError(
            f"Modelo no encontrado para entidad '{entity_name}' y acción '{action}'. "
            f"Entidades disponibles: {available_entities}. "
            f"Acciones disponibles para '{entity_name}': {available_actions}"
        )

def get_all_entities() -> list[str]:
    """Obtiene la lista de todas las entidades disponibles."""
    return list(PYDANTIC_MODELS.keys())

def get_entity_actions(entity_name: str) -> list[str]:
    """Obtiene las acciones disponibles para una entidad específica."""
    if entity_name not in PYDANTIC_MODELS:
        raise KeyError(f"Entidad '{entity_name}' no encontrada")
    return list(PYDANTIC_MODELS[entity_name].keys())

def validate_entity_action(entity_name: str, action: str) -> bool:
    """Valida si existe un modelo para la entidad y acción especificadas."""
    return entity_name in PYDANTIC_MODELS and action in PYDANTIC_MODELS[entity_name]

# =============================================================================
# ALIASES PARA ACCESO RÁPIDO (OPCIONAL)
# =============================================================================

# Acceso directo a modelos específicos
UsuariosCreateModel = PYDANTIC_MODELS["Usuarios"]["create"]
UsuariosUpdateModel = PYDANTIC_MODELS["Usuarios"]["update"]
UsuariosResponseModel = PYDANTIC_MODELS["Usuarios"]["response"]

SistemasOperativosCreateModel = PYDANTIC_MODELS["SistemasOperativos"]["create"]
SistemasOperativosUpdateModel = PYDANTIC_MODELS["SistemasOperativos"]["update"]
SistemasOperativosResponseModel = PYDANTIC_MODELS["SistemasOperativos"]["response"]

RolesCreateModel = PYDANTIC_MODELS["Roles"]["create"]
RolesUpdateModel = PYDANTIC_MODELS["Roles"]["update"]
RolesResponseModel = PYDANTIC_MODELS["Roles"]["response"]

PerfilesCreateModel = PYDANTIC_MODELS["Perfiles"]["create"]
PerfilesUpdateModel = PYDANTIC_MODELS["Perfiles"]["update"]
PerfilesResponseModel = PYDANTIC_MODELS["Perfiles"]["response"]

ImagenesCreateModel = PYDANTIC_MODELS["Imagenes"]["create"]
ImagenesUpdateModel = PYDANTIC_MODELS["Imagenes"]["update"]
ImagenesResponseModel = PYDANTIC_MODELS["Imagenes"]["response"]

ContenedoresCreateModel = PYDANTIC_MODELS["Contenedores"]["create"]
ContenedoresUpdateModel = PYDANTIC_MODELS["Contenedores"]["update"]
ContenedoresResponseModel = PYDANTIC_MODELS["Contenedores"]["response"]

AplicacionesCreateModel = PYDANTIC_MODELS["Aplicaciones"]["create"]
AplicacionesUpdateModel = PYDANTIC_MODELS["Aplicaciones"]["update"]
AplicacionesResponseModel = PYDANTIC_MODELS["Aplicaciones"]["response"]

AplicacionImagenCreateModel = PYDANTIC_MODELS["AplicacionImagen"]["create"]
AplicacionImagenUpdateModel = PYDANTIC_MODELS["AplicacionImagen"]["update"]
AplicacionImagenResponseModel = PYDANTIC_MODELS["AplicacionImagen"]["response"]
