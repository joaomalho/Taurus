////////////////////////////////////
//STOCK CHARTs                    //
//////////////////////////////////// 

// Bar Chart Institutional Holders with Tooltip
document.addEventListener("DOMContentLoaded", function () {
    function fetchAndRenderChart(symbol) {
        fetch(`/stock/${symbol}/institutional_holders/`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    return;
                }

                let chartData = data.data.map(d => ({
                    holder: d.Holder,
                    pctHeld: d.pctHeld,
                    shares: d.Shares.toLocaleString(),
                    value: `$ ${d.Value.toLocaleString()}`,
                    pctChange: d.pctChange.toFixed(2) + "%"
                })).sort((a, b) => b.pctHeld - a.pctHeld); // Ordena do maior para o menor

                renderBarChart(chartData);
            })
            .catch(error => console.error("Erro ao carregar dados:", error));
    }

    function renderBarChart(chartData) {
        let ctx = document.getElementById("hBarChart");

        if (!ctx) {
            console.error("Elemento canvas não encontrado!");
            return;
        }

        if (window.myBarChart) {
            window.myBarChart.destroy();
        }

        window.myBarChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: chartData.map(d => d.holder),
                datasets: [{
                    label: "Percentage Held",
                    data: chartData.map(d => d.pctHeld),
                    backgroundColor: "rgba(54, 162, 235, 0.7)",
                    borderColor: "rgba(0,0,0,0)",
                    borderWidth: 1,
                    barThickness: 15,
                    maxBarThickness: 20,
                    categoryPercentage: 0.5,
                    barPercentage: 0.9,
                    borderRadius: 10
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                let d = chartData[tooltipItem.dataIndex];
                                return [
                                    `Percentage Held: ${d.pctHeld.toFixed(2)}%`,
                                    `Total Shares: ${d.shares}`,
                                    `Shares Value: ${d.value}`,
                                    `Percentage Change: ${d.pctChange}`
                                ];
                            }
                        }
                    },
                    datalabels: {
                        anchor: "end",
                        align: "right",
                        color: "white",
                        font: { weight: "bold", size: 12 },
                        formatter: function(value) {
                            return `${value.toFixed(2)}%`;
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: "Percentage Held (%)", color: "white" },
                        ticks: {
                            color: "#bbbbbb",
                            callback: value => `${value.toFixed(2)}%`
                        }
                    },
                    y: {
                        title: { display: true, text: "Institutional Holders", color: "white" },
                        ticks: { color: "#bbbbbb" }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    }

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        console.log("Carregando gráfico de Holders para:", symbol);
        fetchAndRenderChart(symbol);
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }

    const searchButton = document.getElementById("searchButton");
    if (searchButton) {
        searchButton.addEventListener("click", function () {
            const symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();
            if (symbol) {
                fetchAndRenderChart(symbol);
            } else {
                alert("Por favor, insira um símbolo de ação válido.");
            }
        });
    }
});

// Gauge Chart Fundamental

function renderGaugeChart(canvasId, metric, value) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) {
        console.error(`Elemento com ID '${canvasId}' não encontrado.`);
        return;
    }

    const { classification, color, intervals } = classifyMetricForGauge(metric, value);

    const maxIntervalValue = intervals[intervals.length - 1];
    const pointerValue = Math.min(value, maxIntervalValue);

    const gaugeNeedle = {
        id: 'gaugeNeedle',
        afterDatasetsDraw(chart) {
            const { ctx, chartArea } = chart;
            const { top, bottom, left, right } = chartArea;
            const centerX = (left + right) / 2;
            const centerY = bottom - 20;

            const radius = (bottom - top) / 2; // Tamanho adequado da agulha

            // Cálculo correto do ângulo da agulha (mapeado na escala 0-180 graus)
            const angle = (Math.PI / 180) * (270 + (pointerValue / maxIntervalValue) * 180);

            ctx.save();

            // Desenho da agulha
            ctx.translate(centerX, centerY);
            ctx.rotate(angle);

            ctx.beginPath();
            ctx.moveTo(0, -radius * 1.5); // Ponta da agulha
            ctx.lineTo(-15, 0); // Base esquerda
            ctx.lineTo(15, 0); // Base direita
            ctx.closePath();
            ctx.fillStyle = 'grey';
            ctx.fill();

            ctx.lineWidth = 2;       // Espessura da borda
            ctx.strokeStyle = 'black';
            ctx.stroke();

            // Círculo central da agulha
            ctx.beginPath();
            ctx.arc(0, 0, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'grey';
            ctx.fill();

            ctx.restore();
        }
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: intervals.map(i => i.toFixed(2)),
            datasets: [
                {
                    data: [
                        intervals[0],
                        intervals[1] - intervals[0],
                        intervals[2] - intervals[1],
                        intervals[3] - intervals[2],
                        maxIntervalValue  - intervals[3]
                    ],
                    backgroundColor: ['#ed0000', '#f24536', '#f2b636', '#089981', '#068008'],
                    borderWidth: 2,
                    borderColor: 'black' 
                },
                {
                    // Ponteiro para o valor atual
                    data: [pointerValue, maxIntervalValue - pointerValue],
                    backgroundColor: ['#000000', '#9A8655'],
                    borderWidth: 0,
                    circumference: 180,
                    rotation: 270,
                    cutout: '100%',
                    angleValue: maxIntervalValue
                }
            ]
        },
        options: {
            responsive : true,
            maintainAspectRatio: false,
            circumference: 180,
            rotation: 270,
            aspectRatio: 1.5,
            cutout: '15%',
            plugins: {
                legend: { display: true },
                tooltip: { enabled: true }
            }
        },
        plugins: [gaugeNeedle]
    });

    const labelElement = document.getElementById(`${canvasId}Class`);
    if (labelElement) {
        labelElement.textContent = classification;
        labelElement.style.color = color;
    }
}