from time import sleep

import requests as req

from .movie import Movie

KEY = "93a2951771280d67e877c4f9c336fb5c"
URL = "https://api.themoviedb.org/3"
SELECTED_DATA = ['id', 'title', 'genres', 'keywords', 'budget', 'release_date', 'original_language', 'credits',
                 'overview', 'vote_average', 'vote_count', 'poster_path', 'budget']


class Client:
    def __init__(self, delay=1, language="en-US"):
        self.url = URL
        self.key = KEY
        self.delay = delay
        self.language = language

    def get_movie(self, movie_id):
        sleep(self.delay)

        full_url = f"{self.url}/movie/{movie_id}?api_key={self.key}&language={self.language}&append_to_response=credits,keywords"

        json = req.get(full_url).json()
        try:
            json['keywords'] = json['keywords']['keywords']
        except KeyError:
            json['keywords'] = {}

        if not json.get('poster_path'):
            json['poster_path'] = ""

        json['poster_path'] = "https://image.tmdb.org/t/p/original" + json['poster_path']
        json['vote_average'] *= 10

        attr = {}
        for name in SELECTED_DATA:
            attr[name] = json.get(name, "Unknown")

        print("=> " + attr["title"])

        return Movie(**attr)

    def search(self, query):
        full_url = f"{self.url}/search/movie?api_key={self.key}&language={self.language}&query={query}&page=1"
        list_movies = req.get(full_url).json()['results']

        for movie in list_movies:
            yield self.get_movie(movie["id"])

    def top_movies(self, page=1):
        full_url = f"{self.url}/movie/top_rated?api_key={self.key}&language={self.language}&page={page}"
        list_movies = req.get(full_url).json()['results']

        for movie in list_movies:
            yield self.get_movie(movie["id"])


