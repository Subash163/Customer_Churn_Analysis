# Section 25 — Final Business Insights

## 25.1 Overall Customer Churn

### Finding
The overall customer churn rate is **22.3%**, representing approximately **4,000+ churned customers out of 20,000 customers**.

### Evidence
- Total Customers: **20,000**
- Churn Rate: **22.3%**
- Churned Customers: approximately **4,000+**
- Active Customers: approximately **16,000**

### Interpretation
A churn rate of 22.3% indicates that customer retention is a significant business area that requires attention. The analysis therefore focuses on identifying customer segments with relatively higher churn and determining which factors can be used for targeted retention actions.

### Business Significance
The company should not rely only on the overall churn rate. Segment-level analysis is required to identify where the highest retention risk is concentrated.

---

## 25.2 Contract Type Is a Strong Churn Segmentation Factor

### Finding
Customers on **Monthly contracts have the highest churn rate at 28.0%**, compared with **14.9% for One Year** and **13.7% for Two Year contracts**.

### Evidence

| Contract Type | Churn Rate |
|---|---:|
| Monthly | **28.0%** |
| One Year | **14.9%** |
| Two Year | **13.7%** |

### Interpretation
Monthly customers show substantially higher churn than customers on longer-term contracts. The monthly segment has nearly twice the churn rate of the Two Year segment.

### Business Significance
Contract type is an important segmentation variable for retention planning. However, this analysis identifies an **association rather than causation**. The higher churn may also be related to differences in customer tenure, pricing, customer profile, or other factors.

### Potential Business Action
Develop targeted strategies to encourage suitable Monthly customers to move toward longer-term contracts through:
- Annual-plan upgrade incentives
- Loyalty benefits
- Contract renewal offers
- Value-based discounts
- Personalized retention campaigns

---

## 25.3 Premium Plan Has the Highest Churn Rate

### Finding
The **Premium plan has the highest churn rate at 31.3%**.

### Evidence

| Plan | Churn Rate |
|---|---:|
| Premium | **31.3%** |
| Standard | **21.6%** |
| Basic | **18.3%** |

### Interpretation
Premium customers are the highest-risk customer segment based on churn rate. The Premium churn rate is approximately:
- **9.7 percentage points higher than Standard**
- **13.0 percentage points higher than Basic**

### Business Significance
The Premium segment requires investigation because it represents customers with the highest observed relative churn risk.

Possible areas for investigation include:
- Whether Premium customers receive sufficient value for the price
- Pricing sensitivity
- Product/service expectations
- Feature usage and engagement
- Customer support experience
- Competitor alternatives

These are investigation areas, not confirmed causes from the current dataset.

---

## 25.4 Churn Rate and Churn Volume Tell Different Stories

### Finding
Premium customers have the **highest churn rate**, but Standard customers have the **largest absolute number of churned customers**.

### Evidence

| Plan | Churn Rate | Churned Customers |
|---|---:|---:|
| Premium | **31.3%** | **1,248** |
| Standard | **21.6%** | **1,847** |
| Basic | **18.3%** | **1,368** |

### Interpretation
The analysis demonstrates why both **relative churn rate** and **absolute churn volume** should be considered.

- Premium represents the highest-risk segment proportionally.
- Standard represents the largest churn population in absolute numbers.

### Business Significance
Retention teams should use two different priorities:
1. **Risk priority:** Premium customers because of their high churn rate.
2. **Volume priority:** Standard customers because they contribute the largest number of churned customers.

This provides a more balanced retention strategy than focusing only on the highest churn percentage.

---

## 25.5 Support Ticket Volume Does Not Show a Simple Linear Churn Pattern

### Finding
Churn rate does not increase consistently as the number of support tickets increases.

### Evidence

| Support Ticket Group | Churn Rate |
|---|---:|
| 0 Tickets | **23.1%** |
| 1–2 Tickets | **22.2%** |
| 3–5 Tickets | **22.5%** |
| 6+ Tickets | **19.6%** |

### Interpretation
Customers with 6+ tickets actually show a lower churn rate than the other groups. Therefore, support ticket count alone does not provide a simple linear explanation for churn in this dataset.

### Business Significance
The number of support tickets should not be treated as a standalone churn predictor.

Further analysis should consider:
- Issue type
- Ticket severity
- Resolution quality
- Repeat issues
- Customer tenure
- Customer engagement
- Satisfaction at the individual ticket level

---

## 25.6 Resolution Time Shows Very Little Difference Between Active and Churned Customers

### Finding
Average resolution time is almost identical between Active and Churned customers.

### Evidence

| Customer Status | Avg. Resolution Time |
|---|---:|
| Active | **7.98 hours** |
| Churned | **7.95 hours** |

The difference is approximately **0.03 hours**, or about **2 minutes**.

### Interpretation
The current dataset does not show a meaningful difference in average ticket resolution time between Active and Churned customers.

### Business Significance
Average resolution time alone does not appear to be a strong differentiating metric between the two customer groups.

Further investigation could examine:
- Resolution time by issue type
- Percentage of unresolved tickets
- Repeat tickets
- First-contact resolution
- Resolution time for high-value customers

---

## 25.7 Satisfaction Score Shows Very Little Difference

### Finding
Average satisfaction scores are approximately **4.4 for both Active and Churned customers**.

### Evidence

| Customer Status | Avg. Satisfaction |
|---|---:|
| Active | **4.4** |
| Churned | **4.4** |

### Interpretation
There is no meaningful difference in average satisfaction score between Active and Churned customers at the aggregate level.

### Business Significance
Overall average satisfaction is not sufficient to distinguish churn risk in the current dataset.

A more detailed analysis could investigate:
- Satisfaction distribution rather than only the average
- Low-score customers
- Satisfaction by issue type
- Satisfaction by plan
- Satisfaction by contract type
- Satisfaction immediately before churn

---

## 25.8 Payment Failures Do Not Show a Simple Positive Relationship With Churn

### Finding
The dataset contains approximately **355K payment transactions**, with approximately **21K failed transactions**, resulting in a **94.0% payment success rate**.

The current customer-level comparison shows:
- Active customers with failed payments: approximately **66.0%**
- Churned customers with failed payments: approximately **37.2%**

### Interpretation
The current analysis does **not** support the conclusion that customers with failed payments are more likely to churn.

In fact, the observed failed-payment customer rate is higher among Active customers than Churned customers.

### Business Significance
Failed payments should therefore **not be presented as a confirmed churn driver** based on this analysis.

The metric should be interpreted cautiously because customers may differ in:
- Tenure
- Number of payment opportunities
- Subscription duration
- Payment frequency
- Number of transactions

### Recommended Further Analysis
A stronger payment-risk analysis would use:
- Failed payments per customer
- Failed payment rate per customer
- Failed payment frequency over time
- Failed payment events before churn
- Payment failure rate adjusted for number of transactions

---

# Section 26 — Business Recommendations

## 26.1 Priority 1 — Target Monthly Contract Customers

### Recommendation
Create a targeted retention and contract-conversion strategy for Monthly customers.

### Why
Monthly customers have a **28.0% churn rate**, substantially higher than One Year and Two Year customers.

### Suggested Actions
- Offer annual-plan upgrade incentives
- Provide loyalty benefits for longer commitments
- Create targeted renewal campaigns
- Identify Monthly customers approaching renewal
- Use customer value and tenure to personalize offers

### Expected Business Benefit
Reducing churn within the Monthly segment could have a meaningful impact on overall customer retention.

> **Important:** The analysis establishes an association between contract type and churn, not that changing contract type will automatically reduce churn.

---

## 26.2 Priority 2 — Investigate Premium Customer Churn

### Recommendation
Conduct a deeper investigation into the Premium customer segment.

### Why
Premium customers have the highest churn rate at **31.3%**.

### Suggested Actions
- Analyze Premium customer usage and engagement
- Review pricing versus perceived value
- Compare Premium support experiences
- Identify common characteristics among churned Premium customers
- Examine tenure and contract type within Premium
- Conduct customer-level churn-risk segmentation

### Expected Business Benefit
Understanding why high-value Premium customers leave could help protect revenue and improve customer lifetime value.

---

## 26.3 Priority 3 — Address Standard Customer Churn at Scale

### Recommendation
Create a separate retention initiative for Standard customers.

### Why
Although Standard has a lower churn rate than Premium, it has the **largest absolute number of churned customers: 1,847**.

### Suggested Actions
- Prioritize Standard customers in churn-volume analysis
- Identify high-value Standard customers
- Segment by tenure and contract type
- Develop targeted retention campaigns
- Monitor churn volume monthly

### Expected Business Benefit
Even a moderate reduction in Standard churn could result in a substantial number of retained customers because of the segment's large churn volume.

---

## 26.4 Priority 4 — Do Not Use Support Ticket Count as a Standalone Churn Rule

### Recommendation
Avoid using rules such as "customers with more support tickets are automatically high-risk."

### Why
The current ticket-group analysis does not show a consistent increasing churn pattern.

### Suggested Actions
Build richer support-related features:
- Number of tickets
- Ticket frequency
- Issue type
- Unresolved tickets
- Average resolution time
- Satisfaction score
- Recent ticket activity

These variables should be evaluated together rather than independently.

---

## 26.5 Priority 5 — Use Multi-Factor Churn Risk Analysis

### Recommendation
The next analytical improvement should be a **customer-level churn risk model or scoring framework**.

### Recommended Variables
Combine:
- Contract type
- Plan
- Customer tenure
- Monthly charge
- Payment behavior
- Failed payment frequency
- Support ticket activity
- Issue type
- Resolution time
- Satisfaction score
- Customer engagement

### Why
The current analysis shows that no single operational metric completely explains churn.

A multi-factor approach can identify combinations of characteristics associated with higher churn risk.

---

## 26.6 Priority 6 — Improve Payment Failure Analysis Before Taking Action

### Recommendation
Do not launch a payment-failure-based churn campaign based only on the current aggregate comparison.

### Suggested Next Steps
Calculate customer-level metrics such as:

**Failed Payment Rate**
```text
Failed Payments / Total Payment Attempts
```

**Failed Payment Frequency**
```text
Number of Failed Payments per Customer
```

**Recent Failed Payment Indicator**
```text
Whether a customer experienced a failed payment within a defined period before churn
```

Then compare these metrics between Active and Churned customers while controlling for transaction exposure and tenure.

---

## 26.7 Recommended Retention Priority Framework

| Priority | Segment / Area | Reason |
|---|---|---|
| 1 | Monthly contracts | Highest contract-level churn: 28.0% |
| 2 | Premium customers | Highest plan churn: 31.3% |
| 3 | Standard customers | Largest absolute churn volume: 1,847 |
| 4 | Multi-factor risk segments | Single variables do not fully explain churn |
| 5 | Support & payment analysis | Requires deeper customer-level analysis |

---

# Section 27 — Final Power BI Conclusion

## 27.1 Project Objective

The Power BI dashboard was developed to analyze customer churn, identify high-risk customer segments, understand potential retention signals, and convert analytical findings into actionable business recommendations.

The dashboard integrates customer, subscription, payment, support-ticket, and date information into an interactive analytical model.

---

## 27.2 Key Findings

The completed analysis identifies the following major findings:

1. **Overall churn is 22.3%**, indicating a significant customer-retention challenge.
2. **Monthly customers have the highest contract-level churn at 28.0%**, compared with 14.9% for One Year and 13.7% for Two Year contracts.
3. **Premium customers have the highest plan-level churn at 31.3%**.
4. **Standard customers have the highest absolute churn volume**, with approximately **1,847 churned customers**.
5. **Support ticket count does not show a simple linear relationship with churn**.
6. **Average resolution time is almost identical** between Active and Churned customers.
7. **Average satisfaction is approximately identical** between Active and Churned customers.
8. **Payment failures do not show a simple positive relationship with churn** in the current aggregate analysis.

---

## 27.3 Business Priorities

Based on the analysis, management should prioritize:

### Short-Term
- Focus retention campaigns on Monthly customers.
- Investigate the reasons behind Premium customer churn.
- Address Standard customer churn at scale.

### Medium-Term
- Build richer customer-level behavioral features.
- Analyze customer tenure and engagement.
- Improve payment-failure and support-event analysis.

### Long-Term
- Develop a multi-factor churn-risk model.
- Create proactive customer-retention alerts.
- Measure retention campaign effectiveness.
- Track churn and customer lifetime value over time.

---

## 27.4 Analytical Limitations

The findings should be interpreted within the limitations of the current analysis.

### Limitation 1 — Association vs Causation
The dashboard identifies relationships and differences between customer segments. It does not prove that a particular factor directly causes churn.

### Limitation 2 — Aggregate Metrics
Average satisfaction and average resolution time can hide important customer-level patterns.

### Limitation 3 — Payment Exposure
Customers with different numbers of payment transactions may have different opportunities to experience payment failures. Customer-level payment rates would provide a stronger comparison.

### Limitation 4 — Tenure
Contract type and plan comparisons should ideally be controlled for customer tenure because newer and older customers may have different churn behavior.

### Limitation 5 — Predictive Modeling
The current Power BI dashboard is primarily descriptive and diagnostic. It does not yet provide a machine-learning-based churn prediction score.

---

## 27.5 Final Portfolio Statement

This project demonstrates an end-to-end **Customer Churn & Retention Analytics** workflow:

```text
Raw Data
   ↓
Python Data Cleaning & Validation
   ↓
Excel / CSV Data Preparation
   ↓
MySQL Database & SQL Analysis
   ↓
Business Questions & Interview Queries
   ↓
Power BI Data Modeling
   ↓
DAX Measures
   ↓
Interactive Dashboards
   ↓
Dashboard Validation
   ↓
Business Insights
   ↓
Retention Recommendations
```

The project demonstrates practical skills across:

- Data cleaning
- Data validation
- Data modeling
- SQL
- Power Query
- DAX
- Power BI dashboard development
- KPI design
- Business analysis
- Data storytelling
- Business recommendations
- Analytical validation

### Final Takeaway

The most important business lesson from the analysis is that **churn should not be managed using a single metric**.

Contract type and plan reveal clear segment-level differences, while support and payment metrics demonstrate that some commonly assumed churn indicators do not show a straightforward relationship in this dataset. Therefore, the strongest next step is to combine customer profile, subscription, payment, support, tenure, and engagement variables into a **multi-factor churn-risk framework**.

This approach moves the project from simply reporting **"who churned"** toward answering the more valuable business question:

> **"Which customers are most at risk of churning, and what retention action should the business take?"**

---

## Documentation Status

**Sections 25–27:** Completed  
**Business Insights:** Completed  
**Business Recommendations:** Completed  
**Final Power BI Conclusion:** Completed  
**Dashboard Validation:** Completed  

These sections are intended to serve as the formal business-analysis conclusion of the Power BI stage and can later be reused to create the project's GitHub README, resume project description, and interview talking points.
