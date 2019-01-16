import pandas as pd
import pkg_resources

from suggestore.interfaces.client import Client

client = Client(delay=0, language="fr-FR")

csv_path = pkg_resources.resource_filename(__name__, 'clustering/data/movie_clustered.csv')
df_movies = pd.read_csv(csv_path)


def suggest_movies(id_movie):
    cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster'].values[0]

    return df_movies.loc[df_movies.cluster == int(cluster_id), 'id'].tolist()


def search_movie(query):
    return [movie.json for movie in client.search(query)]


def info_movie(id_movie):
    return client.get_movie(id_movie).json


def get_movie_full_data():
    csv_movie = pkg_resources.resource_filename(__name__, 'clustering/data/movie.csv')
    return pd.read_csv(csv_movie)
