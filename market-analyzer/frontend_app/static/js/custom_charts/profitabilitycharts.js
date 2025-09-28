// static/js/custom_charts/profitabilitycharts.js
import { fetchSymbolProfitability } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {
  // ===== Helpers =====
  const num = (v) => (Number.isFinite(+v) ? +v : null);
  const numOrNull = (v) => {
    if (v === null || v === undefined) return null;
    if (typeof v === "string" && v.trim().toLowerCase() === "n/a") return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };

  const fmtPct = (v) =>
    v == null
      ? "—"
      : new Intl.NumberFormat("pt-PT", {
          style: "percent",
          minimumFractionDigits: 1,
          maximumFractionDigits: 1,
        }).format(v / 100);

  const fmtCur0 = (v) =>
    v == null
      ? "—"
      : new Intl.NumberFormat("pt-PT", {
          style: "currency",
          currency: "USD",
          maximumFractionDigits: 0,
        }).format(v);

  // Normaliza várias formas de payload:
  // Aceita:
  //  a) payload.series = { labels:[], revenue:[], ebit:[], op_margin:[], roe:[], roa:[], fcf_margin:[] }
  //  b) payload.series = [{period, revenue, ebit, op_margin, roe, roa, fcf_margin}, ...]
  function normalizeProfitability(payload) {
    const s = payload?.series;
    if (!s) return { labels: [], revenue: [], ebit: [], opMargin: [], roe: [], roa: [], fcfMargin: [] };

    // (a) objeto com arrays
    if (Array.isArray(s.labels) && (Array.isArray(s.revenue) || Array.isArray(s.ebit))) {
      return {
        labels: s.labels,
        revenue: (s.revenue || []).map(numOrNull),
        ebit: (s.ebit || []).map(numOrNull),
        opMargin: (s.op_margin || s.operating_margin || []).map(numOrNull),
        roe: (s.roe || []).map(numOrNull),
        roa: (s.roa || []).map(numOrNull),
        fcfMargin: (s.fcf_margin || []).map(numOrNull),
      };
    }

    // (b) array de pontos
    if (Array.isArray(s)) {
      const labels = [];
      const revenue = [];
      const ebit = [];
      const opMargin = [];
      const roe = [];
      const roa = [];
      const fcfMargin = [];
      for (const row of s) {
        labels.push(row.period ?? row.year ?? row.label ?? "");
        revenue.push(numOrNull(row.revenue));
        ebit.push(numOrNull(row.ebit));
        opMargin.push(numOrNull(row.op_margin ?? row.operating_margin));
        roe.push(numOrNull(row.roe));
        roa.push(numOrNull(row.roa));
        fcfMargin.push(numOrNull(row.fcf_margin));
      }
      return { labels, revenue, ebit, opMargin, roe, roa, fcfMargin };
    }

    return { labels: [], revenue: [], ebit: [], opMargin: [], roe: [], roa: [], fcfMargin: [] };
  }

  // ===== Charts =====
  let revEbitChart, roeRoaChart, fcfChart;

  function renderRevEbitMarginChart(id, labels, revenue, ebit, opMarginPct) {
    const ctx = document.getElementById(id);
    if (!ctx) return;

    if (revEbitChart) revEbitChart.destroy();

    revEbitChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Receitas",
            data: revenue,
            yAxisID: "y",
            datalabels: {
              anchor: "end",
              align: "end",
              offset: 4,
              formatter: (v) => fmtCur0(v),
            },
          },
          {
            label: "EBIT",
            data: ebit,
            yAxisID: "y",
            datalabels: {
              anchor: "end",
              align: "end",
              offset: 4,
              formatter: (v) => fmtCur0(v),
            },
          },
          {
            label: "Margem Operacional",
            type: "line",
            data: opMarginPct,
            yAxisID: "y1",
            tension: 0.25,
            pointRadius: 3,
            datalabels: {
              anchor: "end",
              align: "end",
              offset: 4,
              formatter: (v) => fmtPct(v),
            },
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: {
            callbacks: {
              label: (c) => {
                const v = c.parsed.y;
                return c.dataset.yAxisID === "y1"
                  ? `${c.dataset.label}: ${fmtPct(v)}`
                  : `${c.dataset.label}: ${fmtCur0(v)}`;
              },
            },
          },
        },
        scales: {
          y: {
            title: { display: true, text: "$" },
            ticks: { callback: (v) => fmtCur0(v) },
            grid: { drawBorder: false },
          },
          y1: {
            position: "right",
            title: { display: true, text: "Margem" },
            ticks: { callback: (v) => fmtPct(v) },
            grid: { drawOnChartArea: false },
          },
        },
      },
    });
  }

  function renderRoeRoaChart(id, labels, roePct, roaPct) {
    const ctx = document.getElementById(id);
    if (!ctx) return;

    if (roeRoaChart) roeRoaChart.destroy();

    roeRoaChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "ROE",
            data: roePct,
            datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtPct(v) },
          },
          {
            label: "ROA",
            data: roaPct,
            datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtPct(v) },
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtPct(c.parsed.y)}` } },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "%" },
            ticks: { callback: (v) => fmtPct(v) },
            grid: { drawBorder: false },
          },
        },
      },
    });
  }

  function renderFcfMarginChart(id, labels, fcfMarginPct) {
    const ctx = document.getElementById(id);
    if (!ctx) return;

    if (fcfChart) fcfChart.destroy();

    fcfChart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Margem FCF",
            data: fcfMarginPct,
            tension: 0.25,
            pointRadius: 3,
            datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtPct(v) },
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtPct(c.parsed.y)}` } },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "%" },
            ticks: { callback: (v) => fmtPct(v) },
            grid: { drawBorder: false },
          },
        },
      },
    });
  }

  // ===== Bootstrap =====
  const symbol = (window.location.pathname.split("/") || [])[2];
  if (!symbol) {
    console.error("Nenhum símbolo encontrado na URL para Profitability");
    return;
  }

  fetchSymbolProfitability(symbol)
    .then((api) => {
      if (api?.error) {
        console.error("Erro API (profitability):", api.error);
        return;
      }
      const data = api?.data ?? api; // aceita ambos
      const series = normalizeProfitability(data);

      // Render
      renderRevEbitMarginChart(
        "revEbitMarginChart",
        series.labels,
        series.revenue,
        series.ebit,
        series.opMargin
      );
      renderRoeRoaChart("roeRoaChart", series.labels, series.roe, series.roa);
      renderFcfMarginChart("fcfMarginChart", series.labels, series.fcfMargin);
    })
    .catch((err) => console.error("Erro ao carregar Profitability:", err));
});
