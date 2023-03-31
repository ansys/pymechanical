"""Miscellaneous embedding tests"""
import os
import shutil
import tempfile

import pytest

@pytest.mark.embedding
def test_app_repr(embedded_app):
    """Test repr of the Application class."""
    app_repr_lines = repr(embedded_app).splitlines()
    assert app_repr_lines[0].startswith("Ansys Mechanical")
    assert app_repr_lines[1].startswith("Product Version")
    assert app_repr_lines[2].startswith("Software build date:")

@pytest.mark.embedding
def test_app_save_open(embedded_app):
    """Test save and open of the Application class."""
    import clr
    import System

    # save without a save_as throws an exception
    with pytest.raises(System.Exception):
        embedded_app.save()

    embedded_app.DataModel.Project.Name = "PROJECT 1"
    tmpname = tempfile.mktemp()
    project_file = f"{tmpname}.mechdat"
    project_files = f"{tmpname}_Mech_Files"
    embedded_app.save_as(project_file)
    try:
        embedded_app.new()
        embedded_app.open(project_file)
        assert embedded_app.DataModel.Project.Name == "PROJECT 1"
        embedded_app.DataModel.Project.Name = "PROJECT 2"
        embedded_app.save()
        embedded_app.new()
        embedded_app.open(project_file)
        assert embedded_app.DataModel.Project.Name == "PROJECT 2"
        embedded_app.new()
    except:
        # clean up the project files
        shutil.rmtree(project_files)
        os.remove(project_file)

@pytest.mark.embedding
def test_app_version(embedded_app):
    """Test version of the Application class."""
    version = embedded_app.version
    assert type(version) is int
    assert version >= 231
