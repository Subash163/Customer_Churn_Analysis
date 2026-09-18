# SQL Business Questions — Customer Churn Analysis

This document is the business-question index for the SQL stage.

## Customer

1. How many customers are in the customer base?
2. What is the demographic profile?
3. Which states have the largest customer bases?
4. Which cities have the largest customer bases?
5. How has customer acquisition changed over time?
6. Which signup cohorts are largest?

## Churn

1. What is the overall churn rate?
2. Which plan has the highest churn?
3. Which contract type has the highest churn?
4. At what lifecycle stage is churn highest?
5. Which segments have high churn and meaningful customer volume?
6. How much monthly revenue is at risk?

## Payments

1. What is the payment success rate?
2. Which payment methods are most used?
3. Do payment failures differ between active and churned customers?
4. Which payment-failure segment has the highest churn?
5. Which payment methods have the highest failure rates?

## Support

1. What is the overall support workload?
2. Which issue types generate the most tickets?
3. Does support experience differ between active and churned customers?
4. Which ticket-volume segment has the highest churn?
5. Which issue types are associated with lower retention?

## Retention

1. What is the overall retention rate?
2. Which plan retains customers best?
3. Which contract type provides the strongest retention?
4. Does service adoption correspond with stronger retention?
5. Which plan/contract segments have strong retention and meaningful volume?
6. How much monthly revenue is currently retained?

## Management

1. Where should management focus first?
2. Which plan/contract combination represents the greatest revenue risk?
3. Which high-value active customers show multiple risk signals?
4. How much revenue is associated with churned customers showing payment/support risk?
5. Which states combine large customer bases with high churn?
6. What does the executive churn scorecard look like?

## Interview framing

For each question, be ready to explain:

```text
Business question
      ↓
Required tables
      ↓
Table grain
      ↓
JOIN strategy
      ↓
Aggregation / CTE / window function
      ↓
Validation
      ↓
Business interpretation
```
