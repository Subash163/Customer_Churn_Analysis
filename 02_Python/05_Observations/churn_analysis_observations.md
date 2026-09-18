# Churn Analysis Observations

## 1. Purpose

The Churn Analysis stage was performed after EDA and Feature Engineering to identify customer segments associated with higher observed churn.

The objective was not to build a predictive machine-learning model, but to understand:

* Overall churn performance
* Customer lifecycle risk
* Subscription-related churn patterns
* Payment-related churn patterns
* Service adoption patterns
* Support experience patterns
* Customer engagement patterns
* High-risk customer combinations
* Retention opportunities

The analysis was performed at the customer level using the feature-engineered analytical dataset.

---

## 2. Source Dataset

Source:

```text
outputs/feature_engineering/customer_analytical_features.xlsx
```

Dataset characteristics:

* Customers analyzed: 20,000
* Columns: 119
* Grain: One row per customer
* Churned customers: 4,463
* Active customers: 15,537
* Verified churn rate: 22.32%
* Verified retention rate: 77.69%

The final analytical dataset was used as the single customer-level analytical source.

---

## 3. Churn KPI Convention

The project uses the following verified KPI convention:

```text
Total Customers = 20,000
Churned Customers = 4,463
Active Customers = 15,537
```

Independent churn calculation:

```text
4,463 / 20,000 × 100
= 22.315%
≈ 22.32%
```

Retention:

```text
15,537 / 20,000 × 100
≈ 77.69%
```

The project uses deterministic two-decimal reporting with `ROUND_HALF_UP`.

---

## 4. Analysis Areas

The Churn Analysis module evaluated the following areas:

1. Overall Churn KPI
2. Customer Profile
3. Subscription
4. Payment
5. Services
6. Support
7. Customer Engagement
8. Risk Segments
9. Numerical Comparisons
10. Churn Driver Summary
11. Retention Analysis
12. Multi-Dimensional Risk Combinations

---

## 5. Important Analytical Rule

Churn outcome and post-outcome fields were excluded from explanatory driver analysis.

The following fields were treated as outcome/leakage or descriptive churn fields rather than independent explanatory drivers:

* churn_target
* churn_status
* churn_date
* is_churned
* is_active
* has_churn_date
* has_end_date
* end_date
* tenure_days_at_churn
* tenure_months_at_churn
* tenure_years_at_churn
* churn_year
* churn_month
* churn_month_name
* churn_quarter
* churn_year_month
* churn_timing_segment
* churn_data_quality_flag
* churn_year_engineered
* churn_month_engineered
* churn_month_name_engineered
* churn_quarter_engineered
* churn_year_month_engineered
* tenure_at_churn_months
* tenure_at_churn_years
* tenure_segment_engineered

These fields can be useful for descriptive churn reporting but should not be presented as independent churn drivers.

---

## 6. Major Churn Patterns Observed

Several segments showed materially higher observed churn than the overall project baseline.

The overall baseline was:

```text
22.32%
```

Examples of higher observed churn segments included:

### Low Payment Activity

Customers classified into the Low payment activity segment showed substantially higher observed churn than the overall baseline.

This indicates that payment activity can be useful as a customer-risk indicator.

---

### Low Payment Value

The Low payment value segment also showed higher observed churn than the project baseline.

This segment should be interpreted together with customer value and engagement rather than treated as a standalone cause.

---

### Early Tenure

Customers in the earliest tenure segments showed particularly high observed churn.

The strongest example was:

```text
0–3 Months
Customer Count: 1,647
Churned: 1,183
Observed Churn Rate: 71.83%
```

This was substantially above the project baseline.

The finding indicates that the early customer lifecycle represents an important retention intervention window.

---

### 4–6 Month Tenure

Another elevated segment was:

```text
4–6 Months
Customer Count: 2,152
Churned: 979
Observed Churn Rate: 45.49%
```

This was also substantially above the project baseline.

Together, the early-tenure findings suggest that retention efforts should not begin only after customers become long-term users.

---

### Payment Method

Some primary payment methods displayed higher observed churn than the overall baseline.

Examples included:

```text
Net Banking
Customer Count: 811
Observed Churn Rate: 39.95%

Debit Card
Customer Count: 1,536
Observed Churn Rate: 35.09%

Wallet
Customer Count: 223
Observed Churn Rate: 32.29%
```

These findings should be interpreted as associations rather than causal relationships.

---

## 7. Small-Sample Caution

A very high observed churn rate does not automatically make a segment a major business driver.

For example:

```text
low_payment_success_flag = 1
Customer Count = 7
Churn Rate = 85.71%
```

Although the observed churn rate is extremely high, the customer population is too small to justify treating it as a major portfolio-level driver.

Therefore, customer segment size was considered alongside churn-rate difference.

---

## 8. Driver Interpretation Framework

The analysis used the following interpretation:

```text
Segment Size
      +
Observed Churn Rate
      +
Difference From Baseline
      ↓
Business Priority
```

This prevents small segments with extreme percentages from automatically receiving the highest business priority.

---

## 9. Causality Guardrail

The analysis does not establish that a particular factor causes churn.

The correct interpretation is:

> The segment is associated with higher observed churn.

The analysis is observational and descriptive.

Therefore, recommendations should be validated through controlled retention experiments before claiming causal impact.

---

## 10. Multi-Dimensional Analysis

The project also evaluated combinations of customer characteristics.

The purpose was to identify situations where multiple risk indicators occur together.

For example, a customer may simultaneously have:

* Low payment activity
* Low service adoption
* Early tenure

Such combinations can potentially represent stronger retention opportunities than considering each characteristic independently.

However, multi-dimensional findings were also evaluated for:

* Customer population size
* Observed churn rate
* Churn difference from baseline
* Evidence strength

This prevents very small combinations from being over-interpreted.

---

## 11. Retention Analysis

Retention was analyzed as the complementary business outcome to churn.

The project baseline:

```text
Churn Rate     = 22.32%
Retention Rate = 77.69%
```

The retention analysis focused on identifying customer groups where improving retention could produce meaningful business value.

---

## 12. Churn Analysis Outputs

The analysis generated:

```text
outputs/churn_analysis/
```

including:

* `churn_analysis_report.xlsx`
* `churn_by_customer_profile.xlsx`
* `churn_by_engagement.xlsx`
* `churn_by_payment.xlsx`
* `churn_by_services.xlsx`
* `churn_by_subscription.xlsx`
* `churn_by_support.xlsx`
* `churn_driver_summary.xlsx`
* `churn_kpi_summary.xlsx`
* `churn_numerical_comparison.xlsx`
* `churn_risk_segments.xlsx`
* `combined_churn_risk_segments.xlsx`
* `retention_analysis.xlsx`

---

## 13. Validation

The independent Churn Analysis validator completed successfully:

```text
Total Checks  : 32
Failed Checks : 0
Overall Churn Analysis Validation : PASS
```

This confirms that the generated churn-analysis outputs passed the defined structural and metric validation rules.

---

## 14. Business Interpretation

The most important observation from this stage is that churn was not uniformly distributed across the customer base.

Higher observed churn was concentrated in specific customer segments, particularly:

* Early-tenure customers
* Low payment activity customers
* Low payment value customers
* Certain payment-method groups
* Selected low-engagement/risk combinations

These patterns became the evidence base for the next stage:

```text
Churn Analysis
      ↓
Business Insights
      ↓
Business Recommendations
```

---

## 15. Key Learning

The Churn Analysis stage demonstrated the difference between:

```text
High Churn Rate
```

and:

```text
High Business Priority
```

A segment becomes more useful for business decision-making when its:

* customer population is meaningful,
* churn is materially above baseline,
* evidence is reliable,
* and the segment can be practically targeted.

This principle was carried forward into Business Insights and Business Recommendations.
