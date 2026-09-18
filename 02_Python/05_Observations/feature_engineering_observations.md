# Feature Engineering Observations

## Project

**Customer Churn & Retention Analysis**

---

# Objective

Transform the 86-column analytical dataset into a business-ready feature dataset for churn analytics and predictive modeling.

---

# Dataset Transformation

| Stage                | Columns |
| -------------------- | ------: |
| Final Dataset        |      86 |
| Feature Dataset      | **119** |
| New Features Created |  **33** |

Rows remained constant at **20,000**.

---

# Feature Categories

## Customer Features

* age_group
* signup_year
* signup_month
* signup_quarter
* signup_year_month

Purpose: Customer demographic segmentation.

---

## Revenue Features

* annual_subscription_value
* monthly_charge_band
* plan_category
* contract_category

Purpose: Revenue and pricing analysis.

---

## Churn Features

* churn_target
* churn_year_engineered
* churn_month_engineered
* churn_quarter_engineered
* tenure_at_churn_months
* tenure_at_churn_years
* tenure_segment_engineered

Purpose: Customer lifecycle modeling.

---

## Payment Features

* payment_failure_flag
* payment_activity_segment
* payment_value_segment
* low_payment_success_flag

Purpose: Payment behavior profiling.

---

## Service Adoption Features

* service_count
* service_adoption_rate
* service_adoption_segment

Purpose: Product engagement measurement.

---

## Support Features

* support_usage_segment
* support_experience_segment
* support_risk_flag
* support_experience_risk

Purpose: Customer support risk analysis.

---

## Engagement Features

* customer_engagement_score
* customer_engagement_level
* high_value_customer

Purpose: Customer value segmentation.

---

# Validation Results

| Metric         |    Value |
| -------------- | -------: |
| Total Checks   |       19 |
| Passed         |       17 |
| Failed         |    **0** |
| Overall Status | **PASS** |

---

# Key Observations

### 1. Business Features Were Created Instead of Raw Metrics

The project emphasizes analytical variables rather than simply storing transactional values.

### 2. Customer Segmentation Became Easier

Age, payment behavior, service adoption, and engagement can now be analyzed as meaningful customer groups.

### 3. Predictive Features Were Separated from Technical Fields

Identifiers remain unchanged while engineered features are clearly distinguishable.

### 4. No Information Loss

Rows remained identical after feature engineering.

---

# Recruiter Highlights

* Created 33 business-ready engineered features.
* Designed interpretable customer segmentation variables.
* Built reusable behavioral indicators for churn prediction.
* Validated engineered features using an automated QA framework.

---

**Pipeline Stage:** Final Dataset → Feature Engineering → Validation
