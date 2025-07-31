.. _connections:

Connections
==============

This section has helper scripts for  Connections .

This section has helper scripts for  Geometry .

.. contents::
   :local:
   :depth: 4


Get information about all Contacts Defined
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    all_contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion , True)
    for contact in all_contacts:
                print("\n" + contact.Parent.Name + " > " + contact.Name + " : " + str(contact.ContactType) + " : " + str(contact.Suppressed)+ " : " + str(contact.ContactFormulation))
                print("Contact : " ,contact.ContactBodies,list(contact.SourceLocation.Ids))
                print("Target : " ,contact.TargetBodies,list(contact.TargetLocation.Ids) )


Insert a Joint using face IDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    face1=44
    face2=251

    model = ExtAPI.DataModel.Project.Model
    j=model.Connections.AddJoint()

    reference_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    reference_scoping.Ids = [face1]
    j.ReferenceLocation=reference_scoping

    mobile_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    mobile_scoping.Ids = [face2]
    j.ReferenceLocation=mobile_scoping


Create Automatic Connections on a chosen named selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    contactgroup=ExtAPI.DataModel.Project.Model.Connections.AddConnectionGroup()
    contactgroup.FaceFace=True
    contactgroup.FaceEdge=contactgroup.FaceEdge.No
    contactgroup.GroupBy=contactgroup.GroupBy.Faces
    contactgroup.Priority=contactgroup.Priority.FaceOverEdge
    contactgroup.InternalObject.DetectCylindricalFacesType=1

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    my_nsel = [i for i in NSall if i.Name == "bodies3"][0]

    contactgroup.Location=my_nsel
    contactgroup.CreateAutomaticConnections()

    mytree = ExtAPI.DataModel.Tree
    mytree.Refresh()


Create a Contact region using face named selections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    c=ExtAPI.DataModel.Project.Model.Connections
    c1=c.AddContactRegion()
    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    a = [i for i in NSall if i.Name == "faces_tube"][0]
    c1.TargetLocation=a
    a = [i for i in NSall if i.Name == "faces_bracket"][0]
    c1.SourceLocation=a


Define  a Bearing
^^^^^^^^^^^^^^^^^
.. code:: python

    brg=ExtAPI.DataModel.Project.Model.Connections.AddBearing()
    brg.ReferenceRotationPlane=RotationPlane.XY
    brg.StiffnessK11.Output.DiscreteValues=[Quantity('11 [N/m]')]
    brg.StiffnessK22.Output.DiscreteValues=[Quantity('22 [N/m]')]
    brg.StiffnessK21.Output.DiscreteValues=[Quantity('21 [N/m]')]
    brg.StiffnessK12.Output.DiscreteValues=[Quantity('12 [N/m]')]

    brg.DampingC11.Output.DiscreteValues=[Quantity('111 [N sec m^-1]')]
    brg.DampingC22.Output.DiscreteValues=[Quantity('122 [N sec m^-1]')]
    brg.DampingC12.Output.DiscreteValues=[Quantity('112 [N sec m^-1]')]
    brg.DampingC21.Output.DiscreteValues=[Quantity('121 [N sec m^-1]')]

    NSall=ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    brg.ReferenceLocation= [i for i in NSall if i.Name == "f1"][0]
    brg.MobileLocation= [i for i in NSall if i.Name == "f2"][0]


