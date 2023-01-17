import os.path
import sys

# Make dummy_module.py available for autodoc.
sys.path.insert(0, os.path.dirname(__file__))


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "elba",
]

napoleon_numpy_docstring = True
