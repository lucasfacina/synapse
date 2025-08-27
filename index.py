import streamlit as st

st.logo("assets/img/sidebar_logo.png", icon_image="assets/img/main_body_logo.png")

st.set_page_config(
    page_icon="assets/img/favicon.png",
    page_title="Sistema Synapse",
)


def Page(filename, title, icon, url_path=None):
    return st.Page(f"presentation/pages/{filename}.py", title=title, icon=f":material/{icon}:", url_path=url_path)


app = st.navigation({
    "Início": [
        Page("home", "Bem-vindo(a)", "waving_hand"),
        Page("about", "Sobre", "info"),
    ]
})

app.run()
