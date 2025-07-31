.. _loads:

Loads and BCs
==============

This section has helper scripts for  Loads and Boundary Conditions .

.. contents::
   :local:
   :depth: 4



Add an Analysis
^^^^^^^^^^^^^^

.. code:: python



    analysis = Model.AddStaticStructuralAnalysis()


Apply Bolt Pretension by Face Id
^^^^^^^^^^^^^^

.. code:: python

        

    analysis_settings = Model.Analyses[0].AnalysisSettings
    analysis_settings.NumberOfSteps = 6

    selection=ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [312]
    csys1=Model.CoordinateSystems.AddCoordinateSystem()
    csys1.OriginLocation= selection

    pretension = Model.Analyses[0].AddBoltPretension()
    pretension.Location=selection
    pretension.CoordinateSystem=csys1
    pretension.SetDefineBy(1 ,BoltLoadDefineBy.Load)
    pretension.Preload.Output.SetDiscreteValue(0 ,Quantity("1500[N]"))
    for i in range(2 ,analysis_settings.NumberOfSteps+1):
        pretension.SetDefineBy(int(i) ,BoltLoadDefineBy.Lock)


Apply a Fixed Support
^^^^^^^^^^^^^^

.. code:: python



    support = Model.Analyses[0].AddFixedSupport()
    support_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    support_scoping.Ids = [67]
    support.Location = support_scoping



Apply a pressure on the first face of the first body for the first part.
^^^^^^^^^^^^^^

.. code:: python




    pressure = Model.Analyses[0].AddPressure()
    part1 = Model.Geometry.Children[0]
    body1 = part1.Children[0]
    face1 = body1.GetGeoBody().Faces[0]  # Get the first face of the body.
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Entities = [face1]
    pressure.Location = selection
    pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]
    pressure.Magnitude.Output.DiscreteValues = [Quantity("10 [Pa]"), Quantity("20 [Pa]")]


Apply a pressure as a Formula
^^^^^^^^^^^^^^

.. code:: python



    pressure = Model.Analyses[0].AddPressure()
    pressure_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    pressure_scoping.Ids = [196]
    pressure.Location = pressure_scoping
    pressure.Magnitude.Output.Formula = '10*time' # as a Formula


Apply a Force
^^^^^^^^^^^^^^

.. code:: python




    force = Model.Analyses[0].AddForce()
    force_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    force_scoping.Ids = [31]
    force.Location = force_scoping
    force.Magnitude.Output.DiscreteValues=[Quantity('11.3 [N]'), Quantity('12.85 [N]')]



Apply Force by Components
^^^^^^^^^^^^^^

.. code:: python



    force = Model.Analyses[0].AddForce()
    force_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    force_scoping.Ids = [31]
    force.Location = force_scoping
    force.DefineBy = LoadDefineBy.Components
    force.ZComponent.Output.DiscreteValues = [Quantity('0 [N]'),Quantity('-9 [N]')]


Apply Nodal Forces by  Components
^^^^^^^^^^^^^^

.. code:: python



    nodes_list=[66,89,105,315,470]
    force_quantities_list= ['100 [N]','-200 [N]','300 [N]','-400 [N]','500 [N]']


    for i in range(0,len(nodes_list)):

        N1=ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.MeshNodes)
        N1.Ids = [nodes_list[i]]
        ExtAPI.SelectionManager.NewSelection(N1)

        NS = ExtAPI.DataModel.Project.Model.AddNamedSelection()
        NS.Name="Node_"+ str(nodes_list[i])

        Force1=ExtAPI.DataModel.Project.Model.Analyses[0].AddNodalForce()
        Force1.Location= NS
        Force1.Name="NodeAtNode_"+str(nodes_list[i])
        Force1.YComponent.Output.DiscreteValues=[Quantity(force_quantities_list[i])]
        Force1.DivideLoadByNodes = False


Apply Force and Fixed Support using  Named Selections
^^^^^^^^^^^^^^

.. code:: python



    selection_manager = ExtAPI.SelectionManager
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [312]

    model = ExtAPI.DataModel.Project.Model
    ns2 = model.AddNamedSelection()
    ns2.Name="fixed"
    ns2.Location = selection
    selection_manager.ClearSelection()

    selection_manager = ExtAPI.SelectionManager
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [312]

    model = ExtAPI.DataModel.Project.Model
    ns2 = model.AddNamedSelection()
    ns2.Name="force"
    ns2.Location = selection
    selection_manager.ClearSelection()


^^^^^^^^^^^^^^

.. code:: python



    NSall=Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    for_fixed_supp = [i for i in NSall if i.Name.startswith("fixed")][0]
    for_force = [i for i in NSall if i.Name.startswith("force")][0]

    model=ExtAPI.DataModel.Project.Model

    f = Model.Analyses[0].AddForce()
    f.Location = for_force
    f.Name='Force1'
    f.Magnitude.Output.DiscreteValues=[Quantity('10 [N]')]


    fs = model.Analyses[0].AddFixedSupport()
    fs.Location = for_fixed_supp
    fs.Name='FixedSupport1'


Apply Radiation - Thermal Analysis
^^^^^^^^^^^^^^

.. code:: python



    radn= Model.Analyses[1].AddRadiation()

    e=radn.Emissivity
    e.Output.DiscreteValues=[Quantity ("0.36")]

    t=radn.AmbientTemperature
    t.Inputs[0].DiscreteValues=[Quantity ("0 [sec]"), Quantity ("1 [sec]")]
    t.Output.DiscreteValues=[Quantity ("22 [C]"),Quantity("2302 [C]")]


Apply Tabular Pressure for ,say, 5 Load Steps
^^^^^^^^^^^^^^

.. code:: python



    pressureLoad=ExtAPI.DataModel.Project.Model.Analyses[0].AddPressure()
    pressureLoad.Magnitude.Inputs[0].DiscreteValues = [Quantity('0 [sec]'), Quantity('1 [sec]'), Quantity('2 [sec]'), Quantity('3 [sec]'), Quantity('4 [sec]'), Quantity('5 [sec]')]
    pressureLoad.Magnitude.Output.DiscreteValues = [Quantity('0 [MPa]'),Quantity('10 [MPa]'),Quantity('30 [MPa]'),Quantity('25 [MPa]'),Quantity('-30 [MPa]'),Quantity('100 [MPa]')]


Applying Direct FE Type Boundary Conditions ( Nodal Pressure , Force and Displacement)
^^^^^^^^^^^^^^

.. code:: python



    CSall=ExtAPI.DataModel.Project.Model.CoordinateSystems.GetChildren[Ansys.ACT.Automation.Mechanical.CoordinateSystem](True)
    a = [i for i in CSall if i.Name == "cyl"][0]
    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    n = [i for i in NSall if i.Name == "ns"][0]


    nf=ExtAPI.DataModel.Project.Model.Analyses[0].AddNodalForce()
    nf.Location=n
    nf.YComponent.Inputs[0].DiscreteValues=[Quantity ("0 [sec]"), Quantity ("1 [sec]")]
    nf.IndependentVariable=LoadVariableVariationType.YValue
    nf.XYZFunctionCoordinateSystem=a
    nf.YComponent.Output.DiscreteValues=[Quantity ("0 [N]"),Quantity("100[N]")]


    nd=ExtAPI.DataModel.Project.Model.Analyses[0].AddNodalDisplacement()
    nd.Location=n
    nd.YComponent.Inputs[0].DiscreteValues=[Quantity ("0 [sec]"), Quantity ("1 [sec]")]
    nd.IndependentVariable=LoadVariableVariationType.YValue
    nd.XYZFunctionCoordinateSystem=a
    nd.YComponent.Output.DiscreteValues=[Quantity ("0 [mm]"),Quantity("100[mm]")]


    np=ExtAPI.DataModel.Project.Model.Analyses[0].AddNodalPressure()
    np.Location=n
    np.Magnitude.Inputs[0].DiscreteValues=[Quantity ("0 [sec]"), Quantity ("1 [sec]")]
    np.IndependentVariable=LoadVariableVariationType.YValue
    np.XYZFunctionCoordinateSystem=a
    np.Magnitude.Output.DiscreteValues=[Quantity ("0 [Pa]"),Quantity("100[Pa]")]


