import pandas as pd
import ast
import json
import requests

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
    df_movies['Movie_release_date'] = pd.to_datetime(df_movies['release_date'], errors='coerce')
    df_movies['genres'] = df_movies['genres'].apply(clean_column)
    df_movies = string_to_list(df_movies, 'genres')
    return df_movies


def load_df_summaries(path):
    df_summaries = pd.read_csv(f"{path}/plot_summaries.txt", sep='\t', header=None)
    df_summaries.columns = [
        'wiki_movie_id',
        'summary'
    ]
    return df_summaries


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

import requests

def get_wikipedia_data_by_id(page_id):
    url = "https://en.wikipedia.org/w/api.php"
    
    # Parameters for the API request
    params = {
        "action": "query",
        "pageids": page_id,
        "prop": "extracts|info",
        "explaintext": True,  # Extract plain text without HTML
        "inprop": "url",      # Include the URL in the response
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Retrieve data for the specific page
    page_data = data.get("query", {}).get("pages", {}).get(str(page_id))
    if not page_data or "missing" in page_data:
        print(f"Page with ID {page_id} does not exist.")
        return None
    
    # Get the full text extract and attempt to isolate the "Plot" section
    full_text = page_data.get("extract", "")
    plot_text = None
    
    if "== Plot ==" in full_text:
        plot_text = full_text.split("== Plot ==")[1]
        
        # Further split if there are additional sections after "Plot"
        if "==" in plot_text:
            plot_text = plot_text.split("==")[0].strip()
    else:
        # If no "Plot" section is found, fall back to using the full text as is
        plot_text = full_text
    
    movie_data = {
        "wiki_id": page_id,
        "title": page_data.get("title"),
        "plot": plot_text,
        "url": page_data.get("fullurl")
    }
    
    return movie_data
