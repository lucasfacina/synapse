# 🧠 Synapse

Este repositório contém o projeto desenvolvido para a disciplina **Algoritmos e Estruturas de Dados II** do curso de **Bacharelado em Ciência da Computação**, ministrada pelo professor [Luiz Ricardo Begosso](https://www.escavador.com/sobre/3201843/luiz-ricardo-begosso).

## 👥 Autores

O desenvolvimento foi realizado em **Pair Programming** por:

- Thiago Ausechi — RA: 2411600623
  - [Github](https://github.com/thiagoausechi)
  - [LinkedIn](https://www.linkedin.com/in/thiagoausechi/)
- Lucas Facina — RA: 2411600015
  - [Github](https://github.com/lucasfacina)
  - [LinkedIn](https://www.linkedin.com/in/lucasfacina/)

## 📋 Requisitos do Trabalho

Desenvolver um sistema de gestão para uma clínica médica, utilizando a lógica de arquivos indexados.
Simular um banco de dados simples para uma clínica médica, que precisa manter os registros de pacientes, médicos, especialidades e consultas.
Para isso:

- A área de índices deve ser implementada como uma Árvore Binária, que será armazenada em memória.
- A área de dados deve ser armazenada em disco (arquivo de texto ou binário), garantindo que as informações fiquem salvas entre as execuções.

O programa deverá ser escrito em Python, com boa usabilidade, interface amigável e menus bem estruturados.

### Estruturas (arquivos/tabelas)

Cada uma gravada em arquivo separado.

```txt
1. [x] Cidades: Código da Cidade, Descrição, Estado
2. [x] Especialidades: Código da Especialidade, Descrição, Valor da Consulta, Limite Diário
3. [x] Diárias: Código do Dia (AAAAMMDD), Código da Especialidade, Quantidade de Consultas
4. [x] Pacientes: Código do Paciente, Nome, Data Nascimento, Endereço, Telefone, Código da Cidade, Peso, Altura
5. [x] Médicos: Código do Médico, Nome, Endereço, Telefone, Código da Cidade, Código da Especialidade
6. [x] Exames: Código do Exame, Descrição, Código Especialidade, Valor do Exame
7. [x] Consultas: Código da Consulta, Código do Paciente, Código do Médico, Código do Exame, Data, Hora
```

### Requisitos

```txt
1. [x] Operações básicas
  1. [x] Inclusão de novos registros nas tabelas.
  2. [x] Consulta de registros das tabelas.
  3. [x] Exclusão de registros das tabelas.
  4. [x] Leitura exaustiva das tabelas.
     A busca, inclusão e exclusão devem ser realizadas utilizando o índice em árvore binária.

2. [x] Ao exibir um paciente na tabela Pacientes, o programa deverá buscar o código da cidade na tabela de Cidades e exibir o nome da cidade e o Estado.
   1. [x] Ao consultar um Paciente, calcular e exibir o IMC (Índice de Massa Corpol.) e exibir o diagnóstico: Abaixo do peso, Peso normal, Sobrepeso, Obesidade.

3. [x] Ao exibir médico na tabela Médicos, o programa deverá buscar o código da cidade na tabela de Cidades e exibir o nome da cidade e o Estado.
   1. [x] O programa também deverá buscar o código da especialidade na tabela Especialidades e exibir a descrição e o valor da consulta e o limite diário de consultas.

4. [x] Ao incluir ou consultar dados na Tabela Exames, o programa deve mostrar o nome da especialidade correspondente e o valor do exame.

5. [x] Ao incluir ou consultar dados na Tabela Consultas, o programa deve mostrar também o nome do Paciente, o nome de sua Cidade, o nome do Médico e a Descrição do Exame.
   1. [x] Antes de inserir uma nova consulta, verificar se ainda há vagas, de acordo com o limite diário da especialidade: quantidade de consultas do dia deve ser menor do que o limite diário da especialidade.
   2. [x] Ao inserir ou consultar uma consulta, o programa deverá mostrar o valor a ser pago pelo paciente, considerando valor da consulta e o valor do exame a ser feito.
   3. [x] Ao inserir ou consultar uma consulta, o programa deverá adicionar uma unidade na Quantidade de Consultas da tabela Diárias.
   4. [x] Ao excluir uma consulta, subtrair 1 no Quantidade de Consultas na tabela Diárias.

6. [x] O programa deverá ter a opção de mostrar o quanto a clínica faturou:
   1. [x] Exibir faturamento por dia
   2. [x] Exibir faturamento por período (data inicial e data final)
   3. [x] Exibir faturamento por Médico
   4. [x] Exibir faturamento por Especialidade.

7. [x] Ler todos os registros da tabela de Consultas e exibi-los em ordem crescente de Código da Consulta. Os seguintes dados deverão ser mostrados:
   Código da Consulta, Nome do Paciente, Nome da Cidade do Paciente, Nome do Médico, Descrição do Exame, Valor a ser pago pelo Paciente
   Ao final, mostrar a quantidade total de pacientes e o valor total a ser pago pelos pacientes.
```

> 📝 **Nota:** Os itens dos requisitos podem ser localizados no código por meio da busca por "Requisito x.x.x" (_ex.: Requisito 4.5.1.2_), utilizando a concatenação dos identificadores dos itens aninhados.

<br />

> 🚨 **Observação importante:** O trabalho deverá ser desenvolvido integralmente pelos alunos, sendo vedado o uso de ferramentas de geração automática de código (como ChatGPT, Copilot ou similares). Para garantir a aprendizagem, a avaliação será feita por meio de apresentações individuais onde cada aluno deve explicar partes específicas do código desenvolvido, as decisões de projeto tomadas, o funcionamento da estrutura de arquivos indexados e da árvore binária, trechos do código, as dificuldades encontradas e como foram resolvidas.

## 📄 Licença

Este projeto é parte de uma atividade acadêmica e não possui fins comerciais.
Uso exclusivo para fins educacionais na [FEMA](https://fema.edu.br/) - Fundação Educacional do Município de Assis.
