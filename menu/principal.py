import os

from lib import divider
from menu.cidades import menu_cidades
from menu.consultas import menu_consultas
from menu.especialidades import menu_especialidades
from menu.exames import menu_exames
from menu.medicos import menu_medicos
from menu.pacientes import menu_pacientes
from menu.relatorios import menu_relatorios


def menu_principal():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- SISTEMA DE GESTÃO DE CLÍNICA MÉDICA ---")
        print("0. Sair")
        print("1. Gerenciar Cidades")
        print("2. Gerenciar Especialidades")
        print("3. Gerenciar Pacientes")
        print("4. Gerenciar Médicos")
        print("5. Gerenciar Exames")
        print("6. Gerenciar Consultas")
        print("7. Relatórios de Faturamento")

        opcao = input("Escolha uma opção: ")

        if opcao == '0':
            print("Saindo do sistema...")
            break
        elif opcao == '1':
            menu_cidades()
        elif opcao == '2':
            menu_especialidades()
        elif opcao == '3':
            menu_pacientes()
        elif opcao == '4':
            menu_medicos()
        elif opcao == '5':
            menu_exames()
        elif opcao == '6':
            menu_consultas()
        elif opcao == '7':
            menu_relatorios()
        else:
            print("Opção inválida. Tente novamente.")

        divider()
