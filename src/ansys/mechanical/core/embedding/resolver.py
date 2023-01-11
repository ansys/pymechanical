"""This is the .NET assembly resolving for embedding Ansys Mechanical.

Note that for some Mechanical Addons - additional resolving may be
necessary. This logic is shipped with Ansys Mechanical on windows starting
in version 23.1 and on linux starting in version 23.2
"""

import os


def resolver222():
    """Resolve function for version 22.2, the first version supported by Mechanical Embedding."""
    installpath = os.environ[f"AWP_ROOT222"]

    def _resolver(sender, args):
        assembly_file_name = args.Name.split(",")[0]
        dll_name = f"{assembly_file_name}.dll"

        if "ACT.Core" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "ACT", "bin", "Win64", dll_name)
            )

        if (
            "Ans.Core" in assembly_file_name
            or "Microsoft.Scripting" in assembly_file_name
            or "Ans.UI.Toolkit" in assembly_file_name
            or "QUT.ShiftReduceParser" in assembly_file_name
            or "TabularData.Interop" in assembly_file_name
            or "Ans.Addins.Infrastructure" in assembly_file_name
        ):
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Framework", "bin", "Win64", dll_name)
            )

        if "TabularData.Commands" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "TabularData", "bin", "Win64", dll_name)
            )

        if "Ans.EngineeringData" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "EngineeringData", "bin", "Win64", dll_name)
            )

        if "Ans.JobManager" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "JobManager", "bin", "Win64", dll_name)
            )

        if "Ans.JobMgrAdapter" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "JobMgrAdapter", "bin", "Win64", dll_name)
            )

        if "Ans.Units.Core" in assembly_file_name:
            return System.Reflection.Assembly.LoadFrom(
                os.path.join(installpath, "Addins", "Units", "bin", "Win64", dll_name)
            )

        # for debugging - we get a lot of names like Ansys.ACT.Math.__spec__
        # which probably come from pythonnet runtime.
        # I only want to print ones that look like:
        #  "DllName, Version=version, Culture=neutral, PublicKeyToken=null"
        if "Culture" in assembly_file_name:
            print(assembly_file_name)

        return System.Reflection.Assembly.LoadFrom(
            os.path.join(installpath, "aisol", "bin", "winx64", dll_name)
        )

    return _resolver


def resolve(version):
    """Resolve function for all versions of Ansys Mechanical."""
    import clr # isort: skip
    import System # isort: skip

    clr.AddReference("Ansys.Mechanical.Embedding")
    import Ansys

    if version > 222:
        assembly_resolver = Ansys.Mechanical.Embedding.AssemblyResolver
        if version == 231:
            resolve_handler = assembly_resolver.WindowsResolveEventHandler
        else:
            try:
                resolve_handler = assembly_resolver.MechanicalResolveEventHandler
            except:
                # TODO - remove me, once people are on a newer build
                resolve_handler = assembly_resolver.WindowsResolveEventHandler
        System.AppDomain.CurrentDomain.AssemblyResolve += resolve_handler
    else:
        System.AppDomain.CurrentDomain.AssemblyResolve += resolver222()
