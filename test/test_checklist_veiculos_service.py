# Vamos implementar os testes para o módulo de checklist de veículos.

import unittest

# Simulação do serviço ChecklistService conforme implementado anteriormente


class ChecklistService:
    def __init__(self):
        self.required_items = [
            "nível de óleo", "nível de combustível", "pressão dos pneus",
            "luzes", "freios", "documentação", "extintor de incêndio", "cintos de segurança"
        ]

    def run_checklist(self, vehicle_id: str, driver_id: str, items: list) -> dict:
        approved = True
        missing_items = []
        failed_items = []

        # Mapeia os itens fornecidos para fácil verificação
        item_status = {item['nome']: item['status'] for item in items}

        # Verifica se todos os itens obrigatórios foram verificados e aprovados
        for required_item in self.required_items:
            if required_item not in item_status:
                missing_items.append(required_item)
                approved = False
            elif item_status[required_item] == "reprovado":
                failed_items.append(required_item)
                approved = False

        return {
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "approved": approved,
            "missing_items": missing_items,
            "failed_items": failed_items
        }

    def generate_checklist_report(self, checklist_result: dict) -> str:
        if checklist_result["approved"]:
            return f"Veículo {checklist_result['vehicle_id']} está APROVADO para viagem."
        else:
            report = f"Veículo {
                checklist_result['vehicle_id']} está REPROVADO para viagem.\n"
            if checklist_result["missing_items"]:
                report += f"Itens não verificados: {
                    ', '.join(checklist_result['missing_items'])}\n"
            if checklist_result["failed_items"]:
                report += f"Itens reprovados: {
                    ', '.join(checklist_result['failed_items'])}\n"
            return report


# Implementando os testes para o serviço de checklist
class TestChecklistService(unittest.TestCase):

    def setUp(self):
        self.checklist_service = ChecklistService()

    def test_checklist_approved(self):
        """
        Testa um checklist onde todos os itens foram aprovados.
        """
        items = [
            {"nome": "nível de óleo", "status": "aprovado"},
            {"nome": "nível de combustível", "status": "aprovado"},
            {"nome": "pressão dos pneus", "status": "aprovado"},
            {"nome": "luzes", "status": "aprovado"},
            {"nome": "freios", "status": "aprovado"},
            {"nome": "documentação", "status": "aprovado"},
            {"nome": "extintor de incêndio", "status": "aprovado"},
            {"nome": "cintos de segurança", "status": "aprovado"}
        ]

        checklist_result = self.checklist_service.run_checklist(
            "V001", "D001", items)
        self.assertTrue(checklist_result['approved'])
        self.assertEqual(len(checklist_result['missing_items']), 0)
        self.assertEqual(len(checklist_result['failed_items']), 0)

    def test_checklist_with_missing_items(self):
        """
        Testa um checklist com itens faltantes.
        """
        items = [
            {"nome": "nível de óleo", "status": "aprovado"},
            {"nome": "nível de combustível", "status": "aprovado"},
            {"nome": "pressão dos pneus", "status": "aprovado"},
            {"nome": "freios", "status": "aprovado"}
        ]

        checklist_result = self.checklist_service.run_checklist(
            "V001", "D001", items)
        self.assertFalse(checklist_result['approved'])
        self.assertIn("luzes", checklist_result['missing_items'])
        self.assertIn("documentação", checklist_result['missing_items'])

    def test_checklist_with_failed_items(self):
        """
        Testa um checklist onde alguns itens foram reprovados.
        """
        items = [
            {"nome": "nível de óleo", "status": "aprovado"},
            {"nome": "nível de combustível", "status": "aprovado"},
            {"nome": "pressão dos pneus", "status": "reprovado"},
            {"nome": "freios", "status": "reprovado"},
            {"nome": "documentação", "status": "aprovado"}
        ]

        checklist_result = self.checklist_service.run_checklist(
            "V001", "D001", items)
        self.assertFalse(checklist_result['approved'])
        self.assertIn("pressão dos pneus", checklist_result['failed_items'])
        self.assertIn("freios", checklist_result['failed_items'])

    def test_generate_checklist_report_approved(self):
        """
        Testa a geração de relatório quando o checklist é aprovado.
        """
        checklist_result = {
            "vehicle_id": "V001",
            "driver_id": "D001",
            "approved": True,
            "missing_items": [],
            "failed_items": []
        }
        report = self.checklist_service.generate_checklist_report(
            checklist_result)
        self.assertEqual(report, "Veículo V001 está APROVADO para viagem.")

    def test_generate_checklist_report_failed(self):
        """
        Testa a geração de relatório quando o checklist é reprovado.
        """
        checklist_result = {
            "vehicle_id": "V001",
            "driver_id": "D001",
            "approved": False,
            "missing_items": ["luzes", "extintor de incêndio"],
            "failed_items": ["freios"]
        }
        report = self.checklist_service.generate_checklist_report(
            checklist_result)
        expected_report = (
            "Veículo V001 está REPROVADO para viagem.\n"
            "Itens não verificados: luzes, extintor de incêndio\n"
            "Itens reprovados: freios\n"
        )
        self.assertEqual(report, expected_report)


# Executando os testes
unittest.TextTestRunner().run(
    unittest.TestLoader().loadTestsFromTestCase(TestChecklistService))
