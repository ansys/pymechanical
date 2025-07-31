.. _mesh:

Mesh
==============

This section has helper scripts for  Mesh.

.. contents::
   :local:
   :depth: 4



Insert a Local Meshing Control for a Named Selection
^^^^^^^^^^^^^^

.. code:: python


    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    use_nsel = [i for i in NSall if i.Name == "body5"][0]

    ms=ExtAPI.DataModel.Project.Model.Mesh.AddAutomaticMethod()
    ms.Location=use_nsel
    ms.Method=ms.Method.AllTriAllTet
    ms.Algorithm=ms.Algorithm.PatchConforming


Insert a Sweep Method (Scoping Method : Named Selection)
^^^^^^^^^^^^^^

.. code:: python

    

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    use_nsel = [i for i in NSall if i.Name == "for_sweep"][0]

    mesh=ExtAPI.DataModel.Project.Model.Mesh
    mesh_method = mesh.AddAutomaticMethod()
    # mesh_method.ScopingMethod = GeometryDefineByType.NamedSelections
    mesh_method.Location=use_nsel
    mesh_method.Method=MethodType.Sweep


Insert a Mesh Sizing Control ( Scoping Method : Geometry Selection)
^^^^^^^^^^^^^^

.. code:: python

    


    body_ids=[312,363]
    sel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    sel.Ids = body_ids 

    mesh = ExtAPI.DataModel.Project.Model.Mesh
    mesh_sizing = mesh.AddSizing()
    #mesh_sizing.ScopingMethod = GeometryDefineByType.Geometry
    mesh_sizing.Location = sel
    mesh_sizing.Behavior=SizingBehavior.Hard


Generate Mesh
^^^^^^^^^^^^^^

.. code:: python

    

    Model.Mesh.GenerateMesh()


Get Element Count of a meshed body
^^^^^^^^^^^^^^

.. code:: python

    

    meshdata = ExtAPI.DataModel.MeshDataByName("Global")

    geoBody = ExtAPI.DataModel.GeoData.GeoEntityById(312)
    body = ExtAPI.DataModel.Project.Model.Geometry.GetBody(geoBody)
    meshregion = meshdata.MeshRegionById(geoBody.Id)
    print(body.Name , meshregion.ElementCount)



