import { renderCandlestickFromData } from "./custom_charts/candlestick.js";
import "./custom_charts/chartsandgraphs.js";
import { initMetricTooltips, initAttributeTooltips } from "./tooltips.js";
import {
    fetchYahooStockGainers,
    fetchYahooStockTrending,
    fetchYahooStockMostActive,
    fetchStockSummary,
    fetchCrossoverData,
    fetchADXData,
    fetchBollingerData,
    fetchRSIData,
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
    displayNewsList,
    displayDecisionVerdict,
} from './display.js';

import { initStockWatchlistButton } from './watchlist.js';


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

        if (document.getElementById("watchlistAddButton")) {
            initStockWatchlistButton(symbol);
        }

        fetchStockSummary(symbol)
            .then(summary => {
                if (summary.verdict && !summary.verdict.error) {
                    displayDecisionVerdict(summary.verdict);
                }
                if (summary.news && !summary.news.error) {
                    displayNewsList(summary.news, { containerId: "symbolNews" });
                }
                if (summary.bio && !summary.bio.error) displayBioResults(summary.bio);
                if (summary.data_history && !summary.data_history.error) {
                    renderCandlestickFromData(symbol, summary.data_history.data);
                }
                if (summary.crossover && !summary.crossover.error) displayCrossoverResults(summary.crossover);
                if (summary.adx && !summary.adx.error) displayADXResults(summary.adx);
                if (summary.bollinger && !summary.bollinger.error) displayBollingerResults(summary.bollinger);
                if (summary.rsi && !summary.rsi.error) displayRSIResults(summary.rsi);
                if (summary.candle_patterns && !summary.candle_patterns.error) {
                    displayCandleResults(summary.candle_patterns);
                }
                if (summary.harmonic_patterns && !summary.harmonic_patterns.error) {
                    displayHarmonicResults(summary.harmonic_patterns);
                }
                if (summary.fundamental_info && !summary.fundamental_info.error) {
                    displayFundamentalResults(summary.fundamental_info);
                }
                if (summary.fundamental_evaluations && !summary.fundamental_evaluations.error) {
                    displayFundamentalResultsClassification(summary.fundamental_evaluations);
                }
                if (summary.inside_transactions && !summary.inside_transactions.error) {
                    displayInsideTransactions(summary.inside_transactions);
                }
            })
            .catch(err => {
                const c = document.getElementById("symbolNews");
                if (c) {
                    c.innerHTML = `<div class="news-error">${(err?.message) || "Falha ao obter dados do ativo."}</div>`;
                }
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
            { toggleSelector: "#funKPIs", contentSelector: ".kpis-content" },
            { toggleSelector: "#funHealth", contentSelector: ".health-content" },
            { toggleSelector: "#funDividends", contentSelector: ".dividends-content" },
            { toggleSelector: "#funGrowth", contentSelector: ".growth-content" },
            { toggleSelector: "#funProfitability", contentSelector: ".profitability-content" },
            { toggleSelector: "#funCapitalEf", contentSelector: ".capitalefi-content" },
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
    const toggleIcon = iconSelector ? toggleElement?.querySelector(iconSelector) : null;

    if (!toggleElement || !contentElement) {
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



