package br.com.datacenterguard.controller;

import br.com.datacenterguard.model.Servidor;
import br.com.datacenterguard.service.AlgoritmoService;
import br.com.datacenterguard.service.ServidorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/servidores")
public class ServidorController {

    private final ServidorService servidorService;
    private final AlgoritmoService algoritmoService;

    public ServidorController(ServidorService servidorService, AlgoritmoService algoritmoService) {
        this.servidorService = servidorService;
        this.algoritmoService = algoritmoService;
    }

    @GetMapping
    public List<Servidor> listarTodos() {
        return servidorService.listarServidores();
    }

    @GetMapping("/criticos")
    public List<Servidor> listarCriticos() {
        return servidorService.listarCriticos();
    }

    @PostMapping("/simular")
    public List<Servidor> simularLeituras() {
        servidorService.gerarNovasLeituras();
        return servidorService.listarServidores();
    }

    @GetMapping("/resumo")
    public Map<String, Integer> obterResumo() {
        return servidorService.obterResumo();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Servidor> buscarPorId(@PathVariable String id) {
        return ResponseEntity.of(algoritmoService.buscarBinariamente(id));
    }
}
