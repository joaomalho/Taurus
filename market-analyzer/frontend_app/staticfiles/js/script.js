import { renderCandlestickFromData } from "./candlestick.js";
import "./chartsandgraphs.js";
import { initMetricTooltips, initAttributeTooltips } from "./tooltips.js";
import {
    fetchYahooStockGainers,
    fetchYahooStockTrending,
    fetchYahooStockMostActive,
    fetchBioData,
    fetchStockData,
    fetchCrossoverData,
    fetchADXData,
    fetchBollingerData,
    fetchRSIData,
    fetchCandlePatternData,
    fetchHarmonicPatternData,
    fetchFundamentalInfo,
    fetchFundamentalInfoClassification,
    fetchInsideTransactions,
    fetchSymbolNews
} from './api.js';

import {
    displayBioResults,
    displayCrossoverResults,
    displayADXResults,
    displayBollingerResults,
    displayRSIResults,
    displayCandleResults,
    displayHarmonicResults,
    displayFundamentalResults,
    displayFundamentalResultsClassification,
    displayInsideTransactions,
    populateYahooStockTable,
    displayNewsList
} from './display.js';


document.addEventListener("DOMContentLoaded", function () {

    setupSearchButton();
    setupStockbytopButton();
    initMetricTooltips({ scope: '#fundamentalAnalysis' });
    initAttributeTooltips({ scope: '#fundamentalAnalysis' });

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];
    // ─────────────── DADOS DA PÁGINA /stock/<symbol> ───────────────
    if (window.location.pathname.startsWith("/stock/") && symbol) {

        setupDownloadLinks(symbol);

        // ─────────────── NOTÍCIAS DO SÍMBOLO ───────────────
        fetchSymbolNews(symbol)
            .then(payload => displayNewsList(payload, { containerId: "symbolNews" }))
            .catch(err => {
                const c = document.getElementById("symbolNews");
                if (c) c.innerHTML = `<div class="news-error">${(err?.message)||"Falha ao obter notícias."}</div>`;
        });

        fetchBioData(symbol).then(data => {
            if (!data.error) displayBioResults(data);
        });

        fetchStockData(symbol).then(data => {
            if (!data.error) renderCandlestickFromData(symbol, data.data);
        });
    
        fetchCrossoverData(symbol).then(data => {
            if (!data.error) displayCrossoverResults(data);
        });
    
        fetchADXData(symbol).then(data => {
            if (!data.error) displayADXResults(data);
        });
    
        fetchBollingerData(symbol).then(data => {
            if (!data.error) displayBollingerResults(data);
        });
    
        fetchRSIData(symbol).then(data => {
            if (!data.error) displayRSIResults(data);
        });
    
        fetchCandlePatternData(symbol).then(data => {
            if (!data.error) displayCandleResults(data);
        });
    
        fetchHarmonicPatternData(symbol).then(data => {
            if (!data.error) displayHarmonicResults(data);
        });
    
        fetchFundamentalInfo(symbol).then(data => {
            if (!data.error) displayFundamentalResults(data);
        });
    
        fetchFundamentalInfoClassification(symbol).then(data => {
            if (!data.error) displayFundamentalResultsClassification(data);
        });
        
        fetchInsideTransactions(symbol).then(data => {
            if (!data.error) displayInsideTransactions(data);
        });

        // ─────────────── EVENTOS DOS BOTÕES ───────────────
        setupTechnicalAnalysisEvents(symbol);

        // ─────────────── CONFIGURAÇÃO DOS TOGGLES ───────────────
        const toggles = [
            { toggleSelector: "#bioToggle", contentSelector: ".bio-content" },
            { toggleSelector: "#tecTrend", contentSelector: ".trend-content" },
            { toggleSelector: "#tecVolatility", contentSelector: ".volatility-content" },
            { toggleSelector: "#tecOscilators", contentSelector: ".oscilators-content" },
            { toggleSelector: "#tecCandles", contentSelector: ".candles-content" },
            { toggleSelector: "#tecHarmonic", contentSelector: ".harmonic-content" },
            { toggleSelector: "#funValuation", contentSelector: ".valuation-content" },
            { toggleSelector: "#funDividends", contentSelector: ".dividends-content" },
            { toggleSelector: "#funProfitability", contentSelector: ".profitability-content" },
            { toggleSelector: "#funHealth", contentSelector: ".health-content" },
            { toggleSelector: "#funCashflow", contentSelector: ".cashflow-content" },
            { toggleSelector: "#funRatios", contentSelector: ".ratios-content" },
            { toggleSelector: "#funRisk", contentSelector: ".risk-content" },
            { toggleSelector: "#funOverview", contentSelector: ".overview-content" },
            { toggleSelector: "#funDownload", contentSelector: ".download-content" },
            { toggleSelector: "#tecInsiders", contentSelector: ".insiders-content" },
        ];

        toggles.forEach(t => {
            setupToggle({ ...t, iconSelector: ".toggle-icon" });
        });
    }    

    if (window.location.pathname.startsWith("/stockbytop/")) {
        fetchYahooStockGainers().then(payload => {
            const rows = Array.isArray(payload) ? payload : payload?.data;
            if (rows?.length) populateYahooStockTable("tableYahooGainers", rows);
        });

        fetchYahooStockTrending().then(payload => {
            const rows = Array.isArray(payload) ? payload : payload?.data;
            if (rows?.length) populateYahooStockTable("tableYahooTrending", rows);
        });

        fetchYahooStockMostActive().then(payload => {
            const rows = Array.isArray(payload) ? payload : payload?.data;
            if (rows?.length) populateYahooStockTable("tableYahooMostActive", rows);
        });
    }
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

function setupStockbytopButton() {
    let stockbytopButton = document.getElementById("stockbytopButton");
    if (stockbytopButton) {
        stockbytopButton.addEventListener("click", function () {
            window.location.href = "/stockbytop/";
        });
    }
}

/* ─────────────── FUNÇÕES DE DOWNLOADS ─────────────── */
function setupDownloadLinks(symbol) {
  const map = [
    ["dl-income-annual",   `/stock/${symbol}/income_download/`],
    ["dl-income-quarter",  `/stock/${symbol}/income_quarterly_download/`],
    ["dl-cf-annual",       `/stock/${symbol}/cashflow_download/`],
    ["dl-cf-quarter",      `/stock/${symbol}/cashflow_quarterly_download/`],
    ["dl-bs-annual",       `/stock/${symbol}/balance_sheet_download/`],
    ["dl-bs-quarter",      `/stock/${symbol}/balance_sheet_quarterly_download/`],
  ];

  for (const [id, href] of map) {
    const el = document.getElementById(id);
    if (el) {
      el.setAttribute("href", href);
      el.setAttribute("download", ""); // opcional, deixa o nome vir do servidor
      el.addEventListener("click", () => {
        // aqui poderias ativar um spinner no botão, se quiseres
      });
    }
  }
}



