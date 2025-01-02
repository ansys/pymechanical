
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

    def __enter__(self):
        """Enter the context of the transaction."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context of the transaction and disposes of resources."""
        self._transaction.Dispose()
