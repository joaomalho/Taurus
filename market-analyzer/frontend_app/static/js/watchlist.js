function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : "";
}

async function watchlistRequest(url, options = {}) {
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
        throw new Error(payload.error || "Watchlist request failed.");
    }
    return payload;
}

export function fetchWatchlist() {
    return watchlistRequest("/watchlist/");
}

export function addToWatchlist(symbol) {
    return watchlistRequest("/watchlist/add/", {
        method: "POST",
        body: JSON.stringify({ symbol }),
    });
}

export function removeFromWatchlist(symbol) {
    return watchlistRequest(`/watchlist/${encodeURIComponent(symbol)}/remove/`, {
        method: "POST",
    });
}

export function initDashboardWatchlist() {
    const listEl = document.getElementById("watchlistItems");
    const emptyEl = document.getElementById("watchlistEmpty");
    const errorEl = document.getElementById("watchlistError");
    const form = document.getElementById("watchlistForm");
    const input = document.getElementById("watchlistSymbolInput");

    if (!listEl || !form || !input) {
        return;
    }

    const showError = (message) => {
        if (errorEl) {
            errorEl.textContent = message;
        }
    };

    const renderItems = (symbols) => {
        listEl.innerHTML = "";
        if (!symbols.length) {
            emptyEl?.classList.remove("hidden");
            return;
        }

        emptyEl?.classList.add("hidden");
        symbols.forEach(({ symbol }) => {
            const li = document.createElement("li");
            li.className = "watchlist-item";
            li.innerHTML = `
                <a href="/stock/${symbol}/">${symbol}</a>
                <button type="button" data-symbol="${symbol}">Remove</button>
            `;
            li.querySelector("button").addEventListener("click", async () => {
                try {
                    await removeFromWatchlist(symbol);
                    await loadWatchlist();
                } catch (err) {
                    showError(err.message);
                }
            });
            listEl.appendChild(li);
        });
    };

    const loadWatchlist = async () => {
        showError("");
        try {
            const payload = await fetchWatchlist();
            renderItems(payload.symbols || []);
        } catch (err) {
            showError(err.message);
        }
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        showError("");
        const symbol = input.value.trim().toUpperCase();
        if (!symbol) {
            showError("Enter a symbol.");
            return;
        }

        try {
            await addToWatchlist(symbol);
            input.value = "";
            await loadWatchlist();
        } catch (err) {
            showError(err.message);
        }
    });

    loadWatchlist();
}

export function initStockWatchlistButton(symbol) {
    const button = document.getElementById("watchlistAddButton");
    const message = document.getElementById("watchlistAddMessage");
    if (!button || !symbol) {
        return;
    }

    const showMessage = (text, isError = false) => {
        if (!message) return;
        message.textContent = text;
        message.classList.toggle("watchlist-error", isError);
    };

    button.addEventListener("click", async () => {
        showMessage("");
        try {
            await addToWatchlist(symbol);
            button.disabled = true;
            button.textContent = "In watchlist";
            showMessage("Added to watchlist.");
        } catch (err) {
            if (err.message.includes("already")) {
                button.disabled = true;
                button.textContent = "In watchlist";
            }
            showMessage(err.message, true);
        }
    });

    fetchWatchlist()
        .then((payload) => {
            const symbols = (payload.symbols || []).map((item) => item.symbol);
            if (symbols.includes(symbol.toUpperCase())) {
                button.disabled = true;
                button.textContent = "In watchlist";
            }
        })
        .catch(() => {});
}
