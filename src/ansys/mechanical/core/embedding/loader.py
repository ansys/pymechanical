"""clr_loader for pymechanical embedding. This loads the CLR on both windows and linux."""
from importlib.metadata import version
import os


def __get_clr_loader_version():
    return version("clr_loader")


def __get_mono(assembly_dir, config_dir):
    import clr_loader

    if __get_clr_loader_version() == "0.2.5":
        libmono = os.path.join(assembly_dir, "libmonosgen-2.0.so")
        mono = clr_loader.get_mono(
            set_signal_chaining=True,
            libmono=libmono,
            assembly_dir=assembly_dir.encode("utf-8"),
            config_dir=config_dir.encode("utf-8"),
        )
    else:
        # the bugs with get_mono are fixed (clr_loader PR #48)
        mono = clr_loader.get_mono(
            set_signal_chaining=True, assembly_dir=assembly_dir, config_dir=config_dir
        )
    return mono


def load_clr_mono(install_loc):
    """Load the clr using mono that is shipped with the unified install."""
    from pythonnet import load

    mono_dir = os.path.join(install_loc, "Tools", "mono", "Linux64")
    assembly_dir = os.path.join(mono_dir, "lib")
    config_dir = os.path.join(mono_dir, "etc")
    mono = __get_mono(assembly_dir, config_dir)
    load(mono)


def load_clr(install_loc: str) -> None:
    """Load the clr, the outcome of this function is that `clr` is usable."""
    if os.name == "nt":  # pragma: no cover
        return
    load_clr_mono(install_loc)


def is_pythonnet_3() -> bool:
    """Return whether pythonnet version 3 is used."""
    import clr

    return 3 == int(clr.__version__.split(".")[0])
