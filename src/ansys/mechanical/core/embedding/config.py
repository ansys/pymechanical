"""Configuration system for embedded mechanical."""
import os


class Configuration:
    """Configuration class for Mechanical."""

    def __init__(self):
        """Construct a new Configuration instance."""
        self._no_act_addins = False
        self._no_wb1_addins = False

    @property
    def no_act_addins(self) -> bool:
        """Property to disable all ACT Addins."""
        return self._no_act_addins

    @no_act_addins.setter
    def no_act_addins(self, value: bool):
        """Setter of property to disable all ACT Addins."""
        self._no_act_addins = value

    @property
    def no_wb1_addins(self) -> bool:
        """Property to disable all WB1 Addins."""
        return self._no_wb1_addins

    @no_wb1_addins.setter
    def no_wb1_addins(self, value: bool):
        """Setter of property to disable all WB1 Addins."""
        self._no_wb1_addins = value


def configure(configuration: Configuration):
    """Apply the given configuration."""
    if configuration.no_act_addins:
        os.environ["ANSYS_MECHANICAL_STANDALONE_NO_ACT_EXTENSIONS"] = "1"

    # TODO - support a configuration option for no wb1 addins

    # TODO - support fine-grained configuration options, design an interface for WB1
    #        to accept these and have the ability to call that interface before
    #        loading WB. (perhaps WB.Initialize can take some new parameters!)
