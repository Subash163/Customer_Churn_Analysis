/*
Customer Churn & Retention Analysis
SQL - Retention Analysis

Purpose:
    Consolidated retention analysis covering lifecycle, subscription,
    payment, service, support, and high-value customer retention.

Database:
    customer_churn_analysis

Execution:
    Run this script after database design, data loading, validation,
    and KPI analysis.

Important:
    - This analytical script does not modify source tables.
    - Payments and support_tickets are one-to-many tables. The source
      modules aggregate them to customer level before joining where required.
    - Retention is generally measured as Active Customers / Total Customers.
    - High-value customers are defined using the methodology in the
      high-value retention module.


*/

USE customer_churn_analysis;
 
-- MODULE: 01_retention_by_lifecycle.sql

-- 01_retention_by_lifecycle.sql
-- Customer Churn Analysis | Retention by Lifecycle

-- 1. Retention by tenure band.
-- For active customers, CURDATE() is used as the current reference date.
-- For churned customers, tenure is measured until Churn_Date.
-- Customer Churn Analysis | Retention by Lifecycle
-- Query 1: Retention Rate by Lifecycle / Tenure Band
-- Analytical cutoff: 2025-12-26

WITH lifecycle AS (
    SELECT
        Customer_ID,
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

    SUM(Churn_Status = 'Active') AS retained_customers,

    SUM(Churn_Status = 'Churned') AS churned_customers,

    ROUND(
        100.0 * SUM(Churn_Status = 'Active') / COUNT(*),
        2
    ) AS retention_rate_pct

FROM lifecycle

GROUP BY
    tenure_band

ORDER BY
    MIN(tenure_months);

-- 2. Active customer tenure profile.
-- Customer Churn Analysis | Retention by Lifecycle
-- Query 2: Active Customer Tenure Profile
-- Analytical cutoff: 2025-12-26

SELECT
    COUNT(*) AS active_customers,
    ROUND(
        AVG(
            GREATEST(
                0,
                TIMESTAMPDIFF(
                    MONTH,
                    Start_Date,
                    '2025-12-26'
                )
            )
        ),
        2
    ) AS avg_active_tenure_months,
    MIN(
        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                Start_Date,
                '2025-12-26'
            )
        )
    ) AS min_active_tenure_months,
    MAX(
        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                Start_Date,
                '2025-12-26'
            )
        )
    ) AS max_active_tenure_months
FROM subscriptions
WHERE Churn_Status = 'Active';

-- MODULE: 02_retention_by_plan.sql

-- 02_retention_by_plan.sql
-- Customer Churn Analysis | Retention by Plan

-- 1. Retention by plan.
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Plan
ORDER BY retention_rate_pct DESC;

-- 2. Retention by plan + contract.
SELECT
    Plan,
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END), 2) AS retained_monthly_revenue
FROM subscriptions
GROUP BY Plan, Contract_Type
HAVING COUNT(*) >= 20
ORDER BY retention_rate_pct DESC;

-- 3. Revenue retained by plan.
SELECT
    Plan,
    ROUND(SUM(CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END), 2)
        AS retained_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END), 2)
        AS churned_monthly_revenue_at_risk
FROM subscriptions
GROUP BY Plan
ORDER BY retained_monthly_revenue DESC;


-- MODULE: 03_retention_by_contract.sql

-- 03_retention_by_contract.sql
-- Customer Churn Analysis | Retention by Contract

-- 1. Retention by contract type.
SELECT
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Contract_Type
ORDER BY retention_rate_pct DESC;

-- 2. Contract retention within each plan.
SELECT
    Plan,
    Contract_Type,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(
        100.0 * SUM(
            CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END
        ) / NULLIF(SUM(Monthly_Charge), 0),
        2
    ) AS revenue_retention_pct
FROM subscriptions
GROUP BY Plan, Contract_Type
HAVING COUNT(*) >= 20
ORDER BY Plan, retention_rate_pct DESC;

-- 3. Active customer mix by contract.
SELECT
    Contract_Type,
    COUNT(*) AS active_customers,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS active_customer_mix_pct
FROM subscriptions
WHERE Churn_Status = 'Active'
GROUP BY Contract_Type
ORDER BY active_customers DESC;


-- MODULE: 04_retention_by_payment.sql

-- 04_retention_by_payment.sql
-- Customer Churn Analysis | Retention by Payment Behavior

-- IMPORTANT:
-- payments is one-to-many per customer. Aggregate before joining.

WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments,
        ROUND(100.0 * SUM(Payment_Status = 'Successful') / COUNT(*), 2)
            AS payment_success_rate_pct,
        ROUND(SUM(Amount), 2) AS total_payment_value
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN COALESCE(p.failed_payments, 0) = 0 THEN 'No Failed Payments'
        WHEN p.failed_payments = 1 THEN '1 Failed Payment'
        WHEN p.failed_payments BETWEEN 2 AND 3 THEN '2-3 Failed Payments'
        ELSE '4+ Failed Payments'
    END AS payment_failure_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct,
    ROUND(AVG(COALESCE(p.payment_success_rate_pct, 0)), 2)
        AS avg_payment_success_rate_pct
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
GROUP BY payment_failure_band
ORDER BY retention_rate_pct DESC;

-- 2. Retention by payment success rate.
WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN 100.0 * successful_payments / NULLIF(total_payments, 0) < 80
            THEN '<80%'
        WHEN 100.0 * successful_payments / NULLIF(total_payments, 0) < 95
            THEN '80-94%'
        ELSE '95-100%'
    END AS payment_success_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM payment_features p
JOIN subscriptions s ON s.Customer_ID = p.Customer_ID
GROUP BY payment_success_band
ORDER BY retention_rate_pct DESC;

-- 3. Retention by primary payment method.
WITH method_counts AS (
    SELECT Customer_ID, Payment_Method, COUNT(*) AS method_count
    FROM payments
    GROUP BY Customer_ID, Payment_Method
),
ranked_methods AS (
    SELECT
        Customer_ID,
        Payment_Method,
        method_count,
        ROW_NUMBER() OVER (
            PARTITION BY Customer_ID
            ORDER BY method_count DESC, Payment_Method
        ) AS rn
    FROM method_counts
)
SELECT
    rm.Payment_Method AS primary_payment_method,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM ranked_methods rm
JOIN subscriptions s ON s.Customer_ID = rm.Customer_ID
WHERE rm.rn = 1
GROUP BY rm.Payment_Method
ORDER BY retention_rate_pct DESC;


-- MODULE: 05_retention_by_service.sql

-- 05_retention_by_service.sql
-- Customer Churn Analysis | Retention by Service Adoption

-- 1. Retention by individual service.
WITH service_flags AS (
    SELECT Customer_ID, 'Mobile_App' AS service_name, Mobile_App AS service_value
    FROM customer_services
    UNION ALL
    SELECT Customer_ID, 'Streaming', Streaming FROM customer_services
    UNION ALL
    SELECT Customer_ID, 'Cloud_Storage', Cloud_Storage FROM customer_services
    UNION ALL
    SELECT Customer_ID, 'Premium_Support', Premium_Support FROM customer_services
    UNION ALL
    SELECT Customer_ID, 'Family_Plan', Family_Plan FROM customer_services
)
SELECT
    service_name,
    service_value,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM service_flags sf
JOIN subscriptions s ON s.Customer_ID = sf.Customer_ID
GROUP BY service_name, service_value
ORDER BY service_name, retention_rate_pct DESC;

-- 2. Retention by number of adopted services.
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
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM service_counts sc
JOIN subscriptions s ON s.Customer_ID = sc.Customer_ID
GROUP BY service_count
ORDER BY service_count;

-- 3. Retention by service-adoption band.
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
    CASE
        WHEN service_count <= 1 THEN '0-1 Services'
        WHEN service_count <= 3 THEN '2-3 Services'
        ELSE '4-5 Services'
    END AS service_adoption_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM service_counts sc
JOIN subscriptions s ON s.Customer_ID = sc.Customer_ID
GROUP BY service_adoption_band
ORDER BY retention_rate_pct DESC;


-- MODULE: 06_retention_by_support.sql

-- 06_retention_by_support.sql
-- Customer Churn Analysis | Retention by Support Experience


-- IMPORTANT:
-- support_tickets is one-to-many. Aggregate to customer level first.

WITH support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'No') AS unresolved_tickets,
        ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
        ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction
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
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY ticket_volume_band
ORDER BY retention_rate_pct DESC;

-- 2. Retention by satisfaction.
WITH support_features AS (
    SELECT
        Customer_ID,
        AVG(Satisfaction_Score) AS avg_satisfaction
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN avg_satisfaction < 2 THEN '1-<2'
        WHEN avg_satisfaction < 3 THEN '2-<3'
        WHEN avg_satisfaction < 4 THEN '3-<4'
        ELSE '4-5'
    END AS satisfaction_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM support_features sf
JOIN subscriptions s ON s.Customer_ID = sf.Customer_ID
GROUP BY satisfaction_band
ORDER BY retention_rate_pct DESC;

-- 3. Retention by unresolved tickets.
WITH support_features AS (
    SELECT
        Customer_ID,
        SUM(Resolved = 'No') AS unresolved_tickets
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN COALESCE(unresolved_tickets, 0) = 0 THEN 'No Unresolved Tickets'
        WHEN unresolved_tickets = 1 THEN '1 Unresolved Ticket'
        ELSE '2+ Unresolved Tickets'
    END AS unresolved_ticket_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY unresolved_ticket_band
ORDER BY retention_rate_pct DESC;

-- 4. Retention by issue type.
WITH issue_customers AS (
    SELECT DISTINCT Customer_ID, Issue_Type
    FROM support_tickets
)
SELECT
    ic.Issue_Type,
    COUNT(*) AS customers_with_issue,
    SUM(s.Churn_Status = 'Active') AS retained_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct
FROM issue_customers ic
JOIN subscriptions s ON s.Customer_ID = ic.Customer_ID
GROUP BY ic.Issue_Type
ORDER BY retention_rate_pct DESC;


-- MODULE: 07_high_value_retention.sql

-- 07_high_value_retention.sql
-- Customer Churn Analysis | High-Value Customer Retention


-- 1. Define high-value customers using the top 25% of monthly charge.
-- NTILE(4) creates quartiles; quartile 4 represents the highest-value
-- monthly-charge group.

WITH ranked_customers AS (
    SELECT
        Customer_ID,
        Plan,
        Contract_Type,
        Monthly_Charge,
        Churn_Status,
        NTILE(4) OVER (ORDER BY Monthly_Charge) AS charge_quartile
    FROM subscriptions
)
SELECT
    CASE
        WHEN charge_quartile = 4 THEN 'High Value (Top 25%)'
        ELSE 'Other Customers'
    END AS value_segment,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'Active' THEN Monthly_Charge ELSE 0 END), 2)
        AS retained_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END), 2)
        AS monthly_revenue_at_risk
FROM ranked_customers
GROUP BY value_segment
ORDER BY retention_rate_pct DESC;

-- 2. High-value retention by plan.
WITH ranked_customers AS (
    SELECT
        Customer_ID,
        Plan,
        Contract_Type,
        Monthly_Charge,
        Churn_Status,
        NTILE(4) OVER (ORDER BY Monthly_Charge) AS charge_quartile
    FROM subscriptions
)
SELECT
    Plan,
    COUNT(*) AS high_value_customers,
    SUM(Churn_Status = 'Active') AS retained_customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Active') / COUNT(*), 2)
        AS retention_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'Churned' THEN Monthly_Charge ELSE 0 END), 2)
        AS monthly_revenue_at_risk
FROM ranked_customers
WHERE charge_quartile = 4
GROUP BY Plan
ORDER BY monthly_revenue_at_risk DESC;

-- 3. High-value customers with multiple retention-risk signals.
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
),
risk AS (
    SELECT *,
        (failed_payments >= 1) +
        (unresolved_tickets >= 1 OR avg_satisfaction < 4) +
        (service_count <= 1) AS risk_factor_count
    FROM ranked
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
    risk_factor_count
FROM risk
WHERE charge_quartile = 4
  AND Churn_Status = 'Active'
  AND risk_factor_count >= 2
ORDER BY risk_factor_count DESC, Monthly_Charge DESC;
