import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("../clustering/data/movie.csv")
df_clean = pd.DataFrame()
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df.drop_duplicates(subset='id', inplace=True)

# date
df_clean['release_date'] = df['release_date'].map(lambda date: int(date[0:4]))

df_clean.loc[df_clean['release_date'] <= 1990, 'release_date'] = 0
df_clean.loc[df_clean['release_date'] > 1990, 'release_date'] = 1

# language
cv_language = CountVectorizer()
vector_language = cv_language.fit_transform(df['original_language']).toarray()
for index, name in enumerate(cv_language.get_feature_names()):
    df_clean[f"language_{name}"] = vector_language[:, index]

# actor
df['actor'] = df['actor_1'] + ' ' + df['actor_2'] + ' ' + df['actor_3']

cast = {'director': 50, 'writer': 25, 'compositor': 25, 'actor': 50}

for job, max_features in cast.items():
    cv = CountVectorizer(max_features=max_features)
    vector = cv.fit_transform(df[job]).toarray()
    for index, name in enumerate(cv.get_feature_names()):
        df_clean[f"{job}_{name}"] = vector[:, index]

df_clean.to_csv('data/movie_binary.csv')
