import pathlib

import pytest

import ansys.mechanical.core
from ansys.mechanical.core.errors import VersionError


def print_info(mechanical, name="no_name", info="no_info"):
    print(mechanical._channel_str + " " + name + " " + info)


def func(mechanical, script, name):
    result = None

    if len(script) > 0:
        print_info(mechanical, name, f"input={script}")
        result = mechanical.run_python_script(script)
        print_info(mechanical, name, f"result={result}")

    return name, result


@pytest.mark.remote_session_launch
def test_available_ports():
    with pytest.raises(RuntimeError):
        ansys.mechanical.core.pool.available_ports(2, starting_port=65536)


@pytest.mark.remote_session_launch
def test_minimum_instances():
    with pytest.raises(ValueError):
        ansys.mechanical.core.pool.LocalMechanicalPool(1)


@pytest.mark.remote_session_launch
def test_map(mechanical_pool):
    if mechanical_pool is None:
        return

    inputs = [("2+3", "first"), ("3+4", "second")]
    results = mechanical_pool.map(func, inputs, clear_at_start=True, progress_bar=True, wait=True)
    print(results)

    # result could come in different order

    # [('first', '5'), ('second', '7')]
    if results[0][0] == "first":
        assert results[0][1] == "5"
    else:
        assert results[0][0] == "second"
        assert results[0][1] == "7"

    if results[1][0] == "second":
        assert results[1][1] == "7"
    else:
        assert results[1][0] == "first"
        assert results[1][1] == "5"


def func_no_args(mechanical):
    result = None

    print_info(mechanical)

    return result


@pytest.mark.remote_session_launch
def test_map_no_job(mechanical_pool):
    if mechanical_pool is None:
        return

    inputs = None
    results = mechanical_pool.map(
        func_no_args, inputs, clear_at_start=True, progress_bar=True, wait=True
    )
    print(results)

    assert results[0] is None
    assert results[1] is None


@pytest.mark.remote_session_launch
def test_run_batch_no_job(mechanical_pool, tmp_path: pathlib.Path):
    if mechanical_pool is None:
        return

    files = ["non_existent_file.py"]
    with pytest.raises(FileNotFoundError):
        mechanical_pool.run_batch(files)

    f1 = tmp_path.joinpath("batch1.py")
    print(f"created {f1}")
    f2 = tmp_path.joinpath("batch2.py")
    print(f"created {f2}")

    f1.write_text("2+3")
    f2.write_text("3+4")

    fpath1 = str(f1)
    fpath2 = str(f2)

    files = [fpath1, fpath2]
    results = mechanical_pool.run_batch(files)

    # result could come in different order
    if results[0] == "5":
        assert results[1] == "7"
    else:
        assert results[0] == "7"
        assert results[1] == "5"


@pytest.mark.remote_session_launch
def test_version_error():
    with pytest.raises(VersionError):
        raise VersionError("Requires Mechanical 2023 R1 or later.")
