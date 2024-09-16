import os
from dotenv import load_dotenv
import streamlit as st
import googlemaps
import pandas as pd
import pydeck as pdk
import polyline  # Para decodificar polylines

load_dotenv()
# Chave de API do Google Maps
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def show_route_page():
    # Initialize Google Maps client
    if not GOOGLE_MAPS_API_KEY:
        st.error("Google Maps API key is not set.")
        return
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    st.title("Cálculo de Rotas e Consumo")
    st.write("Aqui você pode calcular as rotas para sua frota.")

    df_estados = load_estados()
    df_municipios = load_municipios()

    # Select Origin
    estado_origem, cidade_origem, sigla_origem = select_location(
        df_estados, df_municipios, "Origem")

    # Select Destination
    estado_destino, cidade_destino, sigla_destino = select_location(
        df_estados, df_municipios, "Destino")

    # Vehicle type and fuel details
    vehicle_type = st.selectbox(
        "Tipo de Veículo", ["Carro", "Caminhão", "Moto"])
    consumption = st.number_input(f"Consumo do {
                                  vehicle_type} (km/l):", min_value=1.0, value=get_default_consumption(vehicle_type))
    fuel_price = st.number_input(
        "Preço do Combustível (R$/litro):", min_value=0.0, value=6.50)

    if st.button("Calcular Rotas e Exibir Mapa"):
        if validate_inputs(cidade_origem, sigla_origem, cidade_destino, sigla_destino, vehicle_type):
            try:
                start_address = f"{cidade_origem}, {sigla_origem}, Brasil"
                end_address = f"{cidade_destino}, {sigla_destino}, Brasil"

                start_coords = get_coordinates(gmaps, start_address)
                end_coords = get_coordinates(gmaps, end_address)

                if not start_coords or not end_coords:
                    st.error("Não foi possível encontrar os endereços.")
                else:
                    route_points, distance, travel_time, toll_cost = get_route_details(
                        gmaps, start_coords, end_coords)

                    if route_points:
                        display_results(distance, travel_time,
                                        consumption, fuel_price, toll_cost)
                        show_map_with_pydeck(
                            route_points, start_coords, end_coords)
                    else:
                        st.error("Erro ao obter a rota terrestre.")
            except Exception as e:
                st.error(f"Erro ao calcular a rota: {e}")


def select_location(df_estados, df_municipios, label):
    """Helper function to select state and city."""
    col1, col2 = st.columns(2)
    with col1:
        estado = st.selectbox(f"{label} - Estado", df_estados['nome'])
    sigla = df_estados.loc[df_estados['nome'] == estado, 'sigla'].values[0]

    municipios = df_municipios[df_municipios['sigla']
                               == sigla]['municipio'].unique()
    with col2:
        cidade = st.selectbox(f"{label} - Cidade", municipios)

    return estado, cidade, sigla


def validate_inputs(*args):
    """Validates if essential inputs are not None or empty."""
    for arg in args:
        if not arg:
            st.error("Por favor, preencha todos os campos.")
            return False
    return True


def display_results(distance, travel_time, consumption, fuel_price, toll_cost):
    """Display route and cost details."""
    fuel_needed = distance / consumption
    total_fuel_cost = fuel_needed * fuel_price
    total_cost = total_fuel_cost + toll_cost

    st.write(f"**Distância:** {distance:.2f} km")
    st.write(f"**Tempo de viagem:** {travel_time:.2f} horas")
    st.write(f"**Combustível necessário:** {fuel_needed:.2f} litros")
    st.write(f"**Custo total de combustível:** R$ {total_fuel_cost:.2f}")
    st.write(f"**Custo total de pedágios:** R$ {toll_cost:.2f}")
    st.write(f"**Custo total (incluindo pedágios):** R$ {total_cost:.2f}")


@st.cache_data
def load_estados():
    """Carregar a lista de estados do arquivo CSV."""
    return pd.read_csv('data/estados.csv', encoding='latin1', sep=';')


@st.cache_data
def load_municipios():
    """Carregar a lista de municípios do arquivo CSV."""
    return pd.read_csv('data/municipios.csv', encoding='latin1', sep=';')


def get_coordinates(gmaps, address):
    """Obter coordenadas do endereço"""
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            st.error(f"Geocode não retornou resultados para: {address}")
    except Exception as e:
        st.error(f"Erro ao obter coordenadas para {address}: {e}")
    return None, None


def get_route_details(gmaps, start_coords, end_coords):
    """Obter detalhes da rota, incluindo pontos da rota, distância, tempo e custo de pedágios."""
    try:
        directions_result = gmaps.directions(
            origin=start_coords,
            destination=end_coords,
            mode="driving"
        )
        if directions_result:
            polyline_points = directions_result[0]['overview_polyline']['points']
            route_points = polyline.decode(polyline_points)
            distance = directions_result[0]['legs'][0]['distance']['value'] / 1000
            travel_time = directions_result[0]['legs'][0]['duration']['value'] / 3600
            toll_cost = 50.00  # Placeholder for toll cost calculation
            return route_points, distance, travel_time, toll_cost
        else:
            st.error("A resposta da API Directions está vazia.")
    except Exception as e:
        st.error(f"Erro ao obter detalhes da rota: {e}")
    return None, None, None, None


def get_default_consumption(vehicle_type):
    """Consumo de combustível padrão baseado no tipo de veículo"""
    consumption_rates = {"Carro": 12.0, "Caminhão": 6.0, "Moto": 30.0}
    return consumption_rates.get(vehicle_type, 12.0)


def show_map_with_pydeck(route_points, start_coords, end_coords):
    """Exibir mapa interativo com rota e ícones de veículos usando PyDeck"""
    if route_points:
        df = pd.DataFrame(route_points, columns=["lat", "lon"])
        icon_data = pd.DataFrame([
            {"lat": start_coords[0], "lon": start_coords[1], "name": "Início", "icon_data": {
                "url": "https://img.icons8.com/ultraviolet/40/000000/marker.png",
                "width": 128, "height": 128, "anchorY": 128}},
            {"lat": end_coords[0], "lon": end_coords[1], "name": "Destino", "icon_data": {
                "url": "https://img.icons8.com/ultraviolet/40/000000/marker.png",
                "width": 128, "height": 128, "anchorY": 128}}
        ])

        line_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_points}],
            get_path="path",
            get_color=[255, 0, 0],
            width_scale=20,
            width_min_pixels=2,
        )

        icon_layer = pdk.Layer(
            "IconLayer",
            data=icon_data,
            get_icon="icon_data",
            get_position=["lon", "lat"],
            get_size=4,
            size_scale=10,
        )

        midpoint = df.mean()
        view_state = pdk.ViewState(
            latitude=midpoint["lat"], longitude=midpoint["lon"], zoom=8, pitch=50
        )

        r = pdk.Deck(
            map_style="streets",
            layers=[line_layer, icon_layer],
            initial_view_state=view_state
        )

        st.pydeck_chart(r)
    else:
        st.error("Nenhum ponto de rota disponível para exibir no mapa.")
