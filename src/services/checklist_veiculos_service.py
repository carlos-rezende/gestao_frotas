# src/services/checklist_service.py

class ChecklistService:
    def __init__(self):
        self.checklists = {}

    def run_checklist(self, vehicle_id: str, driver_id: str, items: list) -> dict:
        """
        Executa o checklist do veículo e registra os itens aprovados/reprovados.
        """
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

        # Salva o checklist do veículo
        self.checklists[vehicle_id] = checklist_result
        return checklist_result

    def get_checklist_status(self, vehicle_id: str) -> str:
        """
        Retorna o status do último checklist do veículo.
        """
        if vehicle_id in self.checklists:
            return "Aprovado" if self.checklists[vehicle_id]["approved"] else "Reprovado"
        return "Sem checklist registrado"

    def get_failed_items(self, vehicle_id: str) -> list:
        """
        Retorna a lista de itens reprovados no último checklist do veículo.
        """
        if vehicle_id in self.checklists:
            return self.checklists[vehicle_id]["failed_items"]
        return []
