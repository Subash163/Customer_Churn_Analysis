-- Customer Churn Analysis | MySQL Database Design
-- File: 01_database_design.sql
-- Purpose: Complete, self-contained database design.
--
-- Includes:
--   1. Database creation
--   2. Table definitions
--   3. Primary keys
--   4. Foreign keys
--   5. Business-rule CHECK constraints
--   6. Secondary indexes
--
-- Data_Dictionary is documentation metadata and is intentionally
-- not created as a business data table.


CREATE DATABASE IF NOT EXISTS customer_churn_analysis
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE customer_churn_analysis;

-- 1. CUSTOMERS
-- Grain: One row per customer

CREATE TABLE IF NOT EXISTS customers (
    Customer_ID VARCHAR(10) NOT NULL,
    Gender VARCHAR(20) NULL,
    Age SMALLINT UNSIGNED NULL,
    City VARCHAR(50) NULL,
    State VARCHAR(50) NULL,
    Signup_Date DATETIME NOT NULL,

    CONSTRAINT pk_customers
        PRIMARY KEY (Customer_ID),

    CONSTRAINT chk_customers_age
        CHECK (Age IS NULL OR Age BETWEEN 18 AND 75),

    INDEX idx_customers_state (State),
    INDEX idx_customers_gender (Gender),
    INDEX idx_customers_signup_date (Signup_Date)
) ENGINE = InnoDB;



-- 2. SUBSCRIPTIONS
-- Grain: One row per customer subscription

CREATE TABLE IF NOT EXISTS subscriptions (
    Customer_ID VARCHAR(10) NOT NULL,
    Subscription_ID VARCHAR(15) NOT NULL,
    Plan VARCHAR(20) NULL,
    Contract_Type VARCHAR(20) NULL,
    Start_Date DATETIME NOT NULL,
    End_Date DATETIME NULL,
    Monthly_Charge DECIMAL(10,2) NOT NULL,
    Churn_Status VARCHAR(20) NULL,
    Churn_Date DATETIME NULL,

    CONSTRAINT pk_subscriptions
        PRIMARY KEY (Subscription_ID),

    CONSTRAINT fk_subscriptions_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES customers (Customer_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_subscriptions_monthly_charge
        CHECK (Monthly_Charge >= 0),

    CONSTRAINT chk_subscriptions_churn_dates
        CHECK (
            (Churn_Status = 'Active' AND Churn_Date IS NULL)
            OR
            (Churn_Status = 'Churned' AND Churn_Date IS NOT NULL)
            OR
            Churn_Status IS NULL
        ),

    INDEX idx_subscriptions_customer (Customer_ID),
    INDEX idx_subscriptions_churn_status (Churn_Status),
    INDEX idx_subscriptions_plan_contract (Plan, Contract_Type),
    INDEX idx_subscriptions_start_date (Start_Date),
    INDEX idx_subscriptions_churn_date (Churn_Date)
) ENGINE = InnoDB;



-- 3. PAYMENTS
-- Grain: One row per payment transaction

CREATE TABLE IF NOT EXISTS payments (
    Payment_ID VARCHAR(15) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Payment_Date DATETIME NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Method VARCHAR(30) NULL,
    Payment_Status VARCHAR(20) NULL,

    CONSTRAINT pk_payments
        PRIMARY KEY (Payment_ID),

    CONSTRAINT fk_payments_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES customers (Customer_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_payments_amount
        CHECK (Amount >= 0),

    INDEX idx_payments_customer (Customer_ID),
    INDEX idx_payments_customer_date (Customer_ID, Payment_Date),
    INDEX idx_payments_status (Payment_Status),
    INDEX idx_payments_method (Payment_Method),
    INDEX idx_payments_date (Payment_Date)
) ENGINE = InnoDB;



-- 4. CUSTOMER SERVICES
-- Grain: One row per customer

CREATE TABLE IF NOT EXISTS customer_services (
    Customer_ID VARCHAR(10) NOT NULL,
    Mobile_App VARCHAR(10) NULL,
    Streaming VARCHAR(10) NULL,
    Cloud_Storage VARCHAR(10) NULL,
    Premium_Support VARCHAR(10) NULL,
    Family_Plan VARCHAR(10) NULL,

    CONSTRAINT pk_customer_services
        PRIMARY KEY (Customer_ID),

    CONSTRAINT fk_customer_services_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES customers (Customer_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;



-- 5. SUPPORT TICKETS
-- Grain: One row per support ticket

CREATE TABLE IF NOT EXISTS support_tickets (
    Ticket_ID VARCHAR(15) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Ticket_Date DATETIME NOT NULL,
    Issue_Type VARCHAR(30) NULL,
    Resolution_Time_Hours DECIMAL(8,2) NOT NULL,
    Satisfaction_Score TINYINT UNSIGNED NOT NULL,
    Resolved VARCHAR(10) NULL,

    CONSTRAINT pk_support_tickets
        PRIMARY KEY (Ticket_ID),

    CONSTRAINT fk_support_tickets_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES customers (Customer_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_support_satisfaction_score
        CHECK (Satisfaction_Score BETWEEN 1 AND 5),

    CONSTRAINT chk_support_resolution_time
        CHECK (Resolution_Time_Hours >= 0),

    INDEX idx_support_customer (Customer_ID),
    INDEX idx_support_customer_date (Customer_ID, Ticket_Date),
    INDEX idx_support_issue_type (Issue_Type),
    INDEX idx_support_resolved (Resolved),
    INDEX idx_support_ticket_date (Ticket_Date)
) ENGINE = InnoDB;



-- DATABASE DESIGN SUMMARY

--
-- Primary keys:
--   customers.Customer_ID
--   subscriptions.Subscription_ID
--   payments.Payment_ID
--   customer_services.Customer_ID
--   support_tickets.Ticket_ID
--
-- Foreign keys:
--   subscriptions.Customer_ID      -> customers.Customer_ID
--   payments.Customer_ID           -> customers.Customer_ID
--   customer_services.Customer_ID -> customers.Customer_ID
--   support_tickets.Customer_ID    -> customers.Customer_ID
--
-- Professional design note:
--   Primary keys, foreign keys, CHECK constraints, and table-level
--   secondary indexes are defined directly inside CREATE TABLE.
--   This makes each table definition self-contained.
--
--   PRIMARY KEY indexes are created automatically by MySQL.
--   Secondary indexes are explicitly defined above for commonly
--   joined, filtered, grouped, and date-based analytical queries.
--
-- Recommended next step:
--   Load the cleaned CSV datasets using the 02_data_loading scripts.
--

-- END OF DATABASE DESIGN

