import { updateEMALines, updateBollingerBands, renderCandlestickFromData } from './candlestick.js';

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
        fetchHarmonicPatternData(symbol);
        fetchFundamentalInfo(symbol);
        fetchFundamentalInfoClassification(symbol);
        fetchBioData(symbol);
    }

    fetchYahooStockGainers();
    fetchYahooStockTrending();
    fetchYahooStockMostActive();

    // ─────────────── EVENTOS DOS BOTÕES ───────────────
    setupTechnicalAnalysisEvents(symbol);

    // ─────────────── CONFIGURAÇÃO DOS TOGGLES ───────────────
    setupToggle({
        toggleSelector: "#bioToggle",
        contentSelector: ".bio-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#tecTrend",
        contentSelector: ".trend-content",
        iconSelector: ".toggle-icon"
    });
    setupToggle({
        toggleSelector: "#tecVolatility",
        contentSelector: ".volatility-content",
        iconSelector: ".toggle-icon"
    });
    setupToggle({
        toggleSelector: "#tecOscilators",
        contentSelector: ".oscilators-content",
        iconSelector: ".toggle-icon"
    });
    
    setupToggle({
        toggleSelector: "#tecCandles",
        contentSelector: ".candles-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#tecHarmonic",
        contentSelector: ".harmonic-content",
        iconSelector: ".toggle-icon"
    });
    
    setupToggle({
        toggleSelector: "#funValuation",
        contentSelector: ".valuation-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funDividends",
        contentSelector: ".dividends-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funProfitability",
        contentSelector: ".profitability-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funHealth",
        contentSelector: ".health-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funCashflow",
        contentSelector: ".cashflow-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funRatios",
        contentSelector: ".ratios-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funRisk",
        contentSelector: ".risk-content",
        iconSelector: ".toggle-icon"
    });

    setupToggle({
        toggleSelector: "#funOverview",
        contentSelector: ".overview-content",
        iconSelector: ".toggle-icon"
    });

}); 

/* ─────────────── FUNÇÕES DE EVENTOS PARA OS BOTÕES ─────────────── */
function setupTechnicalAnalysisEvents(symbol) {
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

        // Atualizar EMAs no gráfico
        updateEMALines(symbol, fastPeriod, mediumPeriod, slowPeriod);

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

        updateBollingerBands(symbol, bollingerLength, stdBol);

    });

    document.getElementById("RSIButton").addEventListener("click", function () {
        let rsiLength = document.getElementById("rsiLength").value;
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

    document.getElementById("HarmonicButton").addEventListener("click", function () {
            
        if (!symbol) {
            alert("Por favor, selecione um ativo antes de calcular.");
            return;
        }
            
        fetchHarmonicPatternData(symbol);
    });
}

/* ─────────────── FUNÇÃO PARA CONFIGURAR O TOGGLE DO CARD ─────────────── */
function setupToggle({ toggleSelector, contentSelector, iconSelector = null }) {
    const toggleElement = document.querySelector(toggleSelector);
    const contentElement = document.querySelector(contentSelector);
    const toggleIcon = iconSelector ? document.querySelector(iconSelector) : null;

    if (!toggleElement || !contentElement) {
        console.error(`Elemento(s) não encontrado(s) para os seletores fornecidos.`);
        return;
    }

    toggleElement.addEventListener("click", () => {
        contentElement.classList.toggle("hidden");
        toggleElement.classList.toggle("active");
        const isHidden = contentElement.classList.contains("hidden");

        if (toggleIcon) {
            toggleIcon.textContent = isHidden ? "+" : "-";
        }
    });
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

            if (!/^[A-Z0-9.]{1,10}$/.test(symbol)) {
                alert("O símbolo da ação deve conter apenas letras maiúsculas, números e pontos (ex: AAPL, TSLA, RHM.DE).");
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

/* ─────── FUNÇÃO PARA FORMATAR NÚMEROS GRANDES ─────── */
function formatNumber(value) {
    return typeof value === "number" && isFinite(value)
        ? value.toLocaleString("en-EN")
        : "N/A";
}


/* ─────── FUNÇÃO PARA FORMATAR VALORES MONETÁRIOS ─────── */
function formatCurrency(value) {
    return typeof value === "number" && isFinite(value)
        ? value.toLocaleString("en-EN", { style: "currency", currency: "USD" })
        : "N/A";
}

/* ─────────────── FUNÇÕES DE CRIAÇÃO DE TABELAS ─────────────── */
function createGridTable(data, columns, containerId) {
    
    new gridjs.Grid({
        columns: columns,
        data: data.map(row => columns.map(col => row[col] || "N/A")),
        search: true,
        pagination: { limit: 5 },
        sort: true,
        className: {
            table: "gridjs-table",
            container: "gridjs-container"
        }
    }).render(document.getElementById(containerId));
}

/* ─────────────── FUNÇÕES DE CLASSIFICAÇÃO DE METRICAS + CHARTS─────────────── */
function classifyMetricForGauge(metric, value) {
    if (value === "N/A") return { classification: "N/A", color: "#9E9E9E", intervals: [0, 100] };

    switch (metric) {
        case "QuickRatio":
            return {
                classification: value >= 2 ? "Excelente"
                    : value >= 1.5 ? "Bom"
                    : value >= 1.0 ? "Razoável"
                    : value >= 0.5 ? "Fraco"
                    : "Muito Fraco",
                color: value >= 2 ? "#068008"
                    : value >= 1.5 ? "#089981"
                    : value >= 1.0 ? "#f2b636"
                    : value >= 0.5 ? "#f24536"
                    : "#ed0000",
                intervals: [0.5, 1, 1.5, 2]
            };

        case "CurrentRatio":
            return {
                classification: value >= 2.5 ? "Excelente"
                    : value >= 1.5 ? "Bom"
                    : value >= 1.0 ? "Razoável"
                    : value >= 0.5 ? "Fraco"
                    : "Muito Fraco",
                color: value >= 2.5 ? "#068008"
                    : value >= 1.5 ? "#089981"
                    : value >= 1.0 ? "#f2b636"
                    : value >= 0.5 ? "#f24536"
                    : "#ed0000",
                intervals: [0.5, 1, 1.5, 2.5]
            };

        case "CashRatio":
            return {
                classification: value >= 1.5 ? "Excelente"
                    : value >= 1.0 ? "Bom"
                    : value >= 0.5 ? "Razoável"
                    : value >= 0.1 ? "Fraco"
                    : "Muito Fraco",
                color: value >= 1.5 ? "#068008"
                    : value >= 1.0 ? "#089981"
                    : value >= 0.5 ? "#f2b636"
                    : value >= 0.1 ? "#f24536"
                    : "#ed0000",
                intervals: [0.1, 0.5, 1, 1.5]
            };

        default:
            return { classification: "N/A", color: "#9E9E9E", intervals: [0, 100] };
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

            renderCandlestickFromData(symbol, data.data); // <- CHAVE
        })
        .catch(error => console.error("Erro ao buscar dados:", error));
}


function fetchBioData(symbol) {
    fetch(`/stock/${symbol}/bio_info/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar Bio:", data.error);
                return;
            }
            displayBioResults(data); 
        })
        .catch(error => console.error("Erro ao buscar os dados do Bio:", error));
}

/* ─────────────── FUNÇÃO PARA DADOS FUNDAMENTAIS ─────────────── */
function fetchFundamentalInfo(symbol) {
    fetch(`/stock/${symbol}/fundamental_info/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar dados fundamentais:", data.error);
                return;
            }
            displayFundamentalResults(data);
        })
        .catch(error => console.error("Erro ao carregar dados fundamentais:", error));
}

function fetchFundamentalInfoClassification(symbol) {
    fetch(`/stock/${symbol}/fundamental_evaluations/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar Classificações:", data.error);
                return;
            }
            displayFundamentalResultsClassification(data);
        })
        .catch(error => console.error("Erro ao carregar Classificações:", error));
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

function fetchHarmonicPatternData(symbol) {
    fetch(`/stock/${symbol}/harmonic_patterns/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar padrões de velas:", data.error);
                return;
            }
            displayHarmonicResults(data);
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
function displayCrossoverResults(data) {
    // const emaShort = parseFloat(data.ema1_now).toFixed(2);
    // const emaMedium = parseFloat(data.ema2_now).toFixed(2);
    // const emaLong = parseFloat(data.ema3_now).toFixed(2);
    const signal = data.signal;

    // document.getElementById("emaShort").textContent = emaShort;
    // document.getElementById("emaMedium").textContent = emaMedium;
    // document.getElementById("emaLong").textContent = emaLong;
    document.getElementById("CrossSignal").textContent = signal;
}

function displayADXResults(data) {
    // const periods = parseFloat(data.length).toFixed(2);
    // const adx = data.adx_now;
    const signal = data.signal;

    // document.getElementById("AdxPeriods").textContent = periods;
    // document.getElementById("ADX").textContent = adx;
    document.getElementById("AdxSignal").textContent = signal;
}

function displayBollingerResults(data) {
    // const periods = data.length;
    // const std = data.std_dev;
    const signal = data.signal;
  
    // document.getElementById("BollPeriods").textContent = periods;
    // document.getElementById("BollStd").textContent = std;
    document.getElementById("BollSignal").textContent = signal;
}

function displayRSIResults(data) {
    // const periods = data.length;
    const rsi = parseFloat(data.rsi).toFixed(2);
    const signal = data.signal;
  
    // document.getElementById("RsiPeriods").textContent = periods;
    document.getElementById("Rsi").textContent = rsi;
    document.getElementById("RsiSignal").textContent = signal;
}

function displayCandleResults(data) {
    let tableData = [];
    for (let pattern in data.patterns_detected) {
        data.patterns_detected[pattern].forEach(entry => {
            tableData.push({
                "Padrão": pattern,
                "Stoploss": entry.Stoploss ? formatCurrency(entry.Stoploss) : "N/A",
                "Sinal": entry.Signal || "N/A",
                "Data": entry.Date || "N/A",
                "Resultado": entry.Result || "N/A",
            });
        });
    }
    createGridTable(tableData, ["Padrão", "Stoploss", "Sinal", "Data", "Resultado"], "tableCandlePatterns");
}

function displayHarmonicResults(data) {
    let tableDataHarmonic = [];

    for (let pattern of data.patterns_detected || []) {
        const signal = pattern.direction === 1 ? "Buy" : "Sell";
        const result = pattern.hit_tp ? `TP atingido: ${pattern.hit_tp}` :
                        (pattern.stop_hit ? "Stop Loss" : "Aberto");

        tableDataHarmonic.push({
            "Padrão": pattern.pattern,
            "Direção": signal,
            "Data (D)": pattern.pattern_idx_dates?.[4] || "N/A",
            "Preço (D)": pattern.D_price?.toFixed(5) || "N/A",
            "Stop": pattern.STOP?.toFixed(5) || "N/A",
            "TP1": pattern.TP1?.toFixed(5) || "N/A",
            "TP2": pattern.TP2?.toFixed(5) || "N/A",
            "TP3": pattern.TP3?.toFixed(5) || "N/A",
            "RR": pattern.rr_ratio?.toFixed(2) || "N/A",
            "Reward": pattern.reward?.toFixed(5) || "N/A",
            "Risk": pattern.risk?.toFixed(5) || "N/A",
            "CD_DIFF": pattern.CD_DIFF?.toFixed(5) || "N/A",
            "X→D Datas": pattern.pattern_idx_dates?.join(" → ") || "N/A",
            "X→D Preços": pattern.pattern_idx_prices?.map(p => p.toFixed(5)).join(" → ") || "N/A",
            "Resultado": result
        });
    }

    createGridTable(
        tableDataHarmonic,
        ["Padrão", "Direção", "Data (D)", "Preço (D)", "Stop", "TP1", "TP2", "TP3", "RR", "Reward", "Risk", "CD_DIFF", "X→D Datas", "X→D Preços", "Resultado"],
        "tableHarmonicPatterns"
    );
}




function populateYahooStockTable(containerId, data) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = "<h2>Nenhum dado disponível</h2>";
        return;
    }

    let headers = Object.keys(data[0]); // Pegar os títulos automaticamente

    // Gerar dados com links para a coluna 'Symbol'
    let tableData = data.map(row => 
        headers.map(header => {
            if (header === "Symbol") {
                // Cria um link na célula do símbolo
                return gridjs.html(`<a href="/stock/${row[header]}/" class="stock-link">${row[header]}</a>`);
            }
            return row[header] || "-";
        })
    );

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

function displayBioResults(data) {
    const bioData = data.data;

    const elements = {
        LongName: bioData.LongName,
        BusinessName: bioData.BusinessName || "N/A",
        Symbol: bioData.Symbol || "N/A",
        City: bioData.City || "N/A",
        State: bioData.State || "N/A",
        ZipCode: bioData.ZipCode || "N/A",
        Country: bioData.Country || "N/A",
        Sector: bioData.Sector || "N/A",
        Industry: bioData.Industry || "N/A",
        Employees: bioData.Employees ? formatNumber(bioData.Employees) : "N/A",
        Website: bioData.Website || "N/A",
        ReportWebsite: bioData.ReportWebsite || "N/A",
        QuoteSource: bioData.QuoteSource || "N/A",
        QuoteType: bioData.QuoteType || "N/A",
        FinancialCurrency: bioData.FinancialCurrency || "N/A",
        CurrentPrice: bioData.CurrentPrice ? formatCurrency(bioData.CurrentPrice) : "N/A",
        PreviousClose: bioData.PreviousClose ? formatCurrency(bioData.PreviousClose) : "N/A",
        OpenPrice: bioData.OpenPrice ? formatCurrency(bioData.OpenPrice) : "N/A"
    };

    for (const [key, value] of Object.entries(elements)) {
        const element = document.getElementById(key);
        if (element) {
            if ((key === "Website" || key === "ReportWebsite") && value !== "N/A") {
                element.href = value;
                element.textContent = value;
            } else {
                element.textContent = value;
            }
        }
    }
}

/* ─────────────── FUNÇÃO PARA PREENCHER FUNDAMENTALS ─────────────── */
function displayFundamentalResults(data) {
    const valuationData = data.valuation;
    const dividendsData = data.dividends;
    const profitabilityData = data.profitability;
    const liquidityData = data.liquidity;
    const cashflowData = data.cashflow;
    const ratiosData = data.ratios;
    const marketRiskData = data.market_risk_and_sentiment;
    
    const elements = {
        // Valuation
        trailingPE: valuationData.trailingPE || {},
        sectorTrailingPE: valuationData.sectorTrailingPE || {},
        forwardPE: valuationData.forwardPE || {},
        PEGRatio: valuationData.PEGRatio || {},
        // Dividends
        divCoverageRate: dividendsData.divCoverageRate || {},
        dividendYield: dividendsData.dividendYield || {},
        fiveYearAvgDividendYield: dividendsData.fiveYearAvgDividendYield || {},
        // Profitability
        NetIncome: profitabilityData.NetIncome || {},
        TotalRevenue: profitabilityData.TotalRevenue || {},
        CostOfRevenue: profitabilityData.CostOfRevenue || {},
        GrossProfit: profitabilityData.GrossProfit || {},
        OperatingExpenses: profitabilityData.OperatingExpenses || {},
        CostOfRevenueCAGR: profitabilityData.CostOfRevenueCAGR || {},
        TotalRevenueCAGR: profitabilityData.TotalRevenueCAGR || {},
        OperatingExpensesCAGR: profitabilityData.OperatingExpensesCAGR || {},
        // CostOfRevenueYOY: profitabilityData.CostOfRevenueYOY || {},
        // TotalRevenueYOY: profitabilityData.TotalRevenueYOY || {},
        // Debt 
        TotalAssets: liquidityData.TotalAssets || {},
        TotalLiabilities: liquidityData.TotalLiabilities || {},
        NetWorth: liquidityData.NetWorth || {},        
        CashCashEquivalents: liquidityData.CashCashEquivalents || {},        
        ShortTermDebtCoverage: liquidityData.ShortTermDebtCoverage || {},        
        CurrentAssets: liquidityData.CurrentAssets || {},        
        CurrentLiabilities: liquidityData.CurrentLiabilities || {},        
        LongTermDebtCoverage: liquidityData.LongTermDebtCoverage || {},        
        NonCurrentAssets: liquidityData.NonCurrentAssets || {},        
        NonCurrentLiabilities: liquidityData.NonCurrentLiabilities || {},        
        TotalAssetsCAGR: liquidityData.TotalAssetsCAGR || {},        
        TotalLiabilitiesCAGR: liquidityData.TotalLiabilitiesCAGR || {},        
        StockholdersEquityCAGR: liquidityData.StockholdersEquityCAGR || {},        
        StockholdersEquity: liquidityData.StockholdersEquity || {},        
        // Cashflow
        FreeCashflow: cashflowData.FreeCashflow || {},
        OperatingCashflow: cashflowData.OperatingCashflow || {},
        CapitalExpenditure: cashflowData.CapitalExpenditure || {},
        MarketCap: cashflowData.MarketCap || {},
        FreeCashflowYield: cashflowData.FreeCashflowYield || {},
        // Ratios
        CurrentRatio: ratiosData.CurrentRatio || {},
        CurrentRatioCAGR: ratiosData.CurrentRatioCAGR || {},
        CashRatio: ratiosData.CashRatio || {},
        CashRatioCAGR: ratiosData.CashRatioCAGR || {},
        GrossMargin: ratiosData.GrossMargin || {},
        // GrossMarginCAGR: ratiosData.GrossMarginCAGR || {},
        OperatingMargin: ratiosData.OperatingMargin || {},
        OperatingMarginCAGR: ratiosData.OperatingMarginCAGR || {},
        ProfitMargin: ratiosData.ProfitMargin || {},
        ProfitMarginCAGR: ratiosData.ProfitMarginCAGR || {},
        ReturnOnEquity: ratiosData.ReturnOnEquity || {},
        ReturnOnEquityCAGR: ratiosData.ReturnOnEquityCAGR || {},
        // Market Risk Sentiment
        beta: marketRiskData.beta || {},
        auditRisk: marketRiskData.auditRisk || {},
        boardRisk: marketRiskData.boardRisk || {},
        sharesPercentSharesOut: marketRiskData.sharesPercentSharesOut || {},
        recommendationMean: marketRiskData.recommendationMean || {},
        targetMeanPrice: marketRiskData.targetMeanPrice || {}
    }

    for (const [key, data] of Object.entries(elements)) {
        const valueElement = document.getElementById(key);
    
        const value = data?.value ?? null;

        if (valueElement) {
            valueElement.textContent =
                typeof value === "number" && isFinite(value)
                    ? formatNumber(value)
                    : "N/A";
        }
        

    }
}

function displayFundamentalResultsClassification(data) {
    const elements = {
        trailingPE: data.evaluations.valuation?.trailingPE_evaluation ?? null,
        PEGRatio: data.evaluations.valuation?.PEGRatio_evaluation ?? null,
        divCoverageRate: data.evaluations.dividends?.divCoverageRate_evaluation ?? null,
        CostOfRevenueCAGR: data.evaluations.profitability?.CostOfRevenueCAGR_evaluation ?? null,
        TotalRevenueCAGR: data.evaluations.profitability?.TotalRevenueCAGR_evaluation ?? null,
        NetWorth: data.evaluations.liquidity?.NetWorth_evaluation ?? null,
        ShortTermDebtCoverage: data.evaluations.liquidity?.ShortTermDebtCoverage_evaluation ?? null,
        LongTermDebtCoverage: data.evaluations.liquidity?.LongTermDebtCoverage_evaluation ?? null,
        StockholdersEquityCAGR: data.evaluations.liquidity?.StockholdersEquityCAGR_evaluation ?? null,
        TotalAssetsCAGR: data.evaluations.liquidity?.TotalAssetsCAGR_evaluation ?? null,
        TotalLiabilitiesCAGR: data.evaluations.liquidity?.TotalLiabilitiesCAGR_evaluation ?? null,
        FreeCashflowYield: data.evaluations.cashflow?.FreeCashflowYield_evaluation ?? null,
        CurrentRatio: data.evaluations.ratios?.CurrentRatio_evaluation ?? null,
        CurrentRatioCAGR: data.evaluations.ratios?.CurrentRatioCAGR_evaluation ?? null,
        CashRatio: data.evaluations.ratios?.CashRatio_evaluation ?? null,
        CashRatioCAGR: data.evaluations.ratios?.CashRatioCAGR_evaluation ?? null,
        GrossMargin: data.evaluations.ratios?.GrossMargin_evaluation ?? null,
        // GrossMarginCAGR: data.evaluations.ratios?.GrossMarginCAGR_evaluation || "N/A",
        OperatingMargin: data.evaluations.ratios?.OperatingMargin_evaluation ?? null,
        OperatingMarginCAGR: data.evaluations.ratios?.OperatingMarginCAGR_evaluation ?? null,
        ProfitMargin: data.evaluations.ratios?.ProfitMargin_evaluation ?? null,
        ProfitMarginCAGR: data.evaluations.ratios?.ProfitMarginCAGR_evaluation ?? null,
        ReturnOnEquity: data.evaluations.ratios?.ReturnOnEquity_evaluation ?? null,
        ReturnOnEquityCAGR: data.evaluations.ratios?.ReturnOnEquityCAGR_evaluation ?? null,
    }
    
    for (const [key, evaluation] of Object.entries(elements)) {
        const classificationElement = document.getElementById(`${key}Class`);
        if (classificationElement) {
            classificationElement.textContent = evaluation ?? "N/A";
        }

        const classificationElementOverview = document.getElementById(`${key}ClassOverview`);
        if (classificationElementOverview) {
            classificationElementOverview.textContent = evaluation ?? "N/A";
        }
    }
}