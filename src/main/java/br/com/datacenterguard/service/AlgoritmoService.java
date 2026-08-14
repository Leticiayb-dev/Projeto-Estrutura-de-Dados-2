package br.com.datacenterguard.service;

import br.com.datacenterguard.model.Servidor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class AlgoritmoService {

    private final ServidorService servidorService;
    private No raiz;

    public AlgoritmoService(ServidorService servidorService) {
        this.servidorService = servidorService;

        for (Servidor servidor : servidorService.listarServidores()) {
            inserirNaArvore(servidor);
        }
    }

    public List<Servidor> ordenarComInsertionSort() {
        List<Servidor> ordenados = new ArrayList<>(servidorService.listarServidores());

        for (int indice = 1; indice < ordenados.size(); indice++) {
            Servidor atual = ordenados.get(indice);
            int posicao = indice - 1;

            while (posicao >= 0 && ordenados.get(posicao).getPontuacaoRisco() < atual.getPontuacaoRisco()) {
                ordenados.set(posicao + 1, ordenados.get(posicao));
                posicao--;
            }
            ordenados.set(posicao + 1, atual);
        }

        return ordenados;
    }

    public List<Servidor> ordenarComMergeSort() {
        return ordenarComMergeSort(new ArrayList<>(servidorService.listarServidores()));
    }

    public Optional<Servidor> buscarBinariamente(String id) {
        List<Servidor> ordenadosPorId = ordenarPorId(new ArrayList<>(servidorService.listarServidores()));
        int inicio = 0;
        int fim = ordenadosPorId.size() - 1;

        while (inicio <= fim) {
            int meio = (inicio + fim) / 2;
            Servidor servidorDoMeio = ordenadosPorId.get(meio);
            int comparacao = servidorDoMeio.getId().compareTo(id);

            if (comparacao == 0) {
                return Optional.of(servidorDoMeio);
            }
            if (comparacao < 0) {
                inicio = meio + 1;
            } else {
                fim = meio - 1;
            }
        }

        return Optional.empty();
    }

    public Optional<Servidor> buscarNaArvore(String id) {
        No atual = raiz;

        while (atual != null) {
            int comparacao = id.compareTo(atual.servidor.getId());
            if (comparacao == 0) {
                return Optional.of(atual.servidor);
            }
            atual = comparacao < 0 ? atual.esquerda : atual.direita;
        }

        return Optional.empty();
    }

    public List<Servidor> listarArvoreEmOrdem() {
        List<Servidor> servidores = new ArrayList<>();
        percorrerEmOrdem(raiz, servidores);
        return servidores;
    }

    private List<Servidor> ordenarComMergeSort(List<Servidor> servidores) {
        if (servidores.size() <= 1) {
            return servidores;
        }

        int meio = servidores.size() / 2;
        List<Servidor> esquerda = ordenarComMergeSort(new ArrayList<>(servidores.subList(0, meio)));
        List<Servidor> direita = ordenarComMergeSort(new ArrayList<>(servidores.subList(meio, servidores.size())));
        return combinar(esquerda, direita);
    }

    private List<Servidor> combinar(List<Servidor> esquerda, List<Servidor> direita) {
        List<Servidor> combinados = new ArrayList<>();
        int indiceEsquerda = 0;
        int indiceDireita = 0;

        while (indiceEsquerda < esquerda.size() && indiceDireita < direita.size()) {
            if (esquerda.get(indiceEsquerda).getPontuacaoRisco() >= direita.get(indiceDireita).getPontuacaoRisco()) {
                combinados.add(esquerda.get(indiceEsquerda++));
            } else {
                combinados.add(direita.get(indiceDireita++));
            }
        }

        while (indiceEsquerda < esquerda.size()) {
            combinados.add(esquerda.get(indiceEsquerda++));
        }
        while (indiceDireita < direita.size()) {
            combinados.add(direita.get(indiceDireita++));
        }

        return combinados;
    }

    private List<Servidor> ordenarPorId(List<Servidor> servidores) {
        for (int indice = 1; indice < servidores.size(); indice++) {
            Servidor atual = servidores.get(indice);
            int posicao = indice - 1;

            while (posicao >= 0 && servidores.get(posicao).getId().compareTo(atual.getId()) > 0) {
                servidores.set(posicao + 1, servidores.get(posicao));
                posicao--;
            }
            servidores.set(posicao + 1, atual);
        }

        return servidores;
    }

    private void inserirNaArvore(Servidor servidor) {
        raiz = inserir(raiz, servidor);
    }

    private No inserir(No no, Servidor servidor) {
        if (no == null) {
            return new No(servidor);
        }

        int comparacao = servidor.getId().compareTo(no.servidor.getId());
        if (comparacao < 0) {
            no.esquerda = inserir(no.esquerda, servidor);
        } else if (comparacao > 0) {
            no.direita = inserir(no.direita, servidor);
        } else {
            no.servidor = servidor;
        }

        return no;
    }

    private void percorrerEmOrdem(No no, List<Servidor> servidores) {
        if (no == null) {
            return;
        }

        percorrerEmOrdem(no.esquerda, servidores);
        servidores.add(no.servidor);
        percorrerEmOrdem(no.direita, servidores);
    }

    private static class No {
        private Servidor servidor;
        private No esquerda;
        private No direita;

        private No(Servidor servidor) {
            this.servidor = servidor;
        }
    }
}
