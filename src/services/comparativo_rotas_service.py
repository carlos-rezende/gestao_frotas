
from src.services.rotas_service import RouteService


class RouteComparisonService:
    def __init__(self, route_service: RouteService):
        self.route_service = route_service

    def compare_routes(self, vehicle_ids: list) -> str:
        """
        Compara as rotas de diferentes veículos em termos de distância, custo de pedágio e tempo de viagem.
        """
        report = "Relatório Comparativo de Rotas:\n"
        total_data = []

        for vehicle_id in vehicle_ids:
            route_data = self.route_service.get_route_data(vehicle_id)
            total_data.append({
                "vehicle_id": vehicle_id,
                "distance": route_data['distance'],
                "toll_cost": route_data['toll_cost'],
                # Exemplo, pode ser em horas
                "travel_time": route_data['travel_time']
            })

        # Gerando relatório comparativo
        for data in total_data:
            report += (
                f"Veículo {data['vehicle_id']}:\n"
                f"  Distância percorrida: {data['distance']} km\n"
                f"  Custo de pedágios: R$ {data['toll_cost']:.2f}\n"
                f"  Tempo de viagem: {data['travel_time']} horas\n"
            )

        return report
