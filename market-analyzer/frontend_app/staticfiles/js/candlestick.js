let chart;         // Gráfico criado apenas uma vez
let candleSeries;  // Série de candles global
let emaFastSeries, emaMediumSeries, emaSlowSeries;

export function updateEMALines(symbol, fast, medium, slow) {
    fetch(`/stock/${symbol}/crossover_draw/?fast=${fast}&medium=${medium}&slow=${slow}`)
        .then(res => res.json())
        .then(emaData => {
            if (emaData.error) {
                console.error("Erro ao buscar EMAs:", emaData.error);
                return;
            }

            clearEmaSeries();

            renderEMALines(emaData.ema_fast, "#b0570875", "EMA Fast");
            renderEMALines(emaData.ema_medium, "#b0750875", "EMA Medium");
            renderEMALines(emaData.ema_slow, "#b0990875", "EMA Slow");
        })
        .catch(err => console.error("Erro ao buscar EMAs:", err));
}

function renderEMALines(emaData, color, label) {
    const lineSeries = chart.addLineSeries({
        color: color,                 // Cor da linha principal
        lineWidth: 1,                // Espessura da linha
        lineStyle: 0,                // Estilo: 0=linha sólida, 1=tracejada, 2=pontilhada
        lineType: 0,                 // Tipo: 0=simples, 1=com áreas de gaps
        crossHairMarkerVisible: true,  // Mostra o ponto de intersecção no crosshair
        crossHairMarkerRadius: 3,      // Tamanho do marcador do crosshair
        lastValueVisible: true,        // Mostra o último valor da linha
        priceLineVisible: false,        // Linha horizontal com o último valor
        priceLineColor: color,         // Cor da linha de preço
        priceLineStyle: 0,             // Estilo da linha de preço (0 = sólida)
        priceLineWidth: 1,             // Espessura da linha de preço
        title: label,                  // Título da série (pode aparecer em legendas)
        visible: true,                 // Se a série está visível ou não
        overlay: true,                 // Se sobrepõe o gráfico principal
    });

    lineSeries.setData(
        emaData.map(point => ({
            time: point.time,
            value: point.value
        }))
    );

    if (label.includes("Fast")) emaFastSeries = lineSeries;
    if (label.includes("Medium")) emaMediumSeries = lineSeries;
    if (label.includes("Slow")) emaSlowSeries = lineSeries;
}

function clearEmaSeries() {
    if (emaFastSeries) {
        chart.removeSeries(emaFastSeries);
        emaFastSeries = null;
    }
    if (emaMediumSeries) {
        chart.removeSeries(emaMediumSeries);
        emaMediumSeries = null;
    }
    if (emaSlowSeries) {
        chart.removeSeries(emaSlowSeries);
        emaSlowSeries = null;
    }
}


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
        
        updateEMALines(symbol, 14, 25, 200);

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
                const y = chart.priceScale().priceToCoordinate(priceDataPoint.close);
            const cursorY = param.point.y;

            const highY = chart.priceScale().priceToCoordinate(priceDataPoint.high);
            const lowY = chart.priceScale().priceToCoordinate(priceDataPoint.low);

            // Só mostra a tooltip se o cursor estiver dentro do range da vela
            if (cursorY >= highY && cursorY <= lowY) {
                const { open, high, low, close } = priceDataPoint;

                tooltip.innerHTML = `
                    <strong>Abertura:</strong> ${open}<br>
                    <strong>Fechamento:</strong> ${close}<br>
                    <strong>Máxima:</strong> ${high}<br>
                    <strong>Mínima:</strong> ${low}
                `;

                tooltip.style.visibility = "visible";
                tooltip.style.left = `${param.point.x + 10}px`;
                tooltip.style.top = `${cursorY - 50}px`;
            } else {
                tooltip.style.visibility = "hidden";
            }
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
