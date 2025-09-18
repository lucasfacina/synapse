import os

from database import bst_consultas, bst_medicos, bst_especialidades, bst_pacientes, bst_exames, bst_cidades
from lib import format_date_to_save, format_date_to_print
from menu.especialidades import listar_especialidades
from menu.medicos import listar_medicos


def menu_relatorios():
    """Exibe o menu de relatórios."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- RELATÓRIOS E FATURAMENTO ---")
        print("1. Faturamento por Dia")
        print("2. Faturamento por Período")
        print("3. Faturamento por Médico")
        print("4. Faturamento por Especialidade")
        print("5. Relatório Geral de Consultas")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            relatorio_faturamento_dia()
        elif opcao == '2':
            relatorio_faturamento_periodo()
        elif opcao == '3':
            relatorio_faturamento_medico()
        elif opcao == '4':
            relatorio_faturamento_especialidade()
        elif opcao == '5':
            relatorio_geral_consultas()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def relatorio_faturamento_dia():
    """Exibe o faturamento total para um dia específico (Requisito 6.1)."""
    print("\n--- FATURAMENTO POR DIA ---")
    data_usuario = input("Digite a data (DD/MM/AAAA): ")
    data_busca = format_date_to_save(data_usuario)
    if not data_busca:
        print("[ERRO] Formato de data inválido.")
        return
    total_faturado = 0

    todas_consultas = bst_consultas.list_all()
    for consulta in todas_consultas:
        if consulta['data'] == data_busca:
            total_faturado += consulta['valor_total']

    print(f"\nFaturamento total para o dia {data_usuario}: R$ {total_faturado:.2f}")


def relatorio_faturamento_periodo():
    """Exibe o faturamento total para um período (Requisito 6.2)."""
    print("\n--- FATURAMENTO POR PERÍODO ---")
    data_inicio_usuario = input("Digite a data inicial (DD/MM/AAAA): ")
    data_inicio = format_date_to_save(data_inicio_usuario)

    data_fim_usuario = input("Digite a data final (DD/MM/AAAA): ")
    data_fim = format_date_to_save(data_fim_usuario)

    if not data_inicio or not data_fim:
        print("[ERRO] Formato de data inválido.")
        return
    total_faturado = 0

    todas_consultas = bst_consultas.list_all()
    for consulta in todas_consultas:
        if data_inicio <= consulta['data'] <= data_fim:
            total_faturado += consulta['valor_total']

    print(f"\nFaturamento total de {data_inicio_usuario} a {data_fim_usuario}: R$ {total_faturado:.2f}")


def relatorio_faturamento_medico():
    """Exibe o faturamento total para um médico específico (Requisito 6.3)."""
    print("\n--- FATURAMENTO POR MÉDICO ---")
    try:
        listar_medicos()  # Mostra a lista de médicos para o usuário
        cod_medico = int(input("\nDigite o código do médico: "))
        medico = bst_medicos.search_with_path(cod_medico)[0]
        if not medico:
            print("Médico não encontrado.")
            return

        total_faturado = 0
        todas_consultas = bst_consultas.list_all()
        for consulta in todas_consultas:
            if consulta['cod_medico'] == cod_medico:
                total_faturado += consulta['valor_total']

        print(f"\nFaturamento total para o Dr(a). {medico['nome']}: R$ {total_faturado:.2f}")

    except ValueError:
        print("[ERRO] O código deve ser um número.")


def relatorio_faturamento_especialidade():
    """Exibe o faturamento total para uma especialidade (Requisito 6.4)."""
    print("\n--- FATURAMENTO POR ESPECIALIDADE ---")
    try:
        listar_especialidades()  # Mostra a lista para o usuário
        cod_especialidade = int(input("\nDigite o código da especialidade: "))
        especialidade = bst_especialidades.search_with_path(cod_especialidade)[0]
        if not especialidade:
            print("Especialidade não encontrada.")
            return

        total_faturado = 0
        todas_consultas = bst_consultas.list_all()
        for consulta in todas_consultas:
            # Precisamos buscar o médico da consulta para saber sua especialidade
            medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
            if medico and medico['codigo_especialidade'] == cod_especialidade:
                total_faturado += consulta['valor_total']

        print(f"\nFaturamento total para a especialidade '{especialidade['descricao']}': R$ {total_faturado:.2f}")

    except ValueError:
        print("[ERRO] O código deve ser um número.")


def relatorio_geral_consultas():
    """Exibe um relatório completo de todas as consultas (Requisito 7)."""
    print("\n" + "=" * 80)
    print("RELATÓRIO GERAL DE CONSULTAS".center(80))
    print("=" * 80)

    consultas = bst_consultas.list_all()
    if not consultas:
        print("\nNenhuma consulta para exibir.".center(80))
        print("=" * 80)
        return

    # Usamos um 'set' para contar pacientes únicos automaticamente
    pacientes_atendidos = set()
    valor_total_geral = 0

    # Cabeçalho
    print(
        f"\n{'Cód.':<5} | {'Data':<12} | {'Paciente':<20} | {'Cidade':<15} | {'Médico':<20} | {'Exame':<20} | {'Valor'}")
    print("-" * 115)  # Ajuste na largura

    for consulta in consultas:
        # Buscas cruzadas para obter os nomes
        paciente = bst_pacientes.search_with_path(consulta['cod_paciente'])[0]
        medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
        exame = bst_exames.search_with_path(consulta['cod_exame'])[0]
        cidade = bst_cidades.search_with_path(paciente['codigo_cidade'])[0] if paciente else None

        # Prepara as strings para exibição
        nome_paciente = paciente['nome'][:18] if paciente else "N/A"
        nome_cidade = cidade['descricao'][:13] if cidade else "N/A"
        nome_medico = medico['nome'][:18] if medico else "N/A"
        desc_exame = exame['descricao'][:18] if exame else "N/A"
        valor_pago = consulta['valor_total']

        # MUDANÇA AQUI: Formatando a data para exibição
        data_formatada = format_date_to_print(consulta['data'])

        # MUDANÇA AQUI: Adicionada a data_formatada na linha impressa
        print(
            f"{consulta['codigo']:<5} | {data_formatada:<12} | {nome_paciente:<20} | {nome_cidade:<15} | {nome_medico:<20} | {desc_exame:<20} | R$ {valor_pago:<8.2f}")

        # Adiciona aos totais
        pacientes_atendidos.add(consulta['cod_paciente'])
        valor_total_geral += valor_pago

    # Rodapé com os totais
    print("-" * 115)
    print(f"RESUMO GERAL:")
    print(f"  -> Quantidade total de pacientes únicos atendidos: {len(pacientes_atendidos)}")
    print(f"  -> Valor total a ser pago pelos pacientes: R$ {valor_total_geral:.2f}")
    print("=" * 115)
