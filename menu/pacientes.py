import os

from database import bst_pacientes, bst_cidades
from lib import divider


def menu_pacientes():
    """Exibe o menu de gerenciamento de pacientes."""
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

        if opcao == '1':
            incluir_paciente()
        elif opcao == '2':
            consultar_paciente()
        elif opcao == '3':
            alterar_paciente()
        elif opcao == '4':
            listar_pacientes()
        elif opcao == '5':
            excluir_paciente()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_paciente():
    """Pede os dados de um novo paciente e o insere no sistema."""
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

        # Validação da Cidade (Requisito 2)
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
    """Pede um código e busca o paciente, mostrando dados da cidade e IMC."""
    print("\n--- CONSULTA DE PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente: "))
        paciente, caminho = bst_pacientes.search_with_path(codigo)

        print(f"Caminho percorrido na árvore de pacientes: {' -> '.join(map(str, caminho))}")

        if not paciente:
            print("\nPaciente não encontrado.")
            return

        # Busca cruzada: encontrar a cidade do paciente
        cod_cidade = paciente['codigo_cidade']
        cidade, _ = bst_cidades.search_with_path(cod_cidade)
        nome_cidade = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "Cidade não encontrada"

        # Cálculo do IMC
        peso = paciente['peso']
        altura = paciente['altura']
        imc = peso / (altura * altura) if altura > 0 else 0

        diagnostico_imc = ""
        if imc < 18.5:
            diagnostico_imc = "Abaixo do peso"
        elif 18.5 <= imc < 25:
            diagnostico_imc = "Peso normal"
        elif 25 <= imc < 30:
            diagnostico_imc = "Sobrepeso"
        else:
            diagnostico_imc = "Obesidade"

        # Exibição dos resultados
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
    """Altera os dados de um paciente existente."""
    print("\n--- ALTERAÇÃO DE DADOS DO PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente que deseja alterar: "))
        paciente_dic, _ = bst_pacientes.search_with_path(codigo)

        if not paciente_dic:
            print("[ERRO] Paciente não encontrado com este código.")
            return

        print("\nDigite os novos dados. Pressione Enter para manter o valor atual.")

        # --- NOME ---
        print(f"Nome atual: {paciente_dic['nome']}")
        novo_nome = input("Novo nome: ")
        if novo_nome:
            paciente_dic['nome'] = novo_nome

        # --- DATA DE NASCIMENTO ---
        print(f"Nascimento atual: {paciente_dic['nascimento']}")
        novo_nascimento = input("Nova data de nascimento (DD/MM/AAAA): ")
        if novo_nascimento:
            paciente_dic['nascimento'] = novo_nascimento

        # --- ENDEREÇO ---
        print(f"Endereço atual: {paciente_dic['endereco']}")
        novo_endereco = input("Novo endereço: ")
        if novo_endereco:
            paciente_dic['endereco'] = novo_endereco

        # --- TELEFONE ---
        print(f"Telefone atual: {paciente_dic['telefone']}")
        novo_telefone = input("Novo telefone: ")
        if novo_telefone:
            paciente_dic['telefone'] = novo_telefone

        # --- PESO ---
        print(f"Peso atual: {paciente_dic['peso']}")
        novo_peso_str = input("Novo peso (kg): ")
        if novo_peso_str:
            paciente_dic['peso'] = float(novo_peso_str)

        # --- ALTURA ---
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
    """Lista todos os pacientes cadastrados, mostrando o nome da cidade."""
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

        # 2. Criação da string combinando cidade e estado
        cidade_estado = f"{cidade['descricao']} - {cidade['estado']}" if cidade else "N/A"

        # 3. Impressão da linha com a nova string combinada
        print(f"{paciente['codigo']:<10} | {paciente['nome']:<30} | {cidade_estado:<30}")


def excluir_paciente():
    """Pede um código e exclui o paciente correspondente."""
    print("\n--- EXCLUSÃO DE PACIENTE ---")
    try:
        codigo = int(input("Digite o código do paciente a ser excluído: "))

        if bst_pacientes.search_with_path(codigo)[0] is None:
            print("[ERRO] Não existe paciente com este código.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o paciente de código {codigo}? (S/N): ").upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return

        bst_pacientes.delete(codigo)

        print("[SUCESSO] Paciente excluído.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")
