////////////////////////////////////
// FINANCIAL HEALTH CHART (Scatter + Heatmap)
////////////////////////////////////

////////////////////////////////////
// FINANCIAL HEALTH CHART (Scatter)
////////////////////////////////////

import { fetchSymbolFinancialHealth } from "../api.js";

document.addEventListener("DOMContentLoaded", function () {

// --- helpers ---
const sectorColors = {}; // cache de cores por setor
function getSectorColor(sector) {
if (!sector) sector = "Unknown";
if (!sectorColors[sector]) {
    // gera uma cor HSL “estável” a partir do nome do setor
    let hash = 0;
    for (let i = 0; i < sector.length; i++) hash = sector.charCodeAt(i) + ((hash << 5) - hash);
    const hue = Math.abs(hash) % 360;
    sectorColors[sector] = `hsl(${hue}, 65%, 50%)`;
}
return sectorColors[sector];
}

// Normaliza número (aceita null/undefined/"N/A")
function numOrNull(v) {
if (v === null || v === undefined) return null;
if (typeof v === "string" && v.trim().toLowerCase() === "n/a") return null;
const n = Number(v);
return Number.isFinite(n) ? n : null;
}

// --- thresholds (podes tornar dinâmico se quiseres) ---
const thr = {
x1: 3.0, // Net Debt/EBITDA Neutral
x2: 1.0, // Strong
x3: 0.0, // Very Strong
y1: 3.0, // Interest coverage Weak
y2: 8.0  // Neutral
};

async function fetchFinancialHealth(symbol) {
  try {
    const api = await fetchSymbolFinancialHealth(symbol);
    if (api?.error) {
      console.error("Erro ao buscar financial health:", api.error);
      return null;
    }
    return api?.data ?? api; 
  } catch (err) {
    console.error("Erro ao carregar financial health:", err);
    return null;
  }
}

// --- RENDER SCATTER ---
let scatterChart;
function renderFinancialScatter(payload) {
const ctx = document.getElementById("financialHealthScatter");
if (!ctx) return;

if (scatterChart) scatterChart.destroy();

const rows = [];
const pushRow = (item, isMain=false) => {
    const x = numOrNull(item?.metrics?.net_debt_ebitda);
    const y = numOrNull(item?.metrics?.interest_coverage);
    if (x === null || y === null) return; // só plota se ambos existirem
    rows.push({
    x, y,
    r: isMain ? 6 : 4, // raio
    company: item.company || item.symbol,
    sector: item.sector || "Unknown",
    isMain
    });
};

pushRow(payload, true);
(payload.peers || []).forEach(p => pushRow(p, false));

const sectors = [...new Set(rows.map(d => d.sector))];
const datasets = sectors.map(sec => ({
    label: sec,
    data: rows.filter(d => d.sector === sec),
    parsing: false,
    showLine: false,
    pointRadius: rows.filter(d => d.sector === sec).map(d => d.r),
    pointBackgroundColor: getSectorColor(sec),
    pointBorderWidth: 0
}));

const mainLabelPlugin = {
  id: "mainPointLabels",
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    chart.data.datasets.forEach(ds => {
      ds.data.forEach(pt => {
        if (!pt || typeof pt.x !== "number" || typeof pt.y !== "number") return;
        const meta = chart.getDatasetMeta(chart.data.datasets.indexOf(ds));
        const i = ds.data.indexOf(pt);
        const vm = meta.data[i];
        if (!vm) return;

        if (pt.isMain) {
          const { x, y } = vm.getProps(['x','y'], true);
          ctx.save();
          ctx.globalAlpha = 0.9;
          ctx.fillStyle = COLOR_TEXT;
          ctx.textAlign = "left";
          ctx.textBaseline = "middle";
          ctx.fillText(pt.company || "", x + 6, y - 6);
          ctx.restore();
        }
      });
    });
  }
};

const guidePlugin = {
    id: "financialGuide",
    afterDraw(chart, args, opts) {
    const {ctx, chartArea:{left,right,top,bottom}, scales:{x,y}} = chart;

    // linhas verticais
    [thr.x1, thr.x2, thr.x3].forEach((vx, idx) => {
        const X = x.getPixelForValue(vx);
        ctx.save();
        ctx.setLineDash([6,4]);
        ctx.lineWidth = 1;
        ctx.strokeStyle = COLOR_TEXT;
        ctx.beginPath();
        ctx.moveTo(X, top);
        ctx.lineTo(X, bottom);
        ctx.stroke();
        // label na linha
        const labels = ["Neutral","Strong","Very Strong"];
        const text = labels[idx];
        ctx.globalAlpha = 0.5;
        ctx.fillStyle = COLOR_TEXT;
        ctx.textAlign = "left";
        ctx.textBaseline = "alphabetic";
        ctx.translate(X - 6, bottom - 12);
        ctx.rotate(-Math.PI/2);
        ctx.fillText(`↑ ${text} ↑`, 0, 0);
        ctx.restore();
    });
    
    // linhas horizontais
    [thr.y1, thr.y2].forEach((vy, idx) => {
        const Y = y.getPixelForValue(vy);
        ctx.save();
        ctx.setLineDash([6,4]);
        ctx.lineWidth = 1;
        ctx.strokeStyle = COLOR_TEXT;
        ctx.beginPath();
        ctx.moveTo(left, Y);
        ctx.lineTo(right, Y);
        ctx.stroke();
        // label na linha
        const labels = ["Weak","Neutral"];
        const text = labels[idx];
        ctx.globalAlpha = 0.5;
        ctx.fillStyle = COLOR_TEXT;
        ctx.textAlign = "left";
        ctx.textBaseline = "alphabetic";
        ctx.translate(left + 6, Y + 12);
        ctx.fillText(`↓ ${text} ↓`, 0, 0);
        ctx.restore();
    });
    }
};

scatterChart = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false }
    },
    scales: {
        x: {
        title: { display: true, text: "Net Debt / EBITDA (Years)" },
        min: -6, max: 6,
        grid: { display: false }
        },
        y: {
        title: { display: true, text: "Interest Coverage (EBIT) (x)" },
        min: -15, max: 15,
        grid: { display: false }
        }
    },
    parsing: false
    },
    plugins: [guidePlugin, mainLabelPlugin]
});

// Avisos se faltarem métricas da “principal”
const warn = [];
if (numOrNull(payload?.metrics?.net_debt_ebitda) === null) {
    warn.push("Net Debt/EBITDA indisponível (EBITDA ≤ 0 ou dados em falta).");
}
if (numOrNull(payload?.metrics?.interest_coverage) === null) {
    warn.push("Interest Coverage indisponível (dados em falta).");
}
if (warn.length) {
    console.warn(warn.join(" "));
}
}

// --- Bootstrap: obter símbolo da URL e renderizar ---
const pathParts = window.location.pathname.split("/");
const symbol = pathParts[2];

if (symbol) {
fetchFinancialHealth(symbol)
    .then(data => {
    // estrutura mínima de fallback se o backend ainda não estiver pronto
    const fallback = {
        symbol,
        company: data?.company ?? symbol,
        sector: data?.sector ?? "Unknown",
        metrics: {
        net_debt_ebitda: numOrNull(data?.metrics?.net_debt_ebitda),
        interest_coverage: numOrNull(data?.metrics?.interest_coverage),
        current_ratio: numOrNull(data?.metrics?.current_ratio),
        quick_ratio: numOrNull(data?.metrics?.quick_ratio)
        },
        peers: Array.isArray(data?.peers) ? data.peers : [] // [{company, sector, metrics:{...}}, ...]
    };
    renderFinancialScatter(fallback);
    renderLiquidityHeatmap(fallback);
    })
    .catch(err => console.error("Erro ao carregar Financial Health:", err));
} else {
console.error("Nenhum símbolo encontrado na URL para Financial Health");
}

////////////////////////////////////
// FINANCIAL HEALTH CHART (Heatmap)
////////////////////////////////////
// --- RENDER BAR CHART (apenas os dois ratios no eixo X) ---
let liquidityChart;
function renderLiquidityHeatmap(payload) { // mantém o nome p/ drop-in
  const ctx = document.getElementById("liquidityHeatmap");
  if (!ctx) return;

  if (liquidityChart) liquidityChart.destroy();

  // valores da "principal"
  const currentMain = numOrNull(payload?.metrics?.current_ratio);
  const quickMain   = numOrNull(payload?.metrics?.quick_ratio);

  // média simples dos peers (opcional)
  let currentPeers = NaN, quickPeers = NaN;
  if (Array.isArray(payload?.peers) && payload.peers.length) {
    let cSum = 0, cN = 0, qSum = 0, qN = 0;
    for (const p of payload.peers) {
      const c = numOrNull(p?.metrics?.current_ratio);
      const q = numOrNull(p?.metrics?.quick_ratio);
      if (c != null && isFinite(c)) { cSum += c; cN++; }
      if (q != null && isFinite(q)) { qSum += q; qN++; }
    }
    currentPeers = cN ? cSum / cN : NaN;
    quickPeers   = qN ? qSum / qN : NaN;
  }

  const labels = ["Current Ratio", "Quick Ratio"];

  const datasets = [
    {
      label: payload?.ticker || payload?.name || "Empresa",
      data: [currentMain, quickMain],
      borderWidth: 1,
      backgroundColor: "rgba(25, 118, 210, 0.45)",
      borderColor: "rgba(25, 118, 210, 0.9)",
    }
  ];

  // se houver peers válidos, acrescenta dataset de comparação
  if (Number.isFinite(currentPeers) || Number.isFinite(quickPeers)) {
    datasets.push({
      label: "Peers (média)",
      data: [currentPeers, quickPeers],
      borderWidth: 1,
      backgroundColor: "rgba(46, 125, 50, 0.45)",
      borderColor: "rgba(46, 125, 50, 0.9)",
    });
  }

  liquidityChart = new Chart(ctx, {
    type: "bar",
    data: { labels, datasets },
    options: {
      maintainAspectRatio: false,
      responsive: true,
      plugins: {
        legend: { display: false, position: "top" },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const v = ctx.parsed.y;
              return `${ctx.dataset.label}: ${Number.isFinite(v) ? v.toFixed(2) + "x" : "N/A"}`;
            },
          },
        },
        datalabels: {
        anchor: 'end',     // “agarra” ao topo da barra
        align: 'end',      // alinha no topo
        offset: 4,         // pequeno afastamento da barra
        clamp: true,       // impede que saia do chart area
        font: { weight: '600' },
        textAlign: 'center' // centrado horizontalmente na barra
        // color: '#111'    // opcional (senão usa a default)
        },
      },
      scales: {
        x: {
          title: { display: true, text: "Ratios" },
          ticks: { autoSkip: false },
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: "x" },
          grid: { drawBorder: false },
        },
      },
    },
  });
}


});
