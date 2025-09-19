import os

from database import bst_cidades
from lib import divider


def menu_cidades():
    """Exibe o menu de gerenciamento de cidades e gerencia as operações."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("0. Voltar ao menu principal")
        print("1. Cadastrar nova cidade")
        print("2. Consultar cidade por código")
        print("3. Alterar dados de uma cidade")  # <-- NOVO
        print("4. Listar todas as cidades")
        print("5. Excluir cidade")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_cidade()
        elif opcao == '2':
            consultar_cidade()
        elif opcao == '3':
            alterar_cidade()
        elif opcao == '4':
            listar_cidades()
        elif opcao == '5':
            excluir_cidade()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_cidade():
    """Pede os dados de uma nova cidade e a insere no sistema."""
    print("\n--- CADASTRO DE NOVA CIDADE ---")
    try:
        codigo = int(input("Código da cidade: "))

        # Busca na árvore para ver se o código já existe
        if bst_cidades.search_with_path(codigo)[0] is not None:
            print("[ERRO] Já existe uma cidade com este código.")
            return

        descricao = input("Descrição (Nome da cidade): ")
        estado = input("Estado (UF, ex: SP): ").upper()

        cidade_dic = {'codigo': codigo, 'descricao': descricao, 'estado': estado}

        bst_cidades.insert(codigo, cidade_dic)

        print("[SUCESSO] Cidade cadastrada!")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")


def consultar_cidade():
    """Pede um código e busca a cidade correspondente."""
    print("\n--- CONSULTA DE CIDADE ---")
    try:
        codigo = int(input("Digite o código da cidade a ser consultada: "))

        # A busca é SEMPRE feita na árvore, que é super rápida!
        resultado, caminho = bst_cidades.search_with_path(codigo)

        print(f"Caminho percorrido na árvore: {' -> '.join(map(str, caminho))}")

        if resultado:
            print("\n--- DADOS DA CIDADE ---")
            print(f"Código: {resultado['codigo']}")
            print(f"Descrição: {resultado['descricao']}")
            print(f"Estado: {resultado['estado']}")
        else:
            print("\nCidade não encontrada com este código.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")


def alterar_cidade():
    """Altera os dados de uma cidade existente."""
    print("\n--- ALTERAÇÃO DE DADOS DA CIDADE ---")
    try:
        codigo = int(input("Digite o código da cidade que deseja alterar: "))
        cidade_dic, _ = bst_cidades.search_with_path(codigo)
        if not cidade_dic:
            print("[ERRO] Cidade não encontrada.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        print(f"Descrição atual: {cidade_dic['descricao']}")
        nova_desc = input("Nova descrição: ")
        if nova_desc: cidade_dic['descricao'] = nova_desc

        print(f"Estado atual: {cidade_dic['estado']}")
        novo_estado = input("Novo estado (UF): ").upper()
        if novo_estado: cidade_dic['estado'] = novo_estado

        bst_cidades.write_data_to_file()
        print("\n[SUCESSO] Dados da cidade atualizados!")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def listar_cidades():
    """Lista todas as cidades cadastradas em ordem de código."""
    print("\n--- LISTAGEM DE TODAS AS CIDADES ---")

    # O metodo list_all() usa o percurso em-ordem para retornar tudo ordenado
    todas_as_cidades = bst_cidades.list_all()

    if not todas_as_cidades:
        print("Nenhuma cidade cadastrada.")
        return

    # Imprime um cabeçalho para a tabela
    print(f"{'Código':<10} | {'Descrição':<25} | {'UF':<5}")
    divider()

    for cidade in todas_as_cidades:
        print(f"{cidade['codigo']:<10} | {cidade['descricao']:<25} | {cidade['estado']:<5}")


def excluir_cidade():
    """Pede um código e exclui a cidade correspondente."""
    print("\n--- EXCLUSÃO DE CIDADE ---")
    try:
        codigo = int(input("Digite o código da cidade a ser excluída: "))

        # Primeiro, verifica se a cidade existe
        if bst_cidades.search_with_path(codigo)[0] is None:
            print("[ERRO] Não existe cidade com este código.")
            return

        # Pede confirmação
        confirmacao = input(f"Tem certeza que deseja excluir a cidade de código {codigo}? (S/N): ").upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return

        bst_cidades.delete(codigo)

        print("[SUCESSO] Cidade excluída.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")
