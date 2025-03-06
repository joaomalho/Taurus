document.addEventListener("DOMContentLoaded", function () {
    function fetchAndRenderLineChart(symbol, period, interval) {
        fetch(`/stock/${symbol}/data_history/?period=${period}&interval=${interval}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    let el = document.getElementById("lineChart");
                    if (el) el.innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
                    return;
                }
                processLineChartData(data);
            })
            .catch(error => {
                console.error("Erro ao buscar os dados:", error);
                let el = document.getElementById("lineChart");
                if (el) el.innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
            });
    }

    function processLineChartData(data) {
        if (!data.data || data.data.length === 0) {
            console.error("Nenhum dado encontrado no JSON:", data);
            let el = document.getElementById("lineChart");
            if (el) el.innerHTML = `<h3 style="color: red;">Nenhum dado disponível</h3>`;
            return;
        }

        let parsedData = data.data.map(entry => ({
            t: new Date(entry.Date),
            c: parseFloat(entry.Close),
            o: parseFloat(entry.Open)
        }));

        renderLineChart(parsedData);
    }

    function renderLineChart(priceData) {
        const recentData = priceData.slice(-100); // Últimos 100 pontos

        let ctx = document.getElementById("lineChart");
        if (!ctx) {
            console.error("Elemento canvas não encontrado!");
            return;
        }

        if (window.myLineChart) {
            window.myLineChart.destroy();
        }

        // 🔹 Determinar a cor com base no Open inicial e Close final
        const firstOpen = recentData[0].o;
        const lastClose = recentData[recentData.length - 1].c;
        const lineColor = firstOpen > lastClose ? "#f23645" : "#089981"; // Vermelho se caiu, Verde se subiu

        window.myLineChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: recentData.map(d => d.t.toLocaleDateString("en-EN")),
                datasets: [{
                    label: "Close Price",
                    data: recentData.map(d => d.c),
                    borderColor: lineColor,
                    tension: 0.3,
                    pointRadius: 4, // Tamanho dos pontos visíveis
                    pointHoverRadius: 6,
                    pointStyle: 'circle', // Garante que sejam círculos
                    showLine: true // Mostra a linha conectando os pontos
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true, 
                        labels: { 
                            color: "#ffffff",
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: tooltipItem => `Close: $${tooltipItem.raw.toFixed(5)}`
                        }
                    }
                },
                scales: {
                    x: {
                        type: "category",
                        title: { 
                            display: true, 
                            text: "Date", 
                            color: "white"
                        },
                        ticks: {
                            maxTicksLimit: 10,
                            color: "#bbbbbb",
                            callback: function(value, index, values) {
                                return index % 2 === 0 ? this.getLabelForValue(value) : "";
                            }
                        }
                    },
                    y: {
                        title: { 
                            display: true, 
                            text: "Price", 
                            color: "white"
                        },
                        ticks: {
                            color: "#bbbbbb", 
                            callback: value => `$${value.toFixed(2)}`
                        }
                    }
                }
            }
        });
    }

    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        fetchAndRenderLineChart(symbol, "1mo", "1d");
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }
});
