import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import PCA

df = pd.read_csv('../data/movie.csv', error_bad_lines=True)
df.dropna(inplace=True)

df_feature = pd.read_csv('../data/movie_binary.csv', index_col=0)
df_feature.dropna(inplace=True)

pca = PCA()
pca.fit(df_feature)
for index, score in zip(df_feature.columns.values, pca.components_[0]):
    print(index, score)

pca = pca.transform(df_feature)
predict = AffinityPropagation().fit_predict(pca)

pd.DataFrame(data={'id': df['id'], 'cluster': predict, 'title': df['title']}).to_csv("../data/movie_clustered.csv")
