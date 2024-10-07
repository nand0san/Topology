# Archivo conf.py

import os
import sys
from setup import version as version_string

sys.path.insert(0, os.path.abspath('..'))

project = 'Topology'
copyright = '2024, Nand0san'
author = 'Nand0san'
version = version_string  # Asignar la versión desde el archivo version.py
language = 'en'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = ['_static']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Soporte para Google y NumPy docstrings
]

html_theme = 'shibuya'
