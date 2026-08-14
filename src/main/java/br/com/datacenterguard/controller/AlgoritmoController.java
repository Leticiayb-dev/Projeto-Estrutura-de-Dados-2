package br.com.datacenterguard.controller;

import br.com.datacenterguard.model.Servidor;
import br.com.datacenterguard.service.AlgoritmoService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/algoritmos")
public class AlgoritmoController {

    private final AlgoritmoService algoritmoService;

    public AlgoritmoController(AlgoritmoService algoritmoService) {
        this.algoritmoService = algoritmoService;
    }

    @GetMapping("/insertion-sort")
    public List<Servidor> ordenarComInsertionSort() {
        return algoritmoService.ordenarComInsertionSort();
    }

    @GetMapping("/merge-sort")
    public List<Servidor> ordenarComMergeSort() {
        return algoritmoService.ordenarComMergeSort();
    }

    @GetMapping("/arvore")
    public List<Servidor> listarArvoreEmOrdem() {
        return algoritmoService.listarArvoreEmOrdem();
    }

    @GetMapping("/arvore/{id}")
    public ResponseEntity<Servidor> buscarNaArvore(@PathVariable String id) {
        return ResponseEntity.of(algoritmoService.buscarNaArvore(id));
    }
}
