function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : "";
}

async function portfolioRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCsrfToken(),
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...options.headers,
        },
        ...options,
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(payload.error || "Portfolio request failed.");
    }
    return payload;
}

export function fetchPortfolio() {
    return portfolioRequest("/portfolio/");
}

export function upsertPortfolioPosition({ symbol, shares, avg_cost }) {
    return portfolioRequest("/portfolio/upsert/", {
        method: "POST",
        body: JSON.stringify({ symbol, shares, avg_cost }),
    });
}

export function removePortfolioPosition(symbol) {
    return portfolioRequest(`/portfolio/${encodeURIComponent(symbol)}/remove/`, {
        method: "POST",
    });
}

function formatMoney(value) {
    if (value == null || Number.isNaN(Number(value))) return "—";
    return `$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatPct(value) {
    if (value == null || Number.isNaN(Number(value))) return "—";
    const sign = value > 0 ? "+" : "";
    return `${sign}${Number(value).toFixed(2)}%`;
}

function formatShares(value) {
    if (value == null || Number.isNaN(Number(value))) return "—";
    return Number(value).toLocaleString(undefined, { maximumFractionDigits: 4 });
}

export function initDashboardPortfolio() {
    const tableBody = document.getElementById("portfolioTableBody");
    const emptyEl = document.getElementById("portfolioEmpty");
    const errorEl = document.getElementById("portfolioError");
    const form = document.getElementById("portfolioForm");
    const symbolInput = document.getElementById("portfolioSymbolInput");
    const sharesInput = document.getElementById("portfolioSharesInput");
    const avgCostInput = document.getElementById("portfolioAvgCostInput");
    const totalsEl = document.getElementById("portfolioTotals");

    if (!tableBody || !form || !symbolInput || !sharesInput) {
        return;
    }

    const showError = (message) => {
        if (errorEl) {
            errorEl.textContent = message;
        }
    };

    const renderTotals = (totals = {}) => {
        if (!totalsEl) return;
        totalsEl.innerHTML = `
            <p><strong>Market value:</strong> ${formatMoney(totals.market_value)}</p>
            <p><strong>Cost basis:</strong> ${formatMoney(totals.cost_basis)}</p>
            <p><strong>P/L:</strong> ${formatMoney(totals.pnl)} (${formatPct(totals.pnl_pct)})</p>
            <p><strong>Positions:</strong> ${totals.position_count ?? 0}</p>
        `;
    };

    const renderPositions = (positions = []) => {
        tableBody.innerHTML = "";
        if (!positions.length) {
            emptyEl?.classList.remove("hidden");
            renderTotals({ position_count: 0 });
            return;
        }

        emptyEl?.classList.add("hidden");
        positions.forEach((row) => {
            const tr = document.createElement("tr");
            const pnlClass = row.pnl > 0 ? "portfolio-pnl-positive" : row.pnl < 0 ? "portfolio-pnl-negative" : "";
            tr.innerHTML = `
                <td><a href="/stock/${row.symbol}/">${row.symbol}</a></td>
                <td>${row.company || row.symbol}</td>
                <td>${formatShares(row.shares)}</td>
                <td>${formatMoney(row.avg_cost)}</td>
                <td>${formatMoney(row.current_price)}</td>
                <td>${formatMoney(row.market_value)}</td>
                <td class="${pnlClass}">${formatMoney(row.pnl)}</td>
                <td class="${pnlClass}">${formatPct(row.pnl_pct)}</td>
                <td><button type="button" data-symbol="${row.symbol}">Remove</button></td>
            `;
            tr.querySelector("button").addEventListener("click", async () => {
                try {
                    await removePortfolioPosition(row.symbol);
                    await loadPortfolio();
                } catch (err) {
                    showError(err.message);
                }
            });
            tableBody.appendChild(tr);
        });
    };

    const loadPortfolio = async () => {
        showError("");
        try {
            const payload = await fetchPortfolio();
            renderPositions(payload.positions || []);
            renderTotals(payload.totals || {});
        } catch (err) {
            showError(err.message);
        }
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        showError("");

        const symbol = symbolInput.value.trim().toUpperCase();
        const shares = sharesInput.value.trim();
        const avgCost = avgCostInput?.value.trim() || "";

        if (!symbol) {
            showError("Enter a symbol.");
            return;
        }
        if (!shares) {
            showError("Enter the number of shares.");
            return;
        }

        try {
            await upsertPortfolioPosition({
                symbol,
                shares,
                avg_cost: avgCost || null,
            });
            symbolInput.value = "";
            sharesInput.value = "";
            if (avgCostInput) avgCostInput.value = "";
            await loadPortfolio();
        } catch (err) {
            showError(err.message);
        }
    });

    loadPortfolio();
}
