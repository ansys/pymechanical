.. _geometry:

Geometry
==============

This section has helper scripts for  Geometry .

.. contents::
   :local:
   :depth: 4

Get all bodies
^^^^^^^^^^^^^^

.. code:: python

    body_objects = Model.Geometry.GetChildren(DataModelObjectCategory.Body, True)
    # or
    # bodies_objects = Model.Geometry.GetChildren(Ansys.ACT.Automation.Mechanical.Body, True)

    bodies = [body.GetGeoBody() for body in body_objects]  # GeoBodyWrapper
    # or
    # import itertools
    # nested_list = [ x.Bodies for x in ExtAPI.DataModel.GeoData.Assemblies[0].AllParts]
    # bodies = list(itertools.chain(*nested_list))


    bo = body_objects[0]  # Access Object Details and RMB options
    b = bodies[
        0
    ]  # Access Geometric Properties :  'Area', 'GeoData', 'Centroid' , 'Faces' etc


Find Body with Largest Volume
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

    body_names_volumes = []
    for body in body_objects:
        if body.Suppressed == 0 and body.Volume:
            body_names_volumes.append((body.Name, body.Volume, body.GetGeoBody().Id))

    sorted_name_vol = sorted(body_names_volumes)
    bodyname, volu, bodyid = sorted_name_vol.pop()
    print(f"Unit System is : {ExtAPI.Application.ActiveUnitSystem} ")
    print(f"Name of the Largest Body : '{bodyname}'")
    print(f"Its Volume : {round(volu.Value,2)} {volu.Unit} ")
    print(f"Its id : {bodyid} ")



Find Body by its ID
^^^^^^^^^^^^^^^^^^^
.. code:: python

    b2 = ExtAPI.DataModel.GeoData.GeoEntityById(bodyid)
    print(f"Body Name :  {b2.Name}, Body Id :  {b2.Id} ")


Find the Part that the body belongs to
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    # Get Body Name
    body_name = ExtAPI.DataModel.GeoData.GeoEntityById(363).Name
    # Get Part Name
    part_name = ExtAPI.DataModel.GeoData.GeoEntityById(363).Part.Name

    print(f"the Body named  '{body_name}'belongs to the part named   '{part_name}' ")



Find Body by its ID AND print its Faces, Centroid etc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    body2 = ExtAPI.DataModel.GeoData.GeoEntityById(bodyid)


    face_ids = [face.Id for face in body2.Faces]
    centroids_of_each_face = [
        ExtAPI.DataModel.GeoData.GeoEntityById(face_id).Centroid for face_id in face_ids
    ]
    for face_id, centroid in zip(face_ids, centroids_of_each_face):
        print(face_id, list(centroid))



Get all Vertices
^^^^^^^^^^^^^^^^
.. code:: python


    vertices = []
    geo = ExtAPI.DataModel.GeoData
    for asm in geo.Assemblies:
        for part in asm.Parts:
            for body in part.Bodies:
                for i in range(0, body.Vertices.Count):
                    vertices.append(body.Vertices[i].Id)

    print(vertices)


Get all edges of a given length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
    use_length = 75

    geo = ExtAPI.DataModel.GeoData

    edgelist = []

    for asm in geo.Assemblies:
        for part in asm.Parts:
            for body in part.Bodies:
                for edge in body.Edges:
                    if abs(edge.Length - use_length) <= use_length * 0.01:
                        edgelist.append(edge.Id)
    print(edgelist)


Get all circular edges of a given radius
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    radius = 10

    import math

    circumference = 2 * math.pi * radius


    geo = ExtAPI.DataModel.GeoData
    circlelist = []


    for asm in geo.Assemblies:
        for part in asm.Parts:
            for body in part.Bodies:
                for edge in body.Edges:
                    if (
                        abs(edge.Length - circumference) <= circumference * 0.01
                        and str(edge.CurveType) == "GeoCurveCircle"
                    ):
                        circlelist.append(edge.Id)
    print(circlelist)


Get Radius of a selected edge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python


    my_edge = ExtAPI.DataModel.GeoData.GeoEntityById(185)
    my_edge_radius = my_edge.Radius if str(my_edge.CurveType) == "GeoCurveCircle" else 0.0
    print(my_edge_radius)


Create a Named Selection from  a list of body Ids
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    mylist = [bodyid]

    selection_manager = ExtAPI.SelectionManager
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(
        SelectionTypeEnum.GeometryEntities
    )
    selection.Ids = mylist
    selection_manager.NewSelection(selection)

    ns2 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
    ns2.Name = "bodies2"
    ns2.Location = selection


Find a Named Selections with a prefix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python


    NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
        Ansys.ACT.Automation.Mechanical.NamedSelection
    ](True)
    my_nsel = [i for i in NSall if i.Name.startswith("b")][0]
    print(my_nsel.Name)


Create a Named Selection of all bodies with a cylindrical face
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    geo = ExtAPI.DataModel.GeoData
    cyl_body_ids = []

    for asm in geo.Assemblies:
        for part in asm.Parts:
            for body in part.Bodies:
                countcyl = 0
                for face in body.Faces:
                    if (
                        face.SurfaceType
                        == Ansys.ACT.Interfaces.Geometry.GeoSurfaceTypeEnum.GeoSurfaceCylinder
                    ):
                        countcyl = countcyl + 1
                if countcyl != 0:
                    cyl_body_ids.append(body.Id)


    selection_manager = ExtAPI.SelectionManager
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(
        SelectionTypeEnum.GeometryEntities
    )
    selection.Ids = cyl_body_ids

    model = ExtAPI.DataModel.Project.Model
    ns2 = model.AddNamedSelection()
    ns2.Name = "bodies_with_cyl_face"
    ns2.Location = selection
    selection_manager.ClearSelection()


Modify  material assignment
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    allbodies = ExtAPI.DataModel.Project.Model.GetChildren(
        DataModelObjectCategory.Body, True
    )
    for body in allbodies:
        body.Material = "Structural Steel"


Get  all Coordinate Systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    tree_CS = ExtAPI.DataModel.Project.Model.CoordinateSystems


Create a Coordinate System by Global Coordinates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    tree_CS = ExtAPI.DataModel.Project.Model.CoordinateSystems
    objCS = tree_CS.AddCoordinateSystem()  # Create new CS
    objCS.OriginX = Quantity("0.1 [m]")
    objCS.OriginY = Quantity("0.1 [m]")
    objCS.OriginZ = Quantity("0.1 [m]")


Create a Coordinate System Scoped to Named Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
        Ansys.ACT.Automation.Mechanical.NamedSelection
    ](True)
    a = [i for i in NSall if i.Name == "bodies2"][0]

    c = ExtAPI.DataModel.Project.Model.CoordinateSystems
    cc = c.AddCoordinateSystem()
    cc.OriginLocation = a


Create a Coordinate System by defining Directional Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    csys = tree_CS.AddCoordinateSystem()

    # set primary X axis to arbitrary (1,2,3) direction
    csys.PrimaryAxisDirection = Vector3D(1, 2, 3)

    # place csys origin
    csys.SetOriginLocation(Quantity(0, "in"), Quantity(0, "in"), Quantity(0, "in"))

    # force a graphics redraw to get proper annotation
    csys.Suppressed = True
    csys.Suppressed = False


Create Coordinate System at an Edge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    edgeID = 180

    treeCS = ExtAPI.DataModel.Project.Model.CoordinateSystems
    csys = treeCS.AddCoordinateSystem()  # Create a new Coordinate System
    sel = csys.OriginLocation
    sel.Ids = [edgeID]  # We're going to set it to this ID
    csys.OriginLocation = sel  # Scope the CS to the centroid of edgeID


Coordinate System Definition : More Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    objCS.PrimaryAxis = (
        CoordinateSystemAxisType.PositiveZAxis
    )  # Say we want the primary axis to be the z
    objCS.PrimaryAxisDefineBy = (
        CoordinateSystemAlignmentType.Associative
    )  # Say we want to align the primary axis with some geometry selection
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(
        SelectionTypeEnum.GeometryEntities
    )  # We're now going to make our edge the active selection
    selection.Ids = [edgeID]
    ExtAPI.SelectionManager.ClearSelection()  # Clear the active selection
    ExtAPI.SelectionManager.NewSelection(
        selection
    )  # Make the desired edge our active selection
    objCS.InternalObject.PrimaryAxisSelection = (
        ExtAPI.SelectionManager.InternalObject
    )  # Make the desired edge our active selection
    ExtAPI.SelectionManager.ClearSelection()  # Clear the active selection
    objCS.AddTransformation(
        TransformationType.Offset, CoordinateSystemAxisType.PositiveZAxis
    )  # Introduce a new transformation of this CS to an offset in the positive z
    moveDistance = 2.5  # Set some distance to move the CS along its own Z axis
    objCS.SetTransformationValue(
        objCS.TransformationCount, moveDistance
    )  # Set the value of the positive z offset


Coordinate Systems : Find Distance of a point from a local Coordinate System's  origin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python
    

    import math

    lcs = ExtAPI.DataModel.CoordinateSystems[1]  # Retrieve the local coordinate system
    point = (10.0, 11.0, 12.0)  # Define the point 3D coordinates
    distance = math.sqrt(
        math.pow((lcs.OriginX.Value - point[0]), 2)
        + math.pow((lcs.OriginY.Value - point[1]), 2)
        + math.pow((lcs.OriginZ.Value - point[2]), 2)
    )


Insert a Remote Point using a  Coordinate System , Scoping to a known face
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    faceId = 353
    sel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    sel.Ids = [faceId]


    newRP = ExtAPI.DataModel.Project.Model.RemotePoints.AddRemotePoint()
    newRP.Location = sel
    newRP.CoordinateSystem = objCS
    newRP.Behavior = LoadBehavior.Beam
    newRP.Radius = Quantity(11.0, "mm")



Insert a Point Mass
^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    geom = ExtAPI.DataModel.Project.Model.Geometry
    point_mass = geom.AddPointMass()
    my_selection = ExtAPI.SelectionManager.CreateSelectionInfo(
        SelectionTypeEnum.GeometryEntities
    )
    my_selection.Ids = [404]
    point_mass.Location = my_selection
    point_mass.Mass = Quantity("12 [kg]")
    point_mass.MassMomentOfInertiaX = Quantity("1.1 [kg m m]")
    point_mass.MassMomentOfInertiaY = Quantity("1.2 [kg m m]")
    point_mass.MassMomentOfInertiaZ = Quantity("1.3 [kg m m]")
    point_mass.Behavior = LoadBehavior.Coupled
    point_mass.PinballRegion = Quantity("0.2 [m]")


Find all Unsuppressed Point Masses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python
    


    AllObjects = ExtAPI.DataModel.Project.Model.GetChildren(
        DataModelObjectCategory.DataModelObject, True
    )
    all_pm = [
        i
        for i in AllObjects
        if i.GetType() == Ansys.ACT.Automation.Mechanical.PointMass
        and str(i.ObjectState) != "Suppressed"
    ]
