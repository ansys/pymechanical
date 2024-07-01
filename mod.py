import ansys.mechanical.core as mech

def change_project_name(app: mech.App, name: str):
    """Change the project name of `app` to `name`."""
    app.DataModel.Project.Name = name

def get_project_name(app: mech.App):
    return app.DataModel.Project.Name

def get_model_name(app):
    return app.Model.Name


# option B

def remote_method():
    pass

# class ServiceMethods:
#     @remote_method
#     def get_model_name(self, app):
#         return app.Model.Name
#     def helper_func(self):
#         pass

    # more methods

G_CAL: "DSCAL" = None

import typing
class DSObject:
    def __init__(self, objtype: str):
        self.properties: typing.Dict[str, object] = dict()
        self.objtype=objtype
        self._id = None
    def set_property_value(self, prop: str, value: object):
        self.properties[prop] = value
        G_CAL.on_object_modified(self.get_id(), prop)
    def get_property_value(self, prop: str)->object:
        return self.properties[prop]
    def get_id(self) -> int:
        return self._id
    def set_id(self, id: int):
        self._id = id


class DSDB:
    def __init__(self):
        self.objects: typing.Dict[int, DSObject] = dict()
        self.nextid=1
    def add_object(self, obj: DSObject) -> int:
        id = self.nextid
        self.objects[id]=obj
        obj.set_id(id)
        self.nextid=self.nextid+1
        return id
    def get_object(self, id: int) -> DSObject:
        return self.objects[id]

class Delegate:
    def __init__(self):
        self.slots: typing.List[typing.Callable] = []
    def signal(self, payload: object):
        for slot in self.slots:
            slot(payload)
    def add_slot(self, func: typing.Callable):
        self.slots.append(func)

import dataclasses
@dataclasses.dataclass
class ObjectModifiedEventArgs:
    id: int
    prop: str

class DSCAL:
    def __init__(self):
        self.db = DSDB()
        self._on_object_modified: Delegate = Delegate()
    def on_object_modified(self, id: int, prop: str):
        self._on_object_modified.signal(ObjectModifiedEventArgs(id, prop))
    def register_on_object_modified(self, func: typing.Callable):
        self._on_object_modified.add_slot(func)

def get_cal() -> "DSCAL":
    global G_CAL
    if G_CAL == None:
        G_CAL = DSCAL()
    return G_CAL


def redraw(args: ObjectModifiedEventArgs):
    objtype = get_cal().db.get_object(args.id).objtype
    print("objtype is: ", objtype)
    print("prop is: ", args.prop)
    if objtype == "foo" and args.prop == "bar":
        print("redrawing graphics")
    else:
        print("nothing to do")


def useraction100():
    active_id=3
    get_cal().db.get_object(active_id).set_property_value("foo", 11)
    if not batch_mode:
        print("doing some ui stuff")
    if ui_mode:
        pass

# model - data model
# controller - code which updates the data model
# view - what presents the data model to the user, observes changes to data model

def main():
    get_cal().register_on_object_modified(redraw)
    obj = DSObject(("foo"))
    id = get_cal().db.add_object(obj)
    print(id)
    print(obj.get_id())
    obj.set_property_value("x", 1)
    obj.set_property_value("y", 2)
    quuxid = get_cal().db.add_object(DSObject("quux"))
    print("no redraw yet")
    obj.set_property_value("bar", 1)
    print("should have redrawn")
    get_cal().db.get_object(quuxid).set_property_value("bar", 2)
    print("should not have redrawn")

if __name__ == "__main__":
    main()
