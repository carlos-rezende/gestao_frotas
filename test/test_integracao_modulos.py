# Agora vamos implementar os testes para o código corrigido.

import unittest

# Simulação dos serviços necessários usados no serviço de relatórios de desempenho


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

    def check_maintenance_due(self, vehicle_id: str) -> bool:
        return True  # Retorna True indicando que a manutenção está pendente


class ChecklistService:
    def __init__(self):
        self.checklists = {}

    def run_checklist(self, vehicle_id: str, driver_id: str, items: list) -> dict:
        approved = True
        failed_items = []
        item_status = {item['nome']: item['status'] for item in items}

        for item in item_status:
            if item_status[item] == "reprovado":
                failed_items.append(item)
                approved = False

        checklist_result = {
            "vehicle_id": vehicle_id,
            "approved": approved,
            "failed_items": failed_items
        }

        self.checklists[vehicle_id] = checklist_result
        return checklist_result

    def get_checklist_status(self, vehicle_id: str) -> str:
        if vehicle_id in self.checklists:
            return "Aprovado" if self.checklists[vehicle_id]["approved"] else "Reprovado"
        return "Sem checklist registrado"

    def get_failed_items(self, vehicle_id: str) -> list:
        if vehicle_id in self.checklists:
            return self.checklists[vehicle_id]["failed_items"]
        return []


class RouteService:
    def get_route_data(self, vehicle_id: str) -> dict:
        return {
            "distance": 500,  # km
            "toll_cost": 100.00  # R$
        }

# Serviço de Relatório de Desempenho com integração a todos os serviços


class PerformanceReportService:
    def __init__(self):
        self.fine_service = TrafficFineService()
        self.fuel_service = FuelService()
        self.maintenance_service = MaintenanceService()
        self.checklist_service = ChecklistService()
        self.route_service = RouteService()

    def generate_performance_report(self, vehicle_id: str, driver_id: str) -> str:
        fine_totals = self.fine_service.calculate_total_fines(
            vehicle_id=vehicle_id, driver_id=driver_id)
        total_fines = fine_totals['total_fines']
        total_points = fine_totals['total_points']

        fuel_cost = self.fuel_service.calculate_fuel_cost(vehicle_id)
        maintenance_cost = self.maintenance_service.calculate_maintenance_cost(
            vehicle_id)
        maintenance_due = self.maintenance_service.check_maintenance_due(
            vehicle_id)
        checklist_status = self.checklist_service.get_checklist_status(
            vehicle_id)
        failed_items = self.checklist_service.get_failed_items(vehicle_id)
        route_data = self.route_service.get_route_data(vehicle_id)
        total_distance = route_data['distance']
        tolls = route_data['toll_cost']

        report = (
            f"Relatório de Desempenho para o Veículo {
                vehicle_id} e Motorista {driver_id}:\n"
            f"Total de Multas: R$ {total_fines:.2f}, Pontos: {total_points}\n"
            f"Total de Combustível: R$ {fuel_cost:.2f}\n"
            f"Total de Manutenção: R$ {maintenance_cost:.2f}\n"
            f"Status do Checklist: {checklist_status}\n"
        )

        if failed_items:
            report += f"Itens Reprovados no Checklist: {
                ', '.join(failed_items)}\n"

        report += f"Manutenção Preventiva Pendente: {
            'Sim' if maintenance_due else 'Não'}\n"
        report += f"Distância Total Percorrida: {total_distance} km\n"
        report += f"Custo de Pedágios: R$ {tolls:.2f}\n"

        return report

    def analyze_fuel_efficiency(self, vehicle_id: str) -> str:
        fuel_cost = self.fuel_service.calculate_fuel_cost(vehicle_id)
        route_data = self.route_service.get_route_data(vehicle_id)
        total_distance = route_data['distance']

        if total_distance > 0:
            efficiency = fuel_cost / total_distance
            return f"Eficiência de combustível: R$ {efficiency:.2f} por km"
        return "Distância total percorrida é zero. Não é possível calcular eficiência de combustível."

# Testes para o módulo de relatórios de desempenho com integração


class TestPerformanceReportService(unittest.TestCase):

    def setUp(self):
        self.performance_service = PerformanceReportService()
        # Registrar algumas multas
        self.performance_service.fine_service.register_fine(
            "V001", "D001", "2024-08-15", "Excesso de velocidade", 5, 300.00)
        self.performance_service.fine_service.register_fine(
            "V001", "D001", "2024-09-10", "Avanço de sinal", 7, 500.00)

        # Executar o checklist
        items = [
            {"nome": "nível de óleo", "status": "aprovado"},
            {"nome": "freios", "status": "reprovado"},
            {"nome": "luzes", "status": "aprovado"}
        ]
        self.performance_service.checklist_service.run_checklist(
            "V001", "D001", items)

    def test_generate_performance_report(self):
        """
        Testa a geração do relatório de desempenho consolidado com todos os módulos integrados.
        """
        report = self.performance_service.generate_performance_report(
            "V001", "D001")
        expected_report = (
            "Relatório de Desempenho para o Veículo V001 e Motorista D001:\n"
            "Total de Multas: R$ 800.00, Pontos: 12\n"
            "Total de Combustível: R$ 1000.00\n"
            "Total de Manutenção: R$ 500.00\n"
            "Status do Checklist: Reprovado\n"
            "Itens Reprovados no Checklist: freios\n"
            "Manutenção Preventiva Pendente: Sim\n"
            "Distância Total Percorrida: 500 km\n"
            "Custo de Pedágios: R$ 100.00\n"
        )
        self.assertEqual(report, expected_report)

    def test_analyze_fuel_efficiency(self):
        """
        Testa a análise de eficiência de combustível por quilômetro rodado.
        """
        efficiency_report = self.performance_service.analyze_fuel_efficiency(
            "V001")
        expected_efficiency_report = "Eficiência de combustível: R$ 2.00 por km"
        self.assertEqual(efficiency_report, expected_efficiency_report)


# Executando os testes
unittest.TextTestRunner().run(unittest.TestLoader(
).loadTestsFromTestCase(TestPerformanceReportService))
