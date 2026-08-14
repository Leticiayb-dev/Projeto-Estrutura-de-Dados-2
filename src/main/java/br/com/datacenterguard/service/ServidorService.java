package br.com.datacenterguard.service;

import br.com.datacenterguard.model.Servidor;
import br.com.datacenterguard.model.StatusServidor;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

@Service
public class ServidorService {

    private static final int QUANTIDADE_SERVIDORES = 4;
    private static final StatusServidor[] ORDEM_DE_STATUS = {
            StatusServidor.NORMAL,
            StatusServidor.ALTO,
            StatusServidor.CRITICO,
            StatusServidor.ATENCAO
    };

    private final List<Servidor> servidores = new ArrayList<>();
    private final Random random = new Random();
    private int rodadaDeLeituras;

    @PostConstruct
    void criarServidoresIniciais() {
        for (int numero = 1; numero <= QUANTIDADE_SERVIDORES; numero++) {
            servidores.add(new Servidor(formatarId(numero), definirRack(numero)));
        }
        gerarNovasLeituras();
    }

    public List<Servidor> listarServidores() {
        return Collections.unmodifiableList(servidores);
    }

    public void gerarNovasLeituras() {
        for (int indice = 0; indice < servidores.size(); indice++) {
            StatusServidor status = definirStatusSimulado(indice);
            gerarLeituraParaStatus(servidores.get(indice), status);
        }
        rodadaDeLeituras++;
    }

    public List<Servidor> listarCriticos() {
        return servidores.stream()
                .filter(servidor -> servidor.getStatus() == StatusServidor.CRITICO)
                .toList();
    }

    public Map<String, Integer> obterResumo() {
        int normal = 0;
        int atencao = 0;
        int alto = 0;
        int critico = 0;

        for (Servidor servidor : servidores) {
            switch (servidor.getStatus()) {
                case NORMAL -> normal++;
                case ATENCAO -> atencao++;
                case ALTO -> alto++;
                case CRITICO -> critico++;
            }
        }

        Map<String, Integer> resumo = new LinkedHashMap<>();
        resumo.put("total", servidores.size());
        resumo.put("normal", normal);
        resumo.put("atencao", atencao);
        resumo.put("alto", alto);
        resumo.put("critico", critico);
        return resumo;
    }

    private int calcularPontuacao(double cpu, double memoria, double disco, double temperatura, int falhasRecentes) {
        int risco = 0;

        if (temperatura > 75) {
            risco += 30;
        }
        if (cpu > 90) {
            risco += 20;
        }
        if (memoria > 90) {
            risco += 20;
        }
        if (disco > 90) {
            risco += 10;
        }

        risco += Math.min(Math.max(falhasRecentes, 0) * 5, 20);
        return Math.min(risco, 100);
    }

    private StatusServidor classificarStatus(int risco) {
        if (risco <= 29) {
            return StatusServidor.NORMAL;
        }
        if (risco <= 49) {
            return StatusServidor.ATENCAO;
        }
        if (risco <= 74) {
            return StatusServidor.ALTO;
        }
        return StatusServidor.CRITICO;
    }

    private String formatarId(int numero) {
        return String.format("SRV-%03d", numero);
    }

    private String definirRack(int numero) {
        return String.format("RACK-%02d", numero);
    }

    private StatusServidor definirStatusSimulado(int indice) {
        int posicao = (indice + rodadaDeLeituras) % ORDEM_DE_STATUS.length;
        return ORDEM_DE_STATUS[posicao];
    }

    private void gerarLeituraParaStatus(Servidor servidor, StatusServidor statusDesejado) {
        double cpu;
        double memoria;
        double disco;
        double temperatura;
        int falhasRecentes;

        switch (statusDesejado) {
            case NORMAL -> {
                cpu = gerarValor(20, 70);
                memoria = gerarValor(20, 70);
                disco = gerarValor(20, 70);
                temperatura = gerarValor(40, 75);
                falhasRecentes = 0;
            }
            case ATENCAO -> {
                cpu = gerarValor(20, 80);
                memoria = gerarValor(91, 100);
                disco = gerarValor(20, 80);
                temperatura = gerarValor(40, 75);
                falhasRecentes = random.nextInt(2, 6);
            }
            case ALTO -> {
                cpu = gerarValor(91, 100);
                memoria = gerarValor(20, 80);
                disco = gerarValor(20, 80);
                temperatura = gerarValor(76, 90);
                falhasRecentes = random.nextInt(5);
            }
            case CRITICO -> {
                cpu = gerarValor(91, 100);
                memoria = gerarValor(91, 100);
                disco = gerarValor(20, 90);
                temperatura = gerarValor(76, 90);
                falhasRecentes = random.nextInt(1, 5);
            }
            default -> throw new IllegalStateException("Status simulado invalido");
        }

        int risco = calcularPontuacao(cpu, memoria, disco, temperatura, falhasRecentes);
        StatusServidor status = classificarStatus(risco);
        servidor.atualizarLeituras(cpu, memoria, disco, temperatura, falhasRecentes, risco, status);
    }

    private double gerarValor(double minimo, double maximo) {
        return arredondar(random.nextDouble(minimo, maximo));
    }

    private double arredondar(double valor) {
        return Math.round(valor * 10.0) / 10.0;
    }
}
