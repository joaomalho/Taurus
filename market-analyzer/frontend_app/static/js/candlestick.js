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
    
        // Marcar a penúltima vela com um "ícone" usando Unicode
        const highlightCandle = priceData[priceData.length - 2];
        const markers = [
            {
                time: highlightCandle.time,
                position: 'aboveBar',
                // color: 'yellow',
                // shape: 'arrowDown',
                text: '🚩'
            }
        ];
    
        candleSeries.setMarkers(markers);

        addTooltip(chartContainer, chart, priceData);


    }
    
    function drawEMALines(chart, emaFast, emaMedium, emaSlow) {
        // Adiciona série da Fast EMA
        const fastLine = chart.addLineSeries({ color: '#FFD700', lineWidth: 2 });
        fastLine.setData(emaFast);
    
        // Medium EMA
        const mediumLine = chart.addLineSeries({ color: '#00BFFF', lineWidth: 2 });
        mediumLine.setData(emaMedium);
    
        // Slow EMA
        const slowLine = chart.addLineSeries({ color: '#FF4500', lineWidth: 2 });
        slowLine.setData(emaSlow);
    }

    function addTooltip(chartContainer, chart, priceData) {
        const tooltip = document.createElement("div");
        tooltip.style.position = "absolute";
        tooltip.style.background = "#0d1117";
        tooltip.style.color = "#ddd";
        tooltip.fontSize = "12px";
        tooltip.style.padding = "8px 12px";
        tooltip.style.borderRadius = "6px";
        tooltip.style.pointerEvents = "none";
        tooltip.style.visibility = "hidden";
        tooltip.style.opacity = "0.8";
        tooltip.style.zIndex = "999";

        chartContainer.appendChild(tooltip);
    
        chart.subscribeCrosshairMove((param) => {
            if (!param.time || !param.seriesPrices) {
                tooltip.style.visibility = "hidden";
                return;
            }
    
            const priceDataPoint = priceData.find(c => c.time === param.time);
    
            // Exibir apenas se houver uma vela sob o cursor
            if (priceDataPoint) {
                const { time, open, high, low, close } = priceDataPoint;


                tooltip.innerHTML = `
                    <strong>Abertura:</strong> ${open}<br>
                    <strong>Fechamento:</strong> ${close}<br>
                    <strong>Máxima:</strong> ${high}<br>
                    <strong>Mínima:</strong> ${low}
                `;
    
                tooltip.style.visibility = "visible";
                tooltip.style.left = `${param.point.x + 10}px`;
                tooltip.style.top = `${param.point.y - 50}px`;
            } else {
                tooltip.style.visibility = "hidden";
            }
        });
    }
    
    

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        fetchAndRenderCandlestickChart(symbol, "1mo", "1d");
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }


});
