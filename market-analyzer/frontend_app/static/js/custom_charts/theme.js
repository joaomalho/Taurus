// theme.js

const COLOR_TEXT = "white"

// Regista o plugin de data labels para todos os gráficos
Chart.register(ChartDataLabels);

// ---- Fontes / cores base
Chart.defaults.font.family = "'Inter','Roboto',system-ui,-apple-system,sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = COLOR_TEXT; // cor default de texto (ticks/labels)

// ---- Legend / Tooltip (igual ao teu bar chart: legend escondida)
Chart.defaults.plugins.legend.display = false;
Chart.defaults.plugins.tooltip.enabled = true;

// ---- DataLabels (como no bar chart)
Chart.defaults.plugins.datalabels.anchor = "end";
Chart.defaults.plugins.datalabels.align  = "right";
Chart.defaults.plugins.datalabels.color  = COLOR_TEXT;
Chart.defaults.plugins.datalabels.font   = { weight: "bold", size: 12 };
Chart.defaults.plugins.datalabels.formatter = (v) => {
  const n = Number(v);
  return Number.isFinite(n) ? n.toFixed(2) : "";
};

// ---- Barras (mesmo feeling do teu chart)
Chart.defaults.elements.bar.borderRadius = 10;
Chart.defaults.elements.bar.borderWidth  = 1;
Chart.defaults.elements.bar.borderColor  = "rgba(0,0,0,0)";

// ---- Comportamento base
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.responsive = true;

// ---- Escalas: estilo de ticks e títulos
// (Se quiseres títulos brancos por omissão)
Chart.defaults.scales.category.ticks.color = COLOR_TEXT;
Chart.defaults.scales.linear.ticks.color   = COLOR_TEXT;
// Títulos de eixo (quando activados por gráfico)
Chart.defaults.scales.category.title.color = COLOR_TEXT;
Chart.defaults.scales.linear.title.color   = COLOR_TEXT;

// LEGENDA: garante branco sempre
Chart.defaults.plugins.legend.labels.color = COLOR_TEXT;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.boxWidth = 10;
Chart.defaults.plugins.legend.labels.boxHeight = 10;

// Lines
