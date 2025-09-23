export function coerceNumber(v) {
    if (v === null || v === undefined) return NaN;
    if (typeof v === "number") return v;
    if (typeof v === "string") {
        const cleaned = v.replace(/[%\s]/g, "").replace(",", ".");
        const n = parseFloat(cleaned);
        return Number.isFinite(n) ? n : NaN;
    }
    return NaN;
}
