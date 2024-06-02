import streamlit as st


def show(container):
    with container:
        st.title("Welcome to the Weaviate Search Engine")
        st.write(
            """
            This is a demo search engine using Weaviate and Streamlit.
            Use the navigation menu to explore the different sections.
        """
        )
