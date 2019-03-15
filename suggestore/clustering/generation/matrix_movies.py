import pandas as pd

from suggestore.core.client import Client

path_matrix = "../data/movie.csv"


def append_file(list_movies):
    with open(path_matrix, "a") as file_movie:
        for index, movie in enumerate(list_movies):
            payload = {
                'id': movie.id,
                'title': movie.title.replace(",", ""),
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

            if page == 1 and index == 0:  # wtf c'est ouf
                file_movie.write(";".join(f'"{key}"' for key in payload.keys()))

            file_movie.write("\n")
            file_movie.write(";".join(f'"{value}"' for value in payload.values()))


# todo : TV MOVIE => TV_Movie

if __name__ == '__main__':
    for page in range(1, 300):
        movies = Client(delay=0, language='fr-FR').top_movies('top_rated', page)
        append_file(movies)
        print(f':: Page {page}')

    df = pd.read_csv(path_matrix, error_bad_lines=False, delimiter=';', quotechar='"')
    df.drop_duplicates(subset='id', inplace=True)
    df.set_index('id', inplace=True)
    df.to_csv(path_matrix)
