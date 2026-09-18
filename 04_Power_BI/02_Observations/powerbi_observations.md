# Power BI — Customer Churn & Retention Analysis
## Observation & Documentation
### Coverage: Completed through Dashboard Design

---

## 1. Power BI Data Import

The cleaned CSV datasets from the Python stage were imported into Power BI.

| Table | Grain | Approx. Rows | Key Identifier |
|---|---|---:|---|
| customers | One row per customer | 20,000 | customer_id |
| subscriptions | One subscription per customer | 20,000 | subscription_id |
| payments | One row per payment transaction | 355K+ | payment_id |
| customer_services | One row per customer | 20,000 | customer_id |
| support_tickets | One row per support ticket | 50K+ | ticket_id |
| data_dictionary | Documentation/reference | 32 | Description |

The model contains both customer-level tables and transaction/event-level tables, so their different grains must be respected when creating relationships and measures.

---

## 2. Data Model Observations

`customers` is the central customer-level entity.

Main relationships:

- customers ↔ subscriptions
- customers ↔ customer_services
- customers ← payments
- customers ← support_tickets
- Date → payments
- Date → support_tickets
- Churn Date → subscriptions

`data_dictionary` remains disconnected because it is documentation-only.

The 1:1 relationships between customers and subscriptions/customer_services use Both filter direction because that was the usable configuration available in Power BI.

---

## 3. Relationship Modeling

| Relationship | Cardinality | Filter Direction | Status |
|---|---|---|---|
| customers ↔ subscriptions | 1:1 | Both | Active |
| customers ↔ customer_services | 1:1 | Both | Active |
| customers ← payments | 1:* | Single | Active |
| customers ← support_tickets | 1:* | Single | Active |
| Date → payments | 1:* | Single | Active |
| Date → support_tickets | 1:* | Single | Active |
| Churn Date → subscriptions | 1:* | Single | Active |

A direct Date → subscriptions[start_date] relationship was not added because it created filter-path ambiguity through the existing bidirectional 1:1 relationships.

**Modeling principle:** relationships should not be added merely because they are technically possible if they introduce ambiguity.

---

## 4. Date Modeling

A dedicated `Date` table was created using the minimum and maximum dates across signup, subscription, churn, and payment dates.

Supporting columns:

```DAX
Year = YEAR('Date'[Date])
Month Number = MONTH('Date'[Date])
Month Name = FORMAT('Date'[Date], "MMMM")
Year Month = FORMAT('Date'[Date], "YYYY-MM")
Quarter = "Q" & FORMAT('Date'[Date], "Q")
```

`Month Name` was sorted by `Month Number`, and the table was marked as a date table.

Active relationships:

- Date[Date] → payments[payment_date]
- Date[Date] → support_tickets[ticket_date]

This provides a consistent calendar for time-based analysis.

---

## 5. Signup Date Analysis

A separate `Signup Date` table was created:

```DAX
Signup Date =
CALENDAR(
    MIN(customers[signup_date]),
    MAX(customers[signup_date])
)
```

Year, Month Number, Month Name, Year Month, and Quarter were added, and the table was marked as a date table.

Current New Customers measure:

```DAX
New Customers =
VAR MinDate =
    MIN('Date'[Date])
VAR MaxDate =
    MAX('Date'[Date])
RETURN
CALCULATE(
    DISTINCTCOUNT(customers[customer_id]),
    customers[signup_date] >= MinDate,
    customers[signup_date] <= MaxDate
)
```

A `USERELATIONSHIP()` approach was not used because a corresponding inactive Date → customers[signup_date] relationship was not established.

The New Customers KPI requires additional validation because the complete date range can return the full customer population.

---

## 6. Churn Date Analysis

A dedicated `Churn Date` table was created:

```DAX
Churn Date =
CALENDAR(
    MIN(subscriptions[churn_date]),
    MAX(subscriptions[churn_date])
)
```

Supporting date columns were added and the table was marked as a date table.

Relationship:

`Churn Date[Date]` → `subscriptions[churn_date]`

The `subscriptions[churn_date]` field was changed from Date/Time to **Date** in Power Query using an additional transformation step. This fixed the blank monthly churn chart.

---

## 7. Customer KPI Measures

### Total Customers

```DAX
Total Customers =
DISTINCTCOUNT(customers[customer_id])
```

### Churned Customers

```DAX
Churned Customers =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[churn_status] = "Churned"
)
```

### Active Customers

```DAX
Active Customers =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[churn_status] = "Active"
)
```

### Churn Rate

```DAX
Churn Rate =
DIVIDE(
    [Churned Customers],
    [Total Customers],
    0
)
```

These measures form the core customer-health KPIs.

---

## 8. Subscription KPI Measures

```DAX
Total Subscriptions =
DISTINCTCOUNT(subscriptions[subscription_id])
```

```DAX
Average Monthly Charge =
AVERAGE(subscriptions[monthly_charge])
```

```DAX
Monthly Contract Customers =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[contract_type] = "Monthly"
)
```

```DAX
Annual Contract Customers =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[contract_type] = "Annual"
)
```

```DAX
Two Years Contract Customers =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[contract_type] = "Two Years Contract"
)
```

These measures support plan and contract-based churn analysis.

---

## 9. Payment KPI Measures

```DAX
Total Payments =
COUNTROWS(payments)
```

```DAX
Total Payment Amount =
SUM(payments[payment_amount])
```

```DAX
Successful Payments =
CALCULATE(
    COUNTROWS(payments),
    payments[payment_status] = "Success"
)
```

```DAX
Failed Payments =
CALCULATE(
    COUNTROWS(payments),
    payments[payment_status] = "Failed"
)
```

```DAX
Payment Success Rate =
DIVIDE(
    [Successful Payments],
    [Total Payments],
    0
)
```

These measures evaluate transaction volume, payment value, payment failures, and payment reliability.

---

## 10. Support KPI Measures

```DAX
Total Tickets =
COUNTROWS(support_tickets)
```

```DAX
Resolved Tickets =
CALCULATE(
    COUNTROWS(support_tickets),
    support_tickets[resolved] = "Yes"
)
```

```DAX
Average Resolution Time =
AVERAGE(support_tickets[resolution_time_hours])
```

```DAX
Average Satisfaction Score =
AVERAGE(support_tickets[satisfaction_score])
```

These measures enable customer-service experience analysis by churn status.

---

## 11. Failed Payment & Churn Analysis

### Customers with Failed Payments

```DAX
Customers with Failed Payments =
CALCULATE(
    DISTINCTCOUNT(payments[customer_id]),
    payments[payment_status] = "Failed"
)
```

### Failed Payment Customer Rate

```DAX
Failed Payment Customer Rate =
DIVIDE(
    [Customers with Failed Payments],
    [Total Customers],
    0
)
```

### Failed Payment Transactions

```DAX
Failed Payment Transactions =
CALCULATE(
    COUNTROWS(payments),
    payments[payment_status] = "Failed"
)
```

Failed-payment analysis is intended to identify an association between payment issues and churn. It should not be presented as proof of causation.

---

## 12. Customer Support Experience Segmentation

### Ticket Count

```DAX
Ticket Count =
CALCULATE(
    COUNTROWS(support_tickets),
    FILTER(
        support_tickets,
        support_tickets[customer_id] = customers[customer_id]
    )
)
```

### Ticket Group

```DAX
Ticket Group =
SWITCH(
    TRUE(),
    customers[Ticket Count] = 0, "0 Tickets",
    customers[Ticket Count] <= 2, "1-2 Tickets",
    customers[Ticket Count] <= 5, "3-5 Tickets",
    "6+ Tickets"
)
```

Groups:

1. 0 Tickets
2. 1-2 Tickets
3. 3-5 Tickets
4. 6+ Tickets

A separate calculated sort column caused a circular dependency and was not used.

Recommended visual sorting:

**... → Sort axis → Ticket Group → Ascending**

This gives the logical business order above.

---

## 13. Churn by Churn Date

Measure:

```DAX
Churned Customers by Churn Date =
CALCULATE(
    DISTINCTCOUNT(subscriptions[customer_id]),
    subscriptions[churn_status] = "Churned"
)
```

Visual:

- Axis: `Churn Date[Year Month]`
- Value: `[Churned Customers by Churn Date]`

The active Churn Date relationship means `USERELATIONSHIP()` is not required.

---

## 14. Churn Rate by Churn Date

The initial measure produced a flat rate because the Churn Date filter also reduced the denominator through the bidirectional 1:1 model path.

Corrected measure:

```DAX
Churn Rate by Churn Date =
DIVIDE(
    [Churned Customers by Churn Date],
    CALCULATE(
        [Total Customers],
        REMOVEFILTERS('Churn Date')
    ),
    0
)
```

This prevents the denominator from shrinking with the churn-date filter.

### Important Definition

The current metric represents:

**Customers churned in the period ÷ overall customer base**

This is not necessarily the textbook beginning-of-period churn rate. The final project documentation should explicitly state the definition.

---

## 15. New Customer Analysis

Visual configuration:

- Axis: `Date[Year Month]`
- Value: `[New Customers]`

The full date range can cause New Customers to equal the total customer population. Therefore, this metric must be validated before using it as a strong business conclusion.

---

## 16. Power BI Data Validation — Initial Stage

The initial Power BI validation was completed before dashboard design.

Validation included checks for:

1. Customer counts
2. Active and churned customer counts
3. Churn rate
4. Payment totals
5. Support/ticket-related measures

The Power BI measures were checked against the cleaned data and expected business logic.

**Dashboard-level validation is still pending.**

---

# 17. Dashboard Design Overview

The dashboard was designed as three analytical pages:

1. **Executive Overview**
2. **Churn & Retention**
3. **Customer & Service Insights**

The intended flow is:

**Executive KPI summary → Churn/retention diagnosis → Payment and service diagnostics**

The design prioritizes business readability, KPI hierarchy, trend analysis, segmentation, and consistent slicers.

---

# 18. Page 1 — Executive Overview

## Purpose

Provide a high-level view of customer health and major churn patterns.

## KPI Cards

1. Total Customers
2. Active Customers
3. Churned Customers
4. Churn Rate
5. Total Payment Amount

## Visuals

### Monthly Churn Trend
- Axis: `Churn Date[Year Month]`
- Value: `[Churned Customers by Churn Date]`
- Line chart

### Churn Rate by Plan
- Axis: `subscriptions[plan]`
- Value: `[Churn Rate]`
- Column/bar chart

### Churn Rate by Contract Type
- Axis: `subscriptions[contract_type]`
- Value: `[Churn Rate]`
- Column/bar chart

### Churn Rate by Support Ticket Group
- Axis: `customers[Ticket Group]`
- Value: `[Churn Rate]`
- Column/bar chart

## Slicers

- Plan
- Contract Type
- Churn Status

### Design Observation

Page 1 functions as the executive entry point, emphasizing customer base, customer status, churn, payment value, and high-level churn segmentation.

---

# 19. Page 2 — Churn & Retention

## Purpose

Focus on customer retention, churn behavior, and acquisition trends.

## KPI Cards

1. Total Customers
2. Churned Customers
3. Churn Rate
4. New Customers

## Visuals

### Monthly Churn Trend
- Axis: `Churn Date[Year Month]`
- Value: `[Churned Customers by Churn Date]`

### New Customer Trend
- Axis: `Date[Year Month]`
- Value: `[New Customers]`

### Churned Customers by Plan
- Axis: `subscriptions[plan]`
- Value: `[Churned Customers]`

### Churn Rate by Contract Type
- Axis: `subscriptions[contract_type]`
- Value: `[Churn Rate]`

### Churn Rate by Support Ticket Group
- Axis: `customers[Ticket Group]`
- Value: `[Churn Rate]`

## Slicers

- Plan
- Contract Type
- Churn Status

### Design Observation

Page 2 moves from summary metrics into churn segmentation and customer-acquisition trends.

---

# 20. Page 3 — Customer & Service Insights

## Purpose

Analyze payment reliability and customer-service experience in relation to churn.

## KPI Cards

1. Total Payments
2. Failed Payment Transactions
3. Payment Success Rate
4. Average Satisfaction Score

## Visuals

### Failed Payment Customer Rate by Customer Status
- Axis: `subscriptions[churn_status]`
- Value: `[Failed Payment Customer Rate]`

### Customers with Failed Payments by Status
- Axis: `subscriptions[churn_status]`
- Value: `[Customers with Failed Payments]`

### Churn Rate by Support Ticket Group
- Axis: `customers[Ticket Group]`
- Value: `[Churn Rate]`

### Average Resolution Time by Customer Status
- Axis: `subscriptions[churn_status]`
- Value: `[Average Resolution Time]`

### Average Satisfaction Score by Customer Status
- Axis: `subscriptions[churn_status]`
- Value: `[Average Satisfaction Score]`

## Slicers

- Plan
- Contract Type
- Churn Status

### Design Observation

Page 3 acts as a diagnostic page for payment issues, support workload, resolution time, satisfaction, and churn.

---

# 21. Dashboard Formatting & Visual Design

## Page-Level Color Identity

| Page | Primary Identity |
|---|---|
| Executive Overview | Blue |
| Churn & Retention | Green |
| Customer & Service Insights | Purple |

This gives each page a distinct identity while retaining a consistent overall dashboard structure.

## Semantic Color Guidance

| Meaning | Suggested Color |
|---|---|
| Active | Green |
| Churned | Red |
| Neutral/general | Blue |
| Failed payment/risk | Orange or Red |
| Positive service metric | Green |
| Warning/risk | Orange |

Avoid unnecessary rainbow coloring within individual analytical visuals.

## Monthly Trend

The monthly churn chart uses a continuous date axis because a suitable categorical option was not available.

Recommended readability adjustment:

- Keep the existing date field.
- Keep chronological sorting.
- Increase Minimum category width if month labels are crowded, starting around 50–70 and increasing toward 80–100 if needed.
- Y-axis title can be hidden when the chart title already identifies the metric.

## Ticket Group

Use:

**Sort axis → Ticket Group → Ascending**

Expected order:

`0 Tickets → 1-2 Tickets → 3-5 Tickets → 6+ Tickets`

## Percentage Formatting

These measures should display as percentages:

- Churn Rate
- Churn Rate by Churn Date
- Failed Payment Customer Rate
- Payment Success Rate

## Important Page 3 Check

The **Payment Success Rate** card must use `[Payment Success Rate]` and display a percentage.

If it displays a large number such as `334K`, the card is using `[Successful Payments]` instead of `[Payment Success Rate]`.

`Total Payments` displaying approximately `355K` is appropriate because it represents payment transaction count.

---

# 22. Dashboard Design Quality Assessment

The completed design has:

- Clear three-page analytical structure
- Strong KPI hierarchy
- Good business relevance
- Consistent slicer placement
- Clear executive/churn/service separation
- Useful trend and segmentation visuals
- Distinct page-level visual identity
- Good foundation for an interview-quality portfolio project

### Current Design Assessment

**Approximate overall design quality: 8.3/10**

Remaining improvements are mainly:

- Dashboard validation
- Metric/filter validation
- Percentage-card validation
- Ticket-group sorting
- Monthly-axis readability
- Final business insights
- Business recommendations

---

# 23. Current Power BI Project Status

| Stage | Status |
|---|---|
| Data Import | Completed |
| Data Modeling | Completed |
| Relationship Modeling | Completed |
| Date Modeling | Completed |
| Signup Date Modeling | Completed |
| Churn Date Modeling | Completed |
| Customer KPI Measures | Completed |
| Subscription KPI Measures | Completed |
| Payment KPI Measures | Completed |
| Support KPI Measures | Completed |
| Failed Payment Analysis | Completed |
| Ticket Group Segmentation | Completed |
| Churn Trend Analysis | Completed |
| Initial Data Validation | Completed |
| Dashboard Design | Completed |
| Dashboard Formatting | Completed |
| Dashboard Validation | **Next** |
| Final Business Insights | Pending |
| Business Recommendations | Pending |
| GitHub Documentation | Pending |
| Resume Update | Pending |
| Interview Preparation | Pending |

---

# 24. Next Step

The next Power BI stage is **Dashboard Validation**.

Validation should cover:

1. KPI values
2. Slicer behavior
3. Cross-filtering
4. Date trends
5. Churn-rate calculations
6. New-customer calculations
7. Payment metrics
8. Support metrics
9. Percentage formatting
10. Sorting
11. Visual readability
12. Page consistency
13. Business interpretation

After validation, this same master observation file should be updated with:

- Dashboard Validation
- Final Business Insights
- Business Recommendations
- Final Power BI Project Conclusion

This remains the **single master Power BI observation/documentation file**.

---

# 25. Dashboard Validation — Completed

Dashboard validation was completed across all three Power BI pages.

## Page 1 — Executive Overview

### KPI Validation
All five KPI cards were verified:

| KPI | Result |
|---|---:|
| Total Customers | 20K |
| Active Customers | 16K |
| Churned Customers | 4K |
| Churn Rate | 22.3% |
| Total Payment Amount | 205.96M |

All KPI cards were confirmed to use the intended measures.

### Visual Validation
The following visuals were verified:

- Monthly Churn Trend
- Churn Rate by Support Ticket Group
- Churn Rate by Contract Type
- Churn Rate by Plan

The monthly trend sorting was verified as chronological.

Ticket Group sorting was verified using the logical business order:

`0 Tickets → 1-2 Tickets → 3-5 Tickets → 6+ Tickets`

## Page 2 — Churn & Retention

### KPI Validation

| KPI | Result |
|---|---:|
| Total Customers | 20K |
| Churned Customers | 4K |
| Churn Rate | 22.3% |
| New Customers | 20K |

The New Customers DAX measure was verified for the current model.

### Visual Validation

The following visuals were verified:

- Monthly Churn Trend
- New Customers by Year Month
- Churned Customers by Plan
- Churn Rate by Ticket Group
- Churn Rate by Contract Type

The date-based visuals were verified to sort chronologically by `Year Month`.

Ticket Group was verified in business order:

`0 Tickets → 1-2 Tickets → 3-5 Tickets → 6+ Tickets`

### New Customer Observation

The New Customers KPI showing 20K with the full date range is valid because the measure counts customers whose signup dates fall within the complete selected date range. The monthly trend is the more useful view for acquisition analysis.

## Page 3 — Customer & Service Insights

### KPI Validation

| KPI | Result |
|---|---:|
| Total Payments | 355K |
| Payment Success Rate | 94.0% |
| Failed Payment Transactions | 21K |
| Average Satisfaction Score | 4.4 |

The Payment Success Rate card was verified to use the percentage measure rather than the successful-payment transaction count.

### Visual Validation

The following visuals were verified:

- Failed Payment Customer Rate by Churn Status
- Customers with Failed Payments by Churn Status
- Average Resolution Time by Customer Status
- Average Satisfaction Score by Customer Status
- Churn Rate by Support Ticket Group

The Ticket Group visual is correctly ordered:

`0 Tickets → 1-2 Tickets → 3-5 Tickets → 6+ Tickets`

# 26. Slicer & Interaction Validation

The dashboard slicers were tested across the three pages:

- Plan
- Contract Type
- Churn Status

Validation covered KPI response, chart response, filter propagation, cross-filter behavior, clearing/resetting filters, and page consistency.

The slicers and visual interactions behaved as expected. After testing, the dashboard was returned to its default unfiltered state.

# 27. Final Dashboard Validation Result

## Overall Result: PASS ✅

The dashboard successfully passed:

- KPI validation
- DAX measure validation
- Visual field validation
- Date sorting validation
- Ticket Group sorting validation
- Percentage formatting validation
- Slicer validation
- Cross-filter validation
- Final visual/readability review

No critical calculation, relationship, or interaction issue remains from the completed validation checks.

**Dashboard Validation = COMPLETED**

The Power BI dashboard is now ready for the **Final Business Insights & Recommendations** stage.

# 28. Dashboard Validation Lessons / Technical Observations

### 1. Visual sorting can override intended business order

A time-series visual can appear incorrect even when the underlying data is correct if the visual is sorted by its measure rather than the date field. The correct approach is to sort the visual by `Year Month` in ascending order.

### 2. Date relationships can affect denominators

The original Churn Rate by Churn Date calculation became 1.0 because the Churn Date filter also affected the customer denominator through the bidirectional 1:1 relationship. Removing the Churn Date filter from the denominator prevented the denominator from shrinking with the churn-date context.

### 3. Customer counts and transaction counts are different metrics

For failed-payment analysis:

- `COUNTROWS(payments)` = failed payment transactions
- `DISTINCTCOUNT(payments[customer_id])` = customers experiencing failed payments

These answer different business questions and must not be interchanged.

### 4. Metric validation requires business meaning

A card must be validated by its measure, aggregation, format, and business definition—not just by whether its displayed value looks reasonable.

# 29. Current Project Status — Updated

| Stage | Status |
|---|---|
| Python Data Cleaning | Completed |
| Python Data Validation | Completed |
| SQL Analysis | Completed |
| SQL Business Questions | Completed |
| SQL Interview Queries | Completed |
| Power BI Data Import | Completed |
| Power BI Data Modeling | Completed |
| Power BI Relationship Modeling | Completed |
| Power BI Date Modeling | Completed |
| Power BI DAX Measures | Completed |
| Power BI Initial Data Validation | Completed |
| Power BI Dashboard Design | Completed |
| Power BI Dashboard Validation | **Completed ✅** |
| Final Business Insights | **Next** |
| Business Recommendations | Pending |
| Final Power BI Documentation | Pending |
| GitHub Documentation | Pending |
| Resume Update | Pending |
| Interview Preparation | Pending |

# 30. Next Stage — Final Business Insights & Recommendations

The next stage is to convert the validated dashboard into evidence-based business findings.

We will answer:

1. What customer segments have the highest churn?
2. Which contract type represents the greatest churn risk?
3. Which plans show elevated churn?
4. Is there an association between failed payments and churn?
5. Does support-ticket volume meaningfully differentiate churn?
6. Do resolution times differ between active and churned customers?
7. Does satisfaction score differ between active and churned customers?
8. What retention actions should the business prioritize?

The conclusions will distinguish observed association from proven causation.

Each final insight will follow:

**Finding → Evidence → Business Interpretation → Recommended Action**

# 31. Documentation Update Rule

This file remains the **single master Power BI observation/documentation file**.

The next update will add:

- Final Business Insights
- Business Recommendations
- Final Power BI Project Conclusion
