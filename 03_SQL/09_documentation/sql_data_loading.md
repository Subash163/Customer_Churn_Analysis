# Customer Churn & Retention Analysis

## SQL Data Loading Observations

---

## 1. Objective

The objective of the SQL Data Loading stage was to load the cleaned and validated CSV datasets generated during the Python data-preparation stage into the MySQL database `customer_churn_analysis`.

The loading process was designed to:

* Load all five operational datasets into MySQL.
* Preserve the cleaned data structure.
* Maintain primary-key and foreign-key relationships.
* Handle genuine missing values appropriately.
* Convert blank nullable values into SQL `NULL`.
* Verify that the loaded row counts match the expected cleaned datasets.

The `Data_Dictionary` sheet was retained as project documentation and was not loaded as an operational database table.

---

## 2. Operational Tables Loaded

The following five tables were loaded:

| Table             | Expected Rows |
| ----------------- | ------------: |
| customers         |        20,000 |
| subscriptions     |        20,000 |
| payments          |       355,437 |
| customer_services |        20,000 |
| support_tickets   |        50,000 |

The expected row counts were based on the final cleaned datasets produced during the Python stage.

---

## 3. Initial Loading Issues Identified

During the initial SQL loading process, several row-count mismatches were identified.

### Initial results

| Table             | Expected | Initial Loaded | Issue                     |
| ----------------- | -------: | -------------: | ------------------------- |
| customers         |   20,000 |         19,760 | 240 rows missing          |
| subscriptions     |   20,000 |          4,404 | Foreign-key/loading issue |
| payments          |  355,437 |        351,167 | Row parsing issue         |
| customer_services |   20,000 |         19,760 | 240 rows missing          |
| support_tickets   |   50,000 |         49,410 | Row parsing issue         |

The initial problems were investigated rather than simply modifying the data to force the expected row counts.

---

## 4. Root Cause — CSV Line Endings

The cleaned CSV files were generated with Windows-style CRLF line endings:

```text
\r\n
```

The initial loading configuration used:

```sql
LINES TERMINATED BY '\n'
```

This caused incorrect row parsing during the `LOAD DATA LOCAL INFILE` process.

The CSV files were subsequently verified and the loading scripts were changed to:

```sql
LINES TERMINATED BY '\r\n'
```

This resolved the row-parsing issue.

---

## 5. Missing Customer Records

The initial `customers` load contained:

```text
19,760 rows
```

instead of the expected:

```text
20,000 rows
```

The missing 240 records were investigated.

The source CSV contained 240 customers with missing Age values. These customers were genuine records and should not have been removed merely because Age was missing.

The loading process was therefore corrected to allow blank Age values to become SQL `NULL`.

The final customer loading logic uses:

```sql
(Customer_ID, @Gender, @Age, City, State, Signup_Date)
SET
    Gender = NULLIF(TRIM(@Gender), ''),
    Age = NULLIF(@Age, '');
```

The final result was:

```text
20,000 customer records
```

---

## 6. Missing Gender Values

During SQL validation, 79 customer records were found with blank Gender values.

The source CSV was checked independently using Python and confirmed that the same 79 records contained genuinely missing Gender values.

Therefore, these values were not treated as an SQL loading error.

The decision was:

* Do not assume Male or Female.
* Do not use statistical imputation.
* Preserve the missing values.
* Represent them as SQL `NULL`.

The loading process was therefore updated to convert blank Gender values to SQL `NULL` during loading.

Final expected result:

```text
Gender NULL = 79
```

---

## 7. Missing Customer Service Values

The `customer_services` dataset contained genuine missing values in three service columns:

| Column          | Missing Values |
| --------------- | -------------: |
| Streaming       |             70 |
| Cloud_Storage   |             70 |
| Premium_Support |             70 |

Python source validation confirmed that these were genuine blank values in the cleaned CSV rather than an SQL import problem.

The decision was to preserve the missing values rather than assume `Yes` or `No`.

The final loading logic converts blank service values into SQL `NULL`:

```sql
SET
    Mobile_App = NULLIF(TRIM(@Mobile_App), ''),
    Streaming = NULLIF(TRIM(@Streaming), ''),
    Cloud_Storage = NULLIF(TRIM(@Cloud_Storage), ''),
    Premium_Support = NULLIF(TRIM(@Premium_Support), ''),
    Family_Plan = NULLIF(TRIM(@Family_Plan), '');
```

The `customer_services` table was truncated and reloaded using this corrected logic.

Final result:

```text
20,000 rows loaded
0 skipped
0 warnings
```

Expected missing values after loading:

```text
Streaming       = 70 NULL
Cloud_Storage   = 70 NULL
Premium_Support = 70 NULL
```

---

## 8. Subscriptions Loading

The `subscriptions` table contains nullable date fields.

Blank values in:

* `End_Date`
* `Churn_Date`

were converted to SQL `NULL`.

The loading logic uses:

```sql
End_Date = NULLIF(@End_Date, ''),
Churn_Date = NULLIF(@Churn_Date, '');
```

This is consistent with the business rule that active customers do not have a churn date.

Final result:

```text
20,000 subscriptions loaded
0 skipped
0 warnings
```

---

## 9. Payments Loading

The final `payments` dataset contained:

```text
355,437 records
```

The final loading process successfully loaded all records.

Final result:

```text
355,437 rows loaded
0 skipped
0 warnings
```

No missing-value conversion was required for the current payment dataset.

---

## 10. Support Tickets Loading

The final `support_tickets` dataset contained:

```text
50,000 records
```

The final loading process successfully loaded all records.

Final result:

```text
50,000 rows loaded
0 skipped
0 warnings
```

No missing-value conversion was required for the current support-ticket dataset.

---

## 11. Final Loading Results

After correcting the CSV line-ending configuration and nullable-field handling, the final row counts were:

| Table             | Expected | Final Loaded | Status |
| ----------------- | -------: | -----------: | ------ |
| customers         |   20,000 |       20,000 | PASS   |
| subscriptions     |   20,000 |       20,000 | PASS   |
| payments          |  355,437 |      355,437 | PASS   |
| customer_services |   20,000 |       20,000 | PASS   |
| support_tickets   |   50,000 |       50,000 | PASS   |

All final datasets matched their expected row counts.

---

## 12. Missing-Value Strategy

The project deliberately does not impute missing values simply to remove NULLs.

The following approach was used:

| Field                             | Missing Values | Treatment         |
| --------------------------------- | -------------: | ----------------- |
| customers.Age                     |            240 | Preserved as NULL |
| customers.Gender                  |             79 | Preserved as NULL |
| customer_services.Streaming       |             70 | Preserved as NULL |
| customer_services.Cloud_Storage   |             70 | Preserved as NULL |
| customer_services.Premium_Support |             70 | Preserved as NULL |

No mean, median, mode, or business-rule-based guessing was used.

This prevents artificially changing customer information.

---

## 13. Reproducibility Improvement

The final data-loading script was updated so that blank nullable values are converted to SQL `NULL` during the initial load itself.

This makes the loading process reproducible.

For example:

```sql
NULLIF(TRIM(@Gender), '')
```

converts blank Gender values into SQL `NULL`.

Similarly:

```sql
NULLIF(TRIM(@Streaming), '')
```

converts blank Streaming values into SQL `NULL`.

This approach eliminates the need for separate cleanup `UPDATE` statements after loading.

---

## 14. Final Data Loading Quality

The final data-loading stage achieved:

* Correct row counts.
* Correct CSV line-ending handling.
* Correct nullable-field handling.
* No skipped records.
* No loading warnings.
* Preservation of genuine missing values.
* Reproducible loading logic.
* Referential integrity maintained for subsequent validation.

---

## 15. Conclusion

The SQL Data Loading stage is complete.

The cleaned Python datasets were successfully loaded into the MySQL relational database with the expected record counts.

The initial loading issues were investigated and resolved through root-cause analysis rather than manual data manipulation.

The final loading process correctly handles genuine missing values by representing blank nullable values as SQL `NULL`.

The database is therefore ready for the Data Validation stage and subsequent analytical SQL work.

**Status: DATA LOADING — COMPLETED**
