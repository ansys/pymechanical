.. _namedselections:

Named Selections
================

This section has helper scripts for  Named Selections .

.. contents::
   :local:
   :depth: 4




Fetch all Named Selections
^^^^^^^^^^^^^^

.. code:: python

    # ALL NAMED SELECTIONS
    nsall=ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelections.NamedSelection)


Delete a named selection
^^^^^^^^^^^^^^

.. code:: python

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    #myNS = [i for i in NSall if i.Name[:2] == "aa"]
    a = [i for i in NSall if i.Name == "S1"][0]
    a.Delete()

    b=ExtAPI.DataModel.Tree.GetObjectsByName("S1")[0]
    b.Delete()


Create a named selection
^^^^^^^^^^^^^^

.. code:: python

    selection_manager = ExtAPI.SelectionManager
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [1,2,3,4]

    model = ExtAPI.DataModel.Project.Model
    ns2 = model.AddNamedSelection()
    ns2.Name="faces"
    ns2.Location = selection
    selection_manager.ClearSelection()


Create a Named Selection by Worksheet
^^^^^^^^^^^^^^

.. code:: python

    NS1 = DataModel.Project.Model.AddNamedSelection()
    NS1.ScopingMethod = GeometryDefineByType.Worksheet
    GenerationCriteria = NS1.GenerationCriteria

    Criterion1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
    Criterion1.Action = SelectionActionType.Add
    Criterion1.EntityType = SelectionType.GeoFace
    Criterion1.Criterion = SelectionCriterionType.LocationY
    Criterion1.Operator = SelectionOperatorType.Equal
    Criterion1.Value = Quantity("0 [m]")
    GenerationCriteria.Add(Criterion1)

    Criterion2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
    Criterion2.Action = SelectionActionType.Add
    Criterion2.EntityType = SelectionType.GeoFace
    Criterion2.Criterion = SelectionCriterionType.LocationZ
    Criterion2.Operator = SelectionOperatorType.Equal
    Criterion2.Value = Quantity("0 [m]")
    GenerationCriteria.Add(Criterion2)

    NS1.Generate()


Find a Named Selection

^^^^^^^^^^^^^^

.. code:: python

    # using entities


    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    a = [i for i in NSall if i.Name == "bodies2"][0]
    # Ansys.ACT.Automation.Mechanical.NamedSelection


    a.Entities
    # [Ansys.ACT.Common.Geometry.GeoBodyWrapper]




Identify Named Selections based on Name and Type
^^^^^^^^^^^^^^

.. code:: python

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)

    a = ["fix","bushing","roller"]
    ns1 = [i for i in NSall if  a[0] in i.Name ]
    ns2 = [i for i in NSall if  a[1] in i.Name ]
    ns3 = [i for i in NSall if  a[2] in i.Name ]
    filtered =ns1 + ns2 + ns3

    VertexNsels = [i for i in filtered if  str(ExtAPI.DataModel.GeoData.GeoEntityById(i.Ids[0]).Type) == 'GeoVertex' ]