# Customer Churn & Retention Analysis

## Data Cleaning & Validation Observations

**Project:** Customer Churn & Retention Analysis
**Documentation:** Data Cleaning & Validation Observations
**Purpose:** Document data-quality assessment, cleaning decisions, post-cleaning validation, and referential-integrity checks performed before analytical modeling.

---

# 1. Overview

The Customer Churn & Retention Analysis project uses multiple related datasets representing customers, subscriptions, payments, customer services, and support interactions.

The data-quality process was designed to ensure that the datasets were reliable and structurally consistent before performing exploratory data analysis, churn analysis, SQL analysis, feature engineering, and Power BI dashboard development.

The overall data-quality workflow followed this process:

```text
Raw Excel Workbook
        ↓
Data Loading
        ↓
Data Profiling
        ↓
Schema Validation
        ↓
Data Cleaning
        ↓
Post-Cleaning Validation
        ↓
Referential Integrity Validation
        ↓
Final Analytical Dataset
        ↓
EDA & Churn Analysis
        ↓
SQL Analysis
        ↓
Power BI Dashboard
```

The six completed sheets covered in this document are:

1. Customers
2. Subscriptions
3. Payments
4. Customer_Services
5. Support_Tickets
6. Data_Dictionary

> **Note:** The Churn sheet is not included in this document because its cleaning and validation workflow has not yet been completed.

---

# 2. Data Quality Philosophy

The cleaning process followed a few important principles.

## 2.1 Do not blindly remove records

Records were removed only when they matched an identified data-quality problem such as:

* Exact duplicate records
* Duplicate business identifiers
* Other clearly defined cleaning rules

The objective was to preserve valid business information while removing only demonstrably problematic records.

---

## 2.2 Missing values were evaluated contextually

A missing value was not automatically treated as an error.

For example, missing `End_Date` or `Churn_Date` in the Subscriptions dataset can be legitimate for active subscriptions.

Similarly, a missing service flag in Customer_Services means the service status is unknown. It should not automatically be converted to `"No"`.

Therefore:

```text
Missing ≠ No
```

and:

```text
Missing ≠ Invalid
```

The business meaning of missing data was considered before deciding whether to modify it.

---

## 2.3 Referential integrity was validated before analysis

Instead of assuming that Customer IDs matched across datasets, explicit referential-integrity checks were performed.

This helped identify:

* Orphan records
* Missing keys
* Duplicate keys
* Customer coverage
* Relationship cardinality
* Customers without downstream records

---

# 3. Dataset Summary

| Dataset           | Original Rows | Final Rows | Rows Removed | Columns | Missing Values After Cleaning | Validation Status |
| ----------------- | ------------: | ---------: | -----------: | ------: | ----------------------------: | ----------------- |
| Customers         |        20,035 |     20,000 |           35 |       6 |                           439 | PASS              |
| Subscriptions     |        20,000 |     20,000 |            0 |       9 |                        31,074 | PASS              |
| Payments          |       355,557 |    355,437 |          120 |       6 |                             0 | PASS              |
| Customer_Services |        20,000 |     20,000 |            0 |       6 |                           210 | PASS              |
| Support_Tickets   |        50,080 |     50,000 |           80 |       7 |                             0 | PASS              |
| Data_Dictionary   |            32 |         32 |            0 |       5 |                             0 | PASS              |

> Missing values in Subscriptions and Customer_Services were reviewed contextually and intentionally preserved where appropriate.

---

# 4. Customers Dataset

## 4.1 Dataset Structure

Columns:

```text
customer_id
gender
age
city
state
signup_date
```

The Customers dataset represents the customer master data and serves as the primary customer entity for relationships with downstream datasets.

---

## 4.2 Cleaning Results

| Metric                 | Result |
| ---------------------- | -----: |
| Original rows          | 20,035 |
| Final rows             | 20,000 |
| Rows removed           |     35 |
| Columns                |      6 |
| Total missing values   |    439 |
| Duplicate rows         |      0 |
| Missing Customer IDs   |      0 |
| Duplicate Customer IDs |      0 |
| Cleaning issues        |      2 |

---

## 4.3 Key Data-Quality Observations

### Customer ID integrity

Post-cleaning validation confirmed:

```text
Missing Customer IDs     : 0
Duplicate Customer IDs   : 0
```

Therefore, `customer_id` is suitable as the primary customer identifier.

### Missing values

The final dataset contains:

```text
439 missing values
```

These values were not blindly replaced because demographic information such as gender, age, city, or state may legitimately be unavailable.

### Duplicate records

The final dataset contains:

```text
Duplicate Rows : 0
```

The Customer master dataset therefore contains no duplicate complete records after cleaning.

---

## 4.4 Referential Integrity

Customers was validated against:

* Subscriptions
* Payments
* Customer_Services
* Support_Tickets

The Customer ID relationships were successfully validated.

### Customers → Subscriptions

```text
Customers                         : 20,000
Subscriptions                    : 20,000
Missing Customer IDs             : 0
Duplicate Customer IDs           : 0
Orphan Subscription Customer IDs : 0
Customer ID overlap              : 20,000
Customers without subscription   : 0
Relationship                     : One-to-One
Overall integrity                : PASS
```

### Customers → Payments

```text
Customers                       : 20,000
Payments                        : 355,437
Matching Customer IDs           : 20,000
Customers without payments      : 0
Orphan payment customer IDs     : 0
Customer payment coverage       : 100%
Payment customer coverage       : 100%
Relationship                    : One-to-Many
Overall integrity               : PASS
```

### Customers → Customer_Services

```text
Customers                         : 20,000
Customer_Services                 : 20,000
Customer ID overlap               : 20,000
Orphan service records            : 0
Customers without service records: 0
Multiple service records          : 0
Relationship                      : One-to-One
Overall integrity                 : PASS
```

### Customers → Support_Tickets

```text
Customers                         : 20,000
Support Tickets                  : 50,000
Matching Customer IDs             : 18,349
Customers without tickets         : 1,651
Orphan Support Tickets            : 0
Support Ticket customer coverage  : 100%
Customer support ticket coverage  : 91.75%
Relationship                      : One-to-Many
Overall integrity                 : PASS
```

---

## 4.5 Recruiter-Facing Observation

> **Established Customers as the master entity, validated Customer_ID uniqueness, and verified its referential relationships with downstream datasets before analytical modeling.**

---

# 5. Subscriptions Dataset

## 5.1 Dataset Structure

Columns:

```text
customer_id
subscription_id
plan
contract_type
start_date
end_date
monthly_charge
churn_status
churn_date
```

---

## 5.2 Cleaning Results

| Metric                     | Result |
| -------------------------- | -----: |
| Original rows              | 20,000 |
| Final rows                 | 20,000 |
| Rows removed               |      0 |
| Columns                    |      9 |
| Total missing values       | 31,074 |
| Duplicate rows             |      0 |
| Missing Customer IDs       |      0 |
| Duplicate Customer IDs     |      0 |
| Missing Subscription IDs   |      0 |
| Duplicate Subscription IDs |      0 |
| Cleaning issues            |      2 |

---

## 5.3 Key Data-Quality Observation: Missing Values

The dataset contains:

```text
31,074 missing values
```

This was not treated as an automatic data-quality failure.

A significant portion of the missing values occurs in fields such as:

```text
end_date
churn_date
```

For an active subscription, the absence of an end date or churn date can be valid business information.

Therefore, these values were preserved instead of being artificially populated.

### Important principle

```text
Active Subscription
        ↓
End_Date may be NULL
Churn_Date may be NULL
```

This prevents incorrect assumptions from being introduced into the dataset.

---

## 5.4 Validation Results

Post-cleaning validation produced:

```text
Rows                  : 20,000
Columns               : 9
Failed Checks         : 0
```

No critical validation failures were identified.

---

## 5.5 Referential Integrity

Customers ↔ Subscriptions validation:

```text
Customers                         : 20,000
Subscriptions                    : 20,000
Missing Customer IDs             : 0
Duplicate Customer IDs           : 0
Missing Subscription IDs         : 0
Duplicate Subscription IDs       : 0
Orphan Subscription Customer IDs : 0
Customer ID overlap              : 20,000
Customers without subscription   : 0
Relationship                     : One-to-One
Overall integrity                : PASS
```

---

## 5.6 Recruiter-Facing Observation

> **Investigated missing subscription dates contextually instead of blindly imputing NULL values, recognizing that missing End_Date and Churn_Date can represent active subscriptions.**

---

# 6. Payments Dataset

## 6.1 Dataset Structure

Columns:

```text
payment_id
customer_id
payment_date
amount
payment_method
payment_status
```

---

## 6.2 Cleaning Results

| Metric                |  Result |
| --------------------- | ------: |
| Original rows         | 355,557 |
| Final rows            | 355,437 |
| Rows removed          |     120 |
| Columns               |       6 |
| Missing values        |       0 |
| Duplicate rows        |       0 |
| Missing Payment IDs   |       0 |
| Duplicate Payment IDs |       0 |
| Missing Customer IDs  |       0 |
| Unique Payment IDs    | 355,437 |
| Unique Customers      |  20,000 |
| Cleaning issues       |       2 |

---

## 6.3 Key Data-Quality Observations

### Payment ID integrity

```text
Missing Payment IDs   : 0
Duplicate Payment IDs : 0
```

Therefore, `payment_id` can be treated as the payment-level identifier.

### Amount validation

Post-cleaning validation confirmed:

```text
Invalid Payment Amounts : 0
Negative Amounts        : 0
```

### Date validation

```text
Missing Payment Dates : 0
Invalid Payment Dates : 0
Future Payment Dates  : 0
```

---

## 6.4 Customer Coverage

All customers have payment records:

```text
Customers                : 20,000
Unique customers in payments : 20,000
Customers without payments    : 0
Customer payment coverage     : 100%
```

---

## 6.5 Customer → Payments Relationship

The relationship was validated as one-to-many.

```text
Customers with multiple payments : 19,972
Customers with exactly one payment : 28
Minimum payments per customer      : 1
Maximum payments per customer      : 36
Average payments per customer      : 17.77
```

Relationship:

```text
Customers
    1
    │
    ├── Payment
    ├── Payment
    ├── Payment
    └── ...
```

---

## 6.6 Recruiter-Facing Observation

> **Validated payment-level uniqueness and established a one-to-many Customer → Payments relationship, creating a reliable foundation for later payment frequency and revenue analysis.**

---

# 7. Customer_Services Dataset

## 7.1 Dataset Structure

Columns:

```text
customer_id
mobile_app
streaming
cloud_storage
premium_support
family_plan
```

---

## 7.2 Cleaning Results

| Metric                 | Result |
| ---------------------- | -----: |
| Rows                   | 20,000 |
| Columns                |      6 |
| Rows removed           |      0 |
| Missing values         |    210 |
| Duplicate rows         |      0 |
| Missing Customer IDs   |      0 |
| Duplicate Customer IDs |      0 |
| Unique Customer IDs    | 20,000 |
| Cleaning issues        |      3 |

---

## 7.3 Missing Value Analysis

The 210 missing values were distributed as follows:

| Service         | Missing Values |
| --------------- | -------------: |
| Streaming       |             70 |
| Cloud Storage   |             70 |
| Premium Support |             70 |
| Mobile App      |              0 |
| Family Plan     |              0 |
| **Total**       |        **210** |

These missing values were intentionally preserved.

### Important decision

A missing service value was not converted to `"No"`.

For example:

```text
Streaming = Missing
```

does not necessarily mean:

```text
Streaming = No
```

It means the customer's service status is unknown.

This prevents false service-adoption information from entering the analytical dataset.

---

## 7.4 Validation Results

Post-cleaning validation confirmed:

```text
Total Missing Values       : 210 INFO
Missing Customer IDs       : 0 PASS
Duplicate Rows             : 0 PASS
Duplicate Customer IDs     : 0 PASS
Unexpected Service Values  : 0 PASS
Failed Checks              : 0
```

The missing values were treated as informational rather than critical failures.

---

## 7.5 Referential Integrity

```text
Customers                         : 20,000
Customer_Services                 : 20,000
Customer ID overlap               : 20,000
Customers without service records : 0
Orphan service records            : 0
Multiple service records          : 0
Exactly one service record        : 20,000
Relationship                      : One-to-One
Overall integrity                 : PASS
```

---

## 7.6 Recruiter-Facing Observation

> **Preserved unknown service values instead of converting NULLs to "No", preventing inaccurate service-adoption analysis.**

---

# 8. Support_Tickets Dataset

## 8.1 Dataset Structure

Columns:

```text
ticket_id
customer_id
ticket_date
issue_type
resolution_time_hours
satisfaction_score
resolved
```

---

## 8.2 Cleaning Results

| Metric               | Result |
| -------------------- | -----: |
| Original rows        | 50,080 |
| Final rows           | 50,000 |
| Rows removed         |     80 |
| Columns              |      7 |
| Missing values       |      0 |
| Duplicate rows       |      0 |
| Missing Ticket IDs   |      0 |
| Duplicate Ticket IDs |      0 |
| Missing Customer IDs |      0 |
| Unique Ticket IDs    | 50,000 |
| Unique Customers     | 18,349 |
| Cleaning issues      |      3 |

---

## 8.3 Duplicate Record Investigation

The 80 removed records were fully explained:

```text
79 exact duplicate rows
+
1 duplicate Ticket_ID record
=
80 removed records
```

This provides a clear audit trail for the cleaning process.

---

## 8.4 Ticket ID Validation

Final validation confirmed:

```text
Missing Ticket IDs       : 0
Duplicate Ticket IDs     : 0
Blank Ticket IDs         : 0
Unique Ticket IDs        : 50,000
```

Therefore, `ticket_id` is reliable as the ticket-level identifier.

---

## 8.5 Data Validation

The final dataset passed all critical checks:

```text
Missing Ticket Dates       : 0
Future Ticket Dates        : 0
Invalid Resolution Time    : 0
Negative Resolution Time   : 0
Missing Satisfaction Score : 0
Invalid Satisfaction Score : 0
Unexpected Resolved Values : 0
```

Satisfaction scores were confirmed to be within the expected 1–5 range.

---

## 8.6 Support Ticket Profile

The cleaned dataset contains:

```text
Resolved tickets   : 44,421
Unresolved tickets : 5,579
```

Approximately:

```text
Resolved   : 88.84%
Unresolved : 11.16%
```

Average values:

```text
Average Resolution Time : 7.98 hours
Average Satisfaction    : 4.41 / 5
```

These are descriptive data-quality observations and should not yet be interpreted as churn drivers.

---

## 8.7 Customer Coverage

```text
Total Customers                : 20,000
Customers with Support Tickets : 18,349
Customers without Tickets      : 1,651
Customer Support Coverage      : 91.75%
```

Every Support Ticket has a valid Customer ID:

```text
Support Ticket Customer Coverage : 100%
```

This distinction is important:

```text
91.75% of customers have tickets
```

does not mean:

```text
91.75% of tickets are valid
```

In fact, the ticket-level coverage is:

```text
100%
```

because every ticket maps to a valid customer.

---

## 8.8 Customer → Support Tickets Relationship

The relationship was validated as:

```text
One Customer → Many Support Tickets
```

Supporting observations:

```text
Customers with multiple tickets : 14,271
Customers with exactly one ticket : 4,078
Maximum tickets for one customer : 11
Average tickets per customer     : 2.72
```

The average of 2.72 is calculated among customers who have at least one support ticket.

---

## 8.9 Referential Integrity

```text
Customers                         : 20,000
Support Tickets                  : 50,000
Matching Customer IDs             : 18,349
Orphan Support Tickets            : 0
Tickets without Customer          : 0
Customers without Support Tickets : 1,651
Customer Support Coverage         : 91.75%
Ticket Customer Coverage          : 100%
Relationship                      : One-to-Many
Overall integrity                 : PASS
```

Customers without support tickets were treated as valid business cases rather than referential-integrity failures.

---

## 8.10 Recruiter-Facing Observation

> **Validated the one-to-many Customer → Support Tickets relationship and distinguished customers without support interactions from actual referential-integrity errors.**

---

# 9. Data_Dictionary Dataset

## 9.1 Dataset Structure

Columns:

```text
table
column
description
data_type
notes
```

The Data_Dictionary is metadata and documentation rather than operational business data.

Therefore, operational validation rules such as payment amount checks, customer age checks, or date-range checks were not applied to this dataset.

---

## 9.2 Cleaning Results

| Metric                               | Result |
| ------------------------------------ | -----: |
| Original rows                        |     32 |
| Final rows                           |     32 |
| Rows removed                         |      0 |
| Columns                              |      5 |
| Missing values                       |      0 |
| Duplicate rows                       |      0 |
| Duplicate Table + Column definitions |      0 |
| Missing Table names                  |      0 |
| Missing Column names                 |      0 |
| Missing Descriptions                 |      0 |
| Missing Data Types                   |      0 |
| Missing Notes                        |      0 |
| Unique Tables                        |      5 |
| Unique Columns                       |     30 |
| Cleaning issues                      |      0 |

---

## 9.3 Metadata Validation

The Data_Dictionary passed all critical checks:

```text
Expected Columns Present          : PASS
Total Missing Values              : PASS
Blank Table Names                 : PASS
Blank Column Names                : PASS
Duplicate Rows                    : PASS
Duplicate Table + Column          : PASS
Missing Descriptions              : PASS
Missing Data Types                : PASS
Missing Notes                     : PASS
Data Dictionary Contains Records  : PASS
Overall Validation                : PASS
```

Final validation:

```text
Total Checks  : 28
Passed Checks : 18
Failed Checks : 0
Info Checks   : 10
```

---

## 9.4 Recruiter-Facing Observation

> **Maintained the Data Dictionary as a metadata layer documenting table structures, column definitions, data types, and business notes rather than applying operational-data cleaning rules to it.**

---

# 10. Overall Referential Integrity Model

The completed datasets currently establish the following relationships:

```text
                         Customers
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             │              │              │
             ▼              ▼              ▼
      Subscriptions      Payments     Customer_Services
           1:1              1:M              1:1
                            │
                            │
                            ▼
                     Support_Tickets
                           1:M
```

More specifically:

```text
Customers
    │
    ├── 1:1 → Subscriptions
    │
    ├── 1:M → Payments
    │
    ├── 1:1 → Customer_Services
    │
    └── 1:M → Support_Tickets
```

All completed referential-integrity validations passed.

---

# 11. Key Data Quality Decisions

The following decisions are particularly important for this project.

## Decision 1 — Do not blindly impute missing values

Missing values were investigated based on their business meaning.

Example:

```text
Subscriptions
End_Date = NULL
Churn_Date = NULL
```

This may represent an active subscription.

---

## Decision 2 — Do not convert unknown service status to "No"

For Customer_Services:

```text
Missing Streaming
        ≠
Streaming = No
```

The unknown state was preserved.

---

## Decision 3 — Validate keys before joining

Primary and foreign-key-like relationships were checked before combining datasets.

This reduced the risk of:

* Duplicate customers
* Orphan records
* Incorrect joins
* Inflated metrics
* Incorrect aggregation

---

## Decision 4 — Validate relationship cardinality

The project did not assume every table was one-to-one.

Relationships were investigated and validated:

```text
Customers → Subscriptions       : 1:1
Customers → Payments            : 1:M
Customers → Customer_Services   : 1:1
Customers → Support_Tickets     : 1:M
```

---

## Decision 5 — Separate data-quality issues from valid business behavior

Examples:

```text
Customer without Support Ticket
        ↓
Valid business scenario
        ↓
Not a referential-integrity failure
```

Whereas:

```text
Support Ticket with unknown Customer_ID
        ↓
Invalid relationship
        ↓
Referential-integrity failure
```

This distinction was applied consistently.

---

# 12. Important Recruiter/Interview Talking Points

The following points summarize the strongest data-quality practices demonstrated in this project.

### Talking Point 1 — Data profiling

> "Before analysis, I profiled each dataset to understand its structure, missing values, duplicates, key fields, and data types."

### Talking Point 2 — Contextual missing-value handling

> "I did not treat every missing value as an error. I evaluated the business context first. For example, missing End_Date and Churn_Date can be valid for active subscriptions."

### Talking Point 3 — Referential integrity

> "I created separate referential-integrity validations to make sure Customer IDs were valid across related datasets and to identify orphan records before joining the data."

### Talking Point 4 — Relationship cardinality

> "I validated the actual relationship between datasets rather than assuming all tables were one-to-one. Payments and Support Tickets were validated as one-to-many relationships with Customers."

### Talking Point 5 — Duplicate investigation

> "When duplicate records were found, I investigated the reason before removing them. For example, Support_Tickets had 80 removed records consisting of 79 exact duplicates and one duplicate Ticket_ID record."

### Talking Point 6 — Unknown versus negative state

> "For service attributes, I preserved missing values rather than converting them to 'No', because missing information does not necessarily mean the customer does not use the service."

### Talking Point 7 — Auditability

> "Every cleaning process produced a cleaning report, and every post-cleaning validation produced a separate validation report, making the data-preparation process auditable."

---

# 13. Validation Report Inventory

The project generated separate validation reports for the completed datasets.

## Cleaning Reports

```text
outputs/
└── cleaning_reports/
    ├── customers_cleaning_report.xlsx
    ├── subscriptions_cleaning_report.xlsx
    ├── payments_cleaning_report.xlsx
    ├── customer_services_cleaning_report.xlsx
    ├── support_tickets_cleaning_report.xlsx
    └── data_dictionary_cleaning_report.xlsx
```

## Post-Cleaning Validation Reports

```text
outputs/
└── validation_reports/
    ├── customers_post_cleaning_validation_report.xlsx
    ├── subscriptions_post_cleaning_validation_report.xlsx
    ├── payments_post_cleaning_validation_report.xlsx
    ├── customer_services_post_cleaning_validation_report.xlsx
    ├── support_tickets_post_cleaning_validation_report.xlsx
    └── data_dictionary_post_cleaning_validation_report.xlsx
```

## Referential Integrity Reports

```text
outputs/
└── validation_reports/
    ├── customers_subscriptions_referential_integrity.xlsx
    ├── customers_payments_referential_integrity.xlsx
    ├── customers_customer_services_referential_integrity.xlsx
    └── customers_support_tickets_referential_integrity.xlsx
```

---

# 14. Overall Data Quality Conclusion

The six completed datasets successfully passed their respective cleaning and post-cleaning validation workflows.

Key outcomes include:

```text
Customers
    20,000 final records
    Customer_ID unique
    Referential relationships validated

Subscriptions
    20,000 final records
    Missing dates contextually reviewed
    Referential integrity passed

Payments
    355,437 final records
    Payment_ID unique
    100% customer coverage
    One-to-many relationship validated

Customer_Services
    20,000 final records
    Unknown service values preserved
    One-to-one relationship validated

Support_Tickets
    50,000 final records
    Duplicate records investigated and removed
    100% ticket-to-customer coverage
    One-to-many relationship validated

Data_Dictionary
    32 metadata records
    No missing values
    No duplicate definitions
    Metadata validation passed
```

Overall, the data-preparation process established a reliable foundation for the next stages of the Customer Churn & Retention Analysis project.

> **Important:** Data cleaning and validation confirm data reliability; they do not by themselves establish causal relationships or identify churn drivers. Churn insights will be determined during the subsequent analytical phase.

---

# 15. Next Phase

The remaining `Churn` dataset must be cleaned, post-validated, and checked for referential integrity before the final analytical dataset is created.

The planned next workflow is:

```text
Churn
   ↓
Churn Data Cleaning
   ↓
Churn Post-Cleaning Validation
   ↓
Customers ↔ Churn Referential Integrity
   ↓
Final Data Integration
   ↓
Feature Engineering
   ↓
EDA
   ↓
Churn & Retention Analysis
   ↓
SQL Analysis
   ↓
Power BI Dashboard
   ↓
Business Recommendations
```

The final analytical dataset should only be created after all required operational datasets have completed their data-quality and relationship validation.
