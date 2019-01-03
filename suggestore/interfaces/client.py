from time import sleep

import requests as req

from .movie import Movie, Matrix

KEY = "93a2951771280d67e877c4f9c336fb5c"
URL = "https://api.themoviedb.org/3"
SELECTED_DATA = ['id', 'title', 'genres', 'keywords', 'budget', 'release_date', 'original_language', 'credits',
                 'overview', 'vote_average', 'vote_count', 'poster_path']


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

        json['poster_path'] = "https://image.tmdb.org/t/p/original/" + json.get('poster_path')
        json['vote_average'] *= 10

        attr = {}
        for name in SELECTED_DATA:
            attr[name] = json.get(name, "Unknown")

        print("Title : " + attr["title"])

        return Movie(**attr)

    def keyword(self, movie_id):
        path = f"movie/{movie_id}/keywords"
        request = req.get(f"{URL}/{path}?api_key={self.key}").json()
        return request['keywords']

    def search(self, query):
        full_url = f"{self.url}/search/movie?api_key={self.key}&language={self.language}&query={query}&page=1"
        list_movies = req.get(full_url).json()['results']

        for movie in list_movies:
            yield self.get_movie(movie["id"])

    def credits_id(self, movie_id):
        full_url = f"{self.url}/movie/{movie_id}/credits?api_key={self.key}&language=en-US"
        credit = req.get(full_url).json()

        for person in credit['cast'] + credit['crew']:
            yield person

    def all_genres(self):
        path = f"/genre/movie/list?api_key={self.key}&language=en-US"
        return Matrix(req.get(URL + path).json()["genres"])

    def top_movies(self, limit_page=1):
        full_url = f"{self.url}/movie/top_rated?api_key={self.key}&language={self.language}&page={limit_page}"
        list_movies = req.get(full_url).json()['results']

        for movie in list_movies:
            yield self.get_movie(movie["id"])

    def top_movies_limit(self, limit_page, start=1):
        full_url = f"{self.url}/movie/top_rated?api_key={self.key}&language={self.language}&page="
        rest = limit_page * 19
        end = limit_page + start

        for page in range(start, end):
            list_movies = req.get(full_url + str(page)).json()['results']

            for key in range(0, 19):
                rest -= 1
                print(f"Status : {rest}/{limit_page * 19}")

                yield self.get_movie(list_movies[key]["id"])
