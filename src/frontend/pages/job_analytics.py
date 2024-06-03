import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from clustering.text_clustering import TextClustering


def run_clustering(input_path, output_path, text_columns, num_clusters):
    clustering = TextClustering(num_clusters=num_clusters)
    clustering.run(input_path, output_path, text_columns)


def load_clustered_data(file_path):
    df = pd.read_csv(file_path)
    df["text_vector"] = df["text_vector"].apply(json.loads)
    return df


def preprocess_for_plot(df):
    pca = PCA(n_components=3)
    text_vectors = df["text_vector"].tolist()
    pca_results = pca.fit_transform(text_vectors)
    df["pca_one"] = pca_results[:, 0]
    df["pca_two"] = pca_results[:, 1]
    df["pca_three"] = pca_results[:, 2]
    return df


def show(container):
    with container:
        st.title("Job Postings Analysis")
        st.write("Analyze job openings related to machine learning or AI.")

        st.subheader("Upload Dataset")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            input_path = "data/uploaded_postings.csv"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        else:
            input_path = "data/postings_reduced.csv"

        st.subheader("Cluster Settings")
        num_clusters = st.number_input(
            "Number of clusters", min_value=2, max_value=100, value=10
        )
        if st.button("Run Clustering"):
            output_path = "data/postings_clustered.csv"
            run_clustering(
                input_path, output_path, ["title", "description"], num_clusters
            )
            st.success(f"Clustering completed. Results saved to {output_path}")

        st.subheader("Load Clustered Data")
        clustered_data_file = st.text_input(
            "Path to clustered data file", "data/postings_clustered.csv"
        )
        if not os.path.exists(clustered_data_file):
            st.warning(
                "The specified file does not exist. Please run the clustering first."
            )
            return

        if st.button("Load Data"):
            df = load_clustered_data(clustered_data_file)
            df = preprocess_for_plot(df)
            st.session_state["df"] = df
            st.success("Data loaded and processed successfully.")

        if "df" in st.session_state:
            df = st.session_state["df"]

            st.subheader("Clustered Job Postings")
            cluster_selected = st.selectbox(
                "Select Cluster", df["cluster_name"].unique()
            )
            filtered_df = df[df["cluster_name"] == cluster_selected]
            st.write(filtered_df[["title", "description"]])

            st.subheader("Cluster Distribution")
            fig = px.pie(df, names="cluster_name", title="Cluster Distribution")
            st.plotly_chart(fig)

            st.subheader("Job Postings Scatter Plot (3D)")
            fig = px.scatter_3d(
                df,
                x="pca_one",
                y="pca_two",
                z="pca_three",
                color="cluster_name",
                hover_data=["title", "company_name", "location"],
                title="Job Postings Clusters (3D)",
                width=4000,
                height=1200,
            )
            fig.update_layout(scene=dict(camera=dict(eye=dict(x=1.00, y=1.00, z=1.00))))
            st.plotly_chart(fig)
