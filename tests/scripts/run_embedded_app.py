"""Launch embedded instance."""
import sys

import ansys.mechanical.core as pymechanical


def launch_app(appdata_option):
    """Launch embedded instance of app."""
    if appdata_option == "True":
        app = pymechanical.App(private_appdata=appdata_option)
    else:
        app = pymechanical.App()
    return app


def set_showtriad(appdata_option, value):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(appdata_option)
    app.ExtAPI.Graphics.ViewOptions.ShowTriad = value
    app.close()


def print_showtriad(appdata_option):
    """Return ShowTriad value."""
    app = launch_app(appdata_option)
    print(app.ExtAPI.Graphics.ViewOptions.ShowTriad)
    app.close()


try:
    appdata_option = sys.argv[1]
    action = sys.argv[2]

    if action == "Set":
        set_showtriad(appdata_option, False)
    elif action == "Run":
        print_showtriad(appdata_option)
    elif action == "Reset":
        set_showtriad(appdata_option, True)
except:
    launch_app("")
