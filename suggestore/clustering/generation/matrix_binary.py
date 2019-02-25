import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("../data/movie.csv")
df_clean = pd.DataFrame()
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df.drop_duplicates(subset='id', inplace=True)

# Genres
cv_genres = CountVectorizer()
vector_genres = cv_genres.fit_transform(df['genres']).toarray()
for counter, name in enumerate(cv_genres.get_feature_names()):
    df_clean[f"genre_{name}"] = vector_genres[:, counter]

# Keywords
voc = ['adultery', 'aftercreditsstinger', 'airplane', 'alien', 'assassin', 'biography', 'horror', 'mafia', 'california',
       'christmas', 'cia', 'corruption', 'dc_comics', 'death', 'detective', 'space_travel', 'dream', 'drugs',
       'dying_and_death', 'dystopia', 'escape', 'experiment', 'virtual_reality', 'secret_identity', 'family', 'fight',
       'friendship', 'future', 'gangster', 'gore', 'high_school', 'hitman', 'holiday', 'hostage', 'investigation',
       'journalist', 'kidnapping', 'lawyer', 'london_england', 'magical_creature', 'los_angeles', 'loss_of_loved_one',
       'love', 'love_of_one', 'magic', 'marriage', 'martial_arts', 'monster', 'murder', 'musical', 'nazi', 'new_york',
       'parent_child_relationship', 'paris_france', 'party', 'police', 'prison', 'prostitute', 'psychopath', 'rape',
       'rescue', 'revenge', 'robbery', 'post_apocalyptic', 'secret', 'serial_killer', 'sex', 'sibling_relationship',
       'small_town', 'sport', 'spy', 'suicide', 'superhero', 'supernatural', 'suspense', 'teenager', 'time_travel',
       'undercover', 'usa', 'vampire', 'violence', 'wedding', 'wife_husband_relationship', 'witch', 'world_war',
       'zombie', 'moon']

df['keywords'] = df.keywords.str.replace("elves", "magical_creature")
df['keywords'] = df.keywords.str.replace("dwarf", "magical_creature")
df['keywords'] = df.keywords.str.replace("orcs", "magical_creature")
df['keywords'] = df.keywords.str.replace("based_on_comic", "superhero")
df['keywords'] = df.keywords.str.replace("hero", "superhero")
df['keywords'] = df.keywords.str.replace("super_power", "superhero")
df['keywords'] = df.keywords.str.replace("fbi", "cia")
df['keywords'] = df.keywords.str.replace("new_york_city", "new_york")
df['keywords'] = df.keywords.str.replace("manhattan_new_york_city", "new_york")
df['keywords'] = df.keywords.str.replace("dream_world", "dream")
df['keywords'] = df.keywords.str.replace("world_war_ii", "world_war")
df['keywords'] = df.keywords.str.replace("world_war_i", "world_war")
df['keywords'] = df.keywords.str.replace("-", "_")

cv_keyword = CountVectorizer(vocabulary=voc)
vector_keywords = cv_keyword.fit_transform(df['keywords']).toarray()
for counter, name in enumerate(cv_keyword.get_feature_names()):
    df_clean[f"keywords_{name}"] = vector_keywords[:, counter]

df_clean.to_csv('../data/movie_binary.csv')
