// Candlestick Chart using D3.js
document.addEventListener("DOMContentLoaded", function () {
    function fetchAndRenderCandlestick(symbol, period, interval) {
        fetch(`/stock/${symbol}/data_history/?period=${period}&interval=${interval}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao buscar dados do candlestick:", data.error);
                    document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro: ${data.error}</h3>`;
                    return;
                }

                d3.select("#candlestickChart").selectAll("*").remove(); // Remove gráfico anterior

                processCandlestickData(data);
            })
            .catch(error => {
                console.error("Erro ao buscar os dados do candlestick:", error);
                document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Erro ao buscar os dados.</h3>`;
            });
    }

    function processCandlestickData(data) {
        if (!data.data || data.data.length === 0) {
            console.error("Nenhum dado encontrado no JSON:", data);
            document.getElementById("candlestickChart").innerHTML = `<h3 style="color: red;">Nenhum dado disponível</h3>`;
            return;
        }

        console.log("Processando dados para o gráfico:", data.data);

        let parsedData = data.data.map(entry => ({
            Date: new Date(entry.Date),
            Open: parseFloat(entry.Open),
            High: parseFloat(entry.High),
            Low: parseFloat(entry.Low),
            Close: parseFloat(entry.Close)
        }));

        renderCandlestickChart(parsedData);
    }

    function renderCandlestickChart(ticker) {
        // 🔹 Filtrar as últimas 100 velas
        const recentData = ticker.slice(-100);
    
        // 🔹 Filtrar as datas para exibição a cada 15 dias
        const filteredDates = recentData
            .map(d => d.Date)
            .filter((date, i, arr) => i % 15 === 0 || i === arr.length - 1); // Mantém o último item
    
        // Dimensões e margens
        const width = 1200;
        const height = 500;
        const margin = { top: 20, right: 40, bottom: 40, left: 50 };
    
        // Criar escalas
        const x = d3.scaleBand()
            .domain(recentData.map(d => d.Date))
            .range([margin.left, width - margin.right])
            .padding(0.2);
    
        const y = d3.scaleLinear()
            .domain([d3.min(recentData, d => d.Low), d3.max(recentData, d => d.High)])
            .range([height - margin.bottom, margin.top]);
    
        // Criar SVG
        const svg = d3.select("#candlestickChart")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
    
        // Criar um fundo branco para o gráfico
        svg.append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", width)
            .attr("height", height)
            .attr("fill", "#171b26");
    
        // Adicionar eixo X (apenas para as datas filtradas)
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(
                d3.axisBottom(x)
                    .tickValues(filteredDates)
                    .tickFormat(d3.timeFormat("%b %d"))
                    .tickSizeOuter(0)
            )
            .selectAll("text")
            .attr("transform", "rotate(-45)")
            .style("text-anchor", "end");
    
        // Adicionar eixo Y
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y).tickFormat(d3.format(".2f")))
            .call(g => g.select(".domain").remove());
    
        // Adicionar candles
        const g = svg.append("g")
            .attr("stroke-linecap", "round")
            .attr("stroke", "black")
            .selectAll("g")
            .data(recentData)
            .join("g")
            .attr("transform", d => `translate(${x(d.Date)},0)`);
    
        // Linha de alta/baixa
        g.append("line")
            .attr("y1", d => y(d.Low))
            .attr("y2", d => y(d.High))
            .attr("stroke", d => d.Open > d.Close ? "#f23645" : "#089981");
    
        // Corpo do candle
        g.append("line")
            .attr("y1", d => y(d.Open))
            .attr("y2", d => y(d.Close))
            .attr("stroke-width", x.bandwidth())
            .attr("stroke", d => d.Open > d.Close ? "#f23645" : "#089981");
    
        // Tooltip
        const tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("position", "absolute")
            .style("background", "#222")
            .style("color", "#fff")
            .style("padding", "8px")
            .style("border-radius", "4px")
            .style("font-size", "12px")
            .style("opacity", 0)
            .style("pointer-events", "none");
    
        g.on("mouseover", (event, d) => {
            tooltip.style("opacity", 1)
                .html(`
                    <strong>${d3.timeFormat("%B %d, %Y")(d.Date)}</strong><br>
                    Open: ${d.Open.toFixed(2)}<br>
                    Close: ${d.Close.toFixed(2)}<br>
                    High: ${d.High.toFixed(2)}<br>
                    Low: ${d.Low.toFixed(2)}
                `);
        })
        .on("mousemove", (event) => {
            tooltip.style("left", (event.pageX + 15) + "px")
                   .style("top", (event.pageY - 25) + "px");
        })
        .on("mouseout", () => {
            tooltip.style("opacity", 0);
        });
    }
    
    
    // Obter símbolo da URL e carregar o gráfico
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];

    if (symbol) {
        console.log("Carregando gráfico de Candlestick para:", symbol);
        fetchAndRenderCandlestick(symbol, "1mo", "1d");
    } else {
        console.error("Nenhum símbolo encontrado na URL!");
    }
});
