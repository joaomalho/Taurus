// static/js/tooltips.js

// Mapa de textos (podes editar/estender)
export const DEFAULT_TIPS = {
  // ----- Valuations ----- //
  // - KPIs
  evEbitda:
    "test \n test \n * test",
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
