// Bar Chart Institutional Holders with Tooltip
document.addEventListener("DOMContentLoaded", function () {
    const width = 800;
    const barHeight = 25;
    const marginTop = 30;
    const marginRight = 30;
    const marginBottom = 10;
    const marginLeft = 250; // Ajustado para labels longos
    const height = 500;

    // Criar Tooltip
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

                d3.select("#h-bar-chart").selectAll("*").remove(); // Limpa gráfico anterior

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

                // Adicionar labels dentro das barras
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
