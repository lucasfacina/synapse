import os

from menu.cidades import menu_cidades
from menu.consultas import menu_consultas
from menu.especialidades import menu_especialidades
from menu.exames import menu_exames
from menu.medicos import menu_medicos
from menu.pacientes import menu_pacientes


def menu_principal():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- SISTEMA DE GESTÃO DE CLÍNICA MÉDICA ---")
        print("0. Sair")
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Médicos")
        print("3. Gerenciar Consultas")
        print("4. Gerenciar Cidades")
        print("5. Gerenciar Especialidades")
        print("6. Gerenciar Exames")
        print("7. Relatórios de Faturamento")

        opcao = input("Escolha uma opção: ")

        if opcao == '0':
            print("Saindo do sistema...")
            break
        elif opcao == '1':
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
        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")
