import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Añadir la ruta raíz del proyecto

from version import version_string  # Importar desde version.py

project = 'Topology'
copyright = '2024, Nand0san'
author = 'Nand0san'
version = version_string
language = 'en'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = ['_static']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Soporte para Google y NumPy docstrings
]

html_theme = 'shibuya'
