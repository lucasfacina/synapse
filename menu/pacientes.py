import os

from database import bst_pacientes, bst_cidades
from lib import divider


def menu_pacientes():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR PACIENTES ---")
        print("0. Voltar ao menu principal")
        print("1. Cadastrar novo paciente")
        print("2. Consultar paciente por código")
        print("3. Alterar dados de um paciente")
        print("4. Listar todos os pacientes")
        print("5. Excluir paciente")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '0':
                break
            case '1':
                incluir_paciente()
            case '2':
                consultar_paciente()
            case '3':
                alterar_paciente()
            case '4':
                listar_pacientes()
            case '5':
                excluir_paciente()
            case _:
                print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_paciente():
    print("\n--- CADASTRO DE NOVO PACIENTE ---")
    try:
        codigo = int(input("Código do paciente: "))
        if bst_pacientes.search_with_path(codigo)[0] is not None:
            print("[ERRO] Já existe um paciente com este código.")
            return

        nome = input("Nome completo: ")
        nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")

        while True:
            cod_cidade = int(input("Código da cidade: "))
            cidade_encontrada, _ = bst_cidades.search_with_path(cod_cidade)
            if cidade_encontrada:
                print(f"--> Cidade selecionada: {cidade_encontrada['descricao']} - {cidade_encontrada['estado']}")
                break
            else:
                print("[ERRO] Código de cidade inválido. Tente novamente.")

        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m, ex: 1.75): "))

        paciente_dic = {
            'codigo': codigo, 'nome': nome, 'nascimento': nascimento,
            'endereco': endereco, 'telefone': telefone, 'codigo_cidade': cod_cidade,
            'peso': peso, 'altura': altura
        }

        bst_pacientes.insert(codigo, paciente_dic)

        print("[SUCESSO] Paciente cadastrado!")

    except ValueError:
        print("[ERRO] Código, peso e altura devem ser números válidos.")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")


def consultar_paciente():
    print("\n--- CONSULTA DE PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente: "))
        paciente, caminho = bst_pacientes.search_with_path(codigo)

        if not paciente:
            print("\nPaciente não encontrado.")
            return

        cod_cidade = paciente['codigo_cidade']
        cidade, _ = bst_cidades.search_with_path(cod_cidade)
        nome_cidade = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "Cidade não encontrada"

        peso = paciente['peso']
        altura = paciente['altura']

        # Requisito 2.1
        imc = peso / (altura * altura) if altura > 0 else 0

        if imc < 18.5:
            diagnostico_imc = "Abaixo do peso"
        elif 18.5 <= imc < 25:
            diagnostico_imc = "Peso normal"
        elif 25 <= imc < 30:
            diagnostico_imc = "Sobrepeso"
        else:
            diagnostico_imc = "Obesidade"

        print("\n--- DADOS DO PACIENTE ---")
        print(f"Código: {paciente['codigo']}")
        print(f"Nome: {paciente['nome']}")
        print(f"Data de Nascimento: {paciente['nascimento']}")
        print(f"Endereço: {paciente['endereco']}")
        print(f"Telefone: {paciente['telefone']}")
        print(f"Cidade: {nome_cidade}")
        print(f"Peso: {peso} kg, Altura: {altura} m")
        print(f"IMC: {imc:.2f} ({diagnostico_imc})")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")


def alterar_paciente():
    print("\n--- ALTERAÇÃO DE DADOS DO PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente que deseja alterar: "))
        paciente_dic, _ = bst_pacientes.search_with_path(codigo)

        if not paciente_dic:
            print("[ERRO] Paciente não encontrado com este código.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        print(f"Nome atual: {paciente_dic['nome']}")
        novo_nome = input("Novo nome: ")
        if novo_nome:
            paciente_dic['nome'] = novo_nome

        print(f"Nascimento atual: {paciente_dic['nascimento']}")
        novo_nascimento = input("Nova data de nascimento (DD/MM/AAAA): ")
        if novo_nascimento:
            paciente_dic['nascimento'] = novo_nascimento

        print(f"Endereço atual: {paciente_dic['endereco']}")
        novo_endereco = input("Novo endereço: ")
        if novo_endereco:
            paciente_dic['endereco'] = novo_endereco

        print(f"Telefone atual: {paciente_dic['telefone']}")
        novo_telefone = input("Novo telefone: ")
        if novo_telefone:
            paciente_dic['telefone'] = novo_telefone

        print(f"Peso atual: {paciente_dic['peso']}")
        novo_peso_str = input("Novo peso (kg): ")
        if novo_peso_str:
            paciente_dic['peso'] = float(novo_peso_str)

        print(f"Altura atual: {paciente_dic['altura']}")
        nova_altura_str = input("Nova altura (m): ")
        if nova_altura_str:
            paciente_dic['altura'] = float(nova_altura_str)

        bst_pacientes.write_data_to_file()

        print("\n[SUCESSO] Dados do paciente atualizados!")

    except ValueError:
        print("[ERRO] Código, peso e altura devem ser números válidos.")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")


def listar_pacientes():
    print("\n--- LISTAGEM DE TODOS OS PACIENTES ---")

    todos_os_pacientes = bst_pacientes.list_all()

    if not todos_os_pacientes:
        print("Nenhum paciente cadastrado.")
        return

    print(f"{'Código':<10} | {'Nome':<30} | {'Cidade - UF':<30}")
    divider()

    for paciente in todos_os_pacientes:
        cod_cidade = paciente['codigo_cidade']
        cidade, _ = bst_cidades.search_with_path(cod_cidade)

        # Requisito 2
        cidade_estado = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

        print(f"{paciente['codigo']:<10} | {paciente['nome']:<30} | {cidade_estado:<30}")


def excluir_paciente():
    print("\n--- EXCLUSÃO DE PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente a ser excluído: "))

        if bst_pacientes.search_with_path(codigo)[0] is None:
            print("[ERRO] Não existe paciente com este código.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o paciente de código {codigo}? (S/N): ").upper()
        if confirmacao.lower() != 's':
            print("Operação cancelada.")
            return

        bst_pacientes.delete(codigo)

        print("[SUCESSO] Paciente excluído.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")
