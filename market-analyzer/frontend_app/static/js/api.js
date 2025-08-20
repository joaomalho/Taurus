// static/js/api.js


//////////// ###### API: Data for Symbol ###### ////////////
export function fetchBioData(symbol) {
    return fetch(`/stock/${symbol}/bio_info/`).then(res => res.json());
}

export function fetchStockData(symbol) {
    return fetch(`/stock/${symbol}/data_history/?period=1y&interval=1d`).then(res => res.json());
}

export function fetchCrossoverData(symbol, fast = 14, medium = 25, slow = 200) {
    return fetch(`/stock/${symbol}/crossover_trend/?fast=${fast}&medium=${medium}&slow=${slow}`).then(res => res.json());
}

export function fetchADXData(symbol, length = 14) {
    return fetch(`/stock/${symbol}/adx_trend/?length=${length}`).then(res => res.json());
}

export function fetchBollingerData(symbol, length = 14, std = 2) {
    return fetch(`/stock/${symbol}/bollinger_trend/?length=${length}&std=${std}`).then(res => res.json());
}

export function fetchRSIData(symbol, length = 14, upper = 70, lower = 30) {
    return fetch(`/stock/${symbol}/rsi_trend/?length=${length}&upper_level=${upper}&lower_level=${lower}`).then(res => res.json());
}

export function fetchCandlePatternData(symbol) {
    return fetch(`/stock/${symbol}/candle_patterns/`).then(res => res.json());
}

export function fetchHarmonicPatternData(symbol) {
    return fetch(`/stock/${symbol}/harmonic_patterns/`).then(res => res.json());
}

export function fetchFundamentalInfo(symbol) {
    return fetch(`/stock/${symbol}/fundamental_info/`).then(res => res.json());
}

export function fetchFundamentalInfoClassification(symbol) {
    return fetch(`/stock/${symbol}/fundamental_evaluations/`).then(res => res.json());
}

export function fetchInsideTransactions(symbol) {
    return fetch(`/stock/${symbol}/inside_transactions/`).then(res => res.json());
}

//////////// ##### API: Stockbytop ###### ////////////

export function fetchYahooStockGainers() {
    return fetch("/stockbytop/stock_gainers/").then(res => res.json());
}

export function fetchYahooStockTrending() {
    return fetch("/stockbytop/stock_trending/").then(res => res.json());
}

export function fetchYahooStockMostActive() {
    return fetch("/stockbytop/stock_most_active/").then(res => res.json());
}
