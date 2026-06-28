# 📡 Telecom Customer Churn Prediction Pipeline

An end-to-end Azure data engineering pipeline that processes 2 million 
telecom customer records to predict churn risk using PySpark on Databricks.

---

## 🏗️ Architecture

![Architecture](Screenshots/telecom_churn_architecture.png)

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Source | Synthetic Telecom Dataset (2M rows) |
| Ingestion | Azure Data Factory |
| Storage | ADLS Gen2 (Bronze/Silver/Gold) |
| Processing | Azure Databricks (PySpark) |
| Warehouse | Azure SQL Database |
| Visualization | Power BI Desktop (6 pages) |
| Orchestration | ADF Pipeline with daily trigger |

---

## 📊 Dashboard Screenshots

### Page 1 — Executive Overview
![Overview](Screenshots/page1_overview.png)

### Page 2 — Churn Deep Dive
![Deep Dive](Screenshots/page2_churn_deepdive.png)

### Page 3 — Financial Impact
![Financial](Screenshots/page3_financial_impact.png)

### Page 4 — Customer Segmentation
![Segments](Screenshots/page4_customer_segments.png)

### Page 5 — Retention Action Plan
![Retention](Screenshots/page5_retention_plan.png)

### Page 6 — Pipeline Summary
![Pipeline](Screenshots/page6_pipeline_summary.png)

---

## 🔍 Churn Risk Signals Discovered

| Signal | Condition | Weight |
|---|---|---|
| Contract Type | Month-to-month | 35 points |
| Tenure | Less than 18 months | 25 points |
| Monthly Charges | Greater than $74 | 20 points |
| Billing Spike | Max bill > 2x average | 20 points |

---

## 📈 Key Results

- **2,000,000** customer records processed
- **834,842** high risk customers identified (41.7%)
- **$25.73M** monthly revenue at risk
- **34.6%** overall churn rate
- **343K** customers with critical risk score ≥ 80

---

## 🗂️ Project Structure
telecom-churn-project/

├── Screenshots/

│   ├── page1_overview.png

│   ├── page2_churn_deepdive.png

│   ├── page3_financial_impact.png

│   ├── page4_customer_segments.png

│   ├── page5_retention_plan.png

│   ├── page6_pipeline_summary.png

│   └── telecom_churn_architecture.png

├── PowerBI DashBoard/

│   └── churn_dashboard.pbix

├── notebooks/

│   └── churn_transform.ipynb

├── scripts/

│   ├── split_data.py

│   └── generate_data.py

├── config/

│   └── config_sample.py

├── requirement.txt

└── README.md
---

## 🚀 Pipeline Steps

### 1. Data Generation
```python
# Generate 2 million synthetic telecom customers
N = 2_000_000
# Outputs: customer_profile.csv, billing_data.csv, cdr_simulation.csv
python scripts/generate_data.py
```

### 2. Bronze Layer (ADLS Gen2)
- Raw CSV files uploaded to `bronze` container
- No transformation — raw data preserved

### 3. Silver Layer (Databricks)
- Cast data types
- Remove duplicates and nulls
- Standardise categorical values

### 4. Gold Layer (Databricks)
- Join 3 silver tables on `customer_id`
- Engineer churn risk score (0-100 points)
- Classify into High / Medium / Low risk labels

### 5. Azure SQL Database
- Gold table loaded via JDBC
- `fact_churn_signals` table with 2M rows

### 6. Power BI Dashboard
- 6-page interactive dashboard
- Connected to Azure SQL Database
- DAX measures for dynamic KPIs

---

## ⚙️ ADF Pipeline

- Pipeline: `pl_telecom_churn`
- Activity: Databricks Notebook
- Trigger: Daily at 2:00 AM
- Linked services: ADLS Gen2, Azure SQL, Databricks

---

## 💡 Key Learnings

- Medallion architecture (Bronze/Silver/Gold) for data lake design
- PySpark DataFrame operations at scale (2M rows)
- Feature engineering without ML models using domain knowledge
- DAX measures for dynamic KPI calculations in Power BI
- Azure cloud resource management within student credit limits

---

## 🎯 Interview Prep

### Q: Why medallion architecture?
Bronze preserves raw data for reprocessing. Silver ensures clean typed data. Gold contains business-ready aggregations. Each layer serves a different consumer with different quality requirements.

### Q: Why PySpark over pandas?
2 million rows is manageable in pandas but PySpark scales to billions. Using Spark demonstrates production-ready thinking and the ability to handle enterprise data volumes.

### Q: Why these 4 churn signals?
Discovered through manual EDA — month-to-month customers have no switching cost, short tenure customers have not built loyalty, high charges create value perception issues, and billing spikes cause immediate dissatisfaction.

### Q: How does ADF orchestrate the pipeline?
A Databricks Notebook Activity triggers the PySpark transformation after source files land in ADLS bronze. A schedule trigger runs this daily at 2 AM automatically.

---

## 👤 Author

**Vikas Mehta**
Data Engineering Project | Azure | Databricks | PySpark | Power BI

[![GitHub](https://img.shields.io/badge/GitHub-vikasmehta1921-black?logo=github)](https://github.com/vikasmehta1921)
