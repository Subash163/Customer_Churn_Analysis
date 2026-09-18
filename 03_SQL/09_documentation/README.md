# Customer Churn Analysis — SQL Project

## Overview

This SQL project is the MySQL implementation of an end-to-end **Customer Churn & Retention Analysis** portfolio project.

The SQL layer takes the cleaned and validated datasets produced during the Python stage and converts them into a structured relational database for:

- data validation
- KPI analysis
- churn-driver analysis
- retention analysis
- business-question analysis
- SQL interview demonstration
- analytical documentation

---

# Project Architecture

```text
sql/
│
├── README.md
│
├── 01_database_design/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_primary_foreign_keys.sql
│   └── 04_indexes.sql
│
├── 02_data_loading/
│   ├── 01_load_customers.sql
│   ├── 02_load_subscriptions.sql
│   ├── 03_load_payments.sql
│   ├── 04_load_customer_services.sql
│   ├── 05_load_support_tickets.sql
│   └── 06_load_data_dictionary.sql
│
├── 03_data_validation/
│   ├── 01_row_counts.sql
│   ├── 02_primary_key_validation.sql
│   ├── 03_null_validation.sql
│   ├── 04_duplicate_validation.sql
│   ├── 05_referential_integrity.sql
│   ├── 06_business_rule_validation.sql
│   └── 07_python_sql_reconciliation.sql
│
├── 04_kpi_analysis/
│   ├── 01_customer_kpis.sql
│   ├── 02_churn_kpis.sql
│   ├── 03_retention_kpis.sql
│   ├── 04_subscription_kpis.sql
│   ├── 05_payment_kpis.sql
│   └── 06_support_kpis.sql
│
├── 05_churn_driver_analysis/
│   ├── 01_lifecycle_churn.sql
│   ├── 02_subscription_churn.sql
│   ├── 03_payment_churn.sql
│   ├── 04_service_churn.sql
│   ├── 05_support_churn.sql
│   ├── 06_engagement_churn.sql
│   ├── 07_customer_profile_churn.sql
│   └── 08_multidimensional_churn.sql
│
├── 06_retention_analysis/
│   ├── 01_retention_by_lifecycle.sql
│   ├── 02_retention_by_plan.sql
│   ├── 03_retention_by_contract.sql
│   ├── 04_retention_by_payment.sql
│   ├── 05_retention_by_service.sql
│   ├── 06_retention_by_support.sql
│   └── 07_high_value_retention.sql
│
├── 07_business_questions/
│   ├── 01_customer_questions.sql
│   ├── 02_churn_questions.sql
│   ├── 03_payment_questions.sql
│   ├── 04_support_questions.sql
│   ├── 05_retention_questions.sql
│   └── 06_management_questions.sql
│
├── 08_interview_queries/
│   ├── 01_joins.sql
│   ├── 02_aggregations.sql
│   ├── 03_case_when.sql
│   ├── 04_subqueries.sql
│   ├── 05_ctes.sql
│   ├── 06_window_functions.sql
│   ├── 07_date_functions.sql
│   ├── 08_advanced_sql.sql
│   └── 09_business_case_queries.sql
│
└── 09_documentation/
    ├── sql_observations.md
    ├── sql_data_dictionary.md
    └── sql_business_questions.md
```

---

# 01 — Database Design

## Purpose

Create a professional relational database structure before loading data.

### Includes

- database creation
- table definitions
- primary keys
- foreign keys
- business-rule checks
- indexes

### Database

```text
customer_churn_analysis
```

### Main tables

```text
customers
subscriptions
payments
customer_services
support_tickets
```

The workbook's `Data_Dictionary` is documentation metadata rather than a business transaction table.

---

# 02 — Data Loading

## Purpose

Load the **cleaned and validated** CSV datasets into MySQL.

The SQL loading scripts use `LOAD DATA LOCAL INFILE`.

Expected cleaned datasets:

```text
customers.csv
subscriptions.csv
payments.csv
customer_services.csv
support_tickets.csv
```

The Data Dictionary is loaded separately for documentation if desired.

### Important

Do not load the raw Excel workbook directly as the final analytical database.

The raw workbook contains duplicates and inconsistent categorical values that were handled during the Python data-cleaning stage.

---

# 03 — Data Validation

## Purpose

Confirm that the SQL database contains the expected validated data.

Validation covers:

- row counts
- primary keys
- duplicates
- NULLs
- foreign keys
- orphan records
- ID formats
- business rules
- category values
- date ranges
- Python-to-SQL reconciliation

### Expected cleaned row counts

| Table | Rows |
|---|---:|
| customers | 20,000 |
| subscriptions | 20,000 |
| payments | 355,437 |
| customer_services | 20,000 |
| support_tickets | 50,000 |

These values should match the final Python validation output.

---

# 04 — KPI Analysis

## Purpose

Establish the core business metrics before deeper analysis.

### Customer KPIs

- total customers
- demographics
- geography
- signup trends

### Churn KPIs

- total churned
- total active
- churn rate
- churn trends
- churn by plan
- churn by contract
- churn by age
- churn by charge

### Retention KPIs

- retention rate
- tenure
- tenure bands
- active vs churned tenure

### Subscription KPIs

- plan mix
- contract mix
- active MRR
- revenue at risk

### Payment KPIs

- payment count
- payment value
- successful payments
- failed payments
- payment success rate
- payment method performance

### Support KPIs

- ticket volume
- resolution rate
- resolution time
- satisfaction
- issue types

---

# 05 — Churn Driver Analysis

## Purpose

Identify customer characteristics and behaviors associated with churn.

Analysis areas:

```text
Lifecycle
Subscription
Payment
Service
Support
Engagement
Customer Profile
Multidimensional Risk
```

The analysis is descriptive and diagnostic.

It does not claim causal relationships.

---

# 06 — Retention Analysis

## Purpose

Understand which customer segments demonstrate stronger observed retention.

Analysis includes:

- lifecycle retention
- plan retention
- contract retention
- payment behavior
- service adoption
- support experience
- high-value customers

### Baseline formula

```text
Retention Rate =
Active Customers / Total Customers × 100
```

---

# 07 — Business Questions

## Purpose

Translate SQL analysis into realistic stakeholder questions.

Examples:

- Which plan has the highest churn?
- Which contract type retains customers best?
- Which payment behavior is associated with higher churn?
- Which support issues are associated with lower retention?
- Which segment has the highest revenue at risk?
- Which high-value customers should receive retention attention?

This layer demonstrates **business thinking**, not just SQL syntax.

---

# 08 — Interview Queries

## Purpose

Demonstrate practical MySQL interview skills.

Topics:

```text
JOINs
Aggregations
CASE WHEN
Subqueries
CTEs
Window Functions
Date Functions
Advanced SQL
Business Cases
```

Important SQL concepts demonstrated include:

- INNER JOIN
- LEFT JOIN
- anti-join
- GROUP BY
- HAVING
- conditional aggregation
- scalar subqueries
- correlated logic
- CTEs
- ROW_NUMBER
- RANK
- LAG
- running totals
- NTILE
- date functions
- customer-level feature engineering

---

# 09 — Documentation

## Purpose

Document the analytical model, observations, data dictionary, business questions, assumptions, and limitations.

Files:

```text
sql_observations.md
sql_data_dictionary.md
sql_business_questions.md
```

---

# Critical SQL Data-Model Lesson

The most important technical issue in this project is the difference between **table grain**.

```text
customers
1 row / customer

subscriptions
1 row / customer

payments
many rows / customer

customer_services
1 row / customer

support_tickets
many rows / customer
```

Therefore, this is dangerous:

```sql
SELECT ...
FROM subscriptions s
JOIN payments p
    ON s.Customer_ID = p.Customer_ID
JOIN support_tickets st
    ON s.Customer_ID = st.Customer_ID;
```

If one customer has:

```text
10 payments
4 support tickets
```

the join can create:

```text
10 × 4 = 40 rows
```

for that customer.

That can make revenue, ticket counts, averages, and churn metrics incorrect.

### Correct approach

```text
payments
    ↓
aggregate to Customer_ID
    ↓
one row/customer

support_tickets
    ↓
aggregate to Customer_ID
    ↓
one row/customer

then join to subscriptions
```

This pattern is used throughout the project.

---

# Recommended Execution Order

Run the SQL project in this order:

```text
01_database_design
        ↓
02_data_loading
        ↓
03_data_validation
        ↓
04_kpi_analysis
        ↓
05_churn_driver_analysis
        ↓
06_retention_analysis
        ↓
07_business_questions
        ↓
08_interview_queries
        ↓
09_documentation
```

Do not skip validation before business analysis.

---

# Recommended Portfolio Story

When presenting this project to a recruiter or interviewer:

### Step 1 — Problem

> The business wants to understand customer churn, retention, and revenue risk.

### Step 2 — Data

Explain the five operational tables and their grain.

### Step 3 — Data quality

Explain how duplicates, inconsistent categories, NULLs, referential integrity, and business rules were validated.

### Step 4 — SQL model

Explain the relational structure and why primary/foreign keys and indexes were introduced.

### Step 5 — KPIs

Show the core churn, retention, subscription, payment, and support metrics.

### Step 6 — Drivers

Explain which customer behaviors or characteristics are associated with churn.

### Step 7 — Retention

Identify segments with stronger or weaker observed retention.

### Step 8 — Business action

Translate the findings into retention, payment, support, product, or customer-success actions.

---

# Interview Talking Points

Be prepared to answer:

### Why did you use MySQL after Python?

> Python was used for data cleaning, validation, transformation, and exploratory analysis. MySQL was then used to reproduce the validated analytical dataset in a relational environment and perform scalable business analysis.

### Why did you use CTEs?

> CTEs make multi-step analytical logic easier to read, validate, and maintain. They were especially useful for creating customer-level payment and support features before joining them to subscription data.

### Why did you aggregate payments first?

> Payments are one-to-many relative to customers. Aggregating first prevents row multiplication and incorrect customer-level metrics.

### What is the difference between churn rate and retention rate?

```text
Churn Rate =
Churned Customers / Total Customers × 100

Retention Rate =
Active Customers / Total Customers × 100
```

For this project's binary active/churned population:

```text
Churn Rate + Retention Rate = 100%
```

### Does correlation prove causation?

No.

The SQL analysis identifies observed associations. Causal conclusions require additional experimentation or statistical methods.

---

# Reproducibility

Queries using `CURDATE()` are dynamic.

For a final portfolio report, use a documented fixed reference date when calculating historical tenure.

Example:

```text
Analysis Reference Date = 2025-10-31
```

This prevents results from changing simply because the query is executed on a different day.

---

# Final Deliverable

The completed SQL project demonstrates:

```text
Data Modeling
      +
Data Loading
      +
Data Validation
      +
SQL Analytics
      +
Churn Analysis
      +
Retention Analysis
      +
Business Thinking
      +
Interview SQL
      +
Documentation
```

This makes the SQL portion a complete analytical workflow rather than a random collection of SQL queries.

---

# Project Completion Checklist

```text
01_database_design          ✅
02_data_loading             ✅
03_data_validation          ✅
04_kpi_analysis             ✅
05_churn_driver_analysis    ✅
06_retention_analysis       ✅
07_business_questions       ✅
08_interview_queries        ✅
09_documentation            ✅
```

**SQL project: COMPLETE**
