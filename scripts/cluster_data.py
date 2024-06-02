import argparse
from clustering.text_clustering import TextClustering


def main():
    parser = argparse.ArgumentParser(
        description="Cluster text data and save the results to a new CSV file."
    )
    parser.add_argument(
        "--input_path",
        type=str,
        default="data/postings_reduced.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="data/postings_clustered.csv",
        help="Path to save the output CSV file with clusters.",
    )
    parser.add_argument(
        "--text_columns",
        type=str,
        nargs="+",
        default=["title", "description"],
        help="Columns containing text data to be clustered.",
    )
    parser.add_argument(
        "--num_clusters", type=int, default=10, help="Number of clusters (default: 10)."
    )

    args = parser.parse_args()

    clustering = TextClustering(num_clusters=args.num_clusters)
    clustering.run(args.input_path, args.output_path, args.text_columns)


if __name__ == "__main__":
    main()
