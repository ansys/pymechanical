G_stuff = 1


class Foo:
    def propget_quux(self):
        global G_stuff
        return G_stuff

    def propset_quux(self, value):
        global G_stuff
        G_stuff = value

    bar = property(propget_quux, propset_quux)


class Baz:
    def __init__(self, typ):
        print("callinginit")
        super().__setattr__("_inner", typ())
        super().__setattr__("x", 100)
        # here install the property

    def __getattr__(self, attr):
        print(f"calling gettr {attr}")
        if hasattr(self._inner, attr):
            return getattr(self._inner, attr)
        return self.__dict__.items[attr]

    def __setattr__(self, attr, value):
        if hasattr(self._inner, attr):
            inner_prop = getattr(self._inner.__class__, attr)
            if isinstance(inner_prop, property):
                inner_prop.fset(self._inner, value)
        else:
            super().__setattr__(attr, value)


import sys

if __name__ == "__main__":
    # foo=Foo()
    # print(foo.__class__.__dict__)
    # barprop: property =getattr(Foo, "bar")
    # print(barprop.fget(foo))
    # print(barprop.fset(foo, 3))
    # print(foo.bar)
    # baz = Baz(Foo)
    # sys.exit(0)

    baz = Baz(Foo)
    assert baz.bar == 1
    print(baz.bar)
    print(baz.x)
    baz.x = 200
    assert baz.x == 200
    baz.bar = 2
    assert G_stuff == 2
    assert baz.bar == 2


# x = "some string"
# x.capitalize()

# getattr(getattr(x, "capitalize"), "__call__")()
