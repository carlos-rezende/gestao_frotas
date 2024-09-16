import requests


class GPSService:
    def __init__(self):
        # Dicionário de locadoras com suas respectivas chaves de API e URLs
        self.locadoras = {
            "Locadora A": {
                "api_key": "API_KEY_LOCADORA_A",
                "api_url": "https://api.locadoraA.com/get_vehicle_location",
                "type": "default"
            },
            "Locadora B": {
                "api_key": "API_KEY_LOCADORA_B",
                "api_url": "https://api.locadoraB.com/get_vehicle_location",
                "type": "default"
            },
            "SegMinas": {
                "api_key": "SEU_TOKEN_SEGMINAS",
                "api_url": "http://api.segminas.com.br/lastPositions/",
                "type": "segminas"
            },
            "BRT Rio": {
                "api_url": "https://dados.mobilidade.rio/gps/brt",
                "type": "brt"
            }
        }

    def get_vehicle_location(self, vehicle_id, locadora_name):
        locadora_info = self.locadoras.get(locadora_name)
        if not locadora_info:
            raise ValueError(f"Locadora '{locadora_name}' não encontrada.")

        # Verificar o tipo de locadora e chamar a função apropriada
        locadora_type = locadora_info['type']
        if locadora_type == 'segminas':
            return self.get_segminas_location(vehicle_id, locadora_info['api_key'])
        elif locadora_type == 'brt':
            return self.get_brt_vehicles_in_motion(locadora_info['api_url'])
        else:
            return self.get_default_location(vehicle_id, locadora_info['api_url'], locadora_info['api_key'])

    def get_brt_vehicles_in_motion(self, api_url):
        """
        Obter todos os veículos do BRT que estão em movimento ou com ignição ligada.
        :param api_url: URL da API do BRT.
        :return: Lista de veículos que estão em movimento ou com ignição ligada.
        """
        try:
            response = requests.get(api_url)
            response.raise_for_status()

            # Converter a resposta em JSON
            vehicles_data = response.json()

            # Inspecionar a estrutura da resposta
            # print(f"Estrutura da resposta da API do BRT: {vehicles_data}")

            # Verificar se a lista de veículos está em uma chave específica do dicionário
            if isinstance(vehicles_data, dict):
                # Tentar encontrar a chave que contém a lista de veículos
                # Ajuste conforme a estrutura real da resposta da API
                # Substitua 'veiculos' pela chave correta
                vehicles_data = vehicles_data.get('veiculos', [])

            # Verificar se vehicles_data é uma lista
            if not isinstance(vehicles_data, list):
                print(
                    f"Erro: Esperava-se uma lista, mas recebeu {type(vehicles_data)}.")
                return []

            # Filtrar veículos que estão em movimento ou com ignição ligada
            vehicles_in_motion = [
                {
                    "codigo": vehicle.get("codigo"),
                    "placa": vehicle.get("placa"),
                    "latitude": vehicle.get("latitude"),
                    "longitude": vehicle.get("longitude"),
                    "velocidade": vehicle.get("velocidade"),
                    "ignicao": vehicle.get("ignicao"),
                    "trajeto": vehicle.get("trajeto")
                }
                for vehicle in vehicles_data
                if vehicle.get("velocidade", 0) > 0 or vehicle.get("ignicao") == 1
            ]

            return vehicles_in_motion
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do BRT: {e}")
            return []
        except ValueError as e:
            print(f"Erro ao decodificar JSON da resposta da API: {e}")
            return []
