from .credits import Credit
from .generic import GenericList


class Movie:
    def __init__(self, **kwargs):
        self.json = kwargs

        for key, value in kwargs.items():
            data = value

            if type(value) is list:
                data = GenericList(*value)
            if key == 'credits':
                data = Credit(**value)

            setattr(self, key, data)

    def __repr__(self):
        return f"<MovieObject {getattr(self, 'id')} : {getattr(self, 'title')}>"

    def __str__(self):
        return getattr(self, 'title')
