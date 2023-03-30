"""This is the .NET assembly resolving for embedding Ansys Mechanical.

Note that for some Mechanical Addons - additional resolving may be
necessary. A resolve handler is shipped with Ansys Mechanical on windows
starting in version 23.1 and on linux starting in version 23.2
"""


def resolve(version):
    """Resolve function for all versions of Ansys Mechanical."""
    import clr  # isort: skip
    import System  # isort: skip

    clr.AddReference("Ansys.Mechanical.Embedding")
    import Ansys  # isort: skip

    assembly_resolver = Ansys.Mechanical.Embedding.AssemblyResolver
    if version == 231:  # pragma: no cover
        resolve_handler = assembly_resolver.WindowsResolveEventHandler
    else:
        resolve_handler = assembly_resolver.MechanicalResolveEventHandler
    System.AppDomain.CurrentDomain.AssemblyResolve += resolve_handler
