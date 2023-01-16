import os.path
import sys

import pytest


@pytest.mark.sphinx("text", testroot="basic-use")
def test_sphinx_output(app, status):
    app.config.master_doc = "rtype_from_type_annotations"
    app.build()

    assert "build succeeded" in status.getvalue()

    out_path = os.path.join(
        app.srcdir,
        "_build",
        "text",
        "rtype_from_type_annotations.txt"
    )
    with open(out_path, "r") as fh:
        text_contents = fh.read().replace("–", "--")
        import pdb
        pdb.set_trace()
        print(text_contents)
        assert False, "Check something"
