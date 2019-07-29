import os

import requests

from suggestore.retriever.movie import Movie


class Client:
    def __init__(self, base_url='https://api.themoviedb.org/3', language="en-US"):
        self.base_url = base_url

        self.key = os.environ['TOKEN_KEY']
        self.language = language

    def get_url_args(self, **kwargs):
        kwargs.update({'api_key': self.key, 'language': self.language})
        return '&'.join(f'{k}={v}' for k, v in kwargs.items())

    def retrieve(self, movie_id):
        url_args = self.get_url_args(append_to_response='credits,keywords,videos,reviews')
        full_url = f'{self.base_url}/movie/{movie_id}?{url_args}'

        req = requests.get(full_url)
        req.raise_for_status()

        print(f"=> {req.json()['title']}")

        return Movie(**req.json())

    def _list(self, url_args, endpoint, detail):
        full_url = f'{self.base_url}{endpoint}?{url_args}'

        req = requests.get(full_url)
        req.raise_for_status()

        for item in req.json()['results']:
            yield self.retrieve(item['id']) if detail else Movie(**item)

    def search(self, query, page=1, detail=True):
        return self._list(self.get_url_args(query=query, page=page), '/search/movie', detail)

    def top(self, page=1, detail=True):
        return self._list(self.get_url_args(page=page), '/movie/top_rated', detail)

    def now_playing(self, page=1, region='FR', detail=True):
        return self._list(self.get_url_args(page=page, region=region), '/movie/now_playing', detail)


if __name__ == '__main__':
    c = Client()

    for movie in c.top(1):
        print(movie['crew']['Producer'])
