import { fetchSymbolEfficiency } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {
  // ===== Helpers =====
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

  function normalizeSeriesObject(s) {
    // Espera: {labels, ebit, tax_rate, cap_invested, roic, wacc, eva}
    if (!s || !Array.isArray(s.labels)) {
      return { labels: [], ebit: [], tax_rate: [], cap_invested: [], roic: [], wacc: [], eva: [] };
    }
    return {
      labels: s.labels,
      ebit: (s.ebit || []).map(numOrNull),
      tax_rate: (s.tax_rate || []).map(numOrNull),      // em %
      cap_invested: (s.cap_invested || []).map(numOrNull), // nível ($)
      roic: (s.roic || []).map(numOrNull),             // em %
      wacc: (s.wacc || []).map(numOrNull),             // em %
      eva: (s.eva || []).map(numOrNull),               // em %
    };
  }

  // ===== Charts =====
  let roicWaccChart, evaChart/*, capInvEbitChart*/;

  function renderRoicWacc(id, labels, roicPct, waccPct) {
    const ctx = document.getElementById(id);
    if (!ctx) return;
    if (roicWaccChart) roicWaccChart.destroy();

    roicWaccChart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "ROIC",
            data: roicPct,
            tension: 0.25,
            pointRadius: 3,
            datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtPct(v) },
          },
          {
            label: "WACC",
            data: waccPct,
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
          tooltip: {
            callbacks: { label: (c) => `${c.dataset.label}: ${fmtPct(c.parsed.y)}` },
          },
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

  function renderEva(id, labels, evaPct) {
    const ctx = document.getElementById(id);
    if (!ctx) return;
    if (evaChart) evaChart.destroy();

    evaChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "EVA (ROIC − WACC)",
            data: evaPct,
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

  // (Opcional) um gráfico de níveis de capital investido vs EBIT para contexto de escala
  // function renderCapInvEbit(id, labels, capInv, ebit) {
  //   const ctx = document.getElementById(id);
  //   if (!ctx) return;
  //   if (capInvEbitChart) capInvEbitChart.destroy();

  //   capInvEbitChart = new Chart(ctx, {
  //     type: "bar",
  //     data: {
  //       labels,
  //       datasets: [
  //         { label: "Capital Investido", data: capInv, yAxisID: "y", datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtCur0(v) } },
  //         { label: "EBIT", data: ebit, yAxisID: "y", datalabels: { anchor: "end", align: "end", offset: 4, formatter: (v) => fmtCur0(v) } },
  //       ],
  //     },
  //     options: {
  //       maintainAspectRatio: false,
  //       responsive: true,
  //       plugins: {
  //         legend: { position: "top" },
  //         tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtCur0(c.parsed.y)}` } },
  //       },
  //       scales: {
  //         y: { title: { display: true, text: "$" }, ticks: { callback: (v) => fmtCur0(v) }, grid: { drawBorder: false } },
  //       },
  //     },
  //   });
  // }

  function renderAll(series) {
    renderRoicWacc("roicWaccChart", series.labels, series.roic, series.wacc);
    renderEva("evaChart", series.labels, series.eva);
    // renderCapInvEbit("capInvEbitChart", series.labels, series.cap_invested, series.ebit);
  }

  // ===== Bootstrap =====
  const symbol = (window.location.pathname.split("/") || [])[2];
  if (!symbol) {
    console.error("Nenhum símbolo encontrado na URL para Capital Efficiency");
    return;
  }

  fetchSymbolEfficiency(symbol)
    .then((api) => {
      if (api?.error) {
        console.error("Erro API (cap efficiency):", api.error);
        return;
      }
      const data = api?.data ?? api;
      const seriesFY = normalizeSeriesObject(data?.series_fy);
      renderAll(seriesFY);
    })
    .catch((err) => console.error("Erro ao carregar Cap Efficiency:", err));
});
