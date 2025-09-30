import os

from database import bst_medicos, bst_cidades, bst_especialidades
from lib import divider


def menu_medicos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR MÉDICOS ---")
        print("0. Voltar ao menu principal")
        print("1. Cadastrar novo médico")
        print("2. Consultar médico por código")
        print("3. Alterar dados de um médico")
        print("4. Listar todos os médicos")
        print("5. Excluir médico")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '0':
                break
            case '1':
                incluir_medico()
            case '2':
                consultar_medico()
            case '3':
                alterar_medico()
            case '4':
                listar_medicos()
            case '5':
                excluir_medico()
            case _:
                print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_medico():
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
    print("\n--- CONSULTA DE MÉDICO ---")
    try:
        codigo = int(input("Digite o código do médico: "))
        medico, _ = bst_medicos.search_with_path(codigo)
        if not medico:
            print("Médico não encontrado.")
            return

        cidade = bst_cidades.search_with_path(medico['codigo_cidade'])[0]
        nome_cidade = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

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

        bst_medicos.write_data_to_file()
        print("\n[SUCESSO] Dados do médico atualizados!")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def listar_medicos():
    print("\n--- LISTAGEM DE MÉDICOS ---")
    lista = bst_medicos.list_all()
    if not lista:
        print("Nenhum médico cadastrado.")
        return

    print(f"{'Código':<10} | {'Nome':<30} | {'Especialidade':<25} | {'Cidade - UF':<25}")
    divider()
    for medico in lista:
        especialidade = bst_especialidades.search_with_path(medico['codigo_especialidade'])[0]
        nome_especialidade = especialidade['descricao'] if especialidade else "N/A"

        cidade = bst_cidades.search_with_path(medico['codigo_cidade'])[0]
        cidade_estado = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

        print(f"{medico['codigo']:<10} | {medico['nome']:<30} | {nome_especialidade:<25} | {cidade_estado:<25}")


def excluir_medico():
    print("\n--- EXCLUSÃO DE MÉDICO ---")
    try:
        codigo = int(input("Digite o código do médico a ser excluído: "))
        if not bst_medicos.search_with_path(codigo)[0]:
            print("[ERRO] Médico não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o médico de código {codigo}? (S/N): ").upper()
        if confirmacao.lower() == 's':
            bst_medicos.delete(codigo)
            print("[SUCESSO] Médico excluído.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")
