# 🛵 Swiggy End-to-End Data Analytics & Consumer Insights

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Seaborn-Visualization-3776AB?style=for-the-badge" alt="Seaborn"/>
  <img src="https://img.shields.io/badge/Status-Completed-10b981?style=for-the-badge" alt="Status"/>
</p>

---

## 📌 Executive Summary
In the hyper-competitive food-delivery tech landscape, unit economics and delivery SLA compliance determine profitability. This project presents an end-to-end exploratory and diagnostic analytics pipeline on **Swiggy's food ordering and restaurant network records**.

The objective is to identify **peak demand bottlenecks, city-wise customer retention dynamics, restaurant price sensitivity**, and provide actionable operational recommendations for fleet dispatchers and marketplace managers.

---

## 🎯 Business Problem & Core Objectives
1. **Demand Surge Profiling:** Pinpoint exact time windows where order volumes overwhelm kitchen prep capacity.
2. **Geographical Revenue Concentration:** Quantify order density across city zones to test the **Pareto Principle (80/20 Rule)**.
3. **Price Sensitivity vs. Customer Loyalty:** Examine the trade-off between restaurant cost-for-two, discount depth, and customer review scores.
4. **Actionable Marketplace Strategy:** Formulate recommendations to reduce delivery turnaround times and mitigate order cancellations.

---

## 🛠️ Tech Stack & Methodology
* **Language:** Python
* **Libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`
* **Workflow:**
  1. **Data Ingestion & Cleaning:** Handling missing rating values, parsing price strings (e.g. converting `₹350 for two` to clean numerical integers), standardizing cuisine tags, and de-duplicating restaurant entities.
  2. **Feature Engineering:** Extracted `Order_Hour`, `Rush_Hour_Flag`, `Cuisine_Diversity_Score`, and `Price_Tier` bins.
  3. **Univariate & Bivariate EDA:** Distribution analysis of delivery times, ratings, and bill values.
  4. **Multivariate Correlation:** Heatmap analysis evaluating relationships between price, discount percentages, and customer feedback.

---

## 📈 Key Findings & Insights

| Dimension | Finding | Business Impact |
| :--- | :--- | :--- |
| **Peak Rush Windows** | Orders spike **2.4x** between **12:30–2:30 PM (Lunch)** and **7:30–10:30 PM (Dinner)**. | Kitchen prep time climbs by ~14 mins, driving up delivery latency. |
| **Pareto GMV Concentration** | Top **18.5%** of restaurant partners generate **73.2%** of gross order volume. | Prioritizing dispatch to top-tier partners prevents delivery partner idle time. |
| **Sweet Spot Pricing** | Meals priced at **₹300 - ₹500** hold the highest repeat order rate and 4.2+ ratings. | Budget restaurants (<₹200) showed high cancellation due to stockouts. |
| **Cuisine Popularity** | North Indian, Biryani, and Fast Food capture over **65%** of total order volume. | Targeted banner promotions during evening snacks boost cross-selling. |

---

## 💡 Strategic Business Recommendations
* **Dynamic Fleet Staging:** Shift 30% of delivery partners to identified "High GMV Clusters" 30 minutes before 7:30 PM to cut dispatch latency by ~12%.
* **Kitchen Prep SLA Incentives:** Partner with top 20% restaurants to integrate automated prep notifications, eliminating delivery driver waiting times at restaurant gates.
* **Tiered Promotional Bundles:** Curate combo offerings in the optimal ₹350–₹450 price bracket to elevate Average Order Value (AOV).

---

## 📂 Repository Structure
```
├── data/
│   └── swiggy_orders_dataset.csv     # Raw & cleaned datasets
├── notebooks/
│   └── swiggy_end_to_end_eda.ipynb   # Complete reproducible workflow
├── visual_assets/                    # Visualizations & distribution charts
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🚀 How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/Lokesh7-pqndey/Swiggy-End-To-End-Data-Analytics.git
   cd Swiggy-End-To-End-Data-Analytics
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook notebooks/swiggy_end_to_end_eda.ipynb
   ```

---

## 👤 Author
* **Lokesh Pandey**
* [LinkedIn](https://linkedin.com/in/pandeylokesh87) • [Email](mailto:pandeylokesh87@gmail.com)
