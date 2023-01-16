import os.path
import sys

# Make dummy_module.py available for autodoc.
sys.path.insert(0, os.path.dirname(__file__))


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # "sphinx_autodoc_typehints",
    "elba",
]

# autodoc_typehints = "description"
napoleon_numpy_docstring = True
napoleon_use_rtype = False

# typehints_fully_qualified = True
# typehints_document_rtype = True
# typehints_use_rtype = False

napoleon_numpy_returns_no_rtype = True
# napoleon_numpy_returns_no_rtype = False
