document.addEventListener("DOMContentLoaded", function () {

    setupSearchButton();
    setupScreenerButton();

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];
    
    if (symbol) {
        fetchStockData(symbol);
        fetchCrossoverData(symbol);
        fetchADXData(symbol);
        fetchBollingerData(symbol);
        fetchRSIData(symbol);
        fetchCandlePatternData(symbol);
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
        let adxLength = document.getElementById("adxLength").value;
    
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
    
        adxLength = parseInt(adxLength);
    
        if (isNaN(adxLength)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
    
        fetchADXData(symbol, adxLength);
    });

    document.getElementById("BollingerButton").addEventListener("click", function () {
        let bollingerLength = document.getElementById("bollingerLength").value;
        let stdBol = document.getElementById("std_bol").value;
    
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
    
        bollingerLength  = parseInt(bollingerLength);
        stdBol = parseInt(stdBol);
    
        if (isNaN(bollingerLength )) {
            alert("Insira valores numéricos válidos.");
            return;
        }
        if (isNaN(stdBol)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
    
        fetchBollingerData(symbol, bollingerLength, stdBol);
    });

    document.getElementById("RSIButton").addEventListener("click", function () {
        let rsiLength = document.getElementById("rsiLength ").value;
        let upperLevel = document.getElementById("upper_level").value;
        let lowerLevel = document.getElementById("lower_level").value;
    
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
    
        rsiLength = parseInt(rsiLength);
        upperLevel = parseInt(upperLevel);
        lowerLevel  = parseInt(lowerLevel);
    
        if (isNaN(rsiLength)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
        if (isNaN(upperLevel)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
        if (isNaN(lowerLevel)) {
            alert("Insira valores numéricos válidos.");
            return;
        }
    
        fetchRSIData(symbol, rsiLength, upperLevel, lowerLevel);
    });

    document.getElementById("CandleButton").addEventListener("click", function () {
            
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
            
        fetchCandlePatternData(symbol);
    });
});


/* ─────────────── FUNÇÕES DE FORMATAÇÃO ─────────────── */


/* ─────────────── FUNÇÕES DE EVENTOS ─────────────── */

function setupSearchButton() {
    let searchButton = document.getElementById("searchButton");
    let stockInput = document.getElementById("stockSymbol");

    if (searchButton && stockInput) {
        searchButton.addEventListener("click", function () {
            let symbol = stockInput.value.trim().toUpperCase();

            // Validação: apenas letras maiúsculas e números são permitidos
            if (!symbol) {
                alert("⚠️ Por favor, insira um símbolo de ação válido (ex: AAPL).");
                return;
            }

            if (!/^[A-Z0-9]{1,10}$/.test(symbol)) {
                alert("⚠️ O símbolo da ação deve conter apenas letras maiúsculas e números (ex: AAPL, TSLA).");
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
    fetch(`/stock/${symbol}/data_history/?period=1mo&interval=1d`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("tableContainerStock").innerHTML = "<h2>Stock not found</h2>";
                return;
            }

            // Apenas atualiza a tabela, sem interferir no gráfico
            updateTable(data);
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("tableContainerStock").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function fetchCrossoverData(symbol, fastPeriod = 14, mediumPeriod = 25, slowPeriod = 200) {
    fetch(`/stock/${symbol}/crossover_trend/?fast=${fastPeriod}&medium=${mediumPeriod}&slow=${slowPeriod}`)
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
    fetch(`/stock/${symbol}/adx_trend/?length=${length}`)
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

function fetchBollingerData(symbol, length = 14, std_dev=2) {
    fetch(`/stock/${symbol}/bollinger_trend/?length=${length}&std=${std_dev}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("BollingerResults").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                displayBollingerResults(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do Bollinger:", error);
            document.getElementById("BollingerResults").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function fetchRSIData(symbol, length = 14, upper_level = 70, lower_level = 30) {
    fetch(`/stock/${symbol}/rsi_trend/?length=${length}&upper_level=${upper_level}&lower_level=${lower_level}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("RSIResults").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                displayRSIResults(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do RSI:", error);
            document.getElementById("RSIResults").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function fetchCandlePatternData(symbol) {
    fetch(`/stock/${symbol}/candle_patterns/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("CandleResults").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                if (typeof displayCandleResults === "function") {
                    displayCandleResults(data);  // Certifique-se de que essa função existe
                } else {
                    console.error("❌ Função displayCandleResults não encontrada!");
                }
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do Candles:", error);
            document.getElementById("CandleResults").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function fetchYahooStockGainers() {
    fetch("/screener/stock_gainers/")
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
    fetch("/screener/stock_trending/")
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
    fetch("/screener/stock_most_active/")
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
                    <th>EMA Short (${data.fast_period})</th>
                    <th>EMA Medium (${data.medium_period})</th>
                    <th>EMA Long (${data.slow_period})</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
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
                    <th>Periods</th>
                    <th>ADX</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.length}</td>
                    <td>${parseFloat(data.adx_now).toFixed(2)}</td>
                    <td><strong>${data.signal}</strong></td>
                </tr>
            </tbody>
        </table>
    `;

    document.getElementById("AdxResults").innerHTML = tableHTML;
}

function displayBollingerResults(data) {
    let tableHTML = `
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Periods</th>
                    <th>Deviation</th>
                    <th>Upper Band</th>
                    <th>Middle Band</th>
                    <th>Lower Band</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.length}</td>
                    <td>${data.std_dev}</td>
                    <td>${parseFloat(data.upper_band).toFixed(2)}</td>
                    <td>${parseFloat(data.middle_band).toFixed(2)}</td>
                    <td>${parseFloat(data.lower_band).toFixed(2)}</td>
                    <td><strong>${data.signal}</strong></td>
                </tr>
            </tbody>
        </table>
    `;

    document.getElementById("BollingerResults").innerHTML = tableHTML;
}

function displayRSIResults(data) {
    let tableHTML = `
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Periods</th>
                    <th>Upper Level</th>
                    <th>Lower Level</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.length}</td>
                    <td>${parseFloat(data.rsi).toFixed(2)}</td>
                    <td>${data.upper_level}</td>
                    <td>${data.lower_level}</td>
                    <td><strong>${data.signal}</strong></td>
                </tr>
            </tbody>
        </table>
    `;

    document.getElementById("RSIResults").innerHTML = tableHTML;
}

function displayCandleResults(data) {
    let tableHTML = `
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Pattern</th>
                    <th>Stoploss</th>
                    <th>Signal</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (let pattern in data.patterns_detected) {
        data.patterns_detected[pattern].forEach(entry => {
            tableHTML += `
                <tr>
                    <td>${pattern}</td>
                    <td>${parseFloat(entry.Stoploss).toFixed(5)}</td>
                    <td>${entry.Signal}</td>
                    <td>${entry.Date}</td>
                </tr>
            `;
        });
    }

    tableHTML += "</tbody></table>";

    document.getElementById("CandleResults").innerHTML = tableHTML;
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