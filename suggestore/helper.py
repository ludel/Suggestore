import pkg_resources

import pandas as pd

from .interfaces.client import Client

client = Client(delay=0, language="fr-FR")

csv_path = '/home/travis/virtualenv/python3.7.1/src/suggestore/suggestore/clustering/data/movie_clustered.csv'
df_movies = pd.read_csv(csv_path)


def suggest_movies(id_movie, page=0):
    cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster'].values[0]

    return cluster_detail(cluster_id, page)


def cluster_detail(cluster, index):
    try:
        movie_id = df_movies.loc[df_movies.cluster == int(cluster), 'id'].iloc[index]
        movie_detail = client.get_movie(int(movie_id)).json
    except IndexError:
        movie_detail = {}

    return movie_detail


def cluster_details(cluster, limit_head):
    for movie in df_movies.loc[df_movies.cluster == int(cluster), 'id'].head(limit_head):
        yield client.get_movie(int(movie)).json


def search_movie(query):
    return [movie.json for movie in client.search(query)]


def info_movie(id_movie):
    return client.get_movie(id_movie).json


def top_movies(page):
    for movie in client.top_movies(page):
        yield movie.json
