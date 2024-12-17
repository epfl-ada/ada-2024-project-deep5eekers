import os
from typing import List, Dict

import pandas as pd
import json
import re
from bs4 import BeautifulSoup
import requests
import wikipediaapi
import tqdm

from utils.utils import load_df_movies


"""
This file is dedicated to the adding IMBD rating to each movie, as well as parsing information about movie director's name and gender.

We can join the information from wikipedia, which is previously computed by parse_wikipedia.py

This way, for each wiki_id we have unique IMDB id

After that, we download IMDB data from the official IMDB website: https://developer.imdb.com/non-commercial-datasets/

- name.basics.tsv
- title.crew.tsv
- title.ratings.tsv

Joining this together, we have our information about each movie's rating and director's name.

However, there is still work to determine gender of each director, as it's not provided by IMDB or wikipedia.

We use data from IMDB description and wikipedia page and heuristics for that. 
"""

def get_imdb_id(wiki_id, wiki_to_imdb):
    tt = wiki_to_imdb.get(str(wiki_id), None)
    if tt is None:
        return None
    tt = str(tt)
    if len(tt) < 7:
        tt = '0' * (7 - len(tt)) + tt
    return 'tt' + tt


def determine_gender(desc):
    hes = re.findall(r'\bhe\b', desc.lower())
    shes = re.findall(r'\bshe\b', desc.lower())
    hers = re.findall(r'\bher\b', desc.lower())
    hiss = re.findall(r'\bhis\b', desc.lower())
    actor = re.findall(r'\bactor\b', desc.lower())
    actress = re.findall(r'\bactress\b', desc.lower())

    m_markers = hes + hiss + actor
    f_markers = shes + hers + actress

    if len(m_markers) == 0 and len(f_markers) == 0:
        return 'unknown'
    elif len(m_markers) > len(f_markers):
        return 'Male'
    elif len(m_markers) < len(f_markers):
        return 'Female'
    return 'unknown'


def get_wiki_page(name):
    user_agent = "GenderBot/1.0 (https://example.com; bot@example.com)"
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)
    return wiki_wiki.page(name)


def get_wiki_text(page):
    title = page.title.replace(" ", "_")
    wiki_raw_url = f"http://en.wikipedia.org/w/index.php?title={title}"

    response = requests.get(wiki_raw_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code} {wiki_raw_url}")

    soup = BeautifulSoup(response.content, "html.parser")
    paras = [str(paragraph.text) for paragraph in soup.find_all('p')]
    return ' '.join(paras)


def set_gender_label(imdb_id, males, females, unknowns, uname_to_gender):
    if imdb_id in males:
        return 'Male'
    if imdb_id in females:
        return 'Female'
    if imdb_id in uname_to_gender:
        return uname_to_gender[imdb_id]
    if imdb_id in unknowns:
        return 'unknown'


def extract_person_description(entities: List) -> Dict:
    print("In total to process: ", len(set(entities)))

    i = 0
    id_to_descr = {}

    for e in tqdm.tqdm(entities, total=len(entities)):
        name, idx = e

        if idx in id_to_descr:
            continue

        from bs4 import BeautifulSoup
        import requests

        # Example URL
        url = f'https://www.imdb.com/name/{idx}/'

        # Headers to avoid blocking
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        try:

            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Find all meta tags with name="description"
                meta_descriptions = soup.find_all("meta", attrs={"name": "description"})

                # Print content of each found meta tag
                contents = []
                for meta in meta_descriptions:
                    content = meta.get("content")
                    contents.append(content)
                id_to_descr[idx] = contents
            else:
                raise Exception(f"Status code: {response.status_code}")


        except:
            print(f"Failed to fetch page: ", name)

        i = i + 1
        if i % 10 == 0:
            print("Saving iteration", i)
            with open(os.path.join('..', 'person_description.json'), "w") as f:
                json.dump(id_to_descr, f)

    print("Saving end result")
    with open(os.path.join('..', 'person_description.json'), "w") as f:
        json.dump(id_to_descr, f)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

    file_path = os.path.join(data_dir, 'MovieSummaries')

    print("Loading datasets...")
    df_movie_metadata = load_df_movies(file_path)

    imdb = pd.read_csv(os.path.join(data_dir, 'title.ratings.tsv'), sep='\t')
    crew = pd.read_csv(os.path.join(data_dir, 'title.crew.tsv'), sep='\t')
    names = pd.read_csv(os.path.join(data_dir, 'name.basics.tsv'), sep='\t')

    with open('wiki_to_imdb.json', 'r') as f:
        wiki_to_imdb = json.load(f)

    print("Processing datasets...")
    df_movie_metadata['imdb_id'] = df_movie_metadata['wiki_movie_id'].apply(lambda x: get_imdb_id(x, wiki_to_imdb))
    df_movie_metadata = df_movie_metadata.merge(imdb, how='left', left_on='imdb_id', right_on='tconst')
    df_movie_metadata = df_movie_metadata.merge(crew, how='left', left_on='imdb_id', right_on='tconst')
    df_movie_metadata = df_movie_metadata.merge(
        names[['nconst', 'primaryName']], how='left', left_on='directors', right_on='nconst'
    )

    df_movie_metadata['directors_name'] = df_movie_metadata['primaryName']
    df_movie_metadata['directors_imdb_id'] = df_movie_metadata['nconst']
    df_movie_metadata.drop(columns=['primaryName', 'tconst_x', 'tconst_y', 'directors', 'nconst'], inplace=True)

    # Save data with director's names and ratings

    rated_csv_path = os.path.join(data_dir, 'MovieSummaries', 'rated.movie.metadata.tsv')

    df_movie_metadata = df_movie_metadata.applymap(
        lambda x: x.encode('utf-8', 'replace').decode('utf-8') if isinstance(x, str) else x
    )

    df_movie_metadata.to_csv(rated_csv_path, sep='\t', index=False, encoding='utf-8')

    # Extract person's description from IMDB

    entities = []
    for i, row in df_movie_metadata[['directors_name', 'directors_imdb_id']].iterrows():
        name, idx = row['directors_name'], row['directors_imdb_id']

        entities.append((name, idx))

    entities = set([e for e in entities if not pd.isnull(e[1])])

    # saves to ../person_description.json

    # Might take 11 hours, so we have commented this part and use precomputed file
    # extract_person_description(list(entities))

    with open(os.path.join('..', 'person_description.json')) as f:
        person_description = json.load(f)

    # Use person's descriptions to determine gender

    males, females, unknowns, equals = [], [], [], []

    for p, desc in person_description.items():
        desc = desc[0]
        gender = determine_gender(desc)
        if gender == 'Male':
            males.append(p)
        elif gender == 'Female':
            females.append(p)
        else:
            unknowns.append(p)

    print(f"Males: {len(males)}, Females: {len(females)}, Unknowns: {len(unknowns)}, Equals: {len(equals)}")

    df_movie_metadata['directors_gender'] = (df_movie_metadata['directors_imdb_id']
    .apply(
        lambda x: determine_gender(person_description[x][0]) if x in person_description else 'unknown'
    ))

    # Select subset of 10_000 movies and fill gender as much as possible for those
    top_movies = df_movie_metadata.sort_values(by='numVotes', ascending=False)[:10_000]

    uname_to_gender = {}
    unknown_df = top_movies[top_movies['directors_gender'] == 'unknown']

    for name, n_imdb in tqdm.tqdm(
            zip(unknown_df['directors_name'], unknown_df['directors_imdb_id']),
            total=len(unknown_df)
    ):
        page = get_wiki_page(name)
        try:
            wiki_text = get_wiki_text(page)
            uname_to_gender[n_imdb] = determine_gender(wiki_text)
        except:
            uname_to_gender[n_imdb] = "unknown"

    top_movies['directors_gender'] = top_movies['directors_imdb_id'].apply(
        lambda x: set_gender_label(x, males, females, unknowns, uname_to_gender)
    )

    print(top_movies['directors_gender'].value_counts())

    top_movies = top_movies.applymap(
        lambda x: x.encode('utf-8', 'replace').decode('utf-8') if isinstance(x, str) else x
    )

    top_movies_path = os.path.join(data_dir, 'MovieSummaries', 'top_rated.movie.metadata.tsv')
    top_movies.to_csv(top_movies_path, sep='\t', index=False, encoding='utf-8')


if __name__ == "__main__":
    main()
