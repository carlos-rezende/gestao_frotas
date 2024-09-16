# Agora, vamos implementar os testes para o módulo de relatórios de desempenho.

import unittest

# Simulação do serviço de multas e manutenção usados no serviço de relatórios de desempenho.


class TrafficFineService:
    def __init__(self):
        self.fines = []

    def register_fine(self, vehicle_id: str, driver_id: str, date: str, type_of_infringement: str, penalty_points: int, fine_amount: float) -> None:
        self.fines.append({
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "penalty_points": penalty_points,
            "fine_amount": fine_amount
        })

    def calculate_total_fines(self, vehicle_id: str = None, driver_id: str = None) -> dict:
        total_points = 0
        total_fines = 0

        for fine in self.fines:
            if (vehicle_id and fine["vehicle_id"] == vehicle_id) or (driver_id and fine["driver_id"] == driver_id):
                total_points += fine["penalty_points"]
                total_fines += fine["fine_amount"]

        return {
            "total_points": total_points,
            "total_fines": total_fines
        }


class FuelService:
    def calculate_fuel_cost(self, vehicle_id: str) -> float:
        return 1000.00  # Exemplo simples para fins de teste


class MaintenanceService:
    def calculate_maintenance_cost(self, vehicle_id: str) -> float:
        return 500.00  # Exemplo simples para fins de teste


# Serviço de Relatório de Desempenho
class PerformanceReportService:
    def __init__(self):
        self.fine_service = TrafficFineService()
        self.fuel_service = FuelService()
        self.maintenance_service = MaintenanceService()

    def generate_performance_report(self, vehicle_id: str, driver_id: str) -> str:
        fine_totals = self.fine_service.calculate_total_fines(
            vehicle_id=vehicle_id, driver_id=driver_id)
        total_fines = fine_totals['total_fines']
        total_points = fine_totals['total_points']

        fuel_cost = self.fuel_service.calculate_fuel_cost(vehicle_id)
        maintenance_cost = self.maintenance_service.calculate_maintenance_cost(
            vehicle_id)

        report = f"Relatório de Desempenho para o Veículo {
            vehicle_id} e Motorista {driver_id}:\n"
        report += f"Total de Multas: R$ {
            total_fines:.2f}, Pontos: {total_points}\n"
        report += f"Total de Combustível: R$ {fuel_cost:.2f}\n"
        report += f"Total de Manutenção: R$ {maintenance_cost:.2f}\n"

        return report

    def calculate_driver_risk(self, driver_id: str) -> str:
        fine_totals = self.fine_service.calculate_total_fines(
            driver_id=driver_id)
        total_points = fine_totals['total_points']

        if total_points > 15:
            risk_level = "Alto"
        elif total_points > 5:
            risk_level = "Moderado"
        else:
            risk_level = "Baixo"

        return f"Motorista {driver_id} tem um nível de risco {risk_level} com {total_points} pontos acumulados."


# Testes para o módulo de relatórios de desempenho
class TestPerformanceReportService(unittest.TestCase):

    def setUp(self):
        self.performance_service = PerformanceReportService()
        self.performance_service.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.performance_service.fine_service.register_fine(
            "V001", "D001", "2024-09-10", "Avanço de sinal", 7, 500.00)

    def test_generate_performance_report(self):
        """
        Testa a geração do relatório de desempenho consolidado.
        """
        report = self.performance_service.generate_performance_report(
            "V001", "D001")
        expected_report = (
            "Relatório de Desempenho para o Veículo V001 e Motorista D001:\n"
            "Total de Multas: R$ 800.00, Pontos: 12\n"
            "Total de Combustível: R$ 1000.00\n"
            "Total de Manutenção: R$ 500.00\n"
        )
        self.assertEqual(report, expected_report)

    def test_calculate_driver_risk(self):
        """
        Testa o cálculo do risco do motorista baseado nos pontos acumulados.
        """
        risk = self.performance_service.calculate_driver_risk("D001")
        self.assertEqual(
            risk, "Motorista D001 tem um nível de risco Moderado com 12 pontos acumulados.")


# Executando os testes
unittest.TextTestRunner().run(unittest.TestLoader(
).loadTestsFromTestCase(TestPerformanceReportService))
