########################################################################################
# Copyright 2020 Stephen McDowell                                                      #
#                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                      #
# you may not use this file except in compliance with the License.                     #
# You may obtain a copy of the License at                                              #
#                                                                                      #
#     http://www.apache.org/licenses/LICENSE-2.0                                       #
#                                                                                      #
# Unless required by applicable law or agreed to in writing, software                  #
# distributed under the License is distributed on an "AS IS" BASIS,                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.             #
# See the License for the specific language governing permissions and                  #
# limitations under the License.                                                       #
########################################################################################
from typing import List, Tuple


__version__ = "0.1.0.dev"


def setup(app: "sphinx.application.Sphinx"):
    app.setup_extension("sphinx.ext.napoleon")
    app.add_config_value("napoleon_numpy_returns_no_rtype", False, "env")

    def _consume_returns_section(self) -> List[Tuple[str, str, List[str]]]:
        if not self._config.napoleon_numpy_returns_no_rtype:
            return self._consume_fields(prefer_type=True)
        else:
            self._consume_empty()
            desc_lines = []
            while not self._is_section_break():
                desc_lines.append(self._lines.popleft())

            return [("", "", desc_lines)]

    # NOTE: defer import to here so that setuptools does not require sphinx.
    from sphinx.ext.napoleon.docstring import NumpyDocstring
    NumpyDocstring._consume_returns_section = _consume_returns_section

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True
    }
