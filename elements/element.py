

class Component(object):

    def __init__(self, id_object: str, title: str, **kwargs):

        self.id_object = id_object
        self.title = title
        self.options = kwargs

        # for key, value in kwargs.items():
        #
        #     self.__dict__[key] = kwargs.get(key, value)

    def load(self):
        ...