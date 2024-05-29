import argparse
from weaviate_ml.weaviate_indexer import WeaviateIndexer


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Index data into Weaviate")
    parser.add_argument(
        "--csv_path",
        type=str,
        required=True,
        help="Path to the CSV file containing the data to index",
    )
    args = parser.parse_args()

    # Setup Weaviate and index data
    indexer = WeaviateIndexer()
    indexer.create_collection()
    indexer.index_data(args.csv_path)

    print("Data indexing complete.")


if __name__ == "__main__":
    main()
