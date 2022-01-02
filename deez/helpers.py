def method_proxy(cls, attr):
    return object.__getattribute__(cls, attr)
