import json
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA


def load_clustered_data(file_path):
    df = pd.read_csv(file_path)
    df["text_vector"] = df["text_vector"].apply(json.loads)
    return df


def preprocess_for_plot(df):
    # Use PCA to reduce the dimensions for plotting
    pca = PCA(n_components=2)
    text_vectors = df["text_vector"].tolist()
    pca_results = pca.fit_transform(text_vectors)
    df["pca_one"] = pca_results[:, 0]
    df["pca_two"] = pca_results[:, 1]
    return df


def show(container):
    with container:
        st.title("Job Postings Analysis")
        st.write("Analyze job openings related to machine learning or AI.")

        # Load clustered data
        df = load_clustered_data("data/postings_clustered.csv")

        # Assume that 'text_vector' column exists for PCA and plotting (if not, you need to add it during clustering)
        df = preprocess_for_plot(df)

        # Select Cluster
        st.subheader("Clustered Job Postings")
        cluster_selected = st.selectbox("Select Cluster", df["cluster_name"].unique())
        filtered_df = df[df["cluster_name"] == cluster_selected]
        st.write(filtered_df[["title", "description"]])

        # Plot Cluster Distribution
        st.subheader("Cluster Distribution")
        fig = px.pie(df, names="cluster_name", title="Cluster Distribution")
        st.plotly_chart(fig)

        # Plot Scatter Plot of Job Postings
        st.subheader("Job Postings Scatter Plot")
        fig = px.scatter(
            df,
            x="pca_one",
            y="pca_two",
            color="cluster_name",
            hover_data=["title", "company_name", "location"],
            title="Job Postings Clusters",
        )
        st.plotly_chart(fig)
