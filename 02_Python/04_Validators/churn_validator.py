"""
churn_validator.py

Purpose
-------
Validate churn information derived from the cleaned
Subscriptions dataset.

There is no separate Churn sheet.

Churn fields are sourced from:
    subscriptions_cleaned.xlsx

"""

from pathlib import Path
import pandas as pd

######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   CLEANED DATA   ######

CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

######   VALIDATION OUTPUT   ######

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

######   INPUT FILE   ######

INPUT_FILE = (
    CLEANED_DIR
    / "subscriptions_cleaned.xlsx"
)

######   OUTPUT FILE   ######

OUTPUT_FILE = (
    OUTPUT_DIR
    / "churn_validation_report.xlsx"
)

######   REQUIRED COLUMNS   ######

REQUIRED_COLUMNS = [
    "customer_id",
    "subscription_id",
    "start_date",
    "end_date",
    "churn_status",
    "churn_date",
]

######   CHECK FUNCTION   ######

def add_check(
    checks,
    check_name,
    result,
    value,
    notes=""
):
    checks.append(
        {
            "Check": check_name,
            "Result": result,
            "Value": value,
            "Notes": notes,
        }
    )

######   MAIN   ######

def main():

    print("CHURN VALIDATION")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"File not found:\n{INPUT_FILE}"
        )

    df = pd.read_excel(
        INPUT_FILE
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

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

    for column in [
        "start_date",
        "end_date",
        "churn_date"
    ]:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    df["churn_status"] = (
        df["churn_status"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    checks = []

    # STRUCTURE    

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    add_check(
        checks,
        "Required Churn Columns Present",
        "PASS" if not missing_columns else "FAIL",
        len(REQUIRED_COLUMNS) - len(missing_columns),
        (
            "All required columns are present."
            if not missing_columns
            else f"Missing: {missing_columns}"
        )
    )
    
    # CUSTOMER GRAIN
    
    duplicate_customers = (
        df["customer_id"]
        .duplicated()
        .sum()
    )

    add_check(
        checks,
        "Duplicate Customer IDs",
        "PASS" if duplicate_customers == 0 else "FAIL",
        duplicate_customers,
        "Expected one subscription/customer in current dataset."
    )

    # CHURN STATUS    

    valid_statuses = {
        "Active",
        "Churned"
    }

    invalid_status_count = (
        ~df["churn_status"]
        .isin(valid_statuses)
    ).sum()

    add_check(
        checks,
        "Invalid Churn Status",
        "PASS"
        if invalid_status_count == 0
        else "FAIL",
        invalid_status_count,
        "Allowed values: Active, Churned."
    )
    
    # MISSING STATUS
    
    missing_status = (
        df["churn_status"]
        .isna()
        .sum()
    )

    add_check(
        checks,
        "Missing Churn Status",
        "PASS"
        if missing_status == 0
        else "FAIL",
        missing_status,
        "Churn status is required."
    )
    
    # CHURNED WITHOUT CHURN DATE
    
    churned_without_date = (
        (df["churn_status"] == "Churned")
        & df["churn_date"].isna()
    ).sum()

    add_check(
        checks,
        "Churned Without Churn Date",
        "PASS"
        if churned_without_date == 0
        else "FAIL",
        churned_without_date,
        "Churned subscriptions should have a churn date."
    )
    
    # ACTIVE WITH CHURN DATE
    
    active_with_date = (
        (df["churn_status"] == "Active")
        & df["churn_date"].notna()
    ).sum()

    add_check(
        checks,
        "Active With Churn Date",
        "PASS"
        if active_with_date == 0
        else "FAIL",
        active_with_date,
        "Active subscriptions should not have churn dates."
    )
    
    # CHURNED WITHOUT END DATE
    
    churned_without_end = (
        (df["churn_status"] == "Churned")
        & df["end_date"].isna()
    ).sum()

    add_check(
        checks,
        "Churned Without End Date",
        "PASS"
        if churned_without_end == 0
        else "FAIL",
        churned_without_end,
        "Churned subscriptions should have an end date."
    )
    
    # CHURN DATE / END DATE CONSISTENCY
    
    comparable_dates = (
        df["churn_date"].notna()
        & df["end_date"].notna()
    )

    date_mismatch = (
        comparable_dates
        & (
            df["churn_date"]
            != df["end_date"]
        )
    ).sum()

    add_check(
        checks,
        "Churn Date vs End Date Mismatch",
        "PASS"
        if date_mismatch == 0
        else "FAIL",
        date_mismatch,
        "Churn date should match subscription end date."
    )
    
    # START / END LOGIC
    
    invalid_end_date = (
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
        "PASS"
        if invalid_end_date == 0
        else "FAIL",
        invalid_end_date,
        "End date cannot occur before start date."
    )
    
    # START / CHURN LOGIC
    
    invalid_churn_date = (
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
        "PASS"
        if invalid_churn_date == 0
        else "FAIL",
        invalid_churn_date,
        "Churn cannot occur before subscription start."
    )
    
    # CHURNED COUNT
    
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
        "Churned Records",
        "INFO",
        churned_count,
        "Number of churned subscription records."
    )

    add_check(
        checks,
        "Active Records",
        "INFO",
        active_count,
        "Number of active subscription records."
    )
    
    # UNIQUE CUSTOMERS
    
    unique_customers = (
        df["customer_id"]
        .nunique()
    )

    add_check(
        checks,
        "Unique Customers",
        "INFO",
        unique_customers,
        "Unique customer count."
    )
    
    # CHURN DATE COVERAGE
    
    churn_date_count = (
        df["churn_date"]
        .notna()
        .sum()
    )

    add_check(
        checks,
        "Records With Churn Date",
        "INFO",
        churn_date_count,
        "Records containing a churn date."
    )
    
    # RESULT SUMMARY
    
    result_df = pd.DataFrame(
        checks
    )

    total_checks = len(result_df)

    passed = (
        result_df["Result"]
        .eq("PASS")
        .sum()
    )

    failed = (
        result_df["Result"]
        .eq("FAIL")
        .sum()
    )

    info = (
        result_df["Result"]
        .eq("INFO")
        .sum()
    )

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Rows",
                "Columns",
                "Unique Customers",
                "Churned Records",
                "Active Records",
                "Total Checks",
                "Passed Checks",
                "Failed Checks",
                "Info Checks",
                "Overall Validation",
            ],
            "Value": [
                len(df),
                len(df.columns),
                unique_customers,
                churned_count,
                active_count,
                total_checks,
                passed,
                failed,
                info,
                (
                    "PASS"
                    if failed == 0
                    else "FAIL"
                ),
            ],
        }
    )
    
    # SAVE REPORT
    
    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        result_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False
        )
    
    # CONSOLE
    
    print()
    print(f"Rows                  : {len(df):,}")
    print(f"Columns               : {len(df.columns)}")
    print(f"Unique Customers      : {unique_customers:,}")
    print(f"Churned Records       : {churned_count:,}")
    print(f"Active Records        : {active_count:,}")

    print()
    print(f"Total Checks          : {total_checks}")
    print(f"Passed Checks         : {passed}")
    print(f"Failed Checks         : {failed}")
    print(f"Info Checks           : {info}")

    print()
    print("Report:")
    print(OUTPUT_FILE)

    print()
    print(
        "Overall Churn Validation: "
        + (
            "PASS"
            if failed == 0
            else "FAIL"
        )
    )
    print("\n")

if __name__ == "__main__":
    main()