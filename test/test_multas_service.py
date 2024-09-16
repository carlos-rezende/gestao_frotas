# Agora, vamos implementar os testes para o módulo de monitoramento de multas de trânsito.

import unittest
from datetime import datetime

# Simulação do serviço TrafficFineService conforme implementado anteriormente


class TrafficFineService:
    def __init__(self):
        self.fines = []

    def register_fine(self, vehicle_id: str, driver_id: str, date: str, type_of_infringement: str, penalty_points: int, fine_amount: float) -> None:
        self.fines.append({
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "date": datetime.strptime(date, "%Y-%m-%d"),
            "type_of_infringement": type_of_infringement,
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

    def generate_fine_report(self) -> str:
        if not self.fines:
            return "Nenhuma multa registrada."

        report = "Relatório de Multas Registradas:\n"
        for fine in self.fines:
            report += (
                f"Veículo: {fine['vehicle_id']}, Motorista: {
                    fine['driver_id']}, Data: {fine['date'].strftime('%Y-%m-%d')}, "
                f"Infração: {fine['type_of_infringement']}, Pontos: {
                    fine['penalty_points']}, Valor: R$ {fine['fine_amount']:.2f}\n"
            )
        return report

    def identify_recurring_fines(self, driver_id: str, period_in_days: int = 30) -> list:
        fines_by_driver = [
            fine for fine in self.fines if fine["driver_id"] == driver_id]
        recurring_fines = []

        for i in range(len(fines_by_driver)):
            for j in range(i + 1, len(fines_by_driver)):
                delta_days = abs(
                    (fines_by_driver[j]["date"] - fines_by_driver[i]["date"]).days)
                if delta_days <= period_in_days:
                    recurring_fines.append(
                        (fines_by_driver[i], fines_by_driver[j]))

        return recurring_fines


# Implementando os testes para o serviço de multas de trânsito
class TestTrafficFineService(unittest.TestCase):

    def setUp(self):
        self.fine_service = TrafficFineService()

    def test_register_fine(self):
        """
        Testa o registro de uma multa no sistema.
        """
        self.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.assertEqual(len(self.fine_service.fines), 1)
        self.assertEqual(self.fine_service.fines[0]["vehicle_id"], "V001")
        self.assertEqual(self.fine_service.fines[0]["driver_id"], "D001")
        self.assertEqual(self.fine_service.fines[0]["penalty_points"], 5)
        self.assertEqual(self.fine_service.fines[0]["fine_amount"], 300.00)

    def test_calculate_total_fines_by_vehicle(self):
        """
        Testa o cálculo do total de multas para um veículo específico.
        """
        self.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.fine_service.register_fine(
            "V001", "D002", "2024-09-05", "Avanço de sinal", 7, 500.00)

        total_fines = self.fine_service.calculate_total_fines(
            vehicle_id="V001")
        self.assertEqual(total_fines["total_points"], 12)
        self.assertEqual(total_fines["total_fines"], 800.00)

    def test_generate_fine_report(self):
        """
        Testa a geração de um relatório de multas.
        """
        self.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.fine_service.register_fine(
            "V002", "D002", "2024-09-05", "Estacionamento irregular", 3, 150.00)

        report = self.fine_service.generate_fine_report()
        expected_report = (
            "Relatório de Multas Registradas:\n"
            "Veículo: V001, Motorista: D001, Data: 2024-08-15, Infração: Excesso de velocidade, Pontos: 5, Valor: R$ 300.00\n"
            "Veículo: V002, Motorista: D002, Data: 2024-09-05, Infração: Estacionamento irregular, Pontos: 3, Valor: R$ 150.00\n"
        )
        self.assertEqual(report, expected_report)

    def test_identify_recurring_fines(self):
        """
        Testa a identificação de multas recorrentes dentro de um período de 30 dias.
        """
        self.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.fine_service.register_fine(
            "V001", "D001", "2024-09-10", "Avanço de sinal", 7, 500.00)

        recurring_fines = self.fine_service.identify_recurring_fines("D001")
        self.assertEqual(len(recurring_fines), 1)
        self.assertEqual(
            recurring_fines[0][0]["type_of_infringement"], "Excesso de velocidade")
        self.assertEqual(
            recurring_fines[0][1]["type_of_infringement"], "Avanço de sinal")


# Executando os testes
unittest.TextTestRunner().run(
    unittest.TestLoader().loadTestsFromTestCase(TestTrafficFineService))
