# clinica.py

import os

from arvore_binaria import BinarySearchTree

# --- ÁRVORES DE ÍNDICE GLOBAIS ---
bst_cidades = BinarySearchTree(
    "cidades",
    properties_key_order=["codigo", "descricao", "estado"]
)

bst_especialidades = BinarySearchTree(
    "especialidades",
    properties_key_order=["codigo", "descricao", "valor", "limite"]
)

bst_exames = BinarySearchTree(
    "exames",
    properties_key_order=["codigo", "descricao", "codigo_especialidade", "valor"]
)

bst_pacientes = BinarySearchTree(
    "pacientes",
    properties_key_order=["codigo", "nome", "nascimento", "endereco", "telefone", "codigo_cidade", "peso", "altura"]
)

bst_medicos = BinarySearchTree(
    "medicos",
    properties_key_order=["codigo", "nome", "endereco", "telefone", "codigo_cidade", "codigo_especialidade"]
)

bst_consultas = BinarySearchTree(
    "consultas",
    properties_key_order=["codigo", "cod_paciente", "cod_medico", "cod_exame", "data", "hora", "valor_total"]
)

bst_diarias = BinarySearchTree(
    "diarias",
    properties_key_order=["chave", "quantidade"]
)


# --- FUNÇÕES GLOBAIS (Carregar, Salvar, Formatar) ---

def salvar_dados_tabela(nome_arquivo, bst):
    """Salva os dados de uma árvore binária em um arquivo .txt."""
    registros = bst.list_all()

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for registro in registros:
            # Transforma o dicionário de volta em uma string CSV
            # O join é um jeito elegante de fazer isso
            valores = [str(v) for v in registro.values()]
            linha = ",".join(valores)
            f.write(linha + '\n')


def formatar_data_para_exibir(data_aaaammdd):
    """Converte 'AAAAMMDD' para 'DD/MM/AAAA'."""
    if len(data_aaaammdd) == 8:
        ano = data_aaaammdd[0:4]
        mes = data_aaaammdd[4:6]
        dia = data_aaaammdd[6:8]
        return f"{dia}/{mes}/{ano}"
    return data_aaaammdd


def formatar_data_para_salvar(data_ddmmaaaa):
    """Converte 'DD/MM/AAAA' para 'AAAAMMDD'."""
    try:
        dia, mes, ano = data_ddmmaaaa.split('/')
        if len(dia) == 2 and len(mes) == 2 and len(ano) == 4:
            return ano + mes + dia
    except:
        return None  # Retorna None se o formato for inválido


# --- SEÇÃO DE MENUS E FUNÇÕES CRUD ---
def menu_cidades():
    """Exibe o menu de gerenciamento de cidades e gerencia as operações."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Cadastrar nova cidade")
        print("2. Consultar cidade por código")
        print("3. Alterar dados de uma cidade")  # <-- NOVO
        print("4. Listar todas as cidades")
        print("5. Excluir cidade")
        print("6. Voltar ao menu principal")

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
        elif opcao == '6':
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

        # 1. Insere na árvore em memória
        bst_cidades.insert(codigo, cidade_dic)

        # 2. Adiciona no final do arquivo físico (persistência)
        with open('cidades.txt', 'a', encoding='utf-8') as f:
            f.write(f"{codigo},{descricao},{estado}\n")

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

        salvar_dados_tabela('cidades.txt', bst_cidades)
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
    print("-" * 45)

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

        # 1. Exclui da árvore em memória
        bst_cidades.delete(codigo)

        # 2. Reescreve o arquivo físico a partir da árvore atualizada
        salvar_dados_tabela('cidades.txt', bst_cidades)

        print("[SUCESSO] Cidade excluída.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")


def menu_pacientes():
    """Exibe o menu de gerenciamento de pacientes."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR PACIENTES ---")
        print("1. Cadastrar novo paciente")
        print("2. Consultar paciente por código")
        print("3. Alterar dados de um paciente")  # <-- NOVA OPÇÃO
        print("4. Listar todos os pacientes")  # <-- Renumerado
        print("5. Excluir paciente")  # <-- Renumerado
        print("6. Voltar ao menu principal")  # <-- Renumerado

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_paciente()
        elif opcao == '2':
            consultar_paciente()
        elif opcao == '3':
            alterar_paciente()  # <-- NOVO ELIF
        elif opcao == '4':
            listar_pacientes()
        elif opcao == '5':
            excluir_paciente()
        elif opcao == '6':
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

        # Salva a linha no formato correto no .txt
        linha = f"{codigo},{nome},{nascimento},{endereco},{telefone},{cod_cidade},{peso},{altura}\n"
        with open('pacientes.txt', 'a', encoding='utf-8') as f:
            f.write(linha)

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

        # Após alterar o dicionário em memória, salvamos o arquivo inteiro
        salvar_dados_tabela('pacientes.txt', bst_pacientes)

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
    print("-" * 75)

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
        salvar_dados_tabela('pacientes.txt', bst_pacientes)

        print("[SUCESSO] Paciente excluído.")

    except ValueError:
        print("[ERRO] O código deve ser um número inteiro.")


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

        linha = f"{codigo},{descricao},{valor},{limite}\n"
        with open('especialidades.txt', 'a', encoding='utf-8') as f:
            f.write(linha)

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

        salvar_dados_tabela('especialidades.txt', bst_especialidades)
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
    print("-" * 75)
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
            salvar_dados_tabela('especialidades.txt', bst_especialidades)
            print("[SUCESSO] Especialidade excluída.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


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

        linha = f"{codigo},{nome},{endereco},{telefone},{cod_cidade},{cod_especialidade}\n"
        with open('medicos.txt', 'a', encoding='utf-8') as f:
            f.write(linha)

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

        salvar_dados_tabela('medicos.txt', bst_medicos)
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
            salvar_dados_tabela('medicos.txt', bst_medicos)
            print("[SUCESSO] Médico excluído.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


def menu_exames():
    """Exibe o menu de gerenciamento de exames."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- GERENCIAR EXAMES ---")
        print("1. Cadastrar novo exame")
        print("2. Consultar exame por código")
        print("3. Alterar dados de um exame")  # <-- NOVO
        print("4. Listar todos os exames")
        print("5. Excluir exame")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir_exame()
        elif opcao == '2':
            consultar_exame()
        elif opcao == '3':
            alterar_exame()
        elif opcao == '4':
            listar_exames()
        elif opcao == '5':
            excluir_exame()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")


def incluir_exame():
    """Cadastra um novo exame no sistema."""
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

        exame_dic = {'codigo': codigo, 'descricao': descricao, 'codigo_especialidade': cod_especialidade,
                     'valor': valor}
        bst_exames.insert(codigo, exame_dic)

        linha = f"{codigo},{descricao},{cod_especialidade},{valor}\n"
        with open('exames.txt', 'a', encoding='utf-8') as f:
            f.write(linha)

        print("[SUCESSO] Exame cadastrado!")

    except ValueError:
        print("[ERRO] Verifique se os valores numéricos estão corretos.")


def consultar_exame():
    """Consulta um exame e exibe o nome da sua especialidade (Requisito 4)."""
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
    """Altera os dados de um exame existente."""
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

        salvar_dados_tabela('exames.txt', bst_exames)
        print("\n[SUCESSO] Dados do exame atualizados!")
    except ValueError:
        print("[ERRO] Verifique os valores numéricos.")


def listar_exames():
    """Lista todos os exames, mostrando o nome da especialidade."""
    print("\n--- LISTAGEM DE EXAMES ---")
    lista = bst_exames.list_all()
    if not lista:
        print("Nenhum exame cadastrado.")
        return

    print(f"{'Código':<10} | {'Descrição':<30} | {'Especialidade':<25}")
    print("-" * 70)
    for exame in lista:
        especialidade = bst_especialidades.search_with_path(exame['codigo_especialidade'])[0]
        nome_especialidade = especialidade['descricao'] if especialidade else "N/A"
        print(f"{exame['codigo']:<10} | {exame['descricao']:<30} | {nome_especialidade:<25}")


def excluir_exame():
    """Exclui um exame pelo código."""
    print("\n--- EXCLUSÃO DE EXAME ---")
    try:
        codigo = int(input("Digite o código do exame a ser excluído: "))
        if not bst_exames.search_with_path(codigo)[0]:
            print("[ERRO] Exame não encontrado.")
            return

        confirm = input(f"Tem certeza que deseja excluir o exame de código {codigo}? (S/N): ").upper()
        if confirm == 'S':
            bst_exames.delete(codigo)
            salvar_dados_tabela('exames.txt', bst_exames)
            print("[SUCESSO] Exame excluído.")
        else:
            print("Operação cancelada.")
    except ValueError:
        print("[ERRO] O código deve ser um número.")


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
            data_salvar = formatar_data_para_salvar(data_usuario)
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

        linha = f"{cod_consulta},{cod_paciente},{cod_medico},{cod_exame},{data_salvar},{hora},{valor_total}\n"
        with open('consultas.txt', 'a', encoding='utf-8') as f:
            f.write(linha)

        # 5. Atualizar a tabela Diárias (Requisito 5.3)
        if diaria:
            diaria['quantidade'] += 1
            bst_diarias.delete(chave_diaria)
            bst_diarias.insert(chave_diaria, diaria)
        else:
            nova_diaria = {'chave': chave_diaria, 'quantidade': 1}
            bst_diarias.insert(chave_diaria, nova_diaria)

        salvar_dados_tabela('diarias.txt', bst_diarias)
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
        data_formatada = formatar_data_para_exibir(consulta['data'])
        print(f"Data: {data_formatada}  Hora: {consulta['hora']}")
        print("-" * 30)
        print(f"Paciente: {nome_paciente} (Cidade: {nome_cidade_paciente})")
        print(f"Médico: {nome_medico}")
        print(f"Exame: {desc_exame}")
        print("-" * 30)
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
    print("-" * 80)
    for consulta in lista:
        paciente = bst_pacientes.search_with_path(consulta['cod_paciente'])[0]
        medico = bst_medicos.search_with_path(consulta['cod_medico'])[0]
        nome_paciente = paciente['nome'] if paciente else "N/A"
        nome_medico = medico['nome'] if medico else "N/A"

        data_formatada = formatar_data_para_exibir(consulta['data'])
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
        salvar_dados_tabela('consultas.txt', bst_consultas)
        print("[SUCESSO] Consulta removida.")

        # Passo 4: Atualizar (decrementar) a contagem na tabela Diárias
        diaria = bst_diarias.search_with_path(chave_diaria)[0]
        if diaria and diaria['quantidade'] > 0:
            diaria['quantidade'] -= 1
            # Deleta o registro antigo e insere o novo, com a contagem atualizada
            bst_diarias.delete(chave_diaria)
            bst_diarias.insert(chave_diaria, diaria)
            salvar_dados_tabela('diarias.txt', bst_diarias)
            print("[SUCESSO] Contagem diária de consultas foi atualizada.")
        else:
            print(
                "[AVISO] Não foi encontrado um registro de contagem diária para esta data/especialidade para decrementar.")

    except ValueError:
        print("[ERRO] O código da consulta deve ser um número.")


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
    data_busca = formatar_data_para_salvar(data_usuario)
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
    data_inicio = formatar_data_para_salvar(data_inicio_usuario)

    data_fim_usuario = input("Digite a data final (DD/MM/AAAA): ")
    data_fim = formatar_data_para_salvar(data_fim_usuario)

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
        data_formatada = formatar_data_para_exibir(consulta['data'])

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


def menu_principal():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- SISTEMA DE GESTÃO DE CLÍNICA MÉDICA ---")
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Médicos")
        print("3. Gerenciar Consultas")
        print("4. Gerenciar Cidades")
        print("5. Gerenciar Especialidades")
        print("6. Gerenciar Exames")
        print("7. Relatórios de Faturamento")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_pacientes()
        elif opcao == '2':
            menu_medicos()
        elif opcao == '3':
            menu_consultas()
        elif opcao == '4':
            menu_cidades()
        elif opcao == '5':
            menu_especialidades()
        elif opcao == '6':
            menu_exames()
        elif opcao == '7':
            menu_relatorios()
        elif opcao == '8':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")


# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    menu_principal()
