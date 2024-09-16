

class FuelService:
    def __init__(self):
        pass

    def calculate_fuel_cost(self, kilometers: float, fuel_consumption: float, fuel_price: float) -> float:
        """
        Calcula o custo de combustível para um veículo com base na quilometragem, consumo e preço do combustível.

        :param kilometers: Quilometragem percorrida pelo veículo.
        :param fuel_consumption: Consumo de combustível do veículo (km/l).
        :param fuel_price: Preço do combustível por litro.
        :return: Custo total de combustível para o veículo.
        """
        if kilometers < 0 or fuel_price < 0 or fuel_consumption <= 0:
            raise ValueError(
                "Os valores de quilômetros, preço do combustível e consumo devem ser positivos.")

        # Calcular o custo total de combustível
        liters_used = kilometers / fuel_consumption
        total_cost = liters_used * fuel_price
        return total_cost

    def calculate_fleet_fuel_cost(self, fleet_data: list) -> dict:
        """
        Calcula o custo total de combustível para toda a frota.

        :param fleet_data: Lista de dicionários com os dados dos veículos.
        :return: Dicionário com o custo total de combustível por veículo.
        """
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
                print(f"Erro no cálculo de combustível para o veículo {
                      vehicle_id}: {e}")
                fleet_costs[vehicle_id] = None

        return fleet_costs
