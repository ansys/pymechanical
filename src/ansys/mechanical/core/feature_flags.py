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

"""Mechanical beta feature flags."""

import typing
import warnings


class FeatureFlags:
    """Supported feature flag names."""

    ThermalShells = "Mechanical.ThermalShells"
    MultistageHarmonic = "Mechanical.MultistageHarmonic"


def get_feature_flag_names() -> typing.List[str]:
    """Get the available feature flags."""
    return [x for x in dir(FeatureFlags) if "_" not in x]


def _get_flag_arg(flagname: str) -> str:
    """Get the command line name for a given feature flag."""
    if hasattr(FeatureFlags, flagname):
        return getattr(FeatureFlags, flagname)
    warnings.warn(f"Using undocumented feature flag {flagname}")
    return flagname


def get_command_line_arguments(flags: typing.List[str]):
    """Get the command line arguments as an array for the given flags."""
    return ["-featureflags", ";".join([_get_flag_arg(flag) for flag in flags])]
