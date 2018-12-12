import pandas as pd

from client import Client


def append_file(path_file, list_movies):
    with open(path_file, "a") as f:
        for movie in list_movies:
            f.write("\n")

            title = movie.title.replace(",", "")
            director = ""
            main_actor = [""] * 2

            for person in movie.credits.full:
                order = person.get('order', 4)
                if person.get("department", "") == "Directing" and not director:
                    director = person['name'].replace(' ', "_")
                if order < 2:
                    main_actor[order] = person['name'].replace(' ', "_")

            keywords = movie.keywords.firsts(10)

            matrix = [movie.id, title, movie.budget, keywords, movie.genres, movie.release_date,
                      movie.original_language, director, main_actor[0], main_actor[1]]

            print(f"=> New line title: {movie.title}")
            f.write(",".join(str(key) for key in matrix))


# todo : TV MOVIE => TV_Movie

if __name__ == '__main__':
    number_movie = 1
    path_matrix = "../data/movie.csv"

    for i in range(1, 1000):
        movies = Client(delay=3).top_movies(1, start=i)
        append_file(path_matrix, movies)

    df = pd.read_csv(path_matrix, error_bad_lines=False)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop_duplicates(subset='title', inplace=True)
    df.to_csv(path_matrix)
