import streamlit as st
from frontend.pages import home, search, job_analytics
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Weaviate Search Engine",
    page_icon="src/frontend/assets/weaviate-logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = {
    "Introduction": (home, "house-fill"),
    "Search": (search, "search"),
    "Job Analytics": (job_analytics, "files"),
}

session_state_variables = {"searcher": None}

# Initialization of session state
for key, value in session_state_variables.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.sidebar.image("src/frontend/assets/weaviate-nav-logo-light.png")

main_page = st.container()

navigation = st.sidebar.container()

with navigation:

    selected_page = option_menu(
        menu_title=None,
        options=list(pages.keys()),
        icons=[f[1] for f in pages.values()],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"border": "2px solid #818494"},
            "icon": {"font-size": "22px"},
            "nav-link": {"font-size": "15px", "text-align": "left"},
        },
    )
pages[selected_page][0].show(main_page)
