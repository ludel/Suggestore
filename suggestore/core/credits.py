class Credit:
    def __init__(self, **kwargs):
        self.cast = kwargs.get('cast')
        self.crew = kwargs.get('crew')

    def crew_search(self, query):
        for crew in self.crew:
            if crew.get("department") == query:
                return crew['name'].replace(',', '')

        return ''

    @property
    def director(self):
        return self.crew_search('Directing')

    @property
    def compositor(self):
        return self.crew_search('Sound')

    @property
    def writer(self):
        return self.crew_search('Writing')

    def main_actors(self, limit=3):
        for cast in self.cast:
            order = cast['order']

            if order < limit:
                yield cast['name'].replace(',', '')

