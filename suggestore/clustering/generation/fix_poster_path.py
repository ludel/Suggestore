import pandas as pd

from suggestore.interfaces.client import Client

client = Client(delay=0, language="fr-FR")

if __name__ == '__main__':
    posters = []
    path_matrix = "../data/movie.csv"
    df = pd.read_csv(path_matrix, error_bad_lines=False)

    id_list = df['id'].tolist()

    for counter, _id in enumerate(id_list):
        posters.append(client.get_movie(_id).poster_path)
        print(f'{counter}/{len(id_list)}')

        df['poster_path'] = pd.Series(posters)
        df.to_csv('fixed_movies.csv')
