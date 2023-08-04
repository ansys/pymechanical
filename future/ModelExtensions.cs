using Ansys.ACT.Automation.Mechanical;
using Ansys.Common.Interop.DSObjectTypes;
using Ansys.Mechanical.DataModel.Enums;

namespace Ansys.Mechanical.Future
{
    public class ModelHDF5ExportSettings
    {
        public Enums.GeometryType GeometryType { get; set; }
        public WBUnitSystemType UnitSystemType { get; set; }
    }

    public static class ModelExtensions
    {
        public static void ExportHDF5TransferFile(
            this Model model,
            string filename,
            Enums.TransferFileFormat format,
            ModelHDF5ExportSettings settings)
        {
            if (format != Enums.TransferFileFormat.HDF5)
                throw new System.Exception("Unknown format");
            model.InternalObject.WriteHDF5TransferFile((DSGeometryType)settings.GeometryType, filename, (int)settings.UnitSystemType, 0);
        }
    }
}
