// static/js/news.js
import { fetchSymbolNews } from "./api.js";

export function initSymbolNews({
    containerId = "symbolNews",
    symbol,
    locale = "pt-PT",
    timeZone = "Europe/Lisbon",
    limit = 30
    } = {}) {
    const container = document.getElementById(containerId);
    if (!container || !symbol) return;

  mountSkeleton(container);

  fetchSymbolNews(symbol)
    .then(payload => {
        // 1) tratar erro vindo do backend (views.py responde {error: "..."} com status != 200)
        if (payload && payload.error) {
            throw new Error(payload.error);
        }

        // 2) extrair o array de items
        const raw = Array.isArray(payload) ? payload : (payload?.data || []);

        // 3) normalizar, ordenar, deduplicar e limitar
        const items = dedupe(
            sortByDateDesc(raw.map(normalizeNewsItem))
        ).slice(0, limit);

        // 4) render
        renderList(items, container, { locale, timeZone });
    })
    .catch(err => {
        showError(container, err?.message || "Falha ao obter notícias.");
    });
}

/* ---------- helpers ---------- */

export function pickBestImage(t) {
  if (!t) return null;
  const res = Array.isArray(t.resolutions) ? t.resolutions.filter(r => r?.url) : [];
  const best = res.sort((a,b) => (b.width ?? 0) - (a.width ?? 0))[0];
  return best?.url || t.originalUrl || null;
}

export function normalizeNewsItem(raw) {
  const c = raw?.content || {};
  return {
    id: raw?.id || c?.id,
    title: c?.title || "",
    summary: c?.summary || "",
    provider: c?.provider?.displayName || "Fonte",
    url: c?.clickThroughUrl?.url || c?.canonicalUrl?.url || c?.previewUrl || "#",
    publishedAt: c?.displayTime || c?.pubDate || new Date().toISOString(),
    isEditorsPick: !!c?.metadata?.editorsPick,
    isPremium: !!c?.finance?.premiumFinance?.isPremiumNews,
    imageUrl: pickBestImage(c?.thumbnail),
    contentType: c?.contentType || "STORY",
    related: (c?.storyline?.storylineItems || [])
      .map(it => it?.content)
      .filter(Boolean)
      .map(cc => ({
        id: cc.id,
        title: cc.title,
        url: cc.clickThroughUrl?.url || cc.canonicalUrl?.url || cc.previewUrl || "#",
        type: cc.contentType,
        image: pickBestImage(cc.thumbnail),
      })),
  };
}

export function sortByDateDesc(arr){ return [...arr].sort((a,b)=> new Date(b.publishedAt) - new Date(a.publishedAt)); }

function dedupe(arr){
  // usa URL como chave principal; se faltar, usa id
  const seen = new Set();
  return arr.filter(i => {
    const key = i.url || `id:${i.id}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function escapeHTML(s=""){ return s.replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"); }
function timeAgo(iso, now=new Date()){
  const d = (now - new Date(iso))/1000;
  if(d<60) return "agora";
  if(d<3600) return `${Math.floor(d/60)} min`;
  if(d<86400) return `${Math.floor(d/3600)} h`;
  return `${Math.floor(d/86400)} d`;
}
function formatDateISO(iso, locale, timeZone){
  try { return new Intl.DateTimeFormat(locale,{dateStyle:"medium",timeStyle:"short",timeZone}).format(new Date(iso)); }
  catch { return iso || ""; }
}

/* ---------- UI ---------- */

export function renderCard(item, opts){
  const title = escapeHTML(item.title);
  const provider = escapeHTML(item.provider);
  const published = formatDateISO(item.publishedAt, opts.locale, opts.timeZone);
  const ago = timeAgo(item.publishedAt);
  const badges = [
    item.isEditorsPick ? `<span class="news-badge badge-editors">Editor’s pick</span>` : "",
    item.isPremium ? `<span class="news-badge badge-premium">Premium</span>` : "",
    item.contentType === "VIDEO" ? `<span class="news-badge badge-video">Vídeo</span>` : ""
  ].join("");
  const img = item.imageUrl
    ? `<div class="news-thumb"><img src="${item.imageUrl}" alt="${title}" loading="lazy"></div>`
    : `<div class="news-thumb placeholder"></div>`;
  const summary = item.summary ? `<p class="news-summary">${escapeHTML(item.summary)}</p>` : "";
  const related = item.related?.length
    ? `<div class="news-related">
         ${item.related.slice(0,4).map(r =>
           `<a class="news-related-chip" href="${r.url}" target="_blank" rel="noopener noreferrer">${r.type==="VIDEO"?"+ ":""}${escapeHTML(r.title)}</a>`
         ).join("")}
       </div>` : "";

  return `
  <article class="news-card">
    <a class="news-link" href="${item.url}" target="_blank" rel="noopener noreferrer" aria-label="${title}">
      ${img}
      <header class="news-header">
        <div class="news-badges">${badges}</div>
        <span class="news-timeago">${ago}</span>
      </header>
      <h3 class="news-title">${title}</h3>
      ${summary}
      <footer class="news-footer">
        <span class="news-provider">${provider}</span>
        <time datetime="${item.publishedAt}">${published}</time>
      </footer>
    </a>
    ${related}
  </article>`;
}

function renderList(items, container, opts){
  if (!items.length) { container.innerHTML = `<p class="news-empty">Sem notícias.</p>`; return; }
  container.classList.add("news-grid");
  container.innerHTML = items.map(i => renderCard(i, opts)).join("");
}

function mountSkeleton(container, n=6){
  container.classList.add("news-grid");
  container.innerHTML = Array.from({length:n}).map(()=>`
    <div class="news-card skeleton">
      <div class="news-thumb"></div>
      <div class="s-line w-90"></div>
      <div class="s-line w-70"></div>
      <div class="s-line w-50"></div>
    </div>`).join("");
}

function showError(container, msg){
  container.innerHTML = `<div class="news-error">${escapeHTML(msg)}</div>`;
}

export function dedupeByUrl(a) {
  const seen = new Set();
  return a.filter((i) => {
    const k = i.url || `id:${i.id}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}
