"""
Churn & Retention Analysis
==========================

Purpose:
    Perform business-focused churn and retention analysis using
    the feature-engineered customer analytical dataset.

Analytical grain:
    1 row = 1 customer

Input:
    outputs/feature_engineering/customer_analytical_features.xlsx

Outputs:
    outputs/churn_analysis/

Author:
    Customer Churn & Retention Analysis Project
"""

from pathlib import Path

import numpy as np
import pandas as pd


######   PROJECT PATHS

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
    / "05_churn_analysis"
)

CHART_DIR = (
    OUTPUT_DIR
    / "charts"
)

######   REQUIRED COLUMNS 

REQUIRED_COLUMNS = {
    "customer_id",
    "churn_target",
}


######   CHURN OUTCOME / LEAKAGE COLUMNS

CHURN_OUTCOME_COLUMNS = {
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


######    COLUMN GROUPS

CUSTOMER_PROFILE_COLUMNS = [
    "gender",
    "age_group",
    "state",
    "signup_year",
    "signup_quarter",
]

SUBSCRIPTION_COLUMNS = [
    "plan",
    "plan_category",
    "contract_type",
    "contract_category",
    "monthly_charge_band",
    "tenure_segment",
]

PAYMENT_COLUMNS = [
    "primary_payment_method",
    "payment_activity_segment",
    "payment_value_segment",
    "payment_failure_flag",
    "low_payment_success_flag",
]

SERVICE_COLUMNS = [
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
    "service_adoption_segment",
]

SUPPORT_COLUMNS = [
    "support_usage_segment",
    "support_experience_segment",
    "support_risk_flag",
    "support_experience_risk",
    "high_support_usage",
    "has_unresolved_ticket",
    "has_low_satisfaction",
]

ENGAGEMENT_COLUMNS = [
    "customer_engagement_level",
    "high_value_customer",
]


######   HELPER FUNCTIONS

def load_data() -> pd.DataFrame:
    """Load feature-engineered customer dataset."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    return df


def validate_input(df: pd.DataFrame) -> None:
    """Validate basic input structure."""

    missing_columns = sorted(
        REQUIRED_COLUMNS - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Required columns are missing:\n"
            f"{missing_columns}"
        )

    if df["customer_id"].duplicated().any():
        raise ValueError(
            "Duplicate customer_id values detected."
        )

    invalid_target = ~df["churn_target"].isin([0, 1])

    if invalid_target.any():
        raise ValueError(
            "churn_target contains values other than 0 and 1."
        )


def create_output_directories() -> None:
    """Create required output directories."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def churn_rate(series: pd.Series) -> float:
    """Calculate churn rate percentage."""

    if len(series) == 0:
        return np.nan

    return round(series.mean() * 100, 2)


def retention_rate(series: pd.Series) -> float:
    """Calculate retention rate percentage."""

    if len(series) == 0:
        return np.nan

    return round((1 - series.mean()) * 100, 2)


def analyze_by_category(
    df: pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Calculate customer count, churn count, churn rate,
    and retention rate by categorical variable.
    """

    if column not in df.columns:
        return pd.DataFrame()

    temp = df[[column, "churn_target"]].copy()

    temp[column] = temp[column].fillna("Unknown")

    result = (
        temp
        .groupby(column, dropna=False)
        .agg(
            customer_count=("churn_target", "size"),
            churned_customers=("churn_target", "sum"),
            churn_rate=("churn_target", "mean"),
        )
        .reset_index()
    )

    result["retained_customers"] = (
        result["customer_count"]
        - result["churned_customers"]
    )

    result["churn_rate"] = (
        result["churn_rate"] * 100
    ).round(2)

    result["retention_rate"] = (
        100 - result["churn_rate"]
    ).round(2)

    result["churn_share"] = (
        result["churned_customers"]
        / result["churned_customers"].sum()
        * 100
    ).round(2)

    result = result.sort_values(
        by="churn_rate",
        ascending=False
    )

    return result


def analyze_numeric_by_churn(
    df: pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """Compare a numerical feature between churned and active customers."""

    if column not in df.columns:
        return pd.DataFrame()

    temp = df[[column, "churn_target"]].copy()

    temp[column] = pd.to_numeric(
        temp[column],
        errors="coerce"
    )

    result = (
        temp
        .groupby("churn_target")[column]
        .agg(
            customer_count="count",
            mean="mean",
            median="median",
            std="std",
            min="min",
            max="max",
        )
        .reset_index()
    )

    result["churn_status"] = result["churn_target"].map(
        {
            0: "Active",
            1: "Churned",
        }
    )

    result = result[
        [
            "churn_target",
            "churn_status",
            "customer_count",
            "mean",
            "median",
            "std",
            "min",
            "max",
        ]
    ]

    return result.round(2)


def create_segment_summary(
    df: pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """Create a standardized churn segment table."""

    result = analyze_by_category(
        df,
        column
    )

    if result.empty:
        return result

    result.insert(
        0,
        "segment_variable",
        column
    )

    return result


######   1. OVERALL CHURN KPI

def create_churn_kpi_summary(
    df: pd.DataFrame
) -> pd.DataFrame:

    total_customers = len(df)

    churned_customers = int(
        df["churn_target"].sum()
    )

    active_customers = (
        total_customers
        - churned_customers
    )

    churn_rate_value = (
        churned_customers
        / total_customers
        * 100
    )

    retention_rate_value = (
        active_customers
        / total_customers
        * 100
    )

    kpi = pd.DataFrame(
        [
            {
                "metric": "Total Customers",
                "value": total_customers,
            },
            {
                "metric": "Churned Customers",
                "value": churned_customers,
            },
            {
                "metric": "Active Customers",
                "value": active_customers,
            },
            {
                "metric": "Churn Rate (%)",
                "value": round(
                    churn_rate_value,
                    2
                ),
            },
            {
                "metric": "Retention Rate (%)",
                "value": round(
                    retention_rate_value,
                    2
                ),
            },
        ]
    )

    return kpi


######   2. CUSTOMER PROFILE ANALYSIS

def create_customer_profile_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in CUSTOMER_PROFILE_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   3. SUBSCRIPTION ANALYSIS

def create_subscription_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in SUBSCRIPTION_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   4. PAYMENT ANALYSIS

def create_payment_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in PAYMENT_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   5. SERVICE ANALYSIS

def create_service_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in SERVICE_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   6. SUPPORT ANALYSIS

def create_support_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in SUPPORT_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   7. ENGAGEMENT ANALYSIS

def create_engagement_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    for column in ENGAGEMENT_COLUMNS:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   8. NUMERICAL CHURN COMPARISON

def create_numerical_churn_analysis(
    df: pd.DataFrame
) -> dict:

    numerical_columns = [
        "age",
        "monthly_charge",
        "tenure_days",
        "tenure_months",
        "total_payment_count",
        "total_payment_amount",
        "payment_success_rate",
        "payment_failure_rate",
        "payments_per_month",
        "total_ticket_count",
        "average_resolution_time_hours",
        "average_satisfaction_score",
        "ticket_resolution_rate",
        "tickets_per_month",
        "service_count",
        "service_adoption_rate",
        "customer_engagement_score",
    ]

    results = {}

    for column in numerical_columns:

        result = analyze_numeric_by_churn(
            df,
            column
        )

        if not result.empty:
            results[column] = result

    return results


######   9. HIGH-RISK SEGMENT ANALYSIS

def create_risk_segment_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    analysis_columns = [
        "age_group",
        "plan_category",
        "contract_category",
        "monthly_charge_band",
        "payment_activity_segment",
        "payment_value_segment",
        "service_adoption_segment",
        "support_usage_segment",
        "support_experience_segment",
        "customer_engagement_level",
    ]

    frames = []

    for column in analysis_columns:

        result = create_segment_summary(
            df,
            column
        )

        if not result.empty:
            frames.append(result)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(
        frames,
        ignore_index=True
    )

    return combined.sort_values(
        by=[
            "churn_rate",
            "customer_count",
        ],
        ascending=[
            False,
            False,
        ]
    )


######   10. COMBINED RISK SEGMENTS

def create_combined_risk_segments(
    df: pd.DataFrame
) -> pd.DataFrame:

    combinations = [
        (
            "payment_failure_flag",
            "support_risk_flag",
        ),
        (
            "payment_failure_flag",
            "customer_engagement_level",
        ),
        (
            "service_adoption_segment",
            "customer_engagement_level",
        ),
        (
            "support_experience_segment",
            "customer_engagement_level",
        ),
        (
            "contract_category",
            "payment_activity_segment",
        ),
    ]

    frames = []

    for col1, col2 in combinations:

        if col1 not in df.columns or col2 not in df.columns:
            continue

        temp = df[
            [
                col1,
                col2,
                "churn_target",
            ]
        ].copy()

        temp[col1] = temp[col1].fillna("Unknown")
        temp[col2] = temp[col2].fillna("Unknown")

        result = (
            temp
            .groupby(
                [col1, col2],
                dropna=False
            )
            .agg(
                customer_count=("churn_target", "size"),
                churned_customers=("churn_target", "sum"),
                churn_rate=("churn_target", "mean"),
            )
            .reset_index()
        )

        result["retention_rate"] = (
            1 - result["churn_rate"]
        ) * 100

        result["churn_rate"] = (
            result["churn_rate"] * 100
        )

        result["segment_combination"] = (
            col1
            + " + "
            + col2
        )

        result = result[
            [
                "segment_combination",
                col1,
                col2,
                "customer_count",
                "churned_customers",
                "churn_rate",
                "retention_rate",
            ]
        ]

        frames.append(result)

    if not frames:
        return pd.DataFrame()

    result = pd.concat(
        frames,
        ignore_index=True
    )

    result["churn_rate"] = result[
        "churn_rate"
    ].round(2)

    result["retention_rate"] = result[
        "retention_rate"
    ].round(2)

    return result.sort_values(
        by=[
            "churn_rate",
            "customer_count",
        ],
        ascending=[
            False,
            False,
        ]
    )


######   11. DRIVER SUMMARY

def create_driver_summary(
    df: pd.DataFrame
) -> pd.DataFrame:

    categorical_columns = (
        CUSTOMER_PROFILE_COLUMNS
        + SUBSCRIPTION_COLUMNS
        + PAYMENT_COLUMNS
        + SERVICE_COLUMNS
        + SUPPORT_COLUMNS
        + ENGAGEMENT_COLUMNS
    )

    rows = []

    total_customers = len(df)

    churned_customers = int(
        df["churn_target"].sum()
    )

    overall_churn_rate = round(
        churned_customers
        / total_customers
        * 100,
        2
    )

    for column in categorical_columns:

        if column not in df.columns:
            continue

        result = analyze_by_category(
            df,
            column
        )

        if result.empty:
            continue

        for _, row in result.iterrows():

            segment_churn_rate = row[
                "churn_rate"
            ]

            rows.append(
                {
                    "feature": column,
                    "segment": row[column],
                    "customer_count": row[
                        "customer_count"
                    ],
                    "churned_customers": row[
                        "churned_customers"
                    ],
                    "churn_rate": segment_churn_rate,
                    "overall_churn_rate": round(
                        overall_churn_rate,
                        2
                    ),
                    "churn_rate_difference": round(
                        segment_churn_rate
                        - overall_churn_rate,
                        2
                    ),
                }
            )

    result = pd.DataFrame(rows)

    if result.empty:
        return result

    return result.sort_values(
        by="churn_rate_difference",
        ascending=False
    )


######   12. RETENTION ANALYSIS

def create_retention_analysis(
    df: pd.DataFrame
) -> dict:

    results = {}

    # Retention by major customer segments
    retention_columns = [
        "age_group",
        "plan_category",
        "contract_category",
        "tenure_segment",
        "payment_activity_segment",
        "service_adoption_segment",
        "support_experience_segment",
        "customer_engagement_level",
    ]

    for column in retention_columns:

        result = analyze_by_category(
            df,
            column
        )

        if not result.empty:
            results[column] = result[
                [
                    column,
                    "customer_count",
                    "churned_customers",
                    "retained_customers",
                    "churn_rate",
                    "retention_rate",
                ]
            ]

    return results


######   13. EXPORT WORKBOOK

def write_dictionary_workbook(
    results: dict,
    output_file: Path
) -> None:
    """Write dictionary of DataFrames to Excel sheets."""

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        for sheet_name, data in results.items():

            if data is None or data.empty:
                continue

            safe_sheet_name = str(
                sheet_name
            )[:31]

            data.to_excel(
                writer,
                sheet_name=safe_sheet_name,
                index=False
            )


######   MAIN

def main() -> None:

    print("CHURN & RETENTION ANALYSIS")
    print("\n")

    create_output_directories()

    print("\nLoading feature-engineered dataset...")

    df = load_data()

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns):,}"
    )

    validate_input(df)

    print("\nInput validation : PASS")

    ######   Overall KPI

    kpi_summary = create_churn_kpi_summary(
        df
    )

    kpi_summary.to_excel(
        OUTPUT_DIR / "churn_kpi_summary.xlsx",
        index=False
    )

    ######   Customer Profile

    customer_profile = (
        create_customer_profile_analysis(df)
    )

    write_dictionary_workbook(
        customer_profile,
        OUTPUT_DIR
        / "churn_by_customer_profile.xlsx"
    )

    ######   Subscription

    subscription_analysis = (
        create_subscription_analysis(df)
    )

    write_dictionary_workbook(
        subscription_analysis,
        OUTPUT_DIR
        / "churn_by_subscription.xlsx"
    )

    ######   Payment

    payment_analysis = (
        create_payment_analysis(df)
    )

    write_dictionary_workbook(
        payment_analysis,
        OUTPUT_DIR
        / "churn_by_payment.xlsx"
    )

    ######   Services

    service_analysis = (
        create_service_analysis(df)
    )

    write_dictionary_workbook(
        service_analysis,
        OUTPUT_DIR
        / "churn_by_services.xlsx"
    )

    ######   Support

    support_analysis = (
        create_support_analysis(df)
    )

    write_dictionary_workbook(
        support_analysis,
        OUTPUT_DIR
        / "churn_by_support.xlsx"
    )

    ######   Engagement

    engagement_analysis = (
        create_engagement_analysis(df)
    )

    write_dictionary_workbook(
        engagement_analysis,
        OUTPUT_DIR
        / "churn_by_engagement.xlsx"
    )

    ######   Numerical Comparison

    numerical_analysis = (
        create_numerical_churn_analysis(df)
    )

    write_dictionary_workbook(
        numerical_analysis,
        OUTPUT_DIR
        / "churn_numerical_comparison.xlsx"
    )

    ######   Risk Segments

    risk_segments = create_risk_segment_analysis(
        df
    )

    risk_segments.to_excel(
        OUTPUT_DIR
        / "churn_risk_segments.xlsx",
        index=False
    )

    ######   Combined Risk Segments

    combined_risk_segments = (
        create_combined_risk_segments(df)
    )

    combined_risk_segments.to_excel(
        OUTPUT_DIR
        / "combined_churn_risk_segments.xlsx",
        index=False
    )

    ######   Driver Summary

    driver_summary = create_driver_summary(
        df
    )

    driver_summary.to_excel(
        OUTPUT_DIR
        / "churn_driver_summary.xlsx",
        index=False
    )

    ######   Retention Analysis

    retention_analysis = create_retention_analysis(
        df
    )

    write_dictionary_workbook(
        retention_analysis,
        OUTPUT_DIR
        / "retention_analysis.xlsx"
    )

    ######   Consolidated Report

    with pd.ExcelWriter(
        OUTPUT_DIR
        / "churn_analysis_report.xlsx",
        engine="openpyxl"
    ) as writer:

        kpi_summary.to_excel(
            writer,
            sheet_name="Churn_KPIs",
            index=False
        )

        risk_segments.to_excel(
            writer,
            sheet_name="Risk_Segments",
            index=False
        )

        combined_risk_segments.to_excel(
            writer,
            sheet_name="Combined_Risk",
            index=False
        )

        driver_summary.to_excel(
            writer,
            sheet_name="Driver_Summary",
            index=False
        )

        for column, result in numerical_analysis.items():

            sheet_name = (
                "Num_"
                + column
            )[:31]

            result.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    ######   Console Summary

    total_customers = len(df)

    churned_customers = int(
        df["churn_target"].sum()
    )

    active_customers = (
        total_customers
        - churned_customers
    )

    churn_rate_value = (
        churned_customers
        / total_customers
        * 100
    )

    print("CHURN ANALYSIS COMPLETED")
    print("\n")

    print(
        f"Customers analyzed : {total_customers:,}"
    )

    print(
        f"Churned customers  : {churned_customers:,}"
    )

    print(
        f"Active customers   : {active_customers:,}"
    )

    print(
        f"Churn rate         : {churn_rate_value:.2f}%"
    )

    print(
        f"Output directory   : {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()