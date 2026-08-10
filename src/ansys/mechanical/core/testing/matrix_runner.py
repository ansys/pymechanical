# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Reproducer and Test Matrix Runner for PyMechanical.

Executes customer test/reproducer scripts across multiple Mechanical versions
(Docker containers or local installations) and execution modes (embedding, remote gRPC, batch).
Generates a structured Markdown report (README.md) and logs.
"""

import dataclasses
import datetime
import os
from pathlib import Path
import shutil
import subprocess  # nosec: B404
import sys
import time
from typing import List, Optional, Tuple

import ansys.tools.common.path as atp
import click


@dataclasses.dataclass
class MatrixResult:
    """Store results of a single version x mode run."""

    version: str
    mode: str
    target_type: str  # 'docker' or 'local'
    status: str  # 'PASS', 'FAIL', 'SKIP'
    duration: float = 0.0
    exit_code: int = 0
    message: str = ""
    stdout: str = ""
    stderr: str = ""


def resolve_setting(cli_val: Optional[str], env_var: str, default_val: str) -> str:
    """Resolve configuration precedence: Environment variable > CLI Argument > Default."""
    env_val = os.environ.get(env_var, "").strip()
    if env_val:
        return env_val
    if cli_val is not None and str(cli_val).strip() != "":
        return str(cli_val).strip()
    return default_val


class MatrixRunner:
    """Orchestrates test script execution across Mechanical versions and modes."""

    def __init__(
        self,
        script_path: Optional[str] = None,
        versions: Optional[List[str]] = None,
        modes: Optional[List[str]] = None,
        run_type: Optional[str] = None,
        output_file: Optional[str] = None,
        log_file: Optional[str] = None,
    ):
        """Initialize the matrix runner using parameters or environment variables.
        
        Precedence: Environment Variable > Argument / Parameter > Default
        """
        versions_param = ",".join(versions) if isinstance(versions, list) else versions
        modes_param = ",".join(modes) if isinstance(modes, list) else modes

        final_script = resolve_setting(script_path, "PYMECHANICAL_MATRIX_SCRIPT", "tests/scripts/repro.py")
        final_versions_str = resolve_setting(versions_param, "PYMECHANICAL_MATRIX_VERSIONS", "242,251,252,261")
        final_modes_str = resolve_setting(modes_param, "PYMECHANICAL_MATRIX_MODES", "embedding,remote,batch")
        final_run_type = resolve_setting(run_type, "PYMECHANICAL_MATRIX_RUN_TYPE", "auto")
        final_output = resolve_setting(output_file, "PYMECHANICAL_MATRIX_OUTPUT", "README.md")
        final_log = resolve_setting(log_file, "PYMECHANICAL_MATRIX_LOG", "matrix_execution.log")

        self.script_path = Path(final_script).resolve()
        self.versions = [v.strip() for v in final_versions_str.split(",") if v.strip()]
        self.modes = [m.strip() for m in final_modes_str.split(",") if m.strip()]
        self.run_type = final_run_type.lower()
        self.output_file = Path(final_output).resolve()
        self.log_file = Path(final_log).resolve()
        self.results: List[MatrixResult] = []


    def log(self, message: str):
        """Log message to stdout and log file."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception:
            pass

    def check_docker_available(self) -> bool:
        """Check if Docker engine is available on the system."""
        if not shutil.which("docker"):
            return False
        try:
            res = subprocess.run(
                ["docker", "info"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
            )
            return res.returncode == 0
        except Exception:
            return False

    def check_docker_image(self, version_str: str) -> Tuple[bool, str]:
        """Check if Docker image for version exists or can be pulled."""
        # Convert short version format e.g. '251' or '25.1' to image tag
        if "." in version_str:
            tag = f"{version_str}.0" if version_str.count(".") == 1 else version_str
        else:
            v_num = int(version_str)
            major = v_num // 10
            minor = v_num % 10
            tag = f"{major}{minor}.1.0" if major >= 25 else f"{major}{minor}.2.0"

        image_name = f"ghcr.io/ansys/mechanical:{tag}"

        # Check local images first
        res = subprocess.run(
            ["docker", "image", "inspect", image_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if res.returncode == 0:
            return True, image_name

        # Try pulling image
        self.log(f"Attempting docker pull for {image_name}...")
        pull_res = subprocess.run(
            ["docker", "pull", image_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if pull_res.returncode == 0:
            return True, image_name

        return False, image_name

    def check_local_installation(self, version_str: str) -> Tuple[bool, Optional[str]]:
        """Check if Mechanical is installed locally for the given version."""
        try:
            v_int = int(version_str.replace(".", ""))
        except ValueError:
            v_int = None

        exe_path = atp.get_mechanical_path(allow_input=False, version=v_int)
        if exe_path and os.path.exists(exe_path):
            return True, exe_path
        return False, None

    def run_docker_cell(self, image_name: str, version_str: str, mode: str) -> MatrixResult:
        """Run a single test in a Docker container with xvfb-run and mechanical-env."""
        license_env = os.environ.get("ANSYSLMD_LICENSE_FILE", "")
        script_dir = self.script_path.parent
        script_name = self.script_path.name

        base_docker_args = [
            "docker", "run", "--rm",
            "--security-opt", "seccomp=unconfined",
            "-v", f"{script_dir}:/workspace",
            "-w", "/workspace",
            "-e", f"ANSYSLMD_LICENSE_FILE={license_env}",
            image_name,
        ]

        # Construct command based on mode with xvfb-run & mechanical-env
        if mode == "embedding":
            cmd_args = base_docker_args + [
                "bash", "-c",
                f"if command -v mechanical-env >/dev/null 2>&1; then xvfb-run mechanical-env python3 {script_name}; else xvfb-run python3 {script_name}; fi"
            ]
        elif mode == "remote":
            cmd_args = base_docker_args + [
                "bash", "-c",
                f"if command -v mechanical-env >/dev/null 2>&1; then xvfb-run mechanical-env ansys-mechanical -grpc 10000 -i {script_name}; else xvfb-run ansys-mechanical -grpc 10000 -i {script_name}; fi"
            ]
        elif mode == "batch":
            cmd_args = base_docker_args + [
                "bash", "-c",
                f"if command -v mechanical-env >/dev/null 2>&1; then xvfb-run mechanical-env ansys-mechanical -b -i {script_name}; else xvfb-run ansys-mechanical -b -i {script_name}; fi"
            ]
        else:
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="docker",
                status="SKIP",
                message=f"Unknown execution mode '{mode}'",
            )

        start_time = time.time()
        try:
            res = subprocess.run(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
                check=False,
                text=True,
            )
            duration = round(time.time() - start_time, 2)
            status = "PASS" if res.returncode == 0 else "FAIL"
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="docker",
                status=status,
                duration=duration,
                exit_code=res.returncode,
                stdout=res.stdout,
                stderr=res.stderr,
                message="Successfully executed" if status == "PASS" else f"Exited with code {res.returncode}",
            )
        except subprocess.TimeoutExpired:
            duration = round(time.time() - start_time, 2)
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="docker",
                status="FAIL",
                duration=duration,
                exit_code=-1,
                message="Execution timed out (300s limit)",
            )
        except Exception as e:
            duration = round(time.time() - start_time, 2)
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="docker",
                status="FAIL",
                duration=duration,
                exit_code=-1,
                stderr=str(e),
                message=f"System error: {e}",
            )

    def run_local_cell(self, exe_path: str, version_str: str, mode: str) -> MatrixResult:
        """Run a single test using local Mechanical installation with mechanical-env and xvfb-run if on Linux."""
        start_time = time.time()
        env = os.environ.copy()
        script_dir = str(self.script_path.parent)
        script_name = self.script_path.name

        is_linux_sys = sys.platform.startswith("linux")
        has_xvfb = bool(shutil.which("xvfb-run"))
        has_mech_env = bool(shutil.which("mechanical-env"))

        # Base execution command
        if mode == "embedding":
            base_cmd = [sys.executable, str(self.script_path)]
        elif mode == "batch":
            base_cmd = ["ansys-mechanical", "-exe", exe_path, "-b", "-i", str(self.script_path)]
        elif mode == "remote":
            base_cmd = ["ansys-mechanical", "-exe", exe_path, "-port", "10000", "-i", str(self.script_path)]
        else:
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="local",
                status="SKIP",
                message=f"Unknown execution mode '{mode}'",
            )

        cmd_args = list(base_cmd)
        if is_linux_sys:
            if has_mech_env:
                cmd_args = ["mechanical-env", "-r", version_str] + cmd_args
            if has_xvfb:
                cmd_args = ["xvfb-run"] + cmd_args

            cmd_args = ["ansys-mechanical", "-exe", exe_path, "-b", "-i", str(self.script_path)]
        elif mode == "remote":
            cmd_args = ["ansys-mechanical", "-exe", exe_path, "-port", "10000", "-i", str(self.script_path)]
        else:
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="local",
                status="SKIP",
                message=f"Unknown execution mode '{mode}'",
            )

        try:
            res = subprocess.run(
                cmd_args,
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                timeout=300,
                check=False,
                text=True,
            )
            duration = round(time.time() - start_time, 2)
            status = "PASS" if res.returncode == 0 else "FAIL"
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="local",
                status=status,
                duration=duration,
                exit_code=res.returncode,
                stdout=res.stdout,
                stderr=res.stderr,
                message="Successfully executed" if status == "PASS" else f"Exited with code {res.returncode}",
            )
        except subprocess.TimeoutExpired:
            duration = round(time.time() - start_time, 2)
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="local",
                status="FAIL",
                duration=duration,
                exit_code=-1,
                message="Execution timed out (300s limit)",
            )
        except Exception as e:
            duration = round(time.time() - start_time, 2)
            return MatrixResult(
                version=version_str,
                mode=mode,
                target_type="local",
                status="FAIL",
                duration=duration,
                exit_code=-1,
                stderr=str(e),
                message=f"Error executing local cell: {e}",
            )

    def execute_matrix(self):
        """Execute full matrix across versions and modes with fault-tolerance and auto-skipping."""
        self.log(f"Starting PyMechanical Matrix Runner")
        self.log(f"Script: {self.script_path}")
        self.log(f"Versions: {self.versions}")
        self.log(f"Modes: {self.modes}")

        if not self.script_path.exists():
            self.log(f"WARNING: Test script {self.script_path} does not exist. Creating default sample script.")
            self.script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.script_path, "w", encoding="utf-8") as f:
                f.write(
                    "# Sample PyMechanical reproducer script\n"
                    "import ansys.mechanical.core as pymechanical\n"
                    "print(f'PyMechanical version: {pymechanical.__version__}')\n"
                )

        docker_available = self.check_docker_available()
        self.log(f"Docker available: {docker_available}")

        for version in self.versions:
            target_type = None
            image_name = None
            exe_path = None

            # Determine execution target (local or docker)
            if self.run_type in ("auto", "local"):
                local_ok, exe_path = self.check_local_installation(version)
                if local_ok:
                    target_type = "local"

            if target_type is None and self.run_type in ("auto", "docker"):
                if docker_available:
                    img_ok, image_name = self.check_docker_image(version)
                    if img_ok:
                        target_type = "docker"

            # If version is missing on both local and docker, auto-skip all modes for this version
            if target_type is None:
                self.log(f"⚠️ SKIPPING version {version}: No local installation or docker image found.")
                for mode in self.modes:
                    self.results.append(
                        MatrixResult(
                            version=version,
                            mode=mode,
                            target_type="none",
                            status="SKIP",
                            message="Version not installed or Docker image unavailable",
                        )
                    )
                continue

            self.log(f"Target for version {version}: {target_type} ({image_name or exe_path})")

            for mode in self.modes:
                self.log(f"Running Version {version} | Mode {mode} [{target_type}]...")
                try:
                    if target_type == "docker" and image_name:
                        result = self.run_docker_cell(image_name, version, mode)
                    elif target_type == "local" and exe_path:
                        result = self.run_local_cell(exe_path, version, mode)
                    else:
                        result = MatrixResult(
                            version=version,
                            mode=mode,
                            target_type="none",
                            status="SKIP",
                            message="Target engine unavailable",
                        )
                except Exception as e:
                    self.log(f"Unhandled exception during cell execution: {e}")
                    result = MatrixResult(
                        version=version,
                        mode=mode,
                        target_type=target_type or "none",
                        status="FAIL",
                        message=f"Runner exception: {e}",
                    )

                self.results.append(result)
                status_icon = "🟢 PASS" if result.status == "PASS" else ("🔴 FAIL" if result.status == "FAIL" else "⚠️ SKIP")
                self.log(f"Result: {status_icon} ({result.duration}s)")

        self.generate_report()

    def generate_report(self):
        """Generate formatted Markdown report (README.md)."""
        now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        license_info = os.environ.get("ANSYSLMD_LICENSE_FILE", "Not specified")

        report_lines = [
            "# 🧪 PyMechanical Reproducer & Test Matrix Report",
            "",
            f"**Test Script:** `{self.script_path.name}`  ",
            f"**Execution Timestamp:** `{now_utc}`  ",
            f"**License Server Configured:** `{license_info}`  ",
            "",
            "---",
            "",
            "## 📊 Execution Summary Matrix",
            "",
        ]

        # Build matrix header
        headers = ["Version", "Target Engine"] + [f"Mode: `{m}`" for m in self.modes]
        report_lines.append("| " + " | ".join(headers) + " |")
        report_lines.append("| " + " | ".join([":---"] * len(headers)) + " |")

        # Group results by version
        ver_map = {}
        for r in self.results:
            if r.version not in ver_map:
                ver_map[r.version] = {}
            ver_map[r.version][r.mode] = r

        for version, mode_map in ver_map.items():
            first_res = list(mode_map.values())[0] if mode_map else None
            target_str = first_res.target_type if first_res else "unknown"

            row = [f"**{version}**", f"`{target_str}`"]
            for mode in self.modes:
                res = mode_map.get(mode)
                if not res:
                    row.append("⚪ N/A")
                elif res.status == "PASS":
                    row.append(f"🟢 PASS ({res.duration}s)")
                elif res.status == "FAIL":
                    row.append(f"🔴 FAIL ({res.duration}s)")
                else:
                    row.append(f"⚠️ SKIP")
            report_lines.append("| " + " | ".join(row) + " |")

        report_lines.extend([
            "",
            "---",
            "",
            "## 🔍 Detailed Logs & Tracebacks",
            "",
        ])

        for res in self.results:
            if res.status == "SKIP":
                continue

            status_icon = "🟢 PASS" if res.status == "PASS" else "🔴 FAIL"
            report_lines.append(f"### {status_icon} Version {res.version} — Mode: `{res.mode}` ({res.target_type.upper()})")
            report_lines.append(f"- **Duration:** {res.duration} seconds")
            report_lines.append(f"- **Exit Code:** `{res.exit_code}`")
            report_lines.append(f"- **Status Message:** {res.message}")
            report_lines.append("")

            if res.stderr or res.stdout:
                report_lines.append("<details>")
                report_lines.append(f"<summary>Click to expand stdout / stderr logs for {res.version} ({res.mode})</summary>")
                report_lines.append("")
                report_lines.append("```text")
                if res.stdout:
                    report_lines.append("=== STDOUT ===")
                    report_lines.append(res.stdout.strip())
                if res.stderr:
                    report_lines.append("=== STDERR ===")
                    report_lines.append(res.stderr.strip())
                report_lines.append("```")
                report_lines.append("</details>")
                report_lines.append("")

        report_content = "\n".join(report_lines)

        # Write output file
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        self.log(f"Report successfully saved to {self.output_file}")

        # If running inside GitHub Actions, append report to $GITHUB_STEP_SUMMARY
        github_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if github_summary_path and os.path.exists(os.path.dirname(github_summary_path)):
            try:
                with open(github_summary_path, "a", encoding="utf-8") as gf:
                    gf.write(report_content + "\n")
                self.log("Report posted to GitHub Step Summary ($GITHUB_STEP_SUMMARY).")
            except Exception as e:
                self.log(f"Failed writing to GITHUB_STEP_SUMMARY: {e}")


@click.command(name="test-matrix", help="Run customer reproducer script across Mechanical versions & execution modes.")
@click.option("-s", "--script", "script_path", default=None, help="Path to customer reproducer Python script.")
@click.option("-v", "--versions", "versions_str", default=None, help="Comma-separated versions to test (e.g. '242,251,252,261').")
@click.option("-m", "--modes", "modes_str", default=None, help="Comma-separated execution modes (e.g. 'embedding,remote,batch').")
@click.option("-o", "--output", "output_file", default=None, help="Path to output Markdown report (default: README.md).")
@click.option("-t", "--run-type", "run_type", default=None, help="Execution target engine ('auto', 'docker', 'local').")
def cli(
    script_path: Optional[str] = None,
    versions_str: Optional[str] = None,
    modes_str: Optional[str] = None,
    output_file: Optional[str] = None,
    run_type: Optional[str] = None,
):
    """CLI handler for matrix runner."""
    versions = [v.strip() for v in versions_str.split(",") if v.strip()] if versions_str else None
    modes = [m.strip() for m in modes_str.split(",") if m.strip()] if modes_str else None

    runner = MatrixRunner(
        script_path=script_path,
        versions=versions,
        modes=modes,
        run_type=run_type,
        output_file=output_file,
    )
    runner.execute_matrix()


def run_matrix():
    """Main CLI entry point for matrix runner."""
    cli()


if __name__ == "__main__":
    cli()
