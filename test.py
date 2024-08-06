import ansys.mechanical.core as mech

import ansys.mechanical.core.embedding.viz.usd_converter as usd_converter

app = mech.App(version=251, db_file=r"C:\Users\mkoubaa\Desktop\sanderson.mechdat")

usd_converter.to_usd_file(app, "D:\\sanderson2.usda")