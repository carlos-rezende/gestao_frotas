import streamlit as st
from src.utils.multipage import MultiPage
from src.pages.home import home
from src.pages.rotas_page import show_route_page
from src.pages.historico_page import Historico
from src.pages.multas_page import multas
from src.pages.manutencao_page import manutencao
from src.pages.checklist_page import checklist
from src.pages.gps_tracking_page import gps

# Cria a aplicação multipage
app = MultiPage()

# Adiciona as páginas
app.add_page("Home", home)
app.add_page("Cálculo de Rotas", show_route_page)
app.add_page("Dados Históricos", Historico)
app.add_page("Multas", multas)
app.add_page("Manutenção", manutencao)
app.add_page("Checklist de Veículos", checklist)
app.add_page("GPS", gps)

# Executa a aplicação
app.run()
