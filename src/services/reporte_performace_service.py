from src.services.checklist_veiculos_service import ChecklistService
from src.services.combustivel_service import FuelService
from src.services.manutencao_service import MaintenanceService
from src.services.multas_service import TrafficFineService
from src.services.rotas_service import RouteService


class PerformanceReportService:
    def __init__(self):
        self.fine_service = TrafficFineService()
        self.fuel_service = FuelService()
        self.maintenance_service = MaintenanceService()
        self.checklist_service = ChecklistService()
        self.route_service = RouteService()

    def analyze_fuel_efficiency(self, vehicle_id: str) -> str:
        """
        Análise detalhada da eficiência de combustível por quilômetro rodado.
        """
        fuel_consumption = 8.0  # Consumo médio em km por litro
        fuel_price = 6.50  # Preço do combustível por litro
        route_data = self.route_service.get_route_data(vehicle_id)
        # Garantir que total_distance seja numérico
        total_distance = float(route_data['distance'])

        # Chamar calculate_fuel_cost com valores numéricos
        fuel_cost = self.fuel_service.calculate_fuel_cost(
            total_distance, fuel_consumption, fuel_price)

        if total_distance > 0:
            efficiency = fuel_cost / total_distance
            return f"Eficiência de combustível: R$ {efficiency:.2f} por km"
        return "Distância total percorrida é zero. Não é possível calcular eficiência de combustível."

    def generate_performance_report(self, vehicle_id: str, driver_id: str) -> str:
        """
        Gera um relatório consolidado de desempenho de um veículo e motorista,
        incluindo dados de manutenção preventiva.
        """
        # Coleta de dados de multas
        fine_totals = self.fine_service.calculate_total_fines(
            vehicle_id=vehicle_id, driver_id=driver_id)
        total_fines = fine_totals['total_fines']
        total_points = fine_totals['total_points']

        # Coleta de dados de combustível e manutenção
        fuel_consumption = 8.0  # Consumo médio em km por litro
        fuel_price = 6.50  # Preço do combustível por litro
        route_data = self.route_service.get_route_data(vehicle_id)
        # Garantir que total_distance seja numérico
        total_distance = float(route_data['distance'])
        fuel_cost = self.fuel_service.calculate_fuel_cost(
            total_distance, fuel_consumption, fuel_price)
        maintenance_cost = self.maintenance_service.calculate_maintenance_cost(
            vehicle_id)

        # Verificação de manutenção preventiva
        # Função para obter a quilometragem atual
        current_quilometragem = self.get_current_quilometragem(vehicle_id)
        # Exemplo de quilometragem da última manutenção
        last_maintenance_quilometragem = 20000
        maintenance_interval = 10000  # Intervalo de manutenção
        maintenance_due = self.maintenance_service.check_maintenance(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval
        )

        # Coleta de dados do checklist
        checklist_status = self.checklist_service.get_checklist_status(
            vehicle_id)
        failed_items = self.checklist_service.get_failed_items(vehicle_id)

        # Coleta de dados de rotas percorridas
        # Garantir que tolls seja numérico
        tolls = float(route_data['toll_cost'])

        # Gerando o relatório consolidado
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

        # Incluir status de manutenção preventiva
        report += f"Manutenção Preventiva Pendente: {
            'Sim' if maintenance_due else 'Não'}\n"

        # Incluir dados de rotas percorridas
        report += f"Distância Total Percorrida: {total_distance} km\n"
        report += f"Custo de Pedágios: R$ {tolls:.2f}\n"

        return report  # Retorna o relatório gerado

    def get_current_quilometragem(self, vehicle_id: str) -> int:
        """
        Simula a obtenção da quilometragem atual do veículo.
        """
        # Exemplo simples
        return 25000
