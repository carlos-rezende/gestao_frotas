

from src.services.reporte_performace_service import PerformanceReportService


class AlertService:
    def __init__(self, performance_report_service: PerformanceReportService):
        self.performance_report_service = performance_report_service

    def check_for_alerts(self, vehicle_id: str, driver_id: str, last_maintenance_quilometragem: int, maintenance_interval: int) -> list:
        """
        Verifica condições críticas para enviar alertas automáticos.
        """
        alerts = []

        # Verificar multas acumuladas
        fine_totals = self.performance_report_service.fine_service.calculate_total_fines(
            vehicle_id=vehicle_id, driver_id=driver_id)
        print(f"Multas: {fine_totals['total_points']} pontos")  # Debug
        if fine_totals['total_points'] > 10:
            alerts.append(f"Alerta: O motorista {driver_id} acumulou {
                          fine_totals['total_points']} pontos em multas.")

        # Verificar manutenção pendente
        current_quilometragem = self.performance_report_service.get_current_quilometragem(
            vehicle_id)
        print(f"Quilometragem atual: {current_quilometragem}, Última Manutenção: {
              last_maintenance_quilometragem}, Intervalo: {maintenance_interval}")  # Debug
        maintenance_due = self.performance_report_service.maintenance_service.check_maintenance(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval
        )
        if maintenance_due:
            alerts.append(f"Alerta: O veículo {
                          vehicle_id} está com manutenção preventiva pendente.")

        # Verificar eficiência de combustível
        efficiency_report = self.performance_report_service.analyze_fuel_efficiency(
            vehicle_id)
        print(f"Relatório de Eficiência: {efficiency_report}")  # Debug
        if "abaixo" in efficiency_report:
            alerts.append(f"Alerta: A eficiência de combustível do veículo {
                          vehicle_id} está abaixo do esperado.")

        return alerts
