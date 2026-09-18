# SQL Observations — Customer Churn Analysis

## 1. Purpose

The SQL stage recreates and extends the validated customer churn analysis in MySQL using a production-style relational database.

The objective is to demonstrate that the analysis can be reproduced from structured relational data rather than relying only on Python or Excel.

---

## 2. Analytical grain

| Table | Analytical grain | Main key |
|---|---|---|
| customers | One row per customer | Customer_ID |
| subscriptions | One row per customer subscription | Subscription_ID |
| payments | One row per payment transaction | Payment_ID |
| customer_services | One row per customer | Customer_ID |
| support_tickets | One row per support ticket | Ticket_ID |

The cleaned analytical dataset contains one subscription per customer, making `subscriptions` the primary anchor for churn and retention analysis.

---

## 3. Core analytical principle

The most important SQL modeling rule in this project is:

> Aggregate one-to-many tables to customer level before joining them to customer-level tables.

`payments` and `support_tickets` both contain multiple rows per customer.

A direct join such as:

```text
subscriptions
    JOIN payments
    JOIN support_tickets
```

can produce:

```text
1 customer × many payments × many tickets
```

This artificially multiplies rows and can corrupt:

- customer counts
- churn counts
- payment totals
- support metrics
- averages
- churn rates
- revenue calculations

The SQL implementation therefore uses CTEs and customer-level aggregation before combining these tables.

---

## 4. SQL project progression

The project follows a professional analytical workflow:

```text
Database Design
      ↓
Data Loading
      ↓
Data Validation
      ↓
KPI Analysis
      ↓
Churn Driver Analysis
      ↓
Retention Analysis
      ↓
Business Questions
      ↓
Interview Queries
      ↓
Documentation
```

---

## 5. Database design observations

The database uses:

- MySQL 8.x
- InnoDB
- UTF-8 (`utf8mb4`)
- primary keys
- foreign keys
- business-rule checks
- analytical indexes

`Data_Dictionary` is treated as documentation metadata rather than a business transaction table.

The operational schema contains five business tables:

1. customers
2. subscriptions
3. payments
4. customer_services
5. support_tickets

---

## 6. Data loading observations

The SQL loading layer is designed to load the cleaned/validated CSV exports produced during the Python data-cleaning stage.

The raw Excel workbook should not be treated as the final production database because the raw workbook contains duplicates and inconsistent categorical values.

Expected cleaned row counts used for SQL validation are:

| Table | Expected cleaned rows |
|---|---:|
| customers | 20,000 |
| subscriptions | 20,000 |
| payments | 355,437 |
| customer_services | 20,000 |
| support_tickets | 50,000 |

These counts should be reconciled against the final Python validation output before business analysis.

---

## 7. Validation observations

The validation layer checks:

- row counts
- primary-key nulls
- primary-key uniqueness
- duplicate records
- ID formats
- NULL values
- foreign-key integrity
- customer coverage
- business-rule validity
- category distributions
- date ranges
- Python-to-SQL reconciliation

Validation should be completed before interpreting KPI or churn results.

---

## 8. KPI observations

The KPI layer covers:

### Customer KPIs
- customer count
- age statistics
- gender distribution
- geography
- signup trends

### Churn KPIs
- active customers
- churned customers
- churn rate
- churn by plan
- churn by contract
- churn by charge band
- churn trend

### Retention KPIs
- retention rate
- tenure
- active vs churned tenure
- tenure bands

### Subscription KPIs
- plan mix
- contract mix
- MRR
- revenue at risk

### Payment KPIs
- payment volume
- payment value
- successful payments
- failed payments
- payment success rate
- payment-method performance

### Support KPIs
- ticket volume
- resolution rate
- resolution time
- satisfaction
- issue-type performance

---

## 9. Churn-driver observations

The churn-driver layer investigates relationships between churn and:

- lifecycle/tenure
- subscription plan
- contract type
- monthly charge
- payment failures
- payment methods
- service adoption
- support ticket volume
- unresolved tickets
- satisfaction
- issue types
- customer demographics
- geography
- combined risk signals

The analysis is descriptive.

A segment with higher churn is an observed association, not proof of causality.

---

## 10. Retention observations

Retention is primarily defined as:

```text
Retention Rate =
Active Customers / Total Customers × 100
```

Retention is analyzed by:

- lifecycle
- plan
- contract
- payment behavior
- service adoption
- support experience
- customer value

High-value customers are defined in the SQL interview/business analysis as the top quartile of monthly charge unless a business-defined revenue threshold is provided.

---

## 11. Business-question observations

The SQL project translates technical analysis into stakeholder questions.

Examples:

- Which plan has the highest churn?
- Which contract type retains customers best?
- Where is monthly revenue at risk highest?
- Do failed payments correspond with higher churn?
- Does support experience differ between active and churned customers?
- Which service-adoption level has the strongest retention?
- Which customer segments deserve retention intervention?
- Which high-value active customers show multiple risk signals?

This is important because a Data Analyst should not stop at producing SQL results. The analysis should support a business decision.

---

## 12. Interview SQL observations

The interview-query layer demonstrates:

- JOINs
- aggregations
- GROUP BY
- HAVING
- CASE WHEN
- conditional aggregation
- subqueries
- CTEs
- window functions
- ranking
- ROW_NUMBER
- LAG
- running totals
- date functions
- customer-level feature engineering
- business-case SQL

The strongest interview answers should explain both the SQL mechanics and the business reason for using them.

---

## 13. Reproducibility note

For historical portfolio reporting, avoid relying on `CURDATE()` when calculating active-customer tenure if the result needs to remain unchanged.

Instead, define and document a fixed analysis reference date, such as:

```text
Project End Date = 2025-10-31
```

or another date justified by the final validated dataset.

This makes the analysis reproducible.

---

## 14. Limitations

### 14.1 Observational analysis
The data supports descriptive and diagnostic analysis, not causal inference.

### 14.2 No explicit engagement table
The source workbook does not contain a separate engagement table.

Engagement is therefore approximated from:

- successful payment activity
- service adoption
- support activity

### 14.3 Retention definition
The baseline retention metric uses active customers divided by the customer base. More advanced cohort retention can be developed if customer-period history is available.

### 14.4 Historical activity
Payment and support activity are transaction records. They should not automatically be interpreted as product usage or customer satisfaction without appropriate context.

### 14.5 Small segments
Very small segments can show unstable churn or retention percentages. Segment volume should always be considered alongside rates.

### 14.6 Current-date dependency
Queries using `CURDATE()` change over time. A fixed reporting date is preferable for a final portfolio snapshot.

---

## 15. Recommended business interpretation

When evaluating a churn driver, consider all three:

```text
Churn Rate
    +
Churned Customer Volume
    +
Revenue at Risk
```

A high churn rate alone does not necessarily indicate the highest business priority.

---

## 16. Final SQL takeaway

This project demonstrates a complete analyst workflow:

```text
Reliable data
   ↓
Correct relational model
   ↓
Validated SQL dataset
   ↓
Business KPIs
   ↓
Driver analysis
   ↓
Retention analysis
   ↓
Business questions
   ↓
Actionable insights
```

The goal is not simply to demonstrate that SQL queries can be written.

The goal is to demonstrate that SQL can be used to produce **reliable, validated, business-oriented analysis**.
