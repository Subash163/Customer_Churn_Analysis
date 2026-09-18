# Data Aggregation Observations

## Project

**Customer Churn & Retention Analysis**

---

# Objective

Convert transactional payment and support ticket tables into customer-level analytical datasets while preserving the one-customer-one-row design.

---

# Source Datasets

| Dataset         |    Rows | Relationship |
| --------------- | ------: | ------------ |
| Payments        | 355,437 | One-to-Many  |
| Support Tickets |  50,000 | One-to-Many  |

---

# Why Aggregation Was Required

Customers can have multiple payments and multiple support tickets.

Example:

| Customer | Payments | Tickets |
| -------- | -------: | ------: |
| C00001   |       18 |       3 |
| C00002   |       22 |       1 |

A direct join would duplicate customer rows.

**Solution:** Aggregate both transactional tables to customer level before merging.

---

# Payment Aggregation

### Metrics Created

* Total payment count
* Successful payment count
* Failed payment count
* Total payment amount
* Successful payment amount
* Failed payment amount
* Average payment amount
* Minimum payment amount
* Maximum payment amount
* Payment success rate
* Payment failure rate
* First payment date
* Last payment date
* Days since last payment
* Primary payment method
* Payments per month

### Results

| Metric                 |           Value |
| ---------------------- | --------------: |
| Payment Records        |         355,437 |
| Customer-Level Records |          20,000 |
| Unique Customers       |          20,000 |
| Successful Payments    |         334,112 |
| Failed Payments        |          21,325 |
| Total Payment Value    | ₹205,957,486.17 |

### Validation

| Check        | Result   |
| ------------ | -------- |
| Total Checks | 18       |
| Failed       | **0**    |
| Status       | **PASS** |

---

# Support Ticket Aggregation

### Metrics Created

* Total ticket count
* Resolved ticket count
* Unresolved ticket count
* Resolution rate
* Average resolution time
* Satisfaction score
* Issue-type counts
* First ticket date
* Last ticket date
* Tickets per month
* Support risk indicators

### Results

| Metric                    |    Value |
| ------------------------- | -------: |
| Support Tickets           |   50,000 |
| Customer-Level Records    |   18,349 |
| Customers Without Tickets |    1,651 |
| Resolved Tickets          |   44,421 |
| Unresolved Tickets        |    5,579 |
| Average Resolution Time   | 7.98 hrs |
| Average Satisfaction      | 4.41 / 5 |

### Validation

| Check        | Result   |
| ------------ | -------- |
| Total Checks | 28       |
| Failed       | **0**    |
| Status       | **PASS** |

---

# Key Observations

### 1. One-to-Many Relationships Successfully Resolved

Both transactional datasets were transformed into customer-level summaries before merging.

### 2. Complete Payment Coverage

Every customer has payment history, resulting in **100% payment coverage**.

### 3. Partial Support Coverage

Only **18,349 customers** interacted with customer support.

Approximately **8.25%** of customers never created a support ticket.

### 4. Behavioral Metrics Created

Instead of storing raw transactions, customer behavior is represented using aggregated KPIs that are suitable for predictive analytics.

---

# Recruiter Highlights

* Solved one-to-many relationship problems using customer-level aggregation.
* Prevented duplicate customer rows during analytical dataset creation.
* Designed reusable behavioral KPIs from transactional data.
* Maintained referential integrity throughout the aggregation process.

---

**Pipeline Stage:** Transaction Data → Customer-Level Aggregation → Validation
