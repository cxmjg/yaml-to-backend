#!/bin/bash

# Script para publicar YAML-to-Backend en PyPI

set -e  # Salir si hay algún error

echo "🚀 Iniciando publicación de YAML-to-Backend..."

# Verificar que estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: No se encontró pyproject.toml"
    exit 1
fi

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf dist/ build/ *.egg-info/

# Construir la distribución
echo "🔨 Construyendo distribución..."
python -m build

# Verificar el build
echo "✅ Verificando build..."
twine check dist/*

# Preguntar si subir a TestPyPI
read -p "¿Subir a TestPyPI? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Subiendo a TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✅ Subido a TestPyPI exitosamente!"
    echo "🔗 URL: https://test.pypi.org/project/yaml-to-backend/"
fi

# Preguntar si subir a PyPI oficial
read -p "¿Subir a PyPI oficial? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Subiendo a PyPI oficial..."
    twine upload dist/*
    echo "✅ Subido a PyPI oficial exitosamente!"
    echo "🔗 URL: https://pypi.org/project/yaml-to-backend/"
fi

echo "🎉 ¡Publicación completada!" 