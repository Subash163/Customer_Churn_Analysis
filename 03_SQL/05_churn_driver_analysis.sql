-- Customer Churn Analysis | Churn Driver Analysis
-- File: churn_driver_analysis.sql
-- Purpose: Combined churn-driver analysis across lifecycle,
--          subscription, payment, service, support, engagement,
--          customer profile and multidimensional risk factors.
--
-- Modules:
-- 1. Lifecycle Churn
-- 2. Subscription Churn
-- 3. Payment Churn
-- 4. Service Adoption Churn
-- 5. Support Churn
-- 6. Engagement / Activity Signals
-- 7. Customer Profile Churn
-- 8. Multidimensional Churn
--
-- Execution:
-- Run after database design, data loading, data validation
-- and KPI analysis.
--
-- IMPORTANT DATA-GRAIN WARNING:
-- subscriptions is the churn anchor at customer/subscription grain.
-- payments and support_tickets are one-to-many tables per customer.
-- Aggregate these tables to customer level before joining them
-- to subscriptions to avoid row multiplication.
--
-- ANALYTICAL NOTE:
-- These queries identify descriptive churn associations and risk
-- segments. They should not be interpreted as proof of causation.
--

USE customer_churn_analysis;

-- MODULE: LIFECYCLE CHURN | 01_lifecycle_churn.sql

-- 01_lifecycle_churn.sql
-- Customer Churn Analysis | Lifecycle Churn Drivers

-- 1. Churn rate by customer tenure at churn / current tenure.
-- Lifecycle Churn Driver Analysis
-- Query 1: Churn Rate by Observed Tenure Band
-- Analytical cutoff: 2025-12-26

WITH lifecycle AS (
    SELECT
        s.Customer_ID,
        s.Churn_Status,
        CASE
            WHEN s.Churn_Status = 'Churned'
                 AND s.Churn_Date IS NOT NULL
                THEN TIMESTAMPDIFF(
                    MONTH,
                    s.Start_Date,
                    s.Churn_Date
                )

            WHEN s.Churn_Status = 'Active'
                THEN TIMESTAMPDIFF(
                    MONTH,
                    s.Start_Date,
                    '2025-12-26'
                )

            ELSE NULL
        END AS tenure_months
    FROM subscriptions s
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

WHERE tenure_months IS NOT NULL

GROUP BY
    CASE
        WHEN tenure_months < 3 THEN '0-2 Months'
        WHEN tenure_months < 6 THEN '3-5 Months'
        WHEN tenure_months < 12 THEN '6-11 Months'
        WHEN tenure_months < 24 THEN '12-23 Months'
        ELSE '24+ Months'
    END

ORDER BY
    MIN(tenure_months);

-- 2. Churn by signup year.
-- Lifecycle Churn Driver Analysis
-- Query 2: Churn by Signup Cohort
-- Analytical cutoff: 2025-12-26

WITH cohort_analysis AS (
    SELECT
        c.Customer_ID,
        YEAR(c.Signup_Date) AS signup_year,
        s.Churn_Status,
        s.Churn_Date
    FROM customers c
    INNER JOIN subscriptions s
        ON c.Customer_ID = s.Customer_ID
)

SELECT
    signup_year,
    COUNT(*) AS customers,
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
FROM cohort_analysis
GROUP BY signup_year
ORDER BY signup_year;

-- 3. Churn by month since signup (early lifecycle signal).
-- Lifecycle Churn Driver Analysis
-- Query 3: Churn Rate by Exact Observed Tenure Month
-- Analytical cutoff: 2025-12-26

WITH lifecycle AS (
    SELECT
        Customer_ID,
        Churn_Status,
        CASE
            WHEN Churn_Status = 'Churned'
                 AND Churn_Date IS NOT NULL
                THEN TIMESTAMPDIFF(
                    MONTH,
                    Start_Date,
                    Churn_Date
                )

            WHEN Churn_Status = 'Active'
                THEN TIMESTAMPDIFF(
                    MONTH,
                    Start_Date,
                    '2025-12-26'
                )

            ELSE NULL
        END AS tenure_months
    FROM subscriptions
)

SELECT
    tenure_months,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    SUM(Churn_Status = 'Active') AS active_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM lifecycle
WHERE tenure_months IS NOT NULL
GROUP BY tenure_months
ORDER BY tenure_months;


-- MODULE: SUBSCRIPTION CHURN | 02_subscription_churn.sql

-- 02_subscription_churn.sql
-- Customer Churn Analysis | Subscription Churn Drivers


-- 1. Churn by plan.
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Plan
ORDER BY churn_rate_pct DESC;

-- 2. Churn by contract type.
SELECT
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Contract_Type
ORDER BY churn_rate_pct DESC;

-- 3. Churn by plan + contract.
SELECT
    Plan,
    Contract_Type,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY Plan, Contract_Type
ORDER BY churn_rate_pct DESC;

-- 4. Churn by monthly-charge band.
SELECT
    CASE
        WHEN Monthly_Charge < 400 THEN '<400'
        WHEN Monthly_Charge < 600 THEN '400-599'
        WHEN Monthly_Charge < 800 THEN '600-799'
        WHEN Monthly_Charge < 1000 THEN '800-999'
        ELSE '1000+'
    END AS charge_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY charge_band
ORDER BY MIN(Monthly_Charge);

-- 5. Churned revenue at risk by plan.
SELECT
    Plan,
    COUNT(*) AS churned_customers,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_revenue_at_risk
FROM subscriptions
WHERE Churn_Status = 'Churned'
GROUP BY Plan
ORDER BY monthly_revenue_at_risk DESC;


-- MODULE: PAYMENT CHURN | 03_payment_churn.sql

-- 03_payment_churn.sql
-- Customer Churn Analysis | Payment Churn Drivers

-- IMPORTANT:
-- payments is one-to-many per customer. Aggregate it to one row
-- per customer before joining to subscriptions to avoid row multiplication.

WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments,
        ROUND(SUM(CASE WHEN Payment_Status = 'Successful' THEN Amount ELSE 0 END), 2) AS successful_payment_value,
        ROUND(AVG(Amount), 2) AS avg_payment_amount,
        MAX(Payment_Date) AS last_payment_date,
        COUNT(DISTINCT Payment_Method) AS payment_methods_used,
        MAX(CASE WHEN Payment_Status = 'Failed' THEN 1 ELSE 0 END) AS has_failed_payment
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
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(COALESCE(p.failed_payments, 0)), 2) AS avg_failed_payments
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
GROUP BY payment_failure_band
ORDER BY churn_rate_pct DESC;

-- 2. Churn by payment method used most frequently.
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
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM ranked_methods rm
JOIN subscriptions s ON s.Customer_ID = rm.Customer_ID
WHERE rm.rn = 1
GROUP BY rm.Payment_Method
ORDER BY churn_rate_pct DESC;

-- 3. Churn by payment success rate.
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
        WHEN 100.0 * successful_payments / NULLIF(total_payments, 0) < 80 THEN '<80%'
        WHEN 100.0 * successful_payments / NULLIF(total_payments, 0) < 95 THEN '80-94%'
        ELSE '95-100%'
    END AS payment_success_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM payment_features p
JOIN subscriptions s ON s.Customer_ID = p.Customer_ID
GROUP BY payment_success_band
ORDER BY churn_rate_pct DESC;

-- 4. Customer-level payment profile for deeper analysis.
WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments,
        ROUND(SUM(Amount), 2) AS total_payment_value,
        ROUND(AVG(Amount), 2) AS avg_payment_amount,
        MAX(Payment_Date) AS last_payment_date
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    s.Customer_ID,
    s.Churn_Status,
    p.total_payments,
    p.successful_payments,
    p.failed_payments,
    p.total_payment_value,
    p.avg_payment_amount,
    p.last_payment_date
FROM subscriptions s
LEFT JOIN payment_features p ON p.Customer_ID = s.Customer_ID
ORDER BY s.Churn_Status DESC, p.failed_payments DESC, p.total_payment_value DESC;


-- MODULE: SERVICE ADOPTION CHURN | 04_service_churn.sql

-- 04_service_churn.sql
-- Customer Churn Analysis | Service Adoption Churn Drivers

-- 1. Churn by each service.
WITH service_flags AS (
    SELECT Customer_ID, 'Mobile_App' AS service_name, Mobile_App AS service_value FROM customer_services
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
    sf.service_name,
    sf.service_value,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM service_flags sf
JOIN subscriptions s ON s.Customer_ID = sf.Customer_ID
GROUP BY sf.service_name, sf.service_value
ORDER BY sf.service_name, churn_rate_pct DESC;

-- 2. Churn by number of services adopted.
WITH service_counts AS (
    SELECT
        Customer_ID,
        (
            COALESCE(Mobile_App = 'Yes', 0) +
            COALESCE(Streaming = 'Yes', 0) +
            COALESCE(Cloud_Storage = 'Yes', 0) +
            COALESCE(Premium_Support = 'Yes', 0) +
            COALESCE(Family_Plan = 'Yes', 0)
        ) AS service_count
    FROM customer_services
)
SELECT
    sc.service_count,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM service_counts sc
JOIN subscriptions s
    ON s.Customer_ID = sc.Customer_ID
GROUP BY sc.service_count
ORDER BY sc.service_count;

-- 3. Low-adoption vs high-adoption churn.
-- Customer Churn Analysis | Service Adoption Churn Drivers
-- Query 3: Churn Rate by Service Adoption Band

WITH service_counts AS (
    SELECT
        Customer_ID,
        (
            COALESCE(Mobile_App = 'Yes', 0) +
            COALESCE(Streaming = 'Yes', 0) +
            COALESCE(Cloud_Storage = 'Yes', 0) +
            COALESCE(Premium_Support = 'Yes', 0) +
            COALESCE(Family_Plan = 'Yes', 0)
        ) AS service_count
    FROM customer_services
)
SELECT
    CASE
        WHEN service_count <= 1 THEN '0-1 Services'
        WHEN service_count <= 3 THEN '2-3 Services'
        ELSE '4-5 Services'
    END AS service_adoption_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct
FROM service_counts sc
JOIN subscriptions s
    ON s.Customer_ID = sc.Customer_ID
GROUP BY
    CASE
        WHEN service_count <= 1 THEN '0-1 Services'
        WHEN service_count <= 3 THEN '2-3 Services'
        ELSE '4-5 Services'
    END
ORDER BY churn_rate_pct DESC;


-- MODULE: SUPPORT CHURN | 05_support_churn.sql

-- 05_support_churn.sql
-- Customer Churn Analysis | Support Churn Drivers

-- IMPORTANT:
-- support_tickets is one-to-many per customer. Aggregate first.

WITH support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'Yes') AS resolved_tickets,
        SUM(Resolved = 'No') AS unresolved_tickets,
        ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
        ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction,
        COUNT(DISTINCT Issue_Type) AS issue_types_count,
        MAX(Ticket_Date) AS last_ticket_date
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    CASE
        WHEN COALESCE(sf.ticket_count, 0) = 0 THEN 'No Tickets'
        WHEN sf.ticket_count = 1 THEN '1 Ticket'
        WHEN sf.ticket_count BETWEEN 2 AND 3 THEN '2-3 Tickets'
        WHEN sf.ticket_count BETWEEN 4 AND 5 THEN '4-5 Tickets'
        ELSE '6+ Tickets'
    END AS ticket_volume_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY ticket_volume_band
ORDER BY churn_rate_pct DESC;

-- 2. Churn by average satisfaction.
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
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM support_features sf
JOIN subscriptions s ON s.Customer_ID = sf.Customer_ID
GROUP BY satisfaction_band
ORDER BY churn_rate_pct DESC;

-- 3. Churn by unresolved-ticket experience.
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
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
GROUP BY unresolved_ticket_band
ORDER BY churn_rate_pct DESC;

-- 4. Churn by issue type.
WITH issue_customers AS (
    SELECT DISTINCT Customer_ID, Issue_Type
    FROM support_tickets
)
SELECT
    ic.Issue_Type,
    COUNT(*) AS customers_with_issue,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM issue_customers ic
JOIN subscriptions s ON s.Customer_ID = ic.Customer_ID
GROUP BY ic.Issue_Type
ORDER BY churn_rate_pct DESC;

-- 5. Customer-level support profile.
WITH support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'Yes') AS resolved_tickets,
        SUM(Resolved = 'No') AS unresolved_tickets,
        ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
        ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction,
        MAX(Ticket_Date) AS last_ticket_date
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    s.Customer_ID,
    s.Churn_Status,
    COALESCE(sf.ticket_count, 0) AS ticket_count,
    COALESCE(sf.resolved_tickets, 0) AS resolved_tickets,
    COALESCE(sf.unresolved_tickets, 0) AS unresolved_tickets,
    sf.avg_resolution_hours,
    sf.avg_satisfaction,
    sf.last_ticket_date
FROM subscriptions s
LEFT JOIN support_features sf ON sf.Customer_ID = s.Customer_ID
ORDER BY s.Churn_Status DESC, unresolved_tickets DESC, avg_satisfaction ASC;


-- MODULE: ENGAGEMENT / ACTIVITY SIGNALS | 06_engagement_churn.sql

-- 06_engagement_churn.sql
-- Customer Churn Analysis | Engagement / Activity Signals

-- The operational workbook has no separate engagement table.
-- Engagement is therefore derived from available activity:
-- payments, services, and support interactions.

WITH payment_activity AS (
    SELECT
        Customer_ID,
        COUNT(*) AS payment_count,
        COUNT(DISTINCT DATE_FORMAT(Payment_Date, '%Y-%m')) AS active_payment_months,
        MAX(Payment_Date) AS last_payment_date
    FROM payments
    WHERE Payment_Status = 'Successful'
    GROUP BY Customer_ID
),
service_activity AS (
    SELECT
        Customer_ID,
        (Mobile_App = 'Yes') +
        (Streaming = 'Yes') +
        (Cloud_Storage = 'Yes') +
        (Premium_Support = 'Yes') +
        (Family_Plan = 'Yes') AS service_count
    FROM customer_services
),
support_activity AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        COUNT(DISTINCT DATE_FORMAT(Ticket_Date, '%Y-%m')) AS active_support_months
    FROM support_tickets
    GROUP BY Customer_ID
),
customer_activity AS (
    SELECT
        s.Customer_ID,
        s.Churn_Status,
        COALESCE(pa.payment_count, 0) AS payment_count,
        COALESCE(pa.active_payment_months, 0) AS active_payment_months,
        COALESCE(sa.service_count, 0) AS service_count,
        COALESCE(sup.ticket_count, 0) AS ticket_count,
        COALESCE(sup.active_support_months, 0) AS active_support_months,
        pa.last_payment_date
    FROM subscriptions s
    LEFT JOIN payment_activity pa ON pa.Customer_ID = s.Customer_ID
    LEFT JOIN service_activity sa ON sa.Customer_ID = s.Customer_ID
    LEFT JOIN support_activity sup ON sup.Customer_ID = s.Customer_ID
)
SELECT
    CASE
        WHEN active_payment_months <= 3 THEN 'Low Payment Activity'
        WHEN active_payment_months <= 6 THEN 'Medium Payment Activity'
        ELSE 'High Payment Activity'
    END AS payment_activity_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customer_activity
GROUP BY payment_activity_band
ORDER BY churn_rate_pct DESC;

-- 2. Composite engagement band.
WITH payment_activity AS (
    SELECT
        Customer_ID,
        COUNT(DISTINCT DATE_FORMAT(Payment_Date, '%Y-%m')) AS active_payment_months
    FROM payments
    WHERE Payment_Status = 'Successful'
    GROUP BY Customer_ID
),
service_activity AS (
    SELECT
        Customer_ID,
        (Mobile_App = 'Yes') +
        (Streaming = 'Yes') +
        (Cloud_Storage = 'Yes') +
        (Premium_Support = 'Yes') +
        (Family_Plan = 'Yes') AS service_count
    FROM customer_services
),
support_activity AS (
    SELECT Customer_ID, COUNT(*) AS ticket_count
    FROM support_tickets
    GROUP BY Customer_ID
),
activity AS (
    SELECT
        s.Customer_ID,
        s.Churn_Status,
        COALESCE(p.active_payment_months, 0) AS active_payment_months,
        COALESCE(se.service_count, 0) AS service_count,
        COALESCE(su.ticket_count, 0) AS ticket_count
    FROM subscriptions s
    LEFT JOIN payment_activity p ON p.Customer_ID = s.Customer_ID
    LEFT JOIN service_activity se ON se.Customer_ID = s.Customer_ID
    LEFT JOIN support_activity su ON su.Customer_ID = s.Customer_ID
),
scored AS (
    SELECT *,
        (CASE WHEN active_payment_months >= 6 THEN 1 ELSE 0 END) +
        (CASE WHEN service_count >= 3 THEN 1 ELSE 0 END) +
        (CASE WHEN ticket_count > 0 THEN 1 ELSE 0 END) AS engagement_score
    FROM activity
)
SELECT
    CASE
        WHEN engagement_score = 0 THEN '0 - Very Low'
        WHEN engagement_score = 1 THEN '1 - Low'
        WHEN engagement_score = 2 THEN '2 - Medium'
        ELSE '3 - High'
    END AS engagement_band,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM scored
GROUP BY engagement_band
ORDER BY engagement_band;

-- 3. Recent payment inactivity before churn (descriptive, not causal).
-- Customer Churn Analysis | Engagement / Activity Signals
-- Query 3: Churn Rate by Days Since Last Successful Payment
-- Analytical cutoff: 2025-12-26

WITH last_successful_payment AS (
    SELECT
        Customer_ID,
        MAX(Payment_Date) AS last_payment_date
    FROM payments
    WHERE Payment_Status = 'Successful'
      AND Payment_Date <= '2025-12-26'
    GROUP BY Customer_ID
),
payment_recency AS (
    SELECT
        s.Customer_ID,
        s.Churn_Status,
        p.last_payment_date,
        CASE
            WHEN p.last_payment_date IS NULL
                THEN 'No Successful Payment'
            WHEN s.Churn_Status = 'Churned'
                 AND s.Churn_Date IS NOT NULL
                THEN CASE
                    WHEN DATEDIFF(
                        s.Churn_Date,
                        p.last_payment_date
                    ) <= 30 THEN '0-30 Days'
                    WHEN DATEDIFF(
                        s.Churn_Date,
                        p.last_payment_date
                    ) <= 60 THEN '31-60 Days'
                    WHEN DATEDIFF(
                        s.Churn_Date,
                        p.last_payment_date
                    ) <= 90 THEN '61-90 Days'
                    ELSE '91+ Days'
                END
            WHEN s.Churn_Status = 'Active'
                THEN CASE
                    WHEN DATEDIFF(
                        '2025-12-26',
                        p.last_payment_date
                    ) <= 30 THEN '0-30 Days'
                    WHEN DATEDIFF(
                        '2025-12-26',
                        p.last_payment_date
                    ) <= 60 THEN '31-60 Days'
                    WHEN DATEDIFF(
                        '2025-12-26',
                        p.last_payment_date
                    ) <= 90 THEN '61-90 Days'
                    ELSE '91+ Days'
                END
            ELSE 'No Successful Payment'
        END AS payment_recency_band
    FROM subscriptions s
    LEFT JOIN last_successful_payment p
        ON p.Customer_ID = s.Customer_ID
),
banded_results AS (
    SELECT
        payment_recency_band,
        COUNT(*) AS customers,
        SUM(Churn_Status = 'Churned') AS churned_customers,
        ROUND(
            100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
            2
        ) AS churn_rate_pct
    FROM payment_recency
    GROUP BY payment_recency_band
)
SELECT
    payment_recency_band AS days_since_last_successful_payment_band,
        customers,
    churned_customers,
    churn_rate_pct
FROM banded_results
ORDER BY
    CASE payment_recency_band
        WHEN 'No Successful Payment' THEN 1
        WHEN '0-30 Days' THEN 2
        WHEN '31-60 Days' THEN 3
        WHEN '61-90 Days' THEN 4
        WHEN '91+ Days' THEN 5
    END;


-- MODULE: CUSTOMER PROFILE CHURN | 07_customer_profile_churn.sql

-- 07_customer_profile_churn.sql
-- Customer Churn Analysis | Customer Profile Drivers

-- 1. Churn by age band.
SELECT
    CASE
        WHEN c.Age IS NULL THEN 'Unknown'
        WHEN c.Age < 25 THEN '18-24'
        WHEN c.Age < 35 THEN '25-34'
        WHEN c.Age < 45 THEN '35-44'
        WHEN c.Age < 55 THEN '45-54'
        WHEN c.Age < 65 THEN '55-64'
        ELSE '65-75'
    END AS age_band,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY age_band
ORDER BY MIN(COALESCE(c.Age, 999));

-- 2. Churn by gender.
SELECT
    c.Gender,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY c.Gender
ORDER BY churn_rate_pct DESC;

-- 3. Churn by state.
SELECT
    c.State,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY c.State
HAVING COUNT(*) >= 100
ORDER BY churn_rate_pct DESC;

-- 4. Churn by city.
SELECT
    c.City,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY c.City
HAVING COUNT(*) >= 50
ORDER BY churn_rate_pct DESC;

-- 5. Profile intersection: age band + gender.
SELECT
    CASE
        WHEN c.Age IS NULL THEN 'Unknown'
        WHEN c.Age < 25 THEN '18-24'
        WHEN c.Age < 35 THEN '25-34'
        WHEN c.Age < 45 THEN '35-44'
        WHEN c.Age < 55 THEN '45-54'
        WHEN c.Age < 65 THEN '55-64'
        ELSE '65-75'
    END AS age_band,
    c.Gender,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(s.Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN subscriptions s ON s.Customer_ID = c.Customer_ID
GROUP BY age_band, c.Gender
HAVING COUNT(*) >= 50
ORDER BY churn_rate_pct DESC;


-- MODULE: MULTIDIMENSIONAL CHURN | 08_multidimensional_churn.sql

-- 08_multidimensional_churn.sql
-- Customer Churn Analysis | Multidimensional Churn Drivers


-- Build a one-row-per-customer analytical feature set.
-- This avoids the classic many-to-many row multiplication problem.

-- Customer Churn Analysis | Multidimensional Churn
-- Query 1: Multidimensional Churn Segmentation
-- Analytical cutoff: 2025-12-26

WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments,
        SUM(Payment_Status = 'Successful') AS successful_payments,
        ROUND(AVG(Amount), 2) AS avg_payment_amount,
        MAX(Payment_Date) AS last_payment_date
    FROM payments
    GROUP BY Customer_ID
),
support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'No') AS unresolved_tickets,
        ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
        ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction
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
customer_features AS (
    SELECT
        c.Customer_ID,
        c.Gender,
        c.Age,
        c.State,
        s.Plan,
        s.Contract_Type,
        s.Monthly_Charge,
        s.Churn_Status,
        s.Churn_Date,

        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                s.Start_Date,
                CASE
                    WHEN s.Churn_Status = 'Churned'
                         AND s.Churn_Date IS NOT NULL
                        THEN s.Churn_Date
                    WHEN s.Churn_Status = 'Active'
                        THEN '2025-12-26'
                    ELSE NULL
                END
            )
        ) AS tenure_months,

        COALESCE(p.total_payments, 0) AS total_payments,
        COALESCE(p.failed_payments, 0) AS failed_payments,
        COALESCE(p.successful_payments, 0) AS successful_payments,
        p.avg_payment_amount,
        p.last_payment_date,

        COALESCE(su.ticket_count, 0) AS ticket_count,
        COALESCE(su.unresolved_tickets, 0) AS unresolved_tickets,
        su.avg_resolution_hours,
        su.avg_satisfaction,

        COALESCE(se.service_count, 0) AS service_count

    FROM customers c
    JOIN subscriptions s
        ON s.Customer_ID = c.Customer_ID
    LEFT JOIN payment_features p
        ON p.Customer_ID = c.Customer_ID
    LEFT JOIN support_features su
        ON su.Customer_ID = c.Customer_ID
    LEFT JOIN service_features se
        ON se.Customer_ID = c.Customer_ID
),
scored AS (
    SELECT
        *,
        CASE
            WHEN tenure_months < 6 THEN 'New'
            WHEN tenure_months < 12 THEN 'Established'
            ELSE 'Mature'
        END AS lifecycle_stage,

        CASE
            WHEN failed_payments >= 4 THEN 'High Payment Risk'
            WHEN failed_payments >= 1 THEN 'Payment Risk'
            ELSE 'No Payment Risk'
        END AS payment_risk,

        CASE
            WHEN unresolved_tickets >= 2
                 OR avg_satisfaction < 3
                THEN 'High Support Risk'
            WHEN unresolved_tickets = 1
                 OR avg_satisfaction < 4
                THEN 'Support Risk'
            ELSE 'No Support Risk'
        END AS support_risk,

        CASE
            WHEN service_count <= 1 THEN 'Low Service Adoption'
            WHEN service_count <= 3 THEN 'Medium Service Adoption'
            ELSE 'High Service Adoption'
        END AS service_adoption

    FROM customer_features
)
SELECT
    lifecycle_stage,
    Plan,
    Contract_Type,
    payment_risk,
    support_risk,
    service_adoption,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM scored
GROUP BY
    lifecycle_stage,
    Plan,
    Contract_Type,
    payment_risk,
    support_risk,
    service_adoption
HAVING COUNT(*) >= 20
ORDER BY
    churn_rate_pct DESC,
    customers DESC;

-- 2. High-risk segment summary.
-- Customer Churn Analysis | Multidimensional Churn
-- Query 2: Multi-Factor Churn Analysis
-- Analytical cutoff: 2025-12-26

WITH payment_activity AS (
    SELECT
        Customer_ID,
        COUNT(
            DISTINCT CASE
                WHEN Payment_Status = 'Successful'
                 AND Payment_Date <= '2025-12-26'
                THEN DATE_FORMAT(Payment_Date, '%Y-%m')
            END
        ) AS active_payment_months
    FROM payments
    GROUP BY Customer_ID
),

customer_features AS (
    SELECT
        s.Customer_ID,
        s.Plan,
        s.Contract_Type,
        s.Monthly_Charge,
        s.Churn_Status,
        s.Churn_Date,

        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                s.Start_Date,
                CASE
                    WHEN s.Churn_Status = 'Churned'
                         AND s.Churn_Date IS NOT NULL
                        THEN s.Churn_Date
                    WHEN s.Churn_Status = 'Active'
                        THEN '2025-12-26'
                    ELSE NULL
                END
            )
        ) AS tenure_months,

        COALESCE(p.active_payment_months, 0) AS active_payment_months

    FROM subscriptions s

    LEFT JOIN payment_activity p
        ON p.Customer_ID = s.Customer_ID
),

segmented AS (
    SELECT
        *,
        
        CASE
            WHEN tenure_months < 6 THEN 'New'
            WHEN tenure_months < 12 THEN 'Established'
            ELSE 'Mature'
        END AS lifecycle_stage,

        CASE
            WHEN active_payment_months <= 3
                THEN 'Low Payment Engagement'
            WHEN active_payment_months <= 6
                THEN 'Medium Payment Engagement'
            ELSE 'High Payment Engagement'
        END AS payment_engagement

    FROM customer_features
)

SELECT
    lifecycle_stage,
    Plan,
    Contract_Type,
    payment_engagement,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,

    ROUND(
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*),
        2
    ) AS churn_rate_pct,

    ROUND(
        SUM(
            CASE
                WHEN Churn_Status = 'Churned'
                    THEN Monthly_Charge
                ELSE 0
            END
        ),
        2
    ) AS monthly_revenue_at_risk,

    ROUND(
        AVG(Monthly_Charge),
        2
    ) AS avg_monthly_charge

FROM segmented

GROUP BY
    lifecycle_stage,
    Plan,
    Contract_Type,
    payment_engagement

HAVING COUNT(*) >= 20

ORDER BY
    churn_rate_pct DESC,
    customers DESC;

-- 3. Top customer-level churn-risk candidates.
-- Customer Churn Analysis | Multidimensional Churn
-- Query 3: Active Customer Retention Priority
-- Analytical cutoff: 2025-12-26

WITH payment_activity AS (
    SELECT
        Customer_ID,

        COUNT(
            DISTINCT CASE
                WHEN Payment_Status = 'Successful'
                 AND Payment_Date <= '2025-12-26'
                THEN DATE_FORMAT(Payment_Date, '%Y-%m')
            END
        ) AS active_payment_months

    FROM payments

    GROUP BY Customer_ID
),

service_features AS (
    SELECT
        Customer_ID,

        (
            COALESCE(Mobile_App = 'Yes', 0) +
            COALESCE(Streaming = 'Yes', 0) +
            COALESCE(Cloud_Storage = 'Yes', 0) +
            COALESCE(Premium_Support = 'Yes', 0) +
            COALESCE(Family_Plan = 'Yes', 0)
        ) AS service_count

    FROM customer_services
),

active_customers AS (
    SELECT
        s.Customer_ID,
        c.Gender,
        c.Age,
        c.State,

        s.Plan,
        s.Contract_Type,
        s.Start_Date,
        s.Monthly_Charge,
        s.Churn_Status,

        GREATEST(
            0,
            TIMESTAMPDIFF(
                MONTH,
                s.Start_Date,
                '2025-12-26'
            )
        ) AS tenure_months,

        COALESCE(p.active_payment_months, 0)
            AS active_payment_months,

        COALESCE(sf.service_count, 0)
            AS service_count

    FROM subscriptions s

    JOIN customers c
        ON c.Customer_ID = s.Customer_ID

    LEFT JOIN payment_activity p
        ON p.Customer_ID = s.Customer_ID

    LEFT JOIN service_features sf
        ON sf.Customer_ID = s.Customer_ID

    WHERE s.Churn_Status = 'Active'
),

priority_scored AS (
    SELECT
        *,

        CASE
            WHEN tenure_months < 6 THEN 'New'
            WHEN tenure_months < 12 THEN 'Established'
            ELSE 'Mature'
        END AS lifecycle_stage,

        CASE
            WHEN active_payment_months <= 3
                THEN 'Low Payment Engagement'
            WHEN active_payment_months <= 6
                THEN 'Medium Payment Engagement'
            ELSE 'High Payment Engagement'
        END AS payment_engagement,

        (
            CASE
                WHEN tenure_months < 6 THEN 1
                ELSE 0
            END

            +

            CASE
                WHEN Contract_Type = 'Monthly' THEN 1
                ELSE 0
            END

            +

            CASE
                WHEN Plan = 'Premium' THEN 1
                ELSE 0
            END

            +

            CASE
                WHEN active_payment_months <= 3 THEN 1
                ELSE 0
            END

            +

            CASE
                WHEN service_count <= 1 THEN 1
                ELSE 0
            END
        ) AS priority_factor_count

    FROM active_customers
)

SELECT
    Customer_ID,
    Age,
    Gender,
    State,
    Plan,
    Contract_Type,
    lifecycle_stage,
    payment_engagement,
    service_count,
    tenure_months,
    active_payment_months,
    Monthly_Charge,
    priority_factor_count,

    CASE
        WHEN priority_factor_count >= 4
            THEN 'Very High Priority'
        WHEN priority_factor_count = 3
            THEN 'High Priority'
        WHEN priority_factor_count = 2
            THEN 'Medium Priority'
        ELSE 'Lower Priority'
    END AS retention_priority

FROM priority_scored

ORDER BY
    priority_factor_count DESC,
    Monthly_Charge DESC,
    tenure_months ASC

LIMIT 100;

