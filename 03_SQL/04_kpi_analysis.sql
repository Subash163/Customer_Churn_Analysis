-- Customer Churn Analysis | KPI Analysis
-- File: kpi_analysis.sql
-- Purpose: Combined KPI analysis script for the Customer Churn
--          Analysis project.
--
-- KPI modules:
-- 1. Customer KPIs
-- 2. Churn KPIs
-- 3. Retention KPIs
-- 4. Subscription KPIs
-- 5. Payment KPIs
-- 6. Support KPIs
--
-- Execution:
-- Run after database design, data loading and data validation.
--
-- IMPORTANT:
-- This is an analytical layer. The queries are SELECT statements
-- and do not modify the source tables.
--
-- Data-grain warning:
-- payments and support_tickets are one-to-many tables. Avoid
-- directly joining both to each other before aggregating to the
-- appropriate customer-level grain.


USE customer_churn_analysis;

-- KPI MODULE 1: 01_customer_kpis.sql

-- Customer Churn Analysis | KPI Analysis
-- File: 01_customer_kpis.sql
-- Purpose: Core customer-base KPIs.

-- 1. Customer base overview

SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT Customer_ID) AS unique_customers,
    SUM(Age IS NULL) AS customers_missing_age,
    ROUND(AVG(Age), 2) AS average_customer_age,
    MIN(Age) AS minimum_age,
    MAX(Age) AS maximum_age
FROM customers;


-- 2. Customers by gender

SELECT
    Gender,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS customer_share_pct
FROM customers
GROUP BY Gender
ORDER BY customers DESC;


-- 3. Customers by state

SELECT
    State,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS customer_share_pct
FROM customers
GROUP BY State
ORDER BY customers DESC;


-- 4. Customers by city

SELECT
    COALESCE(City, 'Missing') AS City,
    COUNT(*) AS customers,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_share_pct
FROM customers
GROUP BY City
ORDER BY customers DESC;


-- 5. Customer signup trend by month

SELECT
    DATE_FORMAT(Signup_Date, '%Y-%m') AS signup_month,
    COUNT(*) AS new_customers
FROM customers
GROUP BY DATE_FORMAT(Signup_Date, '%Y-%m')
ORDER BY signup_month;


-- 6. Customer signup trend by year

SELECT
    YEAR(Signup_Date) AS signup_year,
    COUNT(*) AS new_customers
FROM customers
GROUP BY YEAR(Signup_Date)
ORDER BY signup_year;


-- KPI MODULE 2: 02_churn_kpis.sql

-- Customer Churn Analysis | KPI Analysis
-- File: 02_churn_kpis.sql
-- Purpose: Core churn KPIs and churn segmentation.

-- 1. Overall churn KPIs

SELECT
    COUNT(*) AS total_subscriptions,
    COUNT(DISTINCT Customer_ID) AS total_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct,
    ROUND(
        100.0 * SUM(Churn_Status = 'Active') / COUNT(*),
        2
    ) AS active_rate_pct
FROM subscriptions;


-- 2. Churn by plan

SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM subscriptions
GROUP BY Plan
ORDER BY churn_rate_pct DESC;


-- 3. Churn by contract type

SELECT
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM subscriptions
GROUP BY Contract_Type
ORDER BY churn_rate_pct DESC;


-- 4. Churn by monthly-charge band

SELECT
    CASE
        WHEN Monthly_Charge < 400 THEN '<400'
        WHEN Monthly_Charge < 600 THEN '400-599.99'
        WHEN Monthly_Charge < 800 THEN '600-799.99'
        ELSE '800+'
    END AS monthly_charge_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM subscriptions
GROUP BY
    CASE
        WHEN Monthly_Charge < 400 THEN '<400'
        WHEN Monthly_Charge < 600 THEN '400-599.99'
        WHEN Monthly_Charge < 800 THEN '600-799.99'
        ELSE '800+'
    END
ORDER BY MIN(Monthly_Charge);


-- 5. Churn trend by churn month

SELECT
    DATE_FORMAT(Churn_Date, '%Y-%m') AS churn_month,
    COUNT(*) AS churned_customers
FROM subscriptions
WHERE Churn_Status = 'Churned'
  AND Churn_Date IS NOT NULL
GROUP BY DATE_FORMAT(Churn_Date, '%Y-%m')
ORDER BY churn_month;


-- 6. Churn by customer age band

SELECT
    CASE
        WHEN c.Age < 25 THEN '<25'
        WHEN c.Age < 35 THEN '25-34'
        WHEN c.Age < 45 THEN '35-44'
        WHEN c.Age < 55 THEN '45-54'
        WHEN c.Age >= 55 THEN '55+'
        ELSE 'Unknown'
    END AS age_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customers c
JOIN subscriptions s
    ON c.Customer_ID = s.Customer_ID
GROUP BY
    CASE
        WHEN c.Age < 25 THEN '<25'
        WHEN c.Age < 35 THEN '25-34'
        WHEN c.Age < 45 THEN '35-44'
        WHEN c.Age < 55 THEN '45-54'
        WHEN c.Age >= 55 THEN '55+'
        ELSE 'Unknown'
    END
ORDER BY churn_rate_pct DESC;


-- 7. Churn by gender

SELECT
    c.Gender,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customers c
JOIN subscriptions s
    ON c.Customer_ID = s.Customer_ID
GROUP BY c.Gender
ORDER BY churn_rate_pct DESC;


-- KPI MODULE 3: 03_retention_kpis.sql

-- Customer Churn Analysis | KPI Analysis
-- File: 03_retention_kpis.sql
-- Purpose: Core retention KPIs and customer tenure metrics.

-- 1. Overall retention rate
-- Definition:
-- Retention rate = active customers / total customers.

SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Active') / COUNT(*),
        2
    ) AS retention_rate_pct,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM subscriptions;


-- 2. Average customer tenure in months
-- Active customers: from Start_Date to current project reference date.
-- Churned customers: from Start_Date to Churn_Date.
-- Reference date is the latest date in the subscription dataset.

-- Retention KPI 2: Average customer tenure
-- Purpose: Compares average observed tenure of all,
--          churned, and active customers.
-- Analysis cutoff: 2025-12-26

WITH tenure AS (
    SELECT
        Customer_ID,
        Churn_Status,
        CASE
            WHEN Churn_Status = 'Churned'
                 AND Churn_Date IS NOT NULL
                THEN TIMESTAMPDIFF(MONTH, Start_Date, Churn_Date)
            ELSE TIMESTAMPDIFF(
                MONTH,
                Start_Date,
                '2025-12-26'
            )
        END AS tenure_months
    FROM subscriptions
)
SELECT
    ROUND(AVG(tenure_months), 2) AS average_tenure_months,
    ROUND(
        AVG(
            CASE
                WHEN Churn_Status = 'Churned'
                THEN tenure_months
            END
        ), 2
    ) AS avg_churned_tenure_months,
    ROUND(
        AVG(
            CASE
                WHEN Churn_Status = 'Active'
                THEN tenure_months
            END
        ), 2
    ) AS avg_active_tenure_months
FROM tenure;


-- 3. Retention by customer tenure band

-- Retention KPI 3: Retention by tenure band
-- Purpose: Compares customer retention across observed tenure groups.
-- Analysis cutoff: 2025-12-26

WITH tenure AS (
    SELECT
        Customer_ID,
        Churn_Status,
        CASE
            WHEN Churn_Status = 'Churned'
                 AND Churn_Date IS NOT NULL
                THEN TIMESTAMPDIFF(MONTH, Start_Date, Churn_Date)
            ELSE TIMESTAMPDIFF(
                MONTH,
                Start_Date,
                '2025-12-26'
            )
        END AS tenure_months
    FROM subscriptions
)
SELECT
    CASE
        WHEN tenure_months < 3 THEN '<3 months'
        WHEN tenure_months < 6 THEN '3-5 months'
        WHEN tenure_months < 12 THEN '6-11 months'
        WHEN tenure_months < 24 THEN '12-23 months'
        ELSE '24+ months'
    END AS tenure_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Active') / COUNT(*),
        2
    ) AS retention_rate_pct
FROM tenure
GROUP BY
    CASE
        WHEN tenure_months < 3 THEN '<3 months'
        WHEN tenure_months < 6 THEN '3-5 months'
        WHEN tenure_months < 12 THEN '6-11 months'
        WHEN tenure_months < 24 THEN '12-23 months'
        ELSE '24+ months'
    END
ORDER BY MIN(tenure_months);


-- 4. Active customers by signup year

-- Retention KPI 4: Retention by signup cohort/year
-- Purpose: Compares current active/churned status across signup cohorts.
-- Analysis cutoff: 2025-12-26
-- Note: Cohorts have different observation periods and should
--       not be interpreted as directly comparable lifetime retention.

SELECT
    YEAR(c.Signup_Date) AS signup_cohort_year,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS active_customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*),
        2
    ) AS retention_rate_pct,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customers c
JOIN subscriptions s
    ON c.Customer_ID = s.Customer_ID
GROUP BY YEAR(c.Signup_Date)
ORDER BY signup_cohort_year;


-- KPI MODULE 4: 04_subscription_kpis.sql


-- Customer Churn Analysis | KPI Analysis
-- File: 04_subscription_kpis.sql
-- Purpose: Subscription mix, revenue and pricing KPIs.

-- 1. Subscription portfolio overview

SELECT
    COUNT(*) AS total_subscriptions,
    COUNT(DISTINCT Customer_ID) AS unique_customers,
    COUNT(DISTINCT Plan) AS number_of_plans,
    COUNT(DISTINCT Contract_Type) AS number_of_contract_types,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(MIN(Monthly_Charge), 2) AS min_monthly_charge,
    ROUND(MAX(Monthly_Charge), 2) AS max_monthly_charge
FROM subscriptions;


-- 2. Subscription mix by plan

SELECT
    Plan,
    COUNT(*) AS subscriptions,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS subscription_share_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_recurring_charge
FROM subscriptions
GROUP BY Plan
ORDER BY subscriptions DESC;


-- 3. Subscription mix by contract

SELECT
    Contract_Type,
    COUNT(*) AS subscriptions,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS subscription_share_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_recurring_charge
FROM subscriptions
GROUP BY Contract_Type
ORDER BY subscriptions DESC;


-- 4. Estimated Monthly Recurring Revenue (MRR)
-- Based on active subscriptions only.

SELECT
    COUNT(*) AS active_subscriptions,
    ROUND(SUM(Monthly_Charge), 2) AS estimated_mrr,
    ROUND(AVG(Monthly_Charge), 2) AS avg_active_monthly_charge
FROM subscriptions
WHERE Churn_Status = 'Active';


-- 5. Estimated MRR at risk from churned subscriptions

SELECT
    COUNT(*) AS churned_subscriptions,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_revenue_at_risk,
    ROUND(AVG(Monthly_Charge), 2) AS avg_churned_monthly_charge
FROM subscriptions
WHERE Churn_Status = 'Churned';


-- 6. MRR by plan and churn status

SELECT
    Plan,
    Churn_Status,
    COUNT(*) AS subscriptions,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_charge_value,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Plan, Churn_Status
ORDER BY Plan, Churn_Status;


-- KPI MODULE 5: 05_payment_kpis.sql

-- Customer Churn Analysis | KPI Analysis
-- File: 05_payment_kpis.sql
-- Purpose: Payment volume, success, failure and customer payment KPIs.


-- 1. Overall payment KPIs

SELECT
    COUNT(*) AS total_payments,
    COUNT(DISTINCT Payment_ID) AS unique_payments,
    COUNT(DISTINCT Customer_ID) AS paying_customers,
    ROUND(SUM(Amount), 2) AS total_payment_value,
    ROUND(AVG(Amount), 2) AS average_payment_amount,
    SUM(Payment_Status = 'Successful') AS successful_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(
        100.0 * SUM(Payment_Status = 'Successful') / COUNT(*),
        2
    ) AS payment_success_rate_pct,
    ROUND(
        100.0 * SUM(Payment_Status = 'Failed') / COUNT(*),
        2
    ) AS payment_failure_rate_pct
FROM payments;

-- 2. Payment KPIs by payment method

SELECT
    Payment_Method,
    COUNT(*) AS payments,
    ROUND(SUM(Amount), 2) AS payment_value,
    ROUND(AVG(Amount), 2) AS avg_payment_amount,
    SUM(Payment_Status = 'Successful') AS successful_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(
        100.0 * SUM(Payment_Status = 'Successful') / COUNT(*),
        2
    ) AS success_rate_pct
FROM payments
GROUP BY Payment_Method
ORDER BY payments DESC;


-- 3. Monthly payment trend

SELECT
    DATE_FORMAT(Payment_Date, '%Y-%m') AS payment_month,
    COUNT(*) AS payments,
    ROUND(SUM(Amount), 2) AS payment_value,
    ROUND(AVG(Amount), 2) AS avg_payment_amount,
    SUM(Payment_Status = 'Failed') AS failed_payments
FROM payments
GROUP BY DATE_FORMAT(Payment_Date, '%Y-%m')
ORDER BY payment_month;


-- 4. Customer-level payment KPIs

SELECT
    Customer_ID,
    COUNT(*) AS total_payments,
    ROUND(SUM(Amount), 2) AS total_payment_value,
    ROUND(AVG(Amount), 2) AS avg_payment_amount,
    SUM(Payment_Status = 'Successful') AS successful_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(
        100.0 * SUM(Payment_Status = 'Failed') / COUNT(*),
        2
    ) AS failure_rate_pct
FROM payments
GROUP BY Customer_ID
ORDER BY total_payment_value DESC;


-- 5. Payment behavior by churn status

SELECT
    s.Churn_Status,
    COUNT(DISTINCT s.Customer_ID) AS customers,
    COUNT(p.Payment_ID) AS payments,
    ROUND(SUM(p.Amount), 2) AS payment_value,
    ROUND(AVG(p.Amount), 2) AS avg_payment_amount,
    SUM(p.Payment_Status = 'Failed') AS failed_payments,
    ROUND(
        100.0 * SUM(p.Payment_Status = 'Failed') / COUNT(p.Payment_ID),
        2
    ) AS payment_failure_rate_pct
FROM subscriptions s
LEFT JOIN payments p
    ON s.Customer_ID = p.Customer_ID
GROUP BY s.Churn_Status
ORDER BY s.Churn_Status;


-- KPI MODULE 6: 06_support_kpis.sql

-- Customer Churn Analysis | KPI Analysis
-- File: 06_support_kpis.sql
-- Purpose: Support volume, resolution and satisfaction KPIs.

-- 1. Overall support KPIs

SELECT
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT Ticket_ID) AS unique_tickets,
    COUNT(DISTINCT Customer_ID) AS customers_with_tickets,
    SUM(Resolved = 'Yes') AS resolved_tickets,
    SUM(Resolved = 'No') AS unresolved_tickets,
    ROUND(
        100.0 * SUM(Resolved = 'Yes') / COUNT(*),
        2
    ) AS resolution_rate_pct,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_time_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction_score
FROM support_tickets;


-- 2. Support KPIs by issue type

SELECT
    Issue_Type,
    COUNT(*) AS tickets,
    COUNT(DISTINCT Customer_ID) AS customers,
    SUM(Resolved = 'Yes') AS resolved_tickets,
    ROUND(
        100.0 * SUM(Resolved = 'Yes') / COUNT(*),
        2
    ) AS resolution_rate_pct,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction_score
FROM support_tickets
GROUP BY Issue_Type
ORDER BY tickets DESC;


-- 3. Monthly support trend

SELECT
    DATE_FORMAT(Ticket_Date, '%Y-%m') AS ticket_month,
    COUNT(*) AS tickets,
    COUNT(DISTINCT Customer_ID) AS customers,
    SUM(Resolved = 'Yes') AS resolved_tickets,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction_score
FROM support_tickets
GROUP BY DATE_FORMAT(Ticket_Date, '%Y-%m')
ORDER BY ticket_month;


-- 4. Support behavior by churn status

SELECT
    s.Churn_Status,
    COUNT(DISTINCT s.Customer_ID) AS customers,
    COUNT(st.Ticket_ID) AS tickets,
    ROUND(
        COUNT(st.Ticket_ID) / COUNT(DISTINCT s.Customer_ID),
        2
    ) AS avg_tickets_per_customer,
    ROUND(AVG(st.Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(st.Satisfaction_Score), 2) AS avg_satisfaction_score,
    ROUND(
        100.0 * SUM(st.Resolved = 'Yes') / NULLIF(COUNT(st.Ticket_ID), 0),
        2
    ) AS resolution_rate_pct
FROM subscriptions s
LEFT JOIN support_tickets st
    ON s.Customer_ID = st.Customer_ID
GROUP BY s.Churn_Status
ORDER BY s.Churn_Status;


-- 5. Customers with high support-ticket volume

SELECT
    Customer_ID,
    COUNT(*) AS ticket_count,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction_score,
    SUM(Resolved = 'No') AS unresolved_tickets
FROM support_tickets
GROUP BY Customer_ID
HAVING COUNT(*) >= 3
ORDER BY ticket_count DESC, avg_satisfaction_score ASC;
