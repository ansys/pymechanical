"""clr_loader for pymechanical embedding. This loads the CLR on both windows and linux."""
import os


def __get_mono(assembly_dir, config_dir):
    import clr_loader

    libmono = os.path.join(assembly_dir, "libmonosgen-2.0.so")
    mono = clr_loader.get_mono(
        set_signal_chaining=True,
        libmono=libmono,  # TODO: find_mono is broken on clr-loader v0.2.6
        assembly_dir=assembly_dir,
        config_dir=config_dir,
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
