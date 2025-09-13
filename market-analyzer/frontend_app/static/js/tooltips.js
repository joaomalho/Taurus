// static/js/tooltips.js

// Mapa de textos (podes editar/estender)
export const DEFAULT_TIPS = {
  // ===== Valuation / KPIs =====
  evEbitda: `
**EV/EBITDA** compara o valor do negócio com a geração operacional.
  
- EV = MarketCap + Dívida + Minoritários + Preferenciais − Caixa
- Preferir **EBITDA TTM**; senão, FY
- Evitar bancos/seguradoras e casos com EBITDA negativo
- Regras (gerais): <8x barato | 8–12x justo | >12x caro
- Comparar sempre com setor e histórico
`,

  PriceToSale: `
**P/S** usa receita quando lucros são voláteis/negativos.
  
- Fórmula: MarketCap / Receita (**TTM**)
- Combinar com margens (bruta/operacional)
- Regras (gerais): <2x barato | 2–6x justo | >6x caro
- Software aceita múltiplos maiores; retalho costuma <2x
`,

  EquityFCFYield: `
**Equity FCF Yield** mede retorno de FCF para o acionista.
  
- Fórmula: FCF / MarketCap
- FCF = OCF − Capex (**TTM** se possível)
- Regras: >5% barato | 3–5% justo | <3% caro
- Atenção a FCF inflado por variações de working capital
`,

  EnterpriseFCFYield: `
**Enterprise FCF Yield** normaliza por EV (comparável com diferentes dívidas).
  
- Fórmula: FCF / EV
- Regras: >4% barato | 2,5–4% justo | <2,5% caro
- Evitar bancos/seguradoras
`,

  NetDebtEbitda: `
**Net Debt/EBITDA** mede alavancagem.
  
- Net Debt = Total Debt − (Caixa + ST investments)
- Usar **EBITDA TTM**; senão, FY
- Regras: <1x forte | 1–3x ok | >3x fraco
- Net cash (negativo) = muito forte
`,

  InterestCoverageEbit: `
**Cobertura de Juros** = EBIT / Despesa de Juros.
  
- Alternativa: EBITDA / Juros
- Regras (EBIT): >8x forte | 3–8x ok | <3x fraco
- Se “juros” ≤ 0 → rever dados
`,

  CurrentRatio: `
**Current Ratio** = Ativo Circulante / Passivo Circulante.
  
- Regras: >1,5 forte | 1,0–1,5 ok | <1,0 fraco
- Usa último **quarter** (não TTM)
`,

  QuickRatio: `
**Quick Ratio** = (Ativo Circ. − Inventários) / Passivo Circ.
  
- Regras: >1,0 forte | 0,8–1,0 ok | <0,8 fraco
- Usa último **quarter**
`,

  OperationalMargin: `
**Margem Operacional** = EBIT / Receita.
  
- Preferir **TTM**; senão, FY
- Regra geral: ≥15% forte (ajustar por setor)
`,

  FcfMargin: `
**Margem FCF** = FCF / Receita.
  
- FCF = OCF − Capex (**TTM**)
- Regras: ≥10% forte | 5–10% ok | <5% fraco
`,

  ROIC: `
**ROIC** = NOPAT / Capital Investido Médio.
  
- NOPAT ≈ EBIT × (1 − taxa efetiva)
- Capital Investido: “Invested Capital” médio (t, t−1) ou dívida + equity − caixa
- **Criar valor**: ROIC > WACC (proxy thresholds: >12% forte | 6–12% ok | <6% fraco)
`,

  ROE: `
**ROE** = Net Income / Equity Médio.
  
- Regras: >15% forte | 8–15% ok | <8% fraco
- Cuidado: alavancagem elevada pode inflacionar o ROE
`,

  ROA: `
**ROA** = Net Income / Ativos Médios.
  
- Regras: >7% forte | 3–7% ok | <3% fraco
- Útil para comparar eficiência entre setores intensivos em ativos
`,

  // ===== Price : Earnings =====
  trailingPE:
    "P/E (TTM). Mais baixo pode indicar ‘undervalued’, mas depende do crescimento e do setor.",
  sectorTrailingPE:
    "P/E médio do setor — bom para comparar com pares imediatos.",
  forwardPE:
    "P/E com base em lucros estimados (12M seguintes). Sensível a revisões de analistas.",
  trailingPEClass:
    "Classificação qualitativa do P/E face a thresholds por setor.",

  // ===== Eficiência de Capital =====
  WACC: `
**WACC** = custo médio ponderado do capital (equity + dívida).
  
- Ce (CAPM): Rf + β × ERP
- Cd: Juros / Dívida (após impostos: × (1 − taxa))
- Pesos: E/(D+E) e D/(D+E) com **market cap** e dívida líquida atuais
- Regra: comparar **ROIC vs WACC** para medir criação de valor
`,

  CapitalTurnover: `
**Giro do Capital Investido** = Receita (**TTM**) / Capital Investido Médio.
  
- Mostra quantas “voltas” a receita dá no capital investido
- Alto em retalho/serviços leves; baixo em setores intensivos em ativos
`,
GrowthReveneuYoY: `
**Crescimento de Vendas (YoY)** = Receita FY atual vs FY anterior.
- Evita sazonalidade dos trimestres
- Regras: ≥10% forte | 4–10% moderado | <4% fraco
`,
CagrGrowthReveneuYoY: `
**CAGR 3 anos (Vendas)** = taxa composta em 3 FY.
- Captura tendência estrutural
- Ignora ruído de um único ano
`,
GrowthEPSYoY: `
**Crescimento de EPS (YoY)** = EPS FY atual vs FY anterior.
- Sensível a recompras e itens não recorrentes
- Regras: ≥10% forte | 4–10% moderado | <4% fraco
`,
CagrGrowthEPSYoY: `
**CAGR 3 anos (EPS)** = taxa composta em 3 FY.
- Preferir EPS diluído
- Se possível, validar com Net Income e ações médias
`,
ShareholderYield: `
**Shareholder Yield** = (Dividendos + Recompras) / Market Cap.

- Dividendos: "Cash Dividends Paid" (TTM)
- Recompras: "Repurchase Of Capital Stock" (TTM)
- Preferir TTM; fallback FY
- Regras: >5% excelente | 2–5% ok | <2% baixo
- Cruzar com FCF e payout para sustentabilidade
`,
};

function createHelpIcon(text) {
  const icon = document.createElement('span');
  icon.className = 'fund-metric-help';
  icon.setAttribute('tabindex', '0');
  icon.setAttribute('aria-label', 'Mais informação');
  icon.setAttribute('aria-haspopup', 'dialog');

  const bubble = document.createElement('div');
  bubble.className = 'fund-tooltip';
  bubble.innerHTML = renderMiniMarkdown(text || '');
  bubble.hidden = true;                       // <-- escondido por defeito
  icon.appendChild(bubble);

  // acessibilidade: associa o tooltip
  const id = 'tip-' + Math.random().toString(36).slice(2);
  bubble.id = id;
  bubble.setAttribute('role', 'tooltip');
  icon.setAttribute('aria-describedby', id);

  // controladores: hover/focus
  const open = () => { bubble.hidden = false; };
  const close = () => { bubble.hidden = true; };
  icon.addEventListener('mouseenter', open);
  icon.addEventListener('mouseleave', close);
  icon.addEventListener('focusin', open);
  icon.addEventListener('focusout', close);

  // mobile/click toggle
  icon.addEventListener('click', (e) => {
    e.stopPropagation();
    bubble.hidden = !bubble.hidden;
    icon.classList.toggle('is-open', !bubble.hidden);
  });
  document.addEventListener('click', () => { bubble.hidden = true; icon.classList.remove('is-open'); });

  return icon;
}


/* Mini parser: -/ * viram <ul><li>, linhas em branco separam <p> */
function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function renderMiniMarkdown(src = "") {
  const lines = src.split(/\r?\n/);
  let html = "";
  let buffer = [];
  let inList = false;

  const flushP = () => {
    if (buffer.length) {
      html += `<p>${escapeHtml(buffer.join(" ").trim())}</p>`;
      buffer = [];
    }
  };

  for (let raw of lines) {
    const line = raw.trim();
    if (!line) { // parágrafo novo
      if (inList) { html += "</ul>"; inList = false; }
      flushP();
      continue;
    }
    const m = line.match(/^[-*]\s+(.*)$/);
    if (m) {
      flushP();
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${escapeHtml(m[1])}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      buffer.push(line);
    }
  }
  if (inList) html += "</ul>";
  flushP();
  return html;
}

/**
 * Inicializa tooltips dentro de um escopo.
 * @param {Object} opts
 * @param {string|Element} [opts.scope='.fund-valuation'] - seletor ou elemento onde procurar
 * @param {string} [opts.selector='p'] - seletor dos elementos que receberão o ícone
 * @param {Object} [opts.tips=DEFAULT_TIPS] - mapa id->texto
 * @param {boolean} [opts.once=true] - evita duplicar ícones
 */
export function initMetricTooltips({
  scope = '.fund-valuation',
  selector = 'p',
  tips = DEFAULT_TIPS,
  once = true,
} = {}) {
  const root = typeof scope === 'string' ? document.querySelector(scope) : scope;
  if (!root) return;

  const paragraphs = root.querySelectorAll(selector);
  paragraphs.forEach(p => {
    if (once && p.querySelector('.fund-metric-help')) return;

    // prioridade: data-tooltip no próprio <p> → data-tooltip no <span> → mapa por ID
    let text =
      p.getAttribute('data-tooltip') ||
      p.querySelector('[data-tooltip]')?.getAttribute('data-tooltip') ||
      null;

    if (!text) {
      const valueSpan = p.querySelector('span[id]');
      if (valueSpan) {
        const key = valueSpan.id;
        text = tips[key] || tips[key.replace(/Class$/, '')] || null;
      }
    }

    if (!text) return;

    p.appendChild(createHelpIcon(text));
  });
}

export function initAttributeTooltips({
  scope = document,
  selector = '.has-tooltip',
  once = true,
} = {}) {
  const root = typeof scope === 'string' ? document.querySelector(scope) : scope;
  if (!root) return;
  root.querySelectorAll(selector).forEach(el => {
    if (once && el.querySelector('.fund-metric-help')) return;
    const text = el.getAttribute('data-tooltip');
    if (!text) return;
    el.appendChild(createHelpIcon(text));
  });
}

/* Pequena ajuda para registar tooltips dinamicamente */
export function registerMetricTip(id, text, tipsMap = DEFAULT_TIPS) {
  tipsMap[id] = text;
}
