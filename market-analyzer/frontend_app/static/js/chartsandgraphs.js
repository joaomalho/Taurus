import { fetchSymbolEarnings } from "./api.js";
import { coerceNumber } from "./helpers.js";

////////////////////////////////////
// STOCK CHARTs
////////////////////////////////////

// Bar Chart Institutional Holders with Tooltip
document.addEventListener("DOMContentLoaded", function () {
  function fetchAndRenderChart(symbol) {
    fetch(`/stock/${symbol}/institutional_holders/`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error("Erro ao buscar dados:", data.error);
          return;
        }

        const chartData = data.data
          .map(d => ({
            holder: d.Holder,
            pctHeld: d.pctHeld,
            shares: d.Shares.toLocaleString(),
            value: `$ ${d.Value.toLocaleString()}`,
            pctChange: d.pctChange.toFixed(2) + "%"
          }))
          .sort((a, b) => b.pctHeld - a.pctHeld);

        renderBarChart(chartData);
      })
      .catch(error => console.error("Erro ao carregar dados:", error));
  }

  function renderBarChart(chartData) {
    const ctx = document.getElementById("hBarChart");
    if (!ctx) {
      console.error("Elemento canvas não encontrado!");
      return;
    }

    if (window.myBarChart) window.myBarChart.destroy();

    window.myBarChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: chartData.map(d => d.holder),
        datasets: [
          {
            label: "Percentage Held",
            data: chartData.map(d => d.pctHeld),
            backgroundColor: "rgba(54, 162, 235, 0.7)", // azul base do tema
            borderColor: "rgba(0,0,0,0)",
            borderWidth: 1,
            barThickness: 15,
            maxBarThickness: 20,
            categoryPercentage: 0.5,
            barPercentage: 0.9,
            borderRadius: 10
          }
        ]
      },
      options: {
        indexAxis: "y",
        // (legend, tooltip, datalabels e cores vêm do theme.js)
        plugins: {
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                const d = chartData[tooltipItem.dataIndex];
                return [
                  `Percentage Held: ${d.pctHeld.toFixed(2)}%`,
                  `Total Shares: ${d.shares}`,
                  `Shares Value: ${d.value}`,
                  `Percentage Change: ${d.pctChange}`
                ];
              }
            }
          },
          datalabels: {
            formatter: (value) => `${Number(value).toFixed(2)}%`
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Percentage Held (%)" },
            ticks: {
              callback: v => `${Number(v).toFixed(2)}%`
            }
          },
          y: {
            title: { display: false, text: "Institutional Holders" }
          }
        }
      }
    });
  }

  const pathParts = window.location.pathname.split("/");
  const symbol = pathParts[2];

  if (symbol) {
    fetchAndRenderChart(symbol);
  } else {
    console.error("Nenhum símbolo encontrado na URL!");
  }

  const searchButton = document.getElementById("searchButton");
  if (searchButton) {
    searchButton.addEventListener("click", function () {
      const symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();
      if (symbol) {
        fetchAndRenderChart(symbol);
      } else {
        alert("Por favor, insira um símbolo de ação válido.");
      }
    });
  }
});

////////////////////////////////////
// EARNINGS CHART (Estimate/Reported/Surprise)
////////////////////////////////////

// helper extra robusto (se o teu helpers.js já faz isto, mantém)
function _coerceNum(v) {
  return coerceNumber ? coerceNumber(v) : (Number(String(v).replace(/[%\s]/g, "").replace(",", ".")));
}

async function fetchAndRenderEarningsChart(symbol) {
  try {
    const payload = await fetchSymbolEarnings(symbol);
    if (payload?.error) {
      console.error("Erro ao buscar earnings:", payload.error);
      return;
    }

    const rows = (payload?.data || [])
      .filter(d => (d.event_type || d.EventType || d["Event Type"]) === "Earnings")
      .map(d => ({
        datetime: d.datetime || d.date || d.Date || d.Datetime,
        epsEstimate: _coerceNum(d.eps_estimate ?? d.epsEstimate ?? d["EPS Estimate"]),
        reportedEps: _coerceNum(d.reported_eps ?? d.reportedEps ?? d["Reported EPS"]),
        surprisePct: _coerceNum(d.surprise_pct ?? d.surprisePercent ?? d["Surprise(%)"])
      }))
      .filter(d =>
        d.datetime &&
        Number.isFinite(d.epsEstimate) &&
        Number.isFinite(d.reportedEps) &&
        Number.isFinite(d.surprisePct)
      )
      .sort((a, b) => new Date(a.datetime) - new Date(b.datetime));

    if (!rows.length) {
      console.warn("Sem dados de Earnings para desenhar.");
      const holder = document.getElementById("earningsChart");
      if (holder) holder.title = "Sem dados de Earnings para este símbolo.";
      return;
    }

    renderEarningsChart(rows);
  } catch (err) {
    console.error("Erro ao carregar earnings:", err);
  }
}

function renderEarningsChart(rows) {
  const ctx = document.getElementById("earningsChart");
  if (!ctx) {
    console.error("Elemento #earningsChart não encontrado.");
    return;
  }

  const labels = rows.map(r => {
    const d = new Date(r.datetime);
    return d.toLocaleDateString(undefined, {
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    });
  });

  const estimate = rows.map(r => r.epsEstimate);
  const reported = rows.map(r => r.reportedEps);
  const surprise = rows.map(r => r.surprisePct);

  if (window.myEarningsChart) window.myEarningsChart.destroy();

  window.myEarningsChart = new Chart(ctx, {
    type: "line", // agora o chart base é de linhas
    data: {
      labels,
      datasets: [
        {
          label: "EPS Estimate",
          data: estimate,
          yAxisID: "yEPS",
          borderWidth: 2,
          pointRadius: 3,
          tension: 0.2,
          fill: false,
          borderColor: "rgba(255, 99, 132, 0.9)" // cor vermelha, só exemplo
        },
        {
          label: "Reported EPS",
          data: reported,
          yAxisID: "yEPS",
          borderWidth: 2,
          pointRadius: 3,
          tension: 0.2,
          fill: false,
          borderColor: "rgba(54, 162, 235, 0.9)" // azul
        },
        {
          label: "Surpresa (%)",
          data: surprise,
          yAxisID: "ySurprise",
          borderWidth: 2,
          pointRadius: 3,
          tension: 0.2,
          fill: false,
          borderColor: "rgba(255, 206, 86, 0.9)" // amarelo
        }
      ]
    },
    options: {
      responsive:true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: true },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              if (ctx.dataset.yAxisID === "ySurprise") {
                return `Surpresa: ${Number(ctx.parsed.y).toFixed(2)}%`;
              }
              const name = ctx.dataset.label || "";
              return `${name}: ${Number(ctx.parsed.y).toFixed(2)}`;
            }
          }
        },
        datalabels: {
          display: false
        }
      },
      scales: {
        yEPS: {
          type: "linear",
          position: "left",
          title: { display: true, text: "EPS" },
          ticks: { callback: v => Number(v).toFixed(2) }
        },
        ySurprise: {
          type: "linear",
          position: "right",
          title: { display: true, text: "Surpresa (%)" },
          grid: { drawOnChartArea: false },
          ticks: { callback: v => `${Number(v).toFixed(0)}%` }
        },
        x: { ticks: { maxRotation: 0, minRotation: 0 } }
      }
    }
  });
}

// inicialização: garante DOM pronto
document.addEventListener("DOMContentLoaded", function () {
  const pathParts = window.location.pathname.split("/");
  const symbol = pathParts[2];

  if (symbol) {
    fetchAndRenderEarningsChart(symbol);
  }

  const searchButton = document.getElementById("searchButton");
  if (searchButton) {
    searchButton.addEventListener("click", function () {
      const s = document.getElementById("stockSymbol").value.trim().toUpperCase();
      if (s) {
        fetchAndRenderEarningsChart(s);
      } else {
        alert("Por favor, insira um símbolo de ação válido.");
      }
    });
  }
});
