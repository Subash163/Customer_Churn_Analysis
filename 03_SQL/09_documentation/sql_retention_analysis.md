# Customer Churn & Retention Analysis

## SQL Retention Analysis — Observations & Business Insights

---

## 1. Objective

The Retention Analysis module examines customer retention from multiple business dimensions using SQL.

The analysis focuses on identifying:

* How retention changes across customer lifecycle stages
* Which subscription plans and contract types retain customers better
* How payment behavior relates to retention
* Whether service adoption is associated with stronger retention
* Whether customer support experience is associated with retention
* Whether high-value customers require greater retention attention
* Which active customers may warrant retention prioritization based on multiple risk indicators

All retention calculations use the subscription-level customer status as the primary retention anchor.

### Retention Definition

Retention Rate:

**Retained Customers / Total Customers × 100**

where:

* Retained Customers = customers with `Churn_Status = 'Active'`
* Churned Customers = customers with `Churn_Status = 'Churned'`

The analysis is descriptive and identifies observed associations. It does not establish causal relationships.

---

# 2. Overall Retention Context

The customer base contains:

* **20,000 total customers**
* **15,537 active customers**
* **4,463 churned customers**
* **77.69% overall retention**
* **22.32% overall churn**

This overall retention rate provides the benchmark against which individual segments are compared.

The analysis shows that retention varies considerably across some dimensions, particularly **customer lifecycle and contract type**, while other dimensions such as **service adoption and support issue type** show relatively limited differentiation.

---

# 3. Retention by Lifecycle

## Key Findings

Retention increases substantially as customers move through the lifecycle.

| Tenure Band  | Customers | Retained | Churned |  Retention |
| ------------ | --------: | -------: | ------: | ---------: |
| 0–2 Months   |     1,642 |      467 |   1,175 | **28.44%** |
| 3–5 Months   |     2,170 |    1,187 |     983 | **54.70%** |
| 6–11 Months  |     3,665 |    2,501 |   1,164 | **68.24%** |
| 12–23 Months |     6,417 |    5,458 |     959 | **85.06%** |
| 24+ Months   |     6,106 |    5,924 |     182 | **97.02%** |

### Observation

The earliest lifecycle stage represents the highest retention risk.

Retention increases from only **28.44% among customers with 0–2 months of tenure** to **97.02% among customers with 24+ months of tenure**.

This represents a difference of approximately **68.58 percentage points**.

### Business Interpretation

The results strongly indicate that the **early customer lifecycle is the most important retention window**.

Customers who successfully remain beyond the early lifecycle stages demonstrate substantially higher observed retention.

### Recommendation

Retention efforts should place particular emphasis on:

* New-customer onboarding
* Early engagement
* First-month experience
* Early payment experience
* Early support experience
* Preventing avoidable early churn

---

# 4. Retention by Plan

## Key Findings

| Plan     | Customers | Retained | Churned |  Retention |
| -------- | --------: | -------: | ------: | ---------: |
| Basic    |     7,479 |    6,111 |   1,368 | **81.71%** |
| Standard |     8,538 |    6,691 |   1,847 | **78.37%** |
| Premium  |     3,983 |    2,735 |   1,248 | **68.67%** |

### Observation

Premium customers have the lowest retention rate:

**Premium: 68.67%**

compared with:

* Standard: 78.37%
* Basic: 81.71%

The difference between Basic and Premium retention is approximately **13.04 percentage points**.

### Business Interpretation

Premium customers represent a smaller customer population but have substantially lower observed retention.

This makes Premium customers particularly important when retention is evaluated together with revenue exposure.

### Recommendation

Premium customers should receive additional retention attention, particularly when they also exhibit other risk indicators.

---

# 5. Retention by Contract Type

## Key Findings

| Contract Type | Customers | Retained | Churned |  Retention |
| ------------- | --------: | -------: | ------: | ---------: |
| Two Year      |     3,046 |    2,629 |     417 | **86.31%** |
| One Year      |     5,326 |    4,534 |     792 | **85.13%** |
| Monthly       |    11,628 |    8,374 |   3,254 | **72.02%** |

### Observation

Monthly-contract customers have substantially lower retention than customers on longer contracts.

* Monthly: **72.02%**
* One Year: **85.13%**
* Two Year: **86.31%**

Monthly retention is approximately **13–14 percentage points lower** than annual and two-year contracts.

### Active Customer Mix

Among active customers:

* Monthly: **53.90%**
* One Year: **29.18%**
* Two Year: **16.92%**

Therefore, monthly contracts represent both:

1. The lowest-retention contract group
2. The largest portion of the current active customer base

### Business Interpretation

The monthly-contract population represents an important retention opportunity because it combines **high customer volume with lower retention**.

### Recommendation

Potential retention strategies should prioritize monthly customers, especially:

* Premium Monthly
* New Monthly customers
* Monthly customers showing payment or support risk indicators

---

# 6. Plan × Contract Retention

The combination of plan and contract type provides more detailed segmentation.

### Highest-retention combinations

* Basic + Two Year: **89.73%**
* Basic + One Year: **88.16%**
* Standard + Two Year: **87.47%**
* Standard + One Year: **85.62%**

### Lowest-retention combinations

* Premium + Monthly: **61.70%**
* Standard + Monthly: **72.64%**
* Basic + Monthly: **76.72%**

### Key Observation

**Premium Monthly customers represent the weakest retention segment among the major plan-contract combinations.**

This is more actionable than analyzing plan or contract type independently because it identifies a specific customer segment.

---

# 7. Retention by Payment Behavior

Payment behavior was analyzed through:

* Number of failed payments
* Payment success rate
* Primary payment method

## 7.1 Payment Failure Count

The observed relationship was non-linear.

| Failure Band        |  Retention |
| ------------------- | ---------: |
| 4+ Failed Payments  | **96.33%** |
| 2–3 Failed Payments | **90.61%** |
| 1 Failed Payment    | **80.94%** |
| No Failed Payments  | **65.35%** |

### Observation

Customers with more recorded payment failures show higher observed retention, which is counterintuitive.

### Interpretation

This result should **not** be interpreted as evidence that failed payments improve retention.

A likely explanation is customer exposure:

* Longer-lived customers have more payment transactions.
* More transactions create more opportunities for payment failures.
* Customers who churn early have fewer opportunities to accumulate failures.

Therefore, payment failure count is affected by customer activity and tenure.

### Conclusion

**Payment failure count is a non-linear and potentially exposure-biased retention indicator.**

---

# 8. Payment Success Rate

| Payment Success Rate | Customers |  Retention |
| -------------------- | --------: | ---------: |
| 80–94%               |     8,329 | **86.57%** |
| 95–100%              |    10,846 | **72.70%** |
| <80%                 |       825 | **53.58%** |

### Observation

Customers with payment success below 80% have substantially lower observed retention at **53.58%**.

However, the 80–94% group has higher retention than the 95–100% group, showing that the relationship is not monotonic.

### Conclusion

**Very low payment success (<80%) is a potentially important retention warning signal, but payment success rate alone should not be interpreted as a simple linear retention driver.**

---

# 9. Retention by Primary Payment Method

| Primary Payment Method | Customers |  Retention |
| ---------------------- | --------: | ---------: |
| UPI                    |    11,371 | **82.91%** |
| Credit Card            |     6,059 | **73.84%** |
| Wallet                 |       223 | **67.71%** |
| Debit Card             |     1,536 | **64.91%** |
| Net Banking            |       811 | **60.05%** |

### Observation

UPI customers have the highest observed retention at **82.91%**.

Net Banking has the lowest at **60.05%**, but the Net Banking group contains only 811 customers.

Wallet also has a relatively small population of 223 customers.

### Interpretation

Payment method may provide a useful segmentation signal, but it should not be interpreted as evidence that payment method itself causes retention differences.

Other factors such as customer profile, tenure, plan and contract type may also differ across payment-method groups.

---

# 10. Retention by Service Adoption

Individual service adoption produced very similar retention rates.

Examples:

* Mobile App: Yes **77.72%**, No **77.50%**
* Streaming: Yes **77.77%**, No **77.57%**
* Premium Support: Yes **77.77%**, No **77.66%**
* Family Plan: Yes **78.16%**, No **77.50%**
* Cloud Storage: Yes **77.50%**, No **77.81%**

### Observation

Individual services show **very limited retention differentiation**.

The largest observed difference among the main Yes/No comparisons is only around one percentage point.

---

# 11. Retention by Service Count

| Services Adopted | Customers |  Retention |
| ---------------: | --------: | ---------: |
|                0 |       413 | **78.21%** |
|                1 |     3,248 | **77.56%** |
|                2 |     7,127 | **77.62%** |
|                3 |     6,472 | **77.52%** |
|                4 |     2,225 | **77.89%** |
|                5 |       305 | **80.66%** |

### Observation

Retention remains clustered around approximately 77–78% across most service-count groups.

The 5-service group has 80.66% retention, but it contains only 305 customers.

### Conclusion

**Service adoption appears to be a weak retention discriminator in this dataset.**

Service adoption alone should therefore not be treated as a primary retention lever.

---

# 12. Retention by Support Experience

Support was analyzed using:

* Ticket volume
* Customer satisfaction
* Unresolved tickets
* Issue type

## 12.1 Ticket Volume

| Ticket Volume |  Retention |
| ------------- | ---------: |
| 6+ Tickets    | **80.41%** |
| 2–3 Tickets   | **77.69%** |
| 4–5 Tickets   | **77.66%** |
| 1 Ticket      | **77.46%** |
| No Tickets    | **76.86%** |

### Observation

Ticket volume does not show a clear monotonic relationship with retention.

Customers with 6+ tickets actually have the highest observed retention.

Therefore:

**Higher ticket volume should not automatically be interpreted as higher churn risk.**

Customer tenure and exposure to support interactions may influence this result.

---

# 13. Retention by Support Satisfaction

| Satisfaction Band | Customers |  Retention |
| ----------------- | --------: | ---------: |
| 4–5               |    15,712 | **77.96%** |
| 3–<4              |     2,245 | **77.06%** |
| 2–<3              |       319 | **74.29%** |
| 1–<2              |        73 | **71.23%** |

### Observation

Support satisfaction shows the clearest relationship among the support metrics.

Retention increases as satisfaction improves:

**71.23% → 74.29% → 77.06% → 77.96%**

The difference between the highest and lowest satisfaction bands is **6.73 percentage points**.

### Important Limitation

The lowest-satisfaction groups are small:

* 319 customers in the 2–<3 band
* 73 customers in the 1–<2 band

Therefore, the result should be treated as a meaningful signal requiring further investigation rather than definitive evidence of causality.

### Business Interpretation

**Customer support satisfaction may be more useful for retention monitoring than ticket volume or issue category.**

---

# 14. Retention by Unresolved Tickets

| Unresolved Tickets    |  Retention |
| --------------------- | ---------: |
| No Unresolved Tickets | **78.00%** |
| 2+ Unresolved Tickets | **77.39%** |
| 1 Unresolved Ticket   | **76.60%** |

### Observation

The difference is relatively small.

The gap between no unresolved tickets and one unresolved ticket is only **1.40 percentage points**.

### Conclusion

Unresolved ticket count appears to be a **weak retention discriminator** in this dataset.

---

# 15. Retention by Support Issue Type

| Issue Type  |  Retention |
| ----------- | ---------: |
| Account     | **78.38%** |
| Technical   | **78.00%** |
| Performance | **77.64%** |
| Billing     | **77.63%** |
| General     | **77.59%** |

### Observation

Retention is highly similar across all issue types.

The difference between the highest and lowest groups is less than one percentage point.

### Conclusion

**Support issue category does not appear to be a major retention discriminator.**

---

# 16. High-Value Customer Retention

High-value customers were defined as the **top 25% of customers by Monthly Charge**.

This produces exactly:

**5,000 high-value customers**

## Key Findings

| Value Segment   | Customers |  Retention | Monthly Revenue at Risk |
| --------------- | --------: | ---------: | ----------------------: |
| Other Customers |    15,000 | **80.19%** |           ₹1,494,165.76 |
| High Value      |     5,000 | **70.18%** |       **₹1,282,982.40** |

### Observation

High-value customers have retention of only **70.18%**, compared with **80.19%** among other customers.

This is a difference of **10.01 percentage points**.

Despite representing only 25% of customers, the high-value group represents a substantial amount of monthly revenue exposure when customers churn.

### Business Interpretation

High-value customers should receive additional retention attention because churn among these customers has greater potential financial impact.

---

# 17. High-Value Retention by Plan

Among high-value customers:

| Plan     | High-Value Customers |  Retention | Monthly Revenue at Risk |
| -------- | -------------------: | ---------: | ----------------------: |
| Premium  |                3,971 | **68.65%** |       **₹1,120,096.65** |
| Standard |                1,029 | **76.09%** |             ₹162,885.75 |

### Key Finding

The high-value retention problem is concentrated heavily in the Premium segment.

Premium represents approximately **79% of high-value customers** and approximately **87% of the high-value monthly revenue at risk**.

### Business Priority

**High-value Premium customers should be the primary focus of targeted retention efforts.**

---

# 18. High-Value Multi-Factor Retention Prioritization

The final query creates a rule-based retention priority framework for active high-value customers.

The risk factors are:

1. At least one failed payment
2. At least one unresolved support ticket OR average support satisfaction below 4
3. Service adoption of one or fewer services

The resulting `risk_factor_count` ranges from **0 to 3**.

Customers are included in the priority list when:

* They belong to the top 25% by Monthly Charge
* They are currently Active
* They have at least two identified risk factors

### Interpretation

This creates a practical retention outreach list rather than attempting to predict churn statistically.

The output should therefore be interpreted as:

> **Active high-value customers who meet multiple rule-based retention risk criteria.**

It should **not** be interpreted as:

> Customers who are guaranteed or predicted to churn.

### Business Use

The list can be used to prioritize proactive retention actions such as:

* Account review
* Payment assistance
* Support follow-up
* Service engagement campaigns
* Premium customer outreach

---

# 19. Cross-Dimensional Retention Insights

Across all seven retention modules, the strongest observed patterns are:

### Strong Retention Signals

**1. Customer Lifecycle**

Retention increases dramatically with tenure.

Early lifecycle customers represent the clearest retention risk.

**2. Contract Type**

Monthly contracts have substantially lower retention than One Year and Two Year contracts.

**3. Plan**

Premium customers have lower retention than Basic and Standard customers.

**4. High-Value Segment**

High-value customers have materially lower retention than other customers and therefore deserve greater financial attention.

---

### Moderate / Potential Signals

**5. Support Satisfaction**

Lower satisfaction is associated with lower observed retention, although the lowest-satisfaction groups are relatively small.

**6. Very Low Payment Success**

Customers with payment success below 80% have substantially lower observed retention.

However, the overall payment-success relationship is non-linear.

---

### Weak Signals

**7. Service Adoption**

Individual service adoption and service count show limited retention differentiation.

**8. Support Issue Type**

Retention is highly similar across issue categories.

**9. Unresolved Ticket Count**

Only small differences in retention were observed.

**10. Ticket Volume**

The relationship is non-linear and does not clearly identify higher churn risk.

---

# 20. Recommended Retention Strategy

Based on the SQL findings, retention efforts should be prioritized rather than applied equally across the entire customer base.

## Priority 1 — New Customers

Focus on customers in the first few months of their lifecycle.

Potential actions:

* Stronger onboarding
* Early engagement campaigns
* First-payment monitoring
* Early support follow-up
* Education about available services

---

## Priority 2 — Monthly Contract Customers

Monthly customers have substantially lower retention and represent **53.90% of active customers**.

Potential actions:

* Contract conversion campaigns
* Annual-plan incentives
* Loyalty benefits
* Targeted renewal messaging

---

## Priority 3 — Premium Customers

Premium customers have only **68.67% overall retention**.

Potential actions:

* Premium customer success programs
* Personalized engagement
* Early warning monitoring
* Service-value communication

---

## Priority 4 — High-Value Premium Customers

This is the most financially important retention segment identified.

Particular attention should be given to **active high-value Premium customers** who have multiple risk indicators.

Potential actions:

* Proactive account management
* Personalized retention offers
* Payment issue resolution
* Dedicated support follow-up
* Service adoption campaigns

---

## Priority 5 — Low-Satisfaction Customers

Customers with lower support satisfaction should be monitored as potential retention-risk customers.

Potential actions:

* Service recovery
* Complaint resolution
* Follow-up after ticket closure
* Customer feedback analysis

---

# 21. Analytical Limitations

Several limitations should be considered when interpreting these results.

### 1. Descriptive analysis

The SQL analysis identifies associations and patterns.

It does **not prove causality**.

For example, the analysis cannot establish that monthly contracts cause churn.

---

### 2. Tenure / exposure bias

Payment and support metrics can depend on how long customers have been active.

Longer-tenured customers naturally have more opportunities to make payments or submit support tickets.

This can create misleading relationships when comparing raw activity counts.

---

### 3. Current-status retention

The analysis primarily evaluates whether a subscription is currently Active or Churned.

Therefore, some cohort comparisons represent current observed status rather than fully matured lifetime retention.

---

### 4. Small segment sizes

Some groups have relatively few customers, particularly:

* Wallet users
* Net Banking users
* Very low support satisfaction groups
* Five-service customers

Small groups should be interpreted cautiously.

---

### 5. Rule-based retention prioritization

The high-value multi-factor query is a **business-rule framework**, not a machine-learning or statistically validated predictive model.

The risk factors have not been statistically weighted or validated against future churn outcomes.

---

### 6. Revenue at risk

`monthly_revenue_at_risk` represents the sum of Monthly Charge among churned customers.

It is best interpreted as **modeled monthly revenue exposure**, not historical realized revenue loss.

---

# 22. Final Retention Analysis Conclusion

The SQL Retention Analysis demonstrates that customer retention is not equally influenced across all business dimensions.

The strongest observed patterns are concentrated around:

* **Customer lifecycle**
* **Contract type**
* **Plan**
* **Customer value**

The most significant retention challenge occurs among **new customers, monthly-contract customers, Premium customers, and high-value customers**.

The analysis also suggests that **support satisfaction and very low payment success may provide useful secondary warning signals**, while service adoption, support issue type, ticket volume and unresolved ticket count show relatively weak differentiation.

The most actionable retention opportunity is therefore to combine these dimensions rather than rely on a single metric.

A practical strategy would prioritize:

> **Active high-value Premium customers, particularly those on monthly contracts, in early lifecycle stages, and exhibiting multiple operational risk indicators.**

This provides a data-driven framework for moving from broad churn measurement toward **targeted customer retention and revenue protection**.

---

## 23. Module Completion Status

| Module                      | Status                                                      |
| --------------------------- | ----------------------------------------------------------- |
| 01 — Retention by Lifecycle | **Complete**                                                |
| 02 — Retention by Plan      | **Complete**                                                |
| 03 — Retention by Contract  | **Complete**                                                |
| 04 — Retention by Payment   | **Complete — with analytical caveats**                      |
| 05 — Retention by Service   | **Complete — weak differentiation**                         |
| 06 — Retention by Support   | **Complete — satisfaction is the strongest support signal** |
| 07 — High-Value Retention   | **Complete — rule-based prioritization**                    |

### Overall Status

**SQL Retention Analysis → COMPLETE**
