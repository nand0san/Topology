import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Añadir la ruta raíz del proyecto


project = 'Topology'
copyright = '2024, Nand0san'
author = 'Nand0san'
# version = version_string
language = 'en'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# html_static_path = ['_static']  # not use of CSS

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',  # Habilitar el soporte de MathJax
]

html_theme = 'shibuya'
