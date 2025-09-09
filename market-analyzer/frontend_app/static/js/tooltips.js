// static/js/tooltips.js

// Mapa de textos (podes editar/estender)
export const DEFAULT_TIPS = {
  // ----- Valuations ----- //
  // - KPIs
  evEbitda: `
    EV/EBITDA compara o valor da empresa (EV) com a geração operacional (EBITDA). É menos sensível à alavancagem do que o P/E.

    - EV = MarketCap + Dívida + Minoritários + Preferenciais − Caixa e ST investments
    - Usar EBITDA TTM; se não houver, FY mais recente
    - Evitar bancos/seguradoras e casos com EBITDA negativo
    - Regras (gerais): <8x barato | 8–12x justo | >12x caro
    - Ajustar por setor: comparar com a mediana do setor e com o histórico (percentis de 5 anos)
    `,
  PriceToSale: `
    P/S (Price to Sales) usa receita quando lucro é volátil ou negativo. Bom para early-stage e cíclicas.

    - Fórmula: MarketCap / Receita (TTM)
    - Útil quando margens ainda estão a escalar; combinar com margens brutas/operacionais
    - Regras (gerais): <2x barato | 2–6x justo | >6x caro
    - Ajustar por setor: software tende a aceitar múltiplos mais altos; retalho costuma <2x
    `,
  EquityFCFYield: `
    Equity FCF Yield mede o retorno de free cash flow para o acionista.

    - Fórmula: Free Cash Flow / MarketCap
    - FCF = Operating Cash Flow − Capex (ideal: TTM e normalizado)
    - Regras (gerais): >5% barato | 3–5% justo | <3% caro
    - Setores regulados podem exigir limiares mais altos; “growth” tolera <3%
    - Se FCF for negativo ou errático, ocultar ou sinalizar outliers
    `,
  EnterpriseFCFYield: `
    Enterprise FCF Yield compara FCF com o valor do negócio (EV), tornando a métrica comparável entre diferentes níveis de dívida.

    - Fórmula: Free Cash Flow / EV
    - EV = MarketCap + Dívida + Minoritários + Preferenciais − Caixa
    - Regras (gerais): >4% barato | 2,5–4% justo | <2,5% caro
    - Evitar bancos/seguradoras; atenção a FCF inflado por variações de working capital
    `,
    NetDebtEbitda: `
**Net Debt/EBITDA** mede alavancagem efetiva.

- Net Debt = Total Debt − (Cash & ST investments)
- Usar EBITDA TTM; se não houver, FY
- Regras: <1x Forte | 1–3x Ok | >3x Fraco
- Net cash (negativo) = muito forte; EBITDA ≤ 0 → N/A/Fraco
`,
  InterestCoverageEbit: `
**Cobertura de Juros** (EBIT / Juros) mostra folga para pagar juros.

- Alternativa: EBITDA / Juros
- Regras (EBIT): >8x Forte | 3–8x Ok | <3x Fraco
- Se “Juros” ≤ 0 ou negativos → verificar qualidade do dado
`,
  CurrentRatio: `
**Current Ratio** = Ativo Circulante / Passivo Circulante.

- Regras: >1,5 Forte | 1,0–1,5 Ok | <1,0 Fraco
- Combina com Quick Ratio p/ visão mais conservadora
`,
  QuickRatio: `
**Quick Ratio** = (Ativo Circ. − Inventários) / Passivo Circ.

- Regras: >1,0 Forte | 0,8–1,0 Ok | <0,8 Fraco
- Evita dependência de vender inventário para pagar obrigações
`,
  OperatingMargin: `
**Margem Operacional** = EBIT / Receita.
- Ideal: usar TTM; senão, FY
- ≥15% costuma ser forte (ajuste por setor)
`,
  FcfMargin: `
**Margem FCF** = Free Cash Flow / Receita.
- FCF = Cash from Ops − Capex (TTM se possível)
- ≥10% forte; 5–10% ok; <5% fraco (ajustar por setor)
`,
  // - Price : Earnings
  trailingPE:
    "Price/Earnings (TTM). Valor mais baixo pode indicar ‘undervalued’, depende do setor e crescimento.",
  sectorTrailingPE:
    "P/E médio do setor, útil para comparação com pares.",
  forwardPE:
    "P/E com base em lucros estimados (12 meses seguintes). Sensível a revisões de analistas.",
  trailingPEClass:
    "Classificação qualitativa do P/E face a thresholds por setor.",
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
