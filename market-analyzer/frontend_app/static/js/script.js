document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada com sucesso!");
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchButton").addEventListener("click", fetchStockData);
});

function fetchStockData() {
    let symbol = document.getElementById("stockSymbol").value.trim();

    if (!symbol) {
        alert("Please enter a stock symbol!");
        return;
    }

    fetch(`/get_stock_data/?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }
            updateTable(data);
        })
        .catch(error => console.error("Error fetching data:", error));
}

function updateTable(data) {
    let tableHTML = `
        <h2>Stock Data for ${data.symbol}</h2>
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

    document.getElementById("tableContainer").innerHTML = tableHTML;
}
