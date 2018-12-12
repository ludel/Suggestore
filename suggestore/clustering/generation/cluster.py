import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

df = pd.read_csv('../data/movie.csv', error_bad_lines=False)
df.dropna(inplace=True)
df.drop_duplicates(subset='title', inplace=True)

df_feature = pd.read_csv('../data/feature.csv', index_col=0)
df_feature.dropna(inplace=True)


pca = PCA()
pca.fit(df_feature)
for index, score in zip(df_feature.columns.values, pca.components_[0]):
    print(index, score)

pca = pca.transform(df_feature)
predict = KMeans(n_clusters=200).fit_predict(pca)

pd.DataFrame(data={'id': df['id'], 'cluster': predict, 'title': df['title']}).to_csv("../data/movie_clustered.csv")