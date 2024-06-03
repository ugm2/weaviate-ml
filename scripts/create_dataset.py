from dataset.rssfeedfetcher import RSSFeedFetcher
import argparse
from datetime import datetime


def main(query, start_date, end_date, delta_days, output_file):
    fetcher = RSSFeedFetcher(query, start_date, end_date, delta_days)
    fetcher.fetch_data_in_batches()
    fetcher.save_to_csv(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch news articles from Google News RSS feed"
    )
    parser.add_argument(
        "--query",
        type=str,
        default="Gaza OR Palestine OR Israel OR Middle East",
        help="Search query (default: 'Gaza OR Palestine OR Israel OR Middle East')",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default="2023-05-27",
        help="Start date (YYYY-MM-DD) (default: 2023-01-01)",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default="2024-05-27",
        help="End date (YYYY-MM-DD) (default: 2024-05-27)",
    )
    parser.add_argument(
        "--delta_days",
        type=int,
        default=7,
        help="Number of days per batch (default: 7)",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="data/rss_feed_articles.csv",
        help="Output CSV file name (default: rss_feed_articles.csv)",
    )

    args = parser.parse_args()

    # Convert date strings to datetime objects
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    main(args.query, start_date, end_date, args.delta_days, args.output_file)
