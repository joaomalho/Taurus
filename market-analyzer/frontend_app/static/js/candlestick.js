document.addEventListener("DOMContentLoaded", function () {

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        fetchCandlestickData(symbol, "1mo", "1d");  
    } else {
        console.error("🚨 Nenhum símbolo encontrado na URL!");
    }
});

function fetchCandlestickData(symbol, period, interval) {
    fetch(`/get_yahoo_data_history/?symbol=${symbol}&period=${period}&interval=${interval}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                processCandlestickData(data);
            }
        })
        .catch(error => {
            document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function processCandlestickData(data) {
    if (!data.data || data.data.length === 0) {
        console.error("🚨 Nenhum dado encontrado no JSON:", data);
        document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Nenhum dado disponível</h3>`;
        return;
    }

    console.log("📊 Processando dados para o gráfico:", data.data);

    // 🔥 Limita os dados para evitar sobrecarga no Plotly
    let maxDataPoints = 500;  // Ajuste conforme necessário
    let trimmedData = data.data.slice(-maxDataPoints);  // Pega os últimos 500 registros

    let dates = trimmedData.map(entry => {
        if (entry.Date) {
            let dateObj = new Date(entry.Date);
            let formattedDate = dateObj.toISOString().split("T")[0]; // YYYY-MM-DD
            let formattedTime = dateObj.toISOString().split("T")[1].substring(0, 5); // HH:MM
            return `${formattedDate} ${formattedTime}`;
        }
        return "Desconhecido";
    }); 
    let openPrices = trimmedData.map(entry => parseFloat(entry.Open) || 0);
    let highPrices = trimmedData.map(entry => parseFloat(entry.High) || 0);
    let lowPrices = trimmedData.map(entry => parseFloat(entry.Low) || 0);
    let closePrices = trimmedData.map(entry => parseFloat(entry.Close) || 0);

    console.log("📈 Dados extraídos para o gráfico (limite de 500):", { dates, openPrices, highPrices, lowPrices, closePrices });

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
        title: 'Histórico de Preços Forex',
        xaxis: { type: 'date' },
        yaxis: { title: 'Preço' },
        dragmode: 'pan'
    };

    Plotly.newPlot('candlestickChart', [trace], layout);
}
