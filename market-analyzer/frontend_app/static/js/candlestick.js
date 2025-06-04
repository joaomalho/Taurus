////////// VARIABLES //////////
let chart;
let rsiChart;
let candleSeries;

/// Crossover ///
let emaFastSeries, emaMediumSeries, emaSlowSeries;
let emaFastData = [], emaMediumData = [], emaSlowData = [];
let emasVisible = false;

/// Bollinger ///
let bbUpperSeries, bbMiddleSeries, bbLowerSeries;
let bbUpperData = [], bbMiddleData = [], bbLowerData = [];
let bollingerVisible = false 

/// Rsi ///
let rsiSeries;
let rsiData = [];
let rsiVisible = false;
let rsiUpperLineSeries = null;
let rsiLowerLineSeries = null;
let rsiUpperData = [];
let rsiLowerData = [];

/// Harmonic Patterns //
let harmonicSeries = [];
let harmonicMarkers = [];
let harmonicVisible = false;
let harmonicRendered = false;
let storedHarmonicPatterns = [];


////////// DRAW HARMONIC PATTERNS //////////
export function updateHarmonicPatterns(symbol) {
    fetch(`/stock/${symbol}/harmonic_patterns/`)
        .then(res => res.json())
        .then(data => {
            if (data.error || !data.patterns_detected) {
                console.error("Erro ao buscar padrões harmônicos:", data.error);
                return;
            }

            storedHarmonicPatterns = data.patterns_detected;

            const toggleBtn = document.getElementById("toggleHarmonicBtn");
            const legendDiv = document.getElementById("customLegendHarmonic");

            if (toggleBtn) {
                toggleBtn.classList.add("visible");
            }
            if (legendDiv) legendDiv.textContent = "Harmonic Patterns";
        })
        .catch(err => console.error("Erro ao buscar padrões harmônicos:", err));
}

function setupToggleHarmonicButton() {
    const toggleBtn = document.getElementById("toggleHarmonicBtn");
    const icon = document.getElementById("toggleHarmonicIcon");

    if (!toggleBtn || !icon) return;

    toggleBtn.addEventListener("click", () => {
        harmonicVisible = !harmonicVisible;

        if (!harmonicRendered && harmonicVisible) {
            renderHarmonicPatterns(storedHarmonicPatterns);
            harmonicRendered = true;
        } else {
            for (let line of harmonicSeries) {
                line.applyOptions({ visible: harmonicVisible });
            }

            if (harmonicVisible) {
                candleSeries.setMarkers(harmonicMarkers);
            } else {
                candleSeries.setMarkers([]);
            }
        }

        icon.src = harmonicVisible
            ? "/static/images/open-eye-white.png"
            : "/static/images/close-eye-white.png";
    });
}

function renderHarmonicPatterns(patterns) {
    clearHarmonicPatterns();

    const markers = [];

    for (let pattern of patterns) {
        const points = pattern.pattern_idx_prices.map((price, i) => ({
            time: Math.floor(new Date(pattern.pattern_idx_dates[i]).getTime() / 1000),
            value: price
        }));

        const colorLine = pattern.direction === 1 ? '#26a699' : '#ef5350';
        const colorPoint = '#7a41b5';

        const series = chart.addLineSeries({
            color: colorLine,
            lineWidth: 3,
            priceLineVisible: false,
            crossHairMarkerVisible: true,
            crossHairMarkerRadius: 3,
            lastValueVisible: false,
            visible: harmonicVisible,
            priceScaleId: 'right',
        });

        series.setData(points);
        harmonicSeries.push(series);

        // Targets & Stoploss
        const dTime = points[4]?.time;
        const extensionDays = 40 * 86400

        const levels = [
            { value: pattern.STOP, color: '#dedede', label: 'STOP' },
            { value: pattern.TP1, color: '#ffd000', label: 'TP1' },
            { value: pattern.TP2, color: '#ffd000', label: 'TP2' },
            { value: pattern.TP3, color: '#ffd000', label: 'TP3' },
        ];

        levels.forEach(({ value, color, label }) => {
            if (value) {
                const line = chart.addLineSeries({
                    color: color,
                    lineWidth: 1,
                    lineStyle: 1,
                    priceLineVisible: false,
                    lastValueVisible: false,
                    crossHairMarkerVisible: false,
                    priceScaleId: 'right',
                    visible: harmonicVisible,
                    text: levels[label] || '',
                    
                });

                line.setData([
                    { time: dTime, value: value },
                    { time: dTime + extensionDays, value: value }
                ]);

                harmonicSeries.push(line);
            }
        });

        // Markers //
        const markerPosition = pattern.direction === 1 ? ['belowBar', 'aboveBar'] : ['aboveBar', 'belowBar'];
        const shapeOptions = pattern.direction === 1 ? ['arrowUp', 'arrowDown'] : ['arrowDown', 'arrowUp'];
        const labels = ['X', 'A', 'B', 'C', 'D'];

        points.forEach((pt, idx) => {
            markers.push({
                time: pt.time,
                position: idx % 2 === 0 ? markerPosition[0] : markerPosition[1],
                color: colorPoint,
                shape: shapeOptions[idx % 2],
                text: labels[idx] || '',
                value: pt.value,
            });
        });
    }

    harmonicMarkers = markers;
    if (harmonicVisible) {
        candleSeries.setMarkers(harmonicMarkers);
    }
}

function clearHarmonicPatterns() {
    for (let line of harmonicSeries) {
        chart.removeSeries(line);
    }
    harmonicSeries = [];

    harmonicMarkers = [];
    candleSeries.setMarkers([]);
}


////////// DRAW RSI //////////
export function updateRsi(symbol, length, upper_level, lower_level) {
    fetch(`/stock/${symbol}/rsi_draw/?length=${length}&upper=${upper_level}&lower=${lower_level}`)
        .then(res => res.json())
        .then(rsiData => {
            if (rsiData.error) {
                console.error("Erro ao buscar RSI:", rsiData.error);
                return;
            }

            clearRsiSeries();

            renderRsi(
                rsiData.rsi,
                rsiData.upper_level,
                rsiData.lower_level
            );
            
            updateRsiInitialLegend();

            const toggleBtn = document.getElementById("toggleRsiBtn");
            if (toggleBtn) {
                // toggleBtn.style.display = "inline-block";
                toggleBtn.classList.add("visible");
            }
        })
        .catch(err => console.error("Erro ao buscar RSI:", err));
}

function setupToggleRsiButton() {
    const toggleBtn = document.getElementById("toggleRsiBtn");
    const icon = document.getElementById("toggleRsiIcon");
    const legendDiv = document.getElementById("customLegendRsi");

    if (!toggleBtn || !icon || !legendDiv) return;

    toggleBtn.addEventListener("click", () => {
        rsiVisible = !rsiVisible;

        if (rsiSeries) rsiSeries.applyOptions({ visible: rsiVisible });
        if (rsiUpperLineSeries) rsiUpperLineSeries.applyOptions({ visible: rsiVisible });
        if (rsiLowerLineSeries) rsiLowerLineSeries.applyOptions({ visible: rsiVisible });

        icon.src = rsiVisible
            ? "/static/images/open-eye-white.png"
            : "/static/images/close-eye-white.png";

        if (!rsiVisible) {
            legendDiv.innerHTML = `<span style="color:#ffb300">Rsi: -</span>`;
        } else {
            updateRsiInitialLegend();
        }

    });
}

function renderRsi(data, upperLevel, lowerLevel) {

    rsiSeries = rsiChart.addLineSeries({
        color: '#ffb300',
        pane: 1,
        lineWidth: 1,
        lineStyle: 0,
        lineType: 0,
        crossHairMarkerVisible: true,
        crossHairMarkerRadius: 3,
        lastValueVisible: false,
        priceLineVisible: false,
        priceLineColor: '#ffb300',
        priceLineStyle: 0,
        priceLineWidth: 1,
        // title: label,
        visible: rsiVisible,
        overlay: false,
        // priceScaleId: 'rsi-scale',
    });

    rsiSeries.setData(data);
    rsiData = data;

    // Cria linhas horizontais como as EMAs
    const fromTime = data[0].time;
    const toTime = data[data.length - 1].time;

    const upperPoints = [
        { time: fromTime, value: upperLevel },
        { time: toTime, value: upperLevel }
    ];
    const lowerPoints = [
        { time: fromTime, value: lowerLevel },
        { time: toTime, value: lowerLevel }
    ];

    rsiUpperLineSeries = rsiChart.addLineSeries({
        color: '#e53935',
        lineWidth: 1,
        lineStyle: 1, // dashed
        visible: rsiVisible,
        crossHairMarkerVisible: false,
        priceLineVisible: false,
        overlay: false,
    });
    rsiUpperLineSeries.setData(upperPoints);
    rsiUpperData = upperPoints;

    rsiLowerLineSeries = rsiChart.addLineSeries({
        color: '#43a047',
        lineWidth: 1,
        lineStyle: 1,
        visible: rsiVisible,
        crossHairMarkerVisible: false,
        priceLineVisible: false,
        overlay: false,
    });
    rsiLowerLineSeries.setData(lowerPoints);
    rsiLowerData = lowerPoints;

    rsiChart.timeScale().fitContent();
    updateRsiInitialLegend();
}

function clearRsiSeries() {
    if (rsiSeries) {
        rsiChart.removeSeries(rsiSeries);
        rsiSeries = null;
    }
    if (rsiUpperLineSeries) {
        rsiChart.removeSeries(rsiUpperLineSeries);
        rsiUpperLineSeries = null;
        rsiUpperData = [];
    }
    if (rsiLowerLineSeries) {
        rsiChart.removeSeries(rsiLowerLineSeries);
        rsiLowerLineSeries = null;
        rsiLowerData = [];
    }
}

function setupRsiDynamicLegend() {
    const legendDiv = document.getElementById("customLegendRsi");

    rsiChart.subscribeCrosshairMove(param => {
        if (!param.time || !param.seriesPrices || !rsiVisible) return;

        const value = param.seriesPrices.get(rsiSeries);
        if (value !== undefined) {
            legendDiv.innerHTML = `<span style="color:#ffb300">Rsi: ${value.toFixed(2)}</span>`;
        }
    });
}

function updateRsiInitialLegend() {
    const legendDiv = document.getElementById("customLegendRsi");

    if (!rsiVisible || rsiData.length === 0) {
        legendDiv.innerHTML = `<span style="color:#ffb300">Rsi: -</span>`;
        return;
    }

    const last = rsiData[rsiData.length - 1];
    legendDiv.innerHTML = `<span style="color:#ffb300">Rsi: ${last.value.toFixed(2)}</span>`;
}


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
                // toggleBtn.style.display = "inline-block";
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
    const createLine = (data, color) => {
        const series = chart.addLineSeries({
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
            visible: bollingerVisible,
            overlay: false,
            priceScaleId: 'right',

        });

        series.applyOptions({
            autoscaleInfoProvider: () => null
        });

        series.setData(data.map(point => ({
            time: point.time,
            value: point.value,
        })));

        return series;
    };

    bbUpperSeries = createLine(upperData, '#e5393580');
    bbMiddleSeries = createLine(middleData, '#1e88e580');
    bbLowerSeries = createLine(lowerData, '#43a04780');

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
        if (!param.time || !param.seriesPrices || !bollingerVisible) return;

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

    if (!bollingerVisible || bbUpperData.length === 0) {
        legendDiv.innerHTML = `
            <span style="color:#e53935">Upper: -</span> |
            <span style="color:#1e88e5">Middle: -</span> |
            <span style="color:#43a047">Lower: -</span>
        `;
        return;
    }

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
                // toggleBtn.style.display = "inline-block";
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
        visible: emasVisible,
        overlay: false,
        priceScaleId: 'right' 
    });

    lineSeries.applyOptions({
        autoscaleInfoProvider: () => null
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
        if (!param.time || !param.seriesPrices || !emasVisible) return;

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
    
    if (!emasVisible || emaFastData.length === 0) {
        legendDiv.innerHTML = `
            <span style="color:#b05708">EMA Fast: -</span> |
            <span style="color:#b07508">EMA Medium: -</span> |
            <span style="color:#b09908">EMA Slow: -</span>
        `;
        return;
    }

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
function renderCandlestickChart(priceData, symbol) {

    const sharedScaleId = 'right';
    const chartContainer = document.getElementById("candlestickChart");
    const rsiContainer = document.getElementById("rsiChart");
    
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

    /// RSI Chart ///
    if (!rsiChart) {
        rsiChart = LightweightCharts.createChart(rsiContainer, {
            layout: {
                backgroundColor: 'transparent',
                textColor: '#9198a1',
            },
            grid: {
                vertLines: { color: false, visible: false },
                horzLines: { color: false, visible: false },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
            },
            timeScale: {
                borderColor: '#3d444d',
                timeVisible: true,
                secondsVisible: false,
            },
        });

        window.addEventListener('resize', () => {
            rsiChart.applyOptions({
                width: rsiContainer.clientWidth,
                height: rsiContainer.clientHeight 
            });
        });
    }

    /// Candles Data ///
    candleSeries.setData(priceData);

    /// Markers ///
    addTooltip(chartContainer, chart, priceData);
    
    /// Indicators ///
    /// EMAS Crossover ///
    updateEMALines(symbol, 14, 25, 200);
    setupEMADynamicLegend();
    setupToggleEMAButton();
    
    /// Bollinger Bands ///
    updateBollingerBands(symbol, 14, 2);
    setupBollingerDynamicLegend();
    setupToggleBollingerButton();
    
    /// Rsi ///
    updateRsi(symbol, 14, 70, 30);
    setupRsiDynamicLegend();
    setupToggleRsiButton();

    /// Harmonic patterns ///
    updateHarmonicPatterns(symbol);
    setupToggleHarmonicButton();
    
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

export function renderCandlestickFromData(symbol, priceDataRaw) {
    if (!priceDataRaw || priceDataRaw.length === 0) {
        console.error("Nenhum dado disponível para o gráfico.");
        const el = document.getElementById("candlestickChart");
        if (el) el.innerHTML = `<h3 class="chart-label" style="color: red;">Nenhum dado disponível</h3>`;
        return;
    }

    const parsedData = priceDataRaw.map(entry => ({
        time: entry.Date,
        open: parseFloat(entry.Open).toFixed(5),
        high: parseFloat(entry.High).toFixed(5),
        low: parseFloat(entry.Low).toFixed(5),
        close: parseFloat(entry.Close).toFixed(5)
    }));

    renderCandlestickChart(parsedData, symbol);
}
