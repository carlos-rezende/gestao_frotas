# src/services/route_service.py

class RouteService:
    def __init__(self):
        pass

    def calculate_route_cost(self, distance: float, toll_cost: float, fuel_consumption: float, fuel_price: float) -> float:
        """
        Calcula o custo total da rota, considerando pedágios e combustível.

        :param distance: Distância percorrida na rota (em km).
        :param toll_cost: Custo total dos pedágios ao longo da rota.
        :param fuel_consumption: Consumo médio de combustível do veículo (km/l).
        :param fuel_price: Preço do combustível por litro.
        :return: Custo total da rota.
        """
        if fuel_consumption <= 0 or distance < 0 or toll_cost < 0 or fuel_price < 0:
            raise ValueError(
                "Valores de entrada devem ser positivos e o consumo de combustível deve ser maior que zero.")

        # Custo do combustível
        fuel_cost = (distance / fuel_consumption) * fuel_price

        # Custo total = pedágios + combustível
        total_cost = toll_cost + fuel_cost
        return total_cost

    def calculate_weigh_station_delay(self, num_weigh_stations: int, avg_delay_per_station: float) -> float:
        """
        Calcula o tempo de atraso total em balanças.

        :param num_weigh_stations: Número de balanças ao longo da rota.
        :param avg_delay_per_station: Atraso médio em cada balança (em minutos).
        :return: Tempo total de atraso (em minutos).
        """
        if num_weigh_stations < 0 or avg_delay_per_station < 0:
            raise ValueError(
                "O número de balanças e o atraso médio devem ser valores positivos.")

        total_delay = num_weigh_stations * avg_delay_per_station
        return total_delay

    def compare_routes(self, routes: list) -> dict:
        """
        Compara diferentes rotas e sugere a mais eficiente com base no custo total e no tempo de atraso.

        :param routes: Lista de dicionários contendo dados das rotas.
        :return: Dicionário com a rota mais eficiente.
        """
        best_route = None
        best_cost = float('inf')
        best_time = float('inf')

        for route in routes:
            # Garantir que tenha um valor padrão
            route_id = route.get('route_id')
            # Garantir que tenha um valor padrão
            distance = route.get('distance', 0)
            toll_cost = route.get('toll_cost', 0)
            fuel_consumption = route.get(
                'fuel_consumption', 1)  # Evitar divisão por zero
            fuel_price = route.get('fuel_price', 1)  # Valor padrão
            num_weigh_stations = route.get(
                'num_weigh_stations', 0)  # Valor padrão
            avg_delay_per_station = route.get(
                'avg_delay_per_station', 0)  # Valor padrão

            try:
                total_cost = self.calculate_route_cost(
                    distance, toll_cost, fuel_consumption, fuel_price)
                total_delay = self.calculate_weigh_station_delay(
                    num_weigh_stations, avg_delay_per_station)

                # Critério de seleção: custo mais baixo e menor atraso
                if total_cost < best_cost or (total_cost == best_cost and total_delay < best_time):
                    best_route = route_id
                    best_cost = total_cost
                    best_time = total_delay

            except ValueError as e:
                print(f"Erro na rota {route_id}: {e}")

        return {"best_route": best_route, "cost": best_cost, "delay": best_time}

    def get_route_data(self, vehicle_id: str) -> dict:
        """
        Simula a obtenção de dados de rota para um veículo.
        Retorna a distância percorrida e o custo dos pedágios.

        :param vehicle_id: Identificador do veículo
        :return: Dicionário contendo a distância percorrida e o custo dos pedágios
        """
        # Exemplo de dados simulados
        route_data = {
            "distance": 500.0,  # Distância em quilômetros
            "toll_cost": 100.0,  # Custo total dos pedágios em R$
            "fuel_consumption": 8.0,  # Consumo de combustível em km/l
            "fuel_price": 6.50,  # Preço do combustível por litro
            "travel_time": 5.5,  # Tempo total de viagem em horas
            "num_weigh_stations": 2,  # Número de balanças
            "avg_delay_per_station": 10.0  # Atraso médio por balança em minutos
        }
        return route_data
