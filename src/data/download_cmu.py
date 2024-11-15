import os
import urllib.request
import tarfile

def download_cmu():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    os.makedirs(data_dir, exist_ok=True)

    download_link = 'https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz'
    file_path = os.path.join(data_dir, 'MovieSummaries.tar.gz')

    # Download the file

    print(f"Downloading CMU to {file_path}")
    urllib.request.urlretrieve(download_link, file_path)

    # Unpack the file
    with tarfile.open(file_path) as tar:
        tar.extractall(path=data_dir)

    os.remove(file_path)


if __name__ == '__main__':
    download_cmu()
