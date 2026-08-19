"""Algoritmos acadêmicos usados pelo DataCenter Guard."""


# INSERTION SORT
def insertion_sort(servidores):
    """Ordena uma cópia por risco, do maior para o menor."""
    ordenados = list(servidores)

    for indice in range(1, len(ordenados)):
        atual = ordenados[indice]
        posicao = indice - 1
        while posicao >= 0 and ordenados[posicao].risco < atual.risco:
            ordenados[posicao + 1] = ordenados[posicao]
            posicao -= 1
        ordenados[posicao + 1] = atual

    return ordenados


# MERGE SORT
def merge_sort(servidores):
    """Ordena uma cópia por risco, do maior para o menor."""
    copia = list(servidores)
    if len(copia) <= 1:
        return copia

    meio = len(copia) // 2
    esquerda = merge_sort(copia[:meio])
    direita = merge_sort(copia[meio:])
    return _combinar(esquerda, direita)


def _combinar(esquerda, direita):
    combinados = []
    indice_esquerda = 0
    indice_direita = 0

    while indice_esquerda < len(esquerda) and indice_direita < len(direita):
        if esquerda[indice_esquerda].risco >= direita[indice_direita].risco:
            combinados.append(esquerda[indice_esquerda])
            indice_esquerda += 1
        else:
            combinados.append(direita[indice_direita])
            indice_direita += 1

    combinados.extend(esquerda[indice_esquerda:])
    combinados.extend(direita[indice_direita:])
    return combinados


# BUSCA BINÁRIA
def busca_binaria(servidores, id_servidor):
    """Prepara uma cópia ordenada por ID e faz a busca manual."""
    ordenados = _ordenar_por_id(list(servidores))
    inicio = 0
    fim = len(ordenados) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if ordenados[meio].id == id_servidor:
            return ordenados[meio]
        if ordenados[meio].id < id_servidor:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None


def _ordenar_por_id(servidores):
    """Insertion Sort manual usado somente para preparar a busca binária."""
    for indice in range(1, len(servidores)):
        atual = servidores[indice]
        posicao = indice - 1
        while posicao >= 0 and servidores[posicao].id > atual.id:
            servidores[posicao + 1] = servidores[posicao]
            posicao -= 1
        servidores[posicao + 1] = atual
    return servidores


# ÁRVORE BINÁRIA DE BUSCA
class No:
    def __init__(self, servidor):
        self.servidor = servidor
        self.esquerda = None
        self.direita = None


class ArvoreBST:
    def __init__(self):
        self.raiz = None

    def inserir(self, servidor):
        self.raiz = self._inserir(self.raiz, servidor)

    def _inserir(self, no, servidor):
        if no is None:
            return No(servidor)
        if servidor.id < no.servidor.id:
            no.esquerda = self._inserir(no.esquerda, servidor)
        elif servidor.id > no.servidor.id:
            no.direita = self._inserir(no.direita, servidor)
        else:
            no.servidor = servidor
        return no

    def buscar(self, id_servidor):
        atual = self.raiz
        while atual is not None:
            if id_servidor == atual.servidor.id:
                return atual.servidor
            if id_servidor < atual.servidor.id:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def percorrer_em_ordem(self):
        servidores = []
        self._percorrer(self.raiz, servidores)
        return servidores

    def _percorrer(self, no, servidores):
        if no is None:
            return
        self._percorrer(no.esquerda, servidores)
        servidores.append(no.servidor)
        self._percorrer(no.direita, servidores)
