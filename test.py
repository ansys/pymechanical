
import ansys.mechanical.core as mech

project_file = r"C:\Users\mkoubaa\Desktop\sanderson.mechdat"
app = mech.App(version=242, db_file=project_file)
app.open(project_file)
app.plot()