////////// VARIABLES //////////
let chart;
let candleSeries;  
let emaFastSeries, emaMediumSeries, emaSlowSeries;
let emaFastData = [];
let emaMediumData = [];
let emaSlowData = [];

////////// DRAW CROSSOVER EMAS //////////
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
            updateInitialLegend();
        })
        .catch(err => console.error("Erro ao buscar EMAs:", err));
}

function renderEMALines(emaData, color, label) {
    
    const lineSeries = chart.addLineSeries({
        color: color,
        lineWidth: 1,
        lineStyle: 0,
        lineType: 0,
        crossHairMarkerVisible: true,
        crossHairMarkerRadius: 3,
        lastValueVisible: false,
        priceLineVisible: false,
        priceLineColor: color,
        priceLineStyle: 0,
        priceLineWidth: 1,
        // title: label,
        visible: true,
        overlay: false,
        priceScaleId: 'right' 
    });

    lineSeries.setData(
        emaData.map(point => ({
            time: point.time,
            value: point.value
        }))
    );

    if (label.includes("Fast")) {
        emaFastSeries = lineSeries;
        emaFastData = emaData;
    }
    if (label.includes("Medium")) {
        emaMediumSeries = lineSeries;
        emaMediumData = emaData;
    }
    if (label.includes("Slow")) {
        emaSlowSeries = lineSeries;
        emaSlowData = emaData;
    }
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

function setupDynamicLegend() {
    const legendDiv = document.getElementById("customLegend");

    chart.subscribeCrosshairMove((param) => {
        if (!param.time || !param.seriesPrices) return;

        const lines = [];

        if (emaFastSeries) {
            const value = param.seriesPrices.get(emaFastSeries);
            if (value !== undefined) {
                lines.push(`<span style="color:#b05708">EMA Fast: ${value.toFixed(2)}</span>`);
            }
        }

        if (emaMediumSeries) {
            const value = param.seriesPrices.get(emaMediumSeries);
            if (value !== undefined) {
                lines.push(`<span style="color:#b07508">EMA Medium: ${value.toFixed(2)}</span>`);
            }
        }

        if (emaSlowSeries) {
            const value = param.seriesPrices.get(emaSlowSeries);
            if (value !== undefined) {
                lines.push(`<span style="color:#b09908">EMA Slow: ${value.toFixed(2)}</span>`);
            }
        }

        // Se houver valores, mostra; se não, mantém o último estado
        if (lines.length > 0) {
            legendDiv.innerHTML = lines.join(" | ");
        }
    });
}

function updateInitialLegend() {
    const legendDiv = document.getElementById("customLegend");
    const lines = [];

    if (emaFastData.length > 0) {
        const last = emaFastData[emaFastData.length - 1];
        lines.push(`<span style="color:#b05708">EMA Fast: ${last.value.toFixed(2)}</span>`);
    }

    if (emaMediumData.length > 0) {
        const last = emaMediumData[emaMediumData.length - 1];
        lines.push(`<span style="color:#b07508">EMA Medium: ${last.value.toFixed(2)}</span>`);
    }

    if (emaSlowData.length > 0) {
        const last = emaSlowData[emaSlowData.length - 1];
        lines.push(`<span style="color:#b09908">EMA Slow: ${last.value.toFixed(2)}</span>`);
    }

    legendDiv.innerHTML = lines.join(" | ");
}



////////// MAIN DOCUMENT //////////
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

        const sharedScaleId = 'right';

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
                priceScaleId: sharedScaleId
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

        setupDynamicLegend();

    }
    
    function addTooltip(chartContainer, chart, priceData) {
        const tooltip = document.createElement("div");
        tooltip.style.position = "absolute";
        tooltip.style.background = "#0d1117";
        tooltip.style.color = "#ddd";
        tooltip.style.fontSize = "12px";
        tooltip.style.padding = "8px 12px";
        tooltip.style.borderRadius = "6px";
        tooltip.style.pointerEvents = "none";
        tooltip.style.visibility = "hidden";
        tooltip.style.opacity = "0.8";
        tooltip.style.zIndex = "999";
    
        chartContainer.appendChild(tooltip);
    
        chart.subscribeCrosshairMove((param) => {
            if (!param.time || !param.seriesPrices || !param.point) {
                tooltip.style.visibility = "hidden";
                return;
            }
    
            const priceDataPoint = priceData.find(c => c.time === param.time);
    
            if (priceDataPoint) {
                const cursorY = param.point.y;
                const highY = candleSeries.priceToCoordinate(priceDataPoint.high);
                const lowY = candleSeries.priceToCoordinate(priceDataPoint.low);
    
                // Proteção extra contra valores null
                if (highY == null || lowY == null || cursorY == null) {
                    tooltip.style.visibility = "hidden";
                    return;
                }
    
                if (cursorY >= highY && cursorY <= lowY) {
                    const { open, high, low, close } = priceDataPoint;
    
                    tooltip.innerHTML = `
                        <strong>Open:</strong> ${open}<br>
                        <strong>Close:</strong> ${close}<br>
                        <strong>High:</strong> ${high}<br>
                        <strong>Low:</strong> ${low}
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
