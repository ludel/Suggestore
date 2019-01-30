import pandas as pd

from suggestore.core.client import Client

path_matrix = "../data/movie.csv"


def append_file(list_movies):
    file_movie = open(path_matrix, "a")

    for movie in list_movies:
        file_movie.write("\n")

        title = movie.title.replace(",", "")

        keywords = movie.keywords.firsts(10)

        main_actors = [actor.remplace(' ', '_') for actor in movie.credits.main_actor(3)]

        compositor = movie.credits.compositor.remplace(' ', '_')
        writer = movie.credits.writer.remplace(' ', '_')
        director = movie.credits.director.remplace(' ', '_')

        matrix = [movie.id, title, movie.budget, keywords, movie.genres, movie.release_date, movie.original_language,
                  director, writer, compositor, main_actors]

        file_movie.write(",".join(str(key) for key in matrix))
    file_movie.close()


# todo : TV MOVIE => TV_Movie
# todo : add poster path to matrix
if __name__ == '__main__':
    for i in range(100, 300):
        movies = Client(delay=0.5).top_movies(i)
        append_file(movies)
        print(f':: Page {i}')

    df = pd.read_csv(path_matrix, error_bad_lines=False)
    df.drop_duplicates(subset='id', inplace=True)
    df.set_index('id', inplace=True)
    df.to_csv(path_matrix)
