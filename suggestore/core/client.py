import os
from time import sleep

import requests as req

from .movie import Movie

KEY = os.environ['TOKEN_KEY']
URL = "https://api.themoviedb.org/3"
SELECTED_DATA = ['id', 'title', 'genres', 'keywords', 'budget', 'release_date', 'original_language', 'credits',
                 'overview', 'vote_average', 'vote_count', 'poster_path', 'budget', 'videos', 'reviews', 'runtime']


class Client:
    def __init__(self, delay=1, language="en-US"):
        self.url = URL
        self.key = KEY
        self.delay = delay
        self.language = language

    def get_movie(self, movie_id):
        sleep(self.delay)

        full_url = f"{self.url}/movie/{movie_id}?api_key={self.key}&language={self.language}&append_to_response=credits,keywords,videos,reviews"

        json = req.get(full_url).json()
        try:
            json['keywords'] = json['keywords']['keywords']
        except KeyError:
            json['keywords'] = {}

        if not json.get('poster_path'):
            json['poster_path'] = ""

        json['vote_average'] *= 10

        attr = {}
        for name in SELECTED_DATA:
            attr[name] = json.get(name, "Unknown")

        print("=> " + attr["title"])

        return Movie(**attr)

    def search(self, query, page=1):
        full_url = f"{self.url}/search/movie?api_key={self.key}&language={self.language}&query={query}&page={page}"
        movies = self.request(full_url)

        for data in movies['results']:
            yield Movie(**data)

    def top_movies(self, order_by, page=1):
        full_url = f"{self.url}/movie/{order_by}?api_key={self.key}&language={self.language}&page={page}"
        movies = self.request(full_url)

        for data in movies['results']:
            yield Movie(**data)

    @staticmethod
    def request(url):
        result = req.get(url)

        if not result.ok:
            raise req.ConnectionError(f'for {url}')
        else:
            return result.json()
