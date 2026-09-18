# Churn Processing Observations

## Project

**Customer Churn & Retention Analysis**

---

# Objective

Convert the subscription table into a customer-level churn dataset by deriving business-ready churn indicators, tenure metrics, and churn timeline features.

---

# Input Dataset

| Dataset                    |   Rows | Columns |
| -------------------------- | -----: | ------: |
| subscriptions_cleaned.xlsx | 20,000 |       9 |

**Analytical Grain:** One row = One customer

---

# Business Logic

Churn was **not available as a separate dataset**. It was derived from the subscription data using the following rules:

| Condition                               | Customer Status    |
| --------------------------------------- | ------------------ |
| `churn_status = Churned`                | Churned Customer   |
| `churn_status = Active`                 | Active Customer    |
| Churned customer with `churn_date`      | Historical churn   |
| Active customer with blank `churn_date` | Currently retained |

---

# Churn Metrics Created

* is_churned
* is_active
* has_churn_date
* has_end_date
* tenure_days
* tenure_months
* tenure_years
* tenure_at_churn
* churn_year
* churn_month
* churn_quarter
* churn_timing_segment

---

# Processing Results

| Metric              |      Value |
| ------------------- | ---------: |
| Customers Processed |     20,000 |
| Churned Customers   |      4,463 |
| Active Customers    |     15,537 |
| Churn Rate          | **22.31%** |
| Active Rate         | **77.69%** |

---

# Validation Summary

| Check          | Result   |
| -------------- | -------- |
| Total Checks   | 14       |
| Passed         | 10       |
| Failed         | **0**    |
| Overall Status | **PASS** |

---

# Key Observations

### 1. Customer-Level Churn Dataset

The churn layer preserves exactly one record per customer, making it suitable for machine learning and business analytics.

### 2. Churn Rate

The company currently experiences a **22.31% customer churn rate**, meaning approximately **1 in every 5 customers** has discontinued their subscription.

### 3. Active Customer Base

More than **77% of customers remain active**, providing a strong retention population for comparison against churned customers.

### 4. Tenure Metrics

Customer tenure was calculated in **days, months, and years**, allowing future analysis of retention by customer lifecycle.

### 5. Churn Timeline

Year, month, quarter, and timing segments were generated to support seasonal churn analysis and trend reporting.

---

# Data Quality Notes

* No duplicate customers created.
* No customer records removed.
* Churn indicators are internally consistent.
* Customer IDs remained unique after processing.

---

# Recruiter Highlights

* Designed customer-level churn logic from transactional subscription data.
* Created business-ready churn KPIs rather than relying on raw fields.
* Built reusable tenure and lifecycle features for downstream analytics.
* Validated the churn layer with an automated QA framework before feature engineering.

---

**Pipeline Stage:** Data Cleaning → Churn Processing → Validation → Feature Engineering
