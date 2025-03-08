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
        fetchFundamentalInfo(symbol);
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


/* ─────────────── FUNÇÃO PARA PEGAR DADOS FUNDAMENTAIS ─────────────── */
function fetchFundamentalInfo(symbol) {
    fetch(`/stock/${symbol}/fundamental_info/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar dados fundamentais:", data.error);
                return;
            }

            console.log("Dados Fundamentais Recebidos:", data);

            // Define as métricas a mostrar para cada tabela
            let selectedMetricsLiquidity = ["Quick Ratio", "Current Ratio", "Cash Ratio"];
            let selectedMetricsProfitability = ["EBIT", "Operating Cash Flow"];
            
            populateFundamentalTable(data.liquidity_and_solvency, "tableLiquidity", selectedMetricsLiquidity);

            populateFundamentalTable(data.profitability, "Lucratividade", "tableProfitability");
            populateFundamentalTable(data.growth, "Crescimento", "tableGrowth");
            populateFundamentalTable(data.valuation, "Valuation", "tableValuation");
            populateFundamentalTable(data.dividends_and_buybacks, "Dividendos e Buybacks", "tableDividends");
            populateFundamentalTable(data.market_risk_and_sentiment, "Risco de Mercado", "tableRisk");
        })
        .catch(error => console.error("Erro ao carregar dados fundamentais:", error));
}

/* ─────────────── FUNÇÃO PARA PREENCHER TABELAS ─────────────── */

function populateFundamentalTable(categoryData, tableId, selectedMetrics) {
    let tableContainer = document.getElementById(tableId);
    
    if (!tableContainer) {
        console.error(`Elemento com ID '${tableId}' não encontrado.`);
        return;
    }

    let tableData = selectedMetrics.map(metric => {
        if (categoryData.hasOwnProperty(metric)) {
            let value = categoryData[metric].value !== null ? categoryData[metric].value : "N/A";
            let conclusion = categoryData[metric].evaluation || "N/A";
            return [metric, value, conclusion];
        }
    }).filter(Boolean);


    new gridjs.Grid({
        columns: ["Métrica", "Valor", "Avaliação"],
        data: tableData,
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(tableContainer);
}

/* ─────────────── FUNÇÕES DE EVENTOS ─────────────── */

function setupSearchButton() {
    let searchButton = document.getElementById("searchButton");
    let stockInput = document.getElementById("stockSymbol");

    if (searchButton && stockInput) {
        searchButton.addEventListener("click", function () {
            let symbol = stockInput.value.trim().toUpperCase();

            if (!symbol) {
                alert("Por favor, insira um símbolo de ação válido (ex: AAPL).");
                return;
            }

            if (!/^[A-Z0-9]{1,10}$/.test(symbol)) {
                alert("O símbolo da ação deve conter apenas letras maiúsculas e números (ex: AAPL, TSLA).");
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
                console.error("Erro ao buscar dados:", data.error);
                return;
            }

            updateTable(data); // Agora usa Grid.js
        })
        .catch(error => console.error("Erro ao buscar dados:", error));
}

function fetchCrossoverData(symbol, fastPeriod = 14, mediumPeriod = 25, slowPeriod = 200) {
    fetch(`/stock/${symbol}/crossover_trend/?fast=${fastPeriod}&medium=${mediumPeriod}&slow=${slowPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar crossover:", data.error);
                return;
            }
            displayCrossoverResults(data);
        })
        .catch(error => console.error("Erro ao buscar os dados do crossover:", error));
}

function fetchADXData(symbol, length = 14) {
    fetch(`/stock/${symbol}/adx_trend/?length=${length}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar ADX:", data.error);
                return;
            }
            displayADXResults(data);
        })
        .catch(error => console.error("Erro ao buscar os dados do ADX:", error));
}

function fetchBollingerData(symbol, length = 14, std_dev=2) {
    fetch(`/stock/${symbol}/bollinger_trend/?length=${length}&std=${std_dev}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar Bollinger:", data.error);
                return;
            }
            displayBollingerResults(data);
        })
        .catch(error => console.error("Erro ao buscar os dados do Bollinger:", error));
}

function fetchRSIData(symbol, length = 14, upper_level = 70, lower_level = 30) {
    fetch(`/stock/${symbol}/rsi_trend/?length=${length}&upper_level=${upper_level}&lower_level=${lower_level}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar RSI:", data.error);
                return;
            }
            displayRSIResults(data);
        })
        .catch(error => console.error("Erro ao buscar os dados do RSI:", error));
}

function fetchCandlePatternData(symbol) {
    fetch(`/stock/${symbol}/candle_patterns/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar padrões de velas:", data.error);
                return;
            }
            displayCandleResults(data);
        })
        .catch(error => console.error("Erro ao buscar os dados do Candles:", error));
}

function fetchYahooStockGainers() {
    fetch("/screener/stock_gainers/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar stocks ganhadores:", data.error);
                return;
            }
            populateYahooStockTable("tableYahooGainers", data.data);
        })
        .catch(error => console.error("Erro ao buscar stocks ganhadores:", error));
}

function fetchYahooStockTrending() {
    fetch("/screener/stock_trending/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar stocks em tendência:", data.error);
                return;
            }
            populateYahooStockTable("tableYahooTrending", data.data);
        })
        .catch(error => console.error("Erro ao buscar stocks em tendência:", error));
}

function fetchYahooStockMostActive() {
    fetch("/screener/stock_most_active/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar stocks mais ativos:", data.error);
                return;
            }
            populateYahooStockTable("tableYahooMostActive", data.data);
        })
        .catch(error => console.error("Erro ao buscar stocks mais ativos:", error));
}


/* ─────────────── FUNÇÕES DE MANIPULAÇÃO DE DADOS ─────────────── */

function updateTable(data) {
    new gridjs.Grid({
        columns: ["Nome", "Preço", "Variação"],
        data: [[data.name, data.price, data.change]],
        search: true,
        pagination: true,
        sort: true, 
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById("tableStockData"));
}

function displayCrossoverResults(data) {
    const emaShort = parseFloat(data.ema1_now).toFixed(2);
    const emaMedium = parseFloat(data.ema2_now).toFixed(2);
    const emaLong = parseFloat(data.ema3_now).toFixed(2);
    const signal = data.signal;

    document.getElementById("emaShort").textContent = emaShort;
    document.getElementById("emaMedium").textContent = emaMedium;
    document.getElementById("emaLong").textContent = emaLong;
    document.getElementById("Signal").textContent = signal;
}

function displayADXResults(data) {
    new gridjs.Grid({
        columns: ["Períodos", "ADX", "Sinal"],
        data: [[data.length, parseFloat(data.adx_now).toFixed(2), data.signal]],
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById("tableADX"));
}

function displayBollingerResults(data) {
    new gridjs.Grid({
        columns: ["Períodos", "Desvio", "Banda Superior", "Banda Média", "Banda Inferior", "Sinal"],
        data: [[data.length, data.std_dev, parseFloat(data.upper_band).toFixed(2), parseFloat(data.middle_band).toFixed(2), parseFloat(data.lower_band).toFixed(2), data.signal]],
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById("tableBollinger"));
}

function displayRSIResults(data) {
    new gridjs.Grid({
        columns: ["Períodos", "Nível Superior", "Nível Inferior", "RSI", "Sinal"],
        data: [[data.length, data.upper_level, data.lower_level, parseFloat(data.rsi).toFixed(2), data.signal]],
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById("tableRSI"));
}

function displayCandleResults(data) {
    let tableData = [];
    for (let pattern in data.patterns_detected) {
        data.patterns_detected[pattern].forEach(entry => {
            tableData.push([pattern, parseFloat(entry.Stoploss).toFixed(5), entry.Signal, entry.Date]);
        });
    }

    new gridjs.Grid({
        columns: ["Padrão", "Stoploss", "Sinal", "Data"],
        data: tableData,
        search: true,
        pagination: true,
        sort: true, 
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById("tableCandlePatterns"));
}

function populateYahooStockTable(containerId, data) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = "<h2>Nenhum dado disponível</h2>";
        return;
    }

    let headers = Object.keys(data[0]); // Pegar os títulos automaticamente

    let tableData = data.map(row => headers.map(header => row[header] || "-"));

    new gridjs.Grid({
        columns: headers,
        data: tableData,
        search: true,
        pagination: true,
        sort: true, 
        className: {
            table: "gridjs-table",
            container: "gridjs-container",
        }
    }).render(document.getElementById(containerId));
}