from ansys.mechanical.core import App

app = App()
print(app.license_manager.get_license_status("Ansys Mechanical Enterprise"))
