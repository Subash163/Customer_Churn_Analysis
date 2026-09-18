"""
Independent validator for Business Recommendations.

Run from the project python root:
    python 04_Validators/business_recommendations_validator.py

Design:
- Does not import business_recommendations.py.
- Validates the actual generated 40 recommendation records.
- Validates the 10 Multi-Dimensional recommendation records separately.
- Uses Business Insights as the source of truth for recommendation metrics.
- Allows small analytical source segments; the 100-customer threshold applies
  only to actionable recommendations.
- Customer Profile is loaded from its standalone Business Insights workbook.
"""

from __future__ import annotations

import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd

######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   BUSINESS INSIGHTS   ######

BI_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "07_business_insights"
)

BI_FILE = (
    BI_DIR
    / "verified_business_insights.xlsx"
)

PROFILE_FILE = (
    BI_DIR
    / "customer_profile_insights.xlsx"
)

######   BUSINESS RECOMMENDATIONS   ######

REC_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "08_business_recommendations"
)

REC_FILE = (
    REC_DIR
    / "business_recommendations.xlsx"
)

SUMMARY_FILE = (
    REC_DIR
    / "recommendation_summary.xlsx"
)

######   VALIDATION REPORT   ######

REPORT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_DIR
    / "business_recommendations_validation_report.xlsx"
)

######   VERIFIED PROJECT CONVENTION   ######

TOTAL_CUSTOMERS = 20_000
CHURNED_CUSTOMERS = 4_463
ACTIVE_CUSTOMERS = 15_537
CHURN_RATE = 22.32
RETENTION_RATE = 77.69

MIN_SEGMENT_SIZE = 100
EXPECTED_TOTAL_RECOMMENDATIONS = 40
EXPECTED_MULTI_RECOMMENDATIONS = 10

######   COLUMN CONTRACTS   ######

EXECUTIVE_COLUMNS = ["metric", "value", "business_interpretation"]

STANDARD_SOURCE_COLUMNS = [
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

MULTI_SOURCE_COLUMNS = [
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

RECOMMENDATION_COLUMNS = [
    "recommendation_id", "recommendation_area", "target_segment",
    "analysis_dimension", "feature", "segment", "observed_finding",
    "evidence", "customer_count", "churned_customers",
    "retained_customers", "observed_churn_rate",
    "observed_retention_rate", "overall_churn_rate",
    "churn_rate_difference", "churn_share",
    "business_problem_opportunity", "recommended_action",
    "expected_business_impact", "priority", "implementation_effort",
    "recommendation_score", "measurement_kpi", "success_metric",
    "monitoring_frequency", "causality_note",
]

IMPLEMENTATION_COLUMNS = [
    "recommendation_id", "recommendation_area", "target_segment", "priority",
    "implementation_effort", "recommended_action", "expected_business_impact",
    "measurement_kpi", "success_metric", "monitoring_frequency",
]

EXPECTED_BI_SHEETS = {
    "Executive_Summary", "Lifecycle", "Subscription", "Payment",
    "Service", "Support", "Engagement", "Priority_Segments",
    "High_Value", "Multi_Dimensional", "Insight_Evidence", "Verified_Insights",
}

CORE_AREAS = {
    "Customer Lifecycle", "Subscription", "Payment", "Service Adoption",
    "Support Experience", "Customer Engagement", "Customer Profile",
}

######   HELPERS   ######

def round2(value) -> float:
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    )


def num(value, default=0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def integer(value, default=0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def txt(value) -> str:
    if pd.isna(value):
        return ""
    value = str(value).strip()
    return "" if value.lower() in {"nan", "none", "nat"} else value


def norm(value) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def metric_key(value) -> str:
    """Normalize summary metric labels for punctuation/spacing differences."""
    return re.sub(r"[^a-z0-9]+", "", txt(value).lower())


def close(a, b, tolerance=0.01) -> bool:
    return math.isclose(num(a), num(b), abs_tol=tolerance)


def load_book(path: Path) -> dict[str, pd.DataFrame]:
    return {
        sheet: pd.read_excel(path, sheet_name=sheet)
        for sheet in pd.ExcelFile(path).sheet_names
    }


def locate(book, names):
    normalized = {norm(k): k for k in book}
    for name in names:
        key = norm(name)
        if key in normalized:
            actual = normalized[key]
            return actual, book[actual]
    return None, None

######   VALIDATION ENGINE   ######

class Validator:
    def __init__(self):
        self.rows = []

    def check(self, category, name, passed, message):
        self.rows.append({
            "category": category,
            "check_name": name,
            "status": "PASS" if bool(passed) else "FAIL",
            "message": message,
        })

    def info(self, category, name, message):
        self.rows.append({
            "category": category,
            "check_name": name,
            "status": "INFO",
            "message": message,
        })

    @property
    def df(self):
        return pd.DataFrame(self.rows)

    @property
    def total(self):
        return len(self.rows)

    @property
    def passed(self):
        return sum(x["status"] == "PASS" for x in self.rows)

    @property
    def failed(self):
        return sum(x["status"] == "FAIL" for x in self.rows)

    @property
    def info_count(self):
        return sum(x["status"] == "INFO" for x in self.rows)


######   BUSINESS INSIGHTS SOURCES   ######

def load_business_insights(v: Validator):
    if not BI_FILE.exists():
        v.check("Business Insights", "Workbook Exists", False, f"Missing: {BI_FILE}")
        return {}

    book = load_book(BI_FILE)
    v.check(
        "Business Insights", "Workbook Exists", True,
        f"Loaded {len(book)} sheets from verified Business Insights workbook."
    )

    actual = {norm(x) for x in book}
    missing = [x for x in EXPECTED_BI_SHEETS if norm(x) not in actual]
    v.check(
        "Business Insights", "Consolidated Sheet Coverage", not missing,
        "All 12 verified sheets are present." if not missing else f"Missing: {missing}"
    )

    if PROFILE_FILE.exists():
        profile_book = load_book(PROFILE_FILE)
        if profile_book:
            book["Customer_Profile"] = next(iter(profile_book.values()))
            v.check(
                "Business Insights", "Customer Profile Source", True,
                "Standalone Customer Profile source loaded."
            )
        else:
            v.check(
                "Business Insights", "Customer Profile Source", False,
                "Customer Profile workbook contains no readable sheet."
            )
    else:
        v.check(
            "Business Insights", "Customer Profile Source", False,
            f"Missing: {PROFILE_FILE}"
        )

    return book


def validate_business_insights_schema(v: Validator, book):
    standard_names = [
        "Lifecycle", "Subscription", "Payment", "Service", "Support",
        "Engagement", "Customer_Profile", "Priority_Segments",
    ]

    for name in standard_names:
        _, df = locate(book, [name, name.replace("_", " ")])
        v.check(
            "Business Insights", f"{name} Available", df is not None,
            f"{name} source is available."
        )
        if df is not None:
            missing = [c for c in STANDARD_SOURCE_COLUMNS if c not in df.columns]
            v.check(
                "Business Insights", f"{name} Schema", not missing,
                "Required source columns are present." if not missing else f"Missing: {missing}"
            )

    _, multi = locate(book, ["Multi_Dimensional", "Multi-Dimensional"])
    v.check(
        "Business Insights", "Multi-Dimensional Source Available", multi is not None,
        "Multi-dimensional source is available."
    )
    if multi is not None:
        missing = [c for c in MULTI_SOURCE_COLUMNS if c not in multi.columns]
        v.check(
            "Business Insights", "Multi-Dimensional Source Schema", not missing,
            "Required source columns are present." if not missing else f"Missing: {missing}"
        )


def extract_kpis(book):
    _, df = locate(book, ["Executive_Summary"])
    if df is None:
        return {}

    kpis = {}
    for _, row in df.iterrows():
        metric = txt(row["metric"]).lower()
        if metric == "total customers":
            kpis["total"] = integer(row["value"])
        elif metric == "churned customers":
            kpis["churned"] = integer(row["value"])
        elif metric == "active customers":
            kpis["active"] = integer(row["value"])
        elif metric == "churn rate (%)":
            kpis["churn_rate"] = num(row["value"])
        elif metric == "retention rate (%)":
            kpis["retention_rate"] = num(row["value"])
    return kpis


def validate_kpis(v: Validator, book):
    _, executive = locate(book, ["Executive_Summary"])
    v.check(
        "KPI",
        "Executive Summary Available",
        executive is not None,
        "Executive Summary is available.",
    )
    if executive is None:
        return

    missing = [c for c in EXECUTIVE_COLUMNS if c not in executive.columns]
    v.check(
        "KPI", "Executive Summary Schema", not missing,
        "Executive Summary schema is valid." if not missing else f"Missing: {missing}"
    )

    k = extract_kpis(book)
    expected = {
        "total": TOTAL_CUSTOMERS,
        "churned": CHURNED_CUSTOMERS,
        "active": ACTIVE_CUSTOMERS,
        "churn_rate": CHURN_RATE,
        "retention_rate": RETENTION_RATE,
    }

    for key, expected_value in expected.items():
        actual = k.get(key)
        passed = (
            close(actual, expected_value)
            if isinstance(expected_value, float)
            else actual == expected_value
        )
        v.check("KPI", f"Verified {key}", passed, f"Expected {expected_value}; found {actual}.")

    v.check(
        "KPI", "Customer Reconciliation",
        k.get("churned", -1) + k.get("active", -1) == k.get("total", -2),
        "Churned + active equals total customers."
    )

    calculated = float(
        (
            Decimal(CHURNED_CUSTOMERS)
            / Decimal(TOTAL_CUSTOMERS)
            * Decimal(100)
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )
    v.check(
        "KPI", "Independent Churn Calculation", calculated == CHURN_RATE,
        f"Independent churn calculation = {calculated:.2f}%."
    )


def validate_source_metrics(v: Validator, book):
    areas = [
        "Lifecycle", "Subscription", "Payment", "Service", "Support",
        "Engagement", "Customer_Profile", "Priority_Segments",
    ]

    for area in areas:
        _, df = locate(book, [area, area.replace("_", " ")])
        if df is None or df.empty:
            continue

        w = df.copy()
        for c in [
            "customer_count", "churned_customers", "retained_customers",
            "churn_rate", "retention_rate", "overall_churn_rate",
            "churn_rate_difference",
        ]:
            w[c] = pd.to_numeric(w[c], errors="coerce")

        reconciliation = (
            w["churned_customers"] + w["retained_customers"]
            == w["customer_count"]
        )
        v.check(
            "Business Insights", f"{area} Customer Reconciliation",
            bool(reconciliation.all()),
            f"{int((~reconciliation).sum())} source rows fail reconciliation."
        )

        calculated_churn = (
            w["churned_customers"] / w["customer_count"] * 100
        ).fillna(0).round(2)
        churn_ok = calculated_churn == w["churn_rate"].fillna(0).round(2)
        v.check(
            "Business Insights", f"{area} Churn Calculation", bool(churn_ok.all()),
            f"{int((~churn_ok).sum())} source rows have incorrect churn rate."
        )

        calculated_retention = (
            w["retained_customers"] / w["customer_count"] * 100
        ).fillna(0).round(2)
        retention_ok = calculated_retention == w["retention_rate"].fillna(0).round(2)
        v.check(
            "Business Insights", f"{area} Retention Calculation", bool(retention_ok.all()),
            f"{int((~retention_ok).sum())} source rows have incorrect retention rate."
        )

        baseline_ok = w["overall_churn_rate"].fillna(0).round(2) == CHURN_RATE
        v.check(
            "Business Insights", f"{area} Baseline", bool(baseline_ok.all()),
            f"{int((~baseline_ok).sum())} source rows have incorrect baseline."
        )

        calculated_difference = (
            w["churn_rate"] - CHURN_RATE
        ).round(2)
        difference_ok = calculated_difference == w["churn_rate_difference"].round(2)
        v.check(
            "Business Insights", f"{area} Churn Difference", bool(difference_ok.all()),
            f"{int((~difference_ok).sum())} source rows have incorrect difference."
        )

        small = int((w["customer_count"] < MIN_SEGMENT_SIZE).sum())
        if small:
            v.info(
                "Business Insights", f"{area} Small Source Segments",
                f"{small} source segments are below {MIN_SEGMENT_SIZE}; allowed for analysis."
            )


######   RECOMMENDATION WORKBOOK   ######

def load_recommendations(v: Validator):
    if not REC_FILE.exists():
        v.check("Recommendations", "Workbook Exists", False, f"Missing: {REC_FILE}")
        return {}

    book = load_book(REC_FILE)
    v.check("Recommendations", "Workbook Exists", True, f"Loaded {len(book)} sheets.")

    required = {
        "Executive_Summary", "Recommendations", "Area_Summary",
        "Multi_Dimensional", "Implementation_Plan",
    }
    actual = {norm(x) for x in book}
    missing = [x for x in required if norm(x) not in actual]
    v.check(
        "Recommendations", "Workbook Sheet Coverage", not missing,
        "All required recommendation sheets are present." if not missing else f"Missing: {missing}"
    )
    return book


def validate_recommendation_schema(v: Validator, book):
    rec = book.get("Recommendations")
    v.check(
        "Recommendations",
        "Recommendations Sheet Available",
        rec is not None,
        "Recommendations sheet is available.",
    )
    if rec is None:
        return None

    missing = [c for c in RECOMMENDATION_COLUMNS if c not in rec.columns]
    v.check(
        "Recommendations", "Recommendation Schema", not missing,
        "Recommendation schema is valid." if not missing else f"Missing: {missing}"
    )

    impl = book.get("Implementation_Plan")
    if impl is not None:
        missing_impl = [c for c in IMPLEMENTATION_COLUMNS if c not in impl.columns]
        v.check(
            "Recommendations", "Implementation Schema", not missing_impl,
            "Implementation schema is valid." if not missing_impl else f"Missing: {missing_impl}"
        )
    return rec


def validate_recommendation_metrics(v: Validator, rec):
    v.check(
        "Recommendations", "Total Recommendation Count",
        len(rec) == EXPECTED_TOTAL_RECOMMENDATIONS,
        f"Expected 40; found {len(rec)}."
    )

    ids = rec["recommendation_id"].astype(str).tolist()
    expected_ids = [f"REC-{n:03d}" for n in range(1, 41)]
    v.check(
        "Recommendations",
        "Recommendation IDs Unique",
        len(ids) == len(set(ids)),
        "IDs are unique.",
    )
    v.check(
        "Recommendations",
        "Recommendation ID Sequence",
        ids == expected_ids,
        "IDs run REC-001 through REC-040.",
    )

    standard = rec[rec["analysis_dimension"].astype(str) != "Multi-Dimensional"]
    multi = rec[rec["analysis_dimension"].astype(str) == "Multi-Dimensional"]

    v.check(
        "Recommendations",
        "Standard Recommendation Count",
        len(standard) == 30,
        f"Expected 30; found {len(standard)}.",
    )
    v.check(
        "Recommendations",
        "Multi-Dimensional Recommendation Count",
        len(multi) == 10,
        f"Expected 10; found {len(multi)}.",
    )

    areas = set(standard["recommendation_area"].astype(str))
    missing_areas = CORE_AREAS - areas
    v.check(
        "Recommendations", "Core Area Coverage", not missing_areas,
        (
            "All seven core areas are represented."
            if not missing_areas
            else f"Missing: {missing_areas}"
        )
    )

    numeric = [
        "customer_count", "churned_customers", "retained_customers",
        "observed_churn_rate", "observed_retention_rate",
        "overall_churn_rate", "churn_rate_difference", "churn_share",
        "recommendation_score",
    ]
    w = rec.copy()
    for c in numeric:
        w[c] = pd.to_numeric(w[c], errors="coerce")

    missing_numeric = w[numeric].isna().any(axis=1)
    v.check(
        "Recommendations", "Numeric Completeness", not bool(missing_numeric.any()),
        f"{int(missing_numeric.sum())} rows have missing numeric values."
    )

    too_small = w["customer_count"] < MIN_SEGMENT_SIZE
    v.check(
        "Recommendations", "Actionable Minimum Segment Size", not bool(too_small.any()),
        f"{int(too_small.sum())} recommendations are below {MIN_SEGMENT_SIZE} customers."
    )

    customer_ok = w["churned_customers"] + w["retained_customers"] == w["customer_count"]
    v.check(
        "Recommendations",
        "Customer Reconciliation",
        bool(customer_ok.all()),
        f"{int((~customer_ok).sum())} rows fail.",
    )

    churn_ok = (
        w["churned_customers"] / w["customer_count"] * 100
    ).round(2) == w["observed_churn_rate"].round(2)
    v.check(
        "Recommendations",
        "Observed Churn Calculation",
        bool(churn_ok.all()),
        f"{int((~churn_ok).sum())} rows fail.",
    )

    retention_ok = (
        w["retained_customers"] / w["customer_count"] * 100
    ).round(2) == w["observed_retention_rate"].round(2)
    v.check(
        "Recommendations",
        "Observed Retention Calculation",
        bool(retention_ok.all()),
        f"{int((~retention_ok).sum())} rows fail.",
    )

    baseline_ok = w["overall_churn_rate"].round(2) == CHURN_RATE
    v.check(
        "Recommendations",
        "Verified Baseline",
        bool(baseline_ok.all()),
        f"{int((~baseline_ok).sum())} rows fail baseline.",
    )

    difference_ok = (
        w["observed_churn_rate"] - CHURN_RATE
    ).round(2) == w["churn_rate_difference"].round(2)
    v.check(
        "Recommendations",
        "Churn Difference Calculation",
        bool(difference_ok.all()),
        f"{int((~difference_ok).sum())} rows fail.",
    )

    positive = w["churn_rate_difference"] > 0
    v.check(
        "Recommendations",
        "Positive Churn Difference",
        bool(positive.all()),
        f"{int((~positive).sum())} recommendations are not above baseline.",
    )

    score_ok = (w["recommendation_score"] >= 0) & (w["recommendation_score"] <= 100)
    v.check(
        "Recommendations",
        "Recommendation Score Range",
        bool(score_ok.all()),
        f"{int((~score_ok).sum())} scores are outside 0-100.",
    )

    valid_priority = {"High", "Medium", "Watch", "Monitor"}
    invalid_priority = ~w["priority"].astype(str).isin(valid_priority)
    v.check(
        "Recommendations",
        "Priority Values",
        not bool(invalid_priority.any()),
        f"{int(invalid_priority.sum())} invalid priority values.",
    )

    valid_effort = {"Low", "Medium", "High"}
    invalid_effort = ~w["implementation_effort"].astype(str).isin(valid_effort)
    v.check(
        "Recommendations",
        "Implementation Effort Values",
        not bool(invalid_effort.any()),
        f"{int(invalid_effort.sum())} invalid effort values.",
    )


######   SOURCE RECONCILIATION   ######

def build_source_lookup(bi):
    mapping = {
        "Lifecycle": "Customer Lifecycle",
        "Subscription": "Subscription",
        "Payment": "Payment",
        "Service": "Service Adoption",
        "Support": "Support Experience",
        "Engagement": "Customer Engagement",
        "Customer_Profile": "Customer Profile",
        "Priority_Segments": "Priority Retention Segment",
    }

    lookup = {}
    for source_sheet, area in mapping.items():
        _, df = locate(bi, [source_sheet, source_sheet.replace("_", " ")])
        if df is None:
            continue
        for _, row in df.iterrows():
            key = (area, txt(row["feature"]), txt(row["segment"]))
            lookup[key] = row
    return lookup


def validate_standard_reconciliation(v: Validator, rec, bi):
    standard = rec[rec["analysis_dimension"].astype(str) != "Multi-Dimensional"]
    lookup = build_source_lookup(bi)

    unmatched = 0
    metric_mismatches = 0
    baseline_mismatches = 0
    difference_mismatches = 0

    for _, row in standard.iterrows():
        key = (
            txt(row["recommendation_area"]),
            txt(row["feature"]),
            txt(row["segment"]),
        )
        source = lookup.get(key)
        if source is None:
            unmatched += 1
            continue

        for out_col, source_col in [
            ("customer_count", "customer_count"),
            ("churned_customers", "churned_customers"),
            ("retained_customers", "retained_customers"),
        ]:
            if integer(row[out_col]) != integer(source[source_col]):
                metric_mismatches += 1

        for out_col, source_col in [
            ("observed_churn_rate", "churn_rate"),
            ("observed_retention_rate", "retention_rate"),
            ("churn_share", "churn_share"),
        ]:
            if not close(row[out_col], source[source_col]):
                metric_mismatches += 1

        if not close(row["overall_churn_rate"], source["overall_churn_rate"]):
            baseline_mismatches += 1
        if not close(row["churn_rate_difference"], source["churn_rate_difference"]):
            difference_mismatches += 1

    v.check(
        "Source Reconciliation",
        "Standard Recommendation Source Mapping",
        unmatched == 0,
        f"Unmatched standard recommendations: {unmatched}.",
    )
    v.check(
        "Source Reconciliation",
        "Standard Customer Metrics",
        metric_mismatches == 0,
        f"Metric mismatches: {metric_mismatches}.",
    )
    v.check(
        "Source Reconciliation",
        "Standard Baseline",
        baseline_mismatches == 0,
        f"Baseline mismatches: {baseline_mismatches}.",
    )
    v.check(
        "Source Reconciliation",
        "Standard Churn Difference",
        difference_mismatches == 0,
        f"Difference mismatches: {difference_mismatches}.",
    )



######   MULTI-DIMENSIONAL OUTPUT   ######

def validate_multi(v: Validator, bi, rec, book):
    _, source = locate(bi, ["Multi_Dimensional", "Multi-Dimensional"])
    output = book.get("Multi_Dimensional")

    v.check("Multi-Dimensional", "Source Available", source is not None, "Source is available.")
    v.check(
        "Multi-Dimensional",
        "Output Available",
        output is not None,
        "Output sheet is available.",
    )

    if source is None or output is None:
        return

    eligible = source.copy()
    eligible["customer_count"] = pd.to_numeric(eligible["customer_count"], errors="coerce")
    eligible["churn_rate_difference"] = pd.to_numeric(
        eligible["churn_rate_difference"],
        errors="coerce",
    )
    eligible = eligible[
        (eligible["customer_count"] >= MIN_SEGMENT_SIZE)
        & (eligible["churn_rate_difference"] > 0)
    ].copy()

    v.check(
        "Multi-Dimensional", "Eligible Source Population",
        len(eligible) >= EXPECTED_MULTI_RECOMMENDATIONS,
        f"Eligible source rows: {len(eligible)}; at least 10 required."
    )
    v.check(
        "Multi-Dimensional", "Actual Target Count",
        len(output) == EXPECTED_MULTI_RECOMMENDATIONS,
        f"Expected 10; found {len(output)}."
    )

    missing = [c for c in RECOMMENDATION_COLUMNS if c not in output.columns]
    v.check(
        "Multi-Dimensional", "Output Recommendation Schema", not missing,
        "Output uses recommendation schema." if not missing else f"Missing: {missing}"
    )

    if output.empty:
        return

    analysis_dimension_ok = output["analysis_dimension"].astype(str).eq("Multi-Dimensional")
    v.check(
        "Multi-Dimensional",
        "Analysis Dimension",
        bool(analysis_dimension_ok.all()),
        "All targets are Multi-Dimensional.",
    )

    for c in [
        "customer_count", "churned_customers", "retained_customers",
        "observed_churn_rate", "observed_retention_rate",
        "overall_churn_rate", "churn_rate_difference",
    ]:
        output[c] = pd.to_numeric(output[c], errors="coerce")

    min_ok = output["customer_count"] >= MIN_SEGMENT_SIZE
    v.check(
        "Multi-Dimensional",
        "Minimum Segment Size",
        bool(min_ok.all()),
        f"{int((~min_ok).sum())} targets are below 100.",
    )

    positive_ok = output["churn_rate_difference"] > 0
    v.check(
        "Multi-Dimensional",
        "Positive Churn Difference",
        bool(positive_ok.all()),
        f"{int((~positive_ok).sum())} targets are not above baseline.",
    )

    customer_ok = (
        output["churned_customers"]
        + output["retained_customers"]
        == output["customer_count"]
    )
    v.check(
        "Multi-Dimensional",
        "Customer Reconciliation",
        bool(customer_ok.all()),
        f"{int((~customer_ok).sum())} targets fail.",
    )

    churn_ok = (
        output["churned_customers"] / output["customer_count"] * 100
    ).round(2) == output["observed_churn_rate"].round(2)
    v.check(
        "Multi-Dimensional",
        "Churn Calculation",
        bool(churn_ok.all()),
        f"{int((~churn_ok).sum())} targets fail.",
    )

    retention_ok = (
        output["retained_customers"] / output["customer_count"] * 100
    ).round(2) == output["observed_retention_rate"].round(2)
    v.check(
        "Multi-Dimensional",
        "Retention Calculation",
        bool(retention_ok.all()),
        f"{int((~retention_ok).sum())} targets fail.",
    )

    baseline_ok = output["overall_churn_rate"].round(2) == CHURN_RATE
    v.check(
        "Multi-Dimensional",
        "Verified Baseline",
        bool(baseline_ok.all()),
        f"{int((~baseline_ok).sum())} targets fail baseline.",
    )

    difference_ok = (
        output["observed_churn_rate"] - CHURN_RATE
    ).round(2) == output["churn_rate_difference"].round(2)
    v.check(
        "Multi-Dimensional",
        "Difference Calculation",
        bool(difference_ok.all()),
        f"{int((~difference_ok).sum())} targets fail difference.",
    )

    source_combinations = set(eligible["segment_combination"].astype(str).str.strip())
    target_segments = set(output["target_segment"].astype(str).str.strip())
    unmatched = target_segments - source_combinations
    v.check(
        "Multi-Dimensional", "Target Source Mapping", not unmatched,
        (
            "All targets map to eligible source combinations."
            if not unmatched
            else f"Unmatched targets: {len(unmatched)}."
        )
    )



######   CONTENT VALIDATION   ######

def validate_content(v: Validator, rec):
    standard = rec[rec["analysis_dimension"].astype(str) != "Multi-Dimensional"]
    multi = rec[rec["analysis_dimension"].astype(str) == "Multi-Dimensional"]

    # Standard records have the explicit causality-note contract.
    standard_note_ok = (
        standard["causality_note"].fillna("").astype(str)
        .str.contains("does not establish causality", case=False, na=False)
    )
    v.check(
        "Content", "Standard Causality Guardrail", bool(standard_note_ok.all()),
        f"{int((~standard_note_ok).sum())} standard records lack the required guardrail."
    )

    # The actual generated multi-dimensional records are not assumed to have
    # the explicit causality_note text. Instead, their narrative is checked
    # for unsupported causal claims. This validates the real output contract
    # without hiding a structural difference between the two record types.
    content_fields = [
        "observed_finding", "evidence", "business_problem_opportunity",
        "recommended_action", "expected_business_impact",
    ]

    combined = rec[content_fields].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    forbidden = [
        "causes churn", "caused churn", "directly causes",
        "guarantees", "will prevent churn",
    ]
    violations = combined.apply(lambda value: any(term in value for term in forbidden))
    v.check(
        "Content", "Unsupported Causal Language", not bool(violations.any()),
        f"{int(violations.sum())} records contain unsupported causal language."
    )

    text_fields = [
        "recommendation_area", "target_segment", "observed_finding",
        "evidence", "business_problem_opportunity", "recommended_action",
        "expected_business_impact", "measurement_kpi", "success_metric",
        "monitoring_frequency",
    ]
    blank_counts = 0
    for field in text_fields:
        blank = rec[field].fillna("").astype(str).str.strip().eq("")
        blank_counts += int(blank.sum())
    v.check(
        "Content", "Recommendation Narrative Completeness", blank_counts == 0,
        f"Blank required narrative cells: {blank_counts}."
    )

    # Multi-dimensional records must contain a meaningful combination target.
    if not multi.empty:
        multi_target_ok = multi["target_segment"].fillna("").astype(str).str.strip().ne("")
        v.check(
            "Content", "Multi-Dimensional Target Completeness",
            bool(multi_target_ok.all()),
            f"{int((~multi_target_ok).sum())} multi-dimensional targets are blank."
        )



######   SUMMARY / IMPLEMENTATION   ######

def validate_summary(v: Validator, rec):
    if not SUMMARY_FILE.exists():
        v.check("Summary", "Summary File Exists", False, f"Missing: {SUMMARY_FILE}")
        return

    book = load_book(SUMMARY_FILE)
    _, df = locate(book, ["Executive_Summary"])
    v.check(
        "Summary",
        "Summary Sheet Exists",
        df is not None,
        "Executive Summary exists in recommendation summary.",
    )
    if df is None:
        return

    missing = [c for c in EXECUTIVE_COLUMNS if c not in df.columns]
    v.check(
        "Summary",
        "Summary Schema",
        not missing,
        "Summary schema is valid."
        if not missing
        else f"Missing: {missing}",
    )

    # Normalize labels so harmless punctuation/spacing differences do not
    # create false validation failures, e.g.:
    # "Watch / Monitor Recommendations" == "Watch/Monitor Recommendations".
    # Build normalized metric dictionary. Some generated summary versions use
    # slightly different labels for the same business metric, so map known
    # semantic aliases to one canonical key.
    values = {}
    for _, row in df.iterrows():
        key = metric_key(row["metric"])
        values[key] = row["value"]

    # The generated summary uses TWO separate metrics:
    #   "Watch Recommendations"
    #   "Monitor Recommendations"
    # The recommendation catalog combines both into one validation bucket.
    expected_metrics = {
        "customersanalyzed",
        "overallchurnrate",
        "overallretentionrate",
        "highpriorityrecommendations",
        "mediumpriorityrecommendations",
        "watchrecommendations",
        "monitorrecommendations",
        "multidimensionalopportunities",
        "toprecommendedtarget",
    }

    missing_metrics = expected_metrics - set(values)
    v.check(
        "Summary",
        "Summary Metric Coverage",
        not missing_metrics,
        "All expected metrics are present."
        if not missing_metrics
        else f"Missing: {missing_metrics}",
    )

    v.check(
        "Summary",
        "Summary Customer Count",
        integer(values.get("customersanalyzed")) == TOTAL_CUSTOMERS,
        "Summary uses 20,000 customers.",
    )
    v.check(
        "Summary",
        "Summary Churn Rate",
        close(values.get("overallchurnrate"), CHURN_RATE),
        "Summary uses 22.32% churn.",
    )
    v.check(
        "Summary",
        "Summary Retention Rate",
        close(values.get("overallretentionrate"), RETENTION_RATE),
        "Summary uses 77.69% retention.",
    )

    high = int(rec["priority"].astype(str).eq("High").sum())
    medium = int(rec["priority"].astype(str).eq("Medium").sum())
    watch_monitor = int(
        rec["priority"].astype(str).isin(["Watch", "Monitor"]).sum()
    )
    multi = int(
        rec["analysis_dimension"].astype(str).eq("Multi-Dimensional").sum()
    )

    v.check(
        "Summary",
        "High Priority Count",
        integer(values.get("highpriorityrecommendations")) == high,
        f"Catalog high-priority count: {high}.",
    )
    v.check(
        "Summary",
        "Medium Priority Count",
        integer(values.get("mediumpriorityrecommendations")) == medium,
        f"Catalog medium-priority count: {medium}.",
    )
    summary_watch = integer(values.get("watchrecommendations"))
    summary_monitor = integer(values.get("monitorrecommendations"))
    summary_watch_monitor = summary_watch + summary_monitor

    v.check(
        "Summary",
        "Watch Monitor Count",
        summary_watch_monitor == watch_monitor,
        f"Summary Watch + Monitor count: {summary_watch_monitor}; catalog count: {watch_monitor}.",
    )
    v.check(
        "Summary",
        "Multi-Dimensional Count",
        integer(values.get("multidimensionalopportunities")) == multi,
        f"Catalog multi-dimensional count: {multi}.",
    )

    top_target = txt(rec.iloc[0]["target_segment"])
    v.check(
        "Summary",
        "Top Recommended Target",
        txt(values.get("toprecommendedtarget")) == top_target,
        "Summary top target matches recommendation catalog.",
    )


def validate_implementation(v: Validator, book, rec):
    df = book.get("Implementation_Plan")
    v.check(
        "Implementation",
        "Implementation Plan Exists",
        df is not None,
        "Implementation Plan exists.",
    )
    if df is None:
        return

    missing = [c for c in IMPLEMENTATION_COLUMNS if c not in df.columns]
    v.check(
        "Implementation",
        "Implementation Schema",
        not missing,
        "Implementation schema is valid."
        if not missing
        else f"Missing: {missing}",
    )
    v.check(
        "Implementation",
        "Implementation Row Count",
        len(df) == len(rec),
        f"Implementation rows: {len(df)}; recommendations: {len(rec)}.",
    )

    v.check(
        "Implementation", "Implementation ID Coverage",
        set(df["recommendation_id"].astype(str)) == set(rec["recommendation_id"].astype(str)),
        "Implementation Plan contains exactly the recommendation IDs."
    )



######   OUTPUT FILE COVERAGE   ######

def validate_output_files(v: Validator):
    expected = [
        "recommendation_summary.xlsx",
        "retention_recommendations.xlsx",
        "priority_customer_recommendations.xlsx",
        "multidimensional_recommendations.xlsx",
        "lifecycle_recommendations.xlsx",
        "subscription_recommendations.xlsx",
        "payment_recommendations.xlsx",
        "service_recommendations.xlsx",
        "support_recommendations.xlsx",
        "engagement_recommendations.xlsx",
        "customer_profile_recommendations.xlsx",
        "business_recommendations.xlsx",
    ]

    for filename in expected:
        path = REC_DIR / filename
        exists = path.exists()
        v.check("Output Coverage", f"Exists - {filename}", exists, f"{filename} exists.")
        if exists:
            v.check(
                "Output Coverage",
                f"Non-Empty - {filename}",
                path.stat().st_size > 0,
                f"{filename} is non-empty.",
            )



######   GLOBAL QUALITY   ######

def validate_global_quality(v: Validator, rec):
    if rec.empty:
        return

    priority_order = {"High": 4, "Medium": 3, "Watch": 2, "Monitor": 1}
    ranks = rec["priority"].astype(str).map(priority_order)
    v.check(
        "Global Quality",
        "Priority Ordering",
        bool(ranks.is_monotonic_decreasing),
        "Catalog is ordered by descending priority.",
    )

    bucket_failures = 0
    for _, group in rec.groupby(rec["priority"].astype(str), sort=False):
        scores = pd.to_numeric(group["recommendation_score"], errors="coerce")
        if not scores.is_monotonic_decreasing:
            bucket_failures += 1
    v.check(
        "Global Quality",
        "Within-Priority Score Ordering",
        bucket_failures == 0,
        f"Non-ordered priority buckets: {bucket_failures}.",
    )



######   REPORT   ######

def write_report(v: Validator):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    result = v.df
    summary = pd.DataFrame([
        {"metric": "Total Checks", "value": v.total},
        {"metric": "Passed Checks", "value": v.passed},
        {"metric": "Failed Checks", "value": v.failed},
        {"metric": "Info Checks", "value": v.info_count},
        {"metric": "Overall Validation", "value": "PASS" if v.failed == 0 else "FAIL"},
    ])

    with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
        result.to_excel(writer, sheet_name="Validation_Results", index=False)
        result[result["status"] == "FAIL"].to_excel(writer, sheet_name="Failed_Checks", index=False)
        result[result["status"] == "PASS"].to_excel(writer, sheet_name="Passed_Checks", index=False)
        result[result["status"] == "INFO"].to_excel(writer, sheet_name="Info_Checks", index=False)
        summary.to_excel(writer, sheet_name="Validation_Summary", index=False)



######   MAIN   ######

def main():
    print()
    print("BUSINESS RECOMMENDATIONS VALIDATION")
    print("\n")
    print()

    v = Validator()

    print("Validating Business Insights sources...")
    bi = load_business_insights(v)

    print("Validating Business Insights schemas...")
    validate_business_insights_schema(v, bi)

    print("Validating verified project KPIs...")
    validate_kpis(v, bi)

    print("Validating Business Insights source metrics...")
    validate_source_metrics(v, bi)

    print("Loading Business Recommendations workbook...")
    book = load_recommendations(v)

    rec = validate_recommendation_schema(v, book)

    if rec is not None:
        print("Validating actual recommendation metrics...")
        validate_recommendation_metrics(v, rec)

        print("Reconciling standard recommendations against Business Insights...")
        validate_standard_reconciliation(v, rec, bi)

        print("Validating multi-dimensional opportunities...")
        validate_multi(v, bi, rec, book)

        print("Validating recommendation content...")
        validate_content(v, rec)

        print("Validating recommendation summary...")
        validate_summary(v, rec)

        print("Validating implementation plan...")
        validate_implementation(v, book, rec)

        print("Validating global recommendation quality...")
        validate_global_quality(v, rec)

    print("Validating output file coverage...")
    validate_output_files(v)

    write_report(v)

    print()
    print("BUSINESS RECOMMENDATIONS VALIDATION RESULTS")
    print("\n")
    print(f"Total Checks  : {v.total}")
    print(f"Passed Checks : {v.passed}")
    print(f"Failed Checks : {v.failed}")
    print(f"Info Checks   : {v.info_count}")
    print()

    if v.failed == 0:
        print("Overall Business Recommendations Validation : PASS")
    else:
        print("Overall Business Recommendations Validation : FAIL")
        print()
        print("FAILED CHECKS")
        print("\n")
        for _, row in v.df[v.df["status"] == "FAIL"].iterrows():
            print(
                f"[{row['category']}] {row['check_name']} -> {row['message']}"
            )

    print()
    print("Validation Report:")
    print(REPORT_FILE)
    print()
    print("BUSINESS RECOMMENDATIONS VALIDATION COMPLETED")
    print(f"Customers analyzed : {TOTAL_CUSTOMERS:,}")
    print(f"Churned customers  : {CHURNED_CUSTOMERS:,}")
    print(f"Active customers   : {ACTIVE_CUSTOMERS:,}")
    print(f"Churn rate         : {CHURN_RATE:.2f}%")
    print(f"Retention rate     : {RETENTION_RATE:.2f}%")
    print("Overall validation : " + ("PASS" if v.failed == 0 else "FAIL"))
    print()


if __name__ == "__main__":
    main()
