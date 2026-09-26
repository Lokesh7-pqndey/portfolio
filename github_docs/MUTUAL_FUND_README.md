# 📊 Mutual Fund Investment Analytics & BI Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Power_BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI"/>
  <img src="https://img.shields.io/badge/DAX-Advanced%20Measures-2D3748?style=for-the-badge" alt="DAX"/>
  <img src="https://img.shields.io/badge/Python-Data%20Extraction-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Domain-Wealth%20Tech-f59e0b?style=for-the-badge" alt="Finance"/>
</p>

---

## 📌 Executive Summary
Most retail investors evaluate mutual funds purely on trailing 1-year or 3-year returns, ignoring downside risk, volatility, and market benchmark comparisons. A fund returning 22% during a bull market could experience catastrophic drawdowns during a correction.

This project delivers an **interactive investment intelligence suite** developed in **Power BI and Python**, designed to evaluate **50+ Indian mutual fund schemes across Large, Mid, Small, and Multi-Cap categories** against the **NIFTY 50** benchmark index. It isolates manager **Alpha** from market **Beta** and empowers wealth advisors to construct risk-optimized portfolios.

---

## 🏗️ Architecture & Data Modeling (Star Schema)

The dashboard data model is built using a strict **Star Schema** architecture in Power BI to maximize DAX calculation speed and prevent circular cross-filtering:

```
          ┌───────────────────┐
          │     Dim_Date      │
          └─────────┬─────────┘
                    │ 1:*
                    ▼
┌──────────────┐ 1:*┌───────────────────┐*:1 ┌───────────────────┐
│   Dim_Fund   ├───►│     Fact_NAV      │◄───┤   Dim_Benchmark   │
└──────────────┘    └───────────────────┘    └───────────────────┘
                            │*:1
                            ▼
                    ┌───────────────────┐
                    │   Dim_Category    │
                    └───────────────────┘
```

* **`Fact_NAV`**: Contains historical daily Net Asset Value records, trade dates, and NAV fluctuations.
* **`Dim_Fund`**: Fund names, Asset Management Companies (AMCs), Expense Ratios, and AUM size.
* **`Dim_Benchmark`**: Historical daily closing values for NIFTY 50 and category indices.
* **`Dim_Date`**: Centralized calendar table supporting standard Time Intelligence functions.

---

## 🧮 Key Financial DAX Measures Implemented

### 1. Compound Annual Growth Rate (CAGR)
$$\text{CAGR} = \left( \frac{\text{Current NAV}}{\text{Initial NAV}} \right)^{\frac{1}{N}} - 1$$
```dax
Fund_CAGR_3Y = 
VAR StartNAV = CALCULATE(SELECTEDMEASURE(), DATEADD('Dim_Date'[Date], -3, YEAR))
VAR EndNAV = SELECTEDMEASURE()
RETURN
IF(NOT ISBLANK(StartNAV), POWER(DIVIDE(EndNAV, StartNAV), 1/3) - 1, BLANK())
```

### 2. Sharpe Ratio (Risk-Adjusted Return)
Measures excess return per unit of volatility relative to the risk-free rate ($R_f \approx 6.5\%$ Govt Bond Yield):
```dax
Sharpe_Ratio = 
VAR RiskFreeRate = 0.065
VAR AnnualReturn = [Fund_CAGR_3Y]
VAR Volatility = STDEV.S('Fact_NAV'[Daily_Return]) * SQRT(252)
RETURN
DIVIDE(AnnualReturn - RiskFreeRate, Volatility)
```

### 3. Maximum Drawdown (Downside Risk)
Tracks the maximum observed loss from a peak to a trough before a new peak is attained:
```dax
Max_Drawdown = 
VAR CumulativeMax = MAXX(FILTER(ALLSELECTED('Dim_Date'), 'Dim_Date'[Date] <= MAX('Dim_Date'[Date])), [Fund_NAV])
RETURN
MINX(VALUES('Dim_Date'[Date]), DIVIDE([Fund_NAV] - CumulativeMax, CumulativeMax))
```

---

## 🖥️ Dashboard Views & Visual Features
1. **Executive Performance Overview:** Multi-period performance benchmarking (1Y, 3Y, 5Y), top gainers, and category-wise AUM distribution.
2. **Risk-Reward Matrix (Scatter Plot):** Plots Annualized Volatility (X-axis) vs. CAGR (Y-axis) with quadrant overlays to visually isolate high-alpha, low-volatility winners.
3. **Fund Deep Dive:** Dynamic drill-through cards evaluating Expense Ratio vs. Manager Alpha and sector weight breakdowns.
4. **Interactive Filters:** Dynamic slicers for Asset Class, AMC, Risk Rating, and Date Time-frames.

---

## 💡 Key Business Takeaways
* **Small Cap Volatility Trap:** Several top-performing small-cap funds exhibited Maximum Drawdowns exceeding **-32%**, yielding Sharpe ratios inferior to disciplined Large & Mid-Cap alternatives.
* **Expense Ratio Disconnect:** Funds charging >2.1% expense ratios failed to produce statistically significant Alpha over the 5-year benchmark.
* **Market Outperformance:** Identified 8 specific mid-cap funds that consistently maintained positive Alpha (>3.4%) during broad-market downturns.

---

## 🚀 How to Open the Dashboard
1. Ensure **Power BI Desktop** is installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/Lokesh7-pqndey/mutual-fund-analysis-Dashboard-Python-PowerBI.git
   ```
3. Open the file `Mutual_Fund_Analytics.pbix` in Power BI Desktop.
4. Use the interactive slicers to filter funds by AMC and risk profiles.

---

## 👤 Author
* **Lokesh Pandey**
* [LinkedIn](https://linkedin.com/in/pandeylokesh87) • [Email](mailto:pandeylokesh87@gmail.com)
