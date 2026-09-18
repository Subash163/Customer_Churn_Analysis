/*
Customer Churn & Retention Analysis
SQL - Interview Queries

Purpose:
    Consolidated SQL interview-practice queries demonstrating core and
    advanced SQL skills using the Customer Churn & Retention Analysis
    database.

Database:
    customer_churn_analysis

Skills Covered:
    01. Joins
    02. Aggregations
    03. CASE WHEN
    04. Subqueries
    05. Common Table Expressions (CTEs)
    06. Window Functions
    07. Date Functions
    08. Advanced SQL

Important:
    - This script is for SQL skill demonstration and interview preparation.
    - Queries are analytical and do not intentionally modify source tables.
    - The original module logic and terminology are preserved.
*/

USE customer_churn_analysis;

-- MODULE: 01_joins.sql

-- 01_joins.sql
-- Customer Churn Analysis | Interview SQL: JOINs

-- Q1. INNER JOIN: customers with their subscription details.
SELECT
    c.Customer_ID,
    c.Gender,
    c.Age,
    c.City,
    c.State,
    s.Plan,
    s.Contract_Type,
    s.Monthly_Charge,
    s.Churn_Status
FROM customers c
INNER JOIN subscriptions s
    ON s.Customer_ID = c.Customer_ID
LIMIT 100;

-- Q2. LEFT JOIN: all customers, including customers with no tickets.
SELECT
    c.Customer_ID,
    c.City,
    c.State,
    COUNT(st.Ticket_ID) AS ticket_count
FROM customers c
LEFT JOIN support_tickets st
    ON st.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID, c.City, c.State
ORDER BY ticket_count DESC;

-- Q3. JOIN three tables: customer + subscription + services.
SELECT
    c.Customer_ID,
    c.City,
    s.Plan,
    s.Contract_Type,
    cs.Mobile_App,
    cs.Streaming,
    cs.Cloud_Storage,
    cs.Premium_Support,
    cs.Family_Plan,
    s.Churn_Status
FROM customers c
JOIN subscriptions s
    ON s.Customer_ID = c.Customer_ID
LEFT JOIN customer_services cs
    ON cs.Customer_ID = c.Customer_ID
LIMIT 100;

-- Q4. Find customers who have never raised a support ticket.
SELECT
    c.Customer_ID,
    c.City,
    c.State
FROM customers c
LEFT JOIN support_tickets st
    ON st.Customer_ID = c.Customer_ID
WHERE st.Customer_ID IS NULL;

-- Q5. Find customers who have made at least one failed payment.
SELECT DISTINCT
    c.Customer_ID,
    s.Plan,
    s.Churn_Status
FROM customers c
JOIN subscriptions s
    ON s.Customer_ID = c.Customer_ID
JOIN payments p
    ON p.Customer_ID = c.Customer_ID
WHERE p.Payment_Status = 'Failed';

-- Q6. Safe customer-level JOIN of multiple one-to-many tables.
WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS payment_count,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
),
support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'No') AS unresolved_tickets
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    s.Customer_ID,
    s.Churn_Status,
    COALESCE(p.payment_count, 0) AS payment_count,
    COALESCE(p.failed_payments, 0) AS failed_payments,
    COALESCE(st.ticket_count, 0) AS ticket_count,
    COALESCE(st.unresolved_tickets, 0) AS unresolved_tickets
FROM subscriptions s
LEFT JOIN payment_features p
    ON p.Customer_ID = s.Customer_ID
LEFT JOIN support_features st
    ON st.Customer_ID = s.Customer_ID;


-- MODULE: 02_aggregations.sql

-- 02_aggregations.sql
-- Customer Churn Analysis | Interview SQL: Aggregations

-- Q1. Basic COUNT, SUM, AVG, MIN, MAX.
SELECT
    COUNT(*) AS subscriptions,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(MIN(Monthly_Charge), 2) AS min_monthly_charge,
    ROUND(MAX(Monthly_Charge), 2) AS max_monthly_charge,
    ROUND(SUM(Monthly_Charge), 2) AS total_monthly_charge
FROM subscriptions;

-- Q2. GROUP BY: churn performance by plan.
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY Plan
ORDER BY churn_rate_pct DESC;

-- Q3. HAVING: plans with at least 5,000 customers.
SELECT
    Plan,
    COUNT(*) AS customers,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge
FROM subscriptions
GROUP BY Plan
HAVING COUNT(*) >= 5000;

-- Q4. Top cities by customer count.
SELECT
    City,
    COUNT(*) AS customers
FROM customers
GROUP BY City
ORDER BY customers DESC
LIMIT 10;

-- Q5. Payment totals by status.
SELECT
    Payment_Status,
    COUNT(*) AS payment_count,
    ROUND(SUM(Amount), 2) AS payment_value,
    ROUND(AVG(Amount), 2) AS avg_payment
FROM payments
GROUP BY Payment_Status;

-- Q6. Support performance by issue type.
SELECT
    Issue_Type,
    COUNT(*) AS tickets,
    ROUND(AVG(Resolution_Time_Hours), 2) AS avg_resolution_hours,
    ROUND(AVG(Satisfaction_Score), 2) AS avg_satisfaction
FROM support_tickets
GROUP BY Issue_Type
ORDER BY tickets DESC;


-- MODULE: 03_case_when.sql

-- 03_case_when.sql
-- Customer Churn Analysis | Interview SQL: CASE WHEN


-- Q1. Create age bands.
SELECT
    Customer_ID,
    Age,
    CASE
        WHEN Age IS NULL THEN 'Unknown'
        WHEN Age < 25 THEN '18-24'
        WHEN Age < 35 THEN '25-34'
        WHEN Age < 45 THEN '35-44'
        WHEN Age < 55 THEN '45-54'
        WHEN Age < 65 THEN '55-64'
        ELSE '65-75'
    END AS age_band
FROM customers;

-- Q2. Classify monthly charge into pricing bands.
SELECT
    Customer_ID,
    Monthly_Charge,
    CASE
        WHEN Monthly_Charge < 400 THEN '<400'
        WHEN Monthly_Charge < 600 THEN '400-599'
        WHEN Monthly_Charge < 800 THEN '600-799'
        WHEN Monthly_Charge < 1000 THEN '800-999'
        ELSE '1000+'
    END AS charge_band
FROM subscriptions;

-- Q3. Create a churn-risk label from multiple business signals.
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
    s.Customer_ID,
    s.Churn_Status,
    CASE
        WHEN COALESCE(p.failed_payments, 0) >= 4
          OR COALESCE(st.unresolved_tickets, 0) >= 2
          OR st.avg_satisfaction < 3
            THEN 'High Risk'
        WHEN COALESCE(p.failed_payments, 0) >= 1
          OR COALESCE(st.unresolved_tickets, 0) = 1
          OR st.avg_satisfaction < 4
            THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS churn_risk_label
FROM subscriptions s
LEFT JOIN payment_features p
    ON p.Customer_ID = s.Customer_ID
LEFT JOIN support_features st
    ON st.Customer_ID = s.Customer_ID;

-- Q4. Conditional aggregation with CASE.
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn_Status = 'Active' THEN 1 ELSE 0 END) AS active_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn_Status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM subscriptions;

-- Q5. Categorize support ticket priority based on customer experience.
SELECT
    Ticket_ID,
    Customer_ID,
    Satisfaction_Score,
    Resolution_Time_Hours,
    CASE
        WHEN Satisfaction_Score <= 2 OR Resolution_Time_Hours > 24 THEN 'High Priority'
        WHEN Satisfaction_Score = 3 OR Resolution_Time_Hours > 12 THEN 'Medium Priority'
        ELSE 'Low Priority'
    END AS support_priority
FROM support_tickets;


-- MODULE: 04_subqueries.sql

-- 04_subqueries.sql
-- Customer Churn Analysis | Interview SQL: Subqueries

-- Q1. Customers paying above the overall average monthly charge.
SELECT
    Customer_ID,
    Plan,
    Monthly_Charge
FROM subscriptions
WHERE Monthly_Charge > (
    SELECT AVG(Monthly_Charge)
    FROM subscriptions
)
ORDER BY Monthly_Charge DESC;

-- Q2. Plans whose churn rate is above the overall churn rate.
SELECT
    Plan,
    COUNT(*) AS customers,
    SUM(Churn_Status = 'Churned') AS churned_customers,
    ROUND(100.0 * SUM(Churn_Status = 'Churned') / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions
GROUP BY Plan
HAVING
    SUM(Churn_Status = 'Churned') / COUNT(*) >
    (
        SELECT AVG(Churn_Status = 'Churned')
        FROM subscriptions
    );

-- Q3. Customers whose payment value is above the average customer payment value.
WITH customer_payment_value AS (
    SELECT
        Customer_ID,
        SUM(Amount) AS total_payment_value
    FROM payments
    GROUP BY Customer_ID
)
SELECT
    Customer_ID,
    ROUND(total_payment_value, 2) AS total_payment_value
FROM customer_payment_value
WHERE total_payment_value > (
    SELECT AVG(total_payment_value)
    FROM customer_payment_value
)
ORDER BY total_payment_value DESC;

-- Q4. Customers with more support tickets than the average customer.
WITH customer_tickets AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    Customer_ID,
    ticket_count
FROM customer_tickets
WHERE ticket_count > (
    SELECT AVG(ticket_count)
    FROM customer_tickets
)
ORDER BY ticket_count DESC;

-- Q5. Find customers whose monthly charge is the maximum within their plan.
SELECT
    s.Customer_ID,
    s.Plan,
    s.Monthly_Charge
FROM subscriptions s
WHERE s.Monthly_Charge = (
    SELECT MAX(s2.Monthly_Charge)
    FROM subscriptions s2
    WHERE s2.Plan = s.Plan
)
ORDER BY s.Plan, s.Monthly_Charge DESC;


-- MODULE: 05_ctes.sql

-- 05_ctes.sql
-- Customer Churn Analysis | Interview SQL: CTEs

-- Q1. CTE for plan-level churn performance.
WITH plan_summary AS (
    SELECT
        Plan,
        COUNT(*) AS customers,
        SUM(Churn_Status = 'Churned') AS churned_customers
    FROM subscriptions
    GROUP BY Plan
)
SELECT
    Plan,
    customers,
    churned_customers,
    ROUND(100.0 * churned_customers / customers, 2) AS churn_rate_pct
FROM plan_summary
ORDER BY churn_rate_pct DESC;

-- Q2. Multi-CTE customer risk profile.
WITH payment_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_payments,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
),
support_features AS (
    SELECT
        Customer_ID,
        COUNT(*) AS ticket_count,
        SUM(Resolved = 'No') AS unresolved_tickets,
        AVG(Satisfaction_Score) AS avg_satisfaction
    FROM support_tickets
    GROUP BY Customer_ID
),
customer_profile AS (
    SELECT
        s.Customer_ID,
        s.Churn_Status,
        s.Plan,
        s.Contract_Type,
        s.Monthly_Charge,
        COALESCE(p.failed_payments, 0) AS failed_payments,
        COALESCE(st.ticket_count, 0) AS ticket_count,
        COALESCE(st.unresolved_tickets, 0) AS unresolved_tickets,
        st.avg_satisfaction
    FROM subscriptions s
    LEFT JOIN payment_features p
        ON p.Customer_ID = s.Customer_ID
    LEFT JOIN support_features st
        ON st.Customer_ID = s.Customer_ID
)
SELECT *
FROM customer_profile
WHERE failed_payments >= 2
   OR unresolved_tickets >= 2
   OR avg_satisfaction < 3
ORDER BY failed_payments DESC, unresolved_tickets DESC;

-- Q3. CTE to identify the highest-churn plan.
WITH plan_churn AS (
    SELECT
        Plan,
        COUNT(*) AS customers,
        SUM(Churn_Status = 'Churned') AS churned_customers,
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*) AS churn_rate
    FROM subscriptions
    GROUP BY Plan
)
SELECT
    Plan,
    customers,
    churned_customers,
    ROUND(churn_rate, 2) AS churn_rate_pct
FROM plan_churn
WHERE churn_rate = (
    SELECT MAX(churn_rate)
    FROM plan_churn
);

-- Q4. Monthly churn trend using a CTE.
WITH monthly_churn AS (
    SELECT
        DATE_FORMAT(Churn_Date, '%Y-%m') AS churn_month,
        COUNT(*) AS churned_customers
    FROM subscriptions
    WHERE Churn_Status = 'Churned'
      AND Churn_Date IS NOT NULL
    GROUP BY DATE_FORMAT(Churn_Date, '%Y-%m')
)
SELECT
    churn_month,
    churned_customers
FROM monthly_churn
ORDER BY churn_month;


-- MODULE: 06_window_functions.sql

-- 06_window_functions.sql
-- Customer Churn Analysis | Interview SQL: Window Functions

-- Q1. Rank plans by churn rate.
WITH plan_churn AS (
    SELECT
        Plan,
        COUNT(*) AS customers,
        SUM(Churn_Status = 'Churned') AS churned_customers,
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*) AS churn_rate
    FROM subscriptions
    GROUP BY Plan
)
SELECT
    Plan,
    customers,
    churned_customers,
    ROUND(churn_rate, 2) AS churn_rate_pct,
    RANK() OVER (ORDER BY churn_rate DESC) AS churn_rate_rank
FROM plan_churn;

-- Q2. Rank customers by monthly charge within each plan.
SELECT
    Customer_ID,
    Plan,
    Monthly_Charge,
    RANK() OVER (
        PARTITION BY Plan
        ORDER BY Monthly_Charge DESC
    ) AS charge_rank
FROM subscriptions;

-- Q3. Top 3 highest-value customers within each plan.
WITH ranked AS (
    SELECT
        Customer_ID,
        Plan,
        Monthly_Charge,
        Churn_Status,
        ROW_NUMBER() OVER (
            PARTITION BY Plan
            ORDER BY Monthly_Charge DESC, Customer_ID
        ) AS rn
    FROM subscriptions
)
SELECT
    Customer_ID,
    Plan,
    Monthly_Charge,
    Churn_Status
FROM ranked
WHERE rn <= 3
ORDER BY Plan, rn;

-- Q4. Compare each plan's churn rate with the average plan churn rate.
WITH plan_churn AS (
    SELECT
        Plan,
        COUNT(*) AS customers,
        100.0 * SUM(Churn_Status = 'Churned') / COUNT(*) AS churn_rate
    FROM subscriptions
    GROUP BY Plan
)
SELECT
    Plan,
    ROUND(churn_rate, 2) AS churn_rate_pct,
    ROUND(AVG(churn_rate) OVER (), 2) AS avg_plan_churn_rate_pct,
    ROUND(churn_rate - AVG(churn_rate) OVER (), 2) AS difference_from_avg_pct
FROM plan_churn;

-- Q5. Running monthly payment value.
WITH monthly_payments AS (
    SELECT
        DATE_FORMAT(Payment_Date, '%Y-%m') AS payment_month,
        SUM(Amount) AS payment_value
    FROM payments
    WHERE Payment_Status = 'Successful'
    GROUP BY DATE_FORMAT(Payment_Date, '%Y-%m')
)
SELECT
    payment_month,
    ROUND(payment_value, 2) AS monthly_payment_value,
    ROUND(
        SUM(payment_value) OVER (
            ORDER BY payment_month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cumulative_payment_value
FROM monthly_payments
ORDER BY payment_month;

-- Q6. Month-over-month payment value comparison.
WITH monthly_payments AS (
    SELECT
        DATE_FORMAT(Payment_Date, '%Y-%m') AS payment_month,
        SUM(Amount) AS payment_value
    FROM payments
    WHERE Payment_Status = 'Successful'
    GROUP BY DATE_FORMAT(Payment_Date, '%Y-%m')
)
SELECT
    payment_month,
    ROUND(payment_value, 2) AS payment_value,
    ROUND(
        LAG(payment_value) OVER (ORDER BY payment_month),
        2
    ) AS previous_month_value,
    ROUND(
        100.0 * (
            payment_value - LAG(payment_value) OVER (ORDER BY payment_month)
        ) / NULLIF(LAG(payment_value) OVER (ORDER BY payment_month), 0),
        2
    ) AS mom_growth_pct
FROM monthly_payments
ORDER BY payment_month;


-- MODULE: 07_date_functions.sql

-- 07_date_functions.sql
-- Customer Churn Analysis | Interview SQL: Date Functions

-- Q1. Customer signup year and month.
SELECT
    Customer_ID,
    Signup_Date,
    YEAR(Signup_Date) AS signup_year,
    MONTH(Signup_Date) AS signup_month,
    DATE_FORMAT(Signup_Date, '%Y-%m') AS signup_month_label
FROM customers
LIMIT 100;

-- Q2. Monthly customer acquisition trend.
SELECT
    DATE_FORMAT(Signup_Date, '%Y-%m') AS signup_month,
    COUNT(*) AS new_customers
FROM customers
GROUP BY DATE_FORMAT(Signup_Date, '%Y-%m')
ORDER BY signup_month;

-- Q3. Tenure in months for each customer.
SELECT
    Customer_ID,
    Start_Date,
    Churn_Status,
    Churn_Date,
    GREATEST(
        0,
        TIMESTAMPDIFF(
            MONTH,
            Start_Date,
            COALESCE(Churn_Date, CURDATE())
        )
    ) AS tenure_months
FROM subscriptions
LIMIT 100;

-- Q4. Average tenure by churn status.
SELECT
    Churn_Status,
    ROUND(
        AVG(
            GREATEST(
                0,
                TIMESTAMPDIFF(
                    MONTH,
                    Start_Date,
                    COALESCE(Churn_Date, CURDATE())
                )
            )
        ),
        2
    ) AS avg_tenure_months
FROM subscriptions
GROUP BY Churn_Status;

-- Q5. Churn trend by month.
SELECT
    DATE_FORMAT(Churn_Date, '%Y-%m') AS churn_month,
    COUNT(*) AS churned_customers
FROM subscriptions
WHERE Churn_Status = 'Churned'
  AND Churn_Date IS NOT NULL
GROUP BY DATE_FORMAT(Churn_Date, '%Y-%m')
ORDER BY churn_month;

-- Q6. Customers who churned within six months of starting.
SELECT
    Customer_ID,
    Start_Date,
    Churn_Date,
    TIMESTAMPDIFF(MONTH, Start_Date, Churn_Date) AS tenure_at_churn_months
FROM subscriptions
WHERE Churn_Status = 'Churned'
  AND Churn_Date IS NOT NULL
  AND TIMESTAMPDIFF(MONTH, Start_Date, Churn_Date) < 6
ORDER BY tenure_at_churn_months;


-- MODULE: 08_advanced_sql.sql

-- 08_advanced_sql.sql
-- Customer Churn Analysis | Interview SQL: Advanced SQL

-- Q1. Find duplicate customer IDs using GROUP BY/HAVING.
SELECT
    Customer_ID,
    COUNT(*) AS row_count
FROM customers
GROUP BY Customer_ID
HAVING COUNT(*) > 1
ORDER BY row_count DESC;

-- Q2. Find customers with both failed payments and unresolved tickets.
WITH payment_risk AS (
    SELECT
        Customer_ID,
        SUM(Payment_Status = 'Failed') AS failed_payments
    FROM payments
    GROUP BY Customer_ID
),
support_risk AS (
    SELECT
        Customer_ID,
        SUM(Resolved = 'No') AS unresolved_tickets
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    s.Customer_ID,
    s.Churn_Status,
    COALESCE(p.failed_payments, 0) AS failed_payments,
    COALESCE(st.unresolved_tickets, 0) AS unresolved_tickets
FROM subscriptions s
JOIN payment_risk p
    ON p.Customer_ID = s.Customer_ID
JOIN support_risk st
    ON st.Customer_ID = s.Customer_ID
WHERE p.failed_payments > 0
  AND st.unresolved_tickets > 0
ORDER BY failed_payments DESC, unresolved_tickets DESC;

-- Q3. Find each customer's most frequently used payment method.
WITH method_counts AS (
    SELECT
        Customer_ID,
        Payment_Method,
        COUNT(*) AS method_count
    FROM payments
    GROUP BY Customer_ID, Payment_Method
),
ranked AS (
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
    Customer_ID,
    Payment_Method AS primary_payment_method,
    method_count
FROM ranked
WHERE rn = 1;

-- Q4. Identify customers whose support ticket count is above
-- their state's average ticket count.
WITH customer_tickets AS (
    SELECT
        c.Customer_ID,
        c.State,
        COUNT(st.Ticket_ID) AS ticket_count
    FROM customers c
    LEFT JOIN support_tickets st
        ON st.Customer_ID = c.Customer_ID
    GROUP BY c.Customer_ID, c.State
),
state_avg AS (
    SELECT
        State,
        AVG(ticket_count) AS avg_state_ticket_count
    FROM customer_tickets
    GROUP BY State
)
SELECT
    ct.Customer_ID,
    ct.State,
    ct.ticket_count,
    ROUND(sa.avg_state_ticket_count, 2) AS avg_state_ticket_count
FROM customer_tickets ct
JOIN state_avg sa
    ON sa.State = ct.State
WHERE ct.ticket_count > sa.avg_state_ticket_count
ORDER BY ct.State, ct.ticket_count DESC;

-- Q5. Revenue contribution by plan.
SELECT
    Plan,
    ROUND(SUM(Monthly_Charge), 2) AS monthly_charge,
    ROUND(
        100.0 * SUM(Monthly_Charge) /
        SUM(SUM(Monthly_Charge)) OVER (),
        2
    ) AS revenue_contribution_pct
FROM subscriptions
GROUP BY Plan
ORDER BY monthly_charge DESC;

-- Q6. Customers with a support ticket after their last successful payment.
WITH last_successful_payment AS (
    SELECT
        Customer_ID,
        MAX(Payment_Date) AS last_successful_payment
    FROM payments
    WHERE Payment_Status = 'Successful'
    GROUP BY Customer_ID
),
last_support_ticket AS (
    SELECT
        Customer_ID,
        MAX(Ticket_Date) AS last_ticket_date
    FROM support_tickets
    GROUP BY Customer_ID
)
SELECT
    s.Customer_ID,
    s.Churn_Status,
    p.last_successful_payment,
    st.last_ticket_date
FROM subscriptions s
JOIN last_successful_payment p
    ON p.Customer_ID = s.Customer_ID
JOIN last_support_ticket st
    ON st.Customer_ID = s.Customer_ID
WHERE st.last_ticket_date > p.last_successful_payment
ORDER BY st.last_ticket_date DESC;

-- Q7. Retention rate by state with a minimum population threshold.
SELECT
    c.State,
    COUNT(*) AS customers,
    SUM(s.Churn_Status = 'Active') AS active_customers,
    ROUND(
        100.0 * SUM(s.Churn_Status = 'Active') / COUNT(*),
        2
    ) AS retention_rate_pct
FROM customers c
JOIN subscriptions s
    ON s.Customer_ID = c.Customer_ID
GROUP BY c.State
HAVING COUNT(*) >= 100
ORDER BY retention_rate_pct DESC;
