# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".. _ref_tips_03:

Project tree
------------

Display the heirarchial Mechanical project structure.
"""

# %%
# Import necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~


from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# %%
# Embed Mechanical and set global variables

app = App()
app.update_globals(globals())
print(app)


# %%
# Download the mechdb file
# ~~~~~~~~~~~~~~~~~~~~~~~~

mechdb_path = download_file("graphics_test.mechdb", "pymechanical", "test_files")

# %%
# Load the mechdb file inside Mechanical

app.open(mechdb_path)

# %%
# Display the project tree
# ~~~~~~~~~~~~~~~~~~~~~~~~

app.print_tree()

# %%
# Display the tree only under the first analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app.print_tree(Model.Analyses[0])


# %%
# Cleanup
# ~~~~~~~

delete_downloads()
app.new()
