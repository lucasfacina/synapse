# -*- coding: utf-8 -*-
import os
import sys

from lib import try_convert, dict_to_csv_line

sys.setrecursionlimit(2000)

DATA_FILE_DIRECTORY = "data/"
DATA_FILE_EXTENSION = ".csv"


class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, file_basename: str, properties_key_order: list[str]):
        self.root = None
        self.filename = DATA_FILE_DIRECTORY + file_basename + DATA_FILE_EXTENSION
        self.properties_order = properties_key_order

        self._load_data_from_file()

    def _load_data_from_file(self):
        try:
            os.makedirs(DATA_FILE_DIRECTORY, exist_ok=True)
        except OSError as e:
            print(f"ERRO: Não foi possível criar o diretório '{DATA_FILE_DIRECTORY}'. Detalhes: {e}")
            return

        print(f"Tentando carregar dados de '{self.filename}'...")

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for row in f:
                    row = row.strip()
                    if not row:
                        continue

                    values_as_str = row.strip().split(',')
                    if len(values_as_str) == len(self.properties_order):
                        converted_values = [try_convert(value) for value in values_as_str]

                        data_dict = dict(zip(self.properties_order, converted_values))
                        self.insert(converted_values[0], data_dict, should_append_to_file=False)

                    print("Dados carregados com sucesso!")


        except FileNotFoundError:
            print(f"AVISO: Arquivo '{self.filename}' não encontrado. Criando um novo arquivo vazio.")
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    pass
                print(f"Arquivo '{self.filename}' criado com sucesso.")
            except Exception as e:
                print(f"ERRO: Falha ao tentar criar o arquivo '{self.filename}'. Detalhes: {e}")

        except Exception as e:
            print(f"ERRO: Ocorreu um erro inesperado ao processar o arquivo: {e}")

    def write_data_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for registry in self.list_all():
                f.write(dict_to_csv_line(registry, fieldnames=self.properties_order))

    # Requisito 1.1
    def insert(self, key, data, should_append_to_file=True):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert_recursive(self.root, key, data)

        if should_append_to_file:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(dict_to_csv_line(data, fieldnames=self.properties_order))

    def _insert_recursive(self, current_node, key, data):
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = Node(key, data)
            else:
                self._insert_recursive(current_node.left, key, data)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = Node(key, data)
            else:
                self._insert_recursive(current_node.right, key, data)

    # Requisito 1.2
    def search_with_path(self, key):
        path_visited = []
        current_node = self.root
        while current_node is not None:
            path_visited.append(current_node.key)
            if key == current_node.key:
                return (current_node.data, path_visited)
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return (None, path_visited)

    # Requisito 1.3
    def delete(self, key, should_write_to_file=True):
        self.root = self._delete_recursive(self.root, key)
        if should_write_to_file:
            self.write_data_to_file()

    def _delete_recursive(self, current_node, key):
        if current_node is None:
            return current_node
        if key < current_node.key:
            current_node.left = self._delete_recursive(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._delete_recursive(current_node.right, key)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left

            temp_node = self._find_min_node(current_node.right)
            current_node.key = temp_node.key
            current_node.data = temp_node.data
            current_node.right = self._delete_recursive(current_node.right, temp_node.key)

        return current_node

    def _find_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Requisito 1.4
    def list_all(self):
        records = []
        self._in_order_traversal(self.root, records.append)
        return records

    def _in_order_traversal(self, current_node, callback):
        if current_node is not None:
            self._in_order_traversal(current_node.left, callback)
            callback(current_node.data)
            self._in_order_traversal(current_node.right, callback)
