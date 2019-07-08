def upper_attr(class_name, class_parents, class_attr):

    new_attr = dict()
    for k, v in class_attr.items():
        if not k.startswith("__"):
            new_attr[k.upper()] = v

    return type(class_name, class_parents, new_attr)


class Foo(object, metaclass=upper_attr):
    bar = "bip"


print(hasattr(Foo, "bar"))
print(hasattr(Foo, "BAR"))

f = Foo()
print(f.BAR)
