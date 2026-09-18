# Interview Queries — SQL Observations

## 1. Objective

The `08_interview_queries.sql` module is a consolidated SQL interview-practice script built on the Customer Churn & Retention Analysis database.

The purpose of this module is to demonstrate practical knowledge of:

* JOINs
* Aggregations
* `CASE WHEN`
* Subqueries
* Common Table Expressions (CTEs)
* Window Functions
* Date Functions
* Advanced SQL techniques

The queries are designed for **SQL skill demonstration and interview preparation** and do not intentionally modify the source tables.

Unlike the KPI, Churn Driver, Retention, and Business Questions modules, this file is primarily focused on demonstrating **SQL problem-solving ability** rather than producing a formal business analysis.

---

# 2. Interview Skill Coverage

The interview queries are organized into eight modules:

| Module    | SQL Skill               | Queries |
| --------- | ----------------------- | ------: |
| 01        | JOINs                   |       6 |
| 02        | Aggregations            |       6 |
| 03        | CASE WHEN               |       5 |
| 04        | Subqueries              |       5 |
| 05        | CTEs                    |       4 |
| 06        | Window Functions        |       6 |
| 07        | Date Functions          |       6 |
| 08        | Advanced SQL            |       7 |
| **Total** | **Core + Advanced SQL** |  **45** |

The file therefore provides broad coverage of the SQL concepts expected from an entry-to-intermediate Data Analyst candidate.

---

# 3. Module 01 — JOINs

## Queries Covered

The JOIN module demonstrates:

1. `INNER JOIN` between customers and subscriptions.
2. `LEFT JOIN` to retain customers with no support tickets.
3. Joining customers, subscriptions, and services.
4. Identifying customers who have never raised a support ticket.
5. Identifying customers with at least one failed payment.
6. Safely combining multiple one-to-many datasets at customer level.

## Key SQL Concepts Demonstrated

### INNER JOIN

The first query demonstrates how to combine customer information with subscription information using `Customer_ID`.

This is useful when the analyst only wants records that have matching records in both tables.

### LEFT JOIN

The second query demonstrates an important analytical pattern:

> Keep all customers even when a related record does not exist.

This is particularly useful for questions such as:

* Customers with no support tickets.
* Customers with no payments.
* Customers without a particular activity.

### Anti-Join Pattern

The fourth query uses:

```sql
LEFT JOIN ...
WHERE related_table.Customer_ID IS NULL
```

This is a common interview pattern for finding records that **do not have a matching record**.

### DISTINCT

The failed-payment query uses `DISTINCT` because payments are a one-to-many relationship.

Without `DISTINCT`, a customer with multiple failed payments would appear multiple times.

### Safe One-to-Many Joining

The sixth query is especially important.

Payments and support tickets are both one-to-many tables relative to customers. Joining them directly can produce row multiplication.

The query therefore aggregates payments and support tickets separately to customer level before joining them to subscriptions.

### Interview Insight

A strong interview explanation would be:

> "When joining multiple one-to-many tables, I aggregate each table to the required grain before joining to avoid fan-out and inflated metrics."

This is one of the most valuable technical concepts demonstrated in the project.

---

# 4. Module 02 — Aggregations

## Queries Covered

The aggregation module demonstrates:

* `COUNT`
* `COUNT(DISTINCT ...)`
* `SUM`
* `AVG`
* `MIN`
* `MAX`
* `GROUP BY`
* `HAVING`
* Aggregation by payment status
* Aggregation by support issue type

## Key Observations

### Basic Aggregation

The first query demonstrates multiple aggregate functions in a single query.

This is a fundamental SQL interview skill.

### GROUP BY

The plan-level query demonstrates how to calculate churn performance separately for each subscription plan.

### HAVING

The third query demonstrates the difference between `WHERE` and `HAVING`.

`WHERE` filters rows before aggregation.

`HAVING` filters groups after aggregation.

For example:

```sql
HAVING COUNT(*) >= 5000
```

means:

> Return only plans whose aggregated customer count is at least 5,000.

### Payment Aggregation

Payment status aggregation demonstrates how transactional data can be summarized into:

* Number of payments.
* Total payment value.
* Average payment amount.

### Support Aggregation

Support issue aggregation demonstrates grouping operational activity by issue type.

This provides a practical example of converting ticket-level data into management-level metrics.

---

# 5. Module 03 — CASE WHEN

## Queries Covered

The `CASE WHEN` module demonstrates:

1. Age-band classification.
2. Monthly-charge classification.
3. Rule-based churn-risk labeling.
4. Conditional aggregation.
5. Support-ticket priority classification.

## Key SQL Concepts

### Creating Business Categories

The age query converts numeric age into meaningful business segments:

* 18–24
* 25–34
* 35–44
* 45–54
* 55–64
* 65–75
* Unknown

This demonstrates how analysts transform raw numerical data into analytical dimensions.

### Handling NULL

The age query explicitly checks:

```sql
WHEN Age IS NULL THEN 'Unknown'
```

This is important because missing values should not automatically be forced into an incorrect category.

### Pricing Bands

Monthly charge is converted into pricing bands.

This is useful for:

* Customer segmentation.
* Revenue analysis.
* Risk segmentation.

### Rule-Based Churn Risk

The churn-risk query combines payment and support characteristics to create:

* High Risk
* Medium Risk
* Low Risk

The rules use failed payments, unresolved tickets, and satisfaction.

### Important Limitation

This is a **business-rule classification**, not a statistically validated churn prediction model.

It should therefore be described as:

> Rule-based churn-risk labeling.

Not:

> Machine-learning churn prediction.

### Conditional Aggregation

The fourth query demonstrates a highly common interview pattern:

```sql
SUM(CASE WHEN ... THEN 1 ELSE 0 END)
```

This is useful for calculating multiple conditional metrics in a single query.

---

# 6. Module 04 — Subqueries

## Queries Covered

The subquery module demonstrates:

1. Customers paying above the overall average monthly charge.
2. Plans with churn above the overall churn rate.
3. Customers whose payment value is above the average customer payment value.
4. Customers with more support tickets than the average customer.
5. Customers with the maximum monthly charge within their plan.

## Key SQL Concepts

### Scalar Subquery

The first query uses:

```sql
WHERE Monthly_Charge > (
    SELECT AVG(Monthly_Charge)
    FROM subscriptions
)
```

This demonstrates comparing individual records against a calculated overall benchmark.

### Group-Level Comparison

The second query compares each plan's churn rate against the overall churn rate.

This is a useful interview problem because it requires understanding the difference between:

* Row-level values.
* Group-level aggregates.
* Overall benchmark values.

### Customer-Level Aggregation Before Comparison

The payment-value query first creates customer-level totals and then compares each customer against the average customer payment value.

This demonstrates how the correct analytical grain can be established before applying a benchmark.

### Correlated Subquery

The final query uses a correlated subquery to identify the maximum monthly charge **within each plan**.

This is a classic interview question.

The important concept is that the subquery depends on the outer query's `Plan`.

---

# 7. Module 05 — CTEs

## Queries Covered

The CTE module demonstrates:

1. Plan-level churn summary using a CTE.
2. Multi-CTE customer risk profile.
3. Identifying the highest-churn plan.
4. Monthly churn trend using a CTE.

## Key SQL Concepts

### CTE for Readability

The first query separates aggregation logic from final presentation.

This makes the query easier to read and maintain.

### Multi-CTE Design

The second query creates separate feature tables for:

* Payment behavior.
* Support behavior.
* Customer subscription information.

These are then combined into a customer-level profile.

This demonstrates practical SQL transformation architecture.

### CTE + Subquery

The highest-churn-plan query demonstrates how a CTE can create an intermediate analytical result and then use it in another operation.

### Monthly Trend

The fourth query demonstrates using a CTE to create a monthly churn summary before presenting the final ordered result.

---

# 8. Module 06 — Window Functions

## Queries Covered

The window-function module demonstrates:

1. Ranking plans by churn rate.
2. Ranking customers within each plan.
3. Finding the top three customers in each plan.
4. Comparing plan churn against average plan churn.
5. Calculating cumulative payment value.
6. Calculating month-over-month payment growth.

## Key SQL Concepts

### RANK()

The first query ranks plans according to churn rate.

This demonstrates how ranking differs from simple sorting.

### PARTITION BY

The second query ranks customers independently within each plan.

```sql
PARTITION BY Plan
```

means the ranking restarts for every plan.

This is an extremely common interview concept.

### ROW_NUMBER()

The third query identifies the top three customers within each plan.

The use of:

```sql
ORDER BY Monthly_Charge DESC, Customer_ID
```

also provides a deterministic tie-breaker.

### Window Average

The fourth query calculates the average churn rate across plans without collapsing the plan-level rows.

This demonstrates the key difference between:

* Aggregate functions with `GROUP BY`.
* Window functions.

### Running Total

The fifth query uses:

```sql
SUM(payment_value) OVER (...)
```

to calculate cumulative payment value.

This is a common business analytics requirement.

### LAG()

The sixth query uses `LAG()` to retrieve the previous month's payment value.

This enables:

* Month-over-month comparison.
* Growth calculations.
* Trend analysis.

The query also uses `NULLIF` to protect against division by zero.

### Interview Insight

A strong explanation is:

> "Window functions allow me to calculate rankings, comparisons, and cumulative metrics while retaining the original row-level or group-level detail."

---

# 9. Module 07 — Date Functions

## Queries Covered

The date-function module demonstrates:

1. Extracting signup year and month.
2. Monthly customer acquisition trend.
3. Calculating customer tenure in months.
4. Average tenure by churn status.
5. Monthly churn trend.
6. Customers who churned within six months.

## Key SQL Concepts

### YEAR() and MONTH()

These functions demonstrate extracting calendar components from datetime fields.

### DATE_FORMAT()

`DATE_FORMAT()` is used to create a monthly analytical label such as:

```text
YYYY-MM
```

This is useful for trend analysis and grouping.

### TIMESTAMPDIFF()

The tenure queries demonstrate calculating the difference between dates in months.

### GREATEST()

The use of:

```sql
GREATEST(0, ...)
```

prevents negative tenure values.

### Early Churn Identification

The final query identifies customers who churned within six months of starting.

This is a useful practical churn-analysis problem.

---

# 10. Important Date-Function Caveat

The interview file currently contains:

```sql
COALESCE(Churn_Date, CURDATE())
```

for active-customer tenure calculations.

This is technically valid SQL, but it introduces a **dynamic-date issue** for this project.

The broader project uses a fixed analytical cutoff of:

**2025-12-26**

for historical tenure analysis.

Using `CURDATE()` causes active-customer tenure to change depending on when the query is executed.

### Interview Perspective

This is actually useful interview discussion material.

You can explain:

> "For a live operational dashboard, CURDATE() may be appropriate. For a reproducible historical analysis, I would use a fixed analytical cutoff date."

For this project, the fixed cutoff is preferable when comparing historical results.

### Recommended Documentation Note

The interview query can remain as an interview-practice example, but the observation file should explicitly mention that **date-dependent outputs are not intended to be identical to the fixed-cutoff analytical modules**.

---

# 11. Module 08 — Advanced SQL

## Queries Covered

The advanced module demonstrates:

1. Duplicate detection.
2. Customers with both payment and support risk.
3. Most frequently used payment method.
4. Customers above their state's average ticket count.
5. Revenue contribution by plan.
6. Support activity after the last successful payment.
7. Retention rate by state with a minimum population threshold.

---

# 12. Duplicate Detection

The first advanced query uses:

```sql
GROUP BY Customer_ID
HAVING COUNT(*) > 1
```

to identify duplicate customer IDs.

This is a fundamental data-quality interview question.

Because `Customer_ID` is the primary key in the production table, the expected analytical result should be empty after successful database validation.

The query nevertheless demonstrates that the candidate understands how to identify duplicates using SQL.

---

# 13. Multi-Factor Customer Risk

The second advanced query identifies customers who have:

* At least one failed payment.
* At least one unresolved support ticket.

It uses separate CTEs to aggregate payment and support risk before joining them.

This demonstrates:

* CTEs.
* Aggregation.
* JOINs.
* `COALESCE`.
* Multi-condition filtering.

It is a strong example of combining multiple behavioral datasets without directly joining raw one-to-many tables.

---

# 14. Primary Payment Method

The third advanced query determines each customer's most frequently used payment method.

The approach is:

1. Count payments by customer and payment method.
2. Rank payment methods within each customer.
3. Select `ROW_NUMBER() = 1`.

This is an excellent practical example of combining:

**GROUP BY + CTE + Window Function**

to solve a customer-level ranking problem.

### Important Detail

The query uses:

```sql
ORDER BY method_count DESC, Payment_Method
```

The second ordering condition provides a deterministic tie-breaker.

If two methods have the same frequency, the alphabetically earlier method will be selected.

Therefore, this should be understood as:

> Most frequently used payment method, with a deterministic tie-break rule.

---

# 15. State-Level Support Benchmarking

The fourth advanced query compares each customer's ticket count against the average ticket count for their state.

The query uses two stages:

### Stage 1

Calculate ticket count for every customer.

### Stage 2

Calculate average ticket count by state.

### Stage 3

Join the two results and retain customers above their state's average.

This demonstrates an important analytical pattern:

> **Compare individual customer behavior against a peer-group benchmark.**

This is highly relevant to real-world customer analytics.

---

# 16. Revenue Contribution by Plan

The fifth advanced query calculates each plan's share of the total monthly charge base.

The query uses a window function:

```sql
SUM(SUM(Monthly_Charge)) OVER ()
```

to calculate the overall total while retaining plan-level grouping.

This demonstrates advanced understanding of:

* Aggregation.
* Nested aggregation.
* Window functions.
* Percentage-of-total calculations.

This is a strong interview example because percentage-of-total calculations are common in business analytics.

---

# 17. Support After Last Successful Payment

The sixth advanced query identifies customers whose most recent support ticket occurred after their most recent successful payment.

The query independently calculates:

* Last successful payment.
* Last support ticket.

It then compares the two dates.

This demonstrates practical event-sequence analysis.

It can be useful for questions such as:

* Did the customer contact support after their last successful payment?
* Is support activity occurring after payment activity stopped?
* Are customers showing possible payment-related service concerns?

### Important Interpretation

The query identifies an **event sequence**, not necessarily a causal relationship.

A support ticket occurring after the last successful payment does not automatically mean the support interaction caused the payment interruption.

---

# 18. State-Level Retention Benchmarking

The final query calculates retention rate by state while applying:

```sql
HAVING COUNT(*) >= 100
```

This demonstrates a practical approach to avoiding unstable results from very small groups.

The query calculates:

* Customer population.
* Active customers.
* Retention rate.

This is a useful example of geographic segmentation with a minimum sample-size threshold.

---

# 19. Major SQL Skills Demonstrated

Across the complete interview file, the project demonstrates the following progression:

### Beginner / Core SQL

* `SELECT`
* `WHERE`
* `DISTINCT`
* `COUNT`
* `SUM`
* `AVG`
* `MIN`
* `MAX`
* `GROUP BY`
* `HAVING`
* `ORDER BY`
* `LIMIT`

### Intermediate SQL

* `INNER JOIN`
* `LEFT JOIN`
* Multiple-table joins
* `CASE WHEN`
* Conditional aggregation
* Subqueries
* CTEs
* `COALESCE`
* `NULLIF`
* Date functions

### Advanced SQL

* `RANK()`
* `ROW_NUMBER()`
* `LAG()`
* `PARTITION BY`
* Running totals
* Percentage-of-total calculations
* Peer-group benchmarking
* Multi-CTE feature construction
* One-to-many join protection
* Event-sequence analysis
* Correlated subqueries

---

# 20. Most Interview-Important Queries

Although all 45 queries demonstrate useful skills, several are particularly valuable for interview preparation.

## High Priority

### 1. Safe one-to-many JOIN

Demonstrates understanding of row multiplication and analytical grain.

### 2. Conditional aggregation

Demonstrates practical use of `CASE WHEN`.

### 3. Correlated subquery

Demonstrates advanced subquery understanding.

### 4. Multi-CTE customer profile

Demonstrates structured analytical SQL.

### 5. Top 3 customers per plan

Demonstrates `ROW_NUMBER()` and `PARTITION BY`.

### 6. Month-over-month payment growth

Demonstrates `LAG()` and window functions.

### 7. Primary payment method

Demonstrates aggregation + ranking + CTEs.

### 8. Revenue contribution by plan

Demonstrates percentage-of-total calculation.

### 9. State-level peer benchmarking

Demonstrates customer-level versus group-level comparison.

### 10. Support-after-payment analysis

Demonstrates temporal/event-sequence reasoning.

---

# 21. Important Analytical Concepts Demonstrated

## Analytical Grain

A major strength of the interview SQL is the use of customer-level aggregation before combining one-to-many datasets.

For example:

* Payments → customer level.
* Support tickets → customer level.
* Services → customer level.
* Subscriptions → customer level.

This prevents incorrect calculations caused by row multiplication.

---

## NULL Handling

The queries demonstrate:

* `COALESCE`
* Explicit `NULL` handling.
* `CASE WHEN ... IS NULL`
* `NULLIF`

These are important skills because real-world datasets frequently contain missing values.

---

## Deterministic Results

Several ranking queries include tie-breaking fields such as `Customer_ID` or `Payment_Method`.

This is good practice because it makes results reproducible when values are tied.

---

## Business Logic in SQL

The project does not use SQL merely for data extraction.

SQL is also used to create:

* Risk categories.
* Age bands.
* Pricing bands.
* Support priorities.
* Customer benchmarks.
* Retention metrics.
* Revenue contribution.
* Behavioral profiles.

This demonstrates the ability to translate business questions into SQL logic.

---

# 22. Important Caveats

## 1. Rule-Based Risk Is Not Predictive Modeling

The `CASE WHEN` churn-risk label and other risk frameworks are business-rule classifications.

They are not statistically validated predictive models.

---

## 2. CURDATE() Creates Dynamic Results

The tenure queries using `CURDATE()` will change as time passes.

For reproducible historical analysis, the project should use the fixed analytical cutoff where appropriate.

---

## 3. Payment and Support Tables Are One-to-Many

Directly joining raw payment and support records to subscriptions can inflate customer-level metrics.

The interview file appropriately demonstrates aggregation-first techniques in several queries.

---

## 4. Correlation Is Not Causation

Queries identifying payment or support patterns around churn demonstrate associations or event sequences.

They do not prove causal relationships.

---

## 5. Minimum Population Thresholds

Queries using thresholds such as:

```sql
HAVING COUNT(*) >= 100
```

are designed to avoid over-interpreting very small segments.

This is good analytical practice.

---

# 23. Interview Questions This File Prepares You For

This module gives practical preparation for questions such as:

### JOIN Questions

* What is the difference between INNER JOIN and LEFT JOIN?
* How do you find customers with no transactions?
* How do you avoid duplicate rows when joining multiple one-to-many tables?
* How would you join three or more tables?

### Aggregation Questions

* What is the difference between WHERE and HAVING?
* How do you calculate churn rate?
* How do you calculate conditional counts?
* How do you calculate percentage contribution?

### CASE WHEN Questions

* How do you create age groups?
* How do you categorize customers into risk bands?
* How do you handle NULL values?

### Subquery Questions

* How do you find customers above average?
* How do you find the maximum value within each group?
* What is a correlated subquery?

### CTE Questions

* What is a CTE?
* Why would you use a CTE instead of a subquery?
* Can you use multiple CTEs?
* How would you construct a customer feature table?

### Window Function Questions

* Difference between RANK and ROW_NUMBER?
* What does PARTITION BY do?
* How do you find the top N customers per group?
* How do you calculate a running total?
* How do you calculate month-over-month growth?
* How does LAG work?

### Date Questions

* How do you calculate tenure?
* How do you group records by month?
* How do you identify early churn?
* How do you calculate monthly trends?

### Advanced SQL Questions

* How do you identify duplicates?
* How do you identify a customer's primary payment method?
* How do you compare a customer against their peer group?
* How do you identify events occurring after another event?
* How do you calculate percentage contribution by category?

---

# 24. Overall Assessment

The interview SQL module demonstrates a solid progression from fundamental SQL to advanced analytical SQL.

The strongest aspect is that the queries are not isolated textbook examples. They use the actual Customer Churn & Retention Analysis schema and address realistic analytical scenarios involving:

* Customers.
* Subscriptions.
* Payments.
* Services.
* Support tickets.
* Churn.
* Retention.
* Revenue.
* Customer risk.

This makes the SQL portfolio more credible than a collection of generic interview exercises.

---

# 25. Recommended Interview Positioning

When presenting this project to recruiters or interviewers, describe the SQL work as:

> **"I built a structured SQL analysis project covering data validation, KPI analysis, churn-driver analysis, retention analysis, management business questions, and a dedicated interview-query module demonstrating core and advanced SQL techniques."**

For the interview-query module specifically:

> **"I practiced 45 SQL queries covering JOINs, aggregations, CASE WHEN, subqueries, CTEs, window functions, date functions, and advanced analytical SQL using the same customer churn database."**

This communicates both **technical breadth and practical application**.

---

# 26. Final Conclusion

The `08_interview_queries.sql` file serves as the technical SQL demonstration layer of the Customer Churn & Retention Analysis project.

The 45 queries collectively demonstrate that the project covers much more than basic `SELECT`, `WHERE`, and `GROUP BY` statements.

The most important technical capabilities demonstrated are:

1. **Joining multiple business datasets correctly.**
2. **Aggregating transactional data to the appropriate analytical grain.**
3. **Creating business classifications with CASE WHEN.**
4. **Using subqueries for benchmark and group-level comparisons.**
5. **Using CTEs to structure complex analytical logic.**
6. **Using window functions for ranking, running totals, and period-over-period analysis.**
7. **Working with dates and customer lifecycle information.**
8. **Solving realistic advanced SQL problems involving customer behavior and business benchmarks.**

The module therefore provides a strong SQL interview-practice foundation for a **Data Analyst portfolio project**.

---

# Module Status

**`08_interview_queries.sql` — COMPLETE**

### SQL Skill Coverage

| Skill            | Status    |
| ---------------- | --------- |
| JOINs            | ✅ Covered |
| Aggregations     | ✅ Covered |
| CASE WHEN        | ✅ Covered |
| Subqueries       | ✅ Covered |
| CTEs             | ✅ Covered |
| Window Functions | ✅ Covered |
| Date Functions   | ✅ Covered |
| Advanced SQL     | ✅ Covered |

**Total Interview Queries: 45**

### Overall SQL Project Status

```text
SQL Project
│
├── 01_database_design
│   └── 01_database_design.sql              ✅
│
├── 02_data_loading
│   └── 01_data_loading.sql                 ✅
│
├── 03_data_validation
│   └── 01_data_validation.sql              ✅
│
├── 04_kpi_analysis
│   └── 01_kpi_analysis.sql                 ✅
│
├── 05_churn_driver_analysis
│   ├── 01_lifecycle_churn.sql              ✅
│   ├── 02_subscription_churn.sql           ✅
│   ├── 03_payment_churn.sql                ✅
│   ├── 04_service_churn.sql                ✅
│   ├── 05_support_churn.sql                ✅
│   ├── 06_engagement_churn.sql             ✅
│   ├── 07_customer_profile_churn.sql       ✅
│   └── 08_multidimensional_churn.sql       ✅
│
├── Retention Analysis
│   ├── 01_retention_by_lifecycle.sql       ✅
│   ├── 02_retention_by_plan.sql             ✅
│   ├── 03_retention_by_contract.sql         ✅
│   ├── 04_retention_by_payment.sql          ✅
│   ├── 05_retention_by_service.sql          ✅
│   ├── 06_retention_by_support.sql          ✅
│   └── 07_high_value_retention.sql          ✅
│
├── Business Questions
│   ├── 01_customer_questions.sql            ✅
│   ├── 02_churn_questions.sql               ✅
│   ├── 03_payment_questions.sql             ✅
│   ├── 04_support_questions.sql             ✅
│   ├── 05_retention_questions.sql           ✅
│   └── 06_management_questions.sql          ✅
│
└── 08_interview_queries.sql                 ✅
```

**Interview SQL Module: COMPLETE**

**Overall SQL Analysis Structure: COMPLETE**
