from algoritmos import ArvoreBST, busca_binaria, insertion_sort, merge_sort
from app import DataCenterGuard, id_servidor_valido
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


def test_operacoes_do_sistema_de_terminal():
    sistema = DataCenterGuard()
    assert len(sistema.servidores) == 4
    assert sistema.buscar_por_id("srv-003").id == "SRV-003"
    assert sistema.buscar_por_id("SRV-999") is None
    assert sistema.buscar_na_arvore("srv-002").id == "SRV-002"

    rodada_anterior = sistema.rodada_de_leituras
    sistema.simular_leituras()
    assert sistema.rodada_de_leituras == rodada_anterior + 1


def test_validacao_do_formato_do_id():
    assert id_servidor_valido("srv-003")
    assert not id_servidor_valido("2")
    assert not id_servidor_valido("SRV-03")
