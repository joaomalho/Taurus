import { formatPercent, formatPercentFromFraction, formatMultiple, formatCurrency, formatNumber, formatDate } from "./formatter.js";
import { Grid, html } from "./gridjs.production.es.min.js";
import {normalizeNewsItem, sortByDateDesc, dedupeByUrl, renderCard} from "./news.js";

/* ─────── HELPERS DE ESTILO POR BUCKET ─────── */
function applyBadgeClass(el, bucket) {
  if (!el) return;
  const b = bucket || "neutral";
  el.classList.remove(
    "badge--verygood",
    "badge--good",
    "badge--neutral",
    "badge--bad",
    "badge--verybad",
    "badge--nodata"
  );
  el.classList.add(`badge--${b}`);
}

function applyModalClass(el, bucket) {
  if (!el) return;
  const b = bucket || "neutral";
  el.classList.remove(
    "modal--verygood",
    "modal--good",
    "modal--neutral",
    "modal--bad",
    "modal--verybad",
    "modal--nodata"
  );
  el.classList.add(`modal--${b}`);
}

/* ─────────────── FUNÇÕES DE CRIAÇÃO DE TABELAS ─────────────── */
function createGridTable(rows, columns, containerId = {}) {
  const gridColumns = columns.map(c =>
    typeof c === "string"
      ? c
      : { name: c.name, formatter: c.formatter, sort: c.sort ?? true }
  );

  const data = rows.map(row =>
    columns.map(c => row[ typeof c === "string" ? c : (c.key || c.name) ] ?? null)
  );

  new Grid({
    columns: gridColumns,
    data,
    pagination: { limit: 5 },
    sort: true,
    className: { table: "gridjs-table", container: "gridjs-container" },
  }).render(document.getElementById(containerId));
}

const cellValue = (v) => (v && typeof v === "object" && "data" in v ? v.data : v);

const toNum = (v) => {
  v = cellValue(v); // <— NOVO
  if (v == null || v === "") return null;
  if (typeof v === "number") return Number.isFinite(v) ? v : null;
  // limpa símbolos e converte vírgula decimal -> ponto
  const s = String(v).replace(/[^\d.,-]/g, "").replace(/\./g, "").replace(",", ".");
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
};

const numCompare = (a, b) => {
  const na = toNum(a); // já faz cellValue por dentro
  const nb = toNum(b);
  if (na == null && nb == null) return 0;
  if (na == null) return 1;
  if (nb == null) return -1;
  return na - nb;
};

const dateCompare = (a, b) => {
  const va = cellValue(a); // <— NOVO
  const vb = cellValue(b); // <— NOVO
  const pa = va ? Date.parse(va) : NaN;
  const pb = vb ? Date.parse(vb) : NaN;
  if (Number.isNaN(pa) && Number.isNaN(pb)) return 0;
  if (Number.isNaN(pa)) return 1;   // inválidas no fim
  if (Number.isNaN(pb)) return -1;
  return pa - pb;
};

function renderStockTable(containerId, headers, tableData) {
  new Grid({
    columns: headers,
    data: tableData,
    search: true,
    pagination: true,
    sort: true,
    className: {
      table: "gridjs-table",
      container: "gridjs-container",
    },
  }).render(document.getElementById(containerId));
}

/* ─────────────── FUNÇÕES DE CLASSIFICAÇÃO DE METRICAS + CHARTS─────────────── */
function classifyMetricForGauge(metric, value) {
  if (value === "N/A")
    return { classification: "N/A", color: "#9E9E9E", intervals: [0, 100] };

  switch (metric) {
    case "QuickRatio":
      return {
        classification:
          value >= 2
            ? "Excelente"
            : value >= 1.5
            ? "Bom"
            : value >= 1.0
            ? "Razoável"
            : value >= 0.5
            ? "Fraco"
            : "Muito Fraco",
        color:
          value >= 2
            ? "#068008"
            : value >= 1.5
            ? "#089981"
            : value >= 1.0
            ? "#f2b636"
            : value >= 0.5
            ? "#f24536"
            : "#ed0000",
        intervals: [0.5, 1, 1.5, 2],
      };

    case "CurrentRatio":
      return {
        classification:
          value >= 2.5
            ? "Excelente"
            : value >= 1.5
            ? "Bom"
            : value >= 1.0
            ? "Razoável"
            : value >= 0.5
            ? "Fraco"
            : "Muito Fraco",
        color:
          value >= 2.5
            ? "#068008"
            : value >= 1.5
            ? "#089981"
            : value >= 1.0
            ? "#f2b636"
            : value >= 0.5
            ? "#f24536"
            : "#ed0000",
        intervals: [0.5, 1, 1.5, 2.5],
      };

    case "CashRatio":
      return {
        classification:
          value >= 1.5
            ? "Excelente"
            : value >= 1.0
            ? "Bom"
            : value >= 0.5
            ? "Razoável"
            : value >= 0.1
            ? "Fraco"
            : "Muito Fraco",
        color:
          value >= 1.5
            ? "#068008"
            : value >= 1.0
            ? "#089981"
            : value >= 0.5
            ? "#f2b636"
            : value >= 0.1
            ? "#f24536"
            : "#ed0000",
        intervals: [0.1, 0.5, 1, 1.5],
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
  const tableData = [];

  for (const pattern in data.patterns_detected) {
    data.patterns_detected[pattern].forEach(entry => {
      tableData.push({
        "Padrão": pattern,
        "Stoploss": entry.Stoploss ?? null,     // number cru
        "Sinal": entry.Signal || "N/A",
        "DateISO": entry.Date || null,          // <- ISO cru
        "Resultado": entry.Result || "N/A",
      });
    });
  }

  createGridTable(
    tableData,
    [
      "Padrão",
      { name: "Stoploss", key: "Stoploss",
        // sem formatter
        sort: { compare: numCompare },
      },
      "Sinal",
      { name: "Data", key: "DateISO",
        // sem formatter
        sort: { compare: dateCompare },
      },
      "Resultado",
    ],
    "tableCandlePatterns"
  );
}


export function displayHarmonicResults(data) {
  let tableDataHarmonic = [];

  for (let pattern of data.patterns_detected || []) {
    const signal = pattern.direction === 1 ? "Buy" : "Sell";
    const result = pattern.hit_tp
      ? `TP atingido: ${pattern.hit_tp}`
      : pattern.stop_hit
      ? "Stop Loss"
      : "Aberto";

    tableDataHarmonic.push({
      Padrão: pattern.pattern,
      Direção: signal,
      "Data (D)": pattern.pattern_idx_dates?.[4] || "N/A",
      "Preço (D)": pattern.D_price?.toFixed(5) || "N/A",
      Stop: pattern.STOP?.toFixed(5) || "N/A",
      TP1: pattern.TP1?.toFixed(5) || "N/A",
      TP2: pattern.TP2?.toFixed(5) || "N/A",
      TP3: pattern.TP3?.toFixed(5) || "N/A",
      RR: pattern.rr_ratio?.toFixed(2) || "N/A",
      Reward: pattern.reward?.toFixed(5) || "N/A",
      Risk: pattern.risk?.toFixed(5) || "N/A",
      CD_DIFF: pattern.CD_DIFF?.toFixed(5) || "N/A",
      "X→D Datas": pattern.pattern_idx_dates?.join(" → ") || "N/A",
      "X→D Preços":
        pattern.pattern_idx_prices?.map((p) => p.toFixed(5)).join(" → ") ||
        "N/A",
      Resultado: result,
    });
  }

  createGridTable(
    tableDataHarmonic,
    [
      "Padrão",
      "Direção",
      "Data (D)",
      "Preço (D)",
      "Stop",
      "TP1",
      "TP2",
      "TP3",
      "RR",
      "Reward",
      "Risk",
      "CD_DIFF",
      "X→D Datas",
      "X→D Preços",
      "Resultado",
    ],
    "tableHarmonicPatterns"
  );
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
    CurrentPrice: bioData.CurrentPrice
      ? formatCurrency(bioData.CurrentPrice)
      : "N/A",
    PreviousClose: bioData.PreviousClose
      ? formatCurrency(bioData.PreviousClose)
      : "N/A",
    OpenPrice: bioData.OpenPrice ? formatCurrency(bioData.OpenPrice) : "N/A",
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

/* ─────── QUAL FORMATADOR USAR POR CHAVE ─────── */
const METRIC_STYLE = {
  // valuation
  trailingPE: "multiple",
  sectorTrailingPE: "multiple",
  forwardPE: "multiple",
  PEGRatio: "multiple",

  // dividends
  divCoverageRate: "multiple",
  dividendYield: "percent",
  fiveYearAvgDividendYield: "percent",

  // profitability (%)
  GrossMargin: "percent",
  OperatingMargin: "percent",
  ProfitMargin: "percent",
  ReturnOnEquity: "percent",

  // growth/CAGR (%)
  CostOfRevenueCAGR: "percent",
  TotalRevenueCAGR: "percent",
  OperatingExpensesCAGR: "percent",
  TotalAssetsCAGR: "percent",
  TotalLiabilitiesCAGR: "percent",
  StockholdersEquityCAGR: "percent",
  CurrentRatioCAGR: "percent",
  CashRatioCAGR: "percent",
  OperatingMarginCAGR: "percent",
  ProfitMarginCAGR: "percent",
  ReturnOnEquityCAGR: "percent",

  // rácios adimensionais
  CurrentRatio: "multiple",
  CashRatio: "multiple",

  // montantes (moeda)
  NetIncome: "currency",
  TotalRevenue: "currency",
  CostOfRevenue: "currency",
  GrossProfit: "currency",
  OperatingExpenses: "currency",
  TotalAssets: "currency",
  TotalLiabilities: "currency",
  NetWorth: "currency",
  ShortTermDebtCoverage: "currency",
  CashCashEquivalents: "currency",
  CurrentAssets: "currency",
  CurrentLiabilities: "currency",
  LongTermDebtCoverage: "currency",
  NonCurrentAssets: "currency",
  NonCurrentLiabilities: "currency",
  StockholdersEquity: "currency",

  // cashflow & mercado
  FreeCashflow: "currency",
  OperatingCashflow: "currency",
  CapitalExpenditure: "currency",
  MarketCap: "currency",
  FreeCashflowYield: "percent",

  // risco/sentimento
  beta: "number",
  auditRisk: "number",
  boardRisk: "number",
  recommendationMean: "number",
  targetMeanPrice: "currency",

  // ATENÇÃO: esta costuma vir EM FRAÇÃO (0.0131 -> 1.31%)
  sharesPercentSharesOut: "percentFraction",
};

/* ─────── FORMATADOR CENTRAL ─────── */
function formatByKey(key, value, currency = "USD") {
  const style = METRIC_STYLE[key] || "number";
  switch (style) {
    case "percent":
      return formatPercent(value);
    case "percentFraction":
      return formatPercentFromFraction(value);
    case "multiple":
      return formatMultiple(value);
    case "currency":
      return formatCurrency(value, currency);
    default:
      return formatNumber(value);
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
    targetMeanPrice: marketRiskData.targetMeanPrice || {},
  };

  for (const [key, d] of Object.entries(elements)) {
    const el = document.getElementById(key);
    if (!el) continue;

    const raw = d?.value;
    const numeric = typeof raw === "number" && isFinite(raw) ? raw : null;

    el.textContent = formatByKey(key, numeric, "USD");
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
  const anchorEval =
    data?.evaluations?.valuation?.trailingPE_evaluation ?? null;
  const anchorBucket =
    data?.evaluations?.valuation?.trailingPE_bucket ??
    (anchorEval ? textToBucket(anchorEval) : "neutral");

  const fundamentalsModal = document.querySelector("#fundamentalsModal");
  applyModalClass(fundamentalsModal, anchorBucket);
}

export function displayInsideTransactions(response) {
  const data = response.data;

  if (!Array.isArray(data) || data.length === 0) {
    document.getElementById("tableInsideTransactions").innerHTML =
      "<p>No data to show.</p>";
    return;
  }

  const tableData = data.map(e => ({
    Shares: e.Shares ?? null,                  // number cru
    Value: e.Value ?? null,                    // number cru (para ordenar)
    Description: e.Text ?? "—",
    Insider: e.Insider ?? "—",
    Position: e.Position ?? "—",
    DateISO: e.StartDate ?? null,              // <- ISO cru p/ ordenar
    Ownership: e.Ownership ?? "—",
  }));

  createGridTable(
    tableData,
    [
      "Shares",
      { name: "Value", key: "Value",
        // sem formatter
        sort: { compare: numCompare },
      },
      "Description",
      "Insider",
      "Position",
      { name: "Date", key: "DateISO",
        // sem formatter
        sort: { compare: dateCompare },
      },
      "Ownership",
    ],
    "tableInsideTransactions"
  );
}

export function populateYahooStockTable(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;

    new Grid({
        columns: [
          { name: "Symbol", formatter: cell => html(`<a href="/stock/${cell}/" class="stock-link">${cell}</a>`) },
          "Name",
          { name: "Price",      sort: { compare: numCompare } },
          { name: "Change %",   sort: { compare: numCompare } },
          { name: "Volume",     sort: { compare: numCompare } },
          { name: "Market Cap", sort: { compare: numCompare } },
        ],
        data: data.map(row => [
          row["Symbol"] ?? "N/A",
          row["Name"] ?? "N/A",
          toNum(row["Price"]),       // ← número cru
          toNum(row["Change %"]),    // ← número cru
          toNum(row["Volume"]),      // ← número cru
          toNum(row["Market Cap"]),  // ← número cru
        ]),
        search: {
          selector: (cell) => {
            if (cell == null) return "";
            if (typeof cell === "number" && isFinite(cell)) {
              const s = String(cell); return `${s} ${s.replace(".", ",")}`;
            }
            if (typeof cell === "string" && !Number.isNaN(Date.parse(cell))) {
              const t = Date.parse(cell); return `${cell} ${t}`;
            }
            return String(cell);
          },
        },
        sort: true,
        pagination: { limit: 25 }
      }).render(container);
    }

export function displayNewsList(payload, {
  containerId = "symbolNews",
  locale = "pt-PT",
  timeZone = "Europe/Lisbon",
  limit = 30
} = {}) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const raw = Array.isArray(payload) ? payload : (payload?.data || []);
  const items = dedupeByUrl(sortByDateDesc(raw.map(normalizeNewsItem))).slice(0, limit);

  container.classList.add("news-grid");
  container.innerHTML = items.length
    ? items.map(i => renderCard(i, { locale, timeZone })).join("")
    : `<p class="news-empty">Sem notícias.</p>`;
}
