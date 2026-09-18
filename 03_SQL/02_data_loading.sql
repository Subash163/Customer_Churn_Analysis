/* ============================================================
   CUSTOMER CHURN & RETENTION ANALYSIS
   SQL DATA LOADING SCRIPT
 

   Purpose:
   - Load cleaned CSV files into MySQL
   - Convert blank nullable values to SQL NULL during loading
   - Preserve genuine missing values without imputation
   - Verify final row counts and basic loading quality

   Database:
   customer_churn_analysis

   Source:
   Python cleaned CSV files

   Expected row counts:
   customers          = 20,000
   subscriptions      = 20,000
   payments           = 355,437
   customer_services  = 20,000
   support_tickets    = 50,000

   Important:
   - Data_Dictionary is documentation only.
   - It is NOT loaded as an operational database table.
   - Missing values are preserved as NULL.
   - No mean/median/mode imputation is performed.
   ============================================================ */


-- 1. SELECT DATABASE

USE customer_churn_analysis;

-- 2. LOAD CUSTOMERS

/*
   Missing-value handling:
   - Blank Gender  -> NULL
   - Blank Age     -> NULL

   The 79 missing Gender values and 240 missing Age values
   are genuine missing values from the cleaned source data.
   They are intentionally preserved as NULL.
*/

LOAD DATA LOCAL INFILE
    'K:/Data_Analyst/Project/Customer_Churn/python/cleaned/customers_cleaned.csv'

IGNORE
INTO TABLE customers

CHARACTER SET utf8mb4

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS

(
    Customer_ID,
    @Gender,
    @Age,
    City,
    State,
    Signup_Date
)

SET
    Gender = NULLIF(TRIM(@Gender), ''),
    Age = NULLIF(@Age, ''),
	City = NULLIF(TRIM(@City), '');


-- 3. LOAD SUBSCRIPTIONS

/*
   Missing-value handling:
   - Blank End_Date   -> NULL
   - Blank Churn_Date -> NULL

   Active subscriptions are expected to have NULL Churn_Date
   and NULL End_Date where applicable.
*/

LOAD DATA LOCAL INFILE
    'K:/Data_Analyst/Project/Customer_Churn/python/cleaned/subscriptions_cleaned.csv'

INTO TABLE subscriptions

CHARACTER SET utf8mb4

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS

(
    Customer_ID,
    Subscription_ID,
    Plan,
    Contract_Type,
    Start_Date,
    @End_Date,
    Monthly_Charge,
    Churn_Status,
    @Churn_Date
)

SET
    End_Date = NULLIF(@End_Date, ''),
    Churn_Date = NULLIF(@Churn_Date, '');



-- 4. LOAD PAYMENTS

/*
   Payment data contains no expected nullable fields in the
   current cleaned dataset.
*/

LOAD DATA LOCAL INFILE
    'K:/Data_Analyst/Project/Customer_Churn/python/cleaned/payments_cleaned.csv'

INTO TABLE payments

CHARACTER SET utf8mb4

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS

(
    Payment_ID,
    Customer_ID,
    Payment_Date,
    Amount,
    Payment_Method,
    Payment_Status
);


-- 5. LOAD CUSTOMER SERVICES

/*
   Missing-value handling:
   - Blank Mobile_App       -> NULL
   - Blank Streaming        -> NULL
   - Blank Cloud_Storage    -> NULL
   - Blank Premium_Support  -> NULL
   - Blank Family_Plan      -> NULL

   In the current source data:
   - Streaming       = 70 missing
   - Cloud_Storage   = 70 missing
   - Premium_Support = 70 missing

   These are genuine missing values from the cleaned source
   data and are intentionally preserved as NULL.
*/

LOAD DATA LOCAL INFILE
    'K:/Data_Analyst/Project/Customer_Churn/python/cleaned/customer_services_cleaned.csv'

INTO TABLE customer_services

CHARACTER SET utf8mb4

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS

(
    Customer_ID,
    @Mobile_App,
    @Streaming,
    @Cloud_Storage,
    @Premium_Support,
    @Family_Plan
)

SET
    Mobile_App = NULLIF(TRIM(@Mobile_App), ''),
    Streaming = NULLIF(TRIM(@Streaming), ''),
    Cloud_Storage = NULLIF(TRIM(@Cloud_Storage), ''),
    Premium_Support = NULLIF(TRIM(@Premium_Support), ''),
    Family_Plan = NULLIF(TRIM(@Family_Plan), '');


-- 6. LOAD SUPPORT TICKETS

/*
   Support ticket data contains no expected nullable fields
   in the current cleaned dataset.
*/

LOAD DATA LOCAL INFILE
    'K:/Data_Analyst/Project/Customer_Churn/python/cleaned/support_tickets_cleaned.csv'

INTO TABLE support_tickets

CHARACTER SET utf8mb4

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS

(
    Ticket_ID,
    Customer_ID,
    Ticket_Date,
    Issue_Type,
    Resolution_Time_Hours,
    Satisfaction_Score,
    Resolved
);


-- 7. FINAL ROW COUNT VERIFICATION

/*
   Expected final row counts:
   customers          = 20,000
   subscriptions      = 20,000
   payments           = 355,437
   customer_services  = 20,000
   support_tickets    = 50,000
*/

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'subscriptions', COUNT(*)
FROM subscriptions

UNION ALL

SELECT 'payments', COUNT(*)
FROM payments

UNION ALL

SELECT 'customer_services', COUNT(*)
FROM customer_services

UNION ALL

SELECT 'support_tickets', COUNT(*)
FROM support_tickets;


-- 8. VERIFY CHURN STATUS DISTRIBUTION

SELECT
    Churn_Status,
    COUNT(*) AS customer_count
FROM subscriptions
GROUP BY Churn_Status
ORDER BY Churn_Status;


-- 9. VERIFY MISSING VALUES WERE LOADED AS NULL

/*
   Expected:
   Gender NULLs             = 79
   Age NULLs                = 240
*/

SELECT
    COUNT(*) AS total_customers,
    SUM(Gender IS NULL) AS gender_nulls,
    SUM(Age IS NULL) AS age_nulls
FROM customers;


/*
   Expected:
   Streaming NULLs          = 70
   Cloud_Storage NULLs      = 70
   Premium_Support NULLs    = 70
*/

SELECT
    COUNT(*) AS total_customer_services,
    SUM(Streaming IS NULL) AS streaming_nulls,
    SUM(Cloud_Storage IS NULL) AS cloud_storage_nulls,
    SUM(Premium_Support IS NULL) AS premium_support_nulls
FROM customer_services;


-- 10. VERIFY NO BLANK STRINGS REMAIN IN THESE COLUMNS

/*
   These checks should return 0 for all columns.
*/

SELECT
    SUM(TRIM(Gender) = '') AS blank_gender,
    SUM(TRIM(City) = '') AS blank_city,
    SUM(TRIM(State) = '') AS blank_state
FROM customers;


SELECT
    SUM(TRIM(Mobile_App) = '') AS blank_mobile_app,
    SUM(TRIM(Streaming) = '') AS blank_streaming,
    SUM(TRIM(Cloud_Storage) = '') AS blank_cloud_storage,
    SUM(TRIM(Premium_Support) = '') AS blank_premium_support,
    SUM(TRIM(Family_Plan) = '') AS blank_family_plan
FROM customer_services;


-- 11. DATA LOADING COMPLETE

/*
   Final expected result:

   customers          = 20,000
   subscriptions      = 20,000
   payments           = 355,437
   customer_services  = 20,000
   support_tickets    = 50,000

   Missing values:
   - Preserved as SQL NULL
   - No statistical imputation performed
   - Blank strings normalized during loading

   Data_Dictionary:
   - Not loaded into the operational database
   - Maintained as project documentation
*/
```
