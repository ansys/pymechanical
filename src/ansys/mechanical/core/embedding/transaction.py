# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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

"""Transaction for embedded mechanical.

Can be used to speed up a block of code that modifies multiple objects.
This object ensures that the tree is not refreshed and that only the bare minimum
graphics and validations occur while the transaction is in scope.
The Transaction should only be used around code blocks that do not require state updates,
such as solving or meshing.
"""


class Transaction:  # When ansys-pythonnet issue #14 is fixed, this class will be removed
    """
    A class to speed up bulk user interactions using Ansys ACT Mechanical Transaction.

    Example
    -------
    >>> with Transaction() as transaction:
    ...     pass   # Perform bulk user interactions here
    ...

    """

    def __init__(self):
        """Initialize the Transaction class."""
        import clr

        clr.AddReference("Ansys.ACT.WB1")
        import Ansys

        self._transaction = Ansys.ACT.Mechanical.Transaction()
        self._disposed = False

    def __enter__(self):
        """Enter the context of the transaction."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context of the transaction and disposes of resources."""
        if not self._disposed:
            self._dispose()

    def _dispose(self):
        if self._disposed:
            return
        self._transaction.Dispose()
        self._disposed = True
