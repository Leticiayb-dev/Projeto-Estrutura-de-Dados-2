# DataCenter Guard

DataCenter Guard é um projeto acadêmico de manutenção preditiva que simula métricas de servidores e calcula o risco de falha. O sistema é executado exclusivamente pelo terminal e mantém os dados em memória enquanto está aberto.

## Tecnologias

- Python 3
- pytest (testes automatizados)

## Algoritmos utilizados

- Insertion Sort: ordenação por risco, em ordem decrescente.
- Merge Sort: ordenação por risco, em ordem decrescente.
- Busca Binária: consulta de servidor pelo ID.
- Árvore Binária de Busca (BST): busca e listagem em ordem de ID.

## Como executar

Na pasta do projeto, instale as dependências de desenvolvimento e inicie o programa:

```bash
python -m pip install -r requirements.txt
python app.py
```

O menu permite listar servidores, ver o resumo, simular leituras, consultar servidores e demonstrar os algoritmos implementados.

## Testes

```bash
python -m pytest -q
```

## Estrutura

```text
app.py          # interface de terminal e fachada do sistema
servidor.py     # modelo, simulação e regras de risco
algoritmos.py   # ordenação, busca binária e BST
tests/          # testes automatizados
```
