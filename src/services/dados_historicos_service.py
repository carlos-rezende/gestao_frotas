import json
import os


class HistoricalDataStorage:
    def __init__(self, storage_file="data/processed/historico_frota.json"):
        self.storage_file = storage_file
        # Se o arquivo não existir, crie um arquivo vazio
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({}, f)

    def load_history(self) -> dict:
        """
        Carrega o histórico de dados do arquivo JSON.
        Retorna um dicionário vazio se o arquivo estiver vazio ou corrompido.
        """
        try:
            with open(self.storage_file, 'r') as f:
                # Verifica se o arquivo está vazio
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_history(self, vehicle_id: str, route_data: dict) -> None:
        """
        Salva o histórico de uma rota para um veículo no arquivo de armazenamento.
        """
        history = self.load_history()
        if vehicle_id not in history:
            history[vehicle_id] = []
        history[vehicle_id].append(route_data)

        with open(self.storage_file, 'w') as f:
            json.dump(history, f, indent=4)

    def get_vehicle_history(self, vehicle_id: str) -> list:
        """
        Retorna o histórico de um veículo específico.
        """
        history = self.load_history()
        return history.get(vehicle_id, [])
