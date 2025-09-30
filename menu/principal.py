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
        match opcao:
            case '0':
                print("Saindo do sistema...")
                break
            case '1':
                menu_cidades()
            case '2':
                menu_especialidades()
            case '3':
                menu_pacientes()
            case '4':
                menu_medicos()
            case '5':
                menu_exames()
            case '6':
                menu_consultas()
            case '7':
                menu_relatorios()
            case _:
                print("Opção inválida. Tente novamente.")

        divider()
