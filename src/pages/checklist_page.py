import streamlit as st
from src.services.checklist_veiculos_service import ChecklistService

checklist_service = ChecklistService()


def checklist():
    st.title("Checklist de Veículo")

    # Entrada para o ID do veículo
    vehicle_id = st.text_input("ID do Veículo:")

    # Entrada para o ID do motorista
    driver_id = st.text_input("ID do Motorista:")

    # Simular itens de checklist para o formulário
    checklist_items = [
        {"nome": "Pneus", "status": st.selectbox(
            "Pneus:", ["aprovado", "reprovado"], key="pneus")},
        {"nome": "Freios", "status": st.selectbox(
            "Freios:", ["aprovado", "reprovado"], key="freios")},
        {"nome": "Luzes", "status": st.selectbox(
            "Luzes:", ["aprovado", "reprovado"], key="luzes")},
        {"nome": "Óleo", "status": st.selectbox(
            "Óleo:", ["aprovado", "reprovado"], key="oleo")},
    ]

    # Botão para executar o checklist
    if st.button("Executar Checklist"):
        if vehicle_id and driver_id:
            # Executa o checklist e obtém o resultado
            checklist_result = checklist_service.run_checklist(
                vehicle_id, driver_id, checklist_items)

            # Exibe o resultado do checklist
            if checklist_result["approved"]:
                st.success("Checklist aprovado!")
            else:
                st.error("Checklist reprovado!")
                st.write("Itens reprovados:")
                for item in checklist_result["failed_items"]:
                    st.write(f"- {item}")
        else:
            st.error("Por favor, insira o ID do veículo e do motorista.")

    # Seção para mostrar o status do último checklist
    st.subheader("Status do Último Checklist")
    if vehicle_id:
        status = checklist_service.get_checklist_status(
            vehicle_id)  # Corrigido para usar a instância do serviço
        st.write(f"Status do veículo {vehicle_id}: {status}")

        # Se houver itens reprovados, mostrá-los
        if status == "Reprovado":
            failed_items = checklist_service.get_failed_items(
                vehicle_id)  # Corrigido para usar a instância do serviço
            if failed_items:
                st.write("Itens reprovados no último checklist:")
                for item in failed_items:
                    st.write(f"- {item}")
