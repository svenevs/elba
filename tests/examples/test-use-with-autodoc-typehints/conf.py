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

# use in when we don't have autodoc type hints
# autodoc_typehints = "description"

napoleon_numpy_docstring = True
