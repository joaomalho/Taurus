const TEXTOS_GENERICOS = {
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

function preencherTextosGenericos() {
  Object.keys(TEXTOS_GENERICOS).forEach((key) => {
    const el = document.getElementById(key);
    if (el) el.innerHTML = TEXTOS_GENERICOS[key];
  });
}

document.addEventListener('DOMContentLoaded', preencherTextosGenericos);
