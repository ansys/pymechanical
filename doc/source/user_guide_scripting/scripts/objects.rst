.. _treeobjects:

Tree Objects
==============

This section has helper scripts for  Tree Objects .

.. contents::
   :local:
   :depth: 4



Accessing Geometry : GeoEntityById
^^^^^^^^^^^^^^

.. code:: python

    

    body=ExtAPI.DataModel.GeoData.GeoEntityById(312)


Accessing Mesh Data : MeshDataByName
^^^^^^^^^^^^^^

.. code:: python

    

    ExtAPI.DataModel.MeshDataByName("Global").NodeById(555)
    ExtAPI.DataModel.MeshDataByName("Global").ElementById(444)


Accessing All Objects and Child Objects: GetObjectsByType and GetChildren
^^^^^^^^^^^^^^

.. code:: python

        

    # ALL TREE OBJECTS
    AllObj=ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject,True)

    # ALL BODIES
    allbodies=ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body,True)

    # ALL NAMED SELECTIONS
    nsall=ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelections.NamedSelection)

    #ALL CONTACT REGIONS
    abc= ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.ContactRegion)
    all_contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion , True)

    # A SPECIFIC CONTACT REGION
    my_contact = [contact for contact in all_contacts if contact.Name == "Contact Region"][0]

    #ALL RESULT OBJECTS OF A SPECIFIC TYPE
    allNormStress= ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result.NormalStress)

    #OTHERS
    all_remote_points= ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.RemotePoint)
    Ana = ExtAPI.DataModel.Tree.GetObjectsByType(DataModelObjectCategory.Analysis)

    # One can also use ACT Automation API instead of DataModelObjectCategory
    all_contacts2=ExtAPI.DataModel.Project.Model.Connections.GetChildren[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion](True)
    all_remote_points2 = ExtAPI.DataModel.Project.Model.GetChildren[Ansys.ACT.Automation.Mechanical.RemotePoint](True)
    all_folders=ExtAPI.DataModel.Project.Model.GetChildren[Ansys.ACT.Automation.Mechanical.TreeGroupingFolder](True)



Find all Duplicate Objects (by Name)
^^^^^^^^^^^^^^

.. code:: python

    

    import collections

    AllObj=ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject,True)
    AllObjNames = [ x.Name for x in AllObj]
    duplicates_by_name= [item for item,count in collections.Counter(AllObjNames).items() if count > 1]
    print(duplicates_by_name)



Using DataObjects and GetByName
^^^^^^^^^^^^^^

.. code:: python

    

    c1='Solution'
    c2='Far-field Sound Power Level Waterfall Diagram'
    c=ExtAPI.DataModel.AnalysisList[0].DataObjects.GetByName(c1).DataObjects.GetByName(c2)


Using DataObjects , NamesbyType and GetByName
^^^^^^^^^^^^^^

.. code:: python

        

    newContactList=[]    
    dataobjects = ExtAPI.DataModel.AnalysisList[0].DataObjects
    for group in dataobjects:
        print(group.Type)
    names = dataobjects.NamesByType('ContactGroup')
    for name in names:
    connetDataObjects = dataobjects.GetByName(name).DataObjects
    CNames = connetDataObjects.Names
    for cName in CNames:
    typeC = connetDataObjects.GetByName(cName).Type
    if typeC == 'ConnectionGroup':
        contactslist = connetDataObjects.GetByName(cName).DataObjects.NamesByType('ContactRegion')
        for contact in contactslist:
        ContactType = connetDataObjects.GetByName(cName).DataObjects.GetByName(contact).PropertyValue('ContactType')
        ContactState = connetDataObjects.GetByName(cName).DataObjects.GetByName(contact).PropertyValue("Suppressed")
        if ContactState == 0 and ContactType == 1:
        newContactList.append(contact)
    print(newContactList)


Using GetObjectsByName
^^^^^^^^^^^^^^

.. code:: python

    

    bb=ExtAPI.DataModel.GetObjectsByName("Gray Cast Iron")[0]


Accessing a  Named Selection
^^^^^^^^^^^^^^

.. code:: python

        

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    my_nsel = [i for i in NSall if i.Name.startswith("b")][0]
    my_nsel2 = [i for i in NSall if i.Name == "aaa"][0]


Get all Unsuppressed bodies and point masses
^^^^^^^^^^^^^^

.. code:: python

        

    allBodies=ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body,True)
    allBodies = [i for i in allBodies if not i.Suppressed ]
    print(len(allBodies))

    allPM=ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.PointMass,True)
    allPM = [i for i in allPM if not i.Suppressed]


