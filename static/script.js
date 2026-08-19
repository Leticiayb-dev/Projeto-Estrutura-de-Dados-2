const api = {
    servidores: "/api/servidores",
    resumo: "/api/servidores/resumo",
    simular: "/api/servidores/simular"
};

const elements = {
    total: document.querySelector("#total"),
    normal: document.querySelector("#normal"),
    atencao: document.querySelector("#atencao"),
    alto: document.querySelector("#alto"),
    critico: document.querySelector("#critico"),
    serversBody: document.querySelector("#servers-body"),
    tableTitle: document.querySelector("#table-title"),
    tableCount: document.querySelector("#table-count"),
    feedback: document.querySelector("#feedback"),
    searchForm: document.querySelector("#search-form"),
    serverId: document.querySelector("#server-id"),
    searchResult: document.querySelector("#search-result"),
    rackFilter: document.querySelector("#rack-filter"),
    statusFilter: document.querySelector("#status-filter"),
    clearFiltersButton: document.querySelector("#clear-filters-button"),
    simulateButton: document.querySelector("#simular-button"),
};

let feedbackTimer;
let servidoresAtuais = [];

async function requisitar(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        const error = new Error("Não foi possível concluir a solicitação.");
        error.status = response.status;
        throw error;
    }
    return response.json();
}

async function carregarResumo() {
    const resumo = await requisitar(api.resumo);
    elements.total.textContent = resumo.total;
    elements.normal.textContent = resumo.normal;
    elements.atencao.textContent = resumo.atencao;
    elements.alto.textContent = resumo.alto;
    elements.critico.textContent = resumo.critico;
}

async function carregarServidores() {
    servidoresAtuais = await requisitar(api.servidores);
    aplicarFiltros();
}

function mostrarTabela(servidores, titulo) {
    elements.tableTitle.textContent = titulo;
    elements.tableCount.textContent = `${servidores.length} ${servidores.length === 1 ? "registro" : "registros"}`;

    if (servidores.length === 0) {
        elements.serversBody.innerHTML = '<tr><td class="empty-row" colspan="8">Nenhum servidor encontrado.</td></tr>';
        return;
    }

    elements.serversBody.innerHTML = servidores.map(criarLinhaServidor).join("");
}

function criarLinhaServidor(servidor) {
    const status = servidor.status.toLowerCase();
    const classeRisco = servidor.risco >= 75 ? "critical" : servidor.risco >= 50 ? "high" : "";
    return `
        <tr>
            <td class="server-id">${servidor.id}</td>
            <td>${servidor.rack}</td>
            <td>${formatarPercentual(servidor.cpu)}</td>
            <td>${formatarPercentual(servidor.memoria)}</td>
            <td>${formatarPercentual(servidor.disco)}</td>
            <td>${formatarTemperatura(servidor.temperatura)}</td>
            <td><div class="risk-cell"><span>${servidor.risco}</span><span class="risk-bar ${classeRisco}"><span style="width:${servidor.risco}%"></span></span></div></td>
            <td><span class="badge ${status}">${formatarStatus(servidor.status)}</span></td>
        </tr>`;
}

function formatarPercentual(valor) { return `${Number(valor).toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`; }
function formatarTemperatura(valor) { return `${Number(valor).toLocaleString("pt-BR", { maximumFractionDigits: 1 })}°C`; }
function formatarStatus(status) {
    const textos = { ATENCAO: "ATENÇÃO", CRITICO: "CRÍTICO" };
    return textos[status] || status;
}

function mostrarFeedback(mensagem, erro = false) {
    clearTimeout(feedbackTimer);
    elements.feedback.textContent = mensagem;
    elements.feedback.classList.toggle("error", erro);
    feedbackTimer = setTimeout(() => { elements.feedback.textContent = ""; }, 4000);
}

async function simularLeituras() {
    alternarCarregamento(elements.simulateButton, true, "Atualizando...");
    try {
        servidoresAtuais = await requisitar(api.simular, { method: "POST" });
        aplicarFiltros();
        await carregarResumo();
        mostrarFeedback("Leituras atualizadas com sucesso.");
    } catch {
        mostrarFeedback("Não foi possível atualizar as leituras.", true);
    } finally {
        alternarCarregamento(elements.simulateButton, false, "Gerar novas leituras");
    }
}

function aplicarFiltros() {
    const rack = elements.rackFilter.value;
    const status = elements.statusFilter.value;
    const servidoresFiltrados = servidoresAtuais.filter((servidor) =>
        (!rack || servidor.rack === rack) && (!status || servidor.status === status)
    );
    const titulo = rack || status ? "Servidores filtrados" : "Todos os servidores";
    mostrarTabela(servidoresFiltrados, titulo);
}

function limparFiltros() {
    elements.rackFilter.value = "";
    elements.statusFilter.value = "";
    aplicarFiltros();
}

async function buscarServidor(event) {
    event.preventDefault();
    const id = elements.serverId.value.trim().toUpperCase();
    elements.searchResult.hidden = false;

    if (!id) {
        elements.searchResult.className = "search-result error";
        elements.searchResult.textContent = "Informe um ID de servidor para buscar.";
        return;
    }

    try {
        const servidor = await requisitar(`${api.servidores}/${encodeURIComponent(id)}`);
        elements.searchResult.className = "search-result";
        elements.searchResult.innerHTML = criarDetalheServidor(servidor);
    } catch (error) {
        elements.searchResult.className = "search-result error";
        elements.searchResult.textContent = error.status === 404 ? "Servidor não encontrado." : "Não foi possível realizar a busca.";
    }
}

function criarDetalheServidor(servidor) {
    return `
        <div class="result-header"><h3>${servidor.id}</h3><span class="badge ${servidor.status.toLowerCase()}">${formatarStatus(servidor.status)}</span></div>
        <div class="detail-grid">
            <div>Rack<strong>${servidor.rack}</strong></div><div>CPU<strong>${formatarPercentual(servidor.cpu)}</strong></div><div>Memória<strong>${formatarPercentual(servidor.memoria)}</strong></div>
            <div>Disco<strong>${formatarPercentual(servidor.disco)}</strong></div><div>Temperatura<strong>${formatarTemperatura(servidor.temperatura)}</strong></div><div>Risco<strong>${servidor.risco}/100</strong></div>
        </div>`;
}

function alternarCarregamento(botao, carregando, texto) {
    botao.disabled = carregando;
    botao.textContent = texto;
}

async function iniciar() {
    try {
        await Promise.all([carregarResumo(), carregarServidores()]);
    } catch {
        mostrarFeedback("Não foi possível carregar os dados iniciais da aplicação.", true);
    }
}

elements.simulateButton.addEventListener("click", simularLeituras);
elements.rackFilter.addEventListener("change", aplicarFiltros);
elements.statusFilter.addEventListener("change", aplicarFiltros);
elements.clearFiltersButton.addEventListener("click", limparFiltros);
elements.searchForm.addEventListener("submit", buscarServidor);

iniciar();
