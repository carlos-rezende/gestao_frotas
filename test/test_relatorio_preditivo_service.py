import unittest

from src.services.dados_historicos_service import HistoricalDataStorage
from src.services.relatorio_preditivo_service import PredictiveReportService


class TestPredictiveReportService(unittest.TestCase):
    def setUp(self):
        self.historical_storage = HistoricalDataStorage(
            "test_historico_frota.json")
        self.predictive_service = PredictiveReportService(
            self.historical_storage)

    def test_predict_fuel_cost(self):
        # Simular histórico para o veículo "V001"
        self.historical_storage.save_history("V001", {
            "distance": 500,
            "fuel_cost": 300,
            "quilometragem": 25000
        })

        predicted_fuel_cost = self.predictive_service.predict_fuel_cost(
            "V001", 600, 8, 6.5)
        self.assertAlmostEqual(predicted_fuel_cost, 360.0, places=1)

    def test_predict_maintenance_due(self):
        # Simular histórico para o veículo "V001"
        self.historical_storage.save_history("V001", {
            "distance": 500,
            "fuel_cost": 300,
            "quilometragem": 25000
        })

        maintenance_due = self.predictive_service.predict_maintenance_due(
            "V001", 35000, 10000)
        self.assertTrue(maintenance_due)


if __name__ == "__main__":
    unittest.main()
