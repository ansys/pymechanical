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


def set_false(appdata_option):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(appdata_option)
    app.ExtAPI.Graphics.ViewOptions.ShowTriad = False
    app.close()


def check_showtriad(appdata_option):
    """Return ShowTriad value."""
    app = launch_app(appdata_option)
    print(app.ExtAPI.Graphics.ViewOptions.ShowTriad)
    app.close()


def reset_showtriad(appdata_option):
    """Set ShowTriad value to True for user."""
    app = launch_app(appdata_option)
    app.ExtAPI.Graphics.ViewOptions.ShowTriad = True
    app.close()


try:
    appdata_option = sys.argv[1]
    action = sys.argv[2]

    if action == "Set":
        set_false(appdata_option)
    elif action == "Run":
        check_showtriad(appdata_option)
    elif action == "Reset":
        reset_showtriad(appdata_option)
except:
    launch_app("")
