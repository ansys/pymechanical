# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Configuration system for embedded mechanical."""
import os


class AddinConfiguration:
    """Configuration class for Mechanical."""

    def __init__(self, addin_configuration: str = "Mechanical", **kwargs):
        """Construct a new Configuration instance."""
        # by default, disable ACT addins on linux
        disable_act_addins: bool = os.name != "nt"

        self._no_act_addins = kwargs.get("disable_act_addins", disable_act_addins)
        self._addin_configuration = addin_configuration

    @property
    def no_act_addins(self) -> bool:
        """Property to disable all ACT Addins."""
        return self._no_act_addins

    @no_act_addins.setter
    def no_act_addins(self, value: bool):
        self._no_act_addins = value

    @property
    def addin_configuration(self) -> str:
        """WB1 Addin configuration name."""
        return self._addin_configuration

    @addin_configuration.setter
    def addin_configuration(self, value: str):
        self._addin_configuration = value


def configure(configuration: AddinConfiguration):
    """Apply the given configuration."""
    if configuration.no_act_addins:
        os.environ["ANSYS_MECHANICAL_STANDALONE_NO_ACT_EXTENSIONS"] = "1"
