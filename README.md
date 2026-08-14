# DataCenter Guard

Projeto acadêmico da disciplina de Algoritmos e Estruturas de Dados II.

O DataCenter Guard é um sistema simples de monitoramento preditivo para um pequeno data center. Ele usa dados simulados de servidores para calcular uma pontuação de risco, classificar cada servidor e apresentar os resultados em um dashboard web.

O projeto foi criado para demonstrar algoritmos e estruturas de dados em Java, sem banco de dados, autenticação ou integração com servidores reais.

## Proposta

Em um data center, servidores podem apresentar sinais de problema, como temperatura alta, CPU muito utilizada, memória próxima do limite, disco cheio ou falhas recentes.

Neste projeto, essas informações são simuladas. A aplicação calcula o risco de cada servidor e mostra o resultado para facilitar a identificação de equipamentos que precisam de atenção.

Atualmente existem quatro servidores simulados:

| Servidor | Rack | Status na simulação |
| --- | --- | --- |
| SRV-001 | RACK-01 | Varia a cada simulação |
| SRV-002 | RACK-02 | Varia a cada simulação |
| SRV-003 | RACK-03 | Varia a cada simulação |
| SRV-004 | RACK-04 | Varia a cada simulação |

Quando o botão de gerar leituras é usado, as métricas e os status mudam. O sistema alterna os status entre os servidores, mantendo um servidor em cada faixa: NORMAL, ATENÇÃO, ALTO e CRÍTICO. Por exemplo, um servidor CRÍTICO passa para ATENÇÃO na rodada seguinte. Isso deixa a demonstração mais clara.

## Regras de risco

A pontuação de risco varia de 0 a 100.

| Regra | Pontos |
| --- | --- |
| Temperatura acima de 75°C | +30 |
| CPU acima de 90% | +20 |
| Memória acima de 90% | +20 |
| Disco acima de 90% | +10 |
| Falhas recentes | +5 por falha, máximo de +20 |

Depois do cálculo, o risco é limitado a 100 pontos.

| Pontuação | Status |
| --- | --- |
| 0 a 29 | NORMAL |
| 30 a 49 | ATENÇÃO |
| 50 a 74 | ALTO |
| 75 a 100 | CRÍTICO |

## Tecnologias utilizadas

- Java 17
- Spring Boot
- Maven
- HTML
- CSS
- JavaScript com `fetch()`

O front-end está dentro do próprio Spring Boot. Por isso, não é necessário instalar React, Node.js, banco de dados ou outras ferramentas extras.

## Estrutura do projeto

```text
datacenter-guard/
├── pom.xml
├── README.md
└── src/
    └── main/
        ├── java/br/com/datacenterguard/
        │   ├── DataCenterGuardApplication.java
        │   ├── model/
        │   │   ├── Servidor.java
        │   │   └── StatusServidor.java
        │   ├── service/
        │   │   ├── ServidorService.java
        │   │   └── AlgoritmoService.java
        │   └── controller/
        │       ├── ServidorController.java
        │       └── AlgoritmoController.java
        └── resources/static/
            ├── index.html
            ├── style.css
            └── script.js
```

### Papel de cada classe

| Arquivo | Responsabilidade |
| --- | --- |
| `DataCenterGuardApplication` | Inicia o Spring Boot e o servidor web. |
| `Servidor` | Representa um servidor com ID, rack, métricas, risco e status. |
| `StatusServidor` | Define os quatro status possíveis. |
| `ServidorService` | Cria os quatro servidores, simula leituras, calcula risco e monta o resumo dos cards. |
| `AlgoritmoService` | Contém Insertion Sort, Merge Sort, Busca Binária e BST. |
| `ServidorController` | Disponibiliza os dados dos servidores pela API REST. |
| `AlgoritmoController` | Disponibiliza os algoritmos pela API REST. |

## Como o sistema funciona

O fluxo principal é:

```text
Página web
    ↓ fetch()
Controller Spring Boot
    ↓
Service Java
    ↓
Dados em memória e algoritmos
    ↓
Resposta JSON
    ↓
Tabela e cards atualizados
```

Os servidores ficam guardados em uma lista em memória no `ServidorService`. Não existe banco de dados. Ao fechar a aplicação, as leituras simuladas são perdidas e uma nova simulação é criada na próxima execução.

## Algoritmos implementados

Os algoritmos continuam no back-end, mesmo que a área visual de algoritmos tenha sido removida do dashboard para deixar a tela mais simples.

### Insertion Sort

Ordena uma cópia da lista de servidores por risco, do maior para o menor.

- Melhor caso: `O(n)`
- Caso médio e pior caso: `O(n²)`

Endpoint: `GET /api/algoritmos/insertion-sort`

### Merge Sort

Também ordena uma cópia da lista por risco decrescente, dividindo a lista em partes menores e depois combinando-as.

- Complexidade: `O(n log n)`

Endpoint: `GET /api/algoritmos/merge-sort`

### Busca Binária

Busca um servidor pelo ID, como `SRV-003`.

Antes da busca, uma cópia da lista é organizada por ID. Essa ordenação por ID é separada da ordenação por risco usada pelo Insertion Sort e Merge Sort.

- Busca após ordenação: `O(log n)`

Endpoint usado pelo campo de busca da página: `GET /api/servidores/{id}`

### Árvore Binária de Busca (BST)

A BST organiza os servidores usando o ID como chave.

- Inserção e busca: `O(h)`, em que `h` é a altura da árvore.
- Percurso em ordem: `O(n)`.
- O percurso em ordem devolve os IDs em ordem crescente.

Endpoints:

- `GET /api/algoritmos/arvore`
- `GET /api/algoritmos/arvore/{id}`

## Endpoints da API

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | `/api/servidores` | Lista os quatro servidores. |
| GET | `/api/servidores/{id}` | Busca um servidor por ID usando Busca Binária. |
| GET | `/api/servidores/criticos` | Lista apenas os servidores críticos. |
| POST | `/api/servidores/simular` | Gera novas leituras simuladas. |
| GET | `/api/servidores/resumo` | Retorna os números dos cards do dashboard. |
| GET | `/api/algoritmos/insertion-sort` | Ordena por risco com Insertion Sort. |
| GET | `/api/algoritmos/merge-sort` | Ordena por risco com Merge Sort. |
| GET | `/api/algoritmos/arvore` | Retorna o percurso em ordem da BST. |
| GET | `/api/algoritmos/arvore/{id}` | Busca um servidor dentro da BST. |

## Dashboard

O dashboard é servido pelo próprio Spring Boot em `src/main/resources/static`.

Ele apresenta:

- Cards com total de servidores e quantidade por status.
- Tabela com CPU, memória, disco, temperatura, risco e status.
- Botão para gerar novas leituras.
- Busca por ID, que usa Busca Binária no Java.
- Filtros visuais por rack e status.

Os filtros da tabela são feitos no JavaScript apenas para organizar a visualização. O cálculo de risco e os algoritmos acadêmicos continuam exclusivamente no Java.

## Como executar

### Pré-requisitos

- JDK 17 instalado.
- Maven instalado e disponível no terminal.

### Comando para iniciar

Abra um terminal na pasta do projeto e execute:

```powershell
mvn spring-boot:run
```

Depois, abra no navegador:

```text
http://localhost:8080
```

Não abra o arquivo `index.html` diretamente. A página deve ser acessada pelo endereço `http://localhost:8080`, pois é o Spring Boot que fornece tanto o front-end quanto a API.

### Comando para gerar o pacote

```powershell
mvn package
```

Esse comando gera o arquivo executável `.jar` dentro da pasta `target`.

## Roteiro curto para apresentação

1. Abra `http://localhost:8080`.
2. Mostre os quatro cards, com um servidor em cada status.
3. Explique rapidamente as regras de risco.
4. Clique em `Gerar novas leituras` e mostre a atualização de métricas e cartões.
5. Use a busca por `SRV-003` e explique que ela chama a Busca Binária no back-end.
6. Mostre os filtros por rack e status.
7. Explique que Insertion Sort, Merge Sort e BST continuam disponíveis pela API para demonstrar os algoritmos da disciplina.

## Limites do projeto

Esta é a N1, então o projeto propositalmente não possui:

- Banco de dados.
- Login ou autenticação.
- Monitoramento de servidores reais.
- Histórico de leituras.
- Gráficos avançados.
- WebSocket.
- Docker.
- Grafos, Dijkstra, Heap ou Huffman.

Essas escolhas mantêm o sistema pequeno, didático e adequado ao objetivo acadêmico atual.
