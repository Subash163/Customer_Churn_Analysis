"""
churn.py

Purpose
-------
Process churn information from the cleaned Subscriptions dataset.

Important:
-----------
There is no separate Churn sheet in the source workbook.

Churn information is stored in:
    - churn_status
    - churn_date
    - end_date

This module:
    1. Loads cleaned subscriptions data
    2. Validates churn-related fields
    3. Creates customer-level churn features
    4. Performs churn consistency checks
    5. Saves the customer-level churn dataset
    6. Saves a processing/validation report

"""

from pathlib import Path

import pandas as pd


######   PROJECT PATHS  ######  

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

###### INPUT DIRECTORY   ######


CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

######   OUTPUT DIRECTORY   ######

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "04_churn_processing"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

######   INPUT FILE   ######

SUBSCRIPTIONS_FILE = (
    CLEANED_DIR
    / "subscriptions_cleaned.xlsx"
)

######   OUTPUT FILES   ######

CHURN_OUTPUT_FILE = (
    OUTPUT_DIR
    / "churn_customer_level.xlsx"
)

CHURN_REPORT_FILE = (
    OUTPUT_DIR
    / "churn_processing_report.xlsx"
)

#####   EXPECTED COLUMNS   #####  

EXPECTED_COLUMNS = [
    "customer_id",
    "subscription_id",
    "plan",
    "contract_type",
    "start_date",
    "end_date",
    "monthly_charge",
    "churn_status",
    "churn_date",
]


######   HELPER FUNCTIONS   #####  

def add_check(
    checks,
    check_name,
    result,
    value,
    category,
    notes=""
):
    """
    Add one validation check to the validation list.
    """

    checks.append(
        {
            "Check": check_name,
            "Result": result,
            "Value": value,
            "Category": category,
            "Notes": notes,
        }
    )


def load_subscriptions():
    """
    Load cleaned subscriptions data.
    """

    print("CHURN PROCESSING - DATA LOADING")
    print("\n")

    if not SUBSCRIPTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned subscriptions file not found:\n"
            f"{SUBSCRIPTIONS_FILE}"
        )

    df = pd.read_excel(
        SUBSCRIPTIONS_FILE
    )

    print(
        f"Subscriptions rows loaded : {len(df):,}"
    )

    print(
        f"Subscriptions columns     : {len(df.columns)}"
    )

    return df


def standardize_columns(df):
    """
    Standardize column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def validate_required_columns(df, checks):
    """
    Validate required columns.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    add_check(
        checks,
        "Required Columns Present",
        "PASS" if not missing_columns else "FAIL",
        len(EXPECTED_COLUMNS) - len(missing_columns),
        "Structure",
        (
            "All required columns are present."
            if not missing_columns
            else f"Missing columns: {missing_columns}"
        )
    )

    add_check(
        checks,
        "Unexpected Columns",
        "INFO",
        len(unexpected_columns),
        "Structure",
        (
            "No unexpected columns."
            if not unexpected_columns
            else f"Unexpected columns: {unexpected_columns}"
        )
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def prepare_types(df):
    """
    Convert churn-related columns into appropriate data types.
    """

    df = df.copy()

    # IDs
    for column in [
        "customer_id",
        "subscription_id"
    ]:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.upper()
        )

    # Dates
    for column in [
        "start_date",
        "end_date",
        "churn_date"
    ]:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    # Numeric
    df["monthly_charge"] = pd.to_numeric(
        df["monthly_charge"],
        errors="coerce"
    )

    # Status
    df["churn_status"] = (
        df["churn_status"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    return df


######   CHURN VALIDATION   #####  

def validate_churn_logic(df, checks):
    """
    Perform churn-specific validation checks.
    """

    ######   Basic counts

    total_rows = len(df)

    churned_count = (
        df["churn_status"]
        .eq("Churned")
        .sum()
    )

    active_count = (
        df["churn_status"]
        .eq("Active")
        .sum()
    )

    add_check(
        checks,
        "Total Subscription Records",
        "INFO",
        total_rows,
        "Summary",
        "Total records available for churn processing."
    )

    add_check(
        checks,
        "Churned Records",
        "INFO",
        churned_count,
        "Summary",
        "Records marked as Churned."
    )

    add_check(
        checks,
        "Active Records",
        "INFO",
        active_count,
        "Summary",
        "Records marked as Active."
    )

    ######   Churn Status

    valid_statuses = {
        "Active",
        "Churned"
    }

    unexpected_statuses = sorted(
        set(
            df["churn_status"]
            .dropna()
            .unique()
        ) - valid_statuses
    )

    add_check(
        checks,
        "Unexpected Churn Status Values",
        "PASS" if not unexpected_statuses else "FAIL",
        len(unexpected_statuses),
        "Churn Logic",
        (
            "Only Active and Churned statuses found."
            if not unexpected_statuses
            else f"Unexpected values: {unexpected_statuses}"
        )
    )

    ######   Missing Churn Status

    missing_status = (
        df["churn_status"]
        .isna()
        .sum()
    )

    add_check(
        checks,
        "Missing Churn Status",
        "PASS" if missing_status == 0 else "FAIL",
        missing_status,
        "Churn Logic",
        "Every subscription should have a churn status."
    )

    ######   Churned → Churn Date

    churned_missing_date = (
        (df["churn_status"] == "Churned")
        & df["churn_date"].isna()
    ).sum()

    add_check(
        checks,
        "Churned Records Missing Churn Date",
        "PASS" if churned_missing_date == 0 else "FAIL",
        churned_missing_date,
        "Churn Logic",
        "Churned subscriptions should have a churn date."
    )

    ######   Active → Churn Date

    active_with_churn_date = (
        (df["churn_status"] == "Active")
        & df["churn_date"].notna()
    ).sum()

    add_check(
        checks,
        "Active Records With Churn Date",
        "PASS" if active_with_churn_date == 0 else "FAIL",
        active_with_churn_date,
        "Churn Logic",
        "Active subscriptions should not have a churn date."
    )

    #####   Churned → End Date

    churned_missing_end_date = (
        (df["churn_status"] == "Churned")
        & df["end_date"].isna()
    ).sum()

    add_check(
        checks,
        "Churned Records Missing End Date",
        "PASS" if churned_missing_end_date == 0 else "FAIL",
        churned_missing_end_date,
        "Churn Logic",
        "Churned subscriptions should have an end date."
    )

    ######   Active → End Date

    active_with_end_date = (
        (df["churn_status"] == "Active")
        & df["end_date"].notna()
    ).sum()

    add_check(
        checks,
        "Active Records With End Date",
        "INFO",
        active_with_end_date,
        "Churn Logic",
        (
            "Normally expected to be zero, "
            "but retained for investigation rather than "
            "automatically treating as invalid."
        )
    )

    ######   Churn Date = End Date

    both_dates_available = (
        df["churn_date"].notna()
        & df["end_date"].notna()
    )

    churn_end_mismatch = (
        both_dates_available
        & (
            df["churn_date"]
            != df["end_date"]
        )
    ).sum()

    add_check(
        checks,
        "Churn Date and End Date Mismatch",
        "PASS" if churn_end_mismatch == 0 else "FAIL",
        churn_end_mismatch,
        "Churn Logic",
        "For churned subscriptions, churn date should match end date."
    )

    ######   Churn Date Before Start Date

    invalid_churn_timing = (
        df["churn_date"].notna()
        & df["start_date"].notna()
        & (
            df["churn_date"]
            < df["start_date"]
        )
    ).sum()

    add_check(
        checks,
        "Churn Date Before Start Date",
        "PASS" if invalid_churn_timing == 0 else "FAIL",
        invalid_churn_timing,
        "Date Logic",
        "Churn cannot occur before subscription start."
    )

    ######   End Date Before Start Date

    invalid_end_timing = (
        df["end_date"].notna()
        & df["start_date"].notna()
        & (
            df["end_date"]
            < df["start_date"]
        )
    ).sum()

    add_check(
        checks,
        "End Date Before Start Date",
        "PASS" if invalid_end_timing == 0 else "FAIL",
        invalid_end_timing,
        "Date Logic",
        "Subscription end cannot occur before start."
    )

    ######   Future Churn Dates

    today = pd.Timestamp.today().normalize()

    future_churn_dates = (
        df["churn_date"].notna()
        & (
            df["churn_date"]
            > today
        )
    ).sum()

    add_check(
        checks,
        "Future Churn Dates",
        "INFO",
        future_churn_dates,
        "Date Logic",
        "Future dates are retained for investigation."
    )

    ######   Duplicate Customer IDs

    duplicate_customer_ids = (
        df["customer_id"]
        .duplicated()
        .sum()
    )

    add_check(
        checks,
        "Duplicate Customer IDs",
        "PASS" if duplicate_customer_ids == 0 else "FAIL",
        duplicate_customer_ids,
        "Grain",
        "Current subscription dataset is expected to be one row per customer."
    )

    return df


#####   CUSTOMER-LEVEL CHURN DATASET   #####  

def create_customer_level_churn(df):
    """
    Create a customer-level churn analytical dataset.

    Since the current subscription data is one row per customer,
    this is primarily a feature engineering and selection step.
    """

    churn = df[
        [
            "customer_id",
            "subscription_id",
            "churn_status",
            "churn_date",
            "start_date",
            "end_date",
            "plan",
            "contract_type",
            "monthly_charge",
        ]
    ].copy()

    ######   Churn Indicator

    churn["is_churned"] = (
        churn["churn_status"]
        .eq("Churned")
        .astype(int)
    )

    ######   Active Indicator

    churn["is_active"] = (
        churn["churn_status"]
        .eq("Active")
        .astype(int)
    )

    ######   Churn Date Available

    churn["has_churn_date"] = (
        churn["churn_date"]
        .notna()
        .astype(int)
    )

    ######   End Date Available

    churn["has_end_date"] = (
        churn["end_date"]
        .notna()
        .astype(int)
    )

    ######   Tenure at Churn

    churn["tenure_days_at_churn"] = (
        churn["churn_date"]
        - churn["start_date"]
    ).dt.total_seconds() / (24 * 60 * 60)

    churn["tenure_months_at_churn"] = (
        churn["tenure_days_at_churn"]
        / 30.4375
    )

    churn["tenure_years_at_churn"] = (
        churn["tenure_days_at_churn"]
        / 365.25
    )

    ######   Active Tenure
    #
    # For active customers we do not use today as a
    # business-defined observation date.
    #
    # Instead, active tenure is calculated relative to the
    # latest date available in the subscription dataset.

    observation_date = max(
        churn["start_date"].max(),
        churn["end_date"].max()
        if churn["end_date"].notna().any()
        else churn["start_date"].max()
    )

    churn["observation_date"] = observation_date

    churn["tenure_days"] = (
        churn["churn_date"]
        .fillna(observation_date)
        - churn["start_date"]
    ).dt.total_seconds() / (24 * 60 * 60)

    churn["tenure_months"] = (
        churn["tenure_days"]
        / 30.4375
    )

    churn["tenure_years"] = (
        churn["tenure_days"]
        / 365.25
    )

    ######   Churn Year / Month

    churn["churn_year"] = (
        churn["churn_date"]
        .dt.year
        .astype("Int64")
    )

    churn["churn_month"] = (
        churn["churn_date"]
        .dt.month
        .astype("Int64")
    )

    churn["churn_month_name"] = (
        churn["churn_date"]
        .dt.month_name()
    )

    churn["churn_quarter"] = (
        churn["churn_date"]
        .dt.quarter
        .apply(
            lambda x: f"Q{x}"
            if pd.notna(x)
            else pd.NA
        )
    )

    churn["churn_year_month"] = (
        churn["churn_date"]
        .dt.to_period("M")
        .astype("string")
    )

    ######   Tenure Segment

    churn["tenure_segment"] = pd.cut(
        churn["tenure_months"],
        bins=[
            -float("inf"),
            3,
            6,
            12,
            24,
            36,
            float("inf"),
        ],
        labels=[
            "0-3 Months",
            "4-6 Months",
            "7-12 Months",
            "13-24 Months",
            "25-36 Months",
            "36+ Months",
        ],
    )

    ######   Churn Timing Segment

    churn["churn_timing_segment"] = pd.cut(
        churn["tenure_months_at_churn"],
        bins=[
            -float("inf"),
            3,
            6,
            12,
            24,
            float("inf"),
        ],
        labels=[
            "Early Churn (0-3M)",
            "Early Churn (4-6M)",
            "Mid-Term Churn (7-12M)",
            "Established Churn (13-24M)",
            "Long-Term Churn (24M+)",
        ],
    )

    ######   Churn Data Quality Flag

    churn["churn_data_quality_flag"] = "Valid"

    churn.loc[
        (
            churn["is_churned"].eq(1)
            & churn["churn_date"].isna()
        ),
        "churn_data_quality_flag"
    ] = "Churned Missing Churn Date"

    churn.loc[
        (
            churn["is_active"].eq(1)
            & churn["churn_date"].notna()
        ),
        "churn_data_quality_flag"
    ] = "Active With Churn Date"

    return churn


######   SUMMARY

def create_summary(df, checks):
    """
    Create summary information.
    """

    total_customers = (
        df["customer_id"]
        .nunique()
    )

    churned_customers = (
        df["is_churned"]
        .sum()
    )

    active_customers = (
        df["is_active"]
        .sum()
    )

    churn_rate = (
        churned_customers / total_customers * 100
        if total_customers > 0
        else 0
    )

    average_tenure_churned = (
        df.loc[
            df["is_churned"] == 1,
            "tenure_months_at_churn"
        ].mean()
    )

    summary = {
        "Metric": [
            "Total Records",
            "Unique Customers",
            "Churned Customers",
            "Active Customers",
            "Churn Rate (%)",
            "Average Tenure at Churn (Months)",
            "Minimum Tenure at Churn (Months)",
            "Maximum Tenure at Churn (Months)",
            "Customers With Churn Date",
            "Customers With End Date",
        ],
        "Value": [
            len(df),
            total_customers,
            churned_customers,
            active_customers,
            round(churn_rate, 2),
            round(average_tenure_churned, 2)
            if pd.notna(average_tenure_churned)
            else None,
            round(
                df.loc[
                    df["is_churned"] == 1,
                    "tenure_months_at_churn"
                ].min(),
                2,
            )
            if churned_customers > 0
            else None,
            round(
                df.loc[
                    df["is_churned"] == 1,
                    "tenure_months_at_churn"
                ].max(),
                2,
            )
            if churned_customers > 0
            else None,
            int(
                df["has_churn_date"].sum()
            ),
            int(
                df["has_end_date"].sum()
            ),
        ],
    }

    summary_df = pd.DataFrame(summary)

    # Validation summary
    validation_df = pd.DataFrame(checks)

    return summary_df, validation_df


######   MAIN

def main():

    print()
    print("CUSTOMER CHURN PROCESSING")
    print("\n")
    print()

    checks = []

    ######   1. Load

    df = load_subscriptions()

    original_rows = len(df)

    ######   2. Standardize

    df = standardize_columns(df)

    ######   3. Validate columns

    validate_required_columns(
        df,
        checks
    )

    ######   4. Prepare data types

    df = prepare_types(df)

    ######   5. Churn validation

    df = validate_churn_logic(
        df,
        checks
    )

    ######   6. Create customer-level churn dataset

    churn_df = create_customer_level_churn(
        df
    )

    ######   7. Summary

    summary_df, validation_df = create_summary(
        churn_df,
        checks
    )

    ######   8. Validation counts

    total_checks = len(validation_df)

    passed_checks = (
        validation_df["Result"]
        .eq("PASS")
        .sum()
    )

    failed_checks = (
        validation_df["Result"]
        .eq("FAIL")
        .sum()
    )

    info_checks = (
        validation_df["Result"]
        .eq("INFO")
        .sum()
    )

    ######   9. Processing metadata

    metadata_df = pd.DataFrame(
        {
            "Metric": [
                "Source File",
                "Original Rows",
                "Final Rows",
                "Rows Removed",
                "Total Checks",
                "Passed Checks",
                "Failed Checks",
                "Info Checks",
                "Overall Validation",
            ],
            "Value": [
                str(SUBSCRIPTIONS_FILE),
                original_rows,
                len(churn_df),
                original_rows - len(churn_df),
                total_checks,
                passed_checks,
                failed_checks,
                info_checks,
                (
                    "PASS"
                    if failed_checks == 0
                    else "FAIL"
                ),
            ],
        }
    )

    ######   10. Save churn dataset

    churn_df.to_excel(
        CHURN_OUTPUT_FILE,
        index=False
    )

    ######   11. Save report

    with pd.ExcelWriter(
        CHURN_REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        metadata_df.to_excel(
            writer,
            sheet_name="Processing_Summary",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Churn_Summary",
            index=False
        )

        validation_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False
        )

        # Churn status distribution
        status_summary = (
            churn_df["churn_status"]
            .value_counts()
            .rename_axis("Churn_Status")
            .reset_index(name="Count")
        )

        status_summary.to_excel(
            writer,
            sheet_name="Status_Distribution",
            index=False
        )

        # Churn by year
        churn_year_summary = (
            churn_df.loc[
                churn_df["is_churned"] == 1
            ]
            .groupby("churn_year")
            .size()
            .reset_index(
                name="Churned_Customers"
            )
        )

        churn_year_summary.to_excel(
            writer,
            sheet_name="Churn_By_Year",
            index=False
        )

        # Churn by plan
        churn_plan_summary = (
            churn_df.loc[
                churn_df["is_churned"] == 1
            ]
            .groupby("plan")
            .size()
            .reset_index(
                name="Churned_Customers"
            )
            .sort_values(
                "Churned_Customers",
                ascending=False
            )
        )

        churn_plan_summary.to_excel(
            writer,
            sheet_name="Churn_By_Plan",
            index=False
        )

        # Churn by contract type
        churn_contract_summary = (
            churn_df.loc[
                churn_df["is_churned"] == 1
            ]
            .groupby("contract_type")
            .size()
            .reset_index(
                name="Churned_Customers"
            )
            .sort_values(
                "Churned_Customers",
                ascending=False
            )
        )

        churn_contract_summary.to_excel(
            writer,
            sheet_name="Churn_By_Contract",
            index=False
        )

    ######   12. Console output

    print()
    print("CHURN PROCESSING COMPLETED")
    print("\n")

    print()
    print(f"Rows loaded                : {original_rows:,}")
    print(f"Customer-level rows        : {len(churn_df):,}")
    print(
        f"Unique customers           : "
        f"{churn_df['customer_id'].nunique():,}"
    )

    print(
        f"Churned customers          : "
        f"{churn_df['is_churned'].sum():,}"
    )

    print(
        f"Active customers           : "
        f"{churn_df['is_active'].sum():,}"
    )

    churn_rate_value = (
    churn_df["is_churned"].sum()
    / churn_df["customer_id"].nunique()
    * 100
    )

    print(
    f"Churn rate                 : "
    f"{churn_rate_value:.2f}%"
    )

    print()
    print(f"Total Checks               : {total_checks}")
    print(f"Passed Checks              : {passed_checks}")
    print(f"Failed Checks              : {failed_checks}")
    print(f"Info Checks                : {info_checks}")

    print()
    print("Output Dataset:")
    print(CHURN_OUTPUT_FILE)

    print()
    print("Processing Report:")
    print(CHURN_REPORT_FILE)

    print()
    print(
        "Overall Churn Processing   : "
        + (
            "PASS"
            if failed_checks == 0
            else "FAIL"
        )
    )


if __name__ == "__main__":
    main()