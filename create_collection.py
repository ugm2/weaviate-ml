import os
import certifi
import weaviate
import weaviate.classes.config as wvc
from weaviate.classes.query import MetadataQuery
import pandas as pd
from rich import print


def setup_weaviate():
    # Ensure SSL_CERT_FILE is set
    os.environ["SSL_CERT_FILE"] = certifi.where()

    # Connect to the local Weaviate instance running in Docker
    client = weaviate.connect_to_local()
    try:
        collection_name = "NewsArticle"

        # Delete the collection if it exists
        if client.collections.exists(collection_name):
            client.collections.delete(collection_name)

        # Create a new collection
        client.collections.create(
            name=collection_name,
            properties=[
                wvc.Property(name="title", data_type=wvc.DataType.TEXT),
                wvc.Property(name="link", data_type=wvc.DataType.TEXT),
                wvc.Property(name="published", data_type=wvc.DataType.TEXT),
                wvc.Property(name="summary", data_type=wvc.DataType.TEXT),
            ],
            vectorizer_config=wvc.Configure.Vectorizer.text2vec_contextionary(),
        )

        # Load data
        df = pd.read_csv("data/rss_feed_articles.csv")

        # Index data
        print(type(client.batch))
        with client.batch.dynamic() as batch:
            for i, row in df.iterrows():
                properties = {
                    "title": row["title"],
                    "link": row["link"],
                    "published": row["published"],
                    "summary": row["summary"],
                }
                batch.add_object(collection=collection_name, properties=properties)
                if i % 100 == 0:
                    print(f"Indexed {i} articles")
            batch.flush()  # Ensure all remaining data is sent
    except Exception as e:
        print(e)
        client.close()
    return client


def retrieve_articles(client, query_text, limit=10):
    collection = client.collections.get("NewsArticle")
    response = collection.query.near_text(
        query=query_text, limit=limit, return_metadata=MetadataQuery(distance=True)
    )
    return response.objects


def main():
    # Setup Weaviate and index data
    client = setup_weaviate()

    try:
        # Example usage
        query_text = "Gaza conflict"
        articles = retrieve_articles(client, query_text)

        print(articles)

        # # Combine summaries for context
        # context = " ".join([article["properties"]["summary"] for article in articles])

        # # Use a local LLM (like GPT-2) for generation
        # from transformers import pipeline

        # generator = pipeline("text-generation", model="gpt-2")

        # def generate_response(context):
        #     prompt = f"Context: {context}\nResponse:"
        #     response = generator(prompt, max_length=100, num_return_sequences=1)
        #     return response[0]["generated_text"]

        # response = generate_response(context)

        # print("Generated Response:")
        # print(response)
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == "__main__":
    main()
