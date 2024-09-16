import streamlit as st
from datetime import datetime
from src.services.multas_service import TrafficFineService

# Instancia o serviço de multas
traffic_fine_service = TrafficFineService()


def multas():
    st.title("Gerenciamento de Multas")

    # Opções do menu
    menu_option = st.selectbox("Escolha uma opção:", [
                               "Registrar Multa", "Consultar Multas", "Relatório de Multas"])

    # Opção 1: Registrar Multa
    if menu_option == "Registrar Multa":
        st.header("Registrar Multa")

        vehicle_id = st.text_input("ID do Veículo:")
        driver_id = st.text_input("ID do Motorista:")
        date = st.date_input("Data da Multa:", datetime.now())
        type_of_infringement = st.text_input("Tipo de Infração:")
        penalty_points = st.number_input(
            "Pontos da Multa:", min_value=0, max_value=20, step=1)
        fine_amount = st.number_input(
            "Valor da Multa (R$):", min_value=0.0, step=0.01)

        if st.button("Registrar Multa"):
            if vehicle_id and driver_id and type_of_infringement:
                # Registrar multa
                traffic_fine_service.register_fine(
                    vehicle_id=vehicle_id,
                    driver_id=driver_id,
                    date=date.strftime("%Y-%m-%d"),
                    type_of_infringement=type_of_infringement,
                    penalty_points=int(penalty_points),
                    fine_amount=float(fine_amount)
                )
                st.success("Multa registrada com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

    # Opção 2: Consultar Multas
    elif menu_option == "Consultar Multas":
        st.header("Consultar Multas")

        vehicle_id = st.text_input("ID do Veículo (opcional):")
        driver_id = st.text_input("ID do Motorista (opcional):")

        if st.button("Calcular Multas"):
            if vehicle_id or driver_id:
                total_fines = traffic_fine_service.calculate_total_fines(
                    vehicle_id=vehicle_id, driver_id=driver_id)
                st.write(f"**Total de Pontos:** {total_fines['total_points']}")
                st.write(
                    f"**Total de Multas:** R$ {total_fines['total_fines']:.2f}")
            else:
                st.error("Por favor, insira o ID do veículo ou do motorista.")

    # Opção 3: Relatório de Multas
    elif menu_option == "Relatório de Multas":
        st.header("Relatório de Multas")
        report = traffic_fine_service.generate_fine_report()
        st.text(report)

    # Integração com a API do DETRAN (Futuro)
    # Aqui você pode adicionar uma seção que futuramente integrará com a API do DETRAN
    # para buscar automaticamente multas registradas.
    # Exemplo (fictício):
    # if st.button("Consultar Multas no DETRAN"):
    #     detran_data = fetch_detran_fines(vehicle_id, driver_id)
    #     st.write(detran_data)
