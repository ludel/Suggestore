from .credits import Credit
from .generic import GenericList


class Movie:
    def __init__(self, id, title, genres=None, keywords=None, budget=0, release_date=None, original_language=None,
                 credits=None, overview='', vote_average=0, vote_count=0, poster_path='', videos=None, reviews=None,
                 runtime=None):

        if genres is None:
            genres = []
        if keywords is None:
            genres = []
        if credits is None:
            credits = {}

        self.id = id
        self.title = title
        self.genres = GenericList(*genres)
        self.keywords = GenericList(*keywords)
        self.budget = budget
        self.release_date = release_date
        self.original_language = original_language
        self.credits = Credit(**credits)
        self.overview = overview
        self.vote_average = vote_average * 10
        self.vote_count = vote_count
        self.videos = videos
        self.reviews = reviews
        self.runtime = runtime
        self.poster_path = "https://image.tmdb.org/t/p/original" + str(poster_path)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f"<MovieObject {getattr(self, 'id')} : {getattr(self, 'title')}>"

    def __str__(self):
        return getattr(self, 'title')
