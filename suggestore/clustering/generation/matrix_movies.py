import pandas as pd

from .client import Client

path_matrix = "../data/movie.csv"


def append_file(list_movies):
    file_movie = open(path_matrix, "a")

    for movie in list_movies:
        file_movie.write("\n")

        title = movie.title.replace(",", "")

        keywords = movie.keywords.firsts(10)

        matrix = [movie.id, title, movie.budget, keywords, movie.genres, movie.release_date, movie.original_language,
                  movie.credits.director, movie.credits.writer, movie.credits.compositor] + list(
            movie.credits.main_actor(3))

        file_movie.write(",".join(str(key) for key in matrix))
    file_movie.close()


# todo : TV MOVIE => TV_Movie

if __name__ == '__main__':
    for i in range(100, 300):
        movies = Client(delay=0.5).top_movies(i)
        append_file(movies)
        print(f':: Page {i}')
    # ,id,title,budget,keywords,genres,release_date,original_language,director,writer,compositor,actor_1,actor_2,actor_3

    df = pd.read_csv(path_matrix, error_bad_lines=False)
    df.drop_duplicates(subset='id', inplace=True)
    df.set_index('id', inplace=True)
    df.to_csv(path_matrix)
