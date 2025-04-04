////////// VARIABLES //////////
let chart;
let candleSeries;

/// crossover ///
let emaFastSeries, emaMediumSeries, emaSlowSeries;
let emaFastData = [], emaMediumData = [], emaSlowData = [];
let emasVisible = true;

/// bollinger ///
let bbUpperSeries, bbMiddleSeries, bbLowerSeries;
let bbUpperData = [], bbMiddleData = [], bbLowerData = [];
let bollingerVisible = true, bbAreaSeries = null;

////////// DRAW BOLLINGER BANDS //////////
export function updateBollingerBands(symbol, length, std) {
    fetch(`/stock/${symbol}/bollinger_draw/?length=${length}&std=${std}`)
        .then(res => res.json())
        .then(bollingerData => {
            if (bollingerData.error) {
                console.error("Erro ao buscar Bollinger Bands:", bollingerData.error);
                return;
            }

            clearBollingerSeries();

            renderBollingerBands(
                bollingerData.bb_upper,
                bollingerData.bb_middle,
                bollingerData.bb_lower
            );

            updateBollingerInitialLegend();

            const toggleBtn = document.getElementById("toggleBollingerBtn");
            if (toggleBtn) {
                toggleBtn.style.display = "inline-block";
                toggleBtn.classList.add("visible");
            }
        })
        .catch(err => console.error("Erro ao buscar Bollinger Bands:", err));
}


function setupToggleBollingerButton() {
    const toggleBtn = document.getElementById("toggleBollingerBtn");
    const icon = document.getElementById("toggleBollingerIcon");
    const legendDiv = document.getElementById("customLegendBollinger");

    if (!toggleBtn || !icon || !legendDiv) return;

    toggleBtn.addEventListener("click", () => {
        bollingerVisible = !bollingerVisible;

        if (bbUpperSeries) bbUpperSeries.applyOptions({ visible: bollingerVisible });
        if (bbMiddleSeries) bbMiddleSeries.applyOptions({ visible: bollingerVisible });
        if (bbLowerSeries) bbLowerSeries.applyOptions({ visible: bollingerVisible });
        if (bbAreaSeries) bbAreaSeries.applyOptions({ visible: bollingerVisible });


        icon.src = bollingerVisible
            ? "/static/images/open-eye-white.png"
            : "/static/images/close-eye-white.png";

        if (!bollingerVisible) {
            legendDiv.innerHTML = `
                <span style="color:#e53935">Upper: -</span> |
                <span style="color:#1e88e5">Middle: -</span> |
                <span style="color:#43a047">Lower: -</span>
            `;
        } else {
            updateBollingerInitialLegend();
        }
    });
}

function renderBollingerBands(upperData, middleData, lowerData) {
    // Remove área anterior, se existir
    if (bbAreaSeries) {
        chart.removeSeries(bbAreaSeries);
        bbAreaSeries = null;
    }

    // // Renderiza a área entre Upper e Lower
    // bbAreaSeries = chart.addAreaSeries({
    //     topColor: 'rgba(33, 150, 243, 0.3)',
    //     bottomColor: 'rgba(33, 150, 243, 0.05)',
    //     lineColor: 'transparent',
    //     lineWidth: 0,
    //     priceScaleId: 'right',
    // });

    // const areaData = lowerData.map((point, i) => ({
    //     time: point.time,
    //     value: upperData[i].value,
    // }));

    // bbAreaSeries.setData(areaData);

    // Função interna para criar uma linha
    const createLine = (data, color) => {
        const series = chart.addLineSeries({
            color: color,
            lineWidth: 1,
            visible: true,
            priceLineVisible: false,
            priceScaleId: 'right',

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

        });

        series.setData(data.map(point => ({
            time: point.time,
            value: point.value,
        })));

        return series;
    };

    // Criar as 3 linhas
    bbUpperSeries = createLine(upperData, '#4caf50');
    bbMiddleSeries = createLine(middleData, '#ffa000');
    bbLowerSeries = createLine(lowerData, '#f44336');

    // Guardar os dados
    bbUpperData = upperData;
    bbMiddleData = middleData;
    bbLowerData = lowerData;
}

function clearBollingerSeries() {
    if (bbUpperSeries) {
        chart.removeSeries(bbUpperSeries);
        bbUpperSeries = null;
    }
    if (bbMiddleSeries) {
        chart.removeSeries(bbMiddleSeries);
        bbMiddleSeries = null;
    }
    if (bbLowerSeries) {
        chart.removeSeries(bbLowerSeries);
        bbLowerSeries = null;
    }
}

function setupBollingerDynamicLegend() {
    const legendDiv = document.getElementById("customLegendBollinger");

    chart.subscribeCrosshairMove(param => {
        if (!param.time || !param.seriesPrices) return;

        const lines = [];

        const val = (series, color, label) => {
            const value = param.seriesPrices.get(series);
            if (value !== undefined) {
                lines.push(`<span style="color:${color}">${label}: ${value.toFixed(2)}</span>`);
            }
        };

        val(bbUpperSeries, "#e53935", "Upper");
        val(bbMiddleSeries, "#1e88e5", "Middle");
        val(bbLowerSeries, "#43a047", "Lower");

        if (lines.length > 0) {
            legendDiv.innerHTML = lines.join(" | ");
        }
    });
}

function updateBollingerInitialLegend() {
    const legendDiv = document.getElementById("customLegendBollinger");
    const lines = [];

    if (bbUpperData.length > 0) {
        const last = bbUpperData[bbUpperData.length - 1];
        lines.push(`<span style="color:#e53935">Upper: ${last.value.toFixed(2)}</span>`);
    }

    if (bbMiddleData.length > 0) {
        const last = bbMiddleData[bbMiddleData.length - 1];
        lines.push(`<span style="color:#1e88e5">Middle: ${last.value.toFixed(2)}</span>`);
    }

    if (bbLowerData.length > 0) {
        const last = bbLowerData[bbLowerData.length - 1];
        lines.push(`<span style="color:#43a047">Lower: ${last.value.toFixed(2)}</span>`);
    }

    legendDiv.innerHTML = lines.join(" | ");
}


////////// DRAW CROSSOVER EMAS //////////
export function updateEMALines(symbol, fast, medium, slow) {
    fetch(`/stock/${symbol}/crossover_draw/?fast=${fast}&medium=${medium}&slow=${slow}`)
        .then(res => res.json())
        .then(emaData => {
            if (emaData.error) {
                console.error("Erro ao buscar EMAs:", emaData.error);
                return;
            }

            clearEMASeries();

            renderEMALines(emaData.ema_fast, "#b0570880", "EMA Fast");
            renderEMALines(emaData.ema_medium, "#b0750880", "EMA Medium");
            renderEMALines(emaData.ema_slow, "#b0990880", "EMA Slow");
            updateEMAInitialLegend();
            const toggleBtn = document.getElementById("toggleEmaBtn");
            if (toggleBtn) {
                toggleBtn.style.display = "inline-block";
                toggleBtn.classList.add("visible");
            }
        })
        .catch(err => console.error("Erro ao buscar EMAs:", err));
}

function setupToggleEMAButton() {
    const toggleBtn = document.getElementById("toggleEmaBtn");
    const icon = document.getElementById("toggleEmaIcon");
    const legendDiv = document.getElementById("customLegendEmas");

    if (!toggleBtn || !icon || !legendDiv) return;

    toggleBtn.addEventListener("click", () => {
        emasVisible = !emasVisible;

        if (emaFastSeries) emaFastSeries.applyOptions({ visible: emasVisible });
        if (emaMediumSeries) emaMediumSeries.applyOptions({ visible: emasVisible });
        if (emaSlowSeries) emaSlowSeries.applyOptions({ visible: emasVisible });

        icon.src = emasVisible
            ? "/static/images/open-eye-white.png"
            : "/static/images/close-eye-white.png";

        if (!emasVisible) {
            // Quando as EMAs estão escondidas, mostrar apenas "-"
            legendDiv.innerHTML = `
                <span style="color:#b05708">EMA Fast: -</span> |
                <span style="color:#b07508">EMA Medium: -</span> |
                <span style="color:#b09908">EMA Slow: -</span>
            `;
        } else {
            // Quando voltam a estar visíveis, atualiza os valores
            updateEMAInitialLegend();
        }
    });
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

function clearEMASeries() {
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

function setupEMADynamicLegend() {
    const legendDiv = document.getElementById("customLegendEmas");

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

function updateEMAInitialLegend() {
    const legendDiv = document.getElementById("customLegendEmas");
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
    
        /// Candlestick Chart ///
        if (!chart) {
            chart = LightweightCharts.createChart(chartContainer, {
                layout: {
                    backgroundColor: 'transparent',
                    textColor: '#9198a1',
                },
                grid: {
                    vertLines: { color: false, visible: false },
                    horzLines: { color: false, visible: false },
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
    
        /// Candles Patterns - WIP - Fazer similar a EMAs///
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
        
        /// EMAS Crossover ///
        updateEMALines(symbol, 14, 25, 200);
        setupEMADynamicLegend();
        setupToggleEMAButton();
        
        /// Bollinger Bands ///
        updateBollingerBands(symbol, 14, 2);
        setupBollingerDynamicLegend();
        setupToggleBollingerButton();

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
