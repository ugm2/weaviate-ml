import weaviate
from weaviate.classes.query import MetadataQuery
from transformers import pipeline


class WeaviateSearcher:
    def __init__(
        self,
        model_id="deepset/roberta-base-squad2",
        generative_field="summary",
        client=None,
    ):
        # Initialize the client, either passed from outside or create a new one
        self.client = client or weaviate.connect_to_local()
        # I used the QnA transformer pipeline because Weaviate's V4 for QnA is not supported yet
        self.reader = pipeline("question-answering", model=model_id)
        self.generative_field = generative_field

    def retrieve_articles(self, query, limit=10):
        collection = self.client.collections.get("NewsArticle")
        response = collection.query.hybrid(
            query=query, limit=limit, return_metadata=MetadataQuery(distance=True)
        )
        return response.objects

    def generate_response(self, query, context):
        inputs = {"question": query, "context": context}
        response = self.reader(inputs)
        return response["answer"]

    def rag_response(self, query, limit=10):
        articles = self.retrieve_articles(query, limit)
        context = " ".join(
            [article.properties[self.generative_field] for article in articles]
        )
        answer = self.generate_response(query, context)
        return answer, articles

    def __del__(self):
        # Close the client when the object is deleted
        self.client.close()
