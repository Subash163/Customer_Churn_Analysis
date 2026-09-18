# Customer Churn & Retention Analysis

## SQL Data Validation Observations

---

## 1. Objective

The objective of the SQL Data Validation stage was to confirm that the data loaded into the MySQL database matches the expected cleaned dataset and satisfies the defined structural, referential, technical, and business rules.

The validation process was performed after the final data-loading corrections.

The validation covered:

* Row counts
* Primary-key integrity
* Duplicate records
* NULL values
* Blank values
* ID formats
* Churn status/date consistency
* Foreign-key integrity
* Orphan records
* Customer coverage
* Category values
* Date ranges
* Numeric business rules
* Python-to-SQL reconciliation

---

# 2. Row Count Validation

The final SQL row counts were compared with the expected cleaned dataset volumes.

| Table             | Expected | SQL Result | Status |
| ----------------- | -------: | ---------: | ------ |
| customers         |   20,000 |     20,000 | PASS   |
| subscriptions     |   20,000 |     20,000 | PASS   |
| payments          |  355,437 |    355,437 | PASS   |
| customer_services |   20,000 |     20,000 | PASS   |
| support_tickets   |   50,000 |     50,000 | PASS   |

### Observation

All five operational tables contain the expected number of records.

**Result: PASS**

---

# 3. Primary-Key Integrity

Primary-key validation checked:

* NULL primary keys
* Duplicate primary keys
* Total rows
* Non-null primary-key count
* Distinct primary-key count

The following primary keys were validated:

| Table             | Primary Key     |
| ----------------- | --------------- |
| customers         | Customer_ID     |
| subscriptions     | Subscription_ID |
| payments          | Payment_ID      |
| customer_services | Customer_ID     |
| support_tickets   | Ticket_ID       |

### Result

All primary keys were:

* Non-null
* Unique
* Consistent with total row counts

No duplicate primary-key records were found.

**Result: PASS**

---

# 4. Explicit Duplicate Validation

Separate duplicate checks were performed for the major business identifiers:

* Customer_ID
* Subscription_ID
* Payment_ID
* Ticket_ID

All duplicate queries returned no records.

Exact full-row duplicate checks were also performed for all five operational tables.

No exact duplicate records were identified.

**Result: PASS**

---

# 5. ID Format Validation

The expected identifier formats were checked using regular expressions.

| ID              | Expected Format | Invalid Records |
| --------------- | --------------- | --------------: |
| Customer_ID     | C + 5 digits    |               0 |
| Subscription_ID | S + 6 digits    |               0 |
| Payment_ID      | P + 7 digits    |               0 |
| Ticket_ID       | T + 7 digits    |               0 |

### Observation

All identifiers conform to the defined project format.

**Result: PASS**

---

# 6. NULL Validation

NULL validation was performed separately for each operational table.

## Customers

| Column      | NULL Count |
| ----------- | ---------: |
| Customer_ID |          0 |
| Gender      |         79 |
| Age         |        240 |
| City        |          0 |
| State       |          0 |
| Signup_Date |          0 |

The missing Gender and Age values were confirmed as genuine missing values in the source dataset.

They were preserved as NULL rather than being imputed.

---

## Subscriptions

| Column          | NULL Count |
| --------------- | ---------: |
| Customer_ID     |          0 |
| Subscription_ID |          0 |
| Plan            |          0 |
| Contract_Type   |          0 |
| Start_Date      |          0 |
| End_Date        |     15,537 |
| Monthly_Charge  |          0 |
| Churn_Status    |          0 |
| Churn_Date      |     15,537 |

The NULL End_Date and Churn_Date values are expected for active subscriptions according to the project business rules.

---

## Payments

All validated payment columns contained:

```text
0 NULL values
```

**Result: PASS**

---

## Customer Services

| Column          | NULL Count |
| --------------- | ---------: |
| Customer_ID     |          0 |
| Mobile_App      |          0 |
| Streaming       |         70 |
| Cloud_Storage   |         70 |
| Premium_Support |         70 |
| Family_Plan     |          0 |

The three service-related missing-value groups were confirmed against the Python source data.

They represent genuine missing information and were intentionally preserved as NULL.

---

## Support Tickets

All validated support-ticket columns contained:

```text
0 NULL values
```

**Result: PASS**

---

# 7. Blank-String Validation

Blank-string checks were performed separately from SQL NULL checks.

This distinction was important because:

```sql
NULL
```

and:

```text
''
```

are different representations in MySQL.

After the final reload of `customer_services`, blank nullable values were converted to SQL NULL during loading.

The final dataset therefore uses:

```text
SQL NULL
```

rather than empty strings for the identified missing values.

**Result: PASS**

---

# 8. Churn Status and Churn Date Consistency

The following business rule was validated:

* Active customers should have NULL Churn_Date.
* Churned customers should have a populated Churn_Date.

Final distribution:

| Churn Status | Customers | NULL Churn Date |
| ------------ | --------: | --------------: |
| Active       |    15,537 |          15,537 |
| Churned      |     4,463 |               0 |

No invalid churn status/date combinations were identified.

**Result: PASS**

---

# 9. Customer Business Rules

## Age

Invalid ages below 18 or above 75 were checked.

```text
Invalid ages = 0
```

The 240 missing Age values were retained as NULL.

**Result: PASS**

---

## Gender

Non-missing Gender values were checked against the expected categories.

Distribution:

| Gender  |  Count |
| ------- | -----: |
| Male    | 10,517 |
| Female  |  9,404 |
| Missing |     79 |

The 79 missing values were permitted and documented rather than imputed.

**Result: PASS — with documented missing values**

---

# 10. Subscription Business Rules

### Plan

| Plan     | Customers |
| -------- | --------: |
| Standard |     8,538 |
| Basic    |     7,479 |
| Premium  |     3,983 |

All observed Plan values belong to the expected categories.

**Result: PASS**

### Contract Type

| Contract Type | Customers |
| ------------- | --------: |
| Monthly       |    11,628 |
| One Year      |     5,326 |
| Two Year      |     3,046 |

All observed Contract_Type values belong to the expected categories.

**Result: PASS**

### Churn Status

| Churn Status | Customers |
| ------------ | --------: |
| Active       |    15,537 |
| Churned      |     4,463 |

No unexpected Churn_Status values were identified.

**Result: PASS**

---

# 11. Subscription Date Validation

The following date rules were checked:

* End_Date should not be earlier than Start_Date.
* Churn_Date should not be earlier than Start_Date.
* Churned customers should have an End_Date.
* Active customers should not have an End_Date under the defined project rule.

Results:

```text
End_Date < Start_Date = 0
Churn_Date < Start_Date = 0
Churned without End_Date = 0
Active with End_Date = 0
```

**Result: PASS**

---

# 12. Monthly Charge Validation

Negative monthly charges were checked.

```text
Negative Monthly_Charge = 0
```

All monthly charges satisfy the defined non-negative business rule.

**Result: PASS**

---

# 13. Customer Services Validation

The service columns were checked for valid categorical values.

### Mobile App

| Value |  Count |
| ----- | -----: |
| Yes   | 16,858 |
| No    |  3,142 |

### Streaming

| Value   |  Count |
| ------- | -----: |
| Yes     | 11,536 |
| No      |  8,394 |
| Missing |     70 |

### Cloud Storage

| Value   |  Count |
| ------- | -----: |
| Yes     |  9,272 |
| No      | 10,658 |
| Missing |     70 |

### Premium Support

| Value   |  Count |
| ------- | -----: |
| Yes     |  4,458 |
| No      | 15,472 |
| Missing |     70 |

### Family Plan

| Value |  Count |
| ----- | -----: |
| Yes   |  5,627 |
| No    | 14,373 |

The identified missing service values were preserved as NULL.

No unexpected Yes/No categories were identified.

**Result: PASS**

---

# 14. Payment Validation

## Payment Status

| Status     |   Count |
| ---------- | ------: |
| Successful | 334,112 |
| Failed     |  21,325 |

No unexpected Payment_Status values were identified.

**Result: PASS**

## Payment Method

| Payment Method |   Count |
| -------------- | ------: |
| UPI            | 127,962 |
| Credit Card    |  89,112 |
| Debit Card     |  56,752 |
| Net Banking    |  46,165 |
| Wallet         |  35,446 |

All observed payment methods belong to the expected categories.

**Result: PASS**

## Payment Amount

```text
Negative payment amounts = 0
```

**Result: PASS**

## Payment Dates

Payment dates were checked against the expected project period:

```text
2023-01-01 to before 2026-01-01
```

No payment dates were outside the expected period.

**Result: PASS**

---

# 15. Support Ticket Validation

## Issue Type

| Issue Type  |  Count |
| ----------- | -----: |
| Technical   | 14,831 |
| Billing     | 10,886 |
| Account     |  9,154 |
| General     |  7,661 |
| Performance |  7,468 |

All Issue_Type values belong to the expected categories.

**Result: PASS**

## Resolution Status

| Resolved |  Count |
| -------- | -----: |
| Yes      | 44,421 |
| No       |  5,579 |

No unexpected resolution categories were identified.

**Result: PASS**

## Satisfaction Score

The defined valid range is:

```text
1 to 5
```

Invalid satisfaction scores:

```text
0
```

**Result: PASS**

## Resolution Time

Negative resolution times:

```text
0
```

**Result: PASS**

## Ticket Dates

Ticket dates were checked against:

```text
2023-01-01 to before 2026-01-01
```

No ticket dates were outside the expected period.

**Result: PASS**

---

# 16. One-to-One Relationship Validation

The following relationships were checked:

### Customer Services

Each Customer_ID has at most one customer_services record.

```text
Duplicate Customer_ID records = 0
```

**Result: PASS**

### Subscriptions

The current dataset contains one subscription per customer.

```text
20,000 subscriptions
20,000 unique customers
```

Therefore, the current dataset has a one-to-one customer-to-subscription structure.

This is a property of the current dataset and is not treated as a universal business rule.

**Result: PASS**

---

# 17. Referential Integrity

Foreign-key relationships were checked between the customer table and the child tables:

* subscriptions → customers
* payments → customers
* customer_services → customers
* support_tickets → customers

The orphan-record checks returned:

| Child Table       | Orphan Records |
| ----------------- | -------------: |
| subscriptions     |              0 |
| payments          |              0 |
| customer_services |              0 |
| support_tickets   |              0 |

No child records reference a non-existent customer.

**Result: PASS**

---

# 18. Customer Coverage

Customer coverage was checked across the main customer-related tables.

Results:

```text
Customers with subscription = 20,000
Customers with services     = 20,000
```

All customers in the customer master table have corresponding subscription and customer-service records.

**Result: PASS**

---

# 19. Python-to-SQL Reconciliation

SQL summary metrics were compared with the validated Python results.

The major SQL metrics confirmed were:

### Customer / Subscription

```text
Total customers       = 20,000
Total subscriptions   = 20,000
Churned customers     = 4,463
Active customers      = 15,537
Churn rate            = 22.32%
Average monthly charge = ₹583.66
```

### Payments

```text
Total payments          = 355,437
Unique payment IDs      = 355,437
Unique paying customers = 20,000
Successful payments     = 334,112
Failed payments         = 21,325
Total payment value     = ₹205,957,486.17
Average payment         = ₹579.45
```

### Support

```text
Total tickets          = 50,000
Unique ticket IDs      = 50,000
Unique ticket customers = 18,349
Resolved tickets       = 44,421
Unresolved tickets     = 5,579
Average resolution     = 7.98 hours
Average satisfaction   = 4.41
```

The SQL database-side metrics align with the validated project metrics.

The existing reconciliation script also includes a comparison template for entering explicit Python baseline values where required.

---

# 20. Overall Validation Summary

| Validation Area              | Result |
| ---------------------------- | ------ |
| Row counts                   | PASS   |
| Primary keys                 | PASS   |
| Duplicate primary keys       | PASS   |
| Full-row duplicates          | PASS   |
| ID formats                   | PASS   |
| NULL handling                | PASS   |
| Blank-string handling        | PASS   |
| Churn/date consistency       | PASS   |
| Customer business rules      | PASS   |
| Subscription business rules  | PASS   |
| Payment business rules       | PASS   |
| Customer service categories  | PASS   |
| Support ticket rules         | PASS   |
| Date ranges                  | PASS   |
| Foreign keys                 | PASS   |
| Orphan records               | PASS   |
| Customer coverage            | PASS   |
| Python-to-SQL reconciliation | PASS   |

---

# 21. Important Data Quality Findings

The validation process identified genuine missing values:

* 240 missing Age values.
* 79 missing Gender values.
* 70 missing Streaming values.
* 70 missing Cloud_Storage values.
* 70 missing Premium_Support values.

These were not treated as errors requiring imputation.

The project intentionally preserves these values as SQL NULL because replacing them with assumed values could introduce false information into the analysis.

---

# 22. Analytical Considerations

The missing Gender values should be excluded or explicitly handled when performing analyses that require known gender.

Similarly, analyses of individual customer services should account for NULL service values rather than automatically treating NULL as `No`.

For example:

```text
NULL ≠ No
```

A NULL service value means that the information is missing, not that the customer definitely does not use the service.

This distinction should be maintained in future churn and retention analysis.

---

# 23. Conclusion

The SQL Data Validation stage is complete.

The final MySQL database satisfies the expected structural, referential, technical, and business-rule checks.

All five operational tables contain the expected number of records, primary keys are unique and non-null, foreign-key relationships are valid, no orphan records were found, identifier formats are valid, and no invalid business-rule values were detected.

The identified missing values were confirmed as genuine source-level missing information and were preserved as SQL NULL rather than being imputed.

The database is therefore ready for the analytical SQL stages:

```text
KPI Analysis
    ↓
Churn Driver Analysis
    ↓
Retention Analysis
    ↓
Business Questions
    ↓
Interview Queries
```

**Status: DATA VALIDATION — COMPLETED**
