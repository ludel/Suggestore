import pandas as pd
from pandas.errors import EmptyDataError

from suggestore.retriever.client import Client

header = ['id', 'title', 'keywords', 'genres', 'director', 'producer', 'compositor', 'actor_1', 'actor_2', 'actor_3']


def get_detail(movie):
    return {
        'id': movie['id'],
        'title': movie['title'].replace(',', ''),
        'keywords': ' '.join(str(k['name']) for k in movie['keywords']['keywords']),
        'genres': ' '.join(str(g['name']) for g in movie['genres']),
        'director': movie.get_crew('crew', 'Director'),
        'producer': movie.get_crew('crew', 'Producer'),
        'compositor': movie.get_crew('crew', 'Original Music Composer'),
        'actor_1': movie.get_cast('cast', 0),
        'actor_2': movie.get_cast('cast', 1),
        'actor_3': movie.get_cast('cast', 2),
    }


def main(file_path):
    try:
        df = pd.read_csv(file_path, names=header)
    except EmptyDataError:
        df = pd.DataFrame(columns=header)

    for page in range(1, 350):
        movies = Client().top(page=page)
        print(f'=> Page {page}')

        for item in movies:
            df = df.append(get_detail(item), ignore_index=True)

        df.to_csv(file_path)


if __name__ == '__main__':
    main('../data/movie.csv')
