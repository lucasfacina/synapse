import os

from database import bst_exames, bst_especialidades
from lib import divider


def menu_exames():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR EXAMES ---")
        print("0. Voltar ao menu principal")
        print("1. Cadastrar novo exame")
        print("2. Consultar exame por código")
        print("3. Alterar dados de um exame")
        print("4. Listar todos os exames")
        print("5. Excluir exame")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '0':
                break
            case '1':
                incluir_exame()
            case '2':
                consultar_exame()
            case '3':
                alterar_exame()
            case '4':
                listar_exames()
            case '5':
                excluir_exame()
            case _:
                print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_exame():
    print("\n--- CADASTRO DE NOVO EXAME ---")
    try:
        codigo = int(input("Código do exame: "))
        if bst_exames.search_with_path(codigo)[0]:
            print("[ERRO] Código de exame já existe.")
            return

        descricao = input("Descrição do exame: ")

        while True:
            cod_especialidade = int(input("Código da especialidade associada: "))
            especialidade = bst_especialidades.search_with_path(cod_especialidade)[0]
            if especialidade:
                print(f"--> Especialidade: {especialidade['descricao']}")
                break
            print("[ERRO] Código de especialidade inválido.")

        valor = float(input("Valor do exame (R$): "))

        exame_dic = {
            'codigo': codigo,
            'descricao': descricao,
            'codigo_especialidade': cod_especialidade,
            'valor': valor
        }
        bst_exames.insert(codigo, exame_dic)

        print("[SUCESSO] Exame cadastrado!")

    except ValueError:
        print("[ERRO] Verifique se os valores numéricos estão corretos.")


def consultar_exame():
    print("\n--- CONSULTA DE EXAME ---")
    try:
        codigo = int(input("Digite o código do exame: "))
        exame = bst_exames.search_with_path(codigo)[0]
        if not exame:
            print("Exame não encontrado.")
            return

        especialidade = bst_especialidades.search_with_path(exame['codigo_especialidade'])[0]
        nome_especialidade = especialidade['descricao'] if especialidade else "N/A"

        print(f"\nCódigo: {exame['codigo']}")
        print(f"Descrição: {exame['descricao']}")
        print(f"Especialidade: {nome_especialidade}")
        print(f"Valor do Exame: R$ {exame['valor']:.2f}")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def alterar_exame():
    print("\n--- ALTERAÇÃO DE DADOS DO EXAME ---")
    try:
        codigo = int(input("Digite o código do exame a alterar: "))
        exame_dic, _ = bst_exames.search_with_path(codigo)
        if not exame_dic:
            print("[ERRO] Exame não encontrado.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        print(f"Descrição atual: {exame_dic['descricao']}")
        nova_desc = input("Nova descrição: ")
        if nova_desc: exame_dic['descricao'] = nova_desc

        print(f"Valor atual: {exame_dic['valor']}")
        novo_valor = input("Novo valor (R$): ")
        if novo_valor: exame_dic['valor'] = float(novo_valor)

        bst_exames.write_data_to_file()
        print("\n[SUCESSO] Dados do exame atualizados!")
    except ValueError:
        print("[ERRO] Verifique os valores numéricos.")


def listar_exames():
    print("\n--- LISTAGEM DE EXAMES ---")
    lista = bst_exames.list_all()
    if not lista:
        print("Nenhum exame cadastrado.")
        return

    print(f"{'Código':<10} | {'Descrição':<30} | {'Especialidade':<25}")
    divider()
    for exame in lista:
        especialidade = bst_especialidades.search_with_path(exame['codigo_especialidade'])[0]
        nome_especialidade = especialidade['descricao'] if especialidade else "N/A"
        print(f"{exame['codigo']:<10} | {exame['descricao']:<30} | {nome_especialidade:<25}")


def excluir_exame():
    print("\n--- EXCLUSÃO DE EXAME ---")
    try:
        codigo = int(input("Digite o código do exame a ser excluído: "))
        if not bst_exames.search_with_path(codigo)[0]:
            print("[ERRO] Exame não encontrado.")
            return

        confirm = input(f"Tem certeza que deseja excluir o exame de código {codigo}? (S/N): ").upper()
        if confirm == 'S':
            bst_exames.delete(codigo)
            print("[SUCESSO] Exame excluído.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")
