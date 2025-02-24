document.addEventListener("DOMContentLoaded", function () {
    console.log("Script carregado com sucesso!");

    // Adiciona evento ao botão de pesquisa (usado tanto no index.html quanto no stock.html)
    let searchButton = document.getElementById("searchButton");
    if (searchButton) {
        searchButton.addEventListener("click", function () {
            let symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();

            if (!symbol) {
                alert("Please enter a stock symbol!");
                return;
            }

            // 🔥 Redireciona para a URL correta definida no `urls.py`
            window.location.href = `/stock/${symbol}/`;
        });
    }

    // 🔥 Captura o símbolo da URL correta `/stock/AAPL/`
    let pathParts = window.location.pathname.split("/");
    let symbol = pathParts[2];  // Captura "AAPL" da URL `/stock/AAPL/`

    if (symbol) {
        console.log("Buscando dados para:", symbol);
        fetchStockData(symbol);
    }
});

function updateTable(data) {
    let tableHTML = `
        <h2>Market Data for ${data.symbol}</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Change</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data.name}</td>
                    <td>${data.price}</td>
                    <td>${data.change}</td>
                </tr>
            </tbody>
        </table>
    `;
    document.getElementById("tableContainerStock").innerHTML = tableHTML;
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Script carregado com sucesso!");

    // 🔥 Redireciona para a página Screener quando o botão for clicado
    let screenerButton = document.getElementById("screenerButton");
    if (screenerButton) {
        screenerButton.addEventListener("click", function () {
            window.location.href = "/screener/";
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    console.log("Script carregado com sucesso!");

    // 🔥 Chama a função para buscar os dados quando a página carrega
    fetchYahooStockGainers();
});

function fetchYahooStockGainers() {
    fetch("/screener/get_yahoo_stock_gainers/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockGainersContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockGainersTable(data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockGainersContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function populateYahooStockGainersTable(data) {
    let headerRow = document.getElementById("yahooStockGainersHeader");
    let tableBody = document.getElementById("yahooStockGainersBody");

    // Limpa qualquer dado antigo
    headerRow.innerHTML = "";
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='100%'>Nenhum dado disponível</td></tr>";
        return;
    }

    // 🔥 Adiciona os cabeçalhos da tabela (baseados nas chaves do JSON)
    let headers = Object.keys(data[0]);
    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });

    // 🔥 Adiciona os dados na tabela
    data.forEach(row => {
        let tr = document.createElement("tr");
        headers.forEach(header => {
            let td = document.createElement("td");
            td.textContent = row[header] ? row[header] : "-";
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    console.log("Script carregado com sucesso!");

    // 🔥 Chama a função para buscar os dados quando a página carrega
    fetchYahooStockTrending();
});

function fetchYahooStockTrending() {
    fetch("/screener/get_yahoo_stock_trending/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockTrendingContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockTrendingTable(data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockTrendingContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function populateYahooStockTrendingTable(data) {
    let headerRow = document.getElementById("yahooStockTrendingHeader");
    let tableBody = document.getElementById("yahooStockTrendingBody");

    // Limpa qualquer dado antigo
    headerRow.innerHTML = "";
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='100%'>Nenhum dado disponível</td></tr>";
        return;
    }

    // 🔥 Adiciona os cabeçalhos da tabela (baseados nas chaves do JSON)
    let headers = Object.keys(data[0]);
    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });

    // 🔥 Adiciona os dados na tabela
    data.forEach(row => {
        let tr = document.createElement("tr");
        headers.forEach(header => {
            let td = document.createElement("td");
            td.textContent = row[header] ? row[header] : "-";
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Script carregado com sucesso!");

    fetchYahooStockMostActive();
});

function fetchYahooStockMostActive() {
    fetch("/screener/get_yahoo_stock_most_active/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooStockMostActiveContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooStockMostActiveTable(data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooStockMostActiveContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

function populateYahooStockMostActiveTable(data) {
    let headerRow = document.getElementById("yahooStockMostActiveHeader");
    let tableBody = document.getElementById("yahooStockMostActiveBody");

    // Limpa qualquer dado antigo
    headerRow.innerHTML = "";
    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='100%'>Nenhum dado disponível</td></tr>";
        return;
    }

    // 🔥 Adiciona os cabeçalhos da tabela (baseados nas chaves do JSON)
    let headers = Object.keys(data[0]);
    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });

    // 🔥 Adiciona os dados na tabela
    data.forEach(row => {
        let tr = document.createElement("tr");
        headers.forEach(header => {
            let td = document.createElement("td");
            td.textContent = row[header] ? row[header] : "-";
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}
