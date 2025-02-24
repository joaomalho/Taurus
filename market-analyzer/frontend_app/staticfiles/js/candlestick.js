function fetchCandlestickData(symbol, period, interval) {
    fetch(`/get_yahoo_data_history/?symbol=${symbol}&period=${period}&interval=${interval}`)
        .then(response => response.json())
        .then(data => {
            console.log("🔍 Dados recebidos da API:", data);  // 🔥 Testa se os dados chegaram

            if (data.error) {
                document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
            } else {
                processCandlestickData(data);
            }
        })
        .catch(error => {
            console.error("🚨 Erro ao buscar dados:", error);
            document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
        });
}

function processCandlestickData(data) {
    // 🔥 Verifica se a estrutura do JSON está correta
    if (!data.data || data.data.length === 0) {
        console.error("🚨 Nenhum dado encontrado no JSON:", data);
        document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Nenhum dado disponível</h3>`;
        return;
    }

    console.log("📊 Processando dados para o gráfico:", data.data);

    // 🔥 Extraindo os dados corretamente
    let dates = data.data.map(entry => entry.Date || entry.date);  // Ajustando caso seja Date ou date
    let openPrices = data.data.map(entry => entry.Open);
    let highPrices = data.data.map(entry => entry.High);
    let lowPrices = data.data.map(entry => entry.Low);
    let closePrices = data.data.map(entry => entry.Close);

    renderCandlestickChart(dates, openPrices, highPrices, lowPrices, closePrices);
}

function renderCandlestickChart(dates, open, high, low, close) {
    console.log("📈 Renderizando gráfico com:", { dates, open, high, low, close });

    let trace = {
        x: dates,  // 🔥 Eixo X com datas
        open: open,
        high: high,
        low: low,
        close: close,
        type: 'candlestick',
        increasing: { line: { color: 'green' } },  // 🔼 Velas de alta verdes
        decreasing: { line: { color: 'red' } }  // 🔽 Velas de baixa vermelhas
    };

    let layout = {
        title: 'Histórico de Preços Forex',
        xaxis: { type: 'date' },
        yaxis: { title: 'Preço' },
        dragmode: 'pan'
    };

    Plotly.newPlot('candlestickChart', [trace], layout);
}
