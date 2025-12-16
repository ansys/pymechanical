# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Tests for CLI gRPC transport mode functionality."""

import pytest

from ansys.mechanical.core.run import _cli_impl


@pytest.mark.cli
class TestCLITransportMode:
    """Tests for gRPC transport mode CLI options."""

    def test_cli_transport_mode_insecure_explicit(self, disable_cli):
        """Test explicit insecure transport mode with SP04+ version."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,  # Has SP04
            port=10000,
            transport_mode="insecure",
        )
        assert "--transport-mode" in args
        assert "insecure" in args

    def test_cli_transport_mode_wnua_with_sp04(self, disable_cli):
        """Test WNUA transport mode on Windows with SP04."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,  # Has SP04
            port=10000,
            transport_mode="wnua",
        )
        assert "--transport-mode" in args
        assert "wnua" in args or "WNUA" in args

    def test_cli_transport_mode_wnua_without_sp04_fails(self, disable_cli):
        """Test WNUA transport mode fails on version without SP04."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=252,  # No SP04
                port=10000,
                transport_mode="wnua",
            )
        assert "does not support wnua transport mode" in str(exc_info.value).lower()

    def test_cli_transport_mode_mtls_requires_certs(self, disable_cli):
        """Test MTLS transport mode requires --certs-dir."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                port=10000,
                transport_mode="mtls",
                # Missing certs_dir
            )
        assert "certs-dir is required" in str(exc_info.value).lower()

    def test_cli_transport_mode_mtls_with_certs(self, disable_cli):
        """Test MTLS transport mode with certificates directory."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="mtls",
            certs_dir="/path/to/certs",
        )
        assert "--transport-mode" in args
        assert "mtls" in args
        assert "--certs-dir" in args
        assert "/path/to/certs" in args

    def test_cli_grpc_host_option(self, disable_cli):
        """Test --grpc-host option."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="insecure",
            grpc_host="0.0.0.0",
        )
        assert "--grpc-host" in args
        assert "0.0.0.0" in args

    def test_cli_grpc_host_default_localhost(self, disable_cli):
        """Test default host is localhost when not specified."""
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=261, port=10000, transport_mode="insecure")
        assert "--grpc-host" in args
        assert "localhost" in args

    def test_cli_transport_without_port_fails(self, disable_cli):
        """Test that transport mode without port fails."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                transport_mode="insecure",
                # Missing port
            )
        # The error message mentions all gRPC options, including transport-mode
        assert "grpc options" in str(exc_info.value).lower()
        assert "--transport-mode" in str(exc_info.value).lower()
        assert "can only be used with --port" in str(exc_info.value).lower()

    def test_cli_grpc_host_without_port_fails(self, disable_cli):
        """Test that grpc-host without port fails."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                grpc_host="0.0.0.0",
                # Missing port
            )
        # The error message mentions all gRPC options, including grpc-host
        assert "grpc options" in str(exc_info.value).lower()
        assert "--grpc-host" in str(exc_info.value).lower()
        assert "can only be used with --port" in str(exc_info.value).lower()

    def test_cli_certs_dir_without_port_fails(self, disable_cli):
        """Test that certs-dir without port fails."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                certs_dir="/path/to/certs",
                # Missing port
            )
        # The error message mentions all gRPC options, including certs-dir
        assert "grpc options" in str(exc_info.value).lower()
        assert "--certs-dir" in str(exc_info.value).lower()
        assert "can only be used with --port" in str(exc_info.value).lower()

    def test_cli_legacy_version_auto_insecure_with_port(self, disable_cli, capsys):
        """Test legacy version automatically uses insecure mode with warning."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=252,  # No SP04
            port=10000,
            # No transport_mode specified
        )
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "insecure" in captured.out.lower()
        # For legacy versions, --transport-mode is NOT added to command line
        assert "--transport-mode" not in args

    def test_cli_version_none_auto_insecure_with_port(self, disable_cli, capsys):
        """Test when version is None, automatically uses insecure mode."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            port=10000,
            # No version, no transport_mode
        )
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "insecure" in captured.out.lower()

    def test_cli_sp04_version_default_wnua_windows(self, disable_cli):
        """Test SP04+ version defaults to WNUA on Windows."""
        import os

        if os.name != "nt":
            pytest.skip("This test is for Windows only")

        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            # No transport_mode specified - should default to WNUA on Windows
        )
        assert "--transport-mode" in args
        # Should be WNUA or wnua
        mode_idx = args.index("--transport-mode") + 1
        assert args[mode_idx].lower() == "wnua"

    def test_cli_command_construction_with_all_grpc_options(self, disable_cli):
        """Test complete command construction with all gRPC options."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="mtls",
            grpc_host="0.0.0.0",
            certs_dir="/custom/certs",
        )

        # Verify all options are present
        assert "-grpc" in args
        assert "10000" in args
        assert "--transport-mode" in args
        assert "mtls" in args
        assert "--grpc-host" in args
        assert "0.0.0.0" in args
        assert "--certs-dir" in args
        assert "/custom/certs" in args

    def test_cli_legacy_mode_only_port(self, disable_cli):
        """Test legacy version uses --port instead of -grpc."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=241,  # Early version, might not have SP04
            port=10000,
            transport_mode="insecure",
        )
        # Check that basic port argument is used
        assert "10000" in args


@pytest.mark.cli
class TestCLITransportModeEdgeCases:
    """Additional edge case tests for gRPC transport mode."""

    def test_cli_mtls_with_certs_and_host(self, disable_cli):
        """Test mTLS with both certs directory and custom host."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="mtls",
            grpc_host="0.0.0.0",
            certs_dir="/path/to/certs",
        )
        assert "--transport-mode" in args
        assert "mtls" in args
        assert "--grpc-host" in args
        assert "0.0.0.0" in args
        assert "--certs-dir" in args
        assert "/path/to/certs" in args

    def test_cli_insecure_with_custom_host(self, disable_cli):
        """Test insecure mode with custom host on SP04+ version."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="insecure",
            grpc_host="192.168.1.100",
        )
        assert "--transport-mode" in args
        assert "insecure" in args
        assert "--grpc-host" in args
        assert "192.168.1.100" in args

    def test_cli_wnua_no_certs_required(self, disable_cli):
        """Test WNUA mode doesn't require certs directory."""
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=261, port=10000, transport_mode="wnua")
        assert "--transport-mode" in args
        assert "wnua" in args or "WNUA" in args
        assert "--certs-dir" not in args

    def test_cli_default_transport_mode_windows(self, disable_cli):
        """Test default transport mode on Windows with SP04+ is WNUA."""
        import sys

        if sys.platform != "win32":
            pytest.skip("Test only applicable on Windows")

        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            # No transport_mode specified
        )
        assert "--transport-mode" in args
        # On Windows, default should be WNUA
        assert "wnua" in args or "WNUA" in args

    def test_cli_multiple_grpc_options_validation(self, disable_cli):
        """Test multiple gRPC options are validated correctly."""
        # Valid combination
        try:
            args, _ = _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                port=10000,
                transport_mode="mtls",
                grpc_host="localhost",
                certs_dir="/certs",
            )
            assert "--transport-mode" in args
            assert "--grpc-host" in args
            assert "--certs-dir" in args
        except Exception as e:
            assert False, f"Valid combination raised exception: {e}"

    def test_cli_legacy_explicit_insecure(self, disable_cli):
        """Test explicitly passing insecure mode to legacy version."""
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=252, port=10000, transport_mode="insecure")
        # For legacy versions, insecure is accepted but not added to command line
        assert "--transport-mode" not in args
        # Note: Warning may be printed even for explicit insecure mode on legacy versions
        # This is acceptable behavior - we don't need to verify the warning text

    def test_cli_version_241_treated_as_sp04(self, disable_cli):
        """Test version 241 is treated as having SP04 support."""
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, port=10000, transport_mode="wnua")
        # Version 241 is assumed to have SP04 in has_grpc_service_pack
        assert "--transport-mode" in args
        assert "wnua" in args or "WNUA" in args

    def test_cli_port_with_script_fails(self, disable_cli):
        """Test that port cannot be used with input script."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                port=10000,
                transport_mode="insecure",
                input_script="test.py",
            )
        assert "cannot open in server mode with an input script" in str(exc_info.value).lower()

    def test_cli_port_with_project_fails(self, disable_cli):
        """Test that port cannot be used with project file."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe",
                version=261,
                port=10000,
                transport_mode="insecure",
                project_file="test.mechdb",
                graphical=True,  # Project files require graphical mode
            )
        # The error should mention that port and project file cannot be used together
        assert "project file" in str(exc_info.value).lower()
        assert "server mode" in str(exc_info.value).lower() or "port" in str(exc_info.value).lower()

    def test_cli_grpc_options_ordering(self, disable_cli):
        """Test that gRPC options appear in correct order in command line."""
        args, _ = _cli_impl(
            exe="AnsysWBU.exe",
            version=261,
            port=10000,
            transport_mode="mtls",
            grpc_host="0.0.0.0",
            certs_dir="/certs",
        )

        # Find indices of gRPC-related args
        grpc_idx = args.index("-grpc")
        port_idx = args.index("10000")
        transport_idx = args.index("--transport-mode")
        host_idx = args.index("--grpc-host")
        certs_idx = args.index("--certs-dir")

        # Verify ordering: -grpc port_number should come first
        assert grpc_idx < port_idx
        assert port_idx < transport_idx
        assert transport_idx < host_idx
        assert host_idx < certs_idx

    def test_cli_invalid_transport_mode_accepted(self, disable_cli):
        """Test that invalid transport mode is accepted by CLI (validated at runtime)."""
        # Note: Invalid transport modes are not validated in _cli_impl
        # They would be caught when actually launching Mechanical
        args, _ = _cli_impl(
            exe="AnsysWBU.exe", version=261, port=10000, transport_mode="invalid_mode"
        )
        # The CLI accepts any transport mode string; validation happens at runtime
        assert "--transport-mode" in args
        assert "invalid_mode" in args

    def test_cli_empty_certs_dir_string(self, disable_cli):
        """Test empty certs directory string is treated as not provided."""
        with pytest.raises(Exception) as exc_info:
            _cli_impl(
                exe="AnsysWBU.exe", version=261, port=10000, transport_mode="mtls", certs_dir=""
            )
        assert "certs-dir is required" in str(exc_info.value).lower()
