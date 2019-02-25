import pandas as pd
import pkg_resources
from sklearn.metrics.pairwise import linear_kernel

from suggestore.core.client import Client

client = Client(delay=0, language="fr-FR")

csv_path = pkg_resources.resource_filename(__name__, 'clustering/data/movie_clustered.csv')
df_movies = pd.read_csv(csv_path)


def suggest_movies(id_movie):
    try:
        cluster_id = df_movies.loc[df_movies.id == id_movie, 'cluster'].values[0]
    except IndexError:
        return []

    cluster_movies = df_movies.loc[df_movies.cluster == int(cluster_id), 'id'].tolist()

    return filter_results(id_movie, cluster_movies)


def filter_results(movie_id, same_cluster_movie):
    df_feature = pd.read_csv(
        pkg_resources.resource_filename(__name__, 'similarity/data/feature_binary.csv')
    )

    context_data = df_feature.loc[df_feature['id'].isin(same_cluster_movie)]
    context_data.reset_index(drop=True, inplace=True)

    idx = context_data.loc[context_data['id'] == movie_id].index.values.astype(int)[0]

    series_id = context_data['id']
    del context_data['id']

    cosine_sim = linear_kernel(context_data, context_data)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores]

    return series_id.iloc[movie_indices].tolist()


def search_movie(query):
    return [movie.to_dict() for movie in client.search(query)]


def info_movie(id_movie):
    return client.get_movie(id_movie).to_dict()


def get_movies(page, order_by, search=None):
    movies = client.search(search, page) if search else client.top_movies(order_by, page)

    return [movie.to_dict() for movie in movies]


def get_movie_full_data():
    csv_movie = pkg_resources.resource_filename(__name__, 'clustering/data/movie.csv')
    return pd.read_csv(csv_movie)


if __name__ == '__main__':
    suggest_movies(55301)
