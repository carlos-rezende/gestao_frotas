from src.services.dados_historicos_service import HistoricalDataStorage
from src.services.relatorio_preditivo_service import PredictiveReportService


class ReportController:
    def __init__(self):
        self.historical_storage = HistoricalDataStorage()
        self.predictive_service = PredictiveReportService(
            self.historical_storage)

    def generate_predictive_fuel_report(self, vehicle_id: str, estimated_distance: float, fuel_consumption: float, fuel_price: float):
        predicted_fuel_cost = self.predictive_service.predict_fuel_cost(
            vehicle_id, estimated_distance, fuel_consumption, fuel_price)
        print(f"Predicted fuel cost for {
              estimated_distance} km: R$ {predicted_fuel_cost:.2f}")

    def check_maintenance_due(self, vehicle_id: str, current_quilometragem: int, maintenance_interval: int) -> bool:
        """
        Verifica se o veículo precisa de manutenção com base no histórico, quilometragem atual e no intervalo de manutenção.

        :param vehicle_id: Identificador do veículo.
        :param current_quilometragem: Quilometragem atual do veículo.
        :param maintenance_interval: Intervalo de manutenção recomendado.
        :return: True se a manutenção é necessária, False caso contrário.
        """
        # Usa a função de previsão para determinar se a manutenção é necessária com base no histórico
        maintenance_due = self.predictive_service.predict_maintenance_due(
            vehicle_id, current_quilometragem, maintenance_interval
        )

        return maintenance_due
