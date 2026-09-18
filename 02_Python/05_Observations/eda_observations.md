# Exploratory Data Analysis (EDA) Observations

## Project

**Customer Churn & Retention Analysis**

---

# Objective

Understand customer behavior, churn patterns, payment behavior, service adoption, and support experience before predictive modeling.

---

# Dataset Used

| Metric     |      Value |
| ---------- | ---------: |
| Customers  |     20,000 |
| Features   |        119 |
| Churn Rate | **22.31%** |

---

# EDA Components

## Dataset Profiling

* Dataset summary
* Column profiling
* Missing-value analysis
* Data-type verification

---

## Customer Analysis

Questions explored:

* Age distribution
* Gender distribution
* Geographic distribution
* Signup trends

---

## Subscription Analysis

Questions explored:

* Plan popularity
* Contract distribution
* Monthly charge distribution
* Tenure distribution

---

## Payment Analysis

Questions explored:

* Payment success behavior
* Payment value distribution
* Customer payment frequency
* Primary payment methods

---

## Customer Services Analysis

Questions explored:

* Service adoption rates
* Multi-service customers
* Adoption segmentation

---

## Support Analysis

Questions explored:

* Ticket volume
* Resolution performance
* Satisfaction distribution
* Support workload
* Issue-type frequency

---

## Churn Analysis

Questions explored:

* Churn by plan
* Churn by contract
* Churn by tenure
* Churn by payment behavior
* Churn by support experience
* Churn by service adoption

---

## Correlation Analysis

Generated:

* Correlation matrix
* Strong feature relationships
* Churn-related numerical correlations

---

# EDA Outputs

Generated workbooks:

* eda_summary_report.xlsx
* column_profile.xlsx
* categorical_analysis.xlsx
* numerical_analysis.xlsx
* churn_analysis.xlsx
* segment_analysis.xlsx
* correlation_analysis.xlsx
* eda_report.xlsx

Charts were also generated for business reporting.

---

# Validation Results

| Metric         |    Value |
| -------------- | -------: |
| Total Checks   |       20 |
| Passed         |       19 |
| Failed         |    **0** |
| Overall Status | **PASS** |

---

# Key Observations

### 1. Customer-Level EDA

All analysis was performed at the customer level rather than the transaction level.

### 2. Business-Oriented Analysis

EDA focused on answering business questions instead of generating generic descriptive statistics.

### 3. Analytical Readiness

The dataset is fully validated and ready for churn modeling and dashboard development.

### 4. Reproducible Reporting

Every analytical workbook can be regenerated automatically using Python.

---

# Recruiter Highlights

* Built a complete automated EDA pipeline.
* Generated reusable analytical reports instead of one-time notebooks.
* Validated analytical outputs with an independent QA layer.
* Prepared the dataset for predictive analytics and executive dashboards.

---

**Pipeline Stage:** Feature Dataset → Exploratory Data Analysis → Validation
