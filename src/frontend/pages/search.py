import streamlit as st
from weaviate_ml.weaviate_searcher import WeaviateSearcher


@st.cache_data()
def search_and_respond(query, limit=5):
    answer, articles = st.session_state.searcher.search_and_respond(query, limit)
    return_articles = []
    for article in articles:
        article.uuid = str(article.uuid)
        return_articles.append(article)
    return answer, articles


def show(container):
    with container:
        st.title("Search Articles")
        st.write(
            "Enter a query to search through articles. You can also select an example query from the dropdown below:"
        )

        examples = [
            "What is happening between Palestina and Israel?",
            "What is EEUU's position in this conflict?",
            "How is U.N. dealing with this situation?",
            "Who is Itamar Ben-Gvir?",
        ]

        selected_example = st.selectbox("Choose an example query", examples, index=0)

        if "results" not in st.session_state:
            st.session_state.results = None

        query = st.text_input(
            "Or type your own query here:",
            selected_example,
            placeholder="Type your search query here...",
        )

        limit = st.slider("Number of results", 1, 5, 5)

        if st.button("Search"):

            if query:
                st.session_state.searcher = (
                    WeaviateSearcher()
                    if not st.session_state.searcher
                    else st.session_state.searcher
                )

                answer, articles = search_and_respond(query, limit)

                # Store the results in session state
                st.session_state.results = {"answer": answer, "articles": articles}
            else:
                st.error("Please enter a query.")
                st.session_state.results = None

        if st.session_state.results:
            st.subheader("Answer")
            st.write(st.session_state.results["answer"])

            st.subheader("Articles")
            for article in st.session_state.results["articles"]:
                st.write(f"**{article.properties['title']}**")
                st.markdown(f'`{article.properties["published"]}`')
                st.link_button("Go to link 🔗", article.properties["link"])
                st.write(article.properties["summary"])
                st.write("---")
