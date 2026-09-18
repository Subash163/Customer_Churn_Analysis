"""
Business Recommendations stage for the Customer Churn project.
"""

from __future__ import annotations

import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable

import pandas as pd

######   1. PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   2. INPUT / OUTPUT PATHS   ######

BUSINESS_INSIGHTS_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "07_business_insights"
    / "verified_business_insights.xlsx"
)

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "08_business_recommendations"
)

CONSOLIDATED_OUTPUT_FILE = (
    OUTPUT_DIR
    / "business_recommendations.xlsx"
)

RECOMMENDATION_SUMMARY_FILE = (
    OUTPUT_DIR
    / "recommendation_summary.xlsx"
)


######   3. VERIFIED PROJECT CONSTANTS   ######

EXPECTED_TOTAL_CUSTOMERS = 20_000
EXPECTED_CHURNED_CUSTOMERS = 4_463
EXPECTED_ACTIVE_CUSTOMERS = 15_537

VERIFIED_CHURN_RATE = 22.32
VERIFIED_RETENTION_RATE = 77.69

MIN_SEGMENT_SIZE = 100

HIGH_PRIORITY_CHURN_DIFFERENCE = 10.00
MEDIUM_PRIORITY_CHURN_DIFFERENCE = 5.00


######   4. STANDARD COLUMN DEFINITIONS   ######

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

EXECUTIVE_COLUMNS = [
    "metric",
    "value",
    "business_interpretation",
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


######   5. HELPER FUNCTIONS   ######

def round2(value) -> float:
    """
    Round a numeric value to two decimal places.
    """

    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )

def safe_float(value, default=0.0) -> float:
    """
    Safely convert a value to float.
    """

    try:
        return (
            default
            if pd.isna(value)
            else float(value)
        )

    except (TypeError, ValueError):
        return default


def safe_int(value, default=0) -> int:
    """
    Safely convert a value to integer.
    """

    try:
        return (
            default
            if pd.isna(value)
            else int(float(value))
        )

    except (TypeError, ValueError):
        return default


def clean_text(value) -> str:
    """
    Clean text values and convert missing values to blank strings.
    """

    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "none", "nat"}:
        return ""

    return text


def humanize(value) -> str:
    """
    Convert technical column names into readable labels.
    """

    text = (
        clean_text(value)
        .replace("_", " ")
        .replace("-", " ")
    )

    return (
        re.sub(r"\s+", " ", text)
        .strip()
        .title()
        or "Unknown"
    )


def norm_sheet(value: str) -> str:
    """
    Normalize sheet names for flexible matching.
    """

    return re.sub(
        r"[^a-z0-9]+",
        "",
        str(value).lower(),
    )


def locate_sheet(
    sheets: dict[str, pd.DataFrame],
    names: Iterable[str],
):
    """
    Locate a sheet using normalized sheet-name matching.
    """

    normalized = {
        norm_sheet(key): key
        for key in sheets
    }

    for name in names:
        actual = normalized.get(
            norm_sheet(name)
        )

        if actual is not None:
            return actual, sheets[actual]

    return None, None



######   6. LOAD BUSINESS INSIGHTS SOURCE   ######

def load_source() -> dict[str, pd.DataFrame]:
    """
    Load the verified Business Insights workbook plus the
    standalone Customer Profile insight output.

    The consolidated verified workbook contains 12 sheets and
    intentionally does not contain Customer_Profile.

    Customer Profile is produced as the separate
    customer_profile_insights.xlsx output.
    """

    if not BUSINESS_INSIGHTS_FILE.exists():
        raise FileNotFoundError(
            "Required Business Insights workbook was not found:\n"
            f"{BUSINESS_INSIGHTS_FILE}"
        )

    sheets = {
        sheet_name: pd.read_excel(
            BUSINESS_INSIGHTS_FILE,
            sheet_name=sheet_name,
        )
        for sheet_name in pd.ExcelFile(
            BUSINESS_INSIGHTS_FILE
        ).sheet_names
    }

    customer_profile_file = (
        BUSINESS_INSIGHTS_FILE.parent
        / "customer_profile_insights.xlsx"
    )

    customer_profile_exists = any(
        norm_sheet(name)
        == norm_sheet("Customer_Profile")
        for name in sheets
    )

    if not customer_profile_exists:

        if not customer_profile_file.exists():
            raise FileNotFoundError(
                "Customer Profile Business Insights output "
                "was not found.\n"
                f"Expected: {customer_profile_file}"
            )

        sheets["Customer_Profile"] = pd.read_excel(
            customer_profile_file,
            sheet_name=0,
        )

    return sheets



######   7. VALIDATE BUSINESS INSIGHTS SOURCE   ######

def validate_source(
    sheets: dict[str, pd.DataFrame],
) -> None:
    """
    Validate the structure of the Business Insights source.
    """

    _, executive = locate_sheet(
        sheets,
        [
            "Executive_Summary",
            "Executive Summary",
        ],
    )

    if executive is None:
        raise ValueError(
            "Missing Executive_Summary sheet."
        )

    missing = [
        column
        for column in EXECUTIVE_COLUMNS
        if column not in executive.columns
    ]

    if missing:
        raise ValueError(
            "Executive_Summary missing columns: "
            + ", ".join(missing)
        )

    required_areas = [
        "Lifecycle",
        "Subscription",
        "Payment",
        "Service",
        "Support",
        "Engagement",
        "Customer_Profile",
    ]

    for area in required_areas:

        _, df = locate_sheet(
            sheets,
            [
                area,
                area.replace("_", " "),
            ],
        )

        if df is None:
            raise ValueError(
                f"Missing required Business Insights sheet: {area}"
            )

        missing = [
            column
            for column in STANDARD_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"{area} missing columns: "
                + ", ".join(missing)
            )

    _, priority = locate_sheet(
        sheets,
        [
            "Priority_Segments",
            "Priority Retention Segments",
        ],
    )

    if priority is None:
        raise ValueError(
            "Missing Priority_Segments sheet."
        )

    missing = [
        column
        for column in STANDARD_COLUMNS
        if column not in priority.columns
    ]

    if missing:
        raise ValueError(
            "Priority_Segments missing columns: "
            + ", ".join(missing)
        )

    _, multi = locate_sheet(
        sheets,
        [
            "Multi_Dimensional",
            "Multi-Dimensional",
        ],
    )

    if multi is not None:

        missing = [
            column
            for column in MULTI_COLUMNS
            if column not in multi.columns
        ]

        if missing:
            raise ValueError(
                "Multi_Dimensional missing columns: "
                + ", ".join(missing)
            )



######   8. EXTRACT AND VALIDATE PROJECT KPIs   ######

def extract_kpis(
    executive: pd.DataFrame,
) -> dict[str, float | int]:
    """
    Extract verified project KPIs from Executive Summary.
    """

    values = {}

    for _, row in executive.iterrows():

        metric = clean_text(
            row["metric"]
        ).lower()

        if metric == "total customers":
            values["total_customers"] = safe_int(
                row["value"]
            )

        elif metric == "churned customers":
            values["churned_customers"] = safe_int(
                row["value"]
            )

        elif metric == "active customers":
            values["active_customers"] = safe_int(
                row["value"]
            )

        elif metric == "churn rate (%)":
            values["churn_rate"] = safe_float(
                row["value"]
            )

        elif metric == "retention rate (%)":
            values["retention_rate"] = safe_float(
                row["value"]
            )

    expected = {
        "total_customers": EXPECTED_TOTAL_CUSTOMERS,
        "churned_customers": EXPECTED_CHURNED_CUSTOMERS,
        "active_customers": EXPECTED_ACTIVE_CUSTOMERS,
        "churn_rate": VERIFIED_CHURN_RATE,
        "retention_rate": VERIFIED_RETENTION_RATE,
    }

    missing = [
        key
        for key in expected
        if key not in values
    ]

    if missing:
        raise ValueError(
            "Executive Summary missing KPIs: "
            + ", ".join(missing)
        )

    for key, expected_value in expected.items():

        actual = values[key]

        if isinstance(expected_value, float):

            if not math.isclose(
                float(actual),
                expected_value,
                abs_tol=0.01,
            ):
                raise ValueError(
                    f"Verified KPI mismatch for {key}: "
                    f"expected {expected_value}, "
                    f"found {actual}"
                )

        elif actual != expected_value:

            raise ValueError(
                f"Verified KPI mismatch for {key}: "
                f"expected {expected_value}, "
                f"found {actual}"
            )

    return values



######   9. PRIORITY FUNCTIONS   ######

def priority_rank(value: str) -> int:
    """
    Convert priority labels into ranking values.
    """

    priority_values = {
        "High": 5,
        "Medium": 4,
        "Watch": 3,
        "Low": 2,
        "Monitor": 1,
    }

    return priority_values.get(
        clean_text(value).title(),
        1,
    )


def normalize_priority(value: str) -> str:
    """
    Normalize priority labels.
    """

    value = clean_text(value).title()

    valid_priorities = {
        "High",
        "Medium",
        "Watch",
        "Low",
        "Monitor",
    }

    if value in valid_priorities:
        return value

    return "Monitor"


def recommendation_priority(
    difference: float,
    count: int,
    original: str,
) -> str:
    """
    Determine recommendation priority based on
    churn-rate difference and segment size.
    """

    if count < MIN_SEGMENT_SIZE:
        return "Monitor"

    if (
        difference >= HIGH_PRIORITY_CHURN_DIFFERENCE
        and priority_rank(original) >= 4
    ):
        return "High"

    if (
        difference >= MEDIUM_PRIORITY_CHURN_DIFFERENCE
        and priority_rank(original) >= 3
    ):
        return "Medium"

    if difference > 0:
        return "Watch"

    return "Monitor"


def recommendation_score(
    difference: float,
    count: int,
    priority: str,
) -> float:
    """
    Calculate recommendation score using:
        - churn-rate difference
        - segment scale
        - analytical priority
    """

    d = min(
        max(
            safe_float(difference),
            0.0,
        )
        / 50.0,
        1.0,
    )

    scale = min(
        math.log1p(
            max(
                safe_int(count),
                0,
            )
        )
        / math.log1p(
            EXPECTED_TOTAL_CUSTOMERS
        ),
        1.0,
    )

    p = priority_rank(priority) / 5.0

    return round2(
        (
            0.60 * d
            + 0.25 * scale
            + 0.15 * p
        )
        * 100
    )



######   10. BUSINESS RECOMMENDATION RULES   ######

RULES = {

    "Lifecycle": {
        "area": "Customer Lifecycle",
        "action": (
            "Launch a structured early-tenure retention "
            "program with onboarding touchpoints, product "
            "education, engagement prompts, and a retention "
            "check before the highest-risk tenure window."
        ),
        "impact": (
            "Reduce preventable early-life churn, improve "
            "onboarding completion, and increase the likelihood "
            "that new customers reach stable usage."
        ),
        "kpi": "Early-tenure churn rate",
        "success": (
            "Targeted segment churn rate decreases versus "
            "the pre-intervention baseline or a comparable "
            "control group."
        ),
        "frequency": "Monthly",
        "effort": "Medium",
    },

    "Subscription": {
        "area": "Subscription",
        "action": (
            "Create a targeted plan and contract retention "
            "program. Review plan value, pricing communication, "
            "contract flexibility, and renewal messaging before "
            "offering targeted incentives."
        ),
        "impact": (
            "Improve plan-value perception, reduce avoidable "
            "subscription attrition, and improve renewal or "
            "contract continuation."
        ),
        "kpi": (
            "Segment churn rate and renewal rate"
        ),
        "success": (
            "Targeted subscription segment shows lower churn "
            "and improved renewal or continuation performance."
        ),
        "frequency": "Monthly",
        "effort": "Medium",
    },

    "Payment": {
        "area": "Payment",
        "action": (
            "Introduce a payment-health retention journey for "
            "customers showing weak payment activity or "
            "payment-related risk, using reminders, failed-payment "
            "recovery, preferred-method prompts, and friction "
            "reduction."
        ),
        "impact": (
            "Reduce payment friction, recover at-risk customers "
            "earlier, and improve successful payment behavior."
        ),
        "kpi": (
            "Payment success rate and payment-risk churn rate"
        ),
        "success": (
            "Payment success improves while churn among targeted "
            "payment-risk customers declines."
        ),
        "frequency": "Weekly",
        "effort": "Medium",
    },

    "Service": {
        "area": "Service Adoption",
        "action": (
            "Build a service-adoption campaign for customers "
            "with low service utilization. Recommend relevant "
            "services, provide feature education, and measure "
            "adoption after outreach."
        ),
        "impact": (
            "Increase product or service engagement, strengthen "
            "perceived value, and create additional opportunities "
            "for retention."
        ),
        "kpi": (
            "Service adoption rate and segment churn rate"
        ),
        "success": (
            "Targeted customers increase service adoption and "
            "subsequently show lower churn than the baseline "
            "segment."
        ),
        "frequency": "Monthly",
        "effort": "Medium",
    },

    "Support": {
        "area": "Support Experience",
        "action": (
            "Create a proactive support-recovery workflow for "
            "customers with unresolved tickets, low satisfaction, "
            "or high support usage. Prioritize unresolved cases "
            "and trigger customer-care follow-up for high-risk "
            "cases."
        ),
        "impact": (
            "Improve support experience, reduce unresolved "
            "issues, and protect customers who may be vulnerable "
            "after a poor service interaction."
        ),
        "kpi": (
            "Unresolved-ticket rate and support-risk churn rate"
        ),
        "success": (
            "Resolution performance and satisfaction improve "
            "while churn among targeted support-risk customers "
            "declines."
        ),
        "frequency": "Weekly",
        "effort": "Medium",
    },

    "Engagement": {
        "area": "Customer Engagement",
        "action": (
            "Launch a targeted engagement program for "
            "low-engagement customers using relevant product "
            "education, personalized messages, usage reminders, "
            "and re-engagement journeys."
        ),
        "impact": (
            "Increase customer engagement, strengthen product "
            "value realization, and reduce churn among disengaged "
            "customers."
        ),
        "kpi": (
            "Customer engagement level and churn rate"
        ),
        "success": (
            "Targeted customers move into stronger engagement "
            "levels and show lower churn."
        ),
        "frequency": "Monthly",
        "effort": "Medium",
    },

    "Customer_Profile": {
        "area": "Customer Profile",
        "action": (
            "Use the identified customer-profile segment for "
            "targeted retention planning rather than applying "
            "one strategy to the entire customer base. Align "
            "messaging, offers, and service interventions with "
            "segment characteristics."
        ),
        "impact": (
            "Improve retention-program relevance and concentrate "
            "resources on customer groups with meaningful "
            "observed churn differences."
        ),
        "kpi": (
            "Segment churn rate and campaign response rate"
        ),
        "success": (
            "Targeted profile segment shows improved retention "
            "and measurable engagement with the intervention."
        ),
        "frequency": "Monthly",
        "effort": "Low",
    },
}



######   11. PREPARE STANDARD DATA   ######

def prepare_standard(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare standard Business Insights segment data.
    """

    out = df.copy()

    numeric = [
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

    for column in numeric:

        out[column] = (
            pd.to_numeric(
                out[column],
                errors="coerce",
            )
            .fillna(0)
        )

    for column in [
        "customer_count",
        "churned_customers",
        "retained_customers",
    ]:

        out[column] = out[column].astype(int)

    out["priority"] = (
        out["priority"]
        .map(normalize_priority)
    )

    out["recommendation_priority"] = out.apply(
        lambda row: recommendation_priority(
            row["churn_rate_difference"],
            row["customer_count"],
            row["priority"],
        ),
        axis=1,
    )

    out["recommendation_score"] = out.apply(
        lambda row: recommendation_score(
            row["churn_rate_difference"],
            row["customer_count"],
            row["priority"],
        ),
        axis=1,
    )

    out["recommendation_candidate"] = (
        (out["customer_count"] >= MIN_SEGMENT_SIZE)
        & (out["churn_rate_difference"] > 0)
    )

    return out



######   12. SELECT TOP SEGMENTS   ######

def select_top(
    df: pd.DataFrame,
    n: int,
) -> pd.DataFrame:
    """
    Select the highest-ranked actionable segments.
    """

    candidates = df.loc[
        df["recommendation_candidate"]
    ].copy()

    if candidates.empty:
        return candidates

    order = {
        "High": 4,
        "Medium": 3,
        "Watch": 2,
        "Monitor": 1,
    }

    candidates["_rank"] = (
        candidates["recommendation_priority"]
        .map(order)
        .fillna(0)
    )

    return (
        candidates
        .sort_values(
            [
                "_rank",
                "recommendation_score",
                "churn_rate_difference",
                "customer_count",
            ],
            ascending=[
                False,
                False,
                False,
                False,
            ],
        )
        .head(n)
        .drop(columns="_rank")
    )



######   13. SEGMENT LABEL   ######

def segment_label(
    row,
) -> str:
    """
    Create a readable segment label.
    """

    return (
        f"{humanize(row.get('feature', ''))}: "
        f"{clean_text(row.get('segment', '')) or 'Unknown'}"
    )



######   14. BUILD STANDARD RECOMMENDATION   ######

def build_standard_record(
    row: pd.Series,
    rule: dict,
) -> dict:

    count, churned, retained = map(
        lambda value: safe_int(row[value]),
        [
            "customer_count",
            "churned_customers",
            "retained_customers",
        ],
    )

    rate = round2(
        row["churn_rate"]
    )

    retention = round2(
        row["retention_rate"]
    )

    diff = round2(
        row["churn_rate_difference"]
    )

    share = round2(
        row["churn_share"]
    )

    original = normalize_priority(
        row["priority"]
    )

    rec_priority = recommendation_priority(
        diff,
        count,
        original,
    )

    label = segment_label(row)

    action = rule["action"]

    if diff >= HIGH_PRIORITY_CHURN_DIFFERENCE:

        action += (
            " Begin with this segment as a high-priority "
            "retention test because its observed churn "
            "difference is at least "
            f"{HIGH_PRIORITY_CHURN_DIFFERENCE:.0f} "
            "percentage points."
        )

    elif diff >= MEDIUM_PRIORITY_CHURN_DIFFERENCE:

        action += (
            " Treat this as a medium-priority retention "
            "opportunity and validate the intervention "
            "through controlled measurement."
        )

    else:

        action += (
            " Treat this as a watch-level opportunity and "
            "validate whether the pattern persists before "
            "scaling investment."
        )

    return {
        "recommendation_id": "",
        "recommendation_area": rule["area"],
        "target_segment": label,
        "analysis_dimension": clean_text(
            row.get("analysis_dimension")
        ),
        "feature": clean_text(
            row.get("feature")
        ),
        "segment": clean_text(
            row.get("segment")
        ),
        "observed_finding": (
            f"{label} contains {count:,} customers with "
            f"{churned:,} churned customers and an observed "
            f"churn rate of {rate:.2f}%, which is "
            f"{diff:.2f} percentage points above the overall "
            f"verified churn rate of "
            f"{VERIFIED_CHURN_RATE:.2f}%."
        ),
        "evidence": (
            f"Evidence strength: "
            f"{clean_text(row.get('evidence_strength')) or 'Limited'}. "
            f"Analytical priority from Business Insights: "
            f"{original}. Minimum actionable segment size is "
            f"{MIN_SEGMENT_SIZE} customers."
        ),
        "customer_count": count,
        "churned_customers": churned,
        "retained_customers": retained,
        "observed_churn_rate": rate,
        "observed_retention_rate": retention,
        "overall_churn_rate": VERIFIED_CHURN_RATE,
        "churn_rate_difference": diff,
        "churn_share": share,
        "business_problem_opportunity": (
            f"The {label} segment has a meaningful observed "
            "churn difference and therefore represents an "
            "opportunity for targeted retention testing."
        ),
        "recommended_action": action,
        "expected_business_impact": rule["impact"],
        "priority": rec_priority,
        "implementation_effort": rule["effort"],
        "recommendation_score": recommendation_score(
            diff,
            count,
            original,
        ),
        "measurement_kpi": rule["kpi"],
        "success_metric": rule["success"],
        "monitoring_frequency": rule["frequency"],
        "causality_note": (
            "This recommendation is based on an observed "
            "association in historical customer data. It does "
            "not establish causality."
        ),
    }

######   15. BUILD MULTI-DIMENSIONAL RECOMMENDATION   ######

def build_multi_record(
    row: pd.Series,
) -> dict:

    count, churned, retained = map(
        lambda value: safe_int(row[value]),
        [
            "customer_count",
            "churned_customers",
            "retained_customers",
        ],
    )

    diff, rate, retention, share = map(
        lambda value: round2(row[value]),
        [
            "churn_rate_difference",
            "churn_rate",
            "retention_rate",
            "churn_share",
        ],
    )

    priority = normalize_priority(
        row["priority"]
    )

    combo = (
        clean_text(
            row.get("segment_combination")
        )
        or
        f"{humanize(row['feature_1'])}: "
        f"{clean_text(row['segment_1'])} + "
        f"{humanize(row['feature_2'])}: "
        f"{clean_text(row['segment_2'])}"
    )

    return {
        "recommendation_id": "",
        "recommendation_area": "Priority Retention Segment",
        "target_segment": combo,
        "analysis_dimension": "Multi-Dimensional",
        "feature": (
            f"{clean_text(row['feature_1'])} + "
            f"{clean_text(row['feature_2'])}"
        ),
        "segment": combo,
        "observed_finding": (
            f"The combined segment {combo} contains "
            f"{count:,} customers with {churned:,} churned "
            f"customers and an observed churn rate of "
            f"{rate:.2f}%, {diff:.2f} percentage points above "
            "the overall verified churn rate."
        ),
        "evidence": (
            f"Evidence strength: "
            f"{clean_text(row.get('evidence_strength')) or 'Limited'}. "
            "Both dimensions are considered together. "
            f"Minimum actionable segment size is "
            f"{MIN_SEGMENT_SIZE} customers."
        ),
        "customer_count": count,
        "churned_customers": churned,
        "retained_customers": retained,
        "observed_churn_rate": rate,
        "observed_retention_rate": retention,
        "overall_churn_rate": VERIFIED_CHURN_RATE,
        "churn_rate_difference": diff,
        "churn_share": share,
        "business_problem_opportunity": (
            "Multiple observed risk characteristics overlap "
            "in this customer group, making it suitable for "
            "a coordinated retention experiment rather than "
            "isolated single-factor outreach."
        ),
        "recommended_action": (
            "Create a coordinated retention treatment for "
            "this combined segment. Prioritize the "
            "customer-journey elements represented by both "
            "dimensions, assign a clear intervention owner, "
            "and measure the segment against a baseline or "
            "control group."
        ),
        "expected_business_impact": (
            "Concentrate retention resources on customers "
            "with multiple observed risk characteristics "
            "and improve the efficiency of targeted "
            "retention activity."
        ),
        "priority": recommendation_priority(
            diff,
            count,
            priority,
        ),
        "implementation_effort": "High",
        "recommendation_score": recommendation_score(
            diff,
            count,
            priority,
        ),
        "measurement_kpi": (
            "Combined-segment churn rate and "
            "intervention response rate"
        ),
        "success_metric": (
            "The combined segment shows a meaningful "
            "reduction in subsequent churn compared with "
            "the baseline or control population."
        ),
        "monitoring_frequency": "Weekly",
        "causality_note": (
            "The combination identifies an observed "
            "high-risk segment; it does not prove that "
            "either characteristic causes churn."
        ),
    }

######   16. BUILD EXECUTIVE SUMMARY   ######

def build_executive_summary(
    kpis,
    recs,
    multi,
) -> pd.DataFrame:

    high = (
        int((recs["priority"] == "High").sum())
        if not recs.empty
        else 0
    )

    medium = (
        int((recs["priority"] == "Medium").sum())
        if not recs.empty
        else 0
    )

    watch = (
        int((recs["priority"] == "Watch").sum())
        if not recs.empty
        else 0
    )

    monitor = (
        int((recs["priority"] == "Monitor").sum())
        if not recs.empty
        else 0
    )

    top = (
        str(recs.iloc[0]["target_segment"])
        if not recs.empty
        else "No actionable segment identified"
    )

    return pd.DataFrame(
        [
            {
                "metric": "Customers Analyzed",
                "value": kpis["total_customers"],
                "business_interpretation": (
                    "Recommendations are based on the full "
                    "verified customer population."
                ),
            },
            {
                "metric": "Overall Churn Rate (%)",
                "value": kpis["churn_rate"],
                "business_interpretation": (
                    "Verified baseline used to identify "
                    "above-baseline customer segments."
                ),
            },
            {
                "metric": "Overall Retention Rate (%)",
                "value": kpis["retention_rate"],
                "business_interpretation": (
                    "Retained customers represent the core "
                    "population to protect through targeted "
                    "retention."
                ),
            },
            {
                "metric": "High-Priority Recommendations",
                "value": high,
                "business_interpretation": (
                    "These should receive the earliest "
                    "intervention design and measurement."
                ),
            },
            {
                "metric": "Medium-Priority Recommendations",
                "value": medium,
                "business_interpretation": (
                    "These should be tested after high-priority "
                    "interventions are defined."
                ),
            },
            {
                "metric": "Watch Recommendations",
                "value": watch,
                "business_interpretation": (
                    "Monitor and validate these opportunities "
                    "before significant investment."
                ),
            },
            {
                "metric": "Monitor Recommendations",
                "value": monitor,
                "business_interpretation": (
                    "These do not currently meet the stronger "
                    "evidence/action thresholds."
                ),
            },
            {
                "metric": "Multi-Dimensional Opportunities",
                "value": len(multi),
                "business_interpretation": (
                    "Overlapping observed characteristics can "
                    "support coordinated retention experiments."
                ),
            },
            {
                "metric": "Top Recommended Target",
                "value": top,
                "business_interpretation": (
                    "Highest-ranked actionable segment after "
                    "considering observed churn difference, "
                    "scale, and analytical priority."
                ),
            },
        ]
    )


######   17. WRITE EXCEL   ######

def write_excel(
    df: pd.DataFrame,
    path: Path,
    sheet: str = "Recommendations",
) -> None:
    """
    Write a DataFrame to an Excel workbook.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:

        df.to_excel(
            writer,
            sheet_name=sheet[:31],
            index=False,
        )


######   18. MAIN FUNCTION   ######

def main() -> None:

    print(
        "\nBUSINESS RECOMMENDATIONS\n"
    )

    print(
        "Loading verified Business Insights workbook..."
    )

    sheets = load_source()

    print(
        f"Sheets loaded   : {len(sheets)}"
    )

    print(
        "Validating Business Insights source structure..."
    )

    validate_source(sheets)

    print(
        "Input validation : PASS"
    )

    _, executive = locate_sheet(
        sheets,
        [
            "Executive_Summary",
            "Executive Summary",
        ],
    )

    kpis = extract_kpis(
        executive
    )

    print(
        "\nVERIFIED PROJECT KPI CONVENTION"
    )

    print(
        f"Customers analyzed : "
        f"{kpis['total_customers']:,}"
    )

    print(
        f"Churned customers  : "
        f"{kpis['churned_customers']:,}"
    )

    print(
        f"Active customers   : "
        f"{kpis['active_customers']:,}"
    )

    print(
        f"Churn rate         : "
        f"{kpis['churn_rate']:.2f}%"
    )

    print(
        f"Retention rate     : "
        f"{kpis['retention_rate']:.2f}%"
    )

    # Generate area-level recommendations

    area_recs = {}

    area_rules = [
        ("Lifecycle", "Lifecycle"),
        ("Subscription", "Subscription"),
        ("Payment", "Payment"),
        ("Service", "Service"),
        ("Support", "Support"),
        ("Engagement", "Engagement"),
        ("Customer_Profile", "Customer_Profile"),
    ]

    for sheet, rule_key in area_rules:

        print(
            f"  - {RULES[rule_key]['area']}"
        )

        _, source = locate_sheet(
            sheets,
            [
                sheet,
                sheet.replace("_", " "),
            ],
        )

        selected = select_top(
            prepare_standard(source),
            3,
        )

        if not selected.empty:

            area_recs[rule_key] = pd.DataFrame(
                [
                    build_standard_record(
                        row,
                        RULES[rule_key],
                    )
                    for _, row in selected.iterrows()
                ]
            )

        else:

            area_recs[rule_key] = pd.DataFrame()


    # Priority retention segments    

    print(
        "  - Priority Retention Segments"
    )

    _, priority_source = locate_sheet(
        sheets,
        [
            "Priority_Segments",
            "Priority Retention Segments",
        ],
    )

    priority_selected = select_top(
        prepare_standard(priority_source),
        10,
    )

    priority_rule = {
        "area": "Priority Retention Segment",
        "action": (
            "Place this segment into a targeted retention "
            "workflow. Define the customer trigger, "
            "intervention, owner, and measurement window "
            "before scaling the program."
        ),
        "impact": (
            "Improve retention-program efficiency by "
            "concentrating resources on a segment with "
            "a meaningful observed churn difference."
        ),
        "kpi": (
            "Segment churn rate and retention response"
        ),
        "success": (
            "The targeted segment shows lower subsequent "
            "churn than its baseline or control population."
        ),
        "frequency": "Weekly",
        "effort": "Medium",
    }

    if not priority_selected.empty:

        priority_recs = pd.DataFrame(
            [
                build_standard_record(
                    row,
                    priority_rule,
                )
                for _, row in priority_selected.iterrows()
            ]
        )

    else:

        priority_recs = pd.DataFrame()
 
    # Multi-dimensional retention opportunities    

    print(
        "\nGenerating multi-dimensional retention opportunities..."
    )

    _, multi_source = locate_sheet(
        sheets,
        [
            "Multi_Dimensional",
            "Multi-Dimensional",
        ],
    )

    multi_recs = pd.DataFrame()

    if (
        multi_source is not None
        and not multi_source.empty
    ):

        multi = multi_source.copy()

        numeric_columns = [
            "customer_count",
            "churned_customers",
            "retained_customers",
            "churn_rate",
            "retention_rate",
            "overall_churn_rate",
            "churn_rate_difference",
            "churn_share",
        ]

        for column in numeric_columns:

            multi[column] = (
                pd.to_numeric(
                    multi[column],
                    errors="coerce",
                )
                .fillna(0)
            )

        multi["customer_count"] = (
            multi["customer_count"]
            .astype(int)
        )

        multi["priority"] = (
            multi["priority"]
            .map(normalize_priority)
        )

        multi["candidate"] = (
            (multi["customer_count"] >= MIN_SEGMENT_SIZE)
            & (multi["churn_rate_difference"] > 0)
        )

        multi["score"] = multi.apply(
            lambda row: recommendation_score(
                row["churn_rate_difference"],
                row["customer_count"],
                row["priority"],
            ),
            axis=1,
        )

        selected = (
            multi.loc[multi["candidate"]]
            .sort_values(
                [
                    "score",
                    "churn_rate_difference",
                    "customer_count",
                ],
                ascending=[
                    False,
                    False,
                    False,
                ],
            )
            .head(10)
        )

        if not selected.empty:

            multi_recs = pd.DataFrame(
                [
                    build_multi_record(row)
                    for _, row in selected.iterrows()
                ]
            )
  
    # Combine recommendations

    frames = [
        df
        for df in (
            list(area_recs.values())
            + [
                priority_recs,
                multi_recs,
            ]
        )
        if not df.empty
    ]

    if not frames:
        raise ValueError(
            "No actionable business recommendations were generated."
        )

    recs = pd.concat(
        frames,
        ignore_index=True,
    )

    order = {
        "High": 4,
        "Medium": 3,
        "Watch": 2,
        "Monitor": 1,
    }

    recs["_rank"] = (
        recs["priority"]
        .map(order)
        .fillna(0)
    )

    recs = (
        recs
        .sort_values(
            [
                "_rank",
                "recommendation_score",
                "churn_rate_difference",
                "customer_count",
            ],
            ascending=[
                False,
                False,
                False,
                False,
            ],
        )
        .drop(columns="_rank")
        .reset_index(drop=True)
    )

    recs["recommendation_id"] = [
        f"REC-{i:03d}"
        for i in range(
            1,
            len(recs) + 1,
        )
    ]

    # Recommendation validation    

    if (
        recs["customer_count"]
        < MIN_SEGMENT_SIZE
    ).any():

        raise ValueError(
            "An actionable recommendation was generated "
            "below the minimum segment size."
        )

    if (
        recs["churn_rate_difference"]
        <= 0
    ).any():

        raise ValueError(
            "A recommendation was generated without "
            "a positive observed churn difference."
        )

    if (
        recs["overall_churn_rate"]
        .round(2)
        .ne(
            round2(
                kpis["churn_rate"]
            )
        )
    ).any():

        raise ValueError(
            "Recommendation baseline churn rate does "
            "not match the verified KPI."
        )
    
    # Build executive summary
    
    executive_summary = build_executive_summary(
        kpis,
        recs,
        multi_recs,
    )
    
    # Build area summary   

    area_summary = []

    for key, df in area_recs.items():

        area_summary.append(
            {
                "recommendation_area": RULES[key]["area"],
                "recommendation_count": len(df),
                "high_priority_count": (
                    int(
                        (df["priority"] == "High").sum()
                    )
                    if not df.empty
                    else 0
                ),
                "medium_priority_count": (
                    int(
                        (df["priority"] == "Medium").sum()
                    )
                    if not df.empty
                    else 0
                ),
                "top_target_segment": (
                    str(
                        df.iloc[0]["target_segment"]
                    )
                    if not df.empty
                    else "No actionable segment"
                ),
                "status": (
                    "High Priority Action"
                    if (
                        not df.empty
                        and (df["priority"] == "High").any()
                    )
                    else (
                        "Action Recommended"
                        if not df.empty
                        else "Monitor"
                    )
                ),
            }
        )


    area_summary.append(
        {
            "recommendation_area": (
                "Priority Retention Segments"
            ),
            "recommendation_count": len(
                priority_recs
            ),
            "high_priority_count": (
                int(
                    (
                        priority_recs["priority"]
                        == "High"
                    ).sum()
                )
                if not priority_recs.empty
                else 0
            ),
            "medium_priority_count": (
                int(
                    (
                        priority_recs["priority"]
                        == "Medium"
                    ).sum()
                )
                if not priority_recs.empty
                else 0
            ),
            "top_target_segment": (
                str(
                    priority_recs.iloc[0][
                        "target_segment"
                    ]
                )
                if not priority_recs.empty
                else "No actionable segment"
            ),
            "status": (
                "High Priority Action"
                if (
                    not priority_recs.empty
                    and (
                        priority_recs["priority"]
                        == "High"
                    ).any()
                )
                else (
                    "Action Recommended"
                    if not priority_recs.empty
                    else "Monitor"
                )
            ),
        }
    )

    area_summary = pd.DataFrame(
        area_summary
    )
  
    # Create output directory
    
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save individual output files    

    write_excel(
        executive_summary,
        RECOMMENDATION_SUMMARY_FILE,
        "Executive_Summary",
    )

    write_excel(
        recs,
        OUTPUT_DIR / "retention_recommendations.xlsx",
    )

    write_excel(
        priority_recs,
        OUTPUT_DIR / "priority_customer_recommendations.xlsx",
    )

    write_excel(
        multi_recs,
        OUTPUT_DIR / "multidimensional_recommendations.xlsx",
    )

    for key, df in area_recs.items():

        write_excel(
            df,
            OUTPUT_DIR
            / f"{key.lower()}_recommendations.xlsx",
        )

    # Implementation plan    

    implementation = recs[
        [
            "recommendation_id",
            "recommendation_area",
            "target_segment",
            "priority",
            "implementation_effort",
            "recommended_action",
            "expected_business_impact",
            "measurement_kpi",
            "success_metric",
            "monitoring_frequency",
        ]
    ]

    # Save consolidated workbook
    
    with pd.ExcelWriter(
        CONSOLIDATED_OUTPUT_FILE,
        engine="openpyxl",
    ) as writer:

        executive_summary.to_excel(
            writer,
            sheet_name="Executive_Summary",
            index=False,
        )

        recs.to_excel(
            writer,
            sheet_name="Recommendations",
            index=False,
        )

        area_summary.to_excel(
            writer,
            sheet_name="Area_Summary",
            index=False,
        )

        multi_recs.to_excel(
            writer,
            sheet_name="Multi_Dimensional",
            index=False,
        )

        implementation.to_excel(
            writer,
            sheet_name="Implementation_Plan",
            index=False,
        )
 
    # Final status
    
    print(
        "\nBUSINESS RECOMMENDATIONS COMPLETED"
    )

    print(
        f"Customers analyzed       : "
        f"{kpis['total_customers']:,}"
    )

    print(
        f"Churned customers        : "
        f"{kpis['churned_customers']:,}"
    )

    print(
        f"Active customers         : "
        f"{kpis['active_customers']:,}"
    )

    print(
        f"Verified churn rate      : "
        f"{kpis['churn_rate']:.2f}%"
    )

    print(
        f"Verified retention rate  : "
        f"{kpis['retention_rate']:.2f}%"
    )

    print(
        f"Recommendations generated: "
        f"{len(recs):,}"
    )

    print(
        f"Multi-dimensional targets: "
        f"{len(multi_recs):,}"
    )

    print(
        f"Output directory         : "
        f"{OUTPUT_DIR}"
    )

    print(
        f"Consolidated file        : "
        f"{CONSOLIDATED_OUTPUT_FILE}"
    )

    print(
        "Business Recommendations : PASS\n"
    )

######   19. PROGRAM ENTRY POINT   ######

if __name__ == "__main__":
    main()