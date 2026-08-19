from algoritmos import ArvoreBST, busca_binaria, insertion_sort, merge_sort
from app import app
from servidor import Servidor, calcular_risco, classificar_status


def servidores_de_teste():
    return [
        Servidor("SRV-003", "RACK-03", risco=50),
        Servidor("SRV-001", "RACK-01", risco=10),
        Servidor("SRV-004", "RACK-04", risco=90),
        Servidor("SRV-002", "RACK-02", risco=70),
    ]


def test_regras_de_risco_e_status():
    assert calcular_risco(20, 20, 20, 40, 0) == 0
    assert calcular_risco(91, 91, 91, 76, 5) == 100
    assert classificar_status(30) == "ATENCAO"
    assert classificar_status(75) == "CRITICO"


def test_insertion_sort_e_merge_sort():
    servidores = servidores_de_teste()
    esperado = [90, 70, 50, 10]

    assert [servidor.risco for servidor in insertion_sort(servidores)] == esperado
    assert [servidor.risco for servidor in merge_sort(servidores)] == esperado
    assert [servidor.risco for servidor in servidores] == [50, 10, 90, 70]


def test_busca_binaria_e_bst():
    servidores = servidores_de_teste()
    assert busca_binaria(servidores, "SRV-002").rack == "RACK-02"
    assert busca_binaria(servidores, "SRV-999") is None

    arvore = ArvoreBST()
    for servidor in servidores:
        arvore.inserir(servidor)
    assert arvore.buscar("SRV-003").risco == 50
    assert [servidor.id for servidor in arvore.percorrer_em_ordem()] == ["SRV-001", "SRV-002", "SRV-003", "SRV-004"]


def test_endpoints_principais():
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert len(client.get("/api/servidores").get_json()) == 4
    assert client.get("/api/servidores/SRV-003").status_code == 200
    assert client.get("/api/servidores/SRV-999").status_code == 404
    assert client.post("/api/servidores/simular").status_code == 200
    assert client.get("/api/algoritmos/insertion-sort").status_code == 200
    assert client.get("/api/algoritmos/merge-sort").status_code == 200
    assert client.get("/api/algoritmos/arvore").status_code == 200
    assert client.get("/api/algoritmos/arvore/SRV-003").status_code == 200
