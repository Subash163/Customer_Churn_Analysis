# Business Questions — SQL Observations

## 1. Objective

The Business Questions module translates the Customer Churn & Retention Analysis into practical management-level questions.

The objective is to identify:

* Which customer segments contribute most to churn.
* Which subscription combinations create the greatest financial exposure.
* Which active customers should receive retention attention.
* How observed payment and support signals relate to churned customers.
* Which geographic markets contribute the most churn.
* What the overall customer and recurring-charge impact of churn looks like.

This module is intended to convert analytical findings into **actionable business insights for management and retention teams**.

---

# 2. Overall Churn Position

The customer base contains **20,000 customers**, of which:

* **15,537 are active**
* **4,463 are churned**
* Overall churn rate = **22.32%**
* Overall retention rate = **77.69%**

The total monthly subscription charge base is approximately **₹1.17 crore**, while the monthly charge associated with churned subscriptions is approximately **₹27.77 lakh**.

This indicates that churn represents a meaningful recurring-value exposure and should be treated as both a **customer-retention issue and a financial-priority issue**.

> Note: Monthly revenue at risk represents the recurring monthly subscription-charge exposure associated with churned subscriptions. It should not be interpreted as historical recognized accounting revenue.

---

# 3. Plan-Level Management Findings

Premium customers show the highest churn rate:

* Premium: **31.33%**
* Standard: **21.63%**
* Basic: **18.29%**

Premium also produces the highest monthly revenue at risk at approximately **₹11.22 lakh**, slightly above Standard at approximately **₹11.09 lakh**.

This makes Premium the most important plan from a **retention-risk perspective**, because it combines:

1. Higher customer value.
2. Higher churn rate.
3. Significant recurring revenue exposure.

Standard generates the largest number of churned customers because it has the largest customer population, but Premium represents the stronger high-value retention concern.

### Management implication

Retention initiatives should not focus only on the plan with the largest number of churned customers. Management should also consider **customer value and revenue exposure** when prioritizing retention efforts.

---

# 4. Plan × Contract Findings

The combination of subscription plan and contract type provides a more detailed view of churn exposure.

The most important combinations are:

* **Premium Monthly** — 38.30% churn rate.
* **Standard Monthly** — 27.36% churn rate.
* **Basic Monthly** — 23.28% churn rate.

Premium Monthly has the **highest churn rate**, while Standard Monthly has the **largest monthly revenue at risk**, approximately ₹8.15 lakh.

Longer contracts generally show substantially better retention than Monthly contracts.

The strongest combinations include:

* Basic Two Year — 10.27% churn.
* Standard Two Year — 12.53% churn.
* Basic One Year — 11.84% churn.
* Standard One Year — 14.38% churn.

### Management implication

Monthly contracts represent the primary contractual retention opportunity.

A practical management strategy would be to investigate whether appropriate Monthly customers can be encouraged to move toward longer-term contracts through:

* Renewal incentives.
* Contract upgrade offers.
* Loyalty benefits.
* Targeted retention campaigns.

However, the analysis identifies an association and does not prove that changing contract type will itself cause lower churn.

---

# 5. Active High-Value Customer Prioritization

A rule-based retention-priority framework was created for active customers.

The framework considers:

1. Failed payment activity.
2. Unresolved support tickets or lower satisfaction.
3. Low service adoption.
4. Top 25% monthly subscription charge.
5. Multiple risk factors occurring together.

The query identifies **100 active high-value customers** meeting at least two of these rule-based risk conditions.

Customers with three observed risk factors receive the highest priority within this framework.

### Management implication

Rather than treating every active customer equally, the retention team can use this framework to create a **targeted retention queue**.

The highest-value customers showing multiple warning signals can receive proactive attention before churn occurs.

### Important limitation

This is a **rule-based prioritization framework**, not a statistically validated or machine-learning churn prediction model.

Therefore, these customers should be described as:

> **Active high-value customers meeting multiple rule-based retention-risk criteria.**

They should not be described as confirmed or predicted future churners.

---

# 6. Observed Risk Signals Among Churned Customers

Among the 4,463 churned customers, **2,430 customers** had at least one observed risk signal involving:

* Failed payments.
* Unresolved support tickets.
* Average support satisfaction below 4.

The monthly subscription-charge exposure associated with these customers is approximately **₹15.10 lakh**.

This suggests that a substantial portion of churned customers had observable customer-experience or payment-related signals before or during their customer lifecycle.

### Management implication

Payment and support data can potentially be incorporated into a broader **early-warning monitoring framework**.

However, these variables should be treated as **observed associations**, not proven causes of churn.

The analysis cannot establish that payment failures or support problems directly caused these customers to churn.

---

# 7. Geographic Churn Findings

Tamil Nadu and Maharashtra have the largest absolute numbers of churned customers:

* Tamil Nadu — **719 churned customers**
* Maharashtra — **718 churned customers**

This is largely influenced by their relatively large customer populations.

When looking at churn rate instead, Telangana has the highest churn rate among the displayed states:

* Telangana — **23.51%**
* Kerala — **23.09%**
* Gujarat — **22.79%**
* Rajasthan — **22.79%**

The differences between states are relatively modest compared with the much stronger differences observed across lifecycle, plan, and contract segments.

### Management implication

Geographic analysis is useful for identifying markets that may deserve additional investigation, but geography does not appear to be the strongest churn discriminator in this dataset.

Management should therefore avoid allocating major retention resources solely based on state-level churn differences without considering customer segment, lifecycle, plan, and contract characteristics.

---

# 8. Overall Financial Impact

The final management-level KPI summary shows:

| Metric                             |           Value |
| ---------------------------------- | --------------: |
| Total customers                    |          20,000 |
| Active customers                   |          15,537 |
| Churned customers                  |           4,463 |
| Churn rate                         |          22.32% |
| Retention rate                     |          77.69% |
| Total monthly charge base          | ₹1,16,73,179.25 |
| Retained monthly charge            |   ₹88,96,031.09 |
| Monthly charge exposure from churn |   ₹27,77,148.16 |

Approximately **23.79% of the total monthly subscription-charge base** is associated with churned subscriptions.

This provides management with a clear financial perspective on the scale of the churn problem.

---

# 9. Management Priorities

Based on the Business Questions analysis, the following priorities emerge.

## Priority 1 — Protect High-Value Customers

Premium customers have the highest churn rate and highest monthly revenue exposure.

Focus particularly on:

* Active Premium customers.
* High monthly-charge customers.
* Premium Monthly customers.
* Customers showing multiple risk signals.

---

## Priority 2 — Address Monthly Contract Risk

Monthly contracts have substantially lower retention than One Year and Two Year contracts.

Management should investigate targeted strategies to improve Monthly-contract retention and encourage suitable customers toward longer-term relationships.

---

## Priority 3 — Prioritize Revenue Exposure, Not Only Churn Volume

Standard produces the largest number of churned customers, while Premium produces the highest churn rate and slightly higher revenue at risk.

Therefore, management should track both:

**Customer churn volume + financial exposure.**

---

## Priority 4 — Develop an Early-Warning Framework

Payment and support behavior can provide additional signals for identifying customers requiring attention.

A future version of the project could combine:

* Lifecycle.
* Plan.
* Contract.
* Payment engagement.
* Support experience.
* Customer value.

into a validated churn-risk scoring model.

---

## Priority 5 — Use Geographic Analysis as a Secondary Lens

States with higher churn rates can be investigated further, but geographic differences should not automatically be treated as the primary cause of churn.

---

# 10. Strongest Management Signals

The Business Questions analysis reinforces the findings from the earlier Churn Driver and Retention modules.

### Stronger signals

* **Customer lifecycle / tenure**
* **Contract type**
* **Subscription plan**
* **Customer value / monthly charge**
* **Plan × contract combinations**

### Secondary signals

* Low payment success.
* Lower support satisfaction.
* Multiple observable customer-risk indicators.

### Weaker signals

* Individual service adoption.
* Service count.
* Support issue type.
* Overall support ticket volume.
* Geographic differences.

The strength of these signals should be interpreted descriptively rather than as proof of causation.

---

# 11. Business Recommendations

### Recommendation 1 — Build a Premium Retention Program

Create targeted retention campaigns for Premium customers, particularly Premium Monthly customers.

Potential actions include:

* Proactive renewal outreach.
* Personalized offers.
* Contract migration incentives.
* Dedicated support for high-value customers.

---

### Recommendation 2 — Target Monthly Customers

Monthly customers represent the largest contract group and have substantially lower retention.

Analyze whether customers showing risk signals can be encouraged toward longer-term contracts.

---

### Recommendation 3 — Create a High-Value Retention Queue

Use the rule-based priority framework to provide the retention team with a focused list of high-value active customers showing multiple risk indicators.

The list should be treated as a **prioritization tool**, not a predictive model.

---

### Recommendation 4 — Monitor Payment and Support Warning Signals

Create regular monitoring for:

* Payment failures.
* Very low payment success rates.
* Unresolved tickets.
* Low satisfaction scores.

These indicators can be combined with lifecycle and customer-value information to identify customers requiring proactive attention.

---

### Recommendation 5 — Measure Retention Financially

Retention performance should be tracked using both:

* Number of customers retained.
* Monthly recurring charge/revenue exposure protected.

This ensures that retention decisions are aligned with business value rather than customer count alone.

---

# 12. Analytical Limitations

The following limitations should be clearly communicated when presenting this analysis:

1. **Association does not establish causation.**
   The SQL analysis identifies patterns associated with churn but does not prove that individual factors caused churn.

2. **Payment activity is affected by customer exposure.**
   Customers with longer tenure naturally have more opportunities to make payments and experience payment failures. Therefore, raw payment counts can create misleading relationships with churn.

3. **Support activity is also exposure-dependent.**
   Ticket counts should be interpreted together with tenure and customer lifecycle.

4. **2025 signup cohorts are incomplete.**
   Current-status retention for recent signup cohorts should not be interpreted as directly comparable lifetime retention.

5. **Rule-based risk scoring is not predictive modeling.**
   The high-value retention-priority framework has not been statistically validated.

6. **Monthly revenue at risk is modeled recurring-charge exposure.**
   It should not be interpreted as accounting revenue already lost.

7. **Small segments require caution.**
   Some combinations contain relatively few customers and should not be over-interpreted.

---

# 13. Final Management Conclusion

The Business Questions analysis shows that customer churn is not simply a volume problem; it is also a **customer-value and recurring-revenue exposure problem**.

The most important management opportunity is concentrated around **high-value customers, Premium subscriptions, and Monthly contracts**. Premium Monthly customers in particular combine a high churn rate with significant financial exposure.

At the same time, payment and support signals provide additional observable indicators that can support proactive retention efforts, although they should not be interpreted as proven causes of churn.

The recommended management approach is therefore to move from broad retention campaigns toward **segmented, value-based and risk-informed retention**:

> **Identify high-value customers → evaluate lifecycle and contract → monitor payment/support signals → prioritize customers with multiple risk indicators → measure both customers retained and recurring value protected.**

This creates a practical bridge between SQL analysis and real-world management decision-making.

---

## Module Status

**`06_management_questions.sql` — COMPLETE**

All 6 management-level SQL questions have been validated.

**Business Questions SQL Section — COMPLETE**

```text
01_customer_questions.sql       ✅ COMPLETE
02_churn_questions.sql          ✅ COMPLETE
03_payment_questions.sql        ✅ COMPLETE
04_support_questions.sql        ✅ COMPLETE
05_retention_questions.sql      ✅ COMPLETE
06_management_questions.sql     ✅ COMPLETE
```

The Business Questions module now provides the executive/business interpretation layer of the SQL project and connects the earlier KPI, churn-driver, and retention analyses to practical management decisions.
