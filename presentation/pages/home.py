import streamlit as st
from PIL import Image

col_left, col_middle, col_right = st.columns((1, 4, 1))
with col_middle:
    st.image(Image.open("assets/img/home_logo.png"))

st.markdown("# Bem-vindo(a) ao Sistema Synapse!")
