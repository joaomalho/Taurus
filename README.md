# <p align="center"> **Taurus** </p>


![Logo](https://github.com/joaomalho/Taurus/blob/main/images/taurus.png?raw=true)

**<p align="center"> Empowering Investors with Real-Time Financial Insights </p>**

Taurus is a cutting-edge tool that analyzes financial markets in real-time, helping investors make smarter and more informed decisions.

---
---


## **📈 Key Features**

### Advanced Technical Analysis:
- `Moving Averages and Crossovers`
- `Bollinger Bands`
- `Relative Strength Index (RSI)`

### Fundamental Analysis:
- 📰 Sentiment Analysis of Recent News
- 💡 Analysts Opinion Metrics

### Risk Management:
- 📉 Max Drawdown and Expectancy
- 🛡️ Sharpe Ratio Calculations

### Real-Time Data:
- Track Stocks, ETFs, Currencies, and Cryptocurrencies with near-instant updates.

---
---

## **🚀 Latest Updates**
- **Risk Manager:** A new feature to help minimize losses in volatile markets.
- **Valuation Metrics:** Powerful indicators for long-term strategies and fundamental analysis.

---
---


## **⏳ Data Types and Expected Delays**

| Data Type            | Source        | Delay           | Description                                        |
|----------------------|---------------|-----------------|----------------------------------------------------|
| **Intraday**         | Yahoo Finance | 1-2 minutes     | Near real-time data for short intervals.           |
| **Daily or Long-Term**| Yahoo Finance | 1-2 minutes | Reliable data for historical analysis.        |
| **Currencies (Forex)**| Yahoo Finance | 1-2 minutes   | Quick updates on currency markets.                |
| **Cryptocurrencies** | Yahoo Finance | 1-2 minutes     | Regular updates, though slower than dedicated APIs like Binance. |

---
---


## **🔧 Tech Stack**

- **Backend:** Python, YFinance API
- **Frontend:** Angular, Material Design
- **Charts:** Chart.js, D3.js
- **Data Analysis:** Pandas, NumPy
- **Machine Learning (Future):** TensorFlow, Scikit-learn

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

*Be the master of your investments with Taurus.*

---
---

## **🛠️ Next steps**
- Risk Manager
- FrontEnd firt version release
- Improve Crypto source (binance)
- Improve Forex source (metatrader5)

---
---

## **📘 Full Documentation**

Follow the Documentation (WIP) for setup, usage details, and FAQs.


## **📝 Installation Prerequisites Guide** 

Before you begin, make sure you have the following:

- **Python 3.8 or later** installed
- **pip** (Python package manager)
- A **Git** client to clone the repository (optional if downloading manually)

### 1️⃣ Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/joaomalho/Taurus.git
cd Taurus
```

Alternatively, if you prefer not to use Git, you can download the repository as a ZIP file from GitHub and extract it to a folder.

### 2️⃣ Install Dependencies

**🐧 For Linux/Mac:**

To install the required dependencies, run the following script:
```bash
./install.sh
```
Make sure the script is executable by running:
```bash
chmod +x install.sh
```
Then, execute it to install all necessary libraries.

**🖥️ For Windows:**

If you’re using Windows, you can install dependencies by running the batch script:
```bash
install.bat
``` 
Just double-click the install.bat file, or run it from a Command Prompt.

### 3️⃣ Direct Installation (Recommendation)
Alternatively, if you want to install the application as a Python package directly, you can use the setup.py file:
```bash
python setup.py install
```
This method installs the app and all its dependencies globally, making it easier to use across different environments.

### **📌 Notes**
⚙️ **yfinance:** The yfinance library requires specific installation options (--upgrade --no-cache-dir). The installation scripts handle this automatically, so you don’t need to worry about it.

🐍 Ensure that **Python 3.8 or later** is installed on your machine. You can check your version by running:
```bash
python --version
```
📦 The installation scripts handle all dependencies listed in requirements.txt, including fastapi, psycopg2, pandas, numpy, yfinance, and others.

### **🛠️ Troubleshooting**
If you encounter any issues during installation, here are some common solutions:

❌ **Missing pip:** If you get an error saying pip is not found, install it by following these instructions.

🔒 **Permission issues:** On Linux/Mac, you may need to prepend sudo to some commands if you get permission errors:
```bash
sudo pip install -r requirements.txt
```
🧩 **Missing dependencies:** If a dependency fails to install, ensure you have all system requirements for the libraries (e.g., development tools, headers, etc.) and try running the installation command again.

---
---

## 🎉 **Congratulations!** 
You’re all set to use Taurus. If you have any issues, feel free to open an issue on the GitHub [ISSUES](https://github.com/joaomalho/Taurus/issues).