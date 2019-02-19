from .credits import Credit
from .generic import GenericList


class Movie:
    def __init__(self, **kwargs):
        self.json = kwargs

        for key, value in kwargs.items():

            if key == 'genres' or key == 'keywords':
                value = GenericList(*value)
            if key == 'credits':
                value = Credit(**value)
            if key == 'poster_path':
                value = "https://image.tmdb.org/t/p/original" + str(value)
            setattr(self, key, value)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f"<MovieObject {getattr(self, 'id')} : {getattr(self, 'title')}>"

    def __str__(self):
        return getattr(self, 'title')
