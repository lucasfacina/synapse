from arvore_binaria import BinarySearchTree

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
