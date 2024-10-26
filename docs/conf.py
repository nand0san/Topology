import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Topology'
copyright = '2024, Nand0san'
author = 'Nand0san'
language = 'en'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
]

# Opciones de autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__, __repr__, __eq__',
    'inherited-members': True,
    'show-inheritance': True
}
autodoc_typehints = 'description'

html_theme = 'shibuya'
