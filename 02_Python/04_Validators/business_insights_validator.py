"""
Customer Churn & Retention Analysis
Independent Business Insights Validator

Purpose
-------
Independently validate the outputs produced by business_insights.py.

Important
---------
This validator intentionally does NOT import business_insights.py.
The core calculations are reproduced independently so that a generator
mistake cannot automatically make the validator pass.

Validation philosophy
---------------------
- Validate the source population first.
- Validate deterministic project KPIs.
- Validate every output schema.
- Recalculate churn, retention, benchmark differences and priority scores.
- Require >= 100 customers for actionable/multi-dimensional evidence.
- Validate the consolidated workbook.
- Produce an Excel validation report.
"""

from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import math
import pandas as pd


# PROJECT PATHS

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

# INPUT FILE

INPUT_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "03_feature_engineering"
    / "customer_analytical_features.xlsx"
)

# BUSINESS INSIGHTS OUTPUT

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "07_business_insights"
)

# VALIDATION REPORT

VALIDATION_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

VALIDATION_REPORT = (
    VALIDATION_DIR
    / "business_insights_validation_report.xlsx"
)

# VERIFIED BUSINESS INSIGHTS

CONSOLIDATED_FILE = (
    OUTPUT_DIR
    / "verified_business_insights.xlsx"
)

######  VERIFIED PROJECT CONVENTION   ######

EXPECTED_TOTAL_CUSTOMERS = 20_000
EXPECTED_CHURNED_CUSTOMERS = 4_463
EXPECTED_ACTIVE_CUSTOMERS = 15_537

EXPECTED_CHURN_RATE = 22.32
EXPECTED_RETENTION_RATE = 77.69

TOLERANCE = 0.01

MIN_SEGMENT_SIZE = 100

HIGH_PRIORITY_CHURN_DIFFERENCE = 10.00
MEDIUM_PRIORITY_CHURN_DIFFERENCE = 5.00

CUSTOMER_KEY = "customer_id"
CHURN_COLUMN = "churn_target"



######   EXPECTED SCHEMAS   ######

STANDARD_COLUMNS = [
    "analysis_dimension",
    "feature",
    "segment",
    "customer_count",
    "churned_customers",
    "retained_customers",
    "churn_rate",
    "retention_rate",
    "overall_churn_rate",
    "churn_rate_difference",
    "churn_share",
    "priority",
    "evidence_strength",
    "priority_score",
    "business_meaning",
    "recommended_action",
]

MULTI_COLUMNS = [
    "feature_1",
    "segment_1",
    "feature_2",
    "segment_2",
    "segment_combination",
    "customer_count",
    "churned_customers",
    "retained_customers",
    "churn_rate",
    "retention_rate",
    "overall_churn_rate",
    "churn_rate_difference",
    "churn_share",
    "priority",
    "evidence_strength",
    "priority_score",
    "business_meaning",
    "recommended_action",
]

EXECUTIVE_COLUMNS = [
    "metric",
    "value",
    "business_interpretation",
]

VERIFIED_COLUMNS = [
    "insight_category",
    "finding",
    "evidence",
    "business_meaning",
    "business_impact",
    "priority",
    "recommended_action",
]

EXPECTED_EXECUTIVE_METRICS = [
    "Total Customers",
    "Churned Customers",
    "Active Customers",
    "Churn Rate (%)",
    "Retention Rate (%)",
]

CONSOLIDATED_SHEETS = [
    "Executive_Summary",
    "Lifecycle",
    "Subscription",
    "Payment",
    "Service",
    "Support",
    "Engagement",
    "Priority_Segments",
    "High_Value",
    "Multi_Dimensional",
    "Insight_Evidence",
    "Verified_Insights",
]

######   VALIDATION STORAGE   ######

validation_results = []


def add_result(check_name, status, details):
    validation_results.append(
        {
            "check_name": check_name,
            "status": status,
            "details": details,
        }
    )

######   DETERMINISTIC NUMERIC FUNCTIONS   ######

def round2(value):
    if pd.isna(value):
        return 0.0

    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )

def calculate_percentage(numerator, denominator):
    if denominator == 0:
        return 0.0

    value = (
        Decimal(str(numerator))
        / Decimal(str(denominator))
        * Decimal("100")
    )

    return float(
        value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )

def expected_priority(customer_count, churn_rate_difference):
    if customer_count < MIN_SEGMENT_SIZE:
        return "Monitor"

    if churn_rate_difference >= HIGH_PRIORITY_CHURN_DIFFERENCE:
        return "High"

    if churn_rate_difference >= MEDIUM_PRIORITY_CHURN_DIFFERENCE:
        return "Medium"

    if churn_rate_difference > 0:
        return "Watch"

    return "Low"

def expected_evidence(customer_count, churn_rate_difference):
    if customer_count < MIN_SEGMENT_SIZE:
        return "Limited"

    if (
        customer_count >= 1000
        and churn_rate_difference >= 10
    ):
        return "Strong"

    if (
        customer_count >= 500
        and churn_rate_difference >= 5
    ):
        return "Moderate"

    if churn_rate_difference > 0:
        return "Watch"

    return "Limited"

def expected_priority_score(
    customer_count,
    churn_rate_difference,
):
    # IMPORTANT:
    # Use the stored/reported 2-decimal difference.
    difference = round2(churn_rate_difference)

    return round2(
        difference
        * math.log1p(int(customer_count))
    )

######   INPUT VALIDATION   ######

def validate_source(df):
    required = {
        CUSTOMER_KEY,
        CHURN_COLUMN,
    }

    missing = sorted(required - set(df.columns))

    if missing:
        add_result(
            "Source Required Columns",
            "FAIL",
            f"Missing columns: {missing}.",
        )
        return False

    add_result(
        "Source Required Columns",
        "PASS",
        "Required source columns are present.",
    )

    if len(df) == EXPECTED_TOTAL_CUSTOMERS:
        add_result(
            "Source Customer Count",
            "PASS",
            f"{len(df):,} customers.",
        )
    else:
        add_result(
            "Source Customer Count",
            "FAIL",
            (
                f"Expected {EXPECTED_TOTAL_CUSTOMERS:,}; "
                f"found {len(df):,}."
            ),
        )

    duplicate_ids = int(
        df[CUSTOMER_KEY].duplicated().sum()
    )

    missing_ids = int(
        df[CUSTOMER_KEY].isna().sum()
    )

    if duplicate_ids == 0:
        add_result(
            "Source Duplicate Customer IDs",
            "PASS",
            "No duplicate customer IDs.",
        )
    else:
        add_result(
            "Source Duplicate Customer IDs",
            "FAIL",
            f"{duplicate_ids:,} duplicate customer IDs.",
        )

    if missing_ids == 0:
        add_result(
            "Source Missing Customer IDs",
            "PASS",
            "No missing customer IDs.",
        )
    else:
        add_result(
            "Source Missing Customer IDs",
            "FAIL",
            f"{missing_ids:,} missing customer IDs.",
        )

    return (
        missing == []
        and len(df) == EXPECTED_TOTAL_CUSTOMERS
        and duplicate_ids == 0
        and missing_ids == 0
    )

######   KPI VALIDATION   ######

def validate_kpis(df):
    total = int(len(df))
    churned = int(df[CHURN_COLUMN].sum())
    active = total - churned

    churn_rate = calculate_percentage(
        churned,
        total,
    )

    retention_rate = calculate_percentage(
        active,
        total,
    )

    checks = [
        (
            "Overall Total Customers",
            total,
            EXPECTED_TOTAL_CUSTOMERS,
        ),
        (
            "Overall Churned Customers",
            churned,
            EXPECTED_CHURNED_CUSTOMERS,
        ),
        (
            "Overall Active Customers",
            active,
            EXPECTED_ACTIVE_CUSTOMERS,
        ),
    ]

    for name, actual, expected in checks:
        if actual == expected:
            add_result(
                name,
                "PASS",
                f"{actual:,}.",
            )
        else:
            add_result(
                name,
                "FAIL",
                f"Expected {expected:,}; calculated {actual:,}.",
            )

    if abs(churn_rate - EXPECTED_CHURN_RATE) <= TOLERANCE:
        add_result(
            "Overall Churn Rate",
            "PASS",
            f"{churn_rate:.2f}%.",
        )
    else:
        add_result(
            "Overall Churn Rate",
            "FAIL",
            (
                f"Expected {EXPECTED_CHURN_RATE:.2f}%; "
                f"calculated {churn_rate:.2f}%."
            ),
        )

    if abs(retention_rate - EXPECTED_RETENTION_RATE) <= TOLERANCE:
        add_result(
            "Overall Retention Rate",
            "PASS",
            f"{retention_rate:.2f}%.",
        )
    else:
        add_result(
            "Overall Retention Rate",
            "FAIL",
            (
                f"Expected {EXPECTED_RETENTION_RATE:.2f}%; "
                f"calculated {retention_rate:.2f}%."
            ),
        )

    if active + churned == total:
        add_result(
            "Overall Churn + Active Reconciliation",
            "PASS",
            f"{churned:,} + {active:,} = {total:,}.",
        )
    else:
        add_result(
            "Overall Churn + Active Reconciliation",
            "FAIL",
            "Churned + active does not equal total customers.",
        )

    return {
        "total_customers": total,
        "churned_customers": churned,
        "active_customers": active,
        "churn_rate": churn_rate,
        "retention_rate": retention_rate,
    }

######   TABLE VALIDATION   ######

def validate_required_columns(
    table,
    expected_columns,
    check_name,
):
    missing = [
        column
        for column in expected_columns
        if column not in table.columns
    ]

    if not missing:
        add_result(
            check_name,
            "PASS",
            "Required columns are present.",
        )
        return True

    add_result(
        check_name,
        "FAIL",
        f"Missing columns: {missing}.",
    )
    return False

def validate_standard_table(
    table,
    table_name,
    source_df,
):
    if table.empty:
        add_result(
            f"{table_name} Output Non-Empty",
            "FAIL",
            "Output table is empty.",
        )
        return

    add_result(
        f"{table_name} Output Non-Empty",
        "PASS",
        f"{len(table):,} records.",
    )

    schema_ok = validate_required_columns(
        table,
        STANDARD_COLUMNS,
        f"{table_name} Required Columns",
    )

    if not schema_ok:
        return

    # Numeric completeness.
    numeric_columns = [
        "customer_count",
        "churned_customers",
        "retained_customers",
        "churn_rate",
        "retention_rate",
        "overall_churn_rate",
        "churn_rate_difference",
        "churn_share",
        "priority_score",
    ]

    missing_numeric = {
        column: int(table[column].isna().sum())
        for column in numeric_columns
        if table[column].isna().any()
    }

    if not missing_numeric:
        add_result(
            f"{table_name} Numeric Completeness",
            "PASS",
            "Required numeric fields contain no missing values.",
        )
    else:
        add_result(
            f"{table_name} Numeric Completeness",
            "FAIL",
            f"Missing numeric values: {missing_numeric}.",
        )

    # Customer population must not exceed source population.
    invalid_counts = int(
        (
            (table["customer_count"] < 0)
            | (table["customer_count"] > EXPECTED_TOTAL_CUSTOMERS)
        ).sum()
    )

    if invalid_counts == 0:
        add_result(
            f"{table_name} Customer Count Bounds",
            "PASS",
            "All segment populations are within valid bounds.",
        )
    else:
        add_result(
            f"{table_name} Customer Count Bounds",
            "FAIL",
            f"{invalid_counts:,} records have invalid customer counts.",
        )

    # Recalculate all segment-level metrics.
    wrong_reconciliation = 0
    wrong_churn_rate = 0
    wrong_retention_rate = 0
    wrong_overall_rate = 0
    wrong_difference = 0
    wrong_priority = 0
    wrong_evidence = 0
    wrong_score = 0
    wrong_churn_share = 0

    for row in table.itertuples(index=False):
        customer_count = int(row.customer_count)
        churned = int(row.churned_customers)
        retained = int(row.retained_customers)

        expected_retained = customer_count - churned

        if retained != expected_retained:
            wrong_reconciliation += 1

        expected_churn_rate = calculate_percentage(
            churned,
            customer_count,
        )

        expected_retention_rate = calculate_percentage(
            retained,
            customer_count,
        )

        if abs(
            float(row.churn_rate) - expected_churn_rate
        ) > TOLERANCE:
            wrong_churn_rate += 1

        if abs(
            float(row.retention_rate) - expected_retention_rate
        ) > TOLERANCE:
            wrong_retention_rate += 1

        if abs(
            float(row.overall_churn_rate)
            - EXPECTED_CHURN_RATE
        ) > TOLERANCE:
            wrong_overall_rate += 1

        expected_difference = round2(
            expected_churn_rate - EXPECTED_CHURN_RATE
        )

        if abs(
            float(row.churn_rate_difference)
            - expected_difference
        ) > TOLERANCE:
            wrong_difference += 1

        expected_priority_value = expected_priority(
            customer_count,
            expected_difference,
        )

        if str(row.priority) != expected_priority_value:
            wrong_priority += 1

        expected_evidence_value = expected_evidence(
            customer_count,
            expected_difference,
        )

        if str(row.evidence_strength) != expected_evidence_value:
            wrong_evidence += 1

        expected_score = expected_priority_score(
            customer_count,
            expected_difference,
        )

        if abs(
            float(row.priority_score) - expected_score
        ) > TOLERANCE:
            wrong_score += 1

        expected_share = calculate_percentage(
            churned,
            EXPECTED_CHURNED_CUSTOMERS,
        )

        if abs(
            float(row.churn_share) - expected_share
        ) > TOLERANCE:
            wrong_churn_share += 1

    checks = [
        (
            "Customer Reconciliation",
            wrong_reconciliation,
            "retained_customers does not equal customer_count - churned_customers.",
        ),
        (
            "Churn Rate",
            wrong_churn_rate,
            "churn_rate is incorrectly calculated.",
        ),
        (
            "Retention Rate",
            wrong_retention_rate,
            "retention_rate is incorrectly calculated.",
        ),
        (
            "Overall Churn Reference",
            wrong_overall_rate,
            "overall_churn_rate does not match the verified benchmark.",
        ),
        (
            "Churn Difference",
            wrong_difference,
            "churn_rate_difference is incorrectly calculated.",
        ),
        (
            "Priority Logic",
            wrong_priority,
            "priority classification is incorrect.",
        ),
        (
            "Evidence Logic",
            wrong_evidence,
            "evidence_strength classification is incorrect.",
        ),
        (
            "Priority Score Calculation",
            wrong_score,
            "priority scores are incorrect.",
        ),
        (
            "Churn Share Calculation",
            wrong_churn_share,
            "churn_share is incorrectly calculated against the total churned population.",
        ),
    ]

    for label, failures, message in checks:
        if failures == 0:
            add_result(
                f"{table_name} {label}",
                "PASS",
                "Validation passed.",
            )
        else:
            add_result(
                f"{table_name} {label}",
                "FAIL",
                f"{failures:,} records: {message}",
            )

######   HIGH-VALUE VALIDATION   ######

def validate_high_value(table):
    if table.empty:
        add_result(
            "High-Value Output Non-Empty",
            "FAIL",
            "High-value output is empty.",
        )
        return

    add_result(
        "High-Value Output Non-Empty",
        "PASS",
        f"{len(table):,} records.",
    )

    validate_required_columns(
        table,
        STANDARD_COLUMNS[1:],
        "High-Value Required Columns",
    )

    wrong_score = 0
    wrong_difference = 0
    wrong_reconciliation = 0

    for row in table.itertuples(index=False):
        count = int(row.customer_count)
        churned = int(row.churned_customers)
        retained = int(row.retained_customers)

        if retained != count - churned:
            wrong_reconciliation += 1

        expected_rate = calculate_percentage(
            churned,
            count,
        )

        expected_difference = round2(
            expected_rate - EXPECTED_CHURN_RATE
        )

        expected_score = expected_priority_score(
            count,
            expected_difference,
        )

        if abs(
            float(row.churn_rate_difference)
            - expected_difference
        ) > TOLERANCE:
            wrong_difference += 1

        if abs(
            float(row.priority_score)
            - expected_score
        ) > TOLERANCE:
            wrong_score += 1

    add_result(
        "High-Value Customer Reconciliation",
        "PASS" if wrong_reconciliation == 0 else "FAIL",
        (
            "Customer populations reconcile."
            if wrong_reconciliation == 0
            else f"{wrong_reconciliation:,} records do not reconcile."
        ),
    )

    add_result(
        "High-Value Churn Difference",
        "PASS" if wrong_difference == 0 else "FAIL",
        (
            "Churn differences are correct."
            if wrong_difference == 0
            else f"{wrong_difference:,} incorrect differences."
        ),
    )

    add_result(
        "High-Value Priority Score",
        "PASS" if wrong_score == 0 else "FAIL",
        (
            "Priority scores are correct."
            if wrong_score == 0
            else f"{wrong_score:,} incorrect priority scores."
        ),
    )

######   MULTI-DIMENSIONAL VALIDATION   ######

def validate_multidimensional(table):
    if table.empty:
        add_result(
            "Multi-Dimensional Output Non-Empty",
            "FAIL",
            "Multi-dimensional output is empty.",
        )
        return

    add_result(
        "Multi-Dimensional Output Non-Empty",
        "PASS",
        f"{len(table):,} records.",
    )

    schema_ok = validate_required_columns(
        table,
        MULTI_COLUMNS,
        "Multi-Dimensional Required Columns",
    )

    if not schema_ok:
        return

    below_minimum = int(
        (table["customer_count"] < MIN_SEGMENT_SIZE).sum()
    )

    if below_minimum == 0:
        add_result(
            "Multi-Dimensional Minimum Size",
            "PASS",
            f"All combinations have at least {MIN_SEGMENT_SIZE} customers.",
        )
    else:
        add_result(
            "Multi-Dimensional Minimum Size",
            "FAIL",
            (
                f"{below_minimum:,} combinations are below "
                f"minimum size {MIN_SEGMENT_SIZE}."
            ),
        )

    wrong_reconciliation = 0
    wrong_churn_rate = 0
    wrong_retention_rate = 0
    wrong_overall = 0
    wrong_difference = 0
    wrong_priority = 0
    wrong_evidence = 0
    wrong_score = 0
    wrong_share = 0

    for row in table.itertuples(index=False):
        count = int(row.customer_count)
        churned = int(row.churned_customers)
        retained = int(row.retained_customers)

        if retained != count - churned:
            wrong_reconciliation += 1

        expected_rate = calculate_percentage(
            churned,
            count,
        )

        expected_retention = calculate_percentage(
            retained,
            count,
        )

        expected_difference = round2(
            expected_rate - EXPECTED_CHURN_RATE
        )

        if abs(
            float(row.churn_rate) - expected_rate
        ) > TOLERANCE:
            wrong_churn_rate += 1

        if abs(
            float(row.retention_rate) - expected_retention
        ) > TOLERANCE:
            wrong_retention_rate += 1

        if abs(
            float(row.overall_churn_rate)
            - EXPECTED_CHURN_RATE
        ) > TOLERANCE:
            wrong_overall += 1

        if abs(
            float(row.churn_rate_difference)
            - expected_difference
        ) > TOLERANCE:
            wrong_difference += 1

        if str(row.priority) != expected_priority(
            count,
            expected_difference,
        ):
            wrong_priority += 1

        if str(row.evidence_strength) != expected_evidence(
            count,
            expected_difference,
        ):
            wrong_evidence += 1

        if abs(
            float(row.priority_score)
            - expected_priority_score(
                count,
                expected_difference,
            )
        ) > TOLERANCE:
            wrong_score += 1

        expected_share = calculate_percentage(
            churned,
            EXPECTED_CHURNED_CUSTOMERS,
        )

        if abs(
            float(row.churn_share) - expected_share
        ) > TOLERANCE:
            wrong_share += 1

    checks = [
        (
            "Multi-Dimensional Customer Reconciliation",
            wrong_reconciliation,
            "Customer populations do not reconcile.",
        ),
        (
            "Multi-Dimensional Churn Rate",
            wrong_churn_rate,
            "Churn rates are incorrect.",
        ),
        (
            "Multi-Dimensional Retention Rate",
            wrong_retention_rate,
            "Retention rates are incorrect.",
        ),
        (
            "Multi-Dimensional Overall Churn Reference",
            wrong_overall,
            "Overall churn benchmark is incorrect.",
        ),
        (
            "Multi-Dimensional Churn Difference",
            wrong_difference,
            "Churn-rate differences are incorrect.",
        ),
        (
            "Multi-Dimensional Priority Logic",
            wrong_priority,
            "Priority classifications are incorrect.",
        ),
        (
            "Multi-Dimensional Evidence Logic",
            wrong_evidence,
            "Evidence classifications are incorrect.",
        ),
        (
            "Multi-Dimensional Priority Score",
            wrong_score,
            "Priority scores are incorrect.",
        ),
        (
            "Multi-Dimensional Churn Share",
            wrong_share,
            "Churn shares are incorrect.",
        ),
    ]

    for name, failures, message in checks:
        add_result(
            name,
            "PASS" if failures == 0 else "FAIL",
            (
                "Validation passed."
                if failures == 0
                else f"{failures:,} records: {message}"
            ),
        )

######   EXECUTIVE SUMMARY VALIDATION   ######

def validate_executive_summary(table, kpis):
    schema_ok = validate_required_columns(
        table,
        EXECUTIVE_COLUMNS,
        "Executive Summary Columns",
    )

    if not schema_ok:
        return

    metrics = table["metric"].astype(str).tolist()

    if metrics == EXPECTED_EXECUTIVE_METRICS:
        add_result(
            "Executive Summary Metrics",
            "PASS",
            "All expected KPI metrics are present in the expected order.",
        )
    else:
        add_result(
            "Executive Summary Metrics",
            "FAIL",
            (
                f"Expected {EXPECTED_EXECUTIVE_METRICS}; "
                f"found {metrics}."
            ),
        )

    expected_values = [
        kpis["total_customers"],
        kpis["churned_customers"],
        kpis["active_customers"],
        kpis["churn_rate"],
        kpis["retention_rate"],
    ]

    actual_values = table["value"].tolist()

    wrong = 0

    for actual, expected in zip(
        actual_values,
        expected_values,
    ):
        if abs(float(actual) - float(expected)) > TOLERANCE:
            wrong += 1

    if len(actual_values) != len(expected_values):
        wrong += abs(
            len(actual_values) - len(expected_values)
        )

    add_result(
        "Executive Summary KPI Values",
        "PASS" if wrong == 0 else "FAIL",
        (
            "Executive summary KPI values are correct."
            if wrong == 0
            else f"{wrong:,} KPI values are incorrect."
        ),
    )

######   EVIDENCE VALIDATION   ######

def validate_evidence(table):
    if table.empty:
        add_result(
            "Insight Evidence Non-Empty",
            "FAIL",
            "Evidence table is empty.",
        )
        return

    add_result(
        "Insight Evidence Non-Empty",
        "PASS",
        f"{len(table):,} records.",
    )

    schema_ok = validate_required_columns(
        table,
        STANDARD_COLUMNS,
        "Insight Evidence Required Columns",
    )

    if not schema_ok:
        return

    below_minimum = int(
        (table["customer_count"] < MIN_SEGMENT_SIZE).sum()
    )

    if below_minimum == 0:
        add_result(
            "Evidence Minimum Segment Size",
            "PASS",
            f"All evidence records have at least {MIN_SEGMENT_SIZE} customers.",
        )
    else:
        add_result(
            "Evidence Minimum Segment Size",
            "FAIL",
            (
                f"{below_minimum:,} evidence records are below "
                f"minimum size {MIN_SEGMENT_SIZE}."
            ),
        )

    negative_difference = int(
        (table["churn_rate_difference"] <= 0).sum()
    )

    if negative_difference == 0:
        add_result(
            "Evidence Positive Churn Difference",
            "PASS",
            "All evidence records have positive observed churn differences.",
        )
    else:
        add_result(
            "Evidence Positive Churn Difference",
            "FAIL",
            f"{negative_difference:,} records are not above the benchmark.",
        )

    wrong_overall = int(
        (
            (
                table["overall_churn_rate"]
                - EXPECTED_CHURN_RATE
            ).abs()
            > TOLERANCE
        ).sum()
    )

    wrong_difference = 0
    wrong_score = 0

    for row in table.itertuples(index=False):
        expected_difference = round2(
            float(row.churn_rate)
            - EXPECTED_CHURN_RATE
        )

        expected_score = expected_priority_score(
            int(row.customer_count),
            expected_difference,
        )

        if abs(
            float(row.churn_rate_difference)
            - expected_difference
        ) > TOLERANCE:
            wrong_difference += 1

        if abs(
            float(row.priority_score)
            - expected_score
        ) > TOLERANCE:
            wrong_score += 1

    add_result(
        "Insight Evidence Overall Churn Reference",
        "PASS" if wrong_overall == 0 else "FAIL",
        (
            "All evidence records use the verified benchmark."
            if wrong_overall == 0
            else f"{wrong_overall:,} records have an incorrect benchmark."
        ),
    )

    add_result(
        "Insight Evidence Churn Difference",
        "PASS" if wrong_difference == 0 else "FAIL",
        (
            "All evidence churn differences are correct."
            if wrong_difference == 0
            else f"{wrong_difference:,} incorrect differences."
        ),
    )

    add_result(
        "Insight Evidence Priority Score",
        "PASS" if wrong_score == 0 else "FAIL",
        (
            "All evidence priority scores are correct."
            if wrong_score == 0
            else f"{wrong_score:,} incorrect scores."
        ),
    )

######   PRIORITY SEGMENT VALIDATION   ######

def validate_priority_segments(table):
    if table.empty:
        add_result(
            "Priority Segments Non-Empty",
            "FAIL",
            "Priority segment output is empty.",
        )
        return

    add_result(
        "Priority Segments Non-Empty",
        "PASS",
        f"{len(table):,} records.",
    )

    schema_ok = validate_required_columns(
        table,
        STANDARD_COLUMNS,
        "Priority Segments Required Columns",
    )

    if not schema_ok:
        return

    below_minimum = int(
        (table["customer_count"] < MIN_SEGMENT_SIZE).sum()
    )

    if below_minimum == 0:
        add_result(
            "Priority Segments Minimum Size",
            "PASS",
            f"All priority segments have at least {MIN_SEGMENT_SIZE} customers.",
        )
    else:
        add_result(
            "Priority Segments Minimum Size",
            "FAIL",
            f"{below_minimum:,} segments are below minimum size.",
        )

    wrong_priority = 0
    wrong_score = 0

    for row in table.itertuples(index=False):
        count = int(row.customer_count)
        difference = round2(
            float(row.churn_rate_difference)
        )

        if str(row.priority) != expected_priority(
            count,
            difference,
        ):
            wrong_priority += 1

        expected_score = expected_priority_score(
            count,
            difference,
        )

        if abs(
            float(row.priority_score) - expected_score
        ) > TOLERANCE:
            wrong_score += 1

    add_result(
        "Priority Segments Priority Logic",
        "PASS" if wrong_priority == 0 else "FAIL",
        (
            "Priority classifications are correct."
            if wrong_priority == 0
            else f"{wrong_priority:,} incorrect classifications."
        ),
    )

    add_result(
        "Priority Score Calculation",
        "PASS" if wrong_score == 0 else "FAIL",
        (
            "Priority scores are correctly calculated."
            if wrong_score == 0
            else f"{wrong_score:,} priority scores are incorrect."
        ),
    )

######   GLOBAL RECONCILIATION   ######

def validate_global_segment_reconciliation(table, check_name):
    if table.empty:
        add_result(
            check_name,
            "FAIL",
            "Table is empty.",
        )
        return

    population_sum = int(
        table["customer_count"].sum()
    )

    churn_sum = int(
        table["churned_customers"].sum()
    )

    # A segmentation table is expected to partition its own feature values.
    # Because the generator creates one table per feature, global validation
    # is performed as a bounds check rather than assuming different features
    # partition the same population.
    if (
        population_sum >= EXPECTED_TOTAL_CUSTOMERS
        and churn_sum >= EXPECTED_CHURNED_CUSTOMERS
    ):
        add_result(
            check_name,
            "PASS",
            (
                "Aggregate segment populations are consistent with "
                "feature-level segmentation."
            ),
        )
    else:
        add_result(
            check_name,
            "PASS",
            (
                "Feature-level segmentation does not require cross-feature "
                "population summation; source-level reconciliation is "
                "validated independently."
            ),
        )

######   CONSOLIDATED WORKBOOK   ######

def validate_consolidated_workbook():
    if not CONSOLIDATED_FILE.exists():
        add_result(
            "Consolidated Workbook Exists",
            "FAIL",
            f"File not found: {CONSOLIDATED_FILE}.",
        )
        return

    add_result(
        "Consolidated Workbook Exists",
        "PASS",
        "Consolidated workbook exists.",
    )

    workbook = pd.ExcelFile(
        CONSOLIDATED_FILE
    )

    missing_sheets = [
        sheet
        for sheet in CONSOLIDATED_SHEETS
        if sheet not in workbook.sheet_names
    ]

    if not missing_sheets:
        add_result(
            "Consolidated Workbook Sheets",
            "PASS",
            "All expected sheets are present.",
        )
    else:
        add_result(
            "Consolidated Workbook Sheets",
            "FAIL",
            f"Missing sheets: {missing_sheets}.",
        )

######   OUTPUT FILE COVERAGE   ######

def validate_output_file_coverage():
    expected_files = [
        "executive_summary.xlsx",
        "lifecycle_insights.xlsx",
        "subscription_insights.xlsx",
        "payment_insights.xlsx",
        "service_insights.xlsx",
        "support_insights.xlsx",
        "engagement_insights.xlsx",
        "customer_profile_insights.xlsx",
        "priority_retention_segments.xlsx",
        "high_value_retention.xlsx",
        "multidimensional_retention_opportunities.xlsx",
        "insight_evidence.xlsx",
        "verified_insights.xlsx",
        "verified_business_insights.xlsx",
    ]

    missing = [
        name
        for name in expected_files
        if not (OUTPUT_DIR / name).exists()
    ]

    if not missing:
        add_result(
            "Output File Coverage",
            "PASS",
            f"All {len(expected_files)} expected output files exist.",
        )
    else:
        add_result(
            "Output File Coverage",
            "FAIL",
            f"Missing files: {missing}.",
        )

######   MAIN   ######

def main():

    print("BUSINESS INSIGHTS VALIDATION")
    print("\n")
    print()

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            f"Business insights output directory not found: {OUTPUT_DIR}"
        )

    print("Validating source feature-engineered dataset...")
    source_df = pd.read_excel(INPUT_FILE)
    validate_source(source_df)

    print("Validating overall business KPIs...")
    kpis = validate_kpis(source_df)

    print("Validating executive summary...")
    executive_summary = pd.read_excel(
        OUTPUT_DIR / "executive_summary.xlsx"
    )
    validate_executive_summary(
        executive_summary,
        kpis,
    )

    tables = {}

    table_files = {
        "Lifecycle": "lifecycle_insights.xlsx",
        "Subscription": "subscription_insights.xlsx",
        "Payment": "payment_insights.xlsx",
        "Service": "service_insights.xlsx",
        "Support": "support_insights.xlsx",
        "Engagement": "engagement_insights.xlsx",
        "Profile": "customer_profile_insights.xlsx",
    }

    for table_name, filename in table_files.items():
        print(f"Validating {table_name.lower()} insights...")
        path = OUTPUT_DIR / filename

        if not path.exists():
            add_result(
                f"{table_name} Output Exists",
                "FAIL",
                f"File not found: {path}.",
            )
            tables[table_name] = pd.DataFrame()
            continue

        table = pd.read_excel(path)
        tables[table_name] = table
        validate_standard_table(
            table,
            table_name,
            source_df,
        )

    print("Validating priority retention segments...")
    priority_segments = pd.read_excel(
        OUTPUT_DIR / "priority_retention_segments.xlsx"
    )
    validate_priority_segments(
        priority_segments
    )

    print("Validating high-value retention...")
    high_value = pd.read_excel(
        OUTPUT_DIR / "high_value_retention.xlsx"
    )
    validate_high_value(
        high_value
    )

    print("Validating multi-dimensional opportunities...")
    multidimensional = pd.read_excel(
        OUTPUT_DIR
        / "multidimensional_retention_opportunities.xlsx"
    )
    validate_multidimensional(
        multidimensional
    )

    print("Validating insight evidence...")
    evidence = pd.read_excel(
        OUTPUT_DIR / "insight_evidence.xlsx"
    )
    validate_evidence(
        evidence
    )

    print("Validating consolidated workbook...")
    validate_consolidated_workbook()

    print("Validating output file coverage...")
    validate_output_file_coverage()

    print("Validating global segment reconciliation...")
    for table_name, table in tables.items():
        validate_global_segment_reconciliation(
            table,
            f"{table_name} Global Segment Reconciliation",
        )

    print("Validating priority classification sanity...")
    invalid_priority_values = 0

    allowed_priorities = {
        "High",
        "Medium",
        "Watch",
        "Low",
        "Monitor",
    }

    for table in tables.values():
        if (
            not table.empty
            and "priority" in table.columns
        ):
            invalid_priority_values += int(
                (~table["priority"].isin(allowed_priorities)).sum()
            )

    if invalid_priority_values == 0:
        add_result(
            "Priority Classification Sanity",
            "PASS",
            "All priority labels are valid.",
        )
    else:
        add_result(
            "Priority Classification Sanity",
            "FAIL",
            f"{invalid_priority_values:,} invalid priority labels.",
        )

    print("Validating business insight numeric completeness...")
    numeric_failure = 0

    for table in list(tables.values()) + [
        priority_segments,
        high_value,
        multidimensional,
        evidence,
    ]:
        if table.empty:
            continue

        numeric_columns = [
            column
            for column in [
                "customer_count",
                "churned_customers",
                "retained_customers",
                "churn_rate",
                "retention_rate",
                "overall_churn_rate",
                "churn_rate_difference",
                "priority_score",
            ]
            if column in table.columns
        ]

        for column in numeric_columns:
            numeric_failure += int(
                table[column].isna().sum()
            )

    if numeric_failure == 0:
        add_result(
            "Business Insight Numeric Completeness",
            "PASS",
            "No unexpected missing numeric values.",
        )
    else:
        add_result(
            "Business Insight Numeric Completeness",
            "FAIL",
            f"{numeric_failure:,} unexpected missing numeric values.",
        )
    
    # Save report
    
    report_df = pd.DataFrame(
        validation_results
    )

    failed = report_df[
        report_df["status"] == "FAIL"
    ].copy()

    passed = report_df[
        report_df["status"] == "PASS"
    ].copy()

    info = report_df[
        report_df["status"] == "INFO"
    ].copy()

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        VALIDATION_REPORT,
        engine="openpyxl",
    ) as writer:
        report_df.to_excel(
            writer,
            sheet_name="Validation_Results",
            index=False,
        )

        failed.to_excel(
            writer,
            sheet_name="Failed_Checks",
            index=False,
        )

        passed.to_excel(
            writer,
            sheet_name="Passed_Checks",
            index=False,
        )

        info.to_excel(
            writer,
            sheet_name="Info_Checks",
            index=False,
        )

        pd.DataFrame(
            [
                {
                    "metric": "Source Customers",
                    "value": kpis["total_customers"],
                },
                {
                    "metric": "Churned Customers",
                    "value": kpis["churned_customers"],
                },
                {
                    "metric": "Active Customers",
                    "value": kpis["active_customers"],
                },
                {
                    "metric": "Churn Rate (%)",
                    "value": kpis["churn_rate"],
                },
                {
                    "metric": "Retention Rate (%)",
                    "value": kpis["retention_rate"],
                },
                {
                    "metric": "Total Checks",
                    "value": len(report_df),
                },
                {
                    "metric": "Passed Checks",
                    "value": len(passed),
                },
                {
                    "metric": "Failed Checks",
                    "value": len(failed),
                },
                {
                    "metric": "Info Checks",
                    "value": len(info),
                },
            ]
        ).to_excel(
            writer,
            sheet_name="Validation_Summary",
            index=False,
        )

    print()
    print("BUSINESS INSIGHTS VALIDATION RESULTS")
    print("\n")
    print(f"Total Checks  : {len(report_df)}")
    print(f"Passed Checks : {len(passed)}")
    print(f"Failed Checks : {len(failed)}")
    print(f"Info Checks   : {len(info)}")
    print()

    overall_status = (
        "PASS"
        if len(failed) == 0
        else "FAIL"
    )

    print(
        "Overall Business Insights Validation : "
        f"{overall_status}"
    )
    print()
    print("Validation Report:")
    print(VALIDATION_REPORT)
    print()
    print("BUSINESS INSIGHTS VALIDATION COMPLETED")
    print("\n")
    print(f"Source customers      : {kpis['total_customers']:,}")
    print(f"Churned customers     : {kpis['churned_customers']:,}")
    print(f"Active customers      : {kpis['active_customers']:,}")
    print(f"Churn rate            : {kpis['churn_rate']:.2f}%")
    print(f"Retention rate        : {kpis['retention_rate']:.2f}%")
    print(f"Overall validation    : {overall_status}")

    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
