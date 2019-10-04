import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer

from suggestore.clustering.generation.config import VOCABULARY, REPLACE


class Clustering:

    def __init__(self, export_dir='../data'):
        self.export_dir = export_dir

    @property
    def clean_data(self):
        df = pd.read_csv(f'{self.export_dir}/movie.csv', index_col=0)
        df.dropna(inplace=True)
        df.drop_duplicates(subset='id', inplace=True)

        return df

    def binary_data(self, export=False):
        df = self.clean_data
        df_binary = pd.DataFrame()
        df_binary['id'] = df['id']

        # Genres
        cv_genres = CountVectorizer()
        vector_genres = cv_genres.fit_transform(df['genres']).toarray()
        for counter, name in enumerate(cv_genres.get_feature_names()):
            df_binary[f'genre_{name}'] = vector_genres[:, counter]

        # Keywords
        for key, value in REPLACE.items():
            df['keywords'] = df.keywords.str.replace(key, value)

        cv_keyword = CountVectorizer(vocabulary=VOCABULARY)
        vector_keywords = cv_keyword.fit_transform(df['keywords']).toarray()
        for counter, name in enumerate(cv_keyword.get_feature_names()):
            df_binary[f'keywords_{name}'] = vector_keywords[:, counter]

        if export:
            df_binary.to_csv(f'{self.export_dir}/movie_binary.csv')

        return df_binary

    def process(self):
        df_binary = self.binary_data(False)
        uid = df_binary['id']
        df_binary.drop('id', axis=1, inplace=True)

        pca = PCA()
        pca.fit(df_binary)
        for index, score in zip(df_binary.columns.values, pca.components_[0]):
            print(f'{index} ==> {score}')

        pca = pca.transform(df_binary)
        predict = AffinityPropagation().fit_predict(pca)

        df_clustered = pd.DataFrame(data={'id': uid, 'cluster': predict})
        df_clustered.set_index('id', inplace=True)

        df_clustered.to_csv(f'{self.export_dir}/movie_clustered.csv')


if __name__ == '__main__':
    clustering = Clustering()
    clustering.process()
