import streamlit as st
import pydeck as pdk
import pandas as pd
from src.services.gps_service import GPSService

# Instanciar o serviço GPS
gps_service = GPSService()

# Função para obter dados dos veículos


@st.cache_data
def get_vehicle_data(locadora_name):
    if locadora_name == "BRT Rio":
        return gps_service.get_brt_vehicles_in_motion(gps_service.locadoras[locadora_name]['api_url'])
    return []


def gps():
    st.title("Monitoramento da Frota em Tempo Real")

    # Selecionar a locadora
    locadora_name = st.selectbox(
        "Selecione a Locadora:", list(gps_service.locadoras.keys()))

    # URL do ícone público
    icon_url = "https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_red.png"

    # Botão para atualizar a localização
    if st.button("Atualizar Localização"):
        vehicle_data = get_vehicle_data(locadora_name)

        if vehicle_data:
            vehicle_list = [
                {
                    "Placa": vehicle["placa"],
                    "Velocidade": vehicle["velocidade"],
                    "Latitude": vehicle["latitude"],
                    "Longitude": vehicle["longitude"]
                }
                for vehicle in vehicle_data
            ]

            # Mostrar dados em uma lista
            st.write(f"Veículos em movimento ou com ignição ligada: {
                     len(vehicle_list)}")
            st.dataframe(pd.DataFrame(vehicle_list))

            # Mapa com ícones personalizados
            icon_data = pd.DataFrame(vehicle_list)
            icon_data["icon_data"] = [
                {
                    "url": icon_url,
                    "width": 128,
                    "height": 128,
                    "anchorY": 128
                }
                for _ in range(len(icon_data))
            ]

            icon_layer = pdk.Layer(
                type="IconLayer",
                data=icon_data,
                get_icon="icon_data",
                get_position=["Longitude", "Latitude"],
                get_size=4,
                size_scale=15,
                pickable=True,  # Torna os ícones clicáveis
                tooltip=True
            )

            # Adicionando a configuração de tooltip
            tooltip = {
                "html": "<b>Placa:</b> {Placa} <br/> <b>Velocidade:</b> {Velocidade} km/h",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }

            view_state = pdk.ViewState(
                latitude=icon_data["Latitude"].mean(),
                longitude=icon_data["Longitude"].mean(),
                zoom=12,
                pitch=50
            )

            r = pdk.Deck(
                map_style="road",
                layers=[icon_layer],
                initial_view_state=view_state,
                tooltip=tooltip  # Configuração do tooltip para exibir informações ao clicar no ícone
            )

            st.pydeck_chart(r)
        else:
            st.error(
                "Nenhum veículo em movimento ou com ignição ligada encontrado.")
    else:
        st.info(
            "Clique no botão 'Atualizar Localização' para carregar os veículos em movimento.")
