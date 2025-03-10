let chart;         // Gráfico criado apenas uma vez
let candleSeries;  // Série de candles global

document.addEventListener("DOMContentLoaded", function () {
    function fetchAndRenderCandlestickChart(symbol, period, interval) {
        fetch(`/stock/${symbol}/data_history/?period=${period}&interval=${interval}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    const el = document.getElementById("candlestickChart");
                    if (el) el.innerHTML = `<h3 class="chart-label" style="color: red;">Erro: ${data.error}</h3>`;
                    return;
                }
                processCandlestickData(data);
            })
            .catch(error => {
                console.error("Erro ao buscar os dados:", error);
                const el = document.getElementById("candlestickChart");
                if (el) el.innerHTML = `<h3 class="chart-label" style="color: red;">Erro ao buscar os dados.</h3>`;
            });
    }

    function processCandlestickData(data) {
        if (!data.data || data.data.length === 0) {
            console.error("Nenhum dado encontrado no JSON:", data);
            const el = document.getElementById("candlestickChart");
            if (el) el.innerHTML = `<h3 class="chart-label" style="color: red;">Nenhum dado disponível</h3>`;
            return;
        }

        const parsedData = data.data.map(entry => ({
            time: entry.Date,
            open: parseFloat(entry.Open).toFixed(5),
            high: parseFloat(entry.High).toFixed(5),
            low: parseFloat(entry.Low).toFixed(5),
            close: parseFloat(entry.Close).toFixed(5)
        }));

        renderCandlestickChart(parsedData);
    }

    function renderCandlestickChart(priceData) {
        const chartContainer = document.getElementById("candlestickChart");

        if (!chart) {
            chart = LightweightCharts.createChart(chartContainer, {
                layout: {
                    backgroundColor: 'transparent',
                    textColor: '#9198a1',
                },
                grid: {
                    vertLines: { color: 'false' },
                    horzLines: { color: 'false' },
                },
                priceScale: {
                    borderColor: '#3d444d',
                },
                crosshair: {
                    mode: LightweightCharts.CrosshairMode.Normal
                },
                timeScale: {
                    borderColor: '#3d444d',
                    timeVisible: true,
                    secondsVisible: false,
                },
            });

            candleSeries = chart.addCandlestickSeries({
                upColor: '#26a69a',
                downColor: '#ef5350',
                borderDownColor: '#ef5350',
                borderUpColor: '#26a69a',
                wickDownColor: '#ef5350',
                wickUpColor: '#26a69a',
            });

            chart.subscribeClick((param) => {
                if (param.time) {
                    const candle = priceData.find(c => c.time === param.time);
                    if (candle) {
                        alert(`Vela Selecionada:\nAbertura: ${candle.open}\nFechamento: ${candle.close}\nAlta: ${candle.high}\nBaixa: ${candle.low}`);
                    }
                }
            });

            window.addEventListener('resize', () => {
                chart.applyOptions({
                    width: chartContainer.clientWidth,
                    height: chartContainer.clientHeight 
                });
            });
        }

        if (!candleSeries) {
            candleSeries.setData(priceData);
        } else {
            priceData.forEach(dataPoint => {
                candleSeries.update(dataPoint);
            });
        }







        const highlightCandle = priceData[2];  // Exemplo: destaca a 3ª vela
        const markers = [
            {
                time: highlightCandle.time,
                position: 'aboveBar',
                color: 'yellow',
                shape: 'arrowDown',
                text: 'Destaque'
            }
        ];

        candleSeries.setMarkers(markers);
    }

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        fetchAndRenderCandlestickChart(symbol, "1mo", "1d");
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }


});
