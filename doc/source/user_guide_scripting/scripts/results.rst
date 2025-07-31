.. _results:

Results
==============

This section has helper Scripts for results.


.. contents::
   :local:
   :depth: 4


Results that are accessible for Getresult
^^^^^^^^^^^^^^

.. code:: python


    ExtAPI.DataModel.AnalysisList[0].GetResultsData().ResultNames

Access max and min of a result
^^^^^^^^^^^^^^

.. code:: python


    minimum_deformation = total_deformation.Minimum
    maximum_deformation = total_deformation.Maximum


Get Results by Node Number
^^^^^^^^^^^^^^

.. code:: python

    

    ExtAPI.DataModel.AnalysisList[0].GetResultsData().GetResult("U").GetNodeValues(2000)


Access other results 
^^^^^^^^^^^^^^

.. code:: python

        


    #FATIGUE TOOL 
    fatigue_tool= ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result.FatigueTool)[0]
    print(a.Children[0].Minimum)

    # insert a command object 
    cs = ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddCommandSnippet()




Fatigue Results 
^^^^^^^^^^^^^^

.. code:: python

        

    analysis = ExtAPI.DataModel.Project.Model.Analyses[0]
    solution = analysis.Solution
    fatigue_tool = solution.AddFatigueTool()

    safety_factor = fatigue_tool.AddSafetyFactor()
    location = safety_factor.Location
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.MeshNodes)
    selection.Ids = [1,2]
    safety_factor.Location = selection
    minimum = safety_factor.Minimum


    safety_factor.ExportToTextFile(True,fname)


User defined Result
^^^^^^^^^^^^^^

.. code:: python

    

    R1=ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddUserDefinedResult();


Get number of result sets
^^^^^^^^^^^^^^

.. code:: python

    

    reader = ExtAPI.DataModel.AnalysisList[0].GetResultsData()
    reader.ListTimeFreq.Count


User Defined Result
^^^^^^^^^^^^^^

.. code:: python

        

    reader = ExtAPI.DataModel.AnalysisList[0].GetResultsData()
    steptimes=reader.ListTimeFreq
    steps=reader.ListTimeFreq.Count
    reader.Dispose()

    timesQ=[]

    for i in range(len(steptimes)):
    timesQ.append(str(steptimes[i])+" [sec]")

    
    for k in range(len(steptimes)-1):
    #for k in range(10,11):
    ii=k+1
    R1=ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddUserDefinedResult()
    R1.Activate()
    R1.Identifier="A"
    R1.Name='eppleqv_A_'+ii.ToString()
    R1.Expression= 'EPPLEQV_RST'
    R1.DisplayTime=Quantity(timesQ[ii-1])
    R1.EvaluateAllResults()



Insert Force reaction for all contacts
^^^^^^^^^^^^^^

.. code:: python

    

    solution = ExtAPI.DataModel.Project.Model.Analyses[0].Solution
    groups=ExtAPI.DataModel.Project.Model.Connections.Children  #connections
    coordSys=ExtAPI.DataModel.Project.Model.CoordinateSystems.Children
    list1 = []


    totalc=group.Children.Count
    mylastcount=6
    c_count=mylastcount+1

    for group in groups:
    for i in range(totalc-mylastcount,totalc):
    e=group.Children[i]
    list1.Add(e)
    a=solution.AddForceReaction()
    a.LocationMethod=a.LocationMethod.ContactRegion
    a.InternalObject.BoundaryConditionSelection = e.ObjectId  
    a.InternalObject.OrientationCoordinateSystem=coordSys[c_count].Id
    c_count=c_count+1


Insert results automatically for all Namedselctions
^^^^^^^^^^^^^^

.. code:: python

        

    a = ExtAPI.DataModel.Project.Model.Analyses[0]
    b=a.Solution.AddNormalStress()

    NSall = ExtAPI.DataModel.Project.Model.NamedSelections#i
    ListOrient=[b.NormalOrientation.XAxis,b.NormalOrientation.YAxis,b.NormalOrientation.ZAxis] #k
    ListPosition=[b.Position.Top,b.Position.Bottom] #m

    b.Delete()
    
    for i in range(0,NSall.Children.Count):
    for k in range(0,len(ListOrient)):
    for m in range(0,len(ListPosition)):
    b=a.Solution.AddNormalStress()
    b.NormalOrientation=ListOrient[k]
    b.Position=ListPosition[m]
    b.DisplayOption=b.DisplayOption.Averaged
    p = NSall.Children[i]
    b.Location=p
    b.Name="Normal_Stress_"+b.NormalOrientation.ToString()+'_'+p.Name+'_'+ b.DisplayOption.ToString()+'_'+b.Position.ToString()
    ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Activate()
    ExtAPI.Application.ScriptByName("jscript").ExecuteCommand("""DS.Script.doGroupSimilarChildren()""")
    pp=a.Solution.Children.Count
    a.Solution.Children[pp-1].Name="Normal_Stress_"+'_'+p.Name+'_'+ b.DisplayOption.ToString()

    a.Solution.EvaluateAllResults()


to export all result in the tree to PNG (2D image) file.
^^^^^^^^^^^^^^

.. code:: python

        

    # get a list of all the results in the project
    results=ExtAPI.DataModel.Tree.GetObjectsByType(DataModelObjectCategory.Result)
    #loop over the results
    for n in range(0,results.Count):
    # select and activate the result                      
    result = results[n]
    result.Activate()
    mvm = ExtAPI.Graphics.ModelViewManager

    # export the result as a 2D PNG file
    mvm.CaptureModelView(result.Name,"PNG","D:\\Images")
    print "Done with Exporting Results"


save a plot at all solved time points
^^^^^^^^^^^^^^

.. code:: python

    

    reader = ExtAPI.DataModel.AnalysisList[0].GetResultsData()
    steptimes=reader.ListTimeFreq
    steps=reader.ListTimeFreq.Count
    reader.Dispose()


    timesQ=[]

    for i in range(len(steptimes)):
    timesQ.append(str(steptimes[i])+" [sec]")

    sol= ExtAPI.DataModel.Project.Model.Analyses[0].Solution 
    R1=sol.AddTemperature()


    for k in range(0,len(timesQ)):
    R1.Activate()
    R1.DisplayTime=Quantity(timesQ[k])
    R1.Name='Temperature_at_time_'+timesQ[k].ToString()
    R1.EvaluateAllResults()
    mvm = ExtAPI.Graphics.ModelViewManager
    mvm.CaptureModelView(R1.Name, "PNG", "D:\My_Projects")


Scoping a result item (3 ways)
^^^^^^^^^^^^^^

.. code:: python

    



    solution = ExtAPI.DataModel.Project.Model.Analyses[0].Solution

    #using a named selection
    total_deformation1 = solution.AddTotalDeformation()
    ns = ExtAPI.DataModel.Project.Model.NamedSelections.Children[0]
    total_deformation1.Location = ns
    total_deformation1.Name='total_deformation1'

    #using Reference Id of Geometry
    total_deformation2 = solution.AddTotalDeformation()
    scope = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    scope.Ids = [18]
    total_deformation2.Location = scope
    total_deformation2.Name='total_deformation2'

    #using current gui selection 
    #TODO ASk Dipin. will this work ?
    gui=ExtAPI.SelectionMgr.CurrentSelection.Ids   #my current selection is stored
    total_deformation3 = solution.AddTotalDeformation()
    scope = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    scope.Ids = gui
    total_deformation3.Location = scope
    total_deformation3.Name='total_deformation3'


Adding a result : Force reaction with surface cons geom
^^^^^^^^^^^^^^

.. code:: python

        

    solu= ExtAPI.DataModel.Project.Model.Analyses[0].Solution
    fb=solu.AddForceReaction()
    fb.LocationMethod=LocationDefinitionMethod.Surface
    surf = ExtAPI.DataModel.Project.Model.ConstructionGeometry.Children[0]
    fb.SurfaceSelection=surf


    geo= ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    geo.Ids=[6]

    NS=ExtAPI.DataModel.AnalysisList[0].Components
    #  NS is a list of lists : [[31], [4, 5, 6, 7, 24, 25, 26, 27, 32, 33, 34, 35]]
    n1=NS[0]

    n2=ExtAPI.DataModel.Project.Model.NamedSelections.Children[0]
    # n2 is : Ansys.ACT.Automation.Mechanical.MainThread.NamedSelection


^^^^^^^^^^^^^^

.. code:: python

        
    ii=1
    R1=ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddUserDefinedResult()
    R1.Activate()
    R1.Identifier="A"
    R1.Name='MaxCrnrAngl'+ii.ToString()
    R1.Expression= 'MESH_MAXIMUM_CORNER_ANGLE'
    R1.DisplayTime=Quantity("0.1 [sec]")
    R1.EvaluateAllResults()


    enum=57
    analysis = ExtAPI.DataModel.AnalysisList[0]
    reader=analysis.GetResultsData()
    reader.CurrentResultSet=1
    res=reader.GetResult('MESH_')
    res.SelectComponents(['MAXIMUM_CORNER_ANGLE'])
    res.GetElementValues(enum)
    reader.Dispose()


    elementId=1

    reader=ExtAPI.DataModel.AnalysisList[0].GetResultsData()
    reader.CurrentResultSet=1
    P=reader.GetResult("S")
    P.SelectComponents(["X"]) 
    f=P.GetElementValues(elementId) 
    reader.Dispose()


change units of results fetched
^^^^^^^^^^^^^^

.. code:: python

        

    import units
    analysis = ExtAPI.DataModel.Project.Model.Analyses[0]
    reader = analysis.GetResultsData()
    stress = reader.GetResult("S")
    unit_stress = stress.GetComponentInfo("X").Unit
    conv_stress = units.ConvertUnit(1.,unit_stress,"Pa","Stress")


Insert an image for all results
^^^^^^^^^^^^^^

.. code:: python

    

    results = ExtAPI.DataModel.Project.Model.GetChildren[Ansys.ACT.Automation.Mechanical.Results.Result](True)
    ids = []
    with Transaction(suspendClicks=False):
        for result in results:
            if not result.Suppressed:
                if not result.ObjectId in ids:
                    result.Activate()
                    result.AddImage()
                    ids.Add(result.ObjectId)
    
    ExtAPI.DataModel.Tree.Refresh()


Export some results to Images
^^^^^^^^^^^^^^

.. code:: python

    

    allresults=ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result)

    rtype=Ansys.ACT.Automation.Mechanical.Results.StressResults.NormalStress
    f = [i for i in allresults if i.GetType() == rtype]

    ExtAPI.Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
    path1=r"D:\myplots"


    for n in range(0,f.Count):                 
        result = f[n]
        result.Parent.Activate()
        selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
        selection.Ids = result.Location.Ids   #or [result.Location.Ids[0]] for the first object only 
        ExtAPI.Graphics.Camera.SetFit(selection)
        result.Activate()
        #ExtAPI.Graphics.Camera.SetFit()
        path3=path1+"\\"+result.Name+"_location"+".png"
        ExtAPI.Graphics.ExportScreenToImage(path3)


find contact and csys  by name mytext="m22"
^^^^^^^^^^^^^^

.. code:: python

        

    #find contact and csys  by name mytext="m22"
    ContAll=ExtAPI.DataModel.Project.Model.Connections.GetChildren[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion](True)
    a1 = [i for i in ContAll if i.Name == mytext][0]


    c1=ExtAPI.DataModel.AnalysisList[0].DataObjects.GetByName('Coordinate Systems').DataObjects.GetByName(mytext) #datawrapper
    c2=ExtAPI.DataModel.GetObjectById(c1.Id) #object

    f = ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddForceReaction()
    f.LocationMethod =  LocationDefinitionMethod.ContactRegion
    f.ContactRegionSelection=a1
    f.Orientation=c2


scope to a path
^^^^^^^^^^^^^^

.. code:: python

    

    model = ExtAPI.DataModel.Project.Model 
    analysis = model.Analyses[0]
    s = analysis.Solution.AddMaximumPrincipalStress()
    s.ScopingMethod = GeometryDefineByType.Path
    path1 = model.ConstructionGeometry.Children[0]
    sel = ExtAPI.SelectionManager.CurrentSelection

    pathLoc = Ansys.Mechanical.Selection.PathLocation(path1, sel)

    s.Location = pathLoc


Export model to AVZ file with white background
^^^^^^^^^^^^^^

.. code:: python

    


    #  export model to AVZ file with white background
    setting3d = Ansys.Mechanical.Graphics.Graphics3DExportSettings()
    setting3d.Background = GraphicsBackgroundType.White
    Graphics.Export3D("c:\\avz_white.avz", Graphics3DExportFormat.AVZ, setting3d)

    #export image with enhanced resolution to PNG file
    setting2d = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
    setting2d.Resolution = GraphicsResolutionType.EnhancedResolution
    Graphics.ExportImage("c:\\temp\\image_enhancement.png", GraphicsImageExportFormat.PNG, setting2d)


Get Layers
^^^^^^^^^^^^^^

.. code:: python

    

    global meshdata , layers
    meshdata = ExtAPI.DataModel.MeshDataByName("Global")
    layers = ExtAPI.DataModel.Project.Model .GetChildren [Ansys.ACT.Automation.Mechanical.LayeredSection] (True)


    def getLcount(myelemnum):
        global meshdata , layers
        for layer in layers:
            meshregion = meshdata.MeshRegionById(layer.Location.Ids[0])
            if myelemnum in meshregion.ElementIds:
                sdata = layer.Layers.RowCount
                break
        return sdata


    L=getLcount(350)
    print L


create a probe on a node
^^^^^^^^^^^^^^

.. code:: python

    

    analysis=ExtAPI.DataModel.AnalysisByName('Static Structural')
    resultObject=ExtAPI.DataModel.GetObjectsByName('Equivalent Stress')[0]
    probeLabel = Graphics.LabelManager.CreateProbeLabel(resultObject)
    probeLabel.Scoping.Node = 1984

