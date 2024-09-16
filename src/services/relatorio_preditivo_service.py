from src.services.dados_historicos_service import HistoricalDataStorage


class PredictiveReportService:
    def __init__(self, historical_storage: HistoricalDataStorage):
        self.historical_storage = historical_storage

    def predict_fuel_cost(self, vehicle_id: str, estimated_distance: float, fuel_consumption: float, fuel_price: float) -> float:
        history = self.historical_storage.get_vehicle_history(vehicle_id)

        if not history:
            return (estimated_distance / fuel_consumption) * fuel_price

        total_fuel_cost = 0
        total_distance = 0
        for route in history:
            total_fuel_cost += route['fuel_cost']
            total_distance += route['distance']

        average_cost_per_km = total_fuel_cost / \
            total_distance if total_distance > 0 else 0
        return average_cost_per_km * estimated_distance

    def predict_maintenance_due(self, vehicle_id: str, current_quilometragem: int, maintenance_interval: int) -> bool:
        history = self.historical_storage.get_vehicle_history(vehicle_id)

        if not history:
            return False

        last_quilometragem = max(route['quilometragem']
                                 for route in history if 'quilometragem' in route)
        return (current_quilometragem - last_quilometragem) >= maintenance_interval
