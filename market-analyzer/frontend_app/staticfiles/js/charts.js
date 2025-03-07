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

