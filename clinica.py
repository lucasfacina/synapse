import database
from menu.principal import menu_principal

if __name__ == "__main__":
    _ = database # Garante que a base de dados esteja carregada
    menu_principal()
