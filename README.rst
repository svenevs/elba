elba
========================================================================================

Automatic type hint inference support for Sphinx Napoleon Numpy Style.

.. contents::

Usage
----------------------------------------------------------------------------------------

This extension monkey-patches the Sphinx `Napoleon <napoleon_>`_ extension's Numpy Style
to allow users who have type annotations in their pure python code to omit types in the
docstrings.  This requires using Sphinx 3.0 or later.  In your ``conf.py``:

.. _napoleon: https://www.sphinx-doc.org/en/latest/usage/extensions/napoleon.html

.. code-block:: py

    extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "elba"
    ]

    autodoc_typehints = "description"
    napoleon_numpy_docstring = True

    # Patched into napoleon via elba.  Default value is False.
    napoleon_numpy_returns_no_rtype = True

+----------------------------------------+----------------------------------------+
| Without ``elba``                       | With ``elba``                          |
+========================================+========================================+
| .. code-block:: py                     | .. code-block:: py                     |
|                                        |                                        |
|     def funky(a: int, b: str) -> bool: |     def funky(a: int, b: str) -> bool: |
|         """A funky function.           |         """A funky function.           |
|                                        |                                        |
|         Parameters                     |         Parameters                     |
|         ----------                     |         ----------                     |
|         a : int                        |         a                              |
|             Some important number.     |             Some important number.     |
|         b : str                        |         b                              |
|             The string of strings.     |             The string of strings.     |
|                                        |                                        |
|         Returns                        |         Returns                        |
|         -------                        |         -------                        |
|         bool                           |         How funky it really is.        |
|             How funky it really is.    |         """                            |
|         """                            |                                        |
+----------------------------------------+----------------------------------------+
| The difference:                                                                 |
+---------------------------------------------------------------------------------+
| .. code-block:: diff                                                            |
|                                                                                 |
|       def funky(a: int, b: str) -> bool:                                        |
|           """A funky function.                                                  |
|                                                                                 |
|           Parameters                                                            |
|           ----------                                                            |
|     -     a : int                                                               |
|     +     a                                                                     |
|               Some important number.                                            |
|     -     b : str                                                               |
|     +     b                                                                     |
|               The string of strings.                                            |
|                                                                                 |
|           Returns                                                               |
|           -------                                                               |
|     -     bool                                                                  |
|     -         How funky it really is.                                           |
|     +     How funky it really is.                                               |
|           """                                                                   |
+---------------------------------------------------------------------------------+

In words,

1. Parameter documentation no longer needs the type, ``autodoc`` will handle this for
   us (provided you actually have type hints in your code!).  As an aside, if you have
   type hints in the python signature and a different one in the docstring, the one in
   the *docstring* prevails.  Note: this extension has nothing to do with this
   capability, that comes entirely from ``autodoc_typehints = "description"`` (see:
   `autodoc_typehints <autodoc_typehints_>`_).
2. The Returns clause is no longer indented under the return type.  This will be
   extracted for us by ``autodoc``.  An important consideration here: only one return
   type is allowed (as is true for the python code).  By setting
   ``napoleon_numpy_returns_no_rtype = True``, you commit to a **global** change to
   the Numpy documentation style that does not use the docs-under-rtype format.  See
   next section.

.. _autodoc_typehints: https://www.sphinx-doc.org/en/latest/usage/extensions/autodoc.html#confval-autodoc_typehints

Why
----------------------------------------------------------------------------------------

I'm a huge fan of the Numpy style documentation.  I find it exceptionally readable as a
developer (and correspondingly, for users using ``help(funky)`` in their console).  With
the advent of type hints and the ``autodoc_typehints = "description"`` capabilities, I
don't want to continue duplicating my types -- once for the signature and once in the
docs.

The Numpy style, though, cannot be changed to stop duplication of the return types.  We
discussed this with the maintainers and they were reluctant to desire this change, since
they have to account for more than just python code (cython, c / manual docs, etc).
See `sphinx-doc/sphinx#7077 <sphinx_7077_>`_ for more information.  Put differently: the
scope of ``elba`` is restricted to pure python code with type hints, which is the only
thing that makes the dedentation of the ``Returns`` clause OK to do.  It is NOT ok for
Numpy in general!  We're on our own little island of shame and glory.

.. _sphinx_7077: https://github.com/sphinx-doc/sphinx/issues/7077

Contributing
----------------------------------------------------------------------------------------

Please feel free to raise an issue if you are having trouble, or a pull request if there
are improvements!  For example, maybe you need a way to globally adopt this style, but
have one or two outlier functions that need the old style?  This package is a hack, I'm
happy to find ways to help make the hack work better for you too :)

Development
----------------------------------------------------------------------------------------

We keep our development pretty simple. In short, make a virtual environment, then just
run everything in there. Here's the commands we use

.. code-block:: sh

   # create virtual environment
   python3 -m venv venv
   # activate it
   source venv/bin/activate
   # install elba in development mode, including the requirements
   # for developers
   pip install -e .[dev]
   # run the tests
   pytest tests

License
----------------------------------------------------------------------------------------

This package is licensed under the Apache v2.0 license.
