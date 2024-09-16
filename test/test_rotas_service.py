#  testes para o módulo de análise de rotas.

import unittest

# Simulação do serviço RouteService conforme implementado anteriormente


class RouteService:
    def __init__(self):
        pass

    def calculate_route_cost(self, distance: float, toll_cost: float, fuel_consumption: float, fuel_price: float) -> float:
        if fuel_consumption <= 0 or distance < 0 or toll_cost < 0 or fuel_price < 0:
            raise ValueError(
                "Valores de entrada devem ser positivos e o consumo de combustível deve ser maior que zero.")

        fuel_cost = (distance / fuel_consumption) * fuel_price
        total_cost = toll_cost + fuel_cost
        return total_cost

    def calculate_weigh_station_delay(self, num_weigh_stations: int, avg_delay_per_station: float) -> float:
        if num_weigh_stations < 0 or avg_delay_per_station < 0:
            raise ValueError(
                "O número de balanças e o atraso médio devem ser valores positivos.")

        total_delay = num_weigh_stations * avg_delay_per_station
        return total_delay

    def compare_routes(self, routes: list) -> dict:
        best_route = None
        best_cost = float('inf')
        best_time = float('inf')

        for route in routes:
            route_id = route.get('route_id')
            distance = route.get('distance')
            toll_cost = route.get('toll_cost')
            fuel_consumption = route.get('fuel_consumption')
            fuel_price = route.get('fuel_price')
            num_weigh_stations = route.get('num_weigh_stations')
            avg_delay_per_station = route.get('avg_delay_per_station')

            try:
                total_cost = self.calculate_route_cost(
                    distance, toll_cost, fuel_consumption, fuel_price)
                total_delay = self.calculate_weigh_station_delay(
                    num_weigh_stations, avg_delay_per_station)

                if total_cost < best_cost or (total_cost == best_cost and total_delay < best_time):
                    best_route = route_id
                    best_cost = total_cost
                    best_time = total_delay

            except ValueError as e:
                print(f"Erro na rota {route_id}: {e}")

        return {"best_route": best_route, "cost": best_cost, "delay": best_time}

# Implementando os testes conforme descrito


class TestRouteService(unittest.TestCase):

    def setUp(self):
        self.route_service = RouteService()

    def test_calculate_route_cost_valid(self):
        """
        Testa o cálculo de custo de rota com valores válidos.
        """
        distance = 100  # km
        toll_cost = 50  # R$
        fuel_consumption = 10  # km/l
        fuel_price = 5.50  # R$/litro

        expected_cost = (distance / fuel_consumption) * fuel_price + toll_cost
        result = self.route_service.calculate_route_cost(
            distance, toll_cost, fuel_consumption, fuel_price)
        self.assertAlmostEqual(result, expected_cost, places=2)

    def test_calculate_route_cost_invalid(self):
        """
        Testa se o cálculo de rota lança exceções para valores inválidos.
        """
        with self.assertRaises(ValueError):
            self.route_service.calculate_route_cost(
                100, 50, 0, 5.50)  # Consumo de combustível inválido

        with self.assertRaises(ValueError):
            # Distância negativa
            self.route_service.calculate_route_cost(-100, 50, 10, 5.50)

        with self.assertRaises(ValueError):
            self.route_service.calculate_route_cost(
                100, -50, 10, 5.50)  # Custo de pedágio negativo

        with self.assertRaises(ValueError):
            self.route_service.calculate_route_cost(
                100, 50, 10, -5.50)  # Preço de combustível negativo

    def test_calculate_weigh_station_delay(self):
        """
        Testa o cálculo do atraso nas balanças.
        """
        num_weigh_stations = 3
        avg_delay_per_station = 15  # minutos

        expected_delay = num_weigh_stations * avg_delay_per_station
        result = self.route_service.calculate_weigh_station_delay(
            num_weigh_stations, avg_delay_per_station)
        self.assertEqual(result, expected_delay)

    def test_calculate_weigh_station_delay_invalid(self):
        """
        Testa se o cálculo de atraso lança exceções para valores inválidos.
        """
        with self.assertRaises(ValueError):
            # Número de balanças negativo
            self.route_service.calculate_weigh_station_delay(-3, 15)

        with self.assertRaises(ValueError):
            self.route_service.calculate_weigh_station_delay(
                3, -15)  # Atraso médio negativo

    def test_compare_routes(self):
        """
        Testa a comparação de rotas para encontrar a mais eficiente.
        """
        routes = [
            {'route_id': 'R001', 'distance': 100, 'toll_cost': 50, 'fuel_consumption': 10,
                'fuel_price': 5.50, 'num_weigh_stations': 2, 'avg_delay_per_station': 15},
            {'route_id': 'R002', 'distance': 120, 'toll_cost': 40, 'fuel_consumption': 12,
                'fuel_price': 5.40, 'num_weigh_stations': 3, 'avg_delay_per_station': 10},
            {'route_id': 'R003', 'distance': 90, 'toll_cost': 60, 'fuel_consumption': 11,
                'fuel_price': 5.30, 'num_weigh_stations': 1, 'avg_delay_per_station': 20},
        ]

        best_route = self.route_service.compare_routes(routes)

        # R002 deve ser a melhor rota, pois tem menor custo e tempo
        self.assertEqual(best_route['best_route'], 'R002')
        self.assertAlmostEqual(
            best_route['cost'], (120 / 12) * 5.40 + 40, places=2)
        # 3 balanças com 10 minutos cada
        self.assertEqual(best_route['delay'], 30)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
