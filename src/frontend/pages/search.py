import streamlit as st
from weaviate_ml.weaviate_searcher import WeaviateSearcher


def show():
    st.title("Search Articles")
    st.write("Enter a query to search through articles.")

    # Initialize session state for query and results
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "results" not in st.session_state:
        st.session_state.results = None

    query = st.text_input("Query", st.session_state.query)
    limit = st.slider("Number of results", 1, 20, 10)

    if st.button("Search"):
        if query:
            searcher = WeaviateSearcher()
            answer, articles = searcher.rag_response(query, limit)

            # Store the results in session state
            st.session_state.query = query
            st.session_state.results = {"answer": answer, "articles": articles}
        else:
            st.error("Please enter a query.")
            st.session_state.query = ""
            st.session_state.results = None

    if st.session_state.results:
        st.subheader("Answer")
        st.write(st.session_state.results["answer"])

        st.subheader("Articles")
        for article in st.session_state.results["articles"]:
            st.write(f"**{article.properties['title']}**")
            st.write(article.properties["summary"])
            st.write("---")
