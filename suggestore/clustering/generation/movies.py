import pandas as pd
from pandas.errors import EmptyDataError

from suggestore.retriever.client import Client

header = ['id', 'title', 'budget', 'keywords', 'genres', 'release_date', 'original_language', 'crew',
          'cast', 'runtime', 'vote_average', 'vote_count', 'poster_path']


def get_detail(movie):
    return {
        'id': movie['id'],
        'title': movie['title'].replace(',', ''),
        'keywords': ' '.join(str(k['id']) for k in movie['keywords']['keywords']),
        'genres': ' '.join(str(g['id']) for g in movie['genres']),
        'release_date': movie['release_date'],
        'original_language': movie['original_language'],
        'directing': '',
        'cast': ' '.join(c['id'] for c in movie['credits']['cast']),
        'runtime': movie['runtime'],
        'vote_average': movie['vote_average'],
        'vote_count': movie['vote_count'],
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
