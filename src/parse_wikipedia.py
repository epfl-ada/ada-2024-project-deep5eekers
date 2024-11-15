import bz2
import json
import re
import tqdm

from typing import Dict, List, Optional
from utils import load_df_movies

"""
This file is dedicated to the Wikipedia Dump Parsing

We have a set of Wiki Page IDs from CMU dataset.

We would like to scrap those wikipedia pages for further analysis.
The fastest solution is to work with wiki-dump.

Here are the steps:

1. Download wikipedia dump and index

2. Parse the index, extracting offsets of the main bz2 file for each page that we are interested in

3. Read pages from those offsets. We are seeking only the necessary offsets 
and reading file by chunks afterward, until all pages are read. 
"""


def process_index_file(index_source, article_ids) -> Dict[int, int]:
    """
    Returns dictionary which maps article_id to corresponding offset in the dump bz2 file
    """
    offsets_dict = {}
    try:
        index_filehandle = bz2.BZ2File(index_source)

        for line in index_filehandle:
            # Parse OFFSET:ID:TITLE structure
            offset = int(line.decode("utf-8").split(":")[0])
            article_id = int(line.decode("utf-8").split(":")[1])
            if article_id in article_ids:
                offsets_dict[article_id] = offset
    finally:
        index_filehandle.close()

    return offsets_dict


def process_wiki_dump(dump_path, offsets_to_read: List[int]) -> Dict[str, bytes]:
    id_to_content = {}

    # List of offsets to read
    sorted_offsets = list(sorted(offsets_to_read))
    with open(dump_path, 'rb') as bz2file:
        for i, offset in tqdm.tqdm(enumerate(sorted_offsets), total=len(sorted_offsets)):
            bz2file.seek(offset)  # Seek to the specific offset
            unzipper = bz2.BZ2Decompressor()
            found_ids = set()

            current_offset = offset
            content = b''

            # Continue to read chunks of data until all pages are read
            while len(found_ids) < len(offset_to_read_ids.get(offset, [])):

                # If we overlap to the next offset, no reason to continue
                if i < len(sorted_offsets) - 1:
                    next_of = sorted_offsets[i + 1]
                    if current_offset > next_of:
                        break

                # Read new chunk
                try:
                    block = bz2file.read(65536)
                    current_offset += 65536
                except Exception as e:
                    print(f"Error while reading: {e}")
                    break

                if not block:
                    # eof
                    break

                try:
                    content += unzipper.decompress(block)
                except Exception as e:
                    print(f"Error while decompressing: {e}")
                    break

                # Check if we have found all the required IDs in this content
                ids_to_check = set(offset_to_read_ids[offset]) - found_ids
                for article_id in ids_to_check:
                    id_mark = f"<id>{article_id}".encode()
                    id_inside = id_mark in content

                    if id_inside:
                        id_mark_content_idx = content.find(id_mark)
                        content_of_page = content[id_mark_content_idx:]

                        page_end = content_of_page.find(b'</page>')
                        if page_end != -1:
                            content_of_page = content_of_page[:page_end]
                            id_to_content[article_id] = content_of_page
                            found_ids.add(article_id)

            # Output if we haven't found some ids on this offset
            if len(found_ids) != len(offset_to_read_ids[offset]):
                print(f"Found {len(found_ids)} / {len(offset_to_read_ids[offset])} articles in offset {offset}")
    return id_to_content


def extract_imdb_patterns(text):
    """
    Extracts IMDb patterns from the given text.

    Args:
    text (str): The text to search within.

    Returns:
    list of str: A list of matched IMDb patterns.
    """
    pattern = r"\{\{IMDb[^\}]*\}\}"
    matches = re.findall(pattern, text)
    return matches


def parse_imdb_template(template: str) -> Optional[int]:
    if '|' not in template:
        return None

    for template_arg in template.split('|'):
        clean_arg = (
            template_arg.replace('}', '')
            .replace('tt', '')
            .replace('id=', '')
            .replace('id= ', '')
            .replace('id =', '')
            .replace('/', '')
            .strip()
        )
        if clean_arg.isdigit():
            return int(clean_arg)
    return None


if __name__ == '__main__':
    file_path = "../data/MovieSummaries"

    print("Dataframes creation starting for CMU datasets...")

    df_movie_metadata = load_df_movies(file_path)

    print("Dataframes creation for CMU datasets done.")

    my_ids = df_movie_metadata['wiki_movie_id'].tolist()

    # Compute offset mapping
    offsets_dict = process_index_file("../enwiki-20241101-pages-articles-multistream-index.txt.bz2",
                                      set(my_ids))

    offset_to_read_ids = {}  # offset -> [set of wiki pages to read that it contains]
    for read_id, of in offsets_dict.items():
        if of not in offset_to_read_ids:
            offset_to_read_ids[of] = []

        offset_to_read_ids[of].append(read_id)

    dump_path = '../enwiki-20241101-pages-articles-multistream.xml.bz2'

    # Processing wiki dump, reading only needed offsets, could take 10 minutes
    id_to_content = process_wiki_dump(dump_path, list(set(offsets_dict.values())))

    # We now have textual content of each movie page from wikipedia!
    with open("wiki_pages.json", "w") as f:
        json.dump(id_to_content, f)

    id_to_content_str = {i: c.decode() for i, c in id_to_content.items()}

    wiki_id_to_imdb_id = {}

    # We retrieve IMDb template information from the page
    for id, content in id_to_content_str.items():
        imdb_matches = extract_imdb_patterns(content)

        if not imdb_matches:
            continue

        tt = parse_imdb_template(imdb_matches[0])
        if tt is not None:
            wiki_id_to_imdb_id[id] = tt

    # We now have mapping of Wiki page ID to IMDb ID!
    with open("wiki_id_to_imdb_id.json", "w") as f:
        json.dump(wiki_id_to_imdb_id, f)
