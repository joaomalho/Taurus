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

/* ─────── FUNÇÃO PARA FORMATAR VALORES DATA ─────── */
function formatDate(dateStr) {
    if (!dateStr) return "N/A";
    const date = new Date(dateStr);
    return date.toLocaleDateString("pt-PT"); 
}

/* ─────── HELPERS DE ESTILO POR BUCKET ─────── */
function applyBadgeClass(el, bucket) {
    if (!el) return;
    const b = bucket || "neutral";
    el.classList.remove(
        "badge--verygood","badge--good","badge--neutral","badge--bad","badge--verybad","badge--nodata"
    );
    el.classList.add(`badge--${b}`);
}

function applyModalClass(el, bucket) {
    if (!el) return;
    const b = bucket || "neutral";
    el.classList.remove(
        "modal--verygood","modal--good","modal--neutral","modal--bad","modal--verybad","modal--nodata"
    );
    el.classList.add(`modal--${b}`);
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

function renderStockTable(containerId, headers, tableData) {
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

/* ─────────────── FUNÇÕES DE MANIPULAÇÃO DE DADOS ─────────────── */
export function displayCrossoverResults(data) {
    const signal = data.signal;
    document.getElementById("CrossSignal").textContent = signal;
}

export function displayADXResults(data) {
    const signal = data.signal;
    document.getElementById("AdxSignal").textContent = signal;
}

export function displayBollingerResults(data) {
    const signal = data.signal;
    document.getElementById("BollSignal").textContent = signal;
}

export function displayRSIResults(data) {
    const rsi = parseFloat(data.rsi).toFixed(2);
    const signal = data.signal;
    document.getElementById("Rsi").textContent = rsi;
    document.getElementById("RsiSignal").textContent = signal;
}

export function displayCandleResults(data) {
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

export function displayHarmonicResults(data) {
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

export function populateYahooStockTable(containerId, data) {
    if (!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = "<h2>Nenhum dado disponível</h2>";
        return;
    }

    let headers = Object.keys(data[0]);

    const tableData = data.map(row =>
        headers.map(header => {
            if (header === "Symbol") {
                return gridjs.html(`<a href="/stock/${row[header]}/" class="stock-link">${row[header]}</a>`);
            }
            return row[header] !== undefined && row[header] !== null ? row[header] : "-";
        })
    );

    renderStockTable(containerId, headers, tableData);
}

export function displayBioResults(data) {
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
export function displayFundamentalResults(data) {
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

export function displayFundamentalResultsClassification(data) {
    // mapa: [secção em data.evaluations, chave base]
    const fields = [
        ["valuation", "trailingPE"],
        ["valuation", "PEGRatio"],
        ["dividends", "divCoverageRate"],
        ["profitability", "CostOfRevenueCAGR"],
        ["profitability", "TotalRevenueCAGR"],
        ["liquidity", "NetWorth"],
        ["liquidity", "ShortTermDebtCoverage"],
        ["liquidity", "LongTermDebtCoverage"],
        ["liquidity", "StockholdersEquityCAGR"],
        ["liquidity", "TotalAssetsCAGR"],
        ["liquidity", "TotalLiabilitiesCAGR"],
        ["cashflow", "FreeCashflowYield"],
        ["ratios", "CurrentRatio"],
        ["ratios", "CurrentRatioCAGR"],
        ["ratios", "CashRatio"],
        ["ratios", "CashRatioCAGR"],
        ["ratios", "GrossMargin"],
        ["ratios", "OperatingMargin"],
        ["ratios", "OperatingMarginCAGR"],
        ["ratios", "ProfitMargin"],
        ["ratios", "ProfitMarginCAGR"],
        ["ratios", "ReturnOnEquity"],
        ["ratios", "ReturnOnEquityCAGR"],
    ];

    for (const [section, key] of fields) {
        const evaluation =
        data?.evaluations?.[section]?.[`${key}_evaluation`] ?? null;

        const bucket =
        data?.evaluations?.[section]?.[`${key}_bucket`] ??
        (evaluation ? textToBucket(evaluation) : "nodata");

        // escreve texto + aplica cor no chip principal
        const el = document.getElementById(`${key}Class`);
        if (el) {
        el.textContent = evaluation ?? "N/A";
        applyBadgeClass(el, bucket);
        }

        // escreve texto + aplica cor na versão “overview” (se existir)
        const elOverview = document.getElementById(`${key}ClassOverview`);
        if (elOverview) {
        elOverview.textContent = evaluation ?? "N/A";
        applyBadgeClass(elOverview, bucket);
        }
    }

    // Pintar a MODAL de fundamentals com uma âncora (ex.: trailingPE)
    const anchorEval = data?.evaluations?.valuation?.trailingPE_evaluation ?? null;
    const anchorBucket =
        data?.evaluations?.valuation?.trailingPE_bucket ??
        (anchorEval ? textToBucket(anchorEval) : "neutral");

    const fundamentalsModal = document.querySelector("#fundamentalsModal");
    applyModalClass(fundamentalsModal, anchorBucket);
}

export function displayInsideTransactions(response) {
    const data = response.data; // <- extrai o array corretamente

    if (!Array.isArray(data) || data.length === 0) {
        document.getElementById("tableInsideTransactions").innerHTML = "<p>No data to show.</p>";
        return;
    }

    const tableData = data.map(entry => ({
        "Shares": entry.Shares?.toLocaleString() || "-",
        "Value": formatCurrency(entry.Value),
        "Description": entry.Text,
        "Insider": entry.Insider,
        "Position": entry.Position,
        "Date": formatDate(entry.StartDate),
        "Ownership": entry.Ownership
    }));

    createGridTable(
        tableData,
        ["Shares", "Value", "Description", "Insider", "Position", "Date", "Ownership"],
        "tableInsideTransactions"
    );
}



