/* ─────── FORMATADORES DE VALORES ─────── */
export function formatPercent(value, min = 2, max = 2) {
  return typeof value === "number" && isFinite(value)
    ? value.toLocaleString("pt-PT", {
        minimumFractionDigits: min,
        maximumFractionDigits: max,
      }) + "%"
    : "N/A";
}

export function formatPercentFromFraction(value, min = 2, max = 2) {
  // 0.0131 -> "1,31%"
  return typeof value === "number" && isFinite(value)
    ? (value * 100).toLocaleString("pt-PT", {
        minimumFractionDigits: min,
        maximumFractionDigits: max,
      }) + "%"
    : "N/A";
}

export function formatMultiple(value, min = 2, max = 2) {
  return typeof value === "number" && isFinite(value)
    ? value.toLocaleString("pt-PT", {
        minimumFractionDigits: min,
        maximumFractionDigits: max,
      }) + "x"
    : "N/A";
}

export function formatCurrency(value, currency = "USD", min = 2, max = 2) {
  if (typeof value !== "number" || !isFinite(value)) return "N/A";

  return value.toLocaleString("pt-PT", {
    style: "currency",
    currency,
    minimumFractionDigits: min,
    maximumFractionDigits: max,
    // notation: "compact",
    currencyDisplay: "narrowSymbol", // "symbol" | "code" | "name" | "narrowSymbol"
  });
}
// "symbol" → 100 000,00 US$
// "code" → 100 000,00 USD
// "name" → 100 000,00 dólares dos Estados Unidos
// "narrowSymbol" → 100 000,00 $

/* ─────── NÚMEROS "LIVRES" ─────── */
export function formatNumber(value, min = 2, max = 2) {
  return typeof value === "number" && isFinite(value)
    ? value.toLocaleString("pt-PT", {
        minimumFractionDigits: min,
        maximumFractionDigits: max,
        // notation: "compact",
      })
    : "N/A";
}

/* ─────── FUNÇÃO PARA FORMATAR VALORES DATA ─────── */
export function formatDate(dateStr) {
  if (!dateStr) return "N/A";
  const date = new Date(dateStr);
  return date.toLocaleString("pt-PT", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
