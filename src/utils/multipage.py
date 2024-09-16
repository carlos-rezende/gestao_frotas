import streamlit as st


class MultiPage:
    def __init__(self):
        self.pages = {}

    def add_page(self, title, func):
        """Adiciona uma nova página à aplicação."""
        self.pages[title] = func

    def run(self):
        # Cria o menu na barra lateral
        page_title = st.sidebar.selectbox(
            'Menu de Navegação', list(self.pages.keys()))
        # Executa a função da página selecionada
        self.pages[page_title]()
