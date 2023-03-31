"""Shims for embedded Mechanical.

These shims are used when APIs are released in newer versions of Mechanical,
but workarounds exist in an older release
"""


def import_materials(
    app: "ansys.mechanical.core.embedding.Application", material_file: str
) -> None:
    """Import material from matml file."""
    if app._version >= 232:
        materials = app.DataModel.Project.Model.Materials
        materials.Import(material_file)
    else:  # pragma: no cover
        material_file = material_file.replace("\\", "\\\\")
        script = 'DS.Tree.Projects.Item(1).LoadEngrDataLibraryFromFile("' + material_file + '");'
        app.ExtAPI.Application.ScriptByName("jscript").ExecuteCommand(script)
