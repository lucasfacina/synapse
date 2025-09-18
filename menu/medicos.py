import os

from database import bst_medicos, bst_cidades, bst_especialidades


def menu_medicos():
    """Exibe o menu de gerenciamento de médicos."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR MÉDICOS ---")
        print("1. Cadastrar novo médico")
        print("2. Consultar médico por código")
        print("3. Alterar dados de um médico")  # <-- NOVO
        print("4. Listar todos os médicos")
        print("5. Excluir médico")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_medico()
        elif opcao == '2':
            consultar_medico()
        elif opcao == '3':
            alterar_medico()
        elif opcao == '4':
            listar_medicos()
        elif opcao == '5':
            excluir_medico()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_medico():
    """Cadastra um novo médico no sistema."""
    print("\n--- CADASTRO DE NOVO MÉDICO ---")
    try:
        codigo = int(input("Código do médico: "))
        if bst_medicos.search_with_path(codigo)[0]:
            print("[ERRO] Código de médico já existe.")
            return

        nome = input("Nome do médico: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")

        while True:
            cod_cidade = int(input("Código da cidade: "))
            cidade = bst_cidades.search_with_path(cod_cidade)[0]
            if cidade:
                print(f"--> Cidade: {cidade['descricao']}")
                break
            print("[ERRO] Código de cidade inválido.")

        while True:
            cod_especialidade = int(input("Código da especialidade: "))
            especialidade = bst_especialidades.search_with_path(cod_especialidade)[0]
            if especialidade:
                print(f"--> Especialidade: {especialidade['descricao']}")
                break
            print("[ERRO] Código de especialidade inválido.")

        medico_dic = {
            'codigo': codigo, 'nome': nome, 'endereco': endereco,
            'telefone': telefone, 'codigo_cidade': cod_cidade,
            'codigo_especialidade': cod_especialidade
        }
        bst_medicos.insert(codigo, medico_dic)

        print("[SUCESSO] Médico cadastrado!")

    except ValueError:
        print("[ERRO] Verifique se os códigos são números válidos.")


def consultar_medico():
    """Consulta um médico e exibe seus dados, incluindo cidade e especialidade."""
    print("\n--- CONSULTA DE MÉDICO ---")
    try:
        codigo = int(input("Digite o código do médico: "))
        medico, _ = bst_medicos.search_with_path(codigo)
        if not medico:
            print("Médico não encontrado.")
            return

        # Busca cruzada #1: Cidade
        cidade = bst_cidades.search_with_path(medico['codigo_cidade'])[0]
        nome_cidade = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

        # Busca cruzada #2: Especialidade (Requisito 3 e 3.1)
        especialidade = bst_especialidades.search_with_path(medico['codigo_especialidade'])[0]

        print("\n--- DADOS DO MÉDICO ---")
        print(f"Código: {medico['codigo']}")
        print(f"Nome: {medico['nome']}")
        print(f"Endereço: {medico['endereco']}")
        print(f"Telefone: {medico['telefone']}")
        print(f"Cidade: {nome_cidade}")
        if especialidade:
            print(f"Especialidade: {especialidade['descricao']}")
            print(f"Valor da Consulta: R$ {especialidade['valor']:.2f}")
            print(f"Limite Diário de Atendimentos: {especialidade['limite']}")
        else:
            print("Especialidade: N/A")

    except ValueError:
        print("[ERRO] O código deve ser um número.")


def alterar_medico():
    """Altera os dados de um médico existente."""
    print("\n--- ALTERAÇÃO DE DADOS DO MÉDICO ---")
    try:
        codigo = int(input("Digite o código do médico a alterar: "))
        medico_dic, _ = bst_medicos.search_with_path(codigo)
        if not medico_dic:
            print("[ERRO] Médico não encontrado.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        print(f"Nome atual: {medico_dic['nome']}")
        novo_nome = input("Novo nome: ")
        if novo_nome: medico_dic['nome'] = novo_nome

        print(f"Endereço atual: {medico_dic['endereco']}")
        novo_endereco = input("Novo endereço: ")
        if novo_endereco: medico_dic['endereco'] = novo_endereco

        print(f"Telefone atual: {medico_dic['telefone']}")
        novo_telefone = input("Novo telefone: ")
        if novo_telefone: medico_dic['telefone'] = novo_telefone

        # Aqui poderíamos adicionar a lógica para alterar cidade e especialidade,
        # com as devidas validações, mas manteremos simples por enquanto.

        bst_medicos.write_data_to_file()
        print("\n[SUCESSO] Dados do médico atualizados!")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def listar_medicos():
    """Lista todos os médicos, mostrando cidade e especialidade."""
    print("\n--- LISTAGEM DE MÉDICOS ---")
    lista = bst_medicos.list_all()
    if not lista:
        print("Nenhum médico cadastrado.")
        return

    print(f"{'Código':<10} | {'Nome':<30} | {'Especialidade':<25} | {'Cidade - UF':<25}")
    print("-" * 100)
    for medico in lista:
        especialidade = bst_especialidades.search_with_path(medico['codigo_especialidade'])[0]
        nome_especialidade = especialidade['descricao'] if especialidade else "N/A"

        # 2. Lógica adicionada para buscar a cidade e o estado
        cidade = bst_cidades.search_with_path(medico['codigo_cidade'])[0]
        cidade_estado = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

        # 3. Impressão da linha com todas as informações
        print(f"{medico['codigo']:<10} | {medico['nome']:<30} | {nome_especialidade:<25} | {cidade_estado:<25}")


def excluir_medico():
    """Exclui um médico pelo código."""
    print("\n--- EXCLUSÃO DE MÉDICO ---")
    try:
        codigo = int(input("Digite o código do médico a ser excluído: "))
        if not bst_medicos.search_with_path(codigo)[0]:
            print("[ERRO] Médico não encontrado.")
            return

        confirm = input(f"Tem certeza que deseja excluir o médico de código {codigo}? (S/N): ").upper()
        if confirm == 'S':
            bst_medicos.delete(codigo)
            print("[SUCESSO] Médico excluído.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")
