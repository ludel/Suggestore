class GenericList:
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
        return ", ".join(word for word in self.name)
