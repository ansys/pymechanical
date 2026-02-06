# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

""".. _ref_steady_state_thermal:

Steady state thermal analysis
-----------------------------

This example problem demonstrates the use of a
simple steady-state thermal analysis to determine the temperatures,
thermal gradients, heat flow rates, and heat fluxes that are caused
by thermal loads that do not vary over time. A steady-state thermal
analysis calculates the effects of steady thermal loads on a system
or component, in this example, a long bar model.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
from typing import TYPE_CHECKING

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

if TYPE_CHECKING:
    import Ansys

# %%
# Initialize the embedded application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = App(globals=globals())
print(app)

# Set the path for the output files (images, gifs, mechdat)
output_path = Path.cwd() / "out"

# Set the camera orientation to isometric view
app.helpers.setup_view("iso")

# %%
# Download the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file from the ansys/example-data repository
geometry_path = download_file("LONGBAR.x_t", "pymechanical", "embedding")

# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

app.helpers.import_geometry(geometry_path, process_named_selections=True)

# Visualize the model in 3D
app.plot()

# %%
# Add steady state thermal analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a steady state thermal analysis to the model
model = app.Model
model.AddSteadyStateThermalAnalysis()
# Set the Mechanical unit system to Standard MKS
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS

# Get the steady state thermal analysis
stat_therm = model.Analyses[0]

# Add a coordinate system to the model
coordinate_systems = model.CoordinateSystems

# Add two coordinate systems
lcs1 = coordinate_systems.AddCoordinateSystem()
lcs1.OriginX = Quantity("0 [m]")

lcs2 = coordinate_systems.AddCoordinateSystem()
lcs2.OriginX = Quantity("0 [m]")
lcs2.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalY

# %%
# Create named selections and construction geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to add a named selection


def setup_named_selection(name, scoping_method=GeometryDefineByType.Worksheet):
    """Create a named selection with the specified scoping method and name.

    Parameters
    ----------
    name : str
        The name of the named selection.
    scoping_method : GeometryDefineByType
        The scoping method for the named selection.

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.NamedSelection
        The created named selection.
    """
    ns = model.AddNamedSelection()
    ns.ScopingMethod = scoping_method
    ns.Name = name
    return ns


# %%
# Create a function to add generation criteria to the named selection


def add_generation_criteria(
    named_selection,
    value,
    set_active_action_criteria=True,
    active=True,
    action=SelectionActionType.Add,
    entity_type=SelectionType.GeoFace,
    criterion=SelectionCriterionType.Size,
    operator=SelectionOperatorType.Equal,
):
    """Add generation criteria to the named selection.

    Parameters
    ----------
    named_selection : Ansys.ACT.Automation.Mechanical.NamedSelection
        The named selection to which the criteria will be added.
    value : Quantity
        The value for the criteria.
    active : bool
        Whether the criteria is active.
    action : SelectionActionType
        The action type for the criteria.
    entity_type : SelectionType
        The entity type for the criteria.
    criterion : SelectionCriterionType
        The criterion type for the criteria.
    operator : SelectionOperatorType
        The operator for the criteria.
    """
    generation_criteria = named_selection.GenerationCriteria
    criteria = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()

    set_criteria_properties(
        criteria,
        value,
        set_active_action_criteria,
        active,
        action,
        entity_type,
        criterion,
        operator,
    )

    if set_active_action_criteria:
        generation_criteria.Add(criteria)


# %%
# Create a function to set the properties of the generation criteria


def set_criteria_properties(
    criteria,
    value,
    set_active_action_criteria=True,
    active=True,
    action=SelectionActionType.Add,
    entity_type=SelectionType.GeoFace,
    criterion=SelectionCriterionType.Size,
    operator=SelectionOperatorType.Equal,
):
    """Set the properties of the generation criteria.

    Parameters
    ----------
    criteria : Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion
        The generation criteria to set properties for.
    active : bool
        Whether the criteria is active.
    action : SelectionActionType
        The action type for the criteria.
    entity_type : SelectionType
        The entity type for the criteria.
    criterion : SelectionCriterionType
        The criterion type for the criteria.
    operator : SelectionOperatorType
        The operator for the criteria.
    """
    if set_active_action_criteria:
        criteria.Active = active
        criteria.Action = action

    criteria.EntityType = entity_type
    criteria.Criterion = criterion
    criteria.Operator = operator
    criteria.Value = value

    return criteria


# %%
# Add named selections to the model

face1 = setup_named_selection("Face1")
add_generation_criteria(face1, Quantity("20 [m]"), criterion=SelectionCriterionType.LocationZ)
face1.Activate()
face1.Generate()

face2 = setup_named_selection("Face2")
add_generation_criteria(face2, Quantity("0 [m]"), criterion=SelectionCriterionType.LocationZ)
face2.Activate()
face2.Generate()

face3 = setup_named_selection("Face3")
add_generation_criteria(face3, Quantity("1 [m]"), criterion=SelectionCriterionType.LocationX)
add_generation_criteria(
    face3,
    Quantity("2 [m]"),
    criterion=SelectionCriterionType.LocationY,
    action=SelectionActionType.Filter,
)
add_generation_criteria(
    face3,
    Quantity("12 [m]"),
    criterion=SelectionCriterionType.LocationZ,
    action=SelectionActionType.Filter,
)
add_generation_criteria(face3, Quantity("4.5 [m]"), criterion=SelectionCriterionType.LocationZ)
add_generation_criteria(
    face3,
    Quantity("2 [m]"),
    criterion=SelectionCriterionType.LocationY,
    action=SelectionActionType.Filter,
)
face3.Activate()
face3.Generate()

body1 = setup_named_selection("Body1")
body1.GenerationCriteria.Add(None)
set_criteria_properties(
    body1.GenerationCriteria[0],
    Quantity("1 [m]"),
    set_active_action_criteria=False,
    criterion=SelectionCriterionType.LocationZ,
)
body1.GenerationCriteria.Add(None)
set_criteria_properties(
    body1.GenerationCriteria[1],
    Quantity("1 [m]"),
    set_active_action_criteria=False,
    criterion=SelectionCriterionType.LocationZ,
)
body1.Generate()

# %%
# Create construction geometry

# Add construction geometry to the model
construction_geometry = model.AddConstructionGeometry()
# Add a path to the construction geometry
construction_geom_path = construction_geometry.AddPath()

# Set the coordinate system for the construction geometry path
construction_geom_path.StartYCoordinate = Quantity(2, "m")
construction_geom_path.StartZCoordinate = Quantity(20, "m")
construction_geom_path.StartZCoordinate = Quantity(20, "m")
construction_geom_path.EndXCoordinate = Quantity(2, "m")

# Add a surface to the construction geometry
surface = construction_geometry.AddSurface()
# Set the coordinate system for the surface
surface.CoordinateSystem = lcs2
# Update the solids in the construction geometry
construction_geometry.UpdateAllSolids()

# %%
# Define the boundary condition and add results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to set the location and output for the temperature boundary condition


def set_loc_and_output(temp, location, values):
    """Add a temperature set output to the boundary condition.

    Parameters
    ----------
    temp : Ansys.Mechanical.DataModel.SteadyStateThermal.Temperature
        The temperature boundary condition.
    location : Ansys.Mechanical.DataModel.Geometry.GeometryObject
        The location of the temperature boundary condition.
    values : list[Quantity]
        The list of values for the temperature.
    """
    temp.Location = location
    temp.Magnitude.Output.DiscreteValues = [Quantity(value) for value in values]


# %%
# Create a function to set the inputs and outputs for the temperature boundary condition


def set_inputs_and_outputs(
    condition,
    input_quantities: list = ["0 [sec]", "1 [sec]", "2 [sec]"],
    output_quantities: list = ["22[C]", "30[C]", "40[C]"],
):
    """Set the temperature inputs for the boundary condition.

    Parameters
    ----------
    condition : Ansys.Mechanical.DataModel.SteadyStateThermal.Temperature
        The temperature boundary condition.
    inputs : list[Quantity]
        The list of input values for the temperature.
    """
    # Set the magnitude for temperature or the ambient temperature for radiation
    if "Temperature" in str(type(condition)):
        prop = condition.Magnitude
    elif "Radiation" in str(type(condition)):
        prop = condition.AmbientTemperature

    # Set the inputs and outputs for the temperature or radiation
    prop.Inputs[0].DiscreteValues = [Quantity(value) for value in input_quantities]
    prop.Output.DiscreteValues = [Quantity(value) for value in output_quantities]


# %%
# Add temperature boundary conditions to the steady state thermal analysis

temp = stat_therm.AddTemperature()
set_loc_and_output(temp, face1, ["22[C]", "30[C]"])
temp2 = stat_therm.AddTemperature()
set_loc_and_output(temp2, face2, ["22[C]", "60[C]"])

set_inputs_and_outputs(temp)
set_inputs_and_outputs(temp2, output_quantities=["22[C]", "50[C]", "80[C]"])

# %%
# Add radiation

# Add a radiation boundary condition to the steady state thermal analysis
radiation = stat_therm.AddRadiation()
radiation.Location = face3
set_inputs_and_outputs(radiation)
radiation.Correlation = RadiationType.SurfaceToSurface

# %%
# Set up the analysis settings

analysis_settings = stat_therm.AnalysisSettings
analysis_settings.NumberOfSteps = 2
analysis_settings.CalculateVolumeEnergy = True

# Activate the static thermal analysis and display the image
image_path = output_path / "bc_steady_state.png"
app.helpers.setup_view()
app.helpers.export_image(stat_therm, image_path)
app.helpers.display_image(image_path)

# %%
# Add results
# ~~~~~~~~~~~

# %%
# Add temperature results to the solution

# Get the solution object for the steady state thermal analysis
stat_therm_soln = model.Analyses[0].Solution

# Add four temperature results to the solution
temp_rst = stat_therm_soln.AddTemperature()
temp_rst.By = SetDriverStyle.MaximumOverTime

# Set the temperature location to the body1 named selection
temp_rst2 = stat_therm_soln.AddTemperature()
temp_rst2.Location = body1

# Set the temperature location to the construction geometry path
temp_rst3 = stat_therm_soln.AddTemperature()
temp_rst3.Location = construction_geom_path

# Set the temperaature location to the construction geometry surface
temp_rst4 = stat_therm_soln.AddTemperature()
temp_rst4.Location = surface

# %%
# Add the total and directional heat flux to the solution

total_heat_flux = stat_therm_soln.AddTotalHeatFlux()
directional_heat_flux = stat_therm_soln.AddTotalHeatFlux()

# Set the thermal result type and normal orientation for the directional heat flux
directional_heat_flux.ThermalResultType = TotalOrDirectional.Directional
directional_heat_flux.NormalOrientation = NormalOrientationType.ZAxis

# Set the coordinate system's primary axis for the directional heat flux
lcs2.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalZ
directional_heat_flux.CoordinateSystem = lcs2

# Set the display option for the directional heat flux
directional_heat_flux.DisplayOption = ResultAveragingType.Averaged

# %%
# Add thermal error and temperature probes

# Add a thermal error to the solution
thermal_error = stat_therm_soln.AddThermalError()

# Add a temperature probe to the solution
temp_probe = stat_therm_soln.AddTemperatureProbe()

# Set the temperature probe location to the face1 named selection
temp_probe.GeometryLocation = face1

# Set the temperature probe location method to the coordinate system
temp_probe.LocationMethod = LocationDefinitionMethod.CoordinateSystem
temp_probe.CoordinateSystemSelection = lcs2

# %%
# Add a heat flux probe

hflux_probe = stat_therm_soln.AddHeatFluxProbe()

# Set the location method for the heat flux probe
hflux_probe.LocationMethod = LocationDefinitionMethod.CoordinateSystem
# Set the coordinate system for the heat flux probe
hflux_probe.CoordinateSystemSelection = lcs2
# Set the result selection to the z-axis for the heat flux probe
hflux_probe.ResultSelection = ProbeDisplayFilter.ZAxis

# %%
# Add a reaction probe

# Update the analysis settings to allow output control nodal forces
analysis_settings.NodalForces = OutputControlsNodalForcesType.Yes

# Add a reaction probe to the solution
reaction_probe = stat_therm_soln.AddReactionProbe()
# Set the reaction probe geometry location to the face1 named selection
reaction_probe.LocationMethod = LocationDefinitionMethod.GeometrySelection
reaction_probe.GeometryLocation = face1

# %%
# Add a radiation probe

radiation_probe = stat_therm_soln.AddRadiationProbe()
# Set the radiation probe boundary condition to the radiation boundary condition
radiation_probe.BoundaryConditionSelection = radiation
# Display all results for the radiation probe
radiation_probe.ResultSelection = ProbeDisplayFilter.All

# %%
# Solve the solution
# ~~~~~~~~~~~~~~~~~~

# Solve the steady state thermal analysis solution
stat_therm_soln.Solve(True)

# sphinx_gallery_start_ignore
assert stat_therm_soln.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Show messages
# ~~~~~~~~~~~~~

# Print all messages from Mechanical
app.messages.show()

# %%
# Display the results
# ~~~~~~~~~~~~~~~~~~~

# Activate the total body temperature and display the image
image_path = output_path / "total_body_temp.png"
app.helpers.setup_view()
app.helpers.export_image(stat_therm, image_path)
app.helpers.display_image(image_path)

# %%
# Temperature on part of the body

# Activate the temperature on part of the body and display the image
image_path = output_path / "part_temp_body.png"
app.helpers.setup_view()
app.helpers.export_image(stat_therm, image_path)
app.helpers.display_image(image_path)

# %%
# Temperature distribution along the specific path

# Activate the temperature distribution along the specific path and display the image
image_path = output_path / "path_temp_distribution.png"
app.helpers.setup_view()
app.helpers.export_image(stat_therm, image_path)
app.helpers.display_image(image_path)

# %%
# Temperature of bottom surface

# Activate the temperature of the bottom surface and display the image
image_path = output_path / "bottom_surface_temp.png"
app.helpers.setup_view()
app.helpers.export_image(stat_therm, image_path)
app.helpers.display_image(image_path)

# %%
# Export the directional heat flux animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Export the directional heat flux animation as a GIF
directional_heat_flux_gif = output_path / "directional_heat_flux.gif"
app.helpers.export_animation(directional_heat_flux_gif)


# %%
# Display the heat flux animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Open the GIF file and create an animation
gif = Image.open(directional_heat_flux_gif)
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("off")
image = ax.imshow(gif.convert("RGBA"))


# Animation update function
def update_frame(frame):
    """Update the frame for the animation."""
    gif.seek(frame)
    image.set_array(gif.convert("RGBA"))
    return (image,)


# Create and display animation
ani = FuncAnimation(fig, update_frame, frames=gif.n_frames, interval=200, blit=True, repeat=True)

# Show the animation
plt.show()


# %%
# Display the output file from the solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the working directory for the steady state thermal analysis
solve_path = Path(stat_therm.WorkingDir)
# Get the path to the solve.out file
solve_out_path = solve_path / "solve.out"
# Print the output of the solve.out file if applicable
if solve_out_path:
    with solve_out_path.open("rt") as file:
        for line in file:
            print(line, end="")

# %%
# Print the project tree
# ~~~~~~~~~~~~~~~~~~~~~~

app.print_tree()

# %%
# Clean up the app and downloaded files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Save the project file
mechdat_path = output_path / "steady_state_thermal.mechdat"
app.save(str(mechdat_path))

# Close the app
app.close()

# Delete the example files
delete_downloads()
