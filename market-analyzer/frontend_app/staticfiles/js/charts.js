
////////////////////////////////////
//STOCK CHARTs                    //
//////////////////////////////////// 

// Bar Chart Institutional Holders with Tooltip

document.addEventListener("DOMContentLoaded", function () {
    const width = 800;
    const barHeight = 25;
    const marginTop = 30;
    const marginRight = 30;
    const marginBottom = 10;
    const marginLeft = 250;
    const height = 500;

    const tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "#333")
        .style("color", "#fff")
        .style("padding", "8px")
        .style("border-radius", "4px")
        .style("font-size", "12px")
        .style("opacity", 0)
        .style("pointer-events", "none");

    function fetchAndRenderChart(symbol) {
        fetch(`/stock/${symbol}/institutional_holders/`)
        .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    return;
                }

                d3.select("#h-bar-chart").selectAll("*").remove();

                const chartData = data.data.map(d => ({
                    holder: d.Holder,
                    pctHeld: d.pctHeld,
                    shares: d.Shares.toLocaleString(),
                    value: `$ ${d.Value.toLocaleString()}`,
                    pctChange: d.pctChange.toFixed(2) + "%"
                })).sort((a, b) => b.pctHeld - a.pctHeld); // Ordena de maior para menor

                const dynamicHeight = Math.ceil((chartData.length + 0.1) * barHeight) + marginTop + marginBottom;
                
                const svg = d3.select("#h-bar-chart")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", dynamicHeight)
                    .attr("viewBox", [0, 0, width, dynamicHeight])
                    .attr("style", "max-width: 100%; height: auto; font: 12px sans-serif;");

                const x = d3.scaleLinear()
                    .domain([0, d3.max(chartData, d => d.pctHeld)])
                    .range([marginLeft, width - marginRight]);

                const y = d3.scaleBand()
                    .domain(chartData.map(d => d.holder))
                    .rangeRound([marginTop, dynamicHeight - marginBottom])
                    .padding(0.1);

                // Criar barras
                svg.append("g")
                    .attr("fill", "steelblue")
                    .selectAll("rect")
                    .data(chartData)
                    .join("rect")
                    .attr("x", x(0))
                    .attr("y", d => y(d.holder))
                    .attr("width", d => x(d.pctHeld) - x(0))
                    .attr("height", y.bandwidth())
                    .on("mouseover", (event, d) => {
                        tooltip.style("opacity", 1)
                            .html(`
                                <strong>${d.holder}</strong><br>
                                Percentage Held: ${d.pctHeld.toFixed(2)}%<br>
                                Total Shares: ${d.shares}<br>
                                Shares Value: ${d.value}<br>
                                Percentage Change: ${d.pctChange}
                            `);
                    })
                    .on("mousemove", (event) => {
                        tooltip.style("left", (event.pageX + 15) + "px")
                               .style("top", (event.pageY - 25) + "px");
                    })
                    .on("mouseout", () => {
                        tooltip.style("opacity", 0);
                    });

                svg.append("g")
                    .attr("fill", "white")
                    .attr("text-anchor", "end")
                    .selectAll("text")
                    .data(chartData)
                    .join("text")
                    .attr("x", d => x(d.pctHeld))
                    .attr("y", d => y(d.holder) + y.bandwidth() / 2)
                    .attr("dy", "0.35em")
                    .attr("dx", -4)
                    .text(d => `${d.pctHeld.toFixed(2)}%`)
                    .call(text => text.filter(d => x(d.pctHeld) - x(0) < 30) // Ajusta para barras curtas
                        .attr("dx", 4)
                        .attr("fill", "black")
                        .attr("text-anchor", "start"));

                // Eixo Y (nomes dos holders)
                svg.append("g")
                    .attr("transform", `translate(${marginLeft},0)`)
                    .call(d3.axisLeft(y).tickSizeOuter(0));
            })
            .catch(error => console.error("Erro ao carregar dados:", error));
    }

    // Obtém o símbolo da URL e carrega o gráfico ao iniciar a página
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        console.log("Carregando gráfico de Holders para:", symbol);
        fetchAndRenderChart(symbol);
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }

    // Configura a busca manual com o botão
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


// Stacked Bar Chart - Stock Recommendations Over Time
document.addEventListener("DOMContentLoaded", function () {
    function fetchAndRenderRecommendations(symbol) {
        fetch(`/stock/${symbol}/recommendations/`)
        .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    return;
                }

                d3.select("#stack-bar-recommendation-chart").selectAll("*").remove();

                const chartData = data.data.map(d => ({
                    period: d.period,
                    strongBuy: d.strongBuy,
                    buy: d.buy,
                    hold: d.hold,
                    sell: d.sell,
                    strongSell: d.strongSell
                }));

                const width = 800;
                const height = 300;
                const margin = { top: 30, right: 30, bottom: 50, left: 120 };

                const svg = d3.select("#stack-bar-recommendation-chart")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height + 50) // Ajustar espaço para a legenda
                    .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);

                // Criar escalas
                const x = d3.scaleLinear()
                    .domain([0, d3.max(chartData, d => d.strongBuy + d.buy + d.hold + d.sell + d.strongSell)])
                    .range([0, width - margin.left - margin.right]);

                const y = d3.scaleBand()
                    .domain(chartData.map(d => d.period))
                    .range([height - margin.top - margin.bottom, 0])
                    .padding(0.5); // Reduzindo a largura das barras

                // Cores para cada categoria
                const colors = {
                    strongBuy: "#14d500",
                    buy: "#6cd500",
                    hold: "#d5d200",
                    sell: "#d53500",
                    strongSell: "#d50000"
                };

                // Stack dos dados
                const stack = d3.stack()
                    .keys(["strongBuy", "buy", "hold", "sell", "strongSell"])
                    .order(d3.stackOrderNone)
                    .offset(d3.stackOffsetNone);

                const series = stack(chartData);

                // Criar barras empilhadas
                svg.selectAll("g")
                    .data(series)
                    .join("g")
                    .attr("fill", d => colors[d.key])
                    .selectAll("rect")
                    .data(d => d)
                    .join("rect")
                    .attr("y", d => y(d.data.period))
                    .attr("x", d => x(d[0]))
                    .attr("width", d => x(d[1]) - x(d[0]))
                    .attr("height", y.bandwidth())
                    .each(function (d) {
                        const textX = x(d[0]) + (x(d[1]) - x(d[0])) / 2;
                        const textY = y(d.data.period) + y.bandwidth() / 2;

                        if (d[1] - d[0] > 5) { // Apenas exibir se a barra for grande o suficiente
                            svg.append("text")
                                .attr("x", textX)
                                .attr("y", textY)
                                .attr("dy", "0.35em")
                                .attr("text-anchor", "middle")
                                .attr("fill", "white")
                                .attr("font-size", "12px")
                                .attr("font-weight", "bold")
                                .text(d[1] - d[0]);
                        }
                    });

                // Remover eixo X (NÃO MOSTRAR)
                // svg.append("g")
                //     .attr("transform", `translate(0,${height - margin.top - margin.bottom})`)
                //     .call(d3.axisBottom(x).ticks(5));

                // Adicionar eixo Y (períodos)
                svg.append("g")
                    .call(d3.axisLeft(y));

                // Criar legenda abaixo do gráfico
                const legend = svg.append("g")
                    .attr("transform", `translate(${width / 4}, ${height - margin.bottom})`);

                const legendSpacing = 20;
                const rectSize = 15;

                Object.keys(colors).forEach((key, i) => {
                    legend.append("rect")
                        .attr("x", i * 120)
                        .attr("y", 0)
                        .attr("width", rectSize)
                        .attr("height", rectSize)
                        .attr("fill", colors[key]);

                    legend.append("text")
                        .attr("x", i * 120 + rectSize + 5)
                        .attr("y", rectSize - 2)
                        .text(key)
                        .attr("fill", "#000")
                        .attr("font-size", "14px")
                        .attr("font-weight", "bold")
                        .attr("alignment-baseline", "middle");
                });
            })
            .catch(error => console.error("Erro ao carregar dados:", error));
    }

    // Obtém o símbolo da URL e carrega o gráfico ao iniciar a página
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        console.log("Carregando gráfico de recomendações para:", symbol);
        fetchAndRenderRecommendations(symbol);
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }

    // Configura a busca manual com o botão
    const searchButton = document.getElementById("searchButton");
    if (searchButton) {
        searchButton.addEventListener("click", function () {
            const symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();
            if (symbol) {
                fetchAndRenderRecommendations(symbol);
            } else {
                alert("Por favor, insira um símbolo de ação válido.");
            }
        });
    }
});
