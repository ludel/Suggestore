import pandas as pd


def write_file(list_movies, page, type_open='a', path_matrix='../data/movie.csv'):
    file_movie = open(path_matrix, type_open)

    for index, movie in enumerate(list_movies):
        payload = {
            'id': movie.id,
            'title': movie.title.replace(',', ''),
            'budget': movie.budget,
            'keywords': ' '.join(movie.keywords.firsts(10)),
            'genres': ' '.join(movie.genres.firsts(10)),
            'release_date': movie.release_date,
            'original_language': movie.original_language,
            'director': movie.credits.director,
            'writer': movie.credits.writer,
            'compositor': movie.credits.compositor,
            'main_actors': ' '.join(movie.credits.main_actors(5)),
            'runtime': movie.runtime,
            'vote_average': movie.vote_average,
            'vote_count': movie.vote_count,
            'poster_path': movie.poster_path,
            'overview': movie.overview.replace(';', ',').replace('"', "'"),
        }

        if page == 1 and index == 0:
            file_movie.write(';'.join(f'"{key}"' for key in payload.keys()))

        file_movie.write('\n')
        file_movie.write(';'.join(f'"{value}"' for value in payload.values()))

    file_movie.close()


def clean_data(path_matrix):
    df = pd.read_csv(path_matrix, error_bad_lines=False, delimiter=';', quotechar='"')
    df.drop_duplicates(subset='id', inplace=True)
    df.set_index('id', inplace=True)
    df.to_csv(path_matrix)

# todo : TV MOVIE => TV_Movie
