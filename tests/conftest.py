import pytest
import asyncio
import tempfile
import os
import yaml
from pathlib import Path

@pytest.fixture(scope="session")
def event_loop():
    """Crear un event loop para las pruebas asíncronas"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_entities_dir():
    """Fixture para crear un directorio temporal de entidades"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_entity_data():
    """Fixture con datos de entidad de ejemplo"""
    return {
        "entidad": "TestEntity",
        "tabla": "test_entities",
        "campos": {
            "id": {
                "tipo": "integer",
                "pk": True
            },
            "nombre": {
                "tipo": "string",
                "max": 100
            }
        },
        "permisos": {
            "admin": ["r", "w", "d"],
            "usuario": ["r"]
        }
    }

@pytest.fixture
def test_config():
    """Fixture con configuración de prueba"""
    return {
        'DB_HOST': 'localhost',
        'DB_PORT': 3306,
        'DB_USER': 'root',
        'DB_PASSWORD': 'root',
        'DB_NAME': 'test_db',
        'DEBUG': True,
        'PORT': 8000,
        'INSTALL': True,
        'LOG': True,
        'JWT_SECRET_KEY': 'test_secret_key',
        'JWT_ALGORITHM': 'HS256',
        'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': 30
    } 