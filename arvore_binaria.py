# -*- coding: utf-8 -*-
import sys

sys.setrecursionlimit(2000)

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert_recursive(self.root, key, data)

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

    def list_all(self):
        records = []
        self._in_order_traversal(self.root, records.append)
        return records

    def _in_order_traversal(self, current_node, callback):
        if current_node is not None:
            self._in_order_traversal(current_node.left, callback)
            callback(current_node.data)
            self._in_order_traversal(current_node.right, callback)
     
    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

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

    def reorganize(self):
        sorted_records = self.list_all()
        self.root = None
        self._build_balanced_from_sorted(sorted_records, 0, len(sorted_records) - 1)

    def _build_balanced_from_sorted(self, records, start, end):
        if start > end:
            return
        mid = (start + end) // 2
        record = records[mid]

        if self.root_key_type == int:
            self.insert(record['codigo'], record)
        else:
            self.insert(record['nome'], record)

        self._build_balanced_from_sorted(records, start, mid - 1)
        self._build_balanced_from_sorted(records, mid + 1, end)
