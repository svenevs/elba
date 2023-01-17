import os.path
import sys

import pytest


def _check_sphinx_output_basic_res(
    res,
    napoleon_numpy_returns_no_rtype,
    napoleon_use_rtype,
    autodoc_typehints,
):
    # autodoc putting the type hints in the source description, no type hints
    # in line anywhere
    if autodoc_typehints == "source":
        if napoleon_use_rtype:
            assert "Returns:\n      A nice float" in res
            assert "Return type:\n      float" in res
        else:
            assert "Returns:\n      A nice float" in res

    # autodoc putting the type hints in the description (in line)
    elif autodoc_typehints == "description":
        if napoleon_use_rtype:
            assert "Returns:\n      A nice float" in res
            assert "Return type:\n      float" in res
        # If we ask for the return type to be in line, it is correctly
        # formatted in line in the description
        else:
            assert 'Returns:\n      "float" -- A nice float' in res

    # guard rail
    else:
        raise NotImplementedError(autodoc_typehints)


@pytest.mark.sphinx("text", testroot="basic")
@pytest.mark.parametrize(
    "napoleon_numpy_returns_no_rtype,napoleon_use_rtype,autodoc_typehints",
    (
        pytest.param(
            True,
            False,
            "source",
            id="elba-on_napoleon-rtype-inline_autodoc-source",
        ),
        pytest.param(
            True,
            True,
            "source",
            id="elba-on_napoleon-rtype-separate_autodoc-source",
            marks=pytest.mark.xfail(
                reason=(
                    "autodoc_typehints `source` seems to override "
                    "`napoleon_use_rtype`"
                )
            ),
        ),
        pytest.param(
            False,
            False,
            "source",
            id="elba-off_napoleon-rtype-inline_autodoc-source",
            marks=pytest.mark.xfail(
                reason=(
                    "Description incorrectly identified as type and formatted "
                    "with italics"
                )
            ),
        ),
        pytest.param(
            False,
            True,
            "source",
            id="elba-off_napoleon-rtype-separate_autodoc-source",
            marks=pytest.mark.xfail(
                reason=(
                    "Description incorrectly identified as type and placed "
                    "with 'Return type' header"
                )
            ),
        ),
        pytest.param(
            True,
            False,
            "description",
            id="elba-on_napoleon-rtype-inline_autodoc-description",
            marks=pytest.mark.xfail(
                reason=(
                    "autodoc_typehints `source` seems to override "
                    "`napoleon_use_rtype`"
                )
            ),
        ),
        pytest.param(
            True,
            True,
            "description",
            id="elba-on_napoleon-rtype-separate_autodoc-description",
        ),
        pytest.param(
            False,
            False,
            "description",
            id="elba-off_napoleon-rtype-inline_autodoc-description",
            marks=pytest.mark.xfail(
                reason=(
                    "Description incorrectly identified as type and formatted "
                    "with italics"
                )
            ),
        ),
        pytest.param(
            False,
            True,
            "description",
            id="elba-off_napoleon-rtype-separate_autodoc-description",
            marks=pytest.mark.xfail(
                reason=(
                    "Description incorrectly identified as type and placed "
                    "with 'Return type' header"
                )
            ),
        ),
    ),
)
def test_sphinx_output_basic(
    app,
    status,
    file_regression,
    napoleon_numpy_returns_no_rtype,
    napoleon_use_rtype,
    autodoc_typehints,
):
    app.config.master_doc = "rtype_from_type_annotations"
    app.config.napoleon_numpy_returns_no_rtype = napoleon_numpy_returns_no_rtype
    app.config.napoleon_use_rtype = napoleon_use_rtype
    app.config.autodoc_typehints = autodoc_typehints

    app.build()

    assert "build succeeded" in status.getvalue()

    out_path = os.path.join(
        app.srcdir, "_build", "text", f"{app.config.master_doc}.txt"
    )
    with open(out_path, "r") as fh:
        text_contents = fh.read()

    file_regression.check(text_contents, extension=".txt")

    _check_sphinx_output_basic_res(
        text_contents,
        napoleon_numpy_returns_no_rtype,
        napoleon_use_rtype,
        autodoc_typehints,
    )


@pytest.mark.sphinx("text", testroot="use-with-autodoc-typehints")
@pytest.mark.parametrize(
    "napoleon_use_rtype,typehints_document_rtype,typehints_use_rtype",
    (
        pytest.param(False, True, True, id="Return type separate"),
        pytest.param(False, True, False, id="Return type inline"),
    ),
)
@pytest.mark.parametrize(
    "napoleon_numpy_returns_no_rtype",
    (
        pytest.param(True, id="elba_on"),
        pytest.param(False, id="elba_off"),
    ),
)
def test_sphinx_output_with_autodoc_typehints(
    app,
    status,
    file_regression,
    napoleon_use_rtype,
    typehints_document_rtype,
    typehints_use_rtype,
    napoleon_numpy_returns_no_rtype,
):
    app.config.master_doc = "rtype_from_type_annotations"
    app.config.napoleon_use_rtype = napoleon_use_rtype
    app.config.typehints_document_rtype = typehints_document_rtype
    app.config.typehints_use_rtype = typehints_use_rtype
    app.config.napoleon_numpy_returns_no_rtype = napoleon_numpy_returns_no_rtype

    app.build()

    assert "build succeeded" in status.getvalue()

    out_path = os.path.join(
        app.srcdir, "_build", "text", f"{app.config.master_doc}.txt"
    )
    with open(out_path, "r") as fh:
        text_contents = fh.read()

    # Without elba, we get the description incorrectly identified as a type
    # and formatted with italics
    badly_formatted_return = "*A nice float*"
    if napoleon_numpy_returns_no_rtype:
        assert badly_formatted_return not in text_contents
    else:
        assert badly_formatted_return in text_contents

    file_regression.check(text_contents, extension=".txt")
