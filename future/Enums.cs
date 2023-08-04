using Ansys.Common.Interop.DSObjectTypes;

namespace Ansys.Mechanical.Future.Enums
{
    public enum GeometryType
    {
        Solid = DSGeometryType.kSolidGeometry,
        Sheet = DSGeometryType.kSheetGeometry
    }

    public enum TransferFileFormat
    {
        HDF5 = 0
    }
}
