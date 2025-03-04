document.addEventListener("DOMContentLoaded", function () {
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        fetchCandlestickData(symbol, "1mo", "1d");  
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }
});

function fetchCandlestickData(symbol, period, interval) {
    fetch(`/stock/${symbol}/data_history/?period=${period}&interval=${interval}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Erro ao buscar dados do candlestick:", data.error);
                document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                processCandlestickData(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar os dados do candlestick:", error);
            document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}


function processCandlestickData(data) {
    if (!data.data || data.data.length === 0) {
        console.error("Nenhum dado encontrado no JSON:", data);
        document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Nenhum dado disponível</h3>`;
        return;
    }

    console.log("Processando dados para o gráfico:", data.data);

    let maxDataPoints = 500;
    let trimmedData = data.data.slice(-maxDataPoints);

    let dates = trimmedData.map(entry => entry.Date ? new Date(entry.Date).toISOString().split("T")[0] : "Desconhecido");
    let openPrices = trimmedData.map(entry => parseFloat(entry.Open) || 0);
    let highPrices = trimmedData.map(entry => parseFloat(entry.High) || 0);
    let lowPrices = trimmedData.map(entry => parseFloat(entry.Low) || 0);
    let closePrices = trimmedData.map(entry => parseFloat(entry.Close) || 0);

    console.log("Dados extraídos para o gráfico:", { dates, openPrices, highPrices, lowPrices, closePrices });

    renderCandlestickChart(dates, openPrices, highPrices, lowPrices, closePrices);
}

function renderCandlestickChart(dates, open, high, low, close) {
    let trace = {
        x: dates,
        open: open,
        high: high,
        low: low,
        close: close,
        type: 'candlestick',
        increasing: { line: { color: 'green' } },
        decreasing: { line: { color: 'red' } }
    };

    let layout = {
        title: 'Histórico de Preços',
        xaxis: { type: 'date' },
        yaxis: { title: 'Preço' },
        dragmode: 'pan'
    };

    Plotly.newPlot('candlestickChart', [trace], layout);
}
