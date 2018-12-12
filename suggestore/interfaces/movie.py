class Matrix:
    def __init__(self, *args):
        self.full = args
        self.id = [data.get('id') for data in args]
        self.name = [data.get('name') for data in args]

    def firsts(self, limit):
        firsts = self.name

        if len(self.name) > limit:
            firsts = self.name[0:limit]

        return " ".join(word.replace(' ', '_') for word in firsts)

    def __str__(self):
        return " ".join(word for word in self.name)


class Movie:
    def __init__(self, **kwargs):
        self.json = kwargs

        for key, value in kwargs.items():
            data = Matrix(*value) if type(value) is list else value
            setattr(self, key, data)

    def __repr__(self):
        return f"<MovieObject {getattr(self,'id')} : {getattr(self,'title')}>"

    def __str__(self):
        return getattr(self, 'title')
