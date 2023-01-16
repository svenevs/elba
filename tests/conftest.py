import os.path
import shutil
from sphinx.testing.path import path

import pytest


pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture
def rootdir(tmpdir):
    src = path(os.path.dirname(__file__)) / "examples"
    dst = tmpdir.join("examples")
    shutil.copytree(src, dst)

    yield path(dst)
