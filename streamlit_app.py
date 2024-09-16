# import streamlit as st
# import googlemaps
# import pandas as pd
# import pydeck as pdk
# import polyline  # Para decodificar polylines

# # Chave de API do Google Maps
# GOOGLE_MAPS_API_KEY = "AIzaSyCTLfLhVAUVvdUZhQ8y_JvjC55xVDQ6NWU"

# # Inicializar cliente do Google Maps
# gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# # Carregar dados de estados e municípios de dois arquivos CSV


# @st.cache_data  # Atualizado para usar st.cache_data
# def load_estados():
#     """Carregar a lista de estados do arquivo CSV."""
#     return pd.read_csv('data/estados.csv', encoding='latin1', sep=';')


# @st.cache_data  # Atualizado para usar st.cache_data
# def load_municipios():
#     """Carregar a lista de municípios do arquivo CSV."""
#     return pd.read_csv('data/municipios.csv', encoding='latin1', sep=';')

# # Funções auxiliares


# def get_coordinates(gmaps, address):
#     """Obter coordenadas do endereço"""
#     try:
#         geocode_result = gmaps.geocode(address)
#         if geocode_result:
#             location = geocode_result[0]['geometry']['location']
#             return location['lat'], location['lng']
#     except Exception as e:
#         st.error(f"Erro ao obter coordenadas para {address}: {e}")
#     return None, None


# def get_driving_route(gmaps, start_coords, end_coords):
#     """Obter pontos da rota de condução (driving) usando a API de Directions"""
#     try:
#         directions_result = gmaps.directions(
#             origin=start_coords,
#             destination=end_coords,
#             mode="driving"
#         )
#         if directions_result:
#             # Extrair a polyline codificada e decodificar em pontos
#             polyline_points = directions_result[0]['overview_polyline']['points']
#             route_points = polyline.decode(polyline_points)

#             # Obter distância e tempo de viagem
#             # em km
#             distance = directions_result[0]['legs'][0]['distance']['value'] / 1000
#             # em horas
#             travel_time = directions_result[0]['legs'][0]['duration']['value'] / 3600
#             return route_points, distance, travel_time
#     except Exception as e:
#         st.error(f"Erro ao obter rota de condução: {e}")
#     return None, None, None


# def get_fuel_consumption(vehicle_type):
#     """Consumo de combustível baseado no tipo de veículo"""
#     consumption_rates = {"Carro": 12, "Caminhão": 6,
#                          "Moto": 30}  # Consumo em km/litro
#     return consumption_rates.get(vehicle_type, 12)


# def show_map_with_pydeck(route_points):
#     """Exibir mapa interativo usando PyDeck"""
#     if route_points:
#         df = pd.DataFrame(route_points, columns=["lat", "lon"])

#         # Criar a camada da rota
#         line_layer = pdk.Layer(
#             "LineLayer",
#             data=df,
#             get_source_position="[lon, lat]",
#             get_target_position="[lon, lat]",
#             get_color=[66, 135, 245],
#             get_width=5
#         )

#         # Configurar a visão inicial do mapa (centralizada na rota)
#         midpoint = df.mean()
#         view_state = pdk.ViewState(
#             latitude=midpoint["lat"], longitude=midpoint["lon"], zoom=8, pitch=50)

#         # Renderizar o mapa com PyDeck
#         r = pdk.Deck(layers=[line_layer], initial_view_state=view_state)
#         st.pydeck_chart(r)
#     else:
#         st.error("Nenhum ponto de rota disponível para exibir no mapa.")


# # Carregar os dados de estados e municípios
# df_estados = load_estados()
# df_municipios = load_municipios()

# # Título da página
# st.title("Gestão de Frotas - Cálculo de Rotas e Consumo")

# # Menu suspenso para estados e municípios
# estado_origem = st.selectbox("Estado Inicial", df_estados['nome'])
# sigla_origem = df_estados.loc[df_estados['nome']
#                               == estado_origem, 'sigla'].values[0]

# # Filtrar municípios pela sigla do estado de origem
# municipios_origem = df_municipios[df_municipios['sigla']
#                                   == sigla_origem]['municipio'].unique()
# cidade_origem = st.selectbox("Cidade Inicial", municipios_origem)

# estado_destino = st.selectbox("Estado Final", df_estados['nome'])
# sigla_destino = df_estados.loc[df_estados['nome']
#                                == estado_destino, 'sigla'].values[0]

# # Filtrar municípios pela sigla do estado de destino
# municipios_destino = df_municipios[df_municipios['sigla']
#                                    == sigla_destino]['municipio'].unique()
# cidade_destino = st.selectbox("Cidade Final", municipios_destino)

# # Tipo de veículo
# vehicle_type = st.selectbox("Tipo de Veículo", ["Carro", "Caminhão", "Moto"])

# # Botão de cálculo
# if st.button("Calcular Rotas e Exibir Mapa"):
#     # Validar se os campos estão preenchidos
#     if cidade_origem and sigla_origem and cidade_destino and sigla_destino and vehicle_type:
#         try:
#             # Endereços completos
#             start_address = f"{cidade_origem}, {sigla_origem}, Brasil"
#             end_address = f"{cidade_destino}, {sigla_destino}, Brasil"

#             # Obter coordenadas
#             start_lat, start_lng = get_coordinates(gmaps, start_address)
#             end_lat, end_lng = get_coordinates(gmaps, end_address)

#             if start_lat is None or end_lat is None:
#                 st.error("Não foi possível encontrar os endereços.")
#             else:
#                 # Obter rota terrestre (driving)
#                 route_points, distance_value, travel_time = get_driving_route(
#                     gmaps, (start_lat, start_lng), (end_lat, end_lng))

#                 if route_points is None:
#                     st.error("Erro ao obter a rota terrestre.")
#                 else:
#                     # Simulação de consumo e custos
#                     fuel_price = 6.50  # R$/litro
#                     toll_cost = 50.00  # R$
#                     consumption = get_fuel_consumption(vehicle_type)
#                     fuel_needed = distance_value / consumption
#                     total_fuel_cost = fuel_needed * fuel_price
#                     total_cost = total_fuel_cost + toll_cost

#                     # Exibir resultados
#                     st.write(f"**Distância:** {distance_value:.2f} km")
#                     st.write(f"**Tempo de viagem:** {travel_time:.2f} horas")
#                     st.write(
#                         f"**Combustível necessário:** {fuel_needed:.2f} litros")
#                     st.write(
#                         f"**Custo total de combustível:** R$ {total_fuel_cost:.2f}")
#                     st.write(
#                         f"**Custo total (incluindo pedágios):** R$ {total_cost:.2f}")

#                     # Exibir mapa interativo com a rota
#                     show_map_with_pydeck(route_points)

#         except Exception as e:
#             st.error(f"Erro ao calcular a rota: {e}")
#     else:
#         st.error("Por favor, preencha todos os campos.")
