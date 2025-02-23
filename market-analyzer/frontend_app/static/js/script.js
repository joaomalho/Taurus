document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada com sucesso!");
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchButton").addEventListener("click", fetchStockData);
});

function fetchStockData() {
    let symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();

    if (!symbol) {
        alert("Please enter a stock symbol!");
        return;
    }

    // Redireciona para uma nova página com o símbolo na URL
    window.location.href = `/stock/${symbol}`;
}
