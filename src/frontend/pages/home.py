import streamlit as st


def show(container):
    with container:
        st.title("Welcome to the Weaviate Search Engine")
        
        st.markdown("""
            **Explore the capabilities of Weaviate with this demo search engine.**
            - **Advanced Search Capabilities**: Find exactly what you're looking for with powerful search features.
            - **Job Analytics**: Gain insights into the current job market for ML and AI roles.
        """)
        
        st.info("Use the navigation menu on the left to explore different sections.")
        st.markdown("---")
