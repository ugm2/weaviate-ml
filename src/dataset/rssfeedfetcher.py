import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import timedelta
import logging
from time import sleep
import random
from rich.progress import (
    Progress,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TextColumn,
    BarColumn,
)
from transformers import pipeline


logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


class RSSFeedFetcher:
    def __init__(self, query, start_date, end_date, delta_days=7):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.delta_days = delta_days
        self.articles = []
        self.summarization_pipeline = pipeline(
            "summarization", model="facebook/bart-large-cnn"
        )

    def fetch_rss_feed(self, from_date, to_date, total_batches, batch_index):
        formatted_from_date = from_date.strftime("%Y-%m-%d")
        formatted_to_date = to_date.strftime("%Y-%m-%d")
        rss_url = f"https://news.google.com/rss/search?q={self.query}+after:{formatted_from_date}+before:{formatted_to_date}&hl=en&gl=US&ceid=US:en"

        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        articles = []

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                f"[cyan]Fetching articles from '{formatted_from_date}' to '{formatted_to_date}'... Batch {batch_index + 1}/{total_batches}",
                total=len(items),
            )
            for item in items:
                title = item.find("title").text if item.find("title") else ""
                link = item.find("link").text if item.find("link") else ""
                published = item.find("pubDate").text if item.find("pubDate") else ""
                summary = self.extract_article_content(title, link)
                if summary is not None:
                    articles.append(
                        {
                            "title": title,
                            "link": link,
                            "published": published,
                            "summary": summary,
                        }
                    )
                progress.advance(task)
                sleep(random.uniform(1, 3))  # to avoid being blocked by the server
        return articles

    def extract_article_content(self, title, url):
        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            content = " ".join([para.get_text() for para in paragraphs[:5]])
            content = f"Title: {title}. Content: {content}"

            if len(content) < 130:
                return None

            summary = self.summarization_pipeline(
                content,
                max_length=130,
                min_length=30,
                do_sample=False,
            )

            return summary[0]["summary_text"]
        except Exception as e:
            logger.error(f"Failed to extract article content from {url}: {e}")
            return None

    def fetch_data_in_batches(self):
        current_date = self.start_date
        total_batches = (self.end_date - self.start_date).days // self.delta_days + 1
        batch_index = 0

        while current_date < self.end_date:
            next_date = current_date + timedelta(days=self.delta_days)
            batch_articles = self.fetch_rss_feed(
                current_date, next_date, total_batches, batch_index
            )
            self.articles.extend(batch_articles)
            current_date = next_date
            batch_index += 1
        return self.articles

    def save_to_csv(self, filename):
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        df = pd.DataFrame(self.articles)
        df.to_csv(filepath, index=False)
        logger.info(
            f"{len(self.articles)} RSS feed articles collected and saved to {filepath}"
        )
