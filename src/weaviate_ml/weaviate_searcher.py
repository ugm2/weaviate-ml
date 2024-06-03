import weaviate


class WeaviateSearcher:
    def __init__(self, client=None, collection_name="NewsArticle"):
        self.client = client or weaviate.connect_to_local()
        self.collection_name = collection_name

    def search_and_respond(self, query, limit=5):
        response = self.client.collections.get(self.collection_name).generate.near_text(
            query=query,
            limit=limit,
            grouped_task=f"Given these articles, answer the following question '{query}' in a concise way:",
        )
        return response.generated, response.objects

    def __del__(self):
        self.client.close()
