import streamlit as st

st.logo("assets/img/sidebar_logo.png", icon_image="assets/img/main_body_logo.png")

st.set_page_config(
    page_icon="assets/img/favicon.png",
)

app = st.navigation({
    "Início": [
        st.Page("presentation/pages/home.py", title="Bem-vindo(a)", icon=":material/home:")
    ],
})

app.run()
