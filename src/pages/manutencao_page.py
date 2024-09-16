import streamlit as st
from src.controllers.controlador_relatorio import ReportController

# Instanciar o controlador de relatórios
report_controller = ReportController()


def manutencao():
    st.title("Manutenção de Veículos")

    # Entrada para o ID do veículo
    vehicle_id = st.text_input(
        "ID do Veículo:", help="Insira o identificador único do veículo.")

    # Entrada para a quilometragem atual do veículo
    current_quilometragem = st.text_input(
        "Quilometragem Atual do Veículo:",
        help="Insira a quilometragem atual do veículo, por exemplo, 11.000 ou 15000."
    )

    # Formatar a quilometragem atual
    try:
        current_quilometragem = int(current_quilometragem.replace('.', ''))
    except ValueError:
        current_quilometragem = None

    # Entrada para o intervalo de manutenção
    maintenance_interval = st.text_input(
        "Intervalo de Manutenção (em km):",
        help="Insira a quilometragem recomendada para manutenção, por exemplo, 10.000 ou 20000."
    )

    # Formatar o intervalo de manutenção
    try:
        maintenance_interval = int(maintenance_interval.replace('.', ''))
    except ValueError:
        maintenance_interval = None

    # Botão para verificar se a manutenção é necessária
    if st.button("Verificar Necessidade de Manutenção"):
        if vehicle_id and current_quilometragem is not None and maintenance_interval is not None:
            # Verificar se a manutenção é necessária
            maintenance_due = report_controller.check_maintenance_due(
                vehicle_id=vehicle_id,
                current_quilometragem=current_quilometragem,
                maintenance_interval=maintenance_interval
            )

            # Exibir o resultado
            if maintenance_due:
                st.warning(f"O veículo {vehicle_id} precisa de manutenção.")
            else:
                st.success(
                    f"O veículo {vehicle_id} não precisa de manutenção no momento.")
        else:
            st.error("Por favor, insira todos os campos corretamente.")
