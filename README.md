# DataCenter Guard

DataCenter Guard é um projeto acadêmico de manutenção preditiva que utiliza
dados simulados de servidores e aplica algoritmos de ordenação, Busca Binária
e Árvore Binária de Busca para organizar e consultar os dados.

O sistema mantém os dados em memória, calcula o risco de cada servidor e os
apresenta em um dashboard web simples. Não utiliza banco de dados,
autenticação ou monitoramento de servidores reais.

## Tecnologias

- Python 3
- Flask
- HTML, CSS e JavaScript
- pytest

## Algoritmos utilizados

- Insertion Sort — ordenação manual por risco, em ordem decrescente.
- Merge Sort — ordenação manual por risco, em ordem decrescente.
- Busca Binária — consulta manual de um servidor pelo ID.
- BST — Árvore Binária de Busca por ID, com busca e percurso em ordem.

## Como executar

Na pasta do projeto, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Inicie a aplicação:

```bash
python app.py
```

Abra no navegador:

```text
http://localhost:5000
```

## Testes

```bash
python -m pytest -q
```

## Estrutura

```text
app.py
requirements.txt
README.md

models/
services/
algorithms/
tests/

templates/
    index.html

static/
    style.css
    script.js
    datacenter-guard-logo.png
```

## Endpoints

- `GET /api/servidores`
- `GET /api/servidores/<id>`
- `GET /api/servidores/criticos`
- `POST /api/servidores/simular`
- `GET /api/servidores/resumo`
- `GET /api/algoritmos/insertion-sort`
- `GET /api/algoritmos/merge-sort`
- `GET /api/algoritmos/arvore`
- `GET /api/algoritmos/arvore/<id>`
