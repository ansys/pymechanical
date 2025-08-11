.. _ref_mechanical_scripting_guide_script_helpers:

Script helpers
==============

This section provides a collection of scripting helpers for Ansys Mechanical. Click the links to see relevant examples in the *Mechanical Scripting Guide*.

.. important::

   The links do not only contain what is described in the bullet points but also additional information.
   For examples of what is being described in the bullet points, refer to the code sections in the
   linked content.


General setup
-------------

- :ansyshelp:`Set up the display unit system <act_script_demo_rbd_contact.html>`
- :ansyshelp:`Log an error message <act_script_examples_suppress_duplicate_contacts.html>`

Tree and object management
--------------------------

- :ansyshelp:`Find a tree object by name using AllObjects <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Find a tree object by name using GetObjectsbyName <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Get objects whose name contains the specified string <act_script_examples_select_by_name.html>`
- :ansyshelp:`Select objects by name <act_script_examples_select_by_name.html>`
- :ansyshelp:`Get all visible properties for a tree object <mech_script_GetVisiblePropertiesForTreeObject.html>`
- :ansyshelp:`Parametrize a property for a tree object <mech_script_ParameterizePropertyForTreeObject.html>`
- :ansyshelp:`Delete an object <act_script_examples_tree_delete_object.html>`
- :ansyshelp:`Refresh and pause a tree <act_script_examples_tree_refresh.html>`

Geometry
--------

- :ansyshelp:`Get all parts <act_script_demo_Cyclic.html>`
- :ansyshelp:`Get the first body whose name contains the specified number <act_script_examples_select_by_name.html>`
- :ansyshelp:`Find a body by name <act_script_demo_Cyclic.html>`
- :ansyshelp:`Select geometry by IDs <act_script_examples_select_geom_or_mesh.html>`
- :ansyshelp:`Given a GeoData body ID, get the tree object of the body <act_script_examples_get_tree_obj.html>`
- :ansyshelp:`Given a tree object of a body, get the GeoData body <act_script_examples_get_GeoData.html>`
- :ansyshelp:`Suppress a body <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Get the volume, area, and length in CAD units <act_script_examples_calc_sum.html>`

--------------------------

- :ansyshelp:`Set the stiffness behavior of bodies as rigid <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Set the stiffness behavior of bodies as flexible <act_script_demo_rbd_flexible.html>`
- :ansyshelp:`Set the integration scheme for bodies (element control) <act_script_demo_random_vib.html>`
- :ansyshelp:`Set the 2D behaviour as plane stress <act_script_demo_transient_therm.html>`
- :ansyshelp:`Set the geometry thickness of a surface body <act_script_demo_transient_therm.html>`

------------------------

- :ansyshelp:`Add a remote point <act_script_demo_static_struct.html>`
- :ansyshelp:`Add a deformable remote point <act_script_demo_random_vib.html>`
- :ansyshelp:`Create a construction surface <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Update the geometries for all construction lines <act_script_examples_update_construct_line.html>`
- :ansyshelp:`Create construction lines from cylindrical faces <act_script_examples_create_construct_line.html>`
- :ansyshelp:`Get all point masses imported from the external model <act_script_demo_External_Model.html>`

------------------------

- :ansyshelp:`Assign materials to bodies <act_script_demo_transient_therm.html>`
- :ansyshelp:`Create material assignment from body materials <act_script_examples_create_mat_assign.html>`
- :ansyshelp:`Find material using Name(GetChildren) <act_script_demo_random_vib.html>`


Coordinate system
-----------------

- :ansyshelp:`Add a cylindrical coordinate system <act_script_demo_Cyclic.html>`
- :ansyshelp:`Add a coordinate system for applying symmetric symmetry <act_script_demo_Symmetric.html>`
- :ansyshelp:`Create aligned coordinate systems in a motor <act_script_examples_create_aligned_coordinate_systems_in_motor.html>`
- :ansyshelp:`Set arbitrary coordinate system properties <act_script_examples_arbitrary_cs.html>`
- :ansyshelp:`Transform coordinate systems with Math <act_script_examples_coordinate_system_math.html>`
- :ansyshelp:`Find a coordinate system using Name(GetChildren) <act_script_demo_random_vib.html>`

Connections
-----------

- :ansyshelp:`Add a contact region <act_script_demo_rbd_contact.html>`
- :ansyshelp:`Add frictionless contact <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add frictional contact <act_script_demo_coupled_field_001.html>`

------------------------

- :ansyshelp:`Add a fixed joint <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Add a cylindrical joint <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Add a revolute joint <act_script_demo_rbd_flexible.html>`
- :ansyshelp:`Add a general joint as translational <act_script_demo_general_joint.html>`
- :ansyshelp:`Add general joint with 6 DOF <act_script_demo_rbd_flexible.html>`
- :ansyshelp:`Add a joint based on proximity of two named selections <act_script_examples_add_joint_based_two_named_selections.html>`

------------------------

- :ansyshelp:`Verify the size and flip contact and target <act_script_examples_verify_contact_size.html>`
- :ansyshelp:`Set the contact formulation <act_script_demo_post1.html>`
- :ansyshelp:`Set a pinball radius to 5mm for all frictionless contacts <act_script_examples_set_pinball.html>`
- :ansyshelp:`Set the interface treatment for a contact <act_script_demo_trans_struct.html>`
- :ansyshelp:`Create a named selection from the scoping of a contact <act_script_examples_create_named_selection.html>`
- :ansyshelp:`Count the number of contacts <act_script_examples_count_contacts.html>`
- :ansyshelp:`Suppress duplicate contacts <act_script_examples_suppress_duplicate_contacts.html>`

Symmetry
--------

- :ansyshelp:`Add a cyclic region <act_script_demo_Cyclic.html>`
- :ansyshelp:`Add symmetric symmetry <act_script_demo_Symmetric.html>`
- :ansyshelp:`Add a pre-meshed cyclic region <act_script_demo_Cyclic.html>`

Named selection
---------------

- :ansyshelp:`Create a named selection using a worksheet <act_script_examples_create_named_selection_faces.html>`
- :ansyshelp:`Create a named selection using Worksheet 2 <act_script_demo_trans_struct.html>`
- :ansyshelp:`Get a named selection using Name(GetObjectsByName) <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Get a named selection using Name(GetChildren) <act_script_demo_random_vib.html>`
- :ansyshelp:`Get named selections whose name contains the specified string <act_script_examples_select_by_name.html>`
- :ansyshelp:`Get the first named selection whose name contains the specified string <act_script_examples_select_by_name.html>`
- :ansyshelp:`Rename a named selection based on scoping <act_script_examples_rename_named_sel.html>`
- :ansyshelp:`Suppress bodies contained in a given named selection <act_script_examples_suppress_bodies.html>`
- :ansyshelp:`Scope a boundary condition to a named selection <act_script_examples_scope_BC.html>`

------------------------

- :ansyshelp:`Add a joint based on proximity of two named selections <act_script_examples_add_joint_based_two_named_selections.html>`
- :ansyshelp:`Create a named selection from the scoping of a contact <act_script_examples_create_named_selection.html>`
- :ansyshelp:`Add face meshing to a named selection <act_script_demo_Linear_Periodic.html>`
- :ansyshelp:`Use a named selection for pressure <act_script_demo_Symmetric.html>`
- :ansyshelp:`Apply spatially varying pressure on a named selection <act_script_demo_varying_load.html>`
- :ansyshelp:`Use a named selection for a fixed support <act_script_demo_Symmetric.html>`

Mesh
----

- :ansyshelp:`Set the global mesh size <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Set the element order <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Set the mesh physics preference <act_script_demo_rbd_contact.html>`
- :ansyshelp:`Add mesh sizing (number of divisions) <act_script_demo_Linear_Periodic.html>`
- :ansyshelp:`Set the mesh sizing behavior as hard <act_script_demo_coupled_field_transient.html>`
- :ansyshelp:`Set the mesh sizing behavior as free <act_script_demo_Linear_Periodic.html>`
- :ansyshelp:`Add the mesh refinement <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add face meshing to a named selection <act_script_demo_Linear_Periodic.html>`
- :ansyshelp:`Add match control <act_script_demo_Cyclic.html>`

------------------------

- :ansyshelp:`Add a sweep method <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Add a hex dominant method <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Add a quad dominant method <act_script_demo_transient_therm.html>`
- :ansyshelp:`Select nodes by IDs <act_script_examples_select_geom_or_mesh.html>`
- :ansyshelp:`Given a node ID, get the node's information <act_script_examples_query_mesh.html>`
- :ansyshelp:`Create a selection based on the location of nodes in Y <act_script_examples_create_selection_based_on_Location_of_nodes_in_Y.html>`
- :ansyshelp:`Add a node merge group <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Create a node merge object at a symmetry plane <act_script_examples_create_node_merage_object.html>`

------------------------

- :ansyshelp:`Suppress or un-suppress meshing objects <act_script_demo_Cyclic.html>`
- :ansyshelp:`Mesh a model multiple times and track its metrics <act_script_examples_remesh_model.html>`
- :ansyshelp:`Clear the mesh <act_script_examples_clear_mesh.html>`

Loads and boundary conditions
-----------------------------

- :ansyshelp:`Create a pressure load <act_script_examples_create_pressure_load.html>`
- :ansyshelp:`Use a named selection for a pressure <act_script_demo_Symmetric.html>`
- :ansyshelp:`Apply spatially varying pressure on a named selection <act_script_demo_varying_load.html>`
- :ansyshelp:`Change the tabular data values of loading condition <act_script_examples_change_tabular_data.html>`
- :ansyshelp:`Use a named selection as scoping of a load or support <act_script_examples_NamedSelection_as_Scoping.html>`
- :ansyshelp:`Add a remote force <act_script_demo_static_struct.html>`
- :ansyshelp:`Add a thermal condition <act_script_demo_static_struct.html>`
- :ansyshelp:`Add imported body temperature <act_script_demo_Cyclic.html>`

------------------------

- :ansyshelp:`Add compression-only support <act_script_demo_trans_struct.html>`
- :ansyshelp:`Use a named selection for a fixed support <act_script_demo_Symmetric.html>`
- :ansyshelp:`Add a fixed or frictionless support <act_script_demo_static_struct.html>`
- :ansyshelp:`Add displacement BC <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add displacement BC 2 <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add remote displacement <act_script_demo_coupled_field_001.html>`

------------------------

- :ansyshelp:`Add a bearing load <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add Earth gravity <act_script_demo_rbd_contact.html>`
- :ansyshelp:`Add a command snippet <act_script_demo_coupled_field_transient.html>`
- :ansyshelp:`Add PSD Acceleration  <act_script_demo_random_vib.html>`

------------------------

- :ansyshelp:`Add convection <act_script_examples_convection.html>`
- :ansyshelp:`Add internal heat generation <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Add radiation <act_script_demo_thermal_electric.html>`
- :ansyshelp:`Add initial temperature - thermal transient <act_script_demo_transient_therm.html>`
- :ansyshelp:`Add heat flux - thermal <act_script_demo_transient_therm.html>`
- :ansyshelp:`Add convection 2 <act_script_demo_steady_state_therm.html>`

------------------------

- :ansyshelp:`Add a physics region - Acoustic <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add an acoustic mass source <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add acoustic pressure <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add a fluid solid interface <act_script_demo_modal_acoustic.html>`

------------------------

- :ansyshelp:`Add a coupled field static physics region <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Add an electric voltage <act_script_demo_electric.html>`
- :ansyshelp:`Add an electric current <act_script_demo_electric.html>`
- :ansyshelp:`Add an electric thermal condition <act_script_demo_electric.html>`
- :ansyshelp:`Add voltage coupling <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add voltage ground <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add voltage <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add plastic heating <act_script_demo_coupled_field_transient.html>`

Solution setup
--------------

- :ansyshelp:`Set transient analysis settings containing multiple steps <act_script_demo_trans_struct.html>`
- :ansyshelp:`Set modal analysis settings <act_script_demo_coupled_field_modal.html>`
- :ansyshelp:`Set random vibration analysis settings <act_script_demo_random_vib.html>`
- :ansyshelp:`Set modal acoustic analysis settings <act_script_demo_modal_acoustic.html>`
- :ansyshelp:`Set harmonic acoustic analysis settings <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Set transient thermal analysis settings <act_script_demo_transient_therm.html>`
- :ansyshelp:`Set steady state thermal analysis settings <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Set RBD analysis settings <act_script_demo_rbd_flexible.html>`
- :ansyshelp:`Set electric analysis settings <act_script_demo_electric.html>`

------------------------

- :ansyshelp:`Set the harmonic range maximum and solution intervals <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Set the modal max modes to find and search the range <act_script_demo_coupled_field_modal.html>`

------------------------

- :ansyshelp:`Set convergence settings <act_script_demo_coupled_field_transient.html>`
- :ansyshelp:`Set sub-steps <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Set the step end time <act_script_demo_Cyclic.html>`
- :ansyshelp:`Set automatic time stepping <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Set the solver type <act_script_demo_coupled_field_modal.html>`
- :ansyshelp:`Perform a solution while specifying the solution handler and the number of cores <act_script_examples_solve_track_core.html>`
- :ansyshelp:`Solve <act_script_demo_static_struct.html>`

Result postprocessing
---------------------

- :ansyshelp:`Add directional deformation <act_script_demo_general_joint.html>`
- :ansyshelp:`Add directional deformation (scope to named selection) <act_script_demo_static_struct.html>`
- :ansyshelp:`Get the maximum or minimum value of a result <act_script_demo_static_struct.html>`
- :ansyshelp:`Add equivalent stress <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add normal stress <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Add thermal strain <act_script_demo_coupled_field_001.html>`
- :ansyshelp:`Add middle principal elastic strain <act_script_demo_rbd_flexible.html>`
- :ansyshelp:`Add equivalent plastic strain <act_script_demo_coupled_field_transient.html>`
- :ansyshelp:`Add normal elastic strain <act_script_demo_random_vib.html>`
- :ansyshelp:`Add a stress tool <act_script_demo_trans_struct.html>`
- :ansyshelp:`Add a user-defined result <act_script_demo_post2.html>`

------------------------

- :ansyshelp:`Add a contact force reaction <act_script_demo_rbd_contact.html>`
- :ansyshelp:`Add a force reaction probe scoped to BC <act_script_demo_static_struct.html>`
- :ansyshelp:`Evaluate spring reaction forces <act_script_examples_evaluate_spring_reaction_forces.html>`
- :ansyshelp:`Add a force reaction probe scoped to BC 2 <act_script_demo_Linear_Periodic.html>`
- :ansyshelp:`Add a joint probe <act_script_demo_general_joint.html>`
- :ansyshelp:`Get a joint probe's relative deformation, velocity, acceleration, rotation, angular velocity, and angular acceleration <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Get the movement and force of a joint probe <act_script_demo_cylindrical_joint.html>`
- :ansyshelp:`Add an energy probe (RBD) <act_script_demo_rbd_contact.html>`

------------------------

- :ansyshelp:`Get modal natural frequencies <act_script_demo_random_vib.html>`
- :ansyshelp:`Add the deformation frequency response <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add the voltage frequency response <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add the charge reaction frequency response <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add the impedance frequency response <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Get the maximum value from a frequency response <act_script_demo_coupled_field_harmonic.html>`
- :ansyshelp:`Add PSD results - Directional Deformation, Velocity, Acceleration <act_script_demo_random_vib.html>`
- :ansyshelp:`Add response PSD <act_script_demo_random_vib.html>`
- :ansyshelp:`Add response PSD tool <act_script_demo_random_vib.html>`

------------------------

- :ansyshelp:`Add a radiation probe <act_script_demo_thermal_electric.html>`
- :ansyshelp:`Add a temperature result <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Add a total heat flux result <act_script_demo_steady_state_therm.html>`
- :ansyshelp:`Add a convection BC reaction probe <act_script_demo_steady_state_therm.html>`

------------------------

- :ansyshelp:`Add an acoustic pressure result <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add an acoustic SPL result <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add an acoustic far field SPL result <act_script_demo_harmonic_acoustic.html>`
- :ansyshelp:`Add an acoustic far field weighted SPL result <act_script_demo_harmonic_acoustic.html>`

------------------------

- :ansyshelp:`Add an electric directional e-field intensity <act_script_demo_electric.html>`
- :ansyshelp:`Add an electric directional current density <act_script_demo_electric.html>`
- :ansyshelp:`Add an electric directional EMAG reaction force <act_script_demo_electric.html>`
- :ansyshelp:`Add an electric voltage result <act_script_demo_electric.html>`
- :ansyshelp:`Add electric joule heat <act_script_demo_electric.html>`

------------------------

- :ansyshelp:`Clear generated data <act_script_demo_post1.html>`
- :ansyshelp:`Evaluate all results <act_script_demo_post2.html>`
- :ansyshelp:`Duplicate a harmonic result object <act_script_examples_duplicate_result_object.html>`
- :ansyshelp:`Scan results, suppress results with invalid display times, and evaluate the results <act_script_examples_scan_results.html>`
- :ansyshelp:`Rename results based on definition <act_script_demo_post2.html>`
- :ansyshelp:`Modify display options for inserted results <act_script_demo_post2.html>`
- :ansyshelp:`Modify display options for user-defined results <act_script_demo_post2.html>`
- :ansyshelp:`Add a figure <act_script_demo_post2.html>`
- :ansyshelp:`Work with solution combinations <act_script_examples_solution_combinations.html>`
- :ansyshelp:`Retrieve stress results <act_script_examples_retreive_stress_resutls.html>`
- :ansyshelp:`Tag and group result objects based on scoping and load steps <act_script_examples_result_objecdts_tag_and_group.html>`
- :ansyshelp:`Use an existing graphics selection on a result object <act_script_examples_use_graphics_selection.html>`
- :ansyshelp:`Rescope a solved result based on the active node or element selection <act_script_examples_rescope.html>`
- :ansyshelp:`Create probe principal stresses from a node selection <act_script_examples_probe_principal.html>`
- :ansyshelp:`Find hot spots <act_script_examples_hot_spot.html>`
- :ansyshelp:`Work with line charts <act_script_examples_line_chart.html>`
- :ansyshelp:`Access contour results for an evaluated result <act_script_examples_access_contour_results_for_evaluated_result.html>`
- :ansyshelp:`Access contour results at individual nodes or elements <act_script_examples_access_contour_results_at_indiv_nodes_elements.html>`

Export and visualization
------------------------

- :ansyshelp:`Set graphics settings <act_script_demo_post1.html>`
- :ansyshelp:`Set the legend direction, ruler, and triad <act_script_demo_post1.html>`
- :ansyshelp:`Change legend bands <act_script_demo_post1.html>`
- :ansyshelp:`Add a section plane <act_script_demo_post1.html>`
- :ansyshelp:`Set the view orientation <act_script_demo_post1.html>`
- :ansyshelp:`Modify export settings <act_script_examples_modfiy_export_settings.html>`

------------------------

- :ansyshelp:`Export figures <act_script_examples_export_figures.html>`
- :ansyshelp:`Export result images to files <act_script_examples_export_result_images.html>`

------------------------

- :ansyshelp:`Search for a keyword and export <act_script_examples_seach_keyword.html>`
- :ansyshelp:`Export all result animations <act_script_examples_export_result_animations.html>`
- :ansyshelp:`Export a result object to an STL file <act_script_examples_export_result_object.html>`
- :ansyshelp:`Write contour results to a text file <act_script_examples_write_contour_results_onto_file.html>`
