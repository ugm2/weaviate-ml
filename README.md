# weaviate-ml

Weaviate's challenge project

## Setup

1. [Install Poetry](https://python-poetry.org/docs/#installing-with-pipx).

2. Install package with `poetry install --with dataset` (`dataset` if you want to recreate the dataset).

3. Run `poetry shell` to get into the environment.

4. [OPTIONAL] Run `python scripts/create_dataset.py` to create the dataset (it's already been created under `data/rss_feed_articles.csv`). By default searches for news related to Gaza (I wanted to make some visibility of this issue 😬).
