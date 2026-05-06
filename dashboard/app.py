from utils.db import load_data

import streamlit as st

# Main App Flow
def main():
    st.set_page_config(page_title="Taiwan Housing Dashboard")
    st.title("🏠 Taiwan Housing Dashboard")

    page = st.sidebar.selectbox(
        "Navigation",
        ['Overview', 'District Analysis', 'Trends', 'Data Explorer', 'ML Lab']
    )

    if page == 'Overview':
        from views import overview
        overview.app()

    elif page == 'District Analysis':
        from views import district
        district.app()

    elif page == 'Trends':
        from views import trends
        trends.app()

    elif page == 'Data Explorer':
        from views import data_explorer
        data_explorer.app()

    elif page == 'ML Lab':
        from views import ml_lab
        ml_lab.app()

if __name__ == "__main__":
    main()