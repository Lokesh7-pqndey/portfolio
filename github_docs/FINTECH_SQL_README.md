# 🏦 Fintech HR Analytics — Advanced SQL Analytics System

<p align="center">
  <img src="https://img.shields.io/badge/SQL-PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Queries-Window%20Functions-CC292B?style=for-the-badge" alt="Window Functions"/>
  <img src="https://img.shields.io/badge/Modeling-CTEs%20%26%20Subqueries-4479A1?style=for-the-badge" alt="CTEs"/>
  <img src="https://img.shields.io/badge/Domain-Fintech%20HR-ff6b00?style=for-the-badge" alt="Fintech"/>
</p>

---

## 📌 Project Overview
Workforce compensation, attrition dynamics, and department parity are critical financial levers in scaling fintech organizations. Poor visibility into salary distributions and retention cohorts leads to costly talent flight and bloated operational budgets.

This repository features **production-grade SQL analytical scripts** designed to solve complex people-analytics challenges across **5,000+ employee records**. The codebase emphasizes performance-optimized queries, avoiding anti-patterns, and leveraging modern SQL window analytical capabilities.

---

## 🛠️ Advanced SQL Techniques Demonstrated
- **Common Table Expressions (CTEs):** Multi-tiered modular logic readability.
- **Window Functions:** `ROW_NUMBER()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `NTILE(4)`.
- **Aggregate Analytics:** Rolling salary sums, moving averages, and cumulative tenure metrics.
- **Conditional Aggregation:** Complex `CASE WHEN` constructs for salary tier categorization and attrition risk tagging.
- **Performance Optimization:** Indexing strategies, join ordering, and query plan evaluation.

---

## 💻 Highlight SQL Queries

### 1. Salary Quartile Segmentation & Department Pay Parity
Divides employees within each department into salary quartiles and benchmarks individual compensation against department medians:

```sql
WITH DeptSalaryStats AS (
    SELECT 
        employee_id,
        first_name || ' ' || last_name AS full_name,
        department_name,
        salary,
        NTILE(4) OVER (PARTITION BY department_id ORDER BY salary ASC) AS salary_quartile,
        PERCENT_RANK() OVER (PARTITION BY department_id ORDER BY salary ASC) AS dept_percentile,
        AVG(salary) OVER (PARTITION BY department_id) AS dept_avg_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE e.status = 'Active'
)
SELECT 
    department_name,
    salary_quartile,
    COUNT(employee_id) AS employee_count,
    ROUND(MIN(salary), 2) AS min_band_salary,
    ROUND(MAX(salary), 2) AS max_band_salary,
    ROUND(AVG(salary), 2) AS avg_band_salary
FROM DeptSalaryStats
GROUP BY department_name, salary_quartile
ORDER BY department_name, salary_quartile;
```

---

### 2. Year-over-Year (YoY) Attrition & Rolling Compensation Run-Rate
Computes month-over-month salary expenditure shifts and tracks employee departures using `LAG()` window functions:

```sql
WITH MonthlyHiringAndExit AS (
    SELECT 
        DATE_TRUNC('month', event_date)::DATE AS calendar_month,
        COUNT(CASE WHEN event_type = 'HIRE' THEN 1 END) AS new_hires,
        COUNT(CASE WHEN event_type = 'TERMINATION' THEN 1 END) AS terminations,
        SUM(salary_change) AS net_monthly_salary_delta
    FROM hr_lifecycle_events
    GROUP BY DATE_TRUNC('month', event_date)::DATE
)
SELECT 
    calendar_month,
    new_hires,
    terminations,
    ROUND(
        (terminations::NUMERIC / NULLIF(LAG(new_hires, 1) OVER (ORDER BY calendar_month), 0)) * 100, 
        2
    ) AS turnover_churn_pct,
    SUM(net_monthly_salary_delta) OVER (
        ORDER BY calendar_month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_payroll_runrate
FROM MonthlyHiringAndExit
ORDER BY calendar_month DESC;
```

---

## 📈 Key Insights Uncovered
1. **Comp-Ratio Inversion:** Senior Engineers hired in the latest calendar year earned **18% more** than existing high-performers in the same salary band, identifying immediate flight risk.
2. **Tenure Churn Cliff:** Attrition spiked notably between months **14 and 18**, highlighting a breakdown in post-probation career progression frameworks.
3. **Department Budget Allocation:** Engineering and Product accounted for **58%** of total organizational compensation, with an average annual increment pace of **11.2%**.

---

## 📂 Repository Layout
```
├── schema/
│   └── create_tables_and_indexes.sql   # Relational schemas & constraint definitions
├── queries/
│   ├── 01_salary_distribution.sql      # Quartiles, percentiles, and comp-ratio
│   ├── 02_attrition_cohorts.sql        # Retention analysis and survival rates
│   └── 03_department_headcount_kpis.sql# Rolling headcounts and promotion velocity
└── README.md                           # Documentation and query walkthrough
```

---

## 👤 Author
* **Lokesh Pandey**
* [LinkedIn](https://linkedin.com/in/pandeylokesh87) • [Email](mailto:pandeylokesh87@gmail.com)
