import pandas as pd
import pkg_resources

from suggestore.core.client import Client

client = Client(delay=0, language="fr-FR")

csv_path = pkg_resources.resource_filename(__name__, 'clustering/data/movie_clustered.csv')
df_movies = pd.read_csv(csv_path)


def suggest_movies(id_movie):
    try:
        cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster'].values[0]
    except IndexError:
        return []

    return df_movies.loc[df_movies.cluster == int(cluster_id), 'id'].tolist()


def search_movie(query):
    return [movie.to_dict for movie in client.search(query)]


def info_movie(id_movie):
    return client.get_movie(id_movie).to_dict


def get_movies(page, order_by, search=None):
    movies = client.search(search, page) if search else client.top_movies(order_by, page)

    return [movie.to_dict for movie in movies]


def get_movie_full_data():
    csv_movie = pkg_resources.resource_filename(__name__, 'clustering/data/movie.csv')
    return pd.read_csv(csv_movie)
