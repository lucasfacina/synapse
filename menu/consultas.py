import os

from database import bst_pacientes, bst_medicos, bst_exames, bst_especialidades, bst_diarias, bst_consultas, bst_cidades
from lib import format_date_to_save, format_date_to_print, divider


def menu_consultas():
    """Exibe o menu de gerenciamento de consultas."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR CONSULTAS ---")
        print("1. Agendar nova consulta")
        print("2. Consultar detalhes de uma consulta")
        print("3. Listar todas as consultas")  # <-- NOVA OPÇÃO
        print("4. Excluir uma consulta")  # <-- NOVA OPÇÃO
        print("5. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_consulta()
        elif opcao == '2':
            consultar_consulta()
        elif opcao == '3':
            listar_consultas()  # <-- NOVO ELIF
        elif opcao == '4':
            excluir_consulta()  # <-- NOVO ELIF
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_consulta():
    """Agenda uma nova consulta, aplicando todas as regras de negócio."""
    print("\n--- AGENDAMENTO DE NOVA CONSULTA ---")
    try:
        # 1. Validação dos dados de entrada com feedback para o usuário
        cod_paciente = int(input("Código do Paciente: "))
        paciente = bst_pacientes.search_with_path(cod_paciente)[0]
        if not paciente: print("[ERRO] Paciente não encontrado."); return
        print(f"--> Paciente selecionado: {paciente['nome']}")  # <-- FEEDBACK ADICIONADO

        cod_medico = int(input("Código do Médico: "))
        medico = bst_medicos.search_with_path(cod_medico)[0]
        if not medico: print("[ERRO] Médico não encontrado."); return
        print(f"--> Médico selecionado: {medico['nome']}")  # <-- FEEDBACK ADICIONADO

        cod_exame = int(input("Código do Exame: "))
        exame = bst_exames.search_with_path(cod_exame)[0]
        if not exame: print("[ERRO] Exame não encontrado."); return
        print(f"--> Exame selecionado: {exame['descricao']}")  # <-- FEEDBACK ADICIONADO

        while True:
            data_usuario = input("Data da consulta (DD/MM/AAAA): ")
            data_salvar = format_date_to_save(data_usuario)
            if data_salvar:
                break
            print("[ERRO] Formato de data inválido. Use DD/MM/AAAA.")

        hora = input("Hora da consulta (HH:MM): ")

        # O restante da função continua exatamente o mesmo...
        # 2. Verificar vagas (Requisito 5.1)
        cod_especialidade = medico['codigo_especialidade']
        especialidade = bst_especialidades.search_with_path(cod_especialidade)[0]

        chave_diaria = f"{data_salvar}_{cod_especialidade}"
        diaria = bst_diarias.search_with_path(chave_diaria)[0]

        qtd_consultas_dia = diaria['quantidade'] if diaria else 0

        if qtd_consultas_dia >= especialidade['limite']:
            print(f"[ERRO] Limite de consultas para a especialidade '{especialidade['descricao']}' atingido neste dia.")
            return

        # 3. Calcular valor total (Requisito 5.2)
        valor_total = especialidade['valor'] + exame['valor']
        print(f"Valor total (Consulta + Exame): R$ {valor_total:.2f}")

        # 4. Salvar a consulta
        cod_consulta = int(input("Defina um código para esta consulta: "))
        if bst_consultas.search_with_path(cod_consulta)[0]:
            print("[ERRO] Código de consulta já existe.")
            return

        consulta_dic = {
            'codigo': cod_consulta, 'cod_paciente': cod_paciente, 'cod_medico': cod_medico,
            'cod_exame': cod_exame, 'data': data_salvar, 'hora': hora, 'valor_total': valor_total
        }
        bst_consultas.insert(cod_consulta, consulta_dic)

        # 5. Atualizar a tabela Diárias (Requisito 5.3)
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
    """Mostra os detalhes de uma consulta, com nomes em vez de códigos (Requisito 5)."""
    print("\n--- DETALHES DA CONSULTA ---")
    try:
        cod_consulta = int(input("Código da consulta: "))
        consulta = bst_consultas.search_with_path(cod_consulta)[0]
        if not consulta:
            print("Consulta não encontrada.")
            return

        # Realiza todas as buscas cruzadas
        paciente = bst_pacientes.search_with_path(consulta['cod_paciente'])[0]
        cidade_paciente = bst_cidades.search_with_path(paciente['codigo_cidade'])[0] if paciente else None
        medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
        exame = bst_exames.search_with_path(consulta['cod_exame'])[0]

        # Prepara os nomes para exibição
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
        print(f"Valor a Pagar: R$ {consulta['valor_total']:.2f}")

    except ValueError:
        print("[ERRO] O código da consulta deve ser um número.")


def listar_consultas():
    """Lista todas as consultas agendadas."""
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
        print(f"{consulta['codigo']:<10} | {data_formatada:<12} | {nome_paciente:<25} | {nome_medico:<25}")


def excluir_consulta():
    """Exclui uma consulta e decrementa a contagem diária da especialidade (Requisito 5.4)."""
    print("\n--- EXCLUSÃO DE CONSULTA ---")
    try:
        cod_consulta = int(input("Digite o código da consulta a ser excluída: "))
        consulta = bst_consultas.search_with_path(cod_consulta)[0]
        if not consulta:
            print("[ERRO] Consulta não encontrada.")
            return

        # Passo 1: Obter os dados necessários ANTES de apagar a consulta
        data_consulta = consulta['data']
        cod_medico = consulta['cod_medico']
        medico = bst_medicos.search_with_path(cod_medico)[0]

        if not medico:
            print(
                "[ERRO CRÍTICO] Médico associado à consulta não foi encontrado. Não é possível ajustar a contagem diária.")
            return

        cod_especialidade = medico['codigo_especialidade']
        chave_diaria = f"{data_consulta}_{cod_especialidade}"

        # Passo 2: Pedir confirmação do usuário
        confirm = input(f"Tem certeza que deseja excluir a consulta de código {cod_consulta}? (S/N): ").upper()
        if confirm != 'S':
            print("Operação cancelada.")
            return

        # Passo 3: Excluir a consulta da árvore e do arquivo
        bst_consultas.delete(cod_consulta)
        print("[SUCESSO] Consulta removida.")

        # Passo 4: Atualizar (decrementar) a contagem na tabela Diárias
        diaria = bst_diarias.search_with_path(chave_diaria)[0]
        if diaria and diaria['quantidade'] > 0:
            diaria['quantidade'] -= 1
            # Deleta o registro antigo e insere o novo, com a contagem atualizada
            bst_diarias.delete(chave_diaria, should_write_to_file=False)
            bst_diarias.insert(chave_diaria, diaria, should_append_to_file=False)
            bst_diarias.write_data_to_file()
            print("[SUCESSO] Contagem diária de consultas foi atualizada.")
        else:
            print(
                "[AVISO] Não foi encontrado um registro de contagem diária para esta data/especialidade para decrementar.")

    except ValueError:
        print("[ERRO] O código da consulta deve ser um número.")
