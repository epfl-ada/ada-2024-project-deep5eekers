#%%
import pandas as pd
import json
#%%
from utils.utils import load_df_movies

file_path = "../data/MovieSummaries"

print("Dataframes creation starting for CMU datasets...")

df_movie_metadata = load_df_movies(file_path)

print("Dataframes creation for CMU datasets done.")
#%%

#%%
imdb = pd.read_csv('../data/title.ratings.tsv', sep='\t')
#%%
imdb.head()
#%%
with open('wiki_to_imdb.json', 'r') as f:
    wiki_to_imdb = json.load(f)
#%%

#%%
def get_imdb_id(wiki_id):
    tt = wiki_to_imdb.get(str(wiki_id), None)
    if tt is None:
        return None
    tt = str(tt)
    if len(tt) < 7:
        tt = '0' * (7 - len(tt)) + tt
    return 'tt' + tt
#%%
imdb[imdb['tconst'] == get_imdb_id('193874')]
#%%
df_movie_metadata['imdb_id'] = df_movie_metadata['wiki_movie_id'].apply(get_imdb_id)
#%%
df_movie_metadata['imdb_id'].head()
#%%
df_movie_metadata = df_movie_metadata.merge(imdb, how='left', left_on='imdb_id', right_on='tconst')
#%%
df_movie_metadata.sort_values(by='numVotes', ascending=False)[:10]
#%%
crew = pd.read_csv('../data/title.crew.tsv', sep='\t')
#%%

#%%
df_movie_metadata = df_movie_metadata.merge(crew, how='left', left_on='imdb_id', right_on='tconst')
#%%
df_movie_metadata.sort_values(by='numVotes', ascending=False)[:10]

#%%
names = pd.read_csv('../data/name.basics.tsv', sep='\t')
#%%
names
#%%
# Merge df_movie_metadata with names DataFrame
df_movie_metadata = df_movie_metadata.merge(
    names[['nconst', 'primaryName']],
    how='left',
    left_on='directors',
    right_on='nconst'
)

# Replace the director identifier with the actual director's name
df_movie_metadata['directors_name'] = df_movie_metadata['primaryName']  # Keep both nconst and name

# Drop unnecessary columns except 'nconst'
df_movie_metadata['directors_imdb_id'] = df_movie_metadata['nconst']

df_movie_metadata.drop(columns=['primaryName', 'tconst_x', 'tconst_y', 'directors', 'nconst'], inplace=True)



# Display the result to verify
df_movie_metadata.head()

#%%

#%%
df_movie_metadata.sort_values(by='numVotes', ascending=False)[:20]
#%%
dir_names = set(df_movie_metadata['directors_name'][df_movie_metadata['directors_name'].notna()])

print(len(dir_names))
#%%
# import wikipediaapi
#
# def get_wiki_page(name):
#     # Initialize the Wikipedia API object for the English language
#     user_agent = "GenderBot/1.0 (https://example.com; bot@example.com)"
#     wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)
#
#     # Get the page for the person
#     page = wiki_wiki.page(name)
#
#
#     return page
#
# # Example usage
# name = "Ridley Scott"
# page = get_wiki_page(name)
#

#%%

#%%
# from bs4 import BeautifulSoup
# import requests
#
# def get_occupations(page):
#     title = page.title.replace(" ", "_")
#     wiki_raw_url = "http://%s.wikipedia.org/w/index.php?title=%s" % ('en', title)
#
#     response = requests.get(wiki_raw_url)
#
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch page: {response.status_code} {wiki_raw_url}")
#
#
#     soup = BeautifulSoup(response.content, "html")
#
#     infobox = soup.find("table", class_="infobox")
#
#     if infobox:
#         # Iterate through each table row
#         for tr in infobox.find_all("tr"):
#             th = tr.find("th")
#             td = tr.find("td")
#             if th and td:
#                 # Check if the row corresponds to "Occupation" or "Occupations"
#                 if "Occupation" in th.text.strip():
#                     # Print the raw text from the cell
#                     # print("Raw Occupation Data:", td.text.strip())
#
#                     # Extract occupations
#                     if td.find_all("li"):  # If there are list items
#                         occupations = [li.text.strip() for li in td.find_all("li")]
#                     else:  # Fallback for plain text
#                         occupations = [td.text.strip()]
#
#                     # Print the cleaned occupations list
#                     return occupations
#     else:
#         return []
#%%
import tqdm
import json

records = []

id_to_descr = {}

entities = []
for i, row in tqdm.tqdm(df_movie_metadata[['directors_name', 'directors_imdb_id']].iterrows(), total=len(df_movie_metadata)):
    name, idx = row['directors_name'], row['directors_imdb_id']

    entities.append((name, idx))

entities = set([e for e in entities if not pd.isnull(e[1])])

i = 0

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
    if i % 100 == 0:
        print("Saving iteration", i)
        with open("person_description.json", "w") as f:
            json.dump(id_to_descr, f)
#%%
# from bs4 import BeautifulSoup
# import requests
#
# # Example URL
# url = 'https://www.imdb.com/name/nm0001068/'
#
# # Headers to avoid blocking
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }
#
# response = requests.get(url, headers=headers)
#
# if response.status_code == 200:
#     # Parse the HTML content
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     # Find all meta tags with name="description"
#     meta_descriptions = soup.find_all("meta", attrs={"name": "description"})
#
#     # Print content of each found meta tag
#     for meta in meta_descriptions:
#         content = meta.get("content")
#         print("Meta Description:", content)
# else:
#     print(f"Failed to fetch page: {response.status_code}")

#%%
