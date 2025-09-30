import os

from database import bst_pacientes, bst_medicos, bst_exames, bst_especialidades, bst_diarias, bst_consultas, bst_cidades
from lib import format_date_to_save, format_date_to_print, divider


def menu_consultas():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR CONSULTAS ---")
        print("0. Voltar ao menu principal")
        print("1. Agendar nova consulta")
        print("2. Consultar detalhes de uma consulta")
        print("3. Listar todas as consultas")
        print("4. Excluir uma consulta")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '0':
                break
            case '1':
                incluir_consulta()
            case '2':
                consultar_consulta()
            case '3':
                listar_consultas()
            case '4':
                excluir_consulta()
            case _:
                print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_consulta():
    print("\n--- AGENDAMENTO DE NOVA CONSULTA ---")
    # Requisito 5
    try:
        cod_paciente = int(input("Código do Paciente: "))
        paciente = bst_pacientes.search_with_path(cod_paciente)[0]
        if not paciente: print("[ERRO] Paciente não encontrado."); return
        print(f"--> Paciente selecionado: {paciente['nome']}")

        cod_medico = int(input("Código do Médico: "))
        medico = bst_medicos.search_with_path(cod_medico)[0]
        if not medico: print("[ERRO] Médico não encontrado."); return
        print(f"--> Médico selecionado: {medico['nome']}")

        cod_exame = int(input("Código do Exame: "))
        exame = bst_exames.search_with_path(cod_exame)[0]
        if not exame: print("[ERRO] Exame não encontrado."); return
        print(f"--> Exame selecionado: {exame['descricao']}")

        while True:
            data_usuario = input("Data da consulta (DD/MM/AAAA): ")
            data_salvar = format_date_to_save(data_usuario)
            if data_salvar:
                break
            print("[ERRO] Formato de data inválido. Use DD/MM/AAAA.")

        hora = input("Hora da consulta (HH:MM): ")

        cod_especialidade = medico['codigo_especialidade']
        especialidade = bst_especialidades.search_with_path(cod_especialidade)[0]

        chave_diaria = f"{data_salvar}_{cod_especialidade}"
        diaria = bst_diarias.search_with_path(chave_diaria)[0]

        qtd_consultas_dia = diaria['quantidade'] if diaria else 0

        # Requisito 5.1
        if qtd_consultas_dia >= especialidade['limite']:
            print(f"[ERRO] Limite de consultas para a especialidade '{especialidade['descricao']}' atingido neste dia.")
            return

        valor_total = especialidade['valor'] + exame['valor']

        # Requisito 5.2
        print(f"Valor total (Consulta + Exame): R$ {valor_total:.2f}")

        cod_consulta = int(input("Defina um código para esta consulta: "))
        if bst_consultas.search_with_path(cod_consulta)[0]:
            print("[ERRO] Código de consulta já existe.")
            return

        consulta_dic = {
            'codigo': cod_consulta, 'cod_paciente': cod_paciente, 'cod_medico': cod_medico,
            'cod_exame': cod_exame, 'data': data_salvar, 'hora': hora, 'valor_total': valor_total
        }
        bst_consultas.insert(cod_consulta, consulta_dic)

        # Requisito 5.3
        if diaria:
            diaria['quantidade'] += 1
            bst_diarias.delete(chave_diaria)
            bst_diarias.insert(chave_diaria, diaria)
        else:
            nova_diaria = {'chave': chave_diaria, 'quantidade': 1}
            bst_diarias.insert(chave_diaria, nova_diaria)

        bst_diarias.write_data_to_file()
        print("[SUCESSO] Consulta agendada e contagem diária atualizada!")

    except ValueError:
        print("[ERRO] Verifique os códigos e valores numéricos.")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")


def consultar_consulta():
    print("\n--- DETALHES DA CONSULTA ---")
    # Requisito 5
    try:
        cod_consulta = int(input("Código da consulta: "))
        consulta = bst_consultas.search_with_path(cod_consulta)[0]
        if not consulta:
            print("Consulta não encontrada.")
            return

        paciente = bst_pacientes.search_with_path(consulta['cod_paciente'])[0]
        cidade_paciente = bst_cidades.search_with_path(paciente['codigo_cidade'])[0] if paciente else None
        medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
        exame = bst_exames.search_with_path(consulta['cod_exame'])[0]

        nome_paciente = paciente['nome'] if paciente else "N/A"
        nome_cidade_paciente = cidade_paciente['descricao'] if cidade_paciente else "N/A"
        nome_medico = medico['nome'] if medico else "N/A"
        desc_exame = exame['descricao'] if exame else "N/A"

        print(f"\nCódigo da Consulta: {consulta['codigo']}")
        data_formatada = format_date_to_print(consulta['data'])
        print(f"Data: {data_formatada}  Hora: {consulta['hora']}")
        divider()
        print(f"Paciente: {nome_paciente} (Cidade: {nome_cidade_paciente})")
        print(f"Médico: {nome_medico}")
        print(f"Exame: {desc_exame}")
        divider()
        # Requisito 5.2
        print(f"Valor a Pagar: R$ {consulta['valor_total']:.2f}")

    except ValueError:
        print("[ERRO] O código da consulta deve ser um número.")


def listar_consultas():
    print("\n--- LISTAGEM DE CONSULTAS AGENDADAS ---")
    lista = bst_consultas.list_all()
    if not lista:
        print("Nenhuma consulta agendada.")
        return

    print(f"{'Código':<10} | {'Data':<12} | {'Paciente':<25} | {'Médico':<25}")
    divider()
    for consulta in lista:
        paciente = bst_pacientes.search_with_path(consulta['cod_paciente'])[0]
        medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
        nome_paciente = paciente['nome'] if paciente else "N/A"
        nome_medico = medico['nome'] if medico else "N/A"

        data_formatada = format_date_to_print(consulta['data'])
        # Requisito 5
        print(f"{consulta['codigo']:<10} | {data_formatada:<12} | {nome_paciente:<25} | {nome_medico:<25}")


def excluir_consulta():
    print("\n--- EXCLUSÃO DE CONSULTA ---")
    try:
        cod_consulta = int(input("Digite o código da consulta a ser excluída: "))
        consulta = bst_consultas.search_with_path(cod_consulta)[0]
        if not consulta:
            print("[ERRO] Consulta não encontrada.")
            return

        data_consulta = consulta['data']
        cod_medico = consulta['cod_medico']
        medico = bst_medicos.search_with_path(cod_medico)[0]

        if not medico:
            print(
                "[ERRO CRÍTICO] Médico associado à consulta não foi encontrado. Não é possível ajustar a contagem diária.")
            return

        cod_especialidade = medico['codigo_especialidade']
        chave_diaria = f"{data_consulta}_{cod_especialidade}"

        confirmacao = input(f"Tem certeza que deseja excluir a consulta de código {cod_consulta}? (S/N): ").upper()
        if confirmacao.lower() != 's':
            print("Operação cancelada.")
            return

        bst_consultas.delete(cod_consulta)
        print("[SUCESSO] Consulta removida.")

        diaria = bst_diarias.search_with_path(chave_diaria)[0]
        if diaria and diaria['quantidade'] > 0:

            # Requisito 5.4
            diaria['quantidade'] -= 1

            bst_diarias.delete(chave_diaria, should_write_to_file=False)
            bst_diarias.insert(chave_diaria, diaria, should_append_to_file=False)
            bst_diarias.write_data_to_file()
            print("[SUCESSO] Contagem diária de consultas foi atualizada.")
        else:
            print(
                "[AVISO] Não foi encontrado um registro de contagem diária para esta data/especialidade para decrementar.")

    except ValueError:
        print("[ERRO] O código da consulta deve ser um número.")
