import os

from database import bst_especialidades
from lib import divider


def menu_especialidades():
    """Exibe o menu de gerenciamento de especialidades."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR ESPECIALIDADES ---")
        print("1. Cadastrar nova especialidade")
        print("2. Consultar especialidade por código")
        print("3. Alterar dados de uma especialidade")  # <-- NOVO
        print("4. Listar todas as especialidades")
        print("5. Excluir especialidade")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_especialidade()
        elif opcao == '2':
            consultar_especialidade()
        elif opcao == '3':
            alterar_especialidade()  # <-- NOVO ELIF
        elif opcao == '4':
            listar_especialidades()
        elif opcao == '5':
            excluir_especialidade()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_especialidade():
    """Cadastra uma nova especialidade médica."""
    print("\n--- CADASTRO DE ESPECIALIDADE ---")
    try:
        codigo = int(input("Código da especialidade: "))
        if bst_especialidades.search_with_path(codigo)[0]:
            print("[ERRO] Código de especialidade já existe.")
            return

        descricao = input("Descrição: ")
        valor = float(input("Valor da consulta (R$): "))
        limite = int(input("Limite diário de consultas: "))

        especialidade_dic = {'codigo': codigo, 'descricao': descricao, 'valor': valor, 'limite': limite}
        bst_especialidades.insert(codigo, especialidade_dic)

        print("[SUCESSO] Especialidade cadastrada!")

    except ValueError:
        print("[ERRO] Verifique se os valores numéricos estão corretos.")


def consultar_especialidade():
    """Consulta uma especialidade pelo código."""
    print("\n--- CONSULTA DE ESPECIALIDADE ---")
    try:
        codigo = int(input("Digite o código da especialidade: "))
        especialidade, _ = bst_especialidades.search_with_path(codigo)
        if especialidade:
            print(f"\nCódigo: {especialidade['codigo']}")
            print(f"Descrição: {especialidade['descricao']}")
            print(f"Valor da Consulta: R$ {especialidade['valor']:.2f}")
            print(f"Limite Diário: {especialidade['limite']} consultas")
        else:
            print("Especialidade não encontrada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def alterar_especialidade():
    """Altera os dados de uma especialidade existente."""
    print("\n--- ALTERAÇÃO DE DADOS DA ESPECIALIDADE ---")
    try:
        codigo = int(input("Digite o código da especialidade a alterar: "))
        esp_dic, _ = bst_especialidades.search_with_path(codigo)
        if not esp_dic:
            print("[ERRO] Especialidade não encontrada.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        print(f"Descrição atual: {esp_dic['descricao']}")
        nova_desc = input("Nova descrição: ")
        if nova_desc: esp_dic['descricao'] = nova_desc

        print(f"Valor atual: {esp_dic['valor']}")
        novo_valor = input("Novo valor (R$): ")
        if novo_valor: esp_dic['valor'] = float(novo_valor)

        print(f"Limite diário atual: {esp_dic['limite']}")
        novo_limite = input("Novo limite diário: ")
        if novo_limite: esp_dic['limite'] = int(novo_limite)

        bst_especialidades.write_data_to_file()
        print("\n[SUCESSO] Dados da especialidade atualizados!")
    except ValueError:
        print("[ERRO] Verifique os valores numéricos.")


def listar_especialidades():
    """Lista todas as especialidades cadastradas."""
    print("\n--- LISTAGEM DE ESPECIALIDADES ---")
    lista = bst_especialidades.list_all()
    if not lista:
        print("Nenhuma especialidade cadastrada.")
        return

    print(f"{'Código':<10} | {'Descrição':<25} | {'Valor (R$)':<15} | {'Limite Diário'}")
    divider()
    for esp in lista:
        print(f"{esp['codigo']:<10} | {esp['descricao']:<25} | {esp['valor']:<15.2f} | {esp['limite']}")


def excluir_especialidade():
    """Exclui uma especialidade pelo código."""
    print("\n--- EXCLUSÃO DE ESPECIALIDADE ---")
    try:
        codigo = int(input("Digite o código da especialidade a ser excluída: "))
        if not bst_especialidades.search_with_path(codigo)[0]:
            print("[ERRO] Especialidade não encontrada.")
            return

        confirm = input(f"Tem certeza que deseja excluir a especialidade de código {codigo}? (S/N): ").upper()
        if confirm == 'S':
            bst_especialidades.delete(codigo)
            print("[SUCESSO] Especialidade excluída.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")
