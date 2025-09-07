// static/js/tooltips.js

// Mapa de textos (podes editar/estender)
export const DEFAULT_TIPS = {
  trailingPE:
    "Price/Earnings (TTM). Valor mais baixo pode indicar ‘undervalued’, depende do setor e crescimento.",
  sectorTrailingPE:
    "P/E médio do setor, útil para comparação com pares.",
  forwardPE:
    "P/E com base em lucros estimados (12 meses seguintes). Sensível a revisões de analistas.",
  trailingPEClass:
    "Classificação qualitativa do P/E face a thresholds por setor.",
};

// Cria o ícone
function createHelpIcon(text) {
  const icon = document.createElement('span');
  icon.className = 'fund-metric-help';
  icon.setAttribute('tabindex', '0');
  icon.setAttribute('aria-label', 'Mais informação');
  icon.dataset.tooltip = text || '';
  return icon;
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
