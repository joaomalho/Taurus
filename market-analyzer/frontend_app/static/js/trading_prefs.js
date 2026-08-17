const PREFS_URL = "/trading-prefs/";

function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
}

async function fetchPrefs() {
  const response = await fetch(PREFS_URL, { credentials: "same-origin" });
  if (!response.ok) {
    throw new Error("Failed to load trading preferences.");
  }
  return response.json();
}

async function savePrefs(payload) {
  const response = await fetch(PREFS_URL, {
    method: "PATCH",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to save trading preferences.");
  }
  return data;
}

export async function initDashboardTradingPrefs() {
  const form = document.getElementById("tradingPrefsForm");
  const portfolioInput = document.getElementById("portfolioValueInput");
  const riskInput = document.getElementById("riskPercentInput");
  const errorEl = document.getElementById("tradingPrefsError");
  const successEl = document.getElementById("tradingPrefsSuccess");

  if (!form || !portfolioInput || !riskInput) {
    return;
  }

  try {
    const prefs = await fetchPrefs();
    portfolioInput.value = prefs.portfolio_value;
    riskInput.value = prefs.risk_percent;
  } catch (err) {
    if (errorEl) errorEl.textContent = err.message;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (errorEl) errorEl.textContent = "";
    if (successEl) successEl.textContent = "";

    try {
      await savePrefs({
        portfolio_value: Number(portfolioInput.value),
        risk_percent: Number(riskInput.value),
      });
      if (successEl) successEl.textContent = "Preferências guardadas.";
    } catch (err) {
      if (errorEl) errorEl.textContent = err.message;
    }
  });
}
