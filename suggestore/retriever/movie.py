import collections


class Movie(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self['vote_average'] = kwargs.get('vote_average') * 10
        self['poster_path'] = f"https://image.tmdb.org/t/p/original{kwargs.get('poster_path')}"
        self['backdrop_path'] = f"https://image.tmdb.org/t/p/original{kwargs.get('backdrop_path')}"

        crews = collections.defaultdict(list)
        for crew in kwargs['credits']['crew']:
            department = crew['job']
            crews[department].append(crew)
        self['crew'] = crews

        self['cast'] = kwargs['credits']['cast']
        del kwargs['credits']['cast']

    def get_crew(self, category, job):
        try:
            crew = self[category][job][0]['name']
        except (IndexError, KeyError):
            crew = ''
        return crew

    def get_cast(self, category, index):
        try:
            cast = self[category][index]['name']
        except (IndexError, KeyError):
            cast = ''
        return cast

    def __repr__(self):
        return f"<Movie {self['id']} : {self['title']}>"

    def __str__(self):
        return self['title']
