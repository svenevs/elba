import os.path
import sys

import pytest


@pytest.mark.sphinx("text", testroot="basic")
@pytest.mark.parametrize(
    "napoleon_use_rtype",
    (
        pytest.param(False, id="Napoleon return type inline"),
        pytest.param(True, id="Napoleon return type separate"),
    )
)
@pytest.mark.parametrize(
    "napoleon_numpy_returns_no_rtype",
    (
        pytest.param(True, id="elba_on"),
        pytest.param(False, id="elba_off"),
    )
)
def test_sphinx_output_basic(
    app,
    status,
    file_regression,
    napoleon_use_rtype,
    napoleon_numpy_returns_no_rtype,
):
    app.config.master_doc = "rtype_from_type_annotations"
    app.config.napoleon_use_rtype = napoleon_use_rtype
    app.config.napoleon_numpy_returns_no_rtype = napoleon_numpy_returns_no_rtype

    app.build()

    assert "build succeeded" in status.getvalue()

    out_path = os.path.join(
        app.srcdir,
        "_build",
        "text",
        f"{app.config.master_doc}.txt"
    )
    with open(out_path, "r") as fh:
        text_contents = fh.read()

    # With elba
    if napoleon_numpy_returns_no_rtype:
        # No matter what the value of `napoleon_use_rtype`, the return type
        # isn't included in line. This surprises me a bit, but maybe is the
        # correct behaviour if we're just letting everything fall back to the
        # value of `autodoc_typehints`?
        assert "Returns:\n      A nice float" in text_contents

    # Without elba
    else:
        # If we ask for the return type to be separate, the description
        # is incorrectly identified as a type and placed as such
        if napoleon_use_rtype:
            assert "Return type:\n      A nice float" in text_contents
        # If we ask for the return type to be in line, we get the description
        # incorrectly identified as a type and formatted with italics
        else:
            assert "*A nice float*" in text_contents

    file_regression.check(text_contents, extension=".txt")


@pytest.mark.sphinx("text", testroot="use-with-autodoc-typehints")
@pytest.mark.parametrize(
    "napoleon_use_rtype,typehints_document_rtype,typehints_use_rtype",
    (
        pytest.param(False, True, True, id="Return type separate"),
        pytest.param(False, True, False, id="Return type inline"),
    )
)
@pytest.mark.parametrize(
    "napoleon_numpy_returns_no_rtype",
    (
        pytest.param(True, id="elba_on"),
        pytest.param(False, id="elba_off"),
    )
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
        app.srcdir,
        "_build",
        "text",
        f"{app.config.master_doc}.txt"
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
