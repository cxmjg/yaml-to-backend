#!/usr/bin/env python3
"""
Setup para YAML-to-Backend - Generador de Backends a partir de YAML
"""

from setuptools import setup, find_packages
import os

# Leer el README para la descripción larga
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="yaml-to-backend",
    version="0.1.0",
    author="IPAS Team",
    author_email="info@ipas.com",
    description="Generador de Backends a partir de YAML",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/cxmjg/yaml-to-backend",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Database",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.0",
        "sqlmodel>=0.0.8",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "bcrypt>=4.0.0",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart>=0.0.6",
        "asyncmy>=0.2.8",
        "python-dotenv>=1.0.0",
        "inflection>=0.5.0",
        "passlib[bcrypt]>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.24.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yaml-to-backend=yaml_to_backend.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "yaml_to_backend": ["*.yaml", "*.yml"],
    },
    keywords="yaml, backend, generator, fastapi, sqlalchemy, crud",
    project_urls={
        "Bug Reports": "https://github.com/cxmjg/yaml-to-backend/issues",
        "Source": "https://github.com/cxmjg/yaml-to-backend",
        "Documentation": "https://github.com/cxmjg/yaml-to-backend#readme",
    },
) 