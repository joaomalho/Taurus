document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Script carregado com sucesso!");

    setupSearchButton();
    setupScreenerButton();

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];
    
    if (symbol) {
        fetchStockData(symbol);
        fetchCrossoverData(symbol);
        fetchADXData(symbol);
    }

    fetchYahooStockGainers();
    fetchYahooStockTrending();
    fetchYahooStockMostActive();

    document.getElementById("crossoverButton").addEventListener("click", function () {
        let fastPeriod = document.getElementById("fastPeriod").value;
        let mediumPeriod = document.getElementById("mediumPeriod").value;
        let slowPeriod = document.getElementById("slowPeriod").value;

        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }

        fastPeriod = parseInt(fastPeriod);
        mediumPeriod = parseInt(mediumPeriod);
        slowPeriod = parseInt(slowPeriod);

        if (isNaN(fastPeriod) || isNaN(mediumPeriod) || isNaN(slowPeriod)) {
            alert("Insira valores numéricos válidos.");
            return;
        }

        fetchCrossoverData(symbol, fastPeriod, mediumPeriod, slowPeriod);
    });

    document.getElementById("AdxButton").addEventListener("click", function () {
        let length = document.getElementById("length").value;
    
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
    
        length = parseInt(length);
    
        if (isNaN(length)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
    
        fetchADXData(symbol, length);
    });
});

/* ─────────────── FUNÇÕES DE EVENTOS ─────────────── */

function setupSearchButton() {
    let searchButton = document.getElementById("searchButton");
    if (searchButton) {
        searchButton.addEventListener("click", function () {
            let symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();
            if (!symbol) {
                alert("Please enter a stock symbol!");
                return;
            }
            window.location.href = `/stock/${symbol}/`;
        });
    }
}

function setupScreenerButton() {
    let screenerButton = document.getElementById("screenerButton");
    if (screenerButton) {
        screenerButton.addEventListener("click", function () {
            window.location.href = "/screener/";
        });
    }
}

/* ─────────────── FUNÇÕES DE REQUISIÇÃO ─────────────── */

function fetchStockData(symbol) {
    fetch(`/stock/${symbol}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("tableContainerStock").innerHTML = "<h2>Stock not found</h2>";
            } else {
                updateTable(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("tableContainerStock").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function fetchCrossoverData(symbol, fastPeriod = 5, mediumPeriod = 10, slowPeriod = 20) {
    fetch(`/get_crossover_trend/?symbol=${symbol}&fast=${fastPeriod}&medium=${mediumPeriod}&slow=${slowPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("crossoverResults").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                displayCrossoverResults(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do crossover:", error);
            document.getElementById("crossoverResults").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function fetchADXData(symbol, length = 14) {
    fetch(`/get_adx_trend/?symbol=${symbol}&length=${length}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("AdxResults").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                displayADXResults(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do ADX:", error);
            document.getElementById("AdxResults").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}


function fetchYahooStockGainers() {
    fetch("/screener/get_yahoo_stock_gainers/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockGainersContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockTable("yahooStockGainers", data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockGainersContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function fetchYahooStockTrending() {
    fetch("/screener/get_yahoo_stock_trending/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockTrendingContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockTable("yahooStockTrending", data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockTrendingContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function fetchYahooStockMostActive() {
    fetch("/screener/get_yahoo_stock_most_active/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockMostActiveContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockTable("yahooStockMostActive", data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockMostActiveContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

/* ─────────────── FUNÇÕES DE MANIPULAÇÃO DE DADOS ─────────────── */

function updateTable(data) {
    let tableHTML = `
        <h2>Market Data for ${data.symbol}</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Change</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.name}</td>
                    <td>${data.price}</td>
                    <td>${data.change}</td>
                </tr>
            </tbody>
        </table>
    `;
    document.getElementById("tableContainerStock").innerHTML = tableHTML;
}

function displayCrossoverResults(data) {
    let tableHTML = `
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>EMA Short (${data.fast_period})</th>
                    <th>EMA Medium (${data.medium_period})</th>
                    <th>EMA Long (${data.slow_period})</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.symbol}</td>
                    <td>${parseFloat(data.ema1_now).toFixed(2)}</td>
                    <td>${parseFloat(data.ema2_now).toFixed(2)}</td>
                    <td>${parseFloat(data.ema3_now).toFixed(2)}</td>
                    <td><strong>${data.signal}</strong></td>
                </tr>
            </tbody>
        </table>
    `;

    document.getElementById("crossoverResults").innerHTML = tableHTML;
}

function displayADXResults(data) {
    let tableHTML = `
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Length</th>
                    <th>ADX</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.symbol}</td>
                    <td>${data.length}</td>
                    <td>${parseFloat(data.adx_now).toFixed(2)}</td>
                    <td><strong>${data.signal}</strong></td>
                </tr>
            </tbody>
        </table>
    `;

    document.getElementById("AdxResults").innerHTML = tableHTML;
}

function populateYahooStockTable(containerPrefix, data) {
    let headerRow = document.getElementById(`${containerPrefix}Header`);
    let tableBody = document.getElementById(`${containerPrefix}Body`);

    headerRow.innerHTML = "";
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='100%'>Nenhum dado disponível</td></tr>";
        return;
    }

    let headers = Object.keys(data[0]);
    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });

    data.forEach(row => {
        let tr = document.createElement("tr");
        headers.forEach(header => {
            let td = document.createElement("td");
            td.textContent = row[header] ? row[header] : "-";
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}