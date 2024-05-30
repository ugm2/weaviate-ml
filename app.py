import streamlit as st
from frontend.pages import home, search

# Configure the app
st.set_page_config(
    page_title="Weaviate Search Engine",
    page_icon="src/frontend/assets/weaviate-logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image("src/frontend/assets/weaviate-nav-logo-light.png")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Search"])

# Render the selected page
if page == "Home":
    home.show()
elif page == "Search":
    search.show()
