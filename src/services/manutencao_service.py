
class MaintenanceService:
    def __init__(self):
        pass

    def check_maintenance(self, current_quilometragem: int, last_maintenance_quilometragem: int, maintenance_interval: int) -> bool:
        """
        Verifica se o veículo precisa de manutenção preventiva com base na quilometragem.
        """
        if current_quilometragem < 0 or last_maintenance_quilometragem < 0 or maintenance_interval <= 0:
            raise ValueError(
                "Os valores de quilometragem e o intervalo de manutenção devem ser positivos.")

        return current_quilometragem - last_maintenance_quilometragem >= maintenance_interval

    def generate_maintenance_alert(self, current_quilometragem: int, last_maintenance_quilometragem: int, maintenance_interval: int) -> str:
        """
        Gera um alerta se a quilometragem estiver próxima da próxima manutenção.
        """
        quilometragem_until_maintenance = maintenance_interval - \
            (current_quilometragem - last_maintenance_quilometragem)

        if quilometragem_until_maintenance <= 0:
            return "Atenção: o veículo já passou do limite para a próxima manutenção!"
        elif quilometragem_until_maintenance <= 1000:
            return f"Atenção: a próxima manutenção está próxima. Faltam {quilometragem_until_maintenance} km."
        else:
            return f"Manutenção OK. Faltam {quilometragem_until_maintenance} km para a próxima manutenção."

    def log_corrective_maintenance(self, vehicle_id: str, description: str) -> str:
        """
        Registra uma manutenção corretiva para o veículo.
        """
        return f"Manutenção corretiva registrada para o veículo {vehicle_id}: {description}"
