# Final Customer Dataset Observations

## Project

**Customer Churn & Retention Analysis**

---

# Objective

Build the **single source of truth** analytical dataset by integrating all cleaned and aggregated datasets into one customer-level table.

---

# Final Data Model

```text
Customers
    │
    ├── Churn Processing
    │
    ├── Customer Services
    │
    ├── Payment Aggregation
    │
    └── Support Aggregation
            │
            ▼
Final Customer Analytical Dataset
```

---

# Merge Strategy

| Dataset             | Join Type  |
| ------------------- | ---------- |
| Customers           | Base Table |
| Churn               | Left Join  |
| Customer Services   | Left Join  |
| Payment Aggregation | Left Join  |
| Support Aggregation | Left Join  |

---

# Dataset Summary

| Metric              |  Value |
| ------------------- | -----: |
| Customers           | 20,000 |
| Final Rows          | 20,000 |
| Final Columns       |     86 |
| Duplicate Customers |      0 |
| Unique Customer IDs | 20,000 |

---

# Support Coverage

| Metric                    |  Value |
| ------------------------- | -----: |
| Customers with Tickets    | 18,349 |
| Customers without Tickets |  1,651 |

Missing support values were expected and retained because those customers never contacted support.

---

# Data Integrity

| Validation            | Result |
| --------------------- | ------ |
| Customer IDs Unique   | PASS   |
| Duplicate Rows        | PASS   |
| Merge Consistency     | PASS   |
| Referential Integrity | PASS   |

---

# Why This Dataset Matters

This dataset becomes the foundation for:

* Feature Engineering
* Exploratory Data Analysis
* Predictive Modeling
* Power BI Dashboard
* Business Reporting

---

# Key Observations

### 1. One Customer = One Row

The final analytical grain is maintained throughout the project.

### 2. Transaction Tables Were Not Directly Joined

Payments and support tickets were aggregated first to prevent row duplication.

### 3. Customer Services Became Behavioral Features

Binary service adoption variables enrich customer profiling without increasing dataset granularity.

### 4. Support Data Is Optional

Customers without support tickets remain valid analytical records.

---

# Recruiter Highlights

* Designed a dimensional customer-level analytical model.
* Integrated multiple relational datasets into one reproducible analytical table.
* Preserved analytical grain during all joins.
* Created a reusable dataset suitable for BI and machine learning.

---

**Pipeline Stage:** Data Integration → Customer Analytical Dataset
