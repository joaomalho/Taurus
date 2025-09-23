// === Financial Health charts (Scatter + Heatmap) ===
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

// constrói pontos (empresa + pares se existirem)
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

// datasets por setor (cores por setor)
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

// plugin para desenhar linhas guia + rótulos de linha + quadrantes
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
        ctx.textAlign = "center";
        ctx.textBaseline = "alphabetic";
        ctx.translate(X + 15, bottom - 50);
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
        ctx.fillText(`↓ ${text} ↓`, left + 6, Y - 6);
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
        legend: { display: true }
    },
    scales: {
        x: {
        title: { display: true, text: "Net Debt / EBITDA (x)" },
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

// --- RENDER HEATMAP (Current vs Quick Ratio por setor) ---
let heatmapChart;
function renderLiquidityHeatmap(payload) {
const ctx = document.getElementById("liquidityHeatmap");
if (!ctx) return;

if (heatmapChart) heatmapChart.destroy();

// Agrega por setor (média simples; podes trocar para mediana)
const rows = [];
const all = [];
const pushRow = (item) => {
    all.push({
    sector: item.sector || "Unknown",
    current: numOrNull(item?.metrics?.current_ratio),
    quick: numOrNull(item?.metrics?.quick_ratio)
    });
};
pushRow(payload);
(payload.peers || []).forEach(pushRow);

const bySector = {};
all.forEach(r => {
    if (r.current === null && r.quick === null) return;
    if (!bySector[r.sector]) bySector[r.sector] = {n:0, current:0, quick:0};
    if (r.current !== null) { bySector[r.sector].current += r.current; }
    if (r.quick   !== null) { bySector[r.sector].quick   += r.quick; }
    bySector[r.sector].n += 1;
});

const sectors = Object.keys(bySector);
sectors.forEach(sec => {
    const n = bySector[sec].n || 1;
    rows.push({ sector: sec, metric: "Current Ratio", value: bySector[sec].current / n });
    rows.push({ sector: sec, metric: "Quick Ratio",   value: bySector[sec].quick   / n });
});

// mapear setores e métricas para coordenadas da matriz
const sectorIndex = [...new Set(rows.map(r => r.sector))];
const metricIndex = ["Current Ratio", "Quick Ratio"];

const matrixData = rows.map(r => ({
    x: metricIndex.indexOf(r.metric),
    y: sectorIndex.indexOf(r.sector),
    v: r.value
}));

// escala de cores simples (quanto maior, mais “intenso”)
function valueToRGBA(v) {
    if (v === null || !Number.isFinite(v)) return "rgba(200,200,200,0.3)";
    // mapeia 0..3.5 para 0..1
    const t = Math.max(0, Math.min(1, v / 3.5));
    const g = Math.round(80 + 150 * t);
    return `rgba(0, ${g}, 0, ${0.15 + 0.55 * t})`; // verde com alpha crescente
}

heatmapChart = new Chart(ctx, {
    type: "matrix",
    data: {
    datasets: [{
        label: "Liquidity by Sector",
        data: matrixData,
        width: ({chart}) => (chart.chartArea.width / metricIndex.length) * 0.9,
        height: ({chart}) => (chart.chartArea.height / sectorIndex.length) * 0.9,
        backgroundColor: (ctx) => valueToRGBA(ctx.raw.v),
        borderWidth: 1,
        borderColor: "rgba(0,0,0,0.1)"
    }]
    },
    options: {
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
        callbacks: {
            title: (items) => {
            const r = items[0].raw;
            return `${sectorIndex[r.y]} — ${metricIndex[r.x]}`;
            },
            label: (item) => {
            const v = item.raw.v;
            return `Valor: ${v != null && isFinite(v) ? v.toFixed(2) + "x" : "N/A"}`;
            }
        }
        }
    },
    scales: {
        x: {
        type: "linear",
        position: "top",
        ticks: {
            callback: (v) => metricIndex[v] ?? ""
        },
        min: -0.5,
        max: metricIndex.length - 0.5,
        grid: { display: false }
        },
        y: {
        type: "linear",
        ticks: {
            callback: (v) => sectorIndex[v] ?? ""
        },
        reverse: true,
        min: -0.5,
        max: sectorIndex.length - 0.5,
        grid: { display: false }
        }
    }
    }
});
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

});
