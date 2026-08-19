from flask import Flask, jsonify, render_template

from algoritmos import ArvoreBST, busca_binaria, insertion_sort, merge_sort
from servidor import criar_servidores, gerar_novas_leituras, listar_criticos, obter_resumo


app = Flask(__name__)

# Os dados ficam em memória enquanto a aplicação está ligada.
servidores = criar_servidores()
rodada_de_leituras = gerar_novas_leituras(servidores, 0)

# A árvore recebe os mesmos objetos da lista. Por isso, suas leituras continuam atualizadas.
arvore = ArvoreBST()
for servidor in servidores:
    arvore.inserir(servidor)


def resposta_servidores(lista):
    return jsonify([servidor.para_json() for servidor in lista])


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/servidores")
def listar_servidores():
    return resposta_servidores(servidores)


@app.get("/api/servidores/criticos")
def listar_criticos_route():
    return resposta_servidores(listar_criticos(servidores))


@app.post("/api/servidores/simular")
def simular_leituras():
    global rodada_de_leituras
    rodada_de_leituras = gerar_novas_leituras(servidores, rodada_de_leituras)
    return resposta_servidores(servidores)


@app.get("/api/servidores/resumo")
def resumo():
    return jsonify(obter_resumo(servidores))


@app.get("/api/servidores/<id_servidor>")
def buscar_servidor(id_servidor):
    servidor = busca_binaria(servidores, id_servidor)
    if servidor is None:
        return jsonify({"message": "Servidor não encontrado."}), 404
    return jsonify(servidor.para_json())


@app.get("/api/algoritmos/insertion-sort")
def ordenar_insertion_sort():
    return resposta_servidores(insertion_sort(servidores))


@app.get("/api/algoritmos/merge-sort")
def ordenar_merge_sort():
    return resposta_servidores(merge_sort(servidores))


@app.get("/api/algoritmos/arvore")
def listar_arvore():
    return resposta_servidores(arvore.percorrer_em_ordem())


@app.get("/api/algoritmos/arvore/<id_servidor>")
def buscar_arvore(id_servidor):
    servidor = arvore.buscar(id_servidor)
    if servidor is None:
        return jsonify({"message": "Servidor não encontrado."}), 404
    return jsonify(servidor.para_json())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
