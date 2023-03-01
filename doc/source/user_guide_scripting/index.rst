.. _ref_user_guide_scripting:

==========================
Mechanical scripting guide
==========================
This section provides an overview of Mechanical scripting.


..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   threading


Overview
========
You could already perform scripting of Mechanical with Python from inside
Mechanical. pyMechanical leverages the same APIs but allow you to run your
automations from outside Mechanical.

Refer to the **Scripting in Mechanical Guide** in the Mechanical documentation at
`ANSYS Help <https://ansyshelp.ansys.com/Views/Secured/corp/v231/en/act_script/act_script.html>`_.
for complete information about these APIs.

Recording
^^^^^^^^^
Mechanical supports some level of recording, which prints APIs that many actions in the User
Interface run. Examples of these actions are assigning selections to scoping, changing values in
the details view, and renaming an object in the **Outline**. For the animated example shown here,
a **Fixed Support** and a **Pressure** were added to the **Outline**.

.. figure:: ../images/gmech_scripting_recording.jpg

Mechanical entities
^^^^^^^^^^^^^^^^^^
Mechanical has an extensive set of entities that represent all the functionality provided
by Mechanical. At it's core, it contains:

* CAD - Usually imported from a **CAD** application
* Mesh - The discretized geometry that is appropriate for Mechanical's solvers
* Materials - Engineering material models that come from **Engineering Data**
* Objects - The entities in the **Outline** that represent the model, analyses, solutions, and results
* Graphics - The 3D graphics engine that renders data from Mechanical visually and allows exporting images and animations
* Solvers - The solver integrations that allow a Mechanical model to be used to run a specific solver
* Post - The engine which computes useful engineering results from solver runs
* Extensions - Mechanical can be extended by plugins or extensions that are defined externally from Mechanical

There is some overlap between these entities. For instance, the **CAD** data is represented visually in the 3D Graphics
but also has representation in the **Outline**. The raw CAD data, which includes the tessellations used to render the
graphics, as well as all the data needed to define vertices, edges, faces, volumes, and parts is considered **GeoData**.
You may interact with these bodies and parts in the **Outline**, assigning materials, thickness, and other data that does
not come from CAD. This is considered **Geometry**. As a result, the API entry point for **GeoData** and **Geometry** are
different. The same is true for **Mesh**, there is a representation in the **Outline** which contains the settings used to
generate the mesh as well as statistics about the mesh, and then there is **MeshData** which is the actual nodes and
elements in the mesh. These have distinct API entry points.

Executing a sequence of APIs can sometimes be slow, as Mechanical may perform background tasks each time any of its entities
are created, updated, or deleted. Mechanical scripting has a mechanism to defer many of these tasks until after a block of
commands are run, using the **Transaction** class. For example:

.. code:: python

    with Transaction():
        for obj in Tree:
            obj.Name = obj.Name + " suffix"

API entry points
^^^^^^^^^^^^^^^^
When running scripts inside of Mechanical, you can access the APIs via the following entry points:

* ExtAPI: Entry point for all APIs
* DataModel: Entry point to access CAD, Mesh, and objects from the **Outline**
* Model: The **Model** object from the **Outline**
* Tree: The **Outline**
* Graphics: The 3D graphics engine

You also would have access to several types and namespaces that are included in the scripting scope, but are not available
from those entry points.

Additional resources
^^^^^^^^^^^^^^^^^^^^
The **ACT API Reference Guide** provides all available descriptions on objects, methods, and properties.
