import pandas as pd

from .interfaces.client import Client

client = Client(delay=0, language="fr-FR")
df_movies = pd.read_csv('~/Workspace/onregardequoi/suggestore/suggestore/clustering/data/movie_clustered.csv')


def suggest_movies(selected_movies: list, limit_head=10):
    suggestions = {}
    selected_movies = [int(_id) for _id in selected_movies]

    for id_movie in selected_movies:
        cluster_id = int(df_movies.loc[df_movies.id == id_movie, 'cluster'])

        suggestions[cluster_id] = list(get_detail(id_movie, cluster_id))

    return suggestions


def get_detail(id_movie: int, cluster: int, limit_head=10):
    for movie in df_movies.loc[df_movies.cluster == int(cluster), 'id'].head(limit_head):
        yield client.get_movie(int(movie)).json


def info_movie(id_movie: int):
    return client.get_movie(id_movie).json


def top_movies(page):
    for movie in client.top_movies(page):
        yield movie.json
