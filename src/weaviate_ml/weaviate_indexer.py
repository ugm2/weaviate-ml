import weaviate
import weaviate.classes.config as wvc
import pandas as pd
from rich.progress import (
    Progress,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)


class WeaviateIndexer:
    def __init__(self, client=None):

        # Initialize the client, either passed from outside or create a new one
        self.client = None
        self.client = client or weaviate.connect_to_local()
        self.collection_name = "NewsArticle"

    def create_collection(self):
        if self.client.collections.exists(self.collection_name):
            self.client.collections.delete(self.collection_name)

        # Create a new collection
        self.client.collections.create(
            name=self.collection_name,
            properties=[
                wvc.Property(name="title", data_type=wvc.DataType.TEXT),
                wvc.Property(name="link", data_type=wvc.DataType.TEXT),
                wvc.Property(name="published", data_type=wvc.DataType.TEXT),
                wvc.Property(name="summary", data_type=wvc.DataType.TEXT),
            ],
            vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(
                model="text-embedding-3-small"
            ),
            generative_config=wvc.Configure.Generative.openai(
                model="gpt-4", max_tokens=256, temperature=0.2
            ),
        )

    def index_data(self, csv_path):
        df = pd.read_csv(csv_path)
        total_articles = len(df)

        with self.client.batch.dynamic() as batch:
            with Progress(
                TextColumn(
                    "[progress.description]{task.description} ({task.completed}/{task.total})"
                ),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(
                    "[cyan]Indexing articles",
                    total=total_articles,
                )
                for i, row in df.iterrows():
                    properties = {
                        "title": row["title"],
                        "link": row["link"],
                        "published": row["published"],
                        "summary": row["summary"],
                    }
                    batch.add_object(
                        collection=self.collection_name, properties=properties
                    )
                    progress.update(task, advance=1)
            batch.flush()  # Ensure all remaining data is sent

    def __del__(self):
        if self.client:
            self.client.close()
