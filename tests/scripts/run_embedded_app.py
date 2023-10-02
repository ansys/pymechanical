"""Launch embedded instance."""
import sys

import ansys.mechanical.core as pymechanical


def launch_app(version, private_appdata):
    """Launch embedded instance of app."""
    app = pymechanical.App(version=version, private_appdata=private_appdata)
    return app


def set_showtriad(version, appdata_option, value):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(version, appdata_option)
    app.ExtAPI.Graphics.ViewOptions.ShowTriad = value
    app.close()


def print_showtriad(version, appdata_option):
    """Return ShowTriad value."""
    app = launch_app(version, appdata_option)
    print(app.ExtAPI.Graphics.ViewOptions.ShowTriad)
    app.close()


if __name__ == "__main__":
    version = int(sys.argv[1])
    if len(sys.argv) == 2:
        launch_app(version, False)
        sys.exit(0)

    appdata_option = sys.argv[2]
    action = sys.argv[3]

    private_appdata = appdata_option == "True"
    if action == "Set":
        set_showtriad(version, private_appdata, False)
    elif action == "Run":
        print_showtriad(version, private_appdata)
    elif action == "Reset":
        set_showtriad(version, private_appdata, True)
