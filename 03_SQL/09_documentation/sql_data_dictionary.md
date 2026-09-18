# SQL Data Dictionary — Customer Churn Analysis

## Database

**Database:** `customer_churn_analysis`

**Technology:** MySQL 8.x

**Storage Engine:** InnoDB

---

## 1. customers

**Grain:** One row per customer.

| Column | Type | Key | Description |
|---|---|---|---|
| Customer_ID | VARCHAR(10) | PK | Unique customer identifier |
| Gender | VARCHAR(20) | | Customer gender/category |
| Age | SMALLINT UNSIGNED | | Customer age |
| City | VARCHAR(50) | | Customer city |
| State | VARCHAR(50) | | Customer state |
| Signup_Date | DATETIME | | Customer signup timestamp |

### Business rules
- Customer_ID must be unique and non-null.
- Age should be between 18 and 75 when populated.
- Signup_Date must be populated.

---

## 2. subscriptions

**Grain:** One row per customer subscription.

| Column | Type | Key | Description |
|---|---|---|---|
| Customer_ID | VARCHAR(10) | FK | Customer associated with subscription |
| Subscription_ID | VARCHAR(15) | PK | Unique subscription identifier |
| Plan | VARCHAR(20) | | Basic, Standard, or Premium |
| Contract_Type | VARCHAR(20) | | Monthly, One Year, or Two Year |
| Start_Date | DATETIME | | Subscription start timestamp |
| End_Date | DATETIME | | Subscription end timestamp; normally NULL for active customers |
| Monthly_Charge | DECIMAL(10,2) | | Monthly subscription charge in INR |
| Churn_Status | VARCHAR(20) | | Active or Churned |
| Churn_Date | DATETIME | | Churn timestamp for churned customers |

### Business rules
- Subscription_ID must be unique and non-null.
- Customer_ID must exist in customers.
- Monthly_Charge must be non-negative.
- Churned subscriptions should have Churn_Date.
- Active subscriptions should not have Churn_Date.
- End_Date and Churn_Date must not precede Start_Date.

---

## 3. payments

**Grain:** One row per payment transaction.

| Column | Type | Key | Description |
|---|---|---|---|
| Payment_ID | VARCHAR(15) | PK | Unique payment identifier |
| Customer_ID | VARCHAR(10) | FK | Customer who made the payment |
| Payment_Date | DATETIME | | Payment timestamp |
| Amount | DECIMAL(10,2) | | Payment amount in INR |
| Payment_Method | VARCHAR(30) | | Payment channel/method |
| Payment_Status | VARCHAR(20) | | Successful or Failed |

### Business rules
- Payment_ID must be unique and non-null.
- Customer_ID must exist in customers.
- Amount must be non-negative.
- Payment_Status should contain valid standardized categories.

---

## 4. customer_services

**Grain:** One row per customer.

| Column | Type | Key | Description |
|---|---|---|---|
| Customer_ID | VARCHAR(10) | PK/FK | Customer identifier |
| Mobile_App | VARCHAR(10) | | Mobile app adoption: Yes/No |
| Streaming | VARCHAR(10) | | Streaming service adoption: Yes/No |
| Cloud_Storage | VARCHAR(10) | | Cloud storage adoption: Yes/No |
| Premium_Support | VARCHAR(10) | | Premium support adoption: Yes/No |
| Family_Plan | VARCHAR(10) | | Family plan adoption: Yes/No |

### Business rules
- One row per customer.
- Customer_ID must exist in customers.
- Service values should be Yes/No.

---

## 5. support_tickets

**Grain:** One row per support ticket.

| Column | Type | Key | Description |
|---|---|---|---|
| Ticket_ID | VARCHAR(15) | PK | Unique support ticket identifier |
| Customer_ID | VARCHAR(10) | FK | Customer associated with ticket |
| Ticket_Date | DATETIME | | Ticket creation timestamp |
| Issue_Type | VARCHAR(30) | | Support issue category |
| Resolution_Time_Hours | DECIMAL(8,2) | | Time required to resolve ticket |
| Satisfaction_Score | TINYINT UNSIGNED | | Customer satisfaction score from 1 to 5 |
| Resolved | VARCHAR(10) | | Whether ticket was resolved: Yes/No |

### Business rules
- Ticket_ID must be unique and non-null.
- Customer_ID must exist in customers.
- Resolution_Time_Hours must be non-negative.
- Satisfaction_Score must be between 1 and 5.
- Resolved should contain Yes/No.

---

## 6. Data_Dictionary

The original workbook contains a `Data_Dictionary` sheet with metadata describing the source fields.

It is documentation metadata rather than an analytical fact table and therefore is not required for business KPI joins.

---

## Relationship model

```text
                    customers
                  Customer_ID PK
                  /     |     \
                 /      |      \
                ↓       ↓       ↓
       subscriptions  payments  customer_services
       Subscription_ID Payment_ID
       Customer_ID FK  Customer_ID FK
                         \
                          \
                       support_tickets
                       Ticket_ID PK
                       Customer_ID FK
```

### Cardinality

```text
customers
    1 ─────── 1 subscriptions

customers
    1 ─────── N payments

customers
    1 ─────── 1 customer_services

customers
    1 ─────── N support_tickets
```

The one-to-many relationships are the reason customer-level pre-aggregation is required before combining payment/support metrics with subscription-level churn metrics.
