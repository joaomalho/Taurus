import { Grid, html } from "./plugins/gridjs.production.es.min.js";

let calendarGrid = null;

function formatDateTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function impactBadge(label) {
  const normalized = String(label || "Low").toLowerCase();
  const cssClass = normalized === "high"
    ? "impact-badge--high"
    : normalized === "medium"
      ? "impact-badge--medium"
      : normalized === "holiday"
        ? "impact-badge--holiday"
        : "impact-badge--low";
  return html(`<span class="impact-badge ${cssClass}">${label || "Low"}</span>`);
}

function renderCalendarTable(events) {
  const container = document.getElementById("ecoCalendarTable");
  if (!container) return;

  container.innerHTML = "";

  if (!events.length) {
    container.innerHTML = "<p class=\"eco-calendar-empty\">No events for this period.</p>";
    return;
  }

  calendarGrid = new Grid({
    columns: [
      { name: "When", formatter: (cell) => formatDateTime(cell) },
      { name: "Country", width: "90px" },
      { name: "Event" },
      { name: "Impact", formatter: (cell) => impactBadge(cell) },
      { name: "Forecast" },
      { name: "Previous" },
      { name: "Actual" },
    ],
    data: events.map((event) => [
      event.datetime,
      event.country || "—",
      event.event || "—",
      event.impact_label || "Low",
      event.forecast || "—",
      event.previous || "—",
      event.actual || "—",
    ]),
    pagination: { limit: 15 },
    sort: true,
    className: { table: "gridjs-table", container: "gridjs-container" },
  }).render(container);
}

async function loadCalendar(timeframe) {
  const meta = document.getElementById("ecoCalendarMeta");
  const notice = document.getElementById("ecoCalendarNotice");
  const errorEl = document.getElementById("ecoCalendarError");

  if (errorEl) errorEl.textContent = "";
  if (notice) notice.classList.add("hidden");
  if (meta) meta.textContent = "Loading…";

  try {
    const response = await fetch(
      `/economic-calendar/events/?timeframe=${encodeURIComponent(timeframe)}`
    );
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Failed to load calendar.");
    }

    renderCalendarTable(payload.events || []);

    if (meta) {
      meta.textContent = `${payload.count || 0} events · source: ${payload.source || "n/a"}`;
    }

    if (notice && payload.notice) {
      notice.textContent = payload.notice;
      notice.classList.remove("hidden");
    }
  } catch (error) {
    if (errorEl) errorEl.textContent = error.message;
    if (meta) meta.textContent = "";
    renderCalendarTable([]);
  }
}

export function initEconomicCalendarPage() {
  const filters = document.querySelectorAll(".eco-filter");
  if (!filters.length) return;

  let activeTimeframe = "today";

  filters.forEach((button) => {
    button.addEventListener("click", () => {
      activeTimeframe = button.dataset.timeframe;
      filters.forEach((item) => item.classList.toggle("active", item === button));
      loadCalendar(activeTimeframe);
    });
  });

  loadCalendar(activeTimeframe);
}
