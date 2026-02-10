# <p align="center"> **Taurus** </p>

![Logo](https://github.com/joaomalho/Taurus/blob/main/assets/taurus.png?raw=true)

**<p align="center"> Empowering Investors with Real-Time Financial Insights </p>**

Taurus is a cutting-edge tool that analyzes financial markets in real-time, helping investors make smarter and more informed decisions.

---

---

## **📈 Key Features**

### Advanced Technical Analysis:

- `Moving Averages and Crossovers`
- `Average Directional Index (ADX)`
- `Bollinger Bands`
- `Relative Strength Index (RSI)`
- `Candle Pattern Detection`
- `Harmonic Patterns Detection`
- `Pivots Points`

### Fundamental Analysis:

- 📊 Fundamental Analysis through complete Income Statements, Cash Flows, Balance Sheets and Insiders Decisions.
- 💡 Analysts Opinion Metrics
- 📰 Sentiment Analysis of Recent News
- 📅 Economic Calendar Correlations

### Risk Management:

- 📉 Max Drawdown and Expectancy
- 🛡️ Essential Ratios Consideration (Financial, Liquidity, Growth, Profitability, ...)
- 🎯 StopLoss detection

### Real-Time Data:

- Track Stocks, ETFs, Currencies, and Cryptocurrencies with near-instant updates.

---

---

## **⏳ Data Types and Expected Delays**

| Data Type              | Source          | Delay       | Description                                     |
| ---------------------- | --------------- | ----------- | ----------------------------------------------- |
| **Intraday**           | Yahoo Finance   | -1 minutes  | Near real-time data for short intervals.        |
| **Daily or Long-Term** | Yahoo Finance   | 1-2 minutes | Reliable data for historical analysis.          |
| **Currencies (Forex)** | Yahoo Finance   | 1 minutes   | Quick updates on currency markets.              |
| **Stock**              | Binance Finance | 1-2 minutes | Regular updates.                                |
| **Cryptocurrencies**   | Binance Finance | -1 minute   | Real-Time updates, dedicated APIs from Binance. |

---

---

## **🔧 Tech Stack**

- **Backend:** Python, JS
- **Frontend:** Django, HTML, CSS, Grid.js and Charts.js
- **Charts:** Charts.js, lightweight-charts
- **Data Analysis:** Pandas, NumPy, TA-Lib, ...
- **Machine Learning (Future):** TensorFlow, Scikit-learn ...

---

---

## **👨‍💻 Authors**

Built with 💻 by [@joaomalho](https://github.com/joaomalho).

---

---

## **📜 License**

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

---

## **⚠️ Disclaimers**

- Data is sourced from public APIs and may experience small delays.
- The analysis provided by the tool is advisory and does not replace investor judgment.
- This tool is open source and do not collect any fee for usage.
- We never ask or intend to collect data from users.

---

---

## **🎯 Vision and Future Impact**

Taurus is continually evolving, with goals to:

- Introduce AI-powered insights to predict market trends.
- Expand support for premium data APIs, such as Alpha Vantage and Binance.
- Enable fully customizable dashboards tailored to user preferences.

---

---

## **📌 Example Use Cases**

**1. Setting New Profitable Stocks Positions Alerts**

- Automatically receive alerts when favoral positions are detected.

**2. Simulating Risk with Sharpe Ratio**

- Assess the risk-return tradeoff of a portfolio before investing.

**3. Easy Understanding of Market Behavior**

- This tool provides a clear and comprehensive view of all asset information on a single screen.

---

---

## **🏆 Why Taurus?**

Taurus bridges the gap between complex market analysis and actionable insights, empowering investors of all levels to make data-driven decisions.

_Be the master of your investments with Taurus._

---

---

---

## **<p align="center"> 📘 Full Documentation</p>**

Follow the Documentation (WIP) for setup, usage details, and FAQs.

## **📝 Installation Prerequisites Guide - WIP**

Before you begin, make sure you have the following:

- **Python 3.8 or later, 11 recommended** installed
- **pip** (Python package manager)
- **Git** client to clone the repository (optional if downloading manually)

### 1️⃣ Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/joaomalho/Taurus.git
```

```bash
cd ~/Taurus
docker compose up --build -d
docker compose logs -f web
```


### **📌 Notes**

⚙️ **yfinance:** The yfinance library requires specific installation options (--upgrade --no-cache-dir). The installation scripts handle this automatically, so you don’t need to worry about it.

🐍 Ensure that **Python 3.8 or later, 11 recommended** is installed on your machine. You can check your version by running:

```bash
python --version
```

💹 **TA-Lib:** The TA-Lib direct installation via `pip install ta-lib` cause an error, probably because you haven't installed actual TA-Lib library which is written in C. Note that the python lib is just a wrapper on top of the actual library. So in order to have python wrapper successfully installed, you'll need to install its prerequisite (the actual TA-Lib). We try to handle that via our installation tool for Windows.

📦 The installation scripts handle all dependencies listed in requirements.txt, including fastapi, psycopg2, pandas, numpy, yfinance, and others. It also try to Linux, although our DEV and QA environments are based on Windows we will further develop for Linux.

### **🛠️ Troubleshooting**

If you encounter any issues during installation, here are some common solutions:

❌ **Missing pip:**
If you get an error saying pip is not found, install it by following these instructions.

🔒 **Permission issues:**
On Linux/Mac, you may need to prepend sudo to some commands if you get permission errors.

🧩 **Missing dependencies:**
If a dependency fails to install, ensure you have all system requirements for the libraries (e.g., development tools, headers, etc.) and try running the installation command again.

---

---

## **🪙 Type of Markets**

Taurus provides comprehensive, detailed and real-time access to the forex, stock, and cryptocurrency markets, collecting complete information on all available tickers across these market types. Our data providers include Yahoo for forex and stock information and Binance for cryptocurrency data.

---

---

## **📝 Caddle Patterns Detection Guide**

Our tool is capable of detecting X-candle patterns in the market.

Each candle pattern has an associated stop-loss target and relevance level as outlined in the table below:

| Pattern Name               | Classification | Candles Range Detection |
| :------------------------- | :------------- | :---------------------- |
| **Doji**                   | Reversal       | 3                       |
| **Dragonfly Doji**         | Reversal       | 3                       |
| **Gravestone Doji**        | Reversal       | 3                       |
| **Engulfing**              | Reversal       | 3                       |
| **Morning Star**           | Reversal       | 5-7                     |
| **Evening Star**           | Reversal       | 5-7                     |
| **Morning Doji Star**      | Reversal       | 5-7                     |
| **Evening Doji Star**      | Reversal       | 5-7                     |
| **Hammer**                 | Reversal       | 3                       |
| **Inverted Hammer**        | Reversal       | 3                       |
| **Hanging Man**            | Reversal       | 3                       |
| **Shooting Star**          | Reversal       | 3                       |
| **Marubozu**               | Continuation   | 3                       |
| **Harami**                 | Reversal       | 3                       |
| **Harami Cross**           | Reversal       | 3                       |
| **Spinning Top**           | Continuation   | 3-5                     |
| **Kicking**                | Reversal       | 3                       |
| **Kicking by Length**      | Reversal       | 3                       |
| **Tasuki Gap**             | Continuation   | 3-5                     |
| **Gap Side By Side White** | Continuation   | 3-5                     |
| **Counterattack**          | Reversal       | 3                       |
| **Piercing**               | Reversal       | 3                       |
| **Dark Cloud Cover**       | Reversal       | 3                       |
| **Tri Star**               | Reversal       | 3                       |
| **On Neck**                | Continuation   | 3                       |
| **In Neck**                | Continuation   | 3                       |
| **Thrusting**              | Continuation   | 3                       |
| **Matching Low**           | Reversal       | 3                       |
| **Three Black Crows**      | Complex        | 5-7                     |
| **Three White Soldiers**   | Complex        | 5-7                     |
| **Three Inside**           | Complex        | 5-7                     |
| **Three Outside**          | Complex        | 5-7                     |
| **Three Stars in South**   | Complex        | 5-7                     |
| **Advance Block**          | Complex        | 5-7                     |
| **Stalled Pattern**        | Complex        | 5-7                     |
| **Abandoned Baby**         | Reversal       | 5-7                     |
| **Unique 3 River**         | Complex        | 5-7                     |
| **Belt Hold**              | Reversal       | 3                       |
| **Separating Lines**       | Continuation   | 3                       |
| **Upside Gap Two Crows**   | Complex        | 5-7                     |

## Application only presents candles which stoploss was not acomplished.

---

### ⚖️ **Relevance:**

**Pattern recency:** The more recent the pattern, the more relevant it is. Patterns that occurred many candles ago lose their influence on the market's current behavior. However, this does not invalidate the targets already defined when the pattern was detected.

**Market volatility:** In highly volatile markets, older patterns lose relevance more quickly, whereas in slower markets, they may remain valid for longer. Once the defined targets are reached, the pattern is disregarded.

**Pattern overlap:** In cases where one pattern overlaps another within the consideration range, if they are contradictory, the new pattern is disregarded. After the consideration range, the new targets are taken into account. In situations where the overlapping patterns are unidirectional, the old targets are maintained, and after they are reached, the new targets are considered.

**Consideration range:** The consideration range depends on the detected pattern and is classified as, `reversal` patterns consider 3 candles, `continuation` patterns consider 3 to 5 candles, and `complex` patterns consider 5 to 7 candles. Aside from this tool presenting candle detection across the full historical dataset, the consideration range will focus exclusively on the last 10 candles, regardless of the timeframe.

**Position opening:** The detection of a pattern **is not** sufficient by itself to justify opening a position.

---

---

## **⚙️ Auto Calibration and Optimization**

Taurus have an auto-calibration and optimization method designed to measure, test, and select the best parameters for technical analysis metrics. This method leverages a backtesting environment to evaluate metric performance over the past 365 days of the selected asset's market data.

---

---

## **🏢 Insider Information**

Real-time insider trading information is available for all US stocks. This data is sourced from the SEC and provides insights into the buying and selling activities of company insiders.

---

---

---

---

---

## 🎉 **Congratulations!**

You’re all set to use Taurus. If you have any issues, feel free to open an issue on the GitHub [ISSUES](https://github.com/joaomalho/Taurus/issues).

---

---

---

## **<p align="center"> 🚀 Calling All Developers! 👨‍💻👩‍💻 </p>**

We are looking for **passionate coders** to join our **open-source community** 🌍.

🎯 **Roles Available:**

- 🛠️ Maintainers
- 🧪 Testers
- 🎨 UI/UX Designers

We are also looking to grow our community with **key roles in market analysis**:

- **📈 Technical Analyst** → Studies price action & indicators.
- **📊 Fundamental Analyst** → Evaluates financial statements & economic factors.
- **🤖 Quantitative Analyst (Quant)** → Develops algorithmic trading models.
- **⚠️ Risk Manager** → Manages portfolio risks & exposure.
- **💸 Short-Term Investor** → Focuses on day & swing trading.
- **🏦 Long-Term Investor** → Buys & holds assets for long-term gains.
- **🪙 Crypto Analyst** → Researches & analyzes cryptocurrency markets.
- **🎯 Options Trader** → Trades derivatives like calls & puts.

📍 **Join us to level up your market knowledge!** 🚀📈

📢 Join us today and contribute! 🤝

🌍 Community:

- 🗨️ **Discord** - 🔗 [Join Here](#https://discord.gg/TnjNUGxr)
- 👽 **Reddit** - 🔗 [Join Here](#) - WIP

---

---

---

## **<p align="center"> 👨‍💻 Developments & Improvements </p>**

## **🛠️ Next steps**

- DevOps

  - Up on VM `ToDo: Medium`

- Technical Analysis

  - Pivots Point - `ToDo: Low`
  - Add metrics and drawn to candlestik graph.
    - ADX `ToDo: Medium`
    - Candles Marks `ToDo: Medium`

- Fundamental Analysis

  - Add Holders last report date to know when info was updated `ToDo: High`

  - Sentiment Analysis of Recent News - `ToDo: Low`
  - Add Tags on Headers to Easly get info - `ToDo: Low`
  - Downloads remaining fundamental documents and full report. `ToDo: High`

- Additional Screens

  - Missing Catalog for penny, top of day, top of week.
  - FAQs page `ToDo: High`
  - Information Page `ToDo: High`
  - Information marker points `ToDo: High`
  - Macro overview
  - Micro overview by sector

- Nice to Have

  - Economic Calendar Correlations - WIP - Pay to use - Standby Nice to Have
  - Economic Calendar - WIP - Pay to use - Standby Nice to Have

## **🚀 Latest Improvements**

- **Cache Improvement**

Notes:
-- Adjust charts over values. Fine tunning.
-- Finish css pallete
-- Finish cache control
