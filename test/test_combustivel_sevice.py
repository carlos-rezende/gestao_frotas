# tests/test_fuel_service.py
import unittest

# Simulação do serviço FuelService conforme implementado anteriormente


class FuelService:
    def __init__(self):
        pass

    def calculate_fuel_cost(self, kilometers: float, fuel_consumption: float, fuel_price: float) -> float:
        if fuel_consumption <= 0:
            raise ValueError(
                "O consumo de combustível deve ser maior que zero.")
        if kilometers < 0 or fuel_price < 0:
            raise ValueError(
                "A quilometragem e o preço do combustível devem ser valores positivos.")

        fuel_used = kilometers / fuel_consumption
        fuel_cost = fuel_used * fuel_price
        return fuel_cost

    def calculate_fleet_fuel_cost(self, fleet_data: list) -> dict:
        fleet_costs = {}

        for vehicle in fleet_data:
            vehicle_id = vehicle.get('vehicle_id')
            kilometers = vehicle.get('kilometers')
            fuel_consumption = vehicle.get('fuel_consumption')
            fuel_price = vehicle.get('fuel_price')

            try:
                cost = self.calculate_fuel_cost(
                    kilometers, fuel_consumption, fuel_price)
                fleet_costs[vehicle_id] = cost
            except ValueError as e:
                fleet_costs[vehicle_id] = None

        return fleet_costs

# Implementando os testes conforme descrito


class TestFuelService(unittest.TestCase):

    def setUp(self):
        self.fuel_service = FuelService()

    def test_calculate_fuel_cost_valid(self):
        kilometers = 500
        fuel_consumption = 10  # km/l
        fuel_price = 5.50  # R$/litro

        expected_cost = (kilometers / fuel_consumption) * fuel_price
        result = self.fuel_service.calculate_fuel_cost(
            kilometers, fuel_consumption, fuel_price)
        self.assertAlmostEqual(result, expected_cost, places=2)

    def test_calculate_fuel_cost_invalid_consumption(self):
        with self.assertRaises(ValueError):
            self.fuel_service.calculate_fuel_cost(500, 0, 5.50)

        with self.assertRaises(ValueError):
            self.fuel_service.calculate_fuel_cost(500, -5, 5.50)

    def test_calculate_fuel_cost_negative_values(self):
        with self.assertRaises(ValueError):
            self.fuel_service.calculate_fuel_cost(-100, 10, 5.50)

        with self.assertRaises(ValueError):
            self.fuel_service.calculate_fuel_cost(100, 10, -5.50)

    def test_calculate_fleet_fuel_cost(self):
        fleet_data = [
            {'vehicle_id': 'V001', 'kilometers': 500,
                'fuel_consumption': 10, 'fuel_price': 5.50},
            {'vehicle_id': 'V002', 'kilometers': 750,
                'fuel_consumption': 8, 'fuel_price': 5.70},
            {'vehicle_id': 'V003', 'kilometers': 600,
                'fuel_consumption': 12, 'fuel_price': 5.40},
        ]

        expected_costs = {
            'V001': (500 / 10) * 5.50,
            'V002': (750 / 8) * 5.70,
            'V003': (600 / 12) * 5.40,
        }

        result = self.fuel_service.calculate_fleet_fuel_cost(fleet_data)
        for vehicle_id, expected_cost in expected_costs.items():
            self.assertAlmostEqual(result[vehicle_id], expected_cost, places=2)

    def test_calculate_fleet_fuel_cost_invalid_data(self):
        fleet_data = [
            {'vehicle_id': 'V001', 'kilometers': 500,
                'fuel_consumption': 10, 'fuel_price': 5.50},
            {'vehicle_id': 'V002', 'kilometers': 750,
                'fuel_consumption': 0, 'fuel_price': 5.70},
            {'vehicle_id': 'V003', 'kilometers': 600,
                'fuel_consumption': 12, 'fuel_price': 5.40},
        ]

        result = self.fuel_service.calculate_fleet_fuel_cost(fleet_data)
        self.assertIsNotNone(result['V001'])
        self.assertIsNone(result['V002'])
        self.assertIsNotNone(result['V003'])


# Executando os testes
suite = unittest.TestLoader().loadTestsFromTestCase(TestFuelService)
unittest.TextTestRunner().run(suite)
