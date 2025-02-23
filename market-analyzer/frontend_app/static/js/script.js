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

// 🔥 Função para buscar dados do servidor
function fetchStockData(symbol) {
    fetch(`/get_stock_data/?symbol=${symbol}`)  // ✅ CORRIGIDO
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("tableContainerStock").innerHTML = "<h2>Stock not found</h2>";
            } else {
                updateTable(data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("tableContainerStock").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

// 🔥 Atualiza a tabela na página stock.html
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
    fetchYahooGainers();
});

function fetchYahooGainers() {
    fetch("/screener/get_yahoo_gainers/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("yahooGainersContainer").innerHTML = "<h2>Erro ao carregar os dados.</h2>";
            } else {
                populateYahooGainersTable(data.data);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            document.getElementById("yahooGainersContainer").innerHTML = "<h2>Erro ao buscar os dados.</h2>";
        });
}

// 🔥 Função para preencher a tabela com os dados recebidos
function populateYahooGainersTable(data) {
    let headerRow = document.getElementById("yahooGainersHeader");
    let tableBody = document.getElementById("yahooGainersBody");

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
