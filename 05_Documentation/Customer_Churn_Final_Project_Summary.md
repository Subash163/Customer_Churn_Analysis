# Customer Churn & Retention Analysis — Final Project Summary

## Executive Summary
Overall customer churn is **22.3%**, representing approximately **4,000+ churned customers out of 20,000 customers**.

## Key Findings
- Monthly contracts have the highest churn at **28.0%**, compared with **14.9% One Year** and **13.7% Two Year**.
- Premium has the highest plan churn at **31.3%**.
- Standard has the largest absolute churn volume with **1,847 churned customers**.
- Support ticket groups do not show a simple linear churn pattern.
- Average resolution time is almost identical for Active and Churned customers: **7.98 vs 7.95 hours**.
- Average satisfaction is approximately **4.4** for both groups.
- Payment failures do not show a simple positive relationship with churn in the current aggregate analysis.

## Business Recommendations
1. Target Monthly customers with retention and contract-conversion strategies.
2. Investigate the reasons behind Premium customer churn.
3. Address Standard churn at scale because of its larger absolute churn volume.
4. Do not use support-ticket count as a standalone churn rule.
5. Build a multi-factor customer-level churn-risk framework.
6. Improve payment-failure analysis using customer-level rates, frequency and timing.

## Retention Priority
| Priority | Segment / Area | Reason |
|---|---|---|
| 1 | Monthly contracts | Highest contract-level churn: 28.0% |
| 2 | Premium customers | Highest plan churn: 31.3% |
| 3 | Standard customers | Largest absolute churn volume: 1,847 |
| 4 | Multi-factor risk segments | Single variables do not fully explain churn |
| 5 | Support & payment analysis | Requires deeper customer-level analysis |

## Limitations
The analysis identifies associations and differences, not causation. Aggregate metrics can hide customer-level patterns. Payment comparisons should account for transaction exposure, and plan/contract comparisons should ideally account for tenure. The current dashboard is descriptive/diagnostic rather than a machine-learning prediction model.

## Final Conclusion
Churn should not be managed using a single metric. Contract type and plan reveal clear segment-level differences, while support and payment metrics do not show straightforward relationships with churn in this dataset.

The strongest next step is to combine customer profile, subscription, payment, support, tenure and engagement variables into a multi-factor churn-risk framework.

> **Which customers are most at risk of churning, and what retention action should the business take?**
