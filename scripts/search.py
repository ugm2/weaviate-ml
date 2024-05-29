import argparse
from weaviate_ml.weaviate_searcher import WeaviateSearcher
from rich import print


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Search data in Weaviate and generate a response"
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Text to search for in the Weaviate instance",
    )
    parser.add_argument(
        "--limit", type=int, default=5, help="Number of search results to return"
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default="deepset/roberta-base-squad2",
        help="ID of the model to use for generation",
    )
    parser.add_argument(
        "--generative_field",
        type=str,
        default="summary",
        help="Field to use for the generative part",
    )
    args = parser.parse_args()

    # Search Weaviate and generate response
    searcher = WeaviateSearcher(
        model_id=args.model_id, generative_field=args.generative_field
    )
    answer, articles = searcher.rag_response(args.query, args.limit)

    print("Query:", args.query)
    print("Articles:")
    print(articles)
    print("Generated Response:")
    print(answer)


if __name__ == "__main__":
    main()
