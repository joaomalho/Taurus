// Pie Chart Institutional Holders 

document.addEventListener("DOMContentLoaded", function () {
    const width = 500;
    const height = Math.min(500, width / 2);
    const outerRadius = height / 2 - 10;
    const innerRadius = outerRadius * 0.75;
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const svg = d3.select("#pie-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const arc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);

    const pie = d3.pie()
        .sort(null)
        .value(d => d.pctHeld);

    function fetchAndRenderChart(symbol) {
        fetch(`/stock/${symbol}/institutional_holders/`)
        .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados:", data.error);
                    return;
                }
                
                svg.selectAll("*").remove();

                const chartData = data.data.map(d => ({
                    holder: d.Holder,
                    pctHeld: d.pctHeld
                }));

                const path = svg.selectAll("path")
                    .data(pie(chartData))
                    .enter()
                    .append("path")
                    .attr("fill", (d, i) => color(i))
                    .attr("d", arc)
                    .each(function (d) { this._current = d; });

                svg.selectAll("text")
                    .data(pie(chartData))
                    .enter()
                    .append("text")
                    .attr("transform", d => `translate(${arc.centroid(d)})`)
                    .attr("text-anchor", "middle")
                    .attr("font-size", "12px")
                    .attr("fill", "white")
                    .text(d => d.data.holder);
            })
            .catch(error => console.error("Erro ao carregar dados:", error));
    }

    // **Obtém o símbolo da URL e carrega o gráfico ao iniciar a página**
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        console.log("Carregando gráfico de Holders para:", symbol);
        fetchAndRenderChart(symbol);
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }

    // **Configura a busca manual com o botão**
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
