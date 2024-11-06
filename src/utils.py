import pandas as pd
import ast
import json

def clean_column(dict_string):
    try:
        parsed_dict = ast.literal_eval(dict_string)
        return ', '.join(parsed_dict.values())  # Join all names into a single string
    except (ValueError, SyntaxError):
        return dict_string  # Return the string as it is if parsing fails
    
def string_to_list(df, column):
    """ Turn the column specified of the df from a string to a list """
    df[column] = df[column].str.split(', ')
    return df

def string_to_dict(df, column):
    """ Turn the column specified of the df from a string to a dictionary and replace the dictionary column 
    with several columns with the keys of the dictionary """
    df[column] = df[column].apply(json.loads)
    keys = list(df[column][0].keys())

    for key in keys:
        df[key] = df[column].apply(lambda x: x[key])

    df = df.drop(columns = column)
    return df


def load_df_movies(path):
    df_movies = pd.read_csv(f"{path}/movie.metadata.tsv", sep='\t', header=None)
    df_movies.columns = [
        'wiki_movie_id',
        'freebase_movie_id',
        'title',
        'release_date',
        'box_office',
        'runtime',
        'languages',
        'countries',
        'genres'
    ]

    df_movies['languages'] = df_movies['languages'].apply(clean_column)
    df_movies['countries'] = df_movies['countries'].apply(clean_column)
    df_movies['genres'] = df_movies['genres'].apply(clean_column)
    df_movies = string_to_list(df_movies, 'genres')
    return df_movies


def load_df_characters(path):
    df_characters = pd.read_csv(f"{path}/character.metadata.tsv", sep='\t', header=None)
    df_characters.columns = [
        'wiki_movie_id',
        'freebase_movie_id',
        'release_date',
        'character_name',
        'birth_date',
        'gender',
        'height',
        'ethnicity',
        'actor_name',
        'age_at_release',
        'freebase_map_id',
        'freebase_character_id',
        'freebase_actor_id'
    ]
    return df_characters


def load_df_character_clusters(path):
    df_clusters = pd.read_table(f"{path}/tvtropes.clusters.txt", sep='\t', header=None)
    df_clusters.columns = ['cluster','dictionary']
    df_clusters = string_to_dict(df_clusters, 'dictionary')
    df_clusters = df_clusters.rename(
        columns={
            "cluster": "cluster",
            "char": "character_name",
            "movie": "movie_title",
            "id": "freebase_map_id",
            "actor": "actor_name",
        }
    )
    return df_clusters

