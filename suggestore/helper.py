import pandas as pd

from .interfaces.client import Client

client = Client(delay=0, language="fr-FR")
df_movies = pd.read_csv('~/Workspace/onregardequoi/suggestore/suggestore/clustering/data/movie_clustered.csv')


def suggest_movies_id(id_movie: int, limit_head=10):
    cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster']
    return df_movies.loc[df_movies.cluster == int(cluster_id), 'id'].head(limit_head).tolist()


def suggest_movies_info(id_movie: int, limit_head=10):
    cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster']

    for movie in df_movies.loc[df_movies.cluster == int(cluster_id), 'id'].head(limit_head):
        yield client.get_movie(int(movie)).json


def info_movie(id_movie: int):
    return client.get_movie(id_movie).json


def top_movies(page):
    for movie in client.top_movies(page):
        yield movie.json


if __name__ == '__main__':
    print(list(suggest_movies_info(299536)))
