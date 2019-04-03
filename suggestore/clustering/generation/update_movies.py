import pandas as pd

from suggestore.clustering.generation.clustering import Clustering
from suggestore.clustering.generation.matrix_movies import write_file, clean_data
from suggestore.core.client import Client


def generate_tmp_latest_movie():
    path = '../data/movie-tmp.csv'
    client = Client(delay=0, language='fr-FR')
    now_playing = client.now_playing(limit_popularity=100)

    write_file(now_playing, page=1, type_open='w', path_matrix=path)
    clean_data(path)


def append_main_data():
    old_data = pd.read_csv('../data/movie.csv')
    extra_data = pd.read_csv('../data/movie-tmp.csv')

    new_data = old_data.append(extra_data).reset_index(drop=True)
    new_data.to_csv('../data/movie.csv')


def main():
    generate_tmp_latest_movie()
    append_main_data()

    Clustering().process()


if __name__ == '__main__':
    main()
