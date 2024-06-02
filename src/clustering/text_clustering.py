import json
import pandas as pd
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer,
    ENGLISH_STOP_WORDS,
)
from sklearn.cluster import KMeans
from collections import Counter


class TextClustering:
    def __init__(self, num_clusters=10):
        self.num_clusters = num_clusters
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.kmeans = KMeans(n_clusters=num_clusters, random_state=0)

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def preprocess_data(self, df, text_columns):
        df = df.dropna(subset=text_columns)
        df["text"] = df[text_columns].agg(" ".join, axis=1)
        df["text"] = df["text"].str.lower()
        df["text"] = df["text"].apply(
            lambda x: " ".join(
                [word for word in x.split() if word not in ENGLISH_STOP_WORDS]
            )
        )
        return df

    def vectorize_text(self, df):
        X = self.vectorizer.fit_transform(df["text"])
        return X

    def cluster_data(self, X):
        self.kmeans.fit(X)
        return self.kmeans.labels_

    def extract_common_keywords(self, df, num_keywords=5):
        count_vectorizer = CountVectorizer(stop_words="english")
        counts = count_vectorizer.fit_transform(df["text"])
        words = count_vectorizer.get_feature_names_out()
        total_counts = counts.sum(axis=0).A1
        word_freq = dict(zip(words, total_counts))
        common_words = Counter(word_freq).most_common(num_keywords)
        return [word for word, freq in common_words]

    def generate_cluster_names(self, df, num_keywords=5):
        cluster_names = []
        for cluster in range(self.num_clusters):
            clusters = df[df["cluster"] == cluster]
            common_keywords = self.extract_common_keywords(clusters, num_keywords)
            cluster_name = " ".join(common_keywords)
            cluster_names.append(cluster_name)
        return cluster_names

    def save_clusters(self, df, X, output_path, cluster_names):
        df["text_vector"] = list(X.toarray())
        df["text_vector"] = df["text_vector"].apply(lambda x: json.dumps(x.tolist()))
        df["cluster_name"] = df["cluster"].map(
            {i: name for i, name in enumerate(cluster_names)}
        )
        df.to_csv(output_path, index=False)

    def run(self, input_path, output_path, text_columns):
        df = self.load_data(input_path)
        df = self.preprocess_data(df, text_columns)
        X = self.vectorize_text(df)
        clusters = self.cluster_data(X)
        df["cluster"] = clusters
        cluster_names = self.generate_cluster_names(df)
        self.save_clusters(df, X, output_path, cluster_names)
