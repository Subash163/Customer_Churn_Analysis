/*
Customer Churn & Retention Analysis
SQL - Business Questions


Purpose:
    Consolidated business-question analysis covering customer, churn,
    payment, support, retention, and management perspectives.

Database:
    customer_churn_analysis

Execution:
    Run this script after database design, data loading, validation,
    KPI analysis, churn driver analysis, and retention analysis.

Important:
    - This analytical script does not modify source tables.
    - Each module addresses stakeholder-oriented business questions.
    - Results should be interpreted together with the KPI, churn-driver,
      and retention analysis layers.
*/

USE customer_churn_analysis;

-- MODULE: 01_customer_questions.sql

-- 01_customer_questions.sql
-- Customer Churn Analysis | Business Questions: Customers

-- Q1. How many customers are in the customer base?
SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT Customer_ID) AS unique_customers
FROM customers;

-- Q2. What is the customer demographic profile?
SELECT
    Gender,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS customer_mix_pct,
    ROUND(AVG(Age), 2) AS avg_age
FROM customers
GROUP BY Gender
ORDER BY customers DESC;

-- Q3. Which states have the largest customer bases?
SELECT
    State,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS customer_mix_pct
FROM customers
GROUP BY State
ORDER BY customers DESC;

-- Q4. Which cities have the largest customer bases?
SELECT
    City,
    State,
    COUNT(*) AS customers
FROM customers
GROUP BY City, State
HAVING COUNT(*) >= 50
ORDER BY customers DESC;

-- Q5. How has customer acquisition changed over time?
SELECT
    YEAR(Signup_Date) AS signup_year,
    MONTH(Signup_Date) AS signup_month,
    COUNT(*) AS new_customers
FROM customers
GROUP BY YEAR(Signup_Date), MONTH(Signup_Date)
ORDER BY signup_year, signup_month;

-- Q6. Which signup years produced the largest customer cohorts?
SELECT
    YEAR(Signup_Date) AS signup_year,
    COUNT(*) AS customers
FROM customers
GROUP BY YEAR(Signup_Date)
ORDER BY customers DESC;


-- MODULE: 02_churn_questions.sql

-- 02_churn_questions.sql
-- Customer Churn Analysis | Business Questions: Churn


-- Q1. What is the overall churn rate?
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct
FROM subscriptions;

-- Q2. Which plan has the highest churn rate?
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY Plan
ORDER BY churn_rate_pct DESC;

-- Q3. Which contract type has the highest churn?
SELECT
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY Contract_Type
ORDER BY churn_rate_pct DESC;

-- Q4. When in the customer lifecycle is churn highest?
WITH lifecycle AS (
    SELECT
        Churn_Status,
        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                Start_Date,
                CASE
                    WHEN Churn_Status = 'Churned'
                         AND Churn_Date IS NOT NULL
                        THEN Churn_Date
                    WHEN Churn_Status = 'Active'
                        THEN '2025-12-26'
                    ELSE NULL
                END
            )
        ) AS tenure_months
    FROM subscriptions
)
SELECT
    CASE
        WHEN tenure_months < 3 THEN '0-2 Months'
        WHEN tenure_months < 6 THEN '3-5 Months'
        WHEN tenure_months < 12 THEN '6-11 Months'
        WHEN tenure_months < 24 THEN '12-23 Months'
        ELSE '24+ Months'
    END AS tenure_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM lifecycle
GROUP BY tenure_band
ORDER BY churn_rate_pct DESC;

-- Q5. Which customer segments have both high churn and meaningful volume?
WITH segments AS (
    SELECT
        Plan AS segment,
        COUNT(*) AS customers,
        SUM(Churn_Status = 'Churned') AS churned_customers
    FROM subscriptions
    GROUP BY Plan
)
SELECT
    segment,
    customers,
    churned_customers,
    ROUND(100.0 * churned_customers / customers, 2) AS churn_rate_pct
FROM segments
WHERE customers >= 100
ORDER BY churn_rate_pct DESC, churned_customers DESC;

-- Q6. How much monthly recurring revenue is at risk from churned customers?
SELECT
    ROUND(SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END), 2)
        AS monthly_revenue_at_risk,
    ROUND(
        100.0 * SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END)
        / NULLIF(SUM(Monthly_Charge), 0),
        2
    ) AS revenue_at_risk_pct
FROM subscriptions;


-- MODULE: 03_payment_questions.sql

-- 03_payment_questions.sql
-- Customer Churn Analysis | Business Questions: Payments


-- Q1. What is the overall payment success rate?
SELECT
    COUNT(*) AS total_payments,
    SUM(Payment_Status = 'Successful') AS successful_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(100.0 * SUM(Payment_Status = 'Successful') / COUNT(*), 2)
        AS payment_success_rate_pct,
    ROUND(100.0 * SUM(Payment_Status = 'Failed') / COUNT(*), 2)
        AS payment_failure_rate_pct
FROM payments;

-- Q2. Which payment methods are most used?
SELECT
    Payment_Method,
    COUNT(*) AS payments,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(SUM(Amount), 2) AS payment_value
FROM payments
GROUP BY Payment_Method
ORDER BY payments DESC;

-- Q3. Does payment failure behavior differ between active and churned customers?
WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    s.Churn_Status,
    COUNT(*) AS customers,
    ROUND(AVG(COALESCE(p.failed_payments, 0)), 2) AS avg_failed_payments,
    ROUND(AVG(COALESCE(p.total_payments, 0)), 2) AS avg_total_payments,
    ROUND(
        AVG(
            CASE
                WHEN p.total_payments > 0
                THEN 100.0 * p.successful_payments / p.total_payments
            END
        ),
        2
    ) AS avg_payment_success_rate_pct
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
GROUP BY s.Churn_Status;

-- Q4. Which payment-failure segment has the highest churn?
WITH payment_features AS (
    SELECT
        Customer_ID,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN COALESCE(failed_payments, 0) = 0 THEN 'No Failed Payments'
        WHEN failed_payments = 1 THEN '1 Failed Payment'
        WHEN failed_payments BETWEEN 2 AND 3 THEN '2-3 Failed Payments'
        ELSE '4+ Failed Payments'
    END AS failure_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
GROUP BY failure_band
ORDER BY churn_rate_pct DESC;

-- Q5. Which payment methods have the highest failure rates?
SELECT
    Payment_Method,
    COUNT(*) AS total_payments,
    SUM(Payment_Status = 'Failed') AS failed_payments,
    ROUND(100.0 * SUM(Payment_Status = 'Failed') / COUNT(*), 2)
        AS failure_rate_pct
FROM payments
GROUP BY Payment_Method
HAVING COUNT(*) >= 100
ORDER BY failure_rate_pct DESC;


-- MODULE: 04_support_questions.sql

-- 04_support_questions.sql
-- Customer Churn Analysis | Business Questions: Support

-- Q1. What is the overall support workload?
SELECT
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT Customer_ID) AS customers_with_tickets,
    SUM(Resolved = 'Yes') AS resolved_tickets,
    SUM(Resolved = 'No') AS unresolved_tickets,
    ROUND(100.0 * SUM(Resolved = 'Yes') / COUNT(*), 2) AS resolution_rate_pct,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction
FROM support_tickets;

-- Q2. Which issue types generate the most tickets?
SELECT
    Issue_Type,
    COUNT(*) AS tickets,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction
FROM support_tickets
GROUP BY Issue_Type
ORDER BY tickets DESC;

-- Q3. Does support experience differ between active and churned customers?
WITH support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'No') AS unresolved_tickets,
        AVG(Resolution_Time_Hours) AS avg_resolution_hours,
        AVG(Satisfaction_Score) AS avg_satisfaction
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    s.Churn_Status,
    COUNT(*) AS customers,
    ROUND(AVG(COALESCE(sf.ticket_count, 0)), 2) AS avg_ticket_count,
    ROUND(AVG(COALESCE(sf.unresolved_tickets, 0)), 2) AS avg_unresolved_tickets,
    ROUND(AVG(sf.avg_resolution_hours), 2) AS avg_resolution_hours,
    ROUND(AVG(sf.avg_satisfaction), 2) AS avg_satisfaction
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY s.Churn_Status;

-- Q4. Which ticket-volume segment has the highest churn?
WITH support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN COALESCE(ticket_count, 0) = 0 THEN 'No Tickets'
        WHEN ticket_count = 1 THEN '1 Ticket'
        WHEN ticket_count BETWEEN 2 AND 3 THEN '2-3 Tickets'
        WHEN ticket_count BETWEEN 4 AND 5 THEN '4-5 Tickets'
        ELSE '6+ Tickets'
    END AS ticket_volume_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY ticket_volume_band
ORDER BY churn_rate_pct DESC;

-- Q5. Which issue types are associated with lower retention?
WITH issue_customers AS (
    SELECT DISTINCT Customer_ID, Issue_Type
    FROM support_tickets
)
SELECT
    Issue_Type,
    COUNT(*) AS customers_with_issue,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM issue_customers ic
JOIN subscriptions s ON s.Customer_ID = ic.Customer_ID
GROUP BY Issue_Type
ORDER BY retention_rate_pct ASC;


-- MODULE: 05_retention_questions.sql

-- 05_retention_questions.sql
-- Customer Churn Analysis | Business Questions: Retention

-- Q1. What is the overall customer retention rate?
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions;

-- Q2. Which plan retains customers best?
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions
GROUP BY Plan
ORDER BY retention_rate_pct DESC;

-- Q3. Which contract type provides the strongest retention?
SELECT
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions
GROUP BY Contract_Type
ORDER BY retention_rate_pct DESC;

-- Q4. Does greater service adoption correspond with stronger retention?
WITH service_counts AS (
    SELECT
        Customer_ID,
        (Mobile_App = 'Yes') +
        (Streaming = 'Yes') +
        (Cloud_Storage = 'Yes') +
        (Premium_Support = 'Yes') +
        (Family_Plan = 'Yes') AS service_count
    FROM customer_services
)
SELECT
    service_count,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM service_counts sc
JOIN subscriptions s ON s.Customer_ID = sc.Customer_ID
GROUP BY service_count
ORDER BY service_count;

-- Q5. Which segments have both strong retention and meaningful customer volume?
SELECT
    Plan,
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions
GROUP BY Plan, Contract_Type
HAVING COUNT(*) >= 100
ORDER BY retention_rate_pct DESC;

-- Q6. How much monthly revenue is currently retained?
SELECT
    ROUND(SUM(CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END), 2)
        AS retained_monthly_revenue,
    ROUND(SUM(Monthly_Charge), 2) AS total_monthly_charge_base
FROM subscriptions;


-- MODULE: 06_management_questions.sql

-- 06_management_questions.sql
-- Customer Churn Analysis | Business / Management Questions


-- Q1. Where should management focus first: highest churn rate or
-- highest number of churned customers?
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(
        SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END),
        2
    ) AS monthly_revenue_at_risk
FROM subscriptions
GROUP BY Plan
HAVING COUNT(*) >= 100
ORDER BY churned_customers DESC;

-- Q2. Which plan + contract combination represents the greatest
-- revenue risk?
SELECT
    Plan,
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(
        SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END),
        2
    ) AS monthly_revenue_at_risk
FROM subscriptions
GROUP BY Plan, Contract_Type
HAVING COUNT(*) >= 100
ORDER BY monthly_revenue_at_risk DESC;

-- Q3. Which high-value active customers show multiple retention-risk signals?
WITH payment_features AS (
    SELECT
        Customer_ID,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
),
support_features AS (
    SELECT
        Customer_ID,
        SUM(Resolved = 'No') AS unresolved_tickets,
        AVG(Satisfaction_Score) AS avg_satisfaction
    FROM support_tickets
    GROUP BY Customer_ID
),
service_features AS (
    SELECT
        Customer_ID,
        (Mobile_App = 'Yes') +
        (Streaming = 'Yes') +
        (Cloud_Storage = 'Yes') +
        (Premium_Support = 'Yes') +
        (Family_Plan = 'Yes') AS service_count
    FROM customer_services
),
ranked AS (
    SELECT
        s.*,
        NTILE(4) OVER (ORDER BY s.Monthly_Charge) AS charge_quartile,
        COALESCE(p.failed_payments, 0) AS failed_payments,
        COALESCE(su.unresolved_tickets, 0) AS unresolved_tickets,
        su.avg_satisfaction,
        COALESCE(se.service_count, 0) AS service_count
    FROM subscriptions s
    LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
    LEFT JOIN support_features su ON su.Customer_ID = s.Customer_ID
    LEFT JOIN service_features se ON se.Customer_ID = s.Customer_ID
)
SELECT
    Customer_ID,
    Plan,
    Contract_Type,
    Monthly_Charge,
    failed_payments,
    unresolved_tickets,
    ROUND(avg_satisfaction, 2) AS avg_satisfaction,
    service_count,
    (
        (failed_payments >= 1) +
        (unresolved_tickets >= 1 OR avg_satisfaction < 4) +
        (service_count <= 1)
    ) AS risk_factor_count
FROM ranked
WHERE Churn_Status = 'Active'
  AND charge_quartile = 4
  AND (
        (failed_payments >= 1) +
        (unresolved_tickets >= 1 OR avg_satisfaction < 4) +
        (service_count <= 1)
      ) >= 2
ORDER BY risk_factor_count DESC, Monthly_Charge DESC
LIMIT 100;

-- Q4. What is the combined monthly revenue at risk from churned
-- customers with payment or support risk?
WITH payment_features AS (
    SELECT
        Customer_ID,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
),
support_features AS (
    SELECT
        Customer_ID,
        SUM(Resolved = 'No') AS unresolved_tickets,
        AVG(Satisfaction_Score) AS avg_satisfaction
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    COUNT(*) AS churned_risk_customers,
    ROUND(SUM(s.Monthly_Charge), 2) AS monthly_revenue_at_risk
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
LEFT JOIN support_features su ON su.Customer_ID = s.Customer_ID
WHERE s.Churn_Status = 'Churned'
  AND (
        COALESCE(p.failed_payments, 0) >= 1
        OR COALESCE(su.unresolved_tickets, 0) >= 1
        OR su.avg_satisfaction < 4
      );

-- Q5. Which states combine a large customer base with high churn?
SELECT
    c.State,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY c.State
HAVING COUNT(*) >= 100
ORDER BY churned_customers DESC;

-- Q6. Executive churn scorecard.
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(SUM(Monthly_Charge), 2) AS total_monthly_charge_base,
    ROUND(SUM(CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END), 2)
        AS retained_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END), 2)
        AS monthly_revenue_at_risk
FROM subscriptions;
