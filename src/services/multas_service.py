# src/services/traffic_fine_service.py
from collections import defaultdict
from datetime import datetime


class TrafficFineService:
    def __init__(self):
        # Lista de multas registradas
        self.fines = []

    def register_fine(self, vehicle_id: str, driver_id: str, date: str, type_of_infringement: str, penalty_points: int, fine_amount: float) -> None:
        """
        Registra uma nova multa no sistema.

        :param vehicle_id: Identificador do veículo.
        :param driver_id: Identificador do motorista.
        :param date: Data da multa (no formato YYYY-MM-DD).
        :param type_of_infringement: Tipo de infração.
        :param penalty_points: Pontos aplicados na carteira do motorista.
        :param fine_amount: Valor da multa.
        """
        self.fines.append({
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "date": datetime.strptime(date, "%Y-%m-%d"),
            "type_of_infringement": type_of_infringement,
            "penalty_points": penalty_points,
            "fine_amount": fine_amount
        })

    def calculate_total_fines(self, vehicle_id: str = None, driver_id: str = None) -> dict:
        """
        Calcula o total de multas (em valor e pontos) para um veículo ou motorista.

        :param vehicle_id: Identificador do veículo (opcional).
        :param driver_id: Identificador do motorista (opcional).
        :return: Dicionário com o total de pontos e valor das multas.
        """
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
        """
        Gera um relatório detalhado com todas as multas registradas.

        :return: Relatório de multas em formato de string.
        """
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
        """
        Verifica se o motorista possui muitas multas recorrentes em um período de tempo.

        :param driver_id: Identificador do motorista.
        :param period_in_days: Período em dias para identificar multas recorrentes.
        :return: Lista de multas recorrentes.
        """
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
