package br.com.datacenterguard.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Servidor {

    private final String id;
    private final String rack;
    private double cpu;
    private double memoria;
    private double disco;
    private double temperatura;
    private int falhasRecentes;
    private int pontuacaoRisco;
    private StatusServidor status;

    public Servidor(String id, String rack) {
        this.id = id;
        this.rack = rack;
        this.status = StatusServidor.NORMAL;
    }

    public void atualizarLeituras(double cpu, double memoria, double disco, double temperatura,
                                  int falhasRecentes, int pontuacaoRisco, StatusServidor status) {
        this.cpu = cpu;
        this.memoria = memoria;
        this.disco = disco;
        this.temperatura = temperatura;
        this.falhasRecentes = falhasRecentes;
        this.pontuacaoRisco = pontuacaoRisco;
        this.status = status;
    }

    public String getId() {
        return id;
    }

    public String getRack() {
        return rack;
    }

    public double getCpu() {
        return cpu;
    }

    public double getMemoria() {
        return memoria;
    }

    public double getDisco() {
        return disco;
    }

    public double getTemperatura() {
        return temperatura;
    }

    public int getFalhasRecentes() {
        return falhasRecentes;
    }

    @JsonProperty("risco")
    public int getPontuacaoRisco() {
        return pontuacaoRisco;
    }

    public StatusServidor getStatus() {
        return status;
    }
}
