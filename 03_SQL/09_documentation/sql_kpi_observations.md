# SQL KPI Analysis Observations

## 1. Objective

The objective of the KPI Analysis stage was to calculate and evaluate key customer, churn, retention, subscription, payment, and support metrics using the validated data stored in the MySQL database.

The analysis was designed to establish a reliable business baseline before moving into deeper churn-driver analysis and business-question analysis.

The KPI analysis covers:

* Customer KPIs
* Churn KPIs
* Retention KPIs
* Subscription KPIs
* Payment KPIs
* Support KPIs

All KPI queries were executed against the validated MySQL database.

---

# 2. Customer KPI Observations

## 2.1 Customer Base

The database contains 20,000 customers, with 20,000 distinct Customer IDs, confirming a one-to-one customer record structure.

The average customer age is 36.20 years, with an age range of 18 to 75 years.

There are 240 customers with missing age values.

### Observation

The customer base is sufficiently complete for overall demographic analysis. Missing age values were retained as NULL rather than being replaced with mean or median values, preserving the original data characteristics.

---

## 2.2 Gender Distribution

The customer base consists of:

* Male: 10,517 customers (52.59%)
* Female: 9,404 customers (47.02%)
* Missing: 79 customers (0.40%)

### Observation

The gender distribution is relatively balanced, with a slightly higher proportion of male customers.

The 79 missing gender values represent only 0.40% of the customer base and are not large enough to materially affect overall gender distribution analysis.

---

## 2.3 Geographic Distribution

Tamil Nadu has the largest customer share at 16.65%, followed by Maharashtra at 16.53%.

The remaining states have customer shares ranging approximately from 7.91% to 8.68%.

At the city level, Lucknow has the highest customer count with 1,728 customers, representing 8.64% of the customer base.

There are 120 customers with missing city information, representing 0.60% of the customer base.

### Observation

The customer base is geographically concentrated in a small number of major states, with Tamil Nadu and Maharashtra accounting for the largest shares.

City-level analysis should treat missing city information explicitly rather than assigning a city based on assumptions.

---

## 2.4 Signup Trend

There are 7,162 customers from 2023, 7,075 from 2024, and 5,763 from 2025.

The 2025 figure represents January through October based on the available signup data and should therefore not be compared directly with the complete 2023 and 2024 years.

### Observation

Customer acquisition remained relatively consistent during 2023 and 2024. The lower 2025 total is partly explained by the incomplete year coverage.

Monthly signup volumes generally remained within a relatively narrow range, with March 2024 recording the highest monthly signup count at 645 customers.

---

# 3. Churn KPI Observations

## 3.1 Overall Churn

The subscription/customer population consists of:

* Total customers: 20,000
* Active customers: 15,537
* Churned customers: 4,463
* Churn rate: 22.32%
* Active/retained rate: 77.69%

### Observation

Approximately one in five customers in the analyzed population is classified as churned.

The 22.32% churn rate establishes the primary baseline for subsequent churn-driver analysis.

---

## 3.2 Churn by Plan

| Plan     | Customers | Churn Rate |
| -------- | --------: | ---------: |
| Basic    |     7,479 |     18.29% |
| Standard |     8,538 |     21.63% |
| Premium  |     3,983 |     31.33% |

### Observation

Premium customers have the highest observed churn rate at 31.33%, considerably higher than Basic and Standard customers.

Premium therefore represents an important segment for deeper investigation, particularly because it also has a substantially higher monthly charge.

This relationship is descriptive and does not establish that the Premium plan causes churn.

---

## 3.3 Churn by Contract Type

| Contract Type | Customers | Churn Rate |
| ------------- | --------: | ---------: |
| Monthly       |    11,628 |     27.98% |
| One Year      |     5,326 |     14.87% |
| Two Year      |     3,046 |     13.69% |

### Observation

Monthly-contract customers have a substantially higher observed churn rate than customers on one-year and two-year contracts.

The monthly contract segment should therefore receive further investigation in the churn-driver analysis.

The result represents an observed association and should not be interpreted as proof that contract duration directly causes or prevents churn.

---

## 3.4 Churn by Monthly Charge

Customers paying ₹800 or more have the highest observed churn rate at 31.38%.

The churn rate increases across the charge bands:

* Below ₹400: 18.58%
* ₹400–₹599.99: 19.77%
* ₹600–₹799.99: 22.02%
* ₹800+: 31.38%

### Observation

Higher monthly charges are associated with higher observed churn rates in this dataset.

This finding requires deeper analysis because monthly charge may be related to other characteristics such as plan type or contract type.

Therefore, the relationship should not be interpreted as causal at the KPI stage.

---

## 3.5 Churn by Age

Observed churn rates are relatively close across most age groups:

* 45–54: 23.03%
* 25–34: 22.48%
* 35–44: 22.07%
* Below 25: 21.98%
* 55+: 21.20%

The missing-age group has a 24.58% churn rate but contains only 240 customers.

### Observation

Age does not show a large difference in observed churn rates across the main age groups.

The missing-age group's higher rate should not be overinterpreted because of its smaller population size.

---

## 3.6 Churn by Gender

* Male: 22.59%
* Female: 21.99%
* Missing: 24.05%

### Observation

Male and female churn rates are very similar, with only a small difference between the two groups.

Gender does not appear to be a strong differentiating factor based on this KPI analysis alone.

The missing-gender group is too small for meaningful interpretation.

---

# 4. Retention KPI Observations

## 4.1 Overall Retention

The overall observed retention rate is 77.69%, corresponding to a churn rate of 22.32%.

### Observation

The retention KPI provides the baseline against which customer segments and future retention initiatives can be evaluated.

---

## 4.2 Average Tenure

The observed average tenure is 16.66 months.

Average tenure by churn status:

* Churned customers: 7.94 months
* Active customers: 19.16 months

### Observation

Churned customers have substantially lower observed tenure than active customers.

This indicates a strong relationship between customer lifecycle stage and churn status in the current dataset.

However, tenure and churn status are inherently related because churned customers have an observed end point while active customers continue to be observed. Therefore, this result should not be interpreted as evidence that increasing tenure independently causes lower churn.

---

## 4.3 Retention by Tenure Band

| Tenure Band  | Customers | Retention Rate |
| ------------ | --------: | -------------: |
| <3 months    |     1,642 |         28.44% |
| 3–5 months   |     2,170 |         54.70% |
| 6–11 months  |     3,665 |         68.24% |
| 12–23 months |     6,417 |         85.06% |
| 24+ months   |     6,106 |         97.02% |

### Observation

Retention increases substantially with observed tenure.

The most significant retention concern appears in the early customer lifecycle, particularly among customers with less than three months of observed tenure.

This finding suggests that early-life customer experience and onboarding should be investigated further.

The analysis is observational and may be affected by survivorship bias because customers who remain longer have already passed earlier churn-risk periods.

---

## 4.4 Retention by Signup Cohort

| Signup Year | Customers | Retention Rate | Churn Rate |
| ----------- | --------: | -------------: | ---------: |
| 2023        |     7,162 |         83.96% |     16.04% |
| 2024        |     7,075 |         77.22% |     22.78% |
| 2025        |     5,763 |         70.47% |     29.53% |

### Observation

Later signup cohorts have lower current active proportions and higher observed churn proportions.

However, these cohorts have different observation periods. The 2025 cohort is newer and therefore cannot be directly compared with the 2023 cohort as lifetime retention.

This metric should therefore be interpreted as current cohort status rather than final cohort lifetime retention.

---

# 5. Subscription KPI Observations

## 5.1 Subscription Profile

The subscription population contains:

* 20,000 subscriptions
* 20,000 unique customers
* 3 plans
* 3 contract types
* Average monthly charge: ₹583.66
* Minimum monthly charge: ₹299.00
* Maximum monthly charge: ₹1,040.58

### Observation

Each customer currently has one subscription record, providing a straightforward customer-to-subscription analytical structure.

---

## 5.2 Plan Distribution and Recurring Charge

| Plan     |  Share | Average Monthly Charge | Monthly Recurring Charge |
| -------- | -----: | ---------------------: | -----------------------: |
| Standard | 42.69% |                ₹599.11 |                   ₹5.12M |
| Basic    | 37.40% |                ₹398.84 |                   ₹2.98M |
| Premium  | 19.92% |                ₹897.58 |                   ₹3.58M |

### Observation

Standard is the largest customer segment, representing 42.69% of subscriptions.

Premium represents only 19.92% of subscriptions but generates approximately ₹3.58M in monthly recurring charge.

The combination of Premium's higher recurring value and its 31.33% churn rate makes this segment strategically important for further investigation.

---

## 5.3 Contract Distribution

Monthly contracts represent 58.14% of subscriptions, followed by One Year at 26.63% and Two Year at 15.23%.

### Observation

The customer base is predominantly composed of monthly-contract customers.

Because monthly contracts also have a significantly higher observed churn rate of 27.98%, contract type should be included as an important variable in subsequent churn-driver analysis.

---

## 5.4 Active MRR

Active subscriptions generate an estimated monthly recurring charge of:

**₹8,896,831.09**

The average active monthly charge is ₹572.57.

### Observation

The active customer base represents an estimated recurring monthly charge of approximately ₹8.90M.

This should be treated as **estimated MRR based on active subscription charges**, not recognized accounting revenue.

---

## 5.5 Recurring Charge at Risk

Churned subscriptions represent approximately:

**₹2,777,148.16**

in monthly recurring charge exposure.

### Observation

The churned customer base represents approximately ₹2.78M of modeled monthly recurring charge at risk.

This represents recurring-charge exposure associated with churned subscriptions and should not be described as historical revenue lost.

---

# 6. Payment KPI Observations

## 6.1 Overall Payment Performance

The payment dataset contains:

* 355,437 payments
* 355,437 unique Payment IDs
* 20,000 paying customers
* Total payment value: ₹205.96M
* Average payment: ₹579.45
* Successful payments: 334,112
* Failed payments: 21,325
* Success rate: 94.00%
* Failure rate: 6.00%

### Observation

Payment processing shows a high overall success rate of 94%.

All 20,000 customers have at least one payment record, indicating complete payment-customer coverage in the dataset.

---

## 6.2 Payment Method Performance

UPI is the most frequently used payment method with 127,962 transactions.

Success rates across payment methods are very similar:

* Credit Card: 94.07%
* Debit Card: 94.04%
* UPI: 93.99%
* Net Banking: 93.94%
* Wallet: 93.89%

### Observation

Payment success rates are highly consistent across payment methods, with only a small difference between the highest and lowest observed rates.

There is therefore no strong evidence at the KPI level that one payment method has materially worse payment processing performance.

---

## 6.3 Monthly Payment Trend

Payment volume generally increases from 2023 through 2025, reaching 16,627 payments in October 2025 before declining in November and December.

Average payment amount gradually decreases over the observation period, from approximately ₹582–₹584 during much of 2023–2024 to ₹572.99 in December 2025.

### Observation

The increase in payment volume should be interpreted alongside customer-base growth rather than as a standalone improvement in payment behavior.

The gradual decrease in average payment amount may warrant further investigation, particularly in relation to customer mix, subscription plans, and payment timing.

---

## 6.4 Customer-Level Payment Behavior

Customer-level payment aggregation provides:

* Total payment count
* Total payment value
* Average payment amount
* Successful payment count
* Failed payment count
* Payment failure rate

### Observation

Customer-level payment metrics provide an analytical foundation for identifying relationships between payment behavior and churn.

These metrics should be aggregated to customer grain before being joined with subscription or churn data to avoid one-to-many join duplication.

---

## 6.5 Payment Behavior by Churn Status

| Churn Status | Payments | Payment Value | Avg Payment | Failure Rate |
| ------------ | -------: | ------------: | ----------: | -----------: |
| Active       |  315,609 |      ₹181.02M |     ₹573.54 |        6.02% |
| Churned      |   39,828 |       ₹24.94M |     ₹626.25 |        5.86% |

### Observation

Churned customers have a higher average payment amount than active customers, while their payment failure rate is slightly lower.

The relatively similar failure rates indicate that payment failure frequency alone does not appear to provide a strong distinction between active and churned customers.

These results are descriptive associations and do not establish payment behavior as a cause of churn.

---

# 7. Support KPI Observations

## 7.1 Overall Support Performance

The support dataset contains:

* 50,000 tickets
* 50,000 unique Ticket IDs
* 18,349 customers with support tickets
* 44,421 resolved tickets
* 5,579 unresolved tickets
* Resolution rate: 88.84%
* Average resolution time: 7.98 hours
* Average satisfaction score: 4.41 / 5

### Observation

Overall support performance is relatively strong based on the available metrics, with an 88.84% resolution rate and an average satisfaction score of 4.41 out of 5.

---

## 7.2 Support Performance by Issue Type

Technical issues generate the highest ticket volume with 14,831 tickets.

Performance across issue types is relatively consistent:

* Resolution rates range from 88.62% to 89.78%
* Average resolution times range from 7.91 to 8.01 hours
* Satisfaction scores range from 4.40 to 4.42

### Observation

No major performance gap is visible across issue categories.

Performance issues have the highest observed resolution rate at 89.78%, while Account issues have the lowest at 88.62%.

The relatively narrow range suggests that issue type alone may not be a major differentiator of support performance.

---

## 7.3 Monthly Support Trend

Monthly ticket volumes remain relatively stable throughout the 36-month observation period.

Average resolution time remains close to eight hours, while average satisfaction remains close to 4.4 out of 5.

### Observation

Support performance appears relatively stable over time, with no clear sustained deterioration in resolution time or customer satisfaction.

---

## 7.4 Support Behavior by Churn Status

| Churn Status | Customers | Tickets | Avg Tickets/Customer | Resolution Rate | Satisfaction |
| ------------ | --------: | ------: | -------------------: | --------------: | -----------: |
| Active       |    15,537 |  38,975 |                 2.51 |          89.00% |         4.41 |
| Churned      |     4,463 |  11,025 |                 2.47 |          88.27% |         4.40 |

### Observation

Support-ticket frequency is very similar between active and churned customers.

Churned customers have a slightly lower resolution rate and satisfaction score, but the differences are small.

Based on these KPIs alone, support interaction volume does not appear to be a strong standalone differentiator between active and churned customers.

---

## 7.5 High-Frequency Support Customers

The customer-level support query identifies customers with three or more support tickets and summarizes their:

* Ticket count
* Average resolution time
* Average satisfaction
* Unresolved-ticket count

### Observation

This customer-level view is useful for identifying customers with repeated support interactions.

It provides a foundation for the next stage of analysis, where repeated support contact, unresolved issues, and satisfaction can be compared directly against churn status.

The KPI query itself does not establish that these factors cause churn.

---

# 8. Cross-KPI Business Observations

The KPI analysis highlights several areas that warrant deeper investigation.

### 8.1 Premium Segment Risk

Premium customers have a 31.33% observed churn rate, the highest among the three plans.

At the same time, Premium generates approximately ₹3.58M in monthly recurring charge.

This makes Premium churn an important business area because the segment combines relatively high customer value with elevated churn.

---

### 8.2 Monthly Contract Risk

Monthly-contract customers account for 58.14% of subscriptions and have a 27.98% observed churn rate.

This is substantially higher than the churn rates of one-year and two-year contracts.

Contract type should therefore be examined alongside other variables rather than analyzed in isolation.

---

### 8.3 Early-Lifecycle Retention Risk

Customers with less than three months of observed tenure have only a 28.44% retention rate.

Retention improves considerably as observed tenure increases, reaching 97.02% among customers with 24+ months of observed tenure.

This indicates that the early customer lifecycle is an important area for further investigation.

---

### 8.4 Payment Failure Is Not an Obvious Churn Differentiator

Overall payment failure is 6.00%.

The failure rate is 6.02% for active customers and 5.86% for churned customers.

The similarity suggests that payment failure alone does not appear to explain the difference between active and churned customers in this dataset.

---

### 8.5 Support Metrics Are Relatively Similar Across Churn Groups

Active and churned customers have similar:

* Ticket frequency
* Resolution time
* Satisfaction
* Resolution rates

Therefore, simple support volume or average support performance may not be sufficient to explain churn.

More granular analysis may be required, such as:

* Unresolved ticket burden
* Repeated tickets
* Specific issue types
* Recent support interactions before churn
* Customer-level support history

---

# 9. Key Areas for Churn Driver Analysis

Based on the KPI findings, the following areas should be prioritized in the next analysis stage:

1. **Plan type**, especially Premium
2. **Contract type**, especially Monthly
3. **Monthly charge**
4. **Customer tenure and early lifecycle**
5. **Customer payment behavior**
6. **Support interaction frequency**
7. **Unresolved support tickets**
8. **Support satisfaction**
9. **Customer services adoption**
10. **Interactions between multiple customer attributes**

The next stage should move beyond descriptive KPIs and quantify the relationship between these variables and churn.

---

# 10. Analytical Limitations

The KPI analysis is descriptive and does not establish causal relationships.

Several results require additional analysis before making business recommendations:

* Higher Premium churn does not prove the Premium plan causes churn.
* Higher churn among monthly-contract customers does not prove monthly contracts cause churn.
* Higher churn among high-charge customers does not prove price causes churn.
* Longer tenure is associated with higher retention, but survivorship bias may influence this relationship.
* Cohort retention rates are not directly comparable when cohorts have different observation periods.
* Payment and support data are one-to-many datasets and must be aggregated to customer grain before being joined with customer/subscription data.
* Estimated MRR and recurring charge at risk are analytical measures, not accounting revenue measures.

---

# 11. KPI Analysis Conclusion

The KPI analysis establishes a reliable business baseline for the Customer Churn & Retention Analysis project.

The overall customer base contains 20,000 customers with an observed churn rate of 22.32% and an observed active/retained rate of 77.69%.

The strongest areas requiring further investigation are:

* Premium plan churn
* Monthly contract churn
* High monthly-charge segments
* Early customer lifecycle retention
* Customer-level payment behavior
* Repeated and unresolved support interactions
* Customer service adoption

These findings will be used as the starting point for the **Churn Driver Analysis** stage, where customer-level attributes and behavioral metrics will be compared more systematically against churn status.

**KPI Analysis Status: COMPLETED**
