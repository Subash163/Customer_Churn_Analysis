# SQL Churn Driver Analysis — Observations

## 1. Objective

The Churn Driver Analysis evaluates customer churn across multiple dimensions to identify the customer characteristics, subscription attributes, payment behavior, service adoption, support experience, engagement patterns, and demographic segments associated with higher or lower observed churn.

The analysis is divided into eight modules:

1. Lifecycle Churn
2. Subscription Churn
3. Payment Churn
4. Service Churn
5. Support Churn
6. Engagement Churn
7. Customer Profile Churn
8. Multidimensional Churn

The objective is not to establish causation or build a statistically validated predictive model. Instead, the analysis identifies descriptive patterns that can support retention strategy and further investigation.

---

# 2. Overall Churn Context

The customer base contains:

* Total customers: 20,000
* Churned customers: 4,463
* Active customers: 15,537
* Overall churn rate: 22.32%
* Overall retention rate: 77.69%

The churn-driver analysis therefore focuses on understanding why churn varies across different customer segments rather than simply measuring overall churn.

---

# 3. Lifecycle Churn Observations

## 3.1 Churn by Tenure Band

Observed churn decreases substantially as customer tenure increases.

| Tenure Band  | Customers | Churned | Churn Rate |
| ------------ | --------: | ------: | ---------: |
| 0–2 months   |     1,642 |   1,175 |     71.56% |
| 3–5 months   |     2,170 |     983 |     45.30% |
| 6–11 months  |     3,665 |   1,164 |     31.76% |
| 12–23 months |     6,417 |     959 |     14.94% |
| 24+ months   |     6,106 |     182 |      2.98% |

### Observation

The strongest lifecycle pattern is concentrated in the early customer journey.

Customers with less than six months of tenure have substantially higher observed churn than customers with longer tenure. Churn falls from 71.56% among customers with 0–2 months of tenure to only 2.98% among customers with 24+ months of tenure.

### Business implication

The early customer lifecycle should be treated as a critical retention period.

Potential business actions include:

* Stronger onboarding during the first few months.
* Early engagement campaigns.
* Proactive communication with newly acquired customers.
* Monitoring early payment and usage activity.
* Identifying customers who become inactive shortly after signup.

---

## 3.2 Signup Cohort Churn

Current-status churn varies across signup cohorts:

* 2023 cohort: 16.04% churn
* 2024 cohort: 22.78% churn
* 2025 cohort: 29.53% churn

### Observation

Later signup cohorts currently show higher churn.

However, these figures should **not be interpreted as directly comparable lifetime churn rates**, because customers from the 2025 cohort have had less time to mature than customers from the 2023 cohort.

### Business implication

Recent cohorts should be monitored closely to determine whether the higher current churn reflects:

* weaker onboarding,
* changes in acquisition quality,
* changes in customer behavior,
* or simply shorter observation periods.

---

# 4. Subscription Churn Observations

## 4.1 Churn by Plan

Observed churn rates:

* Premium: 31.33%
* Standard: 21.63%
* Basic: 18.29%

### Observation

Premium customers have the highest observed churn rate among the three plans.

The Premium segment therefore represents an important retention opportunity because it combines relatively high churn with the highest monthly charges.

### Business implication

Retention strategies should pay particular attention to Premium customers, especially when Premium customers also exhibit other high-risk characteristics such as short tenure or low payment engagement.

---

## 4.2 Churn by Contract Type

Observed churn rates:

* Monthly: 27.98%
* One Year: 14.87%
* Two Year: 13.69%

### Observation

Monthly-contract customers show substantially higher churn than customers on longer contracts.

This is one of the clearest subscription-level churn patterns in the analysis.

### Business implication

Potential strategies include:

* Incentives for longer-term contracts.
* Renewal campaigns before monthly customers become inactive.
* Targeted offers encouraging monthly customers to move to annual contracts.
* Stronger retention communication for monthly subscribers.

This analysis shows an association between contract type and churn; it does not establish that changing contract type would itself cause churn to decrease.

---

## 4.3 Plan × Contract Interaction

The highest observed churn segment is:

* Premium + Monthly: 38.30%

Other combinations show considerably lower churn, particularly Basic customers on Two Year contracts:

* Basic + Two Year: 10.27%

### Observation

Plan and contract type appear to interact.

Premium Monthly customers combine two characteristics associated with higher churn:

* Premium plan
* Monthly contract

### Business implication

Retention programs should consider both dimensions together rather than targeting all customers within a plan or contract type equally.

---

## 4.4 Monthly Revenue at Risk

Modeled monthly recurring charge exposure from churned customers:

* Premium: ₹1,121,935.37
* Standard: ₹1,108,907.19
* Basic: ₹546,305.60
* Total: ₹2,777,148.16

### Observation

Premium and Standard customers account for the largest portions of modeled monthly recurring charge exposure among churned customers.

This metric represents **monthly recurring charge associated with churned subscriptions**, not historical realized revenue loss.

### Business implication

Retention prioritization should consider both:

1. Probability/observed rate of churn
2. Financial value associated with the customer

---

# 5. Payment Churn Observations

## 5.1 Failed Payment Count

The analysis shows:

* No failed payments: 34.65% churn
* 1 failed payment: 19.06%
* 2–3 failed payments: 9.39%
* 4+ failed payments: 3.67%

### Observation

The relationship is not monotonic. Customers with no failed payments have higher observed churn than customers with failed payments.

Therefore, failed payment count should **not** be interpreted as a standalone causal churn driver.

### Analytical consideration

Customers must have sufficient payment exposure to experience failed payments. Customers with short lifecycles may have fewer opportunities to generate failed payments.

This creates a potential lifecycle/exposure effect.

---

## 5.2 Primary Payment Method

Observed churn varies across customers' most frequently used payment methods:

* Net Banking: 39.95%
* Debit Card: 35.09%
* Wallet: 32.29%
* Credit Card: 26.16%
* UPI: 17.09%

### Observation

Payment method shows substantial variation in observed churn, with UPI customers showing the lowest churn among the major groups.

However, payment method alone should not be interpreted as a causal driver.

The Wallet group is also relatively small, so its rate should be interpreted cautiously.

---

## 5.3 Payment Success Rate

Customers with payment success rates below 80% show:

* 825 customers
* 46.42% churn

Customers with 95–100% payment success show:

* 10,846 customers
* 27.30% churn

### Observation

Low payment success appears to be a potentially useful customer-risk signal.

However, the relationship is not strictly linear across all bands, so payment success rate should be treated as a segmentation feature rather than a standalone predictive rule.

### Business implication

Customers experiencing repeated payment failures or low payment success may benefit from:

* Payment-method assistance.
* Payment retry communication.
* Alternative payment options.
* Proactive billing support.

---

# 6. Service Churn Observations

## 6.1 Individual Service Adoption

Churn rates across individual services are very similar, generally around 22%.

Examples include:

* Cloud Storage: 22.50% among users
* Family Plan: 21.84% among users
* Mobile App: 22.28% among users
* Premium Support: 22.23% among users
* Streaming: 22.23% among users

### Observation

Individual service adoption is a **weak discriminator of churn** in this dataset.

The differences between users and non-users are small.

### Business implication

Service adoption should not be treated as a major standalone churn driver based on this analysis.

---

## 6.2 Number of Services Adopted

Observed churn:

* 0 services: 21.48%
* 1 service: 22.49%
* 2 services: 22.37%
* 3 services: 22.44%
* 4 services: 22.08%
* 5 services: 19.34%

### Observation

Customers with different numbers of adopted services have broadly similar churn rates.

Customers using all five services show somewhat lower churn, but the group is relatively small.

### Conclusion

Overall service adoption appears to have limited explanatory power compared with lifecycle, contract type, and payment engagement.

---

# 7. Support Churn Observations

## 7.1 Ticket Volume

Observed churn is relatively similar across support-ticket frequency groups.

The highest rate occurs among customers with no tickets:

* No tickets: 23.14%

Customers with 6+ tickets show:

* 19.59% churn

### Observation

Higher support-ticket volume does not correspond to higher churn in a simple linear pattern.

Therefore, ticket volume alone is not a strong churn discriminator in this dataset.

---

## 7.2 Customer Satisfaction

Observed churn increases as satisfaction decreases:

* Satisfaction 1–<2: 28.77%
* Satisfaction 2–<3: 25.71%
* Satisfaction 3–<4: 22.94%
* Satisfaction 4–5: 22.04%

### Observation

Lower support satisfaction is associated with higher observed churn.

This is one of the more meaningful support-related patterns.

However, the lowest satisfaction groups are relatively small and should therefore be monitored rather than treated as definitive predictive segments.

### Business implication

Customers giving low satisfaction scores could be prioritized for:

* Service recovery.
* Follow-up communication.
* Escalation of unresolved issues.
* Retention outreach.

---

## 7.3 Unresolved Tickets

Observed churn:

* No unresolved tickets: 22.00%
* 1 unresolved ticket: 23.40%
* 2+ unresolved tickets: 22.61%

### Observation

Unresolved tickets show only a modest difference in observed churn.

Therefore, unresolved-ticket count alone is a weak discriminator.

---

## 7.4 Issue Type

Churn rates across issue categories are tightly grouped:

* General: 22.41%
* Billing: 22.37%
* Performance: 22.36%
* Technical: 22.00%
* Account: 21.62%

### Observation

Support issue type has very limited differentiation in this dataset.

The analysis does not show one particular support issue category as a major standalone churn driver.

---

# 8. Engagement Churn Observations

## 8.1 Successful Payment Activity

Customers were grouped according to the number of months with successful payments.

Observed churn:

* Low activity (≤3 months): 71.28%
* Medium activity (4–6 months): 44.20%
* High activity (>6 months): 13.71%

### Observation

Payment activity is one of the strongest behavioral signals identified in the analysis.

Customers with low successful-payment activity have substantially higher observed churn than highly active customers.

### Important analytical consideration

Payment activity is strongly related to customer lifecycle. New customers naturally have fewer months of payment history.

Therefore, this result should be interpreted as a strong **engagement signal**, not proof that increasing payment frequency would necessarily prevent churn.

---

## 8.2 Composite Engagement Score

The rule-based engagement score produced:

* Very Low: 66.90% churn
* Low: 46.58%
* Medium: 20.62%
* High: 14.89%

### Observation

The composite score shows a clear relationship between stronger engagement and lower observed churn.

This supports using multiple engagement indicators together rather than relying on one behavioral metric.

### Limitation

The score is rule-based and has not been statistically validated.

It should therefore be treated as an analytical segmentation framework rather than a predictive churn model.

---

## 8.3 Payment Recency

Using the analytical cutoff of 2025-12-26:

* No successful payment: 85.71% churn
* 0–30 days: 22.06%
* 31–60 days: 26.11%
* 61–90 days: 20.41%
* 91+ days: 50.00%

### Observation

The very small "No Successful Payment" and 91+ day groups should not be overinterpreted.

The 31–60 day group shows higher churn than the 0–30 day group, but the pattern is not perfectly monotonic.

### Conclusion

Payment recency can be useful as an engagement-monitoring feature, but the small tail groups require additional data before establishing robust thresholds.

---

# 9. Customer Profile Churn

## 9.1 Age

Churn rates across the major age bands are relatively close, generally around 21–23%.

The highest standard age-band churn is:

* 45–54: 23.03%

### Observation

Age is a weak churn discriminator in this dataset.

---

## 9.2 Gender

Observed churn:

* Male: 22.59%
* Female: 21.99%
* Missing: 24.05%

### Observation

Gender differences are very small.

Gender should therefore not be considered a major churn driver based on this analysis.

The missing-gender group is also very small.

---

## 9.3 State

State-level churn rates show modest variation.

Highest observed churn:

* Telangana: 23.51%
* Kerala: 23.09%

Lowest:

* Tamil Nadu: 21.60%

### Observation

Geographic variation exists but remains relatively narrow.

State is therefore a potential segmentation variable, but it is substantially weaker than lifecycle, contract type, and engagement.

---

## 9.4 Age × Gender

The age × gender analysis also shows relatively modest differences.

Some small groups show higher rates, but these groups should not be overinterpreted because of smaller sample sizes.

### Conclusion

Demographic variables appear to have limited explanatory value compared with behavioral and subscription characteristics.

---

# 10. Multidimensional Churn Observations

## 10.1 Multidimensional Segmentation

Combining lifecycle, plan, contract type, payment risk, support risk, and service adoption reveals substantial variation between customer segments.

The highest observed churn rates are concentrated among **New customers**, particularly Premium and Monthly-contract customers.

For example:

* New + Standard + Monthly + High Support Risk: 86.36%
* New + Premium + Monthly + Support Risk: 83.64%
* New + Premium + Monthly + No Support Risk + High Service Adoption: 81.40%

These segments demonstrate that lifecycle stage can dominate the observed churn pattern when combined with subscription characteristics.

### Observation

The multidimensional analysis demonstrates why single-variable churn analysis is insufficient.

Customer characteristics interact, and the same payment or support condition can have very different observed churn rates depending on lifecycle and subscription structure.

---

## 10.2 Lifecycle × Subscription × Payment Engagement

The second multidimensional analysis produced a particularly clear pattern.

Examples:

* New + Premium + Monthly + Low Payment Engagement: 81.88% churn
* New + Standard + Monthly + Low Payment Engagement: 77.17%
* New + Basic + Monthly + Low Payment Engagement: 70.05%

In contrast:

* Mature + Standard + Two Year + High Payment Engagement: 3.60%
* Mature + Basic + Two Year + High Payment Engagement: 2.96%

### Observation

The combination of **early lifecycle + monthly contract + low payment engagement** represents a particularly important retention segment.

Conversely, mature customers with high payment engagement and longer contracts show much lower observed churn.

### Business implication

Retention strategy should prioritize combinations of characteristics rather than treating each driver independently.

---

# 11. Active Customer Retention Priority

The final multidimensional query translated historical churn patterns into an actionable retention-priority framework.

The framework evaluates active customers using five observed characteristics:

1. New lifecycle
2. Monthly contract
3. Premium plan
4. Low payment engagement
5. Low service adoption

Customers receive a priority factor count from 0 to 5.

The resulting top-100 list contains active customers with the highest concentration of these characteristics.

Several of the highest-priority customers have all five factors and are therefore classified as **Very High Priority**.

### Business implication

This output can be used as a starting point for a retention campaign.

Potential actions include:

* Proactive onboarding for new customers.
* Personal outreach to Premium Monthly customers.
* Payment-engagement campaigns.
* Service adoption education.
* Retention offers before the customer reaches a likely disengagement point.

### Important limitation

The priority framework is **rule-based**.

It is not a machine-learning model, probability-of-churn score, or statistically validated risk model.

The framework should therefore be described as:

> "A rule-based retention prioritization framework derived from observed historical churn patterns."

---

# 12. Major Churn Drivers Identified

Based on the combined analysis, the strongest observable patterns are:

### Strong signals

**1. Customer lifecycle / tenure**

Early-tenure customers have dramatically higher observed churn.

**2. Contract type**

Monthly customers show substantially higher churn than One Year and Two Year customers.

**3. Payment engagement**

Low successful-payment activity is strongly associated with higher churn.

**4. Composite engagement**

Customers with weaker engagement profiles show substantially higher observed churn.

**5. Premium Monthly combination**

Premium customers on Monthly contracts represent a particularly high-churn subscription segment.

---

# 13. Moderate / Supporting Signals

The following variables show some useful variation but should not be treated as dominant drivers:

* Payment method
* Payment success rate
* Support satisfaction
* Payment recency
* Geographic state
* Service adoption

These variables may become more useful when combined with stronger lifecycle and subscription variables.

---

# 14. Weak Churn Discriminators

The analysis shows limited differentiation from:

* Gender
* Age
* Individual service adoption
* Number of support tickets
* Support issue type
* Unresolved ticket count

These variables may still be useful for segmentation, but they should not be prioritized as major churn drivers based on the current dataset.

---

# 15. Key Business Recommendations

Based on the SQL churn-driver analysis, the following retention strategy is recommended.

## 15.1 Strengthen Early-Lifecycle Retention

Focus heavily on the first six months.

Recommended actions:

* Structured onboarding journey.
* First-30/60/90-day engagement monitoring.
* Early payment and usage monitoring.
* Proactive communication when engagement drops.

---

## 15.2 Target Monthly Customers

Monthly customers have materially higher churn than longer-term contract customers.

Recommended actions:

* Renewal reminders.
* Loyalty incentives.
* Annual-plan upgrade offers.
* Benefits communication for longer contracts.

---

## 15.3 Prioritize Premium Monthly Customers

Premium Monthly customers combine:

* Higher plan value
* Higher observed churn
* Monthly contract structure

This makes them strategically important from both a retention and revenue perspective.

---

## 15.4 Monitor Payment Engagement

Customers with low successful-payment activity should be monitored as potential disengagement signals.

Recommended actions:

* Payment reminders.
* Payment-method assistance.
* Alternative payment options.
* Proactive customer contact.

---

## 15.5 Use Engagement-Based Retention

Rather than relying only on demographic characteristics, prioritize behavioral indicators such as:

* Successful payment activity
* Payment recency
* Contract type
* Tenure
* Plan
* Service engagement

These variables provide more actionable segmentation.

---

## 15.6 Combine Churn Risk With Customer Value

Retention efforts should consider both:

* likelihood/observed rate of churn
* monthly recurring charge associated with the customer

This prevents the business from focusing only on the largest churn percentages while overlooking financially important customers.

---

# 16. Analytical Limitations

The following limitations should be explicitly acknowledged.

### 16.1 Association Is Not Causation

The analysis identifies relationships between customer characteristics and churn.

It does not prove that a particular characteristic causes churn.

---

### 16.2 Lifecycle / Exposure Effect

Many behavioral measures naturally depend on how long a customer has been active.

For example, newer customers have fewer opportunities to accumulate successful payment months.

Therefore, engagement metrics should be interpreted alongside tenure.

---

### 16.3 Cohort Comparability

Signup cohorts have different observation periods.

The 2025 cohort has had less time to mature than the 2023 cohort.

Therefore, cohort churn rates represent current status rather than directly comparable lifetime churn.

---

### 16.4 Small Segments

Some multidimensional segments contain relatively few customers.

High churn rates in small groups should not automatically be treated as reliable business rules.

Minimum sample-size filters were used in multidimensional analyses to reduce this problem.

---

### 16.5 Rule-Based Prioritization

The final retention-priority framework is manually defined from observed patterns.

It has not been statistically validated.

It should not be represented as a predictive model.

---

### 16.6 Historical Analysis

The analysis describes the available historical dataset.

Future customer behavior may differ from historical behavior.

---

# 17. Overall Conclusion

The SQL Churn Driver Analysis shows that **customer lifecycle, contract structure, and behavioral engagement are substantially more informative churn dimensions than basic demographics or individual service adoption**.

The strongest observed pattern is concentrated among customers who are:

* early in their lifecycle,
* subscribed to Monthly contracts,
* particularly on Premium plans,
* and showing low payment engagement.

In contrast, mature customers with strong payment engagement and longer-term contracts show substantially lower observed churn.

The analysis therefore supports a retention strategy centered on:

**early-lifecycle intervention + monthly-contract management + engagement monitoring + value-based customer prioritization.**

The final multidimensional analysis translates these findings into an actionable active-customer retention-priority list while clearly distinguishing rule-based prioritization from statistically validated churn prediction.

---

## 18. SQL Analysis Status

| Module                 | Status   |
| ---------------------- | -------- |
| Lifecycle Churn        | COMPLETE |
| Subscription Churn     | COMPLETE |
| Payment Churn          | COMPLETE |
| Service Churn          | COMPLETE |
| Support Churn          | COMPLETE |
| Engagement Churn       | COMPLETE |
| Customer Profile Churn | COMPLETE |
| Multidimensional Churn | COMPLETE |

**Overall Churn Driver Analysis: COMPLETE**
