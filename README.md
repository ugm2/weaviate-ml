# weaviate-ml

Weaviate's challenge project

## Setup

1. [Install Poetry](https://python-poetry.org/docs/#installing-with-pipx).

2. Install Python 3.10. I recommend using Pyenv to manage Python versions within a computer.

3. Run `poetry shell` to create the Poetry environment.

4. Install package with `poetry install --with dataset` (`dataset` if you want to recreate the dataset, but I don't recommend it since it took a lot of time).

5. **[OPTIONAL]** Run `python scripts/create_dataset.py` to create the dataset (it's already been created under `data/rss_feed_articles.csv`). By default searches for news related to Gaza (I wanted to make some visibility of this issue 😬).

6. Copy paste the `.env_samples` file into `.env` with the command `cp .env_samples .env` and add the value for `OPENAI_APIKEY` that I've provided.

7. Start Docker and run `docker-compose up -d` to start Weaviate local server.

8. Run `python scripts/index.py` to index the data. By default, it indexes the dataset we created `data/rss_feed_articles.csv`. It takes around 2 minutes.

9. Now you can jump into the frontend by running `python -m streamlit run app.py`.

10. Explore the UI.
