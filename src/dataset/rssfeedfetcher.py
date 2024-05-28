import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


class RSSFeedFetcher:
    def __init__(self, query, start_date, end_date, delta_days=7):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.delta_days = delta_days
        self.articles = []

    def fetch_rss_feed(self, from_date, to_date):
        formatted_from_date = from_date.strftime("%Y-%m-%d")
        formatted_to_date = to_date.strftime("%Y-%m-%d")
        rss_url = f"https://news.google.com/rss/search?q={self.query}+after:{formatted_from_date}+before:{formatted_to_date}&hl=en&gl=US&ceid=US:en"

        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        articles = []
        for item in items:
            title = item.find("title").text if item.find("title") else ""
            link = item.find("link").text if item.find("link") else ""
            published = item.find("pubDate").text if item.find("pubDate") else ""
            summary_html = (
                item.find("description").text if item.find("description") else ""
            )
            summary = BeautifulSoup(summary_html, "html.parser").get_text()
            articles.append(
                {
                    "title": title,
                    "link": link,
                    "published": published,
                    "summary": summary,
                }
            )
        return articles

    def fetch_data_in_batches(self):
        current_date = self.start_date
        while current_date < self.end_date:
            next_date = current_date + timedelta(days=self.delta_days)
            batch_articles = self.fetch_rss_feed(current_date, next_date)
            self.articles.extend(batch_articles)
            current_date = next_date
        return self.articles

    def save_to_csv(self, filename):
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        df = pd.DataFrame(self.articles)
        df.to_csv(filepath, index=False)
        logger.info(
            f"{len(self.articles)} RSS feed articles collected and saved to {filepath}"
        )
