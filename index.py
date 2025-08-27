import streamlit as st

home_page = st.Page("presentation/pages/home.py", title="Início", icon="🏠")

pg = st.navigation([home_page])

pg.run()
