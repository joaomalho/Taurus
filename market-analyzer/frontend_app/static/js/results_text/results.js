const TEXTOS_RESULTADOS = {
  net_debt_ebitda_generico: `
    <p><strong>Net Debt / EBITDA</strong> =
    Mede <strong>quantos anos</strong> a empresa levaria para pagar a sua dívida líquida com o <strong>EBITDA</strong> gerado.</p>
  `,
  net_debt_generico: `
    <p><strong>Net Debt (Dívida Líquida)</strong> =
    Dívida total com custo – Caixa & equivalentes.</p>
  `,
  ebitda_generico: `
    <p><strong>EBITDA</strong> =
    Lucro antes de juros, impostos, depreciação e amortização.</p>
  `,
  roic_generico: `
    <p><strong>ROIC</strong> = NOPAT ÷ Capital Investido. Mede a criação de valor.</p>
  `
};


async function fetchSymbolEarningsFunc(symbol) {
  try {
    const payload = await fetchSymbolEarnings(symbol);
    if (payload?.error) {
      console.error("Erro ao buscar earnings:", payload.error);
      return;
    }
    } catch (err) {
    console.error("Erro ao carregar earnings:", err);
  }
}

function preencherTextosResultados() {
  Object.keys(TEXTOS_RESULTADOS).forEach((key) => {
    const el = document.getElementById(key);
    if (el) el.innerHTML = TEXTOS_RESULTADOS[key];
  });
}

document.addEventListener('DOMContentLoaded', preencherTextosResultados);
