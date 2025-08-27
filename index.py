import streamlit as st

app = st.navigation({
    "Início": [
        st.Page("presentation/pages/home.py", title="Bem-vindo(a)", icon=":material/home:")
    ],
})

app.run()
