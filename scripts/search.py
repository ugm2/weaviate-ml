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
    args = parser.parse_args()

    # Search Weaviate and generate response
    searcher = WeaviateSearcher()
    answer, articles = searcher.search_and_respond(args.query, args.limit)

    print("Query:", args.query)
    print("Articles:")
    print(articles)
    print("Generated Response:")
    print(answer)


if __name__ == "__main__":
    main()
