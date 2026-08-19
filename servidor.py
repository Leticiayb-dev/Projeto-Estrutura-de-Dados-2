"""Dados, simulação e regras de risco dos servidores."""

from dataclasses import dataclass
import random


@dataclass
class Servidor:
    id: str
    rack: str
    cpu: float = 0.0
    memoria: float = 0.0
    disco: float = 0.0
    temperatura: float = 0.0
    falhas_recentes: int = 0
    risco: int = 0
    status: str = "NORMAL"

    def atualizar(self, cpu, memoria, disco, temperatura, falhas_recentes, risco, status):
        self.cpu = cpu
        self.memoria = memoria
        self.disco = disco
        self.temperatura = temperatura
        self.falhas_recentes = falhas_recentes
        self.risco = risco
        self.status = status

    def para_json(self):
        return {
            "id": self.id,
            "rack": self.rack,
            "cpu": self.cpu,
            "memoria": self.memoria,
            "disco": self.disco,
            "temperatura": self.temperatura,
            "falhasRecentes": self.falhas_recentes,
            "risco": self.risco,
            "status": self.status,
        }


def criar_servidores():
    """Cria os quatro servidores e racks existentes no projeto."""
    return [Servidor(f"SRV-{numero:03d}", f"RACK-{numero:02d}") for numero in range(1, 5)]


def calcular_risco(cpu, memoria, disco, temperatura, falhas_recentes):
    risco = 0
    if temperatura > 75:
        risco += 30
    if cpu > 90:
        risco += 20
    if memoria > 90:
        risco += 20
    if disco > 90:
        risco += 10

    risco += min(max(falhas_recentes, 0) * 5, 20)
    return min(risco, 100)


def classificar_status(risco):
    if risco <= 29:
        return "NORMAL"
    if risco <= 49:
        return "ATENCAO"
    if risco <= 74:
        return "ALTO"
    return "CRITICO"


def gerar_novas_leituras(servidores, rodada):
    """Atualiza só as métricas e devolve o número da próxima rodada."""
    ordem_de_status = ("NORMAL", "ALTO", "CRITICO", "ATENCAO")

    for indice, servidor in enumerate(servidores):
        status_desejado = ordem_de_status[(indice + rodada) % len(ordem_de_status)]
        cpu, memoria, disco, temperatura, falhas = _leitura_para_status(status_desejado)
        risco = calcular_risco(cpu, memoria, disco, temperatura, falhas)
        servidor.atualizar(cpu, memoria, disco, temperatura, falhas, risco, classificar_status(risco))

    return rodada + 1


def listar_criticos(servidores):
    return [servidor for servidor in servidores if servidor.status == "CRITICO"]


def obter_resumo(servidores):
    resumo = {"total": len(servidores), "normal": 0, "atencao": 0, "alto": 0, "critico": 0}
    for servidor in servidores:
        resumo[servidor.status.lower()] += 1
    return resumo


def _leitura_para_status(status):
    if status == "NORMAL":
        return _valor(20, 70), _valor(20, 70), _valor(20, 70), _valor(40, 75), 0
    if status == "ATENCAO":
        return _valor(20, 80), _valor(91, 100), _valor(20, 80), _valor(40, 75), random.randrange(2, 6)
    if status == "ALTO":
        return _valor(91, 100), _valor(20, 80), _valor(20, 80), _valor(76, 90), random.randrange(0, 5)
    return _valor(91, 100), _valor(91, 100), _valor(20, 90), _valor(76, 90), random.randrange(1, 5)


def _valor(minimo, maximo):
    return round(random.uniform(minimo, maximo), 1)
