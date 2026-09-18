-- Customer Churn Analysis | Data Validation
-- File: data_validation.sql
-- Purpose: Combined SQL validation script for the five operational
--          tables in the customer_churn_analysis database.
--
-- Validation sequence:
-- 1. Row counts
-- 2. Primary key validation
-- 3. NULL validation
-- 4. Duplicate validation
-- 5. Referential integrity
-- 6. Business-rule validation
-- 7. Python <-> SQL reconciliation
--
-- IMPORTANT:
-- This script validates the data currently loaded in MySQL.
-- The expected cleaned-data row counts are retained from the
-- original validation module. Update them when the final cleaned
-- Python outputs are confirmed.
--
-- Current expected target counts:
-- customers           20,000
-- subscriptions       20,000
-- payments            355,437
-- customer_services   20,000
-- support_tickets     50,000

-- VALIDATION MODULE 1: 01_row_counts.sql

-- Customer Churn Analysis | Data Validation
-- File: 01_row_counts.sql
-- Purpose: Validate loaded row counts against expected cleaned-data
--          counts from the Python/Excel validation stage.

USE customer_churn_analysis;

-- Actual SQL row counts
SELECT 'customers' AS table_name, COUNT(*) AS actual_row_count
FROM customers
UNION ALL
SELECT 'subscriptions', COUNT(*) FROM subscriptions
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'customer_services', COUNT(*) FROM customer_services
UNION ALL
SELECT 'support_tickets', COUNT(*) FROM support_tickets
ORDER BY table_name;

-- Expected counts from the validated cleaned datasets.
-- Update these values if your final cleaned outputs contain different
-- row counts before using this reconciliation query.

WITH expected_counts AS (
    SELECT 'customers' AS table_name, 20000 AS expected_row_count
    UNION ALL SELECT 'subscriptions', 20000
    UNION ALL SELECT 'payments', 355437
    UNION ALL SELECT 'customer_services', 20000
    UNION ALL SELECT 'support_tickets', 50000
),
actual_counts AS (
    SELECT 'customers' AS table_name, COUNT(*) AS actual_row_count FROM customers
    UNION ALL SELECT 'subscriptions', COUNT(*) FROM subscriptions
    UNION ALL SELECT 'payments', COUNT(*) FROM payments
    UNION ALL SELECT 'customer_services', COUNT(*) FROM customer_services
    UNION ALL SELECT 'support_tickets', COUNT(*) FROM support_tickets
)
SELECT
    e.table_name,
    e.expected_row_count,
    a.actual_row_count,
    a.actual_row_count - e.expected_row_count AS variance,
    CASE
        WHEN a.actual_row_count = e.expected_row_count THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM expected_counts e
JOIN actual_counts a
    ON e.table_name = a.table_name
ORDER BY e.table_name;


-- VALIDATION MODULE 2: 02_primary_key_validation.sql

-- Customer Churn Analysis | Data Validation
-- File: 02_primary_key_validation.sql
-- Purpose: Validate PK completeness, uniqueness and format.


USE customer_churn_analysis;

-- Primary-key completeness and uniqueness summary

SELECT
    'customers' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(Customer_ID) AS non_null_pk,
    COUNT(DISTINCT Customer_ID) AS distinct_pk,
    COUNT(*) - COUNT(Customer_ID) AS null_pk,
    COUNT(*) - COUNT(DISTINCT Customer_ID) AS duplicate_pk_rows
FROM customers

UNION ALL

SELECT
    'subscriptions',
    COUNT(*),
    COUNT(Subscription_ID),
    COUNT(DISTINCT Subscription_ID),
    COUNT(*) - COUNT(Subscription_ID),
    COUNT(*) - COUNT(DISTINCT Subscription_ID)
FROM subscriptions

UNION ALL

SELECT
    'payments',
    COUNT(*),
    COUNT(Payment_ID),
    COUNT(DISTINCT Payment_ID),
    COUNT(*) - COUNT(Payment_ID),
    COUNT(*) - COUNT(DISTINCT Payment_ID)
FROM payments

UNION ALL

SELECT
    'customer_services',
    COUNT(*),
    COUNT(Customer_ID),
    COUNT(DISTINCT Customer_ID),
    COUNT(*) - COUNT(Customer_ID),
    COUNT(*) - COUNT(DISTINCT Customer_ID)
FROM customer_services

UNION ALL

SELECT
    'support_tickets',
    COUNT(*),
    COUNT(Ticket_ID),
    COUNT(DISTINCT Ticket_ID),
    COUNT(*) - COUNT(Ticket_ID),
    COUNT(*) - COUNT(DISTINCT Ticket_ID)
FROM support_tickets;


-- Duplicate primary-key values
-- These queries should return zero rows.


SELECT Customer_ID, COUNT(*) AS duplicate_count
FROM customers
GROUP BY Customer_ID
HAVING COUNT(*) > 1;

SELECT Subscription_ID, COUNT(*) AS duplicate_count
FROM subscriptions
GROUP BY Subscription_ID
HAVING COUNT(*) > 1;

SELECT Payment_ID, COUNT(*) AS duplicate_count
FROM payments
GROUP BY Payment_ID
HAVING COUNT(*) > 1;

SELECT Ticket_ID, COUNT(*) AS duplicate_count
FROM support_tickets
GROUP BY Ticket_ID
HAVING COUNT(*) > 1;


-- ID format validation
-- Expected patterns:
-- Customer_ID     C00001
-- Subscription_ID S000001
-- Payment_ID      P0000001
-- Ticket_ID       T0000001


SELECT COUNT(*) AS invalid_customer_id_format
FROM customers
WHERE Customer_ID NOT REGEXP '^C[0-9]{5}$';

SELECT COUNT(*) AS invalid_subscription_id_format
FROM subscriptions
WHERE Subscription_ID NOT REGEXP '^S[0-9]{6}$';

SELECT COUNT(*) AS invalid_payment_id_format
FROM payments
WHERE Payment_ID NOT REGEXP '^P[0-9]{7}$';

SELECT COUNT(*) AS invalid_ticket_id_format
FROM support_tickets
WHERE Ticket_ID NOT REGEXP '^T[0-9]{7}$';


-- VALIDATION MODULE 3: 03_null_validation.sql

-- Customer Churn Analysis | Data Validation
-- File: 03_null_validation.sql
-- Purpose: Validate NULL/missing-value patterns.

USE customer_churn_analysis;

-- Customers

SELECT
    COUNT(*) AS total_rows,
    SUM(Customer_ID IS NULL) AS customer_id_nulls,
    SUM(Gender IS NULL) AS gender_nulls,
    SUM(Age IS NULL) AS age_nulls,
    SUM(City IS NULL) AS city_nulls,
    SUM(State IS NULL) AS state_nulls,
    SUM(Signup_Date IS NULL) AS signup_date_nulls
FROM customers;


-- Subscriptions

SELECT
    COUNT(*) AS total_rows,
    SUM(Customer_ID IS NULL) AS customer_id_nulls,
    SUM(Subscription_ID IS NULL) AS subscription_id_nulls,
    SUM(Plan IS NULL) AS plan_nulls,
    SUM(Contract_Type IS NULL) AS contract_type_nulls,
    SUM(Start_Date IS NULL) AS start_date_nulls,
    SUM(End_Date IS NULL) AS end_date_nulls,
    SUM(Monthly_Charge IS NULL) AS monthly_charge_nulls,
    SUM(Churn_Status IS NULL) AS churn_status_nulls,
    SUM(Churn_Date IS NULL) AS churn_date_nulls
FROM subscriptions;


-- Payments

SELECT
    COUNT(*) AS total_rows,
    SUM(Payment_ID IS NULL) AS payment_id_nulls,
    SUM(Customer_ID IS NULL) AS customer_id_nulls,
    SUM(Payment_Date IS NULL) AS payment_date_nulls,
    SUM(Amount IS NULL) AS amount_nulls,
    SUM(Payment_Method IS NULL) AS payment_method_nulls,
    SUM(Payment_Status IS NULL) AS payment_status_nulls
FROM payments;


-- Customer services

SELECT
    COUNT(*) AS total_rows,
    SUM(Customer_ID IS NULL) AS customer_id_nulls,
    SUM(Mobile_App IS NULL) AS mobile_app_nulls,
    SUM(Streaming IS NULL) AS streaming_nulls,
    SUM(Cloud_Storage IS NULL) AS cloud_storage_nulls,
    SUM(Premium_Support IS NULL) AS premium_support_nulls,
    SUM(Family_Plan IS NULL) AS family_plan_nulls
FROM customer_services;


-- Support tickets

SELECT
    COUNT(*) AS total_rows,
    SUM(Ticket_ID IS NULL) AS ticket_id_nulls,
    SUM(Customer_ID IS NULL) AS customer_id_nulls,
    SUM(Ticket_Date IS NULL) AS ticket_date_nulls,
    SUM(Issue_Type IS NULL) AS issue_type_nulls,
    SUM(Resolution_Time_Hours IS NULL) AS resolution_time_nulls,
    SUM(Satisfaction_Score IS NULL) AS satisfaction_score_nulls,
    SUM(Resolved IS NULL) AS resolved_nulls
FROM support_tickets;


-- Important business NULL checks

-- Churn_Date should be NULL for Active customers and populated for
-- Churned customers. This is tested more explicitly in file 06.
SELECT
    Churn_Status,
    COUNT(*) AS rows,
    SUM(Churn_Date IS NULL) AS null_churn_dates
FROM subscriptions
GROUP BY Churn_Status;


-- VALIDATION MODULE 4: 04_duplicate_validation.sql

-- Customer Churn Analysis | Data Validation
-- File: 04_duplicate_validation.sql
-- Purpose: Detect duplicate business records beyond PK checks.

USE customer_churn_analysis;

-- Exact duplicate rows in customers
SELECT
    Customer_ID, Gender, Age, City, State, Signup_Date,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY Customer_ID, Gender, Age, City, State, Signup_Date
HAVING COUNT(*) > 1;

-- Exact duplicate rows in subscriptions
SELECT
    Customer_ID, Subscription_ID, Plan, Contract_Type,
    Start_Date, End_Date, Monthly_Charge, Churn_Status, Churn_Date,
    COUNT(*) AS duplicate_count
FROM subscriptions
GROUP BY Customer_ID, Subscription_ID, Plan, Contract_Type,
         Start_Date, End_Date, Monthly_Charge, Churn_Status, Churn_Date
HAVING COUNT(*) > 1;

-- Exact duplicate rows in payments
SELECT
    Payment_ID, Customer_ID, Payment_Date, Amount,
    Payment_Method, Payment_Status,
    COUNT(*) AS duplicate_count
FROM payments
GROUP BY Payment_ID, Customer_ID, Payment_Date, Amount,
         Payment_Method, Payment_Status
HAVING COUNT(*) > 1;

-- Exact duplicate rows in customer services
SELECT
    Customer_ID, Mobile_App, Streaming, Cloud_Storage,
    Premium_Support, Family_Plan,
    COUNT(*) AS duplicate_count
FROM customer_services
GROUP BY Customer_ID, Mobile_App, Streaming, Cloud_Storage,
         Premium_Support, Family_Plan
HAVING COUNT(*) > 1;

-- Exact duplicate rows in support tickets
SELECT
    Ticket_ID, Customer_ID, Ticket_Date, Issue_Type,
    Resolution_Time_Hours, Satisfaction_Score, Resolved,
    COUNT(*) AS duplicate_count
FROM support_tickets
GROUP BY Ticket_ID, Customer_ID, Ticket_Date, Issue_Type,
         Resolution_Time_Hours, Satisfaction_Score, Resolved
HAVING COUNT(*) > 1;


-- One-to-one relationship check:
-- customer_services should contain at most one row per customer.


SELECT Customer_ID, COUNT(*) AS service_rows
FROM customer_services
GROUP BY Customer_ID
HAVING COUNT(*) > 1;

-- One subscription per customer is expected for this project.
SELECT Customer_ID, COUNT(*) AS subscription_count
FROM subscriptions
GROUP BY Customer_ID
HAVING COUNT(*) > 1;


-- VALIDATION MODULE 5: 05_referential_integrity.sql

-- Customer Churn Analysis | Data Validation
-- File: 05_referential_integrity.sql
-- Purpose: Validate parent-child relationships.

USE customer_churn_analysis;

-- Orphan Customer_ID checks
-- Each query should return zero rows.

SELECT s.Customer_ID
FROM subscriptions s
LEFT JOIN customers c
    ON s.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;

SELECT p.Customer_ID
FROM payments p
LEFT JOIN customers c
    ON p.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;

SELECT cs.Customer_ID
FROM customer_services cs
LEFT JOIN customers c
    ON cs.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;

SELECT st.Customer_ID
FROM support_tickets st
LEFT JOIN customers c
    ON st.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;


-- Summary version

SELECT
    'subscriptions' AS child_table,
    COUNT(*) AS orphan_rows
FROM subscriptions s
LEFT JOIN customers c
    ON s.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL

UNION ALL

SELECT
    'payments',
    COUNT(*)
FROM payments p
LEFT JOIN customers c
    ON p.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL

UNION ALL

SELECT
    'customer_services',
    COUNT(*)
FROM customer_services cs
LEFT JOIN customers c
    ON cs.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL

UNION ALL

SELECT
    'support_tickets',
    COUNT(*)
FROM support_tickets st
LEFT JOIN customers c
    ON st.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;


-- Coverage checks

SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT s.Customer_ID) AS customers_with_subscription
FROM customers c
LEFT JOIN subscriptions s
    ON c.Customer_ID = s.Customer_ID;

SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT cs.Customer_ID) AS customers_with_services
FROM customers c
LEFT JOIN customer_services cs
    ON c.Customer_ID = cs.Customer_ID;


-- VALIDATION MODULE 6: 06_business_rule_validation.sql

-- Customer Churn Analysis | Data Validation
-- File: 06_business_rule_validation.sql
-- Purpose: Validate domain/business rules defined by the project.

USE customer_churn_analysis;

-- CUSTOMERS

-- Age must be 18-75 when populated.
SELECT COUNT(*) AS invalid_age_rows
FROM customers
WHERE Age IS NOT NULL
  AND Age NOT BETWEEN 18 AND 75;

-- Gender after cleaning should be Female/Male.
SELECT Gender, COUNT(*) AS row_count
FROM customers
GROUP BY Gender
ORDER BY row_count DESC;


-- SUBSCRIPTIONS

-- Expected plans
SELECT Plan, COUNT(*) AS row_count
FROM subscriptions
GROUP BY Plan
ORDER BY row_count DESC;

-- Expected contract types
SELECT Contract_Type, COUNT(*) AS row_count
FROM subscriptions
GROUP BY Contract_Type
ORDER BY row_count DESC;

-- Expected churn statuses
SELECT Churn_Status, COUNT(*) AS row_count
FROM subscriptions
GROUP BY Churn_Status
ORDER BY row_count DESC;

-- Churn-status/date consistency
SELECT COUNT(*) AS invalid_churn_date_rows
FROM subscriptions
WHERE (Churn_Status = 'Active' AND Churn_Date IS NOT NULL)
   OR (Churn_Status = 'Churned' AND Churn_Date IS NULL);

-- End date must not precede start date
SELECT COUNT(*) AS invalid_end_dates
FROM subscriptions
WHERE End_Date IS NOT NULL
  AND End_Date < Start_Date;

-- Churn date must not precede start date
SELECT COUNT(*) AS invalid_churn_dates
FROM subscriptions
WHERE Churn_Date IS NOT NULL
  AND Churn_Date < Start_Date;

-- Monthly charge must be non-negative
SELECT COUNT(*) AS invalid_monthly_charge
FROM subscriptions
WHERE Monthly_Charge < 0;

-- Churned customers should have a valid end date in this dataset.
SELECT COUNT(*) AS churned_without_end_date
FROM subscriptions
WHERE Churn_Status = 'Churned'
  AND End_Date IS NULL;

-- Active customers should not have an end date.
SELECT COUNT(*) AS active_with_end_date
FROM subscriptions
WHERE Churn_Status = 'Active'
  AND End_Date IS NOT NULL;


-- PAYMENTS

SELECT Payment_Status, COUNT(*) AS row_count
FROM payments
GROUP BY Payment_Status
ORDER BY row_count DESC;

SELECT Payment_Method, COUNT(*) AS row_count
FROM payments
GROUP BY Payment_Method
ORDER BY row_count DESC;

SELECT COUNT(*) AS invalid_payment_amount
FROM payments
WHERE Amount < 0;

-- Payment date should be within the project's observed period.
SELECT COUNT(*) AS payment_dates_outside_expected_period
FROM payments
WHERE Payment_Date < '2023-01-01'
   OR Payment_Date >= '2026-01-01';


-- CUSTOMER SERVICES

SELECT 'Mobile_App' AS service, Mobile_App AS value, COUNT(*) AS row_count
FROM customer_services
GROUP BY Mobile_App
UNION ALL
SELECT 'Streaming', Streaming, COUNT(*)
FROM customer_services
GROUP BY Streaming
UNION ALL
SELECT 'Cloud_Storage', Cloud_Storage, COUNT(*)
FROM customer_services
GROUP BY Cloud_Storage
UNION ALL
SELECT 'Premium_Support', Premium_Support, COUNT(*)
FROM customer_services
GROUP BY Premium_Support
UNION ALL
SELECT 'Family_Plan', Family_Plan, COUNT(*)
FROM customer_services
GROUP BY Family_Plan
ORDER BY service, row_count DESC;


-- SUPPORT TICKETS

SELECT Issue_Type, COUNT(*) AS row_count
FROM support_tickets
GROUP BY Issue_Type
ORDER BY row_count DESC;

SELECT Resolved, COUNT(*) AS row_count
FROM support_tickets
GROUP BY Resolved
ORDER BY row_count DESC;

SELECT COUNT(*) AS invalid_satisfaction_scores
FROM support_tickets
WHERE Satisfaction_Score NOT BETWEEN 1 AND 5;

SELECT COUNT(*) AS invalid_resolution_times
FROM support_tickets
WHERE Resolution_Time_Hours < 0;

-- Ticket dates should be within the observed project period.
SELECT COUNT(*) AS ticket_dates_outside_expected_period
FROM support_tickets
WHERE Ticket_Date < '2023-01-01'
   OR Ticket_Date >= '2026-01-01';


-- VALIDATION MODULE 7: 07_python_sql_reconciliation.sql

-- Customer Churn Analysis | Data Validation
-- File: 07_python_sql_reconciliation.sql
-- Purpose: Reconcile SQL results with the validated Python results.
--
-- IMPORTANT:
-- SQL can calculate the database-side metrics automatically.
-- Expected Python values should be copied from your final Python
-- validation/summary output into the expected_values CTE below.


USE customer_churn_analysis;

-- 1. SQL summary metrics

WITH sql_metrics AS (
    SELECT
        'customers' AS metric_group,
        COUNT(*) AS total_rows,
        COUNT(DISTINCT Customer_ID) AS distinct_id
    FROM customers

    UNION ALL

    SELECT
        'subscriptions',
        COUNT(*),
        COUNT(DISTINCT Subscription_ID)
    FROM subscriptions

    UNION ALL

    SELECT
        'payments',
        COUNT(*),
        COUNT(DISTINCT Payment_ID)
    FROM payments

    UNION ALL

    SELECT
        'customer_services',
        COUNT(*),
        COUNT(DISTINCT Customer_ID)
    FROM customer_services

    UNION ALL

    SELECT
        'support_tickets',
        COUNT(*),
        COUNT(DISTINCT Ticket_ID)
    FROM support_tickets
)
SELECT *
FROM sql_metrics
ORDER BY metric_group;


-- 2. Subscription reconciliation metrics

SELECT
    COUNT(*) AS total_subscriptions,
    COUNT(DISTINCT Customer_ID) AS unique_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    MIN(Start_Date) AS min_start_date,
    MAX(Start_Date) AS max_start_date
FROM subscriptions;


-- 3. Payment reconciliation metrics

SELECT
    COUNT(*) AS total_payments,
    COUNT(DISTINCT Payment_ID) AS unique_payment_ids,
    COUNT(DISTINCT Customer_ID) AS unique_paying_customers,
    SUM(Payment_Status = 'Successful') AS successful_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(SUM(Amount), 2) AS total_payment_value,
    ROUND(AVG(Amount), 2) AS average_payment_amount,
    MIN(Payment_Date) AS min_payment_date,
    MAX(Payment_Date) AS max_payment_date
FROM payments;


-- 4. Support reconciliation metrics

SELECT
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT Ticket_ID) AS unique_ticket_ids,
    COUNT(DISTINCT Customer_ID) AS unique_ticket_customers,
    SUM(Resolved = 'Yes') AS resolved_tickets,
    SUM(Resolved = 'No') AS unresolved_tickets,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction_score
FROM support_tickets;


-- 5. Python vs SQL comparison template
--
-- Replace the NULL values with metrics from your final Python
-- validation output. Do not invent these values.


WITH expected_values AS (
    SELECT 'customers_rows' AS metric_name, NULL AS python_value
    UNION ALL SELECT 'subscriptions_rows', NULL
    UNION ALL SELECT 'payments_rows', NULL
    UNION ALL SELECT 'customer_services_rows', NULL
    UNION ALL SELECT 'support_tickets_rows', NULL
    UNION ALL SELECT 'total_churned_customers', NULL
    UNION ALL SELECT 'total_active_customers', NULL
),
sql_values AS (
    SELECT 'customers_rows' AS metric_name, COUNT(*) AS sql_value
    FROM customers

    UNION ALL
    SELECT 'subscriptions_rows', COUNT(*)
    FROM subscriptions

    UNION ALL
    SELECT 'payments_rows', COUNT(*)
    FROM payments

    UNION ALL
    SELECT 'customer_services_rows', COUNT(*)
    FROM customer_services

    UNION ALL
    SELECT 'support_tickets_rows', COUNT(*)
    FROM support_tickets

    UNION ALL
    SELECT 'total_churned_customers',
           SUM(Churn_Status = 'Churned')
    FROM subscriptions

    UNION ALL
    SELECT 'total_active_customers',
           SUM(Churn_Status = 'Active')
    FROM subscriptions
)
SELECT
    e.metric_name,
    e.python_value,
    s.sql_value,
    CASE
        WHEN e.python_value IS NULL THEN 'UPDATE PYTHON VALUE'
        WHEN e.python_value = s.sql_value THEN 'PASS'
        ELSE 'FAIL'
    END AS reconciliation_status
FROM expected_values e
JOIN sql_values s
    ON e.metric_name = s.metric_name
ORDER BY e.metric_name;
