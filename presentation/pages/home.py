import streamlit as st
from PIL import Image

col1, col2, col3 = st.columns((1, 4, 1))
with col2:
    st.image(Image.open("assets/img/home_logo.png"))

st.markdown("# Bem-vindo(a) ao Sistema Synapse!")
