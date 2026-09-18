"""
Customer Churn & Retention Analysis
Business Insights Generator

Purpose
-------
Generate a clean, deterministic, portfolio-ready business-insights layer
from the feature-engineered customer-level analytical dataset.

Input
-----
outputs/feature_engineering/customer_analytical_features.xlsx

Output directory
----------------
outputs/business_insights/

Design principles
-----------------
- Final analytical grain = 1 row per customer.
- KPI convention is deterministic:
      Churn Rate     = 4,463 / 20,000 = 22.32%
      Retention Rate = 15,537 / 20,000 = 77.69%
- Use Decimal + ROUND_HALF_UP for reported percentages.
- Never use churn outcome/leakage fields as explanatory drivers.
- Never claim causation from observational churn analysis.
- Standard actionable segments require >= 100 customers.
- Multi-dimensional opportunities require >= 100 customers.
- Priority score is calculated from the reported (2-decimal)
  churn-rate difference, making generator and validator deterministic.
"""

from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import math
import pandas as pd


###### PATHS

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

INPUT_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "03_feature_engineering"
    / "customer_analytical_features.xlsx"
)

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "07_business_insights"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


######   VERIFIED PROJECT KPI CONVENTION

EXPECTED_TOTAL_CUSTOMERS = 20_000
EXPECTED_CHURNED_CUSTOMERS = 4_463
EXPECTED_ACTIVE_CUSTOMERS = 15_537

VERIFIED_CHURN_RATE = 22.32
VERIFIED_RETENTION_RATE = 77.69

MIN_SEGMENT_SIZE = 100

HIGH_PRIORITY_CHURN_DIFFERENCE = 10.00
MEDIUM_PRIORITY_CHURN_DIFFERENCE = 5.00


######   COLUMN DEFINITIONS

CUSTOMER_KEY = "customer_id"
CHURN_COLUMN = "churn_target"

LEAKAGE_COLUMNS = {
    "churn_target",
    "churn_status",
    "churn_date",
    "is_churned",
    "is_active",
    "has_churn_date",
    "has_end_date",
    "end_date",
    "tenure_days_at_churn",
    "tenure_months_at_churn",
    "tenure_years_at_churn",
    "churn_year",
    "churn_month",
    "churn_month_name",
    "churn_quarter",
    "churn_year_month",
    "churn_timing_segment",
    "churn_data_quality_flag",
    "churn_year_engineered",
    "churn_month_engineered",
    "churn_month_name_engineered",
    "churn_quarter_engineered",
    "churn_year_month_engineered",
    "tenure_at_churn_months",
    "tenure_at_churn_years",
    "tenure_segment_engineered",
}

PROFILE_FEATURES = [
    "gender",
    "age_group",
    "city",
    "state",
]

SUBSCRIPTION_FEATURES = [
    "plan",
    "contract_type",
    "plan_category",
    "contract_category",
    "monthly_charge_band",
]

PAYMENT_FEATURES = [
    "primary_payment_method",
    "payment_activity_segment",
    "payment_value_segment",
    "payment_failure_flag",
    "low_payment_success_flag",
]

SERVICE_FEATURES = [
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
    "service_adoption_segment",
    "service_adoption_rate",
]

SUPPORT_FEATURES = [
    "support_usage_segment",
    "support_experience_segment",
    "support_risk_flag",
    "support_experience_risk",
    "has_unresolved_ticket",
    "has_low_satisfaction",
]

ENGAGEMENT_FEATURES = [
    "customer_engagement_level",
    "customer_engagement_score",
    "payment_activity_segment",
    "service_adoption_segment",
    "support_experience_segment",
]

# Explicit combinations only. This prevents accidental Cartesian explosions.
MULTI_DIMENSIONAL_COMBINATIONS = [
    ("contract_type", "payment_activity_segment"),
    ("plan", "payment_activity_segment"),
    ("contract_type", "service_adoption_segment"),
    ("plan", "service_adoption_segment"),
    ("contract_type", "support_experience_segment"),
    ("plan", "support_experience_segment"),
    ("payment_activity_segment", "service_adoption_segment"),
    ("payment_activity_segment", "support_experience_segment"),
    ("service_adoption_segment", "support_experience_segment"),
]


######   GENERAL UTILITIES

def round2(value):
    """Deterministically round a numeric value to two decimals."""
    if pd.isna(value):
        return 0.0

    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def calculate_percentage(numerator, denominator):
    """Calculate and deterministically round a percentage."""
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


def clean_value(value):
    """Return a stable string representation for categorical values."""
    if pd.isna(value):
        return "Unknown"

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "nat"}:
        return "Unknown"

    return text


def safe_numeric(series):
    """Convert a Series to numeric without raising errors."""
    return pd.to_numeric(series, errors="coerce")


def validate_input(df):
    """Validate the minimum source requirements."""
    required = {
        CUSTOMER_KEY,
        CHURN_COLUMN,
    }

    missing = sorted(required - set(df.columns))

    if missing:
        raise ValueError(
            "Feature-engineered dataset is missing required columns: "
            + ", ".join(missing)
        )

    if len(df) != EXPECTED_TOTAL_CUSTOMERS:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL_CUSTOMERS:,} customers; "
            f"found {len(df):,}."
        )

    if df[CUSTOMER_KEY].isna().any():
        raise ValueError("customer_id contains missing values.")

    if df[CUSTOMER_KEY].duplicated().any():
        raise ValueError("customer_id contains duplicate values.")

    if not set(df[CHURN_COLUMN].dropna().unique()).issubset({0, 1}):
        raise ValueError("churn_target must contain only 0/1 values.")

    return True


######   KPI

def calculate_overall_kpis(df):
    """Calculate the project-level customer and churn KPIs."""
    total = int(len(df))
    churned = int(df[CHURN_COLUMN].sum())
    active = int(total - churned)

    churn_rate = calculate_percentage(churned, total)
    retention_rate = calculate_percentage(active, total)

    return {
        "total_customers": total,
        "churned_customers": churned,
        "active_customers": active,
        "churn_rate": churn_rate,
        "retention_rate": retention_rate,
    }


######   PRIORITY / EVIDENCE

def classify_priority(customer_count, churn_rate_difference):
    """Classify an actionable segment."""
    if customer_count < MIN_SEGMENT_SIZE:
        return "Monitor"

    if churn_rate_difference >= HIGH_PRIORITY_CHURN_DIFFERENCE:
        return "High"

    if churn_rate_difference >= MEDIUM_PRIORITY_CHURN_DIFFERENCE:
        return "Medium"

    if churn_rate_difference > 0:
        return "Watch"

    return "Low"


def classify_evidence(customer_count, churn_rate_difference):
    """Classify evidence strength using both size and effect."""
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


def calculate_priority_score(churn_rate_difference, customer_count):
    """
    Deterministic priority score.

    The already-reported two-decimal churn-rate difference is used.
    This prevents floating-point/rounding disagreement with the validator.
    """
    difference = round2(churn_rate_difference)

    score = difference * math.log1p(int(customer_count))

    return round2(score)


######   BUSINESS LANGUAGE

def business_meaning(feature, segment, churn_rate, difference):
    return (
        f"{segment} customers have an observed churn rate of "
        f"{churn_rate:.2f}% versus the overall benchmark of "
        f"{VERIFIED_CHURN_RATE:.2f}%, a difference of "
        f"{difference:.2f} percentage points."
    )


def recommended_action(feature, segment):
    feature = str(feature).lower()

    if feature == "tenure_segment":
        return (
            f"Strengthen onboarding and early-life retention for "
            f"{segment} customers."
        )

    if feature in {"plan", "plan_category"}:
        return (
            f"Review value perception, pricing and retention offers for "
            f"{segment} customers."
        )

    if feature in {"contract_type", "contract_category"}:
        return (
            f"Evaluate contract-specific retention journeys and renewal "
            f"offers for {segment} customers."
        )

    if feature == "monthly_charge_band":
        return (
            f"Review pricing/value communication and targeted retention "
            f"offers for {segment} customers."
        )

    if feature == "primary_payment_method":
        return (
            f"Investigate payment-method experience and encourage reliable "
            f"payment options among {segment} customers."
        )

    if feature in {
        "payment_activity_segment",
        "payment_value_segment",
        "payment_failure_flag",
        "low_payment_success_flag",
    }:
        return (
            f"Strengthen payment engagement and proactively address payment "
            f"friction for {segment} customers."
        )

    if feature in {
        "service_adoption_segment",
        "service_adoption_rate",
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    }:
        return (
            f"Increase relevant service adoption and communicate customer "
            f"value more clearly for {segment} customers."
        )

    if feature in {
        "support_usage_segment",
        "support_experience_segment",
        "support_risk_flag",
        "support_experience_risk",
        "has_unresolved_ticket",
        "has_low_satisfaction",
    }:
        return (
            f"Prioritize proactive support follow-up and improve service "
            f"resolution experience for {segment} customers."
        )

    if feature in {
        "customer_engagement_level",
        "customer_engagement_score",
    }:
        return (
            f"Use targeted engagement campaigns to increase ongoing "
            f"customer activity among {segment} customers."
        )

    return (
        f"Investigate the customer experience and retention needs of "
        f"{segment} customers."
    )


######   GROUPED INSIGHT TABLE

def build_grouped_insight_table(df, features, category_name):
    """
    Build one insight table per analytical area.

    Only categorical/discrete features are grouped directly. Continuous
    features are included only when they already represent engineered bands
    or rates suitable for segmentation.
    """
    records = []

    for feature in features:
        if feature not in df.columns:
            continue

        work = df[[feature, CHURN_COLUMN]].copy()
        work[feature] = work[feature].map(clean_value)

        grouped = (
            work.groupby(feature, dropna=False)[CHURN_COLUMN]
            .agg(customer_count="size", churned_customers="sum")
            .reset_index()
            .rename(columns={feature: "segment"})
        )

        for row in grouped.itertuples(index=False):
            customer_count = int(row.customer_count)
            churned = int(row.churned_customers)
            retained = customer_count - churned

            churn_rate = calculate_percentage(
                churned,
                customer_count,
            )

            retention_rate = calculate_percentage(
                retained,
                customer_count,
            )

            difference = round2(
                churn_rate - VERIFIED_CHURN_RATE
            )

            priority = classify_priority(
                customer_count,
                difference,
            )

            evidence = classify_evidence(
                customer_count,
                difference,
            )

            score = calculate_priority_score(
                difference,
                customer_count,
            )

            records.append(
                {
                    "analysis_dimension": category_name,
                    "feature": feature,
                    "segment": row.segment,
                    "customer_count": customer_count,
                    "churned_customers": churned,
                    "retained_customers": retained,
                    "churn_rate": churn_rate,
                    "retention_rate": retention_rate,
                    "overall_churn_rate": VERIFIED_CHURN_RATE,
                    "churn_rate_difference": difference,
                    "churn_share": calculate_percentage(
                        churned,
                        EXPECTED_CHURNED_CUSTOMERS,
                    ),
                    "priority": priority,
                    "evidence_strength": evidence,
                    "priority_score": score,
                    "business_meaning": business_meaning(
                        feature,
                        row.segment,
                        churn_rate,
                        difference,
                    ),
                    "recommended_action": recommended_action(
                        feature,
                        row.segment,
                    ),
                }
            )

    columns = [
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

    if not records:
        return pd.DataFrame(columns=columns)

    return (
        pd.DataFrame(records)
        .sort_values(
            ["priority_score", "customer_count"],
            ascending=False,
        )
        .reset_index(drop=True)
    )


######   HIGH-VALUE CUSTOMER ANALYSIS

def build_high_value_analysis(df):
    if "high_value_customer" not in df.columns:
        return pd.DataFrame()

    work = df[["high_value_customer", CHURN_COLUMN]].copy()
    work["segment"] = work["high_value_customer"].map(clean_value)

    result = (
        work.groupby("segment", dropna=False)[CHURN_COLUMN]
        .agg(customer_count="size", churned_customers="sum")
        .reset_index()
    )

    result["retained_customers"] = (
        result["customer_count"] - result["churned_customers"]
    )

    result["churn_rate"] = result.apply(
        lambda r: calculate_percentage(
            int(r["churned_customers"]),
            int(r["customer_count"]),
        ),
        axis=1,
    )

    result["retention_rate"] = result.apply(
        lambda r: calculate_percentage(
            int(r["retained_customers"]),
            int(r["customer_count"]),
        ),
        axis=1,
    )

    result["overall_churn_rate"] = VERIFIED_CHURN_RATE

    result["churn_rate_difference"] = result["churn_rate"].map(
        lambda x: round2(x - VERIFIED_CHURN_RATE)
    )

    result["priority"] = result.apply(
        lambda r: classify_priority(
            int(r["customer_count"]),
            float(r["churn_rate_difference"]),
        ),
        axis=1,
    )

    result["priority_score"] = result.apply(
        lambda r: calculate_priority_score(
            float(r["churn_rate_difference"]),
            int(r["customer_count"]),
        ),
        axis=1,
    )

    result["evidence_strength"] = result.apply(
        lambda r: classify_evidence(
            int(r["customer_count"]),
            float(r["churn_rate_difference"]),
        ),
        axis=1,
    )

    result["business_meaning"] = (
        "Compare high-value customer churn with the verified overall "
        "churn benchmark."
    )

    result["recommended_action"] = (
        "Use differentiated retention outreach for high-value customers "
        "with elevated observed churn."
    )

    result["churn_share"] = result["churned_customers"].map(
        lambda x: calculate_percentage(
            int(x),
            EXPECTED_CHURNED_CUSTOMERS,
        )
    )

    return result[
        [
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
    ] if "feature" in result.columns else result.assign(
        feature="high_value_customer"
    )[
        [
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
    ]


######   MULTI-DIMENSIONAL RETENTION OPPORTUNITIES

def build_multidimensional_opportunities(df):
    """
    Build actionable two-dimensional combinations.

    IMPORTANT:
    Combinations with fewer than MIN_SEGMENT_SIZE customers are excluded.
    This avoids presenting unstable tiny populations as business priorities.
    """
    records = []

    for col1, col2 in MULTI_DIMENSIONAL_COMBINATIONS:
        if col1 not in df.columns or col2 not in df.columns:
            continue

        work = df[[col1, col2, CHURN_COLUMN]].copy()
        work[col1] = work[col1].map(clean_value)
        work[col2] = work[col2].map(clean_value)

        grouped = (
            work.groupby([col1, col2], dropna=False)[CHURN_COLUMN]
            .agg(customer_count="size", churned_customers="sum")
            .reset_index()
        )

        for row in grouped.itertuples(index=False):
            customer_count = int(row.customer_count)

            if customer_count < MIN_SEGMENT_SIZE:
                continue

            churned = int(row.churned_customers)
            retained = customer_count - churned

            churn_rate = calculate_percentage(
                churned,
                customer_count,
            )

            retention_rate = calculate_percentage(
                retained,
                customer_count,
            )

            difference = round2(
                churn_rate - VERIFIED_CHURN_RATE
            )

            priority = classify_priority(
                customer_count,
                difference,
            )

            evidence = classify_evidence(
                customer_count,
                difference,
            )

            score = calculate_priority_score(
                difference,
                customer_count,
            )

            segment_1 = clean_value(getattr(row, col1))
            segment_2 = clean_value(getattr(row, col2))

            records.append(
                {
                    "feature_1": col1,
                    "segment_1": segment_1,
                    "feature_2": col2,
                    "segment_2": segment_2,
                    "segment_combination": (
                        f"{col1}={segment_1} | "
                        f"{col2}={segment_2}"
                    ),
                    "customer_count": customer_count,
                    "churned_customers": churned,
                    "retained_customers": retained,
                    "churn_rate": churn_rate,
                    "retention_rate": retention_rate,
                    "overall_churn_rate": VERIFIED_CHURN_RATE,
                    "churn_rate_difference": difference,
                    "churn_share": calculate_percentage(
                        churned,
                        EXPECTED_CHURNED_CUSTOMERS,
                    ),
                    "priority": priority,
                    "evidence_strength": evidence,
                    "priority_score": score,
                    "business_meaning": (
                        f"Customers in the combination "
                        f"{col1}={segment_1} and "
                        f"{col2}={segment_2} have an observed "
                        f"churn rate of {churn_rate:.2f}% versus "
                        f"the overall benchmark of "
                        f"{VERIFIED_CHURN_RATE:.2f}%."
                    ),
                    "recommended_action": (
                        f"Use a targeted retention journey for customers "
                        f"matching {col1}={segment_1} and "
                        f"{col2}={segment_2}, subject to business "
                        f"validation and campaign feasibility."
                    ),
                }
            )

    columns = [
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

    if not records:
        return pd.DataFrame(columns=columns)

    return (
        pd.DataFrame(records)
        .sort_values(
            ["priority_score", "customer_count"],
            ascending=False,
        )
        .reset_index(drop=True)
    )


######   PRIORITY RETENTION SEGMENTS

def build_priority_segments(tables):
    frames = []

    for table in tables.values():
        if table.empty:
            continue

        selected = table[
            table["customer_count"] >= MIN_SEGMENT_SIZE
        ].copy()

        if not selected.empty:
            frames.append(selected)

    if not frames:
        return pd.DataFrame()

    result = (
        pd.concat(frames, ignore_index=True)
        .sort_values(
            ["priority_score", "customer_count"],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return result


######   INSIGHT EVIDENCE

def build_evidence(tables, multidimensional):
    """
    Consolidate positive-difference evidence.

    Every evidence record must have at least 100 customers.
    """
    frames = []

    for table in tables.values():
        if table.empty:
            continue

        selected = table[
            (table["customer_count"] >= MIN_SEGMENT_SIZE)
            & (table["churn_rate_difference"] > 0)
        ].copy()

        if not selected.empty:
            frames.append(selected)

    if not multidimensional.empty:
        selected = multidimensional[
            (multidimensional["customer_count"] >= MIN_SEGMENT_SIZE)
            & (multidimensional["churn_rate_difference"] > 0)
        ].copy()

        if not selected.empty:
            selected = selected.copy()
            selected["analysis_dimension"] = "Multi-Dimensional"
            selected["feature"] = "multi_dimensional"
            selected["segment"] = selected["segment_combination"]
            frames.append(
                selected[
                    [
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
                ]
            )

    if not frames:
        return pd.DataFrame()

    evidence = pd.concat(
        frames,
        ignore_index=True,
    )

    return (
        evidence
        .drop_duplicates(
            subset=[
                "analysis_dimension",
                "feature",
                "segment",
            ]
        )
        .sort_values(
            ["priority_score", "customer_count"],
            ascending=False,
        )
        .reset_index(drop=True)
    )


######   EXECUTIVE SUMMARY

def build_executive_summary(kpis):
    """Create the validated executive-summary schema."""
    return pd.DataFrame(
        [
            {
                "metric": "Total Customers",
                "value": kpis["total_customers"],
                "business_interpretation": (
                    "Total customer population analyzed."
                ),
            },
            {
                "metric": "Churned Customers",
                "value": kpis["churned_customers"],
                "business_interpretation": (
                    "Customers classified as churned."
                ),
            },
            {
                "metric": "Active Customers",
                "value": kpis["active_customers"],
                "business_interpretation": (
                    "Customers classified as active."
                ),
            },
            {
                "metric": "Churn Rate (%)",
                "value": kpis["churn_rate"],
                "business_interpretation": (
                    "Overall observed churn rate for the customer "
                    "population."
                ),
            },
            {
                "metric": "Retention Rate (%)",
                "value": kpis["retention_rate"],
                "business_interpretation": (
                    "Overall observed retention rate for the customer "
                    "population."
                ),
            },
        ]
    )


######   CONSOLIDATED VERIFIED INSIGHTS

def build_verified_insights(
    kpis,
    priority_segments,
    evidence,
):
    records = [
        {
            "insight_category": "Overall Churn Health",
            "finding": (
                f"The customer base has a verified churn rate of "
                f"{VERIFIED_CHURN_RATE:.2f}% and retention rate of "
                f"{VERIFIED_RETENTION_RATE:.2f}%."
            ),
            "evidence": (
                f"{EXPECTED_CHURNED_CUSTOMERS:,} churned customers out of "
                f"{EXPECTED_TOTAL_CUSTOMERS:,} analyzed customers."
            ),
            "business_meaning": (
                "Retention is a meaningful business priority because more "
                "than one-fifth of customers are classified as churned."
            ),
            "business_impact": (
                "Revenue and customer lifetime value risk."
            ),
            "priority": "High",
            "recommended_action": (
                "Prioritize targeted retention programs using the highest "
                "observed-risk customer segments."
            ),
        }
    ]

    if not priority_segments.empty:
        top = priority_segments.iloc[0]

        records.append(
            {
                "insight_category": "Top Retention Opportunity",
                "finding": (
                    f"{top['feature']} segment '{top['segment']}' has an "
                    f"observed churn rate of {top['churn_rate']:.2f}%."
                ),
                "evidence": (
                    f"{int(top['customer_count']):,} customers, "
                    f"{int(top['churned_customers']):,} churned, "
                    f"{top['churn_rate_difference']:.2f} percentage points "
                    f"above the overall benchmark."
                ),
                "business_meaning": (
                    "This is the highest-scoring actionable observed-risk "
                    "segment in the generated analysis."
                ),
                "business_impact": (
                    "Potentially meaningful retention opportunity."
                ),
                "priority": str(top["priority"]),
                "recommended_action": str(
                    top["recommended_action"]
                ),
            }
        )

    if not evidence.empty:
        records.append(
            {
                "insight_category": "Evidence Quality",
                "finding": (
                    f"{len(evidence):,} customer segments show positive "
                    "observed churn-rate differences and meet the minimum "
                    "population requirement."
                ),
                "evidence": (
                    "Evidence is filtered to segments with at least "
                    f"{MIN_SEGMENT_SIZE} customers."
                ),
                "business_meaning": (
                    "The retention opportunity list emphasizes segments "
                    "large enough for more stable descriptive analysis."
                ),
                "business_impact": (
                    "Improves prioritization quality and reduces overreaction "
                    "to very small populations."
                ),
                "priority": "High",
                "recommended_action": (
                    "Validate high-priority segments against business "
                    "context before launching retention interventions."
                ),
            }
        )

    return pd.DataFrame(records)


######   OUTPUT WRITER

def write_excel(df, path, sheet_name):
    path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:
        df.to_excel(
            writer,
            sheet_name=sheet_name[:31],
            index=False,
        )


def write_consolidated_workbook(
    executive_summary,
    lifecycle,
    subscription,
    payment,
    service,
    support,
    engagement,
    priority_segments,
    high_value,
    multidimensional,
    evidence,
    verified_insights,
):
    path = OUTPUT_DIR / "verified_business_insights.xlsx"

    sheets = {
        "Executive_Summary": executive_summary,
        "Lifecycle": lifecycle,
        "Subscription": subscription,
        "Payment": payment,
        "Service": service,
        "Support": support,
        "Engagement": engagement,
        "Priority_Segments": priority_segments,
        "High_Value": high_value,
        "Multi_Dimensional": multidimensional,
        "Insight_Evidence": evidence,
        "Verified_Insights": verified_insights,
    }

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:
        for sheet_name, frame in sheets.items():
            frame.to_excel(
                writer,
                sheet_name=sheet_name[:31],
                index=False,
            )

    return path


######   MAIN

def main():
    print("VERIFIED BUSINESS INSIGHTS")
    print("\n")
    print()
    print("Loading feature-engineered dataset...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    print(f"Rows loaded    : {len(df):,}")
    print(f"Columns loaded : {len(df.columns):,}")
    print()

    validate_input(df)
    print("Input validation : PASS")
    print()

    kpis = calculate_overall_kpis(df)

    # The dataset is expected to reproduce the verified project convention.
    if (
        kpis["total_customers"] != EXPECTED_TOTAL_CUSTOMERS
        or kpis["churned_customers"] != EXPECTED_CHURNED_CUSTOMERS
        or kpis["active_customers"] != EXPECTED_ACTIVE_CUSTOMERS
        or kpis["churn_rate"] != VERIFIED_CHURN_RATE
        or kpis["retention_rate"] != VERIFIED_RETENTION_RATE
    ):
        raise ValueError(
            "Source data does not reproduce the verified project KPI "
            "convention."
        )

    print("VERIFIED PROJECT KPI CONVENTION")
    print("\n")
    print(f"Customers analyzed : {kpis['total_customers']:,}")
    print(f"Churned customers  : {kpis['churned_customers']:,}")
    print(f"Active customers   : {kpis['active_customers']:,}")
    print(f"Churn rate         : {kpis['churn_rate']:.2f}%")
    print(f"Retention rate     : {kpis['retention_rate']:.2f}%")
    print()

    lifecycle = build_grouped_insight_table(
        df,
        ["tenure_segment_engineered"],
        "Lifecycle",
    )

    subscription = build_grouped_insight_table(
        df,
        SUBSCRIPTION_FEATURES,
        "Subscription",
    )

    payment = build_grouped_insight_table(
        df,
        PAYMENT_FEATURES,
        "Payment",
    )

    service = build_grouped_insight_table(
        df,
        SERVICE_FEATURES,
        "Service",
    )

    support = build_grouped_insight_table(
        df,
        SUPPORT_FEATURES,
        "Support",
    )

    engagement = build_grouped_insight_table(
        df,
        ENGAGEMENT_FEATURES,
        "Engagement",
    )

    profile = build_grouped_insight_table(
        df,
        PROFILE_FEATURES,
        "Customer Profile",
    )

    all_tables = {
        "Lifecycle": lifecycle,
        "Subscription": subscription,
        "Payment": payment,
        "Service": service,
        "Support": support,
        "Engagement": engagement,
        "Profile": profile,
    }

    priority_segments = build_priority_segments(
        all_tables
    )

    high_value = build_high_value_analysis(df)

    multidimensional = build_multidimensional_opportunities(
        df
    )

    evidence = build_evidence(
        all_tables,
        multidimensional,
    )

    executive_summary = build_executive_summary(
        kpis
    )

    verified_insights = build_verified_insights(
        kpis,
        priority_segments,
        evidence,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_excel(
        executive_summary,
        OUTPUT_DIR / "executive_summary.xlsx",
        "Executive_Summary",
    )

    write_excel(
        lifecycle,
        OUTPUT_DIR / "lifecycle_insights.xlsx",
        "Lifecycle",
    )

    write_excel(
        subscription,
        OUTPUT_DIR / "subscription_insights.xlsx",
        "Subscription",
    )

    write_excel(
        payment,
        OUTPUT_DIR / "payment_insights.xlsx",
        "Payment",
    )

    write_excel(
        service,
        OUTPUT_DIR / "service_insights.xlsx",
        "Service",
    )

    write_excel(
        support,
        OUTPUT_DIR / "support_insights.xlsx",
        "Support",
    )

    write_excel(
        engagement,
        OUTPUT_DIR / "engagement_insights.xlsx",
        "Engagement",
    )

    write_excel(
        profile,
        OUTPUT_DIR / "customer_profile_insights.xlsx",
        "Customer_Profile",
    )

    write_excel(
        priority_segments,
        OUTPUT_DIR / "priority_retention_segments.xlsx",
        "Priority_Segments",
    )

    write_excel(
        high_value,
        OUTPUT_DIR / "high_value_retention.xlsx",
        "High_Value",
    )

    write_excel(
        multidimensional,
        OUTPUT_DIR / "multidimensional_retention_opportunities.xlsx",
        "Multi_Dimensional",
    )

    write_excel(
        evidence,
        OUTPUT_DIR / "insight_evidence.xlsx",
        "Insight_Evidence",
    )

    write_excel(
        verified_insights,
        OUTPUT_DIR / "verified_insights.xlsx",
        "Verified_Insights",
    )

    consolidated = write_consolidated_workbook(
        executive_summary,
        lifecycle,
        subscription,
        payment,
        service,
        support,
        engagement,
        priority_segments,
        high_value,
        multidimensional,
        evidence,
        verified_insights,
    )

    print("VERIFIED BUSINESS INSIGHTS COMPLETED")
    print("\n")
    print(f"Customers analyzed : {kpis['total_customers']:,}")
    print(f"Churned customers  : {kpis['churned_customers']:,}")
    print(f"Active customers   : {kpis['active_customers']:,}")
    print(f"Churn rate         : {kpis['churn_rate']:.2f}%")
    print(f"Retention rate     : {kpis['retention_rate']:.2f}%")
    print(f"Priority segments  : {len(priority_segments):,}")
    print(f"Evidence records   : {len(evidence):,}")
    print(f"Output directory   : {OUTPUT_DIR}")
    print(f"Consolidated file  : {consolidated}")


if __name__ == "__main__":
    main()
