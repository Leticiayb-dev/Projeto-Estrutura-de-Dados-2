"""Interface de terminal do DataCenter Guard."""

import re

from algoritmos import ArvoreBST, busca_binaria, insertion_sort, merge_sort
from servidor import criar_servidores, gerar_novas_leituras, listar_criticos, obter_resumo


class DataCenterGuard:
    """Mantem os dados em memoria e disponibiliza as operacoes do sistema."""

    def __init__(self):
        self.servidores = criar_servidores()
        self.rodada_de_leituras = gerar_novas_leituras(self.servidores, 0)
        self.arvore = ArvoreBST()
        for servidor in self.servidores:
            self.arvore.inserir(servidor)

    def simular_leituras(self):
        self.rodada_de_leituras = gerar_novas_leituras(
            self.servidores, self.rodada_de_leituras
        )

    def buscar_por_id(self, id_servidor):
        return busca_binaria(self.servidores, id_servidor.upper())

    def buscar_na_arvore(self, id_servidor):
        return self.arvore.buscar(id_servidor.upper())


def imprimir_servidores(servidores):
    servidores = list(servidores)
    if not servidores:
        print("Nenhum servidor encontrado.")
        return

    cabecalho = (
        f"{'ID':<9} {'RACK':<9} {'CPU':>6} {'MEM.':>6} {'DISCO':>7} "
        f"{'TEMP.':>7} {'FALHAS':>7} {'RISCO':>6}  STATUS"
    )
    print(cabecalho)
    print("-" * len(cabecalho))
    for servidor in servidores:
        print(
            f"{servidor.id:<9} {servidor.rack:<9} {servidor.cpu:>5.1f}% "
            f"{servidor.memoria:>5.1f}% {servidor.disco:>6.1f}% "
            f"{servidor.temperatura:>5.1f} C {servidor.falhas_recentes:>7} "
            f"{servidor.risco:>6}/100  {servidor.status}"
        )


def imprimir_resumo(servidores):
    resumo = obter_resumo(servidores)
    print("\nResumo do monitoramento")
    print(f"  Total: {resumo['total']}")
    print(f"  Normal: {resumo['normal']}")
    print(f"  Atencao: {resumo['atencao']}")
    print(f"  Alto risco: {resumo['alto']}")
    print(f"  Critico: {resumo['critico']}")


def id_servidor_valido(id_servidor):
    return bool(re.fullmatch(r"SRV-\d{3}", id_servidor.upper()))


def ler_id():
    id_servidor = input("ID do servidor (ex.: SRV-003): ").strip().upper()
    if not id_servidor_valido(id_servidor):
        print("Formato de ID invalido. Use o padrao SRV-001 a SRV-004.")
        return None
    return id_servidor


def exibir_menu():
    print("\n" + "=" * 52)
    print("              DATACENTER GUARD")
    print("=" * 52)
    print("1. Listar todos os servidores")
    print("2. Exibir resumo")
    print("3. Gerar novas leituras")
    print("4. Listar servidores criticos")
    print("5. Buscar por ID (busca binaria)")
    print("6. Ordenar por risco (Insertion Sort)")
    print("7. Ordenar por risco (Merge Sort)")
    print("8. Listar por ID (arvore BST)")
    print("9. Buscar por ID (arvore BST)")
    print("0. Sair")


def executar():
    sistema = DataCenterGuard()
    print("DataCenter Guard iniciado. Leituras iniciais geradas.")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()
        print()

        if opcao == "0":
            print("Sistema encerrado.")
            return
        if opcao == "1":
            imprimir_servidores(sistema.servidores)
        elif opcao == "2":
            imprimir_resumo(sistema.servidores)
        elif opcao == "3":
            sistema.simular_leituras()
            print("Novas leituras geradas com sucesso.")
            imprimir_servidores(sistema.servidores)
        elif opcao == "4":
            print("Servidores criticos:")
            imprimir_servidores(listar_criticos(sistema.servidores))
        elif opcao == "5":
            id_servidor = ler_id()
            if id_servidor:
                servidor = sistema.buscar_por_id(id_servidor)
                imprimir_servidores([servidor] if servidor else [])
        elif opcao == "6":
            print("Servidores em ordem decrescente de risco (Insertion Sort):")
            imprimir_servidores(insertion_sort(sistema.servidores))
        elif opcao == "7":
            print("Servidores em ordem decrescente de risco (Merge Sort):")
            imprimir_servidores(merge_sort(sistema.servidores))
        elif opcao == "8":
            print("Servidores em ordem crescente de ID (BST):")
            imprimir_servidores(sistema.arvore.percorrer_em_ordem())
        elif opcao == "9":
            id_servidor = ler_id()
            if id_servidor:
                servidor = sistema.buscar_na_arvore(id_servidor)
                imprimir_servidores([servidor] if servidor else [])
        else:
            print("Opcao invalida. Escolha um numero de 0 a 9.")


if __name__ == "__main__":
    try:
        executar()
    except (EOFError, KeyboardInterrupt):
        print("\nSistema encerrado.")
