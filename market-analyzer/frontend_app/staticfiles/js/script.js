import { updateEMALines, updateBollingerBands, renderCandlestickFromData } from './candlestick.js';

import {
    fetchStockData,
    fetchCrossoverData,
    fetchADXData,
    fetchBollingerData,
    fetchRSIData,
    fetchCandlePatternData,
    fetchHarmonicPatternData,
    fetchFundamentalInfo,
    fetchFundamentalInfoClassification,
    fetchBioData,
    fetchYahooStockGainers,
    fetchYahooStockTrending,
    fetchYahooStockMostActive
} from './api.js';

import {
    displayBioResults,
    displayFundamentalResults,
    displayFundamentalResultsClassification,
    displayCrossoverResults,
    displayADXResults,
    displayBollingerResults,
    displayRSIResults,
    displayCandleResults,
    displayHarmonicResults
} from './display.js';

document.addEventListener("DOMContentLoaded", function () {

    setupSearchButton();
    setupScreenerButton();

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];
    
    if (symbol) {
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
    
        fetchBioData(symbol).then(data => {
            if (!data.error) displayBioResults(data);
        });
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

