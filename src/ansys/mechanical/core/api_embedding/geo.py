
class Geometry:
    def __init__(self, geometry_import_obj):
        self._import_obj = geometry_import_obj
        self._preferences =  Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
        self._preferences.ProcessNamedSelections = True
        self._format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic

    def import_geometry(self, path: str):
        self._import_obj.Import(path, self._format,self._preferences)


class GeometryGroup:
    def __init__(self, geometry_import_group):
        self._group = geometry_import_group

    def add_geometry(self) -> Geometry:
        return Geometry(self._group.AddGeometryImport())


class Model:
    def __init__(self, app):
        self._model = app.model

    @property
    def geometry_group(self) -> GeometryGroup:
        return GeometryGroup(self._model.GeometryImportGroup)