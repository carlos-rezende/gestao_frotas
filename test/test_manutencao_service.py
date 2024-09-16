import unittest

from src.services.manutencao_service import MaintenanceService


class TestMaintenanceService(unittest.TestCase):

    def setUp(self):
        self.maintenance_service = MaintenanceService()

    def test_check_maintenance_needed(self):
        """
        Testa se a manutenção preventiva é necessária com base na quilometragem.
        """
        current_quilometragem = 25000
        last_maintenance_quilometragem = 15000
        maintenance_interval = 10000

        self.assertTrue(self.maintenance_service.check_maintenance(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval))

    def test_check_maintenance_not_needed(self):
        """
        Testa se a manutenção preventiva não é necessária.
        """
        current_quilometragem = 18000
        last_maintenance_quilometragem = 15000
        maintenance_interval = 10000

        self.assertFalse(self.maintenance_service.check_maintenance(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval))

    def test_check_maintenance_invalid_values(self):
        """
        Testa se a função lança exceções para valores inválidos.
        """
        with self.assertRaises(ValueError):
            self.maintenance_service.check_maintenance(-500, 15000, 10000)

        with self.assertRaises(ValueError):
            self.maintenance_service.check_maintenance(
                20000, -15000, 10000)

        with self.assertRaises(ValueError):
            self.maintenance_service.check_maintenance(
                20000, 15000, 0)

    def test_generate_maintenance_alert_close(self):
        """
        Testa se o alerta de manutenção é gerado corretamente quando a manutenção está próxima.
        """
        current_quilometragem = 19500
        last_maintenance_quilometragem = 15000
        maintenance_interval = 5000

        alert = self.maintenance_service.generate_maintenance_alert(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval)
        self.assertEqual(
            alert, "Atenção: a próxima manutenção está próxima. Faltam 500 km.")

    def test_generate_maintenance_alert_not_needed(self):
        """
        Testa se o alerta indica que a manutenção não é necessária quando há bastante quilometragem restante.
        """
        current_quilometragem = 16000
        last_maintenance_quilometragem = 15000
        maintenance_interval = 10000

        alert = self.maintenance_service.generate_maintenance_alert(
            current_quilometragem, last_maintenance_quilometragem, maintenance_interval)
        self.assertEqual(
            alert, "Manutenção OK. Faltam 9000 km para a próxima manutenção.")

    def test_log_corrective_maintenance(self):
        """
        Testa o registro de uma manutenção corretiva.
        """
        vehicle_id = "V001"
        description = "Troca da correia dentada"

        log = self.maintenance_service.log_corrective_maintenance(
            vehicle_id, description)
        self.assertEqual(log, f"Manutenção corretiva registrada para o veículo {
                         vehicle_id}: {description}")


# Reexecutando os testes após as correções nos valores
unittest.TextTestRunner().run(
    unittest.TestLoader().loadTestsFromTestCase(TestMaintenanceService))
