"""
Customer Churn & Retention Analysis
Independent Feature Engineering Validator

Purpose
-------
Independently validate the feature-engineered customer dataset.

Input
-----
outputs/final_data/final_customer_analytical_dataset.xlsx
outputs/feature_engineering/customer_analytical_features.xlsx

Output
------
outputs/validation_reports/feature_engineering_validation_report.xlsx
"""

from pathlib import Path

import numpy as np
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   FINAL DATASET SOURCE   ######

SOURCE_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "03_Final"
    / "final_customer_analytical_dataset.xlsx"
)


######   FEATURE ENGINEERING OUTPUT   ######

FEATURE_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "03_feature_engineering"
    / "customer_analytical_features.xlsx"
)


######   VALIDATION REPORT   ######

REPORT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_DIR
    / "feature_engineering_validation_report.xlsx"
)


######   UTILITY   ######

def standardize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


def add_check(
    checks,
    check_name,
    category,
    actual_value,
    expected_value,
    status,
    description,
):

    checks.append(
        {
            "Check_Name": check_name,
            "Category": category,
            "Actual_Value": actual_value,
            "Expected_Value": expected_value,
            "Status": status,
            "Description": description,
        }
    )


######   LOAD   ######

def load_datasets():

    print("FEATURE ENGINEERING VALIDATION")

    print("\nLoading validation datasets...")

    if not SOURCE_FILE.exists():

        raise FileNotFoundError(
            f"Source dataset not found:\n{SOURCE_FILE}"
        )

    if not FEATURE_FILE.exists():

        raise FileNotFoundError(
            f"Feature dataset not found:\n{FEATURE_FILE}\n\n"
            "Run feature_engineering first."
        )

    source_df = pd.read_excel(
        SOURCE_FILE
    )

    feature_df = pd.read_excel(
        FEATURE_FILE
    )

    source_df = standardize_columns(
        source_df
    )

    feature_df = standardize_columns(
        feature_df
    )

    print(
        f"Source dataset rows       : "
        f"{len(source_df):,}"
    )

    print(
        f"Source dataset columns    : "
        f"{len(source_df.columns):,}"
    )

    print(
        f"Feature dataset rows      : "
        f"{len(feature_df):,}"
    )

    print(
        f"Feature dataset columns   : "
        f"{len(feature_df.columns):,}"
    )

    return source_df, feature_df


######   VALIDATION   ######

def validate(source_df, feature_df):

    print("FEATURE ENGINEERING VALIDATION RESULTS")

    checks = []
    
    # Row Count
    
    add_check(
        checks,
        "Row Count Preserved",
        "Structure",
        len(feature_df),
        len(source_df),
        "PASS"
        if len(feature_df) == len(source_df)
        else "FAIL",
        "Feature engineering must preserve customer-level analytical grain.",
    )
    
    # Customer ID
    
    if "customer_id" in source_df.columns:

        source_ids = set(
            source_df["customer_id"]
            .dropna()
        )

        feature_ids = set(
            feature_df["customer_id"]
            .dropna()
        )

        missing_in_feature = (
            source_ids - feature_ids
        )

        unexpected_in_feature = (
            feature_ids - source_ids
        )

        add_check(
            checks,
            "Customer IDs Preserved",
            "Key Integrity",
            len(missing_in_feature),
            0,
            "PASS"
            if len(missing_in_feature) == 0
            else "FAIL",
            "No source customers should disappear.",
        )

        add_check(
            checks,
            "Unexpected Customer IDs",
            "Key Integrity",
            len(unexpected_in_feature),
            0,
            "PASS"
            if len(unexpected_in_feature) == 0
            else "FAIL",
            "Feature engineering must not create new customers.",
        )
    
    # Missing Customer IDs
    
    missing_customer_ids = int(
        feature_df["customer_id"]
        .isna()
        .sum()
    )

    add_check(
        checks,
        "Missing Customer IDs",
        "Key Integrity",
        missing_customer_ids,
        0,
        "PASS"
        if missing_customer_ids == 0
        else "FAIL",
        "Customer ID is the analytical primary key.",
    )
    
    # Duplicate Customer IDs
    
    duplicate_customer_ids = int(
        feature_df["customer_id"]
        .duplicated()
        .sum()
    )

    add_check(
        checks,
        "Duplicate Customer IDs",
        "Key Integrity",
        duplicate_customer_ids,
        0,
        "PASS"
        if duplicate_customer_ids == 0
        else "FAIL",
        "There must be exactly one row per customer.",
    )
    
    # New Features
    
    new_features = [
        column
        for column in feature_df.columns
        if column not in source_df.columns
    ]

    add_check(
        checks,
        "New Feature Columns",
        "Feature Engineering",
        len(new_features),
        "> 0",
        "PASS"
        if len(new_features) > 0
        else "FAIL",
        "Feature engineering must create analytical features.",
    )
    
    # Churn Target
    
    if "churn_target" in feature_df.columns:

        churn_target = pd.to_numeric(
            feature_df["churn_target"],
            errors="coerce",
        )

        invalid_values = (
            ~churn_target.isin([0, 1])
            & churn_target.notna()
        ).sum()

        add_check(
            checks,
            "Churn Target Values",
            "Churn Target",
            int(invalid_values),
            0,
            "PASS"
            if invalid_values == 0
            else "FAIL",
            "Churn target must contain only 0 and 1.",
        )

        churn_count = int(
            churn_target.sum()
        )

        add_check(
            checks,
            "Churn Target Count",
            "Churn Target",
            churn_count,
            4463,
            "PASS"
            if churn_count == 4463
            else "FAIL",
            "Churn target must reconcile with validated churn processing.",
        )

        active_count = int(
            (churn_target == 0).sum()
        )

        add_check(
            checks,
            "Active Target Count",
            "Churn Target",
            active_count,
            15537,
            "PASS"
            if active_count == 15537
            else "FAIL",
            "Active target count must reconcile with validated churn data.",
        )

    else:

        add_check(
            checks,
            "Churn Target Exists",
            "Churn Target",
            False,
            True,
            "FAIL",
            "A binary churn target is required for downstream analysis.",
        )
    
    # Annual Subscription Value
    
    if {
        "monthly_charge",
        "annual_subscription_value",
    }.issubset(feature_df.columns):

        monthly_charge = pd.to_numeric(
            feature_df["monthly_charge"],
            errors="coerce",
        )

        annual_value = pd.to_numeric(
            feature_df["annual_subscription_value"],
            errors="coerce",
        )

        differences = (
            annual_value
            - monthly_charge * 12
        ).abs()

        max_difference = differences.max()

        if pd.isna(max_difference):

            max_difference = 0

        add_check(
            checks,
            "Annual Subscription Value",
            "Calculation",
            round(float(max_difference), 6),
            0,
            "PASS"
            if max_difference <= 0.000001
            else "FAIL",
            "Annual subscription value must equal monthly charge × 12.",
        )
    
    # Payment Failure Flag
    
    if {
        "failed_payment_count",
        "payment_failure_flag",
    }.issubset(feature_df.columns):

        failed_count = pd.to_numeric(
            feature_df["failed_payment_count"],
            errors="coerce",
        ).fillna(0)

        expected_flag = (
            failed_count
            .gt(0)
            .astype(int)
        )

        actual_flag = pd.to_numeric(
            feature_df["payment_failure_flag"],
            errors="coerce",
        )

        mismatches = int(
            (actual_flag != expected_flag)
            .sum()
        )

        add_check(
            checks,
            "Payment Failure Flag",
            "Calculation",
            mismatches,
            0,
            "PASS"
            if mismatches == 0
            else "FAIL",
            "Payment failure flag must match failed payment count.",
        )
    
    # Service Adoption Rate
    
    if "service_adoption_rate" in feature_df.columns:

        invalid_service_rates = int(
            (
                (feature_df["service_adoption_rate"] < 0)
                |
                (feature_df["service_adoption_rate"] > 1)
            )
            .fillna(False)
            .sum()
        )

        add_check(
            checks,
            "Service Adoption Rate Range",
            "Calculation",
            invalid_service_rates,
            0,
            "PASS"
            if invalid_service_rates == 0
            else "FAIL",
            "Service adoption rate must be between 0 and 1.",
        )
    
    # Support Risk Flag
    
    if "support_risk_flag" in feature_df.columns:

        invalid_support_risk = int(
        (
            ~feature_df["support_risk_flag"].isin([0, 1])
        ).sum()
    )

        add_check(
            checks,
            "Support Risk Flag",
            "Business Logic",
            invalid_support_risk,
            0,
            "PASS"
            if invalid_support_risk == 0
            else "FAIL",
            "Support risk flag must contain only 0 or 1.",
        )
    
    # No Support Customers
    
    if {
        "total_ticket_count",
        "average_satisfaction_score",
    }.issubset(feature_df.columns):

        no_support = (
            feature_df["total_ticket_count"]
            .fillna(0)
            .eq(0)
        )

        invalid_satisfaction = int(
            feature_df.loc[
                no_support,
                "average_satisfaction_score",
            ]
            .notna()
            .sum()
        )

        add_check(
            checks,
            "No Support Satisfaction Values",
            "Missingness",
            invalid_satisfaction,
            0,
            "PASS"
            if invalid_satisfaction == 0
            else "FAIL",
            "Customers without support activity should retain "
            "missing satisfaction values.",
        )

        no_support_count = int(
            no_support.sum()
        )

        add_check(
            checks,
            "Customers Without Support",
            "Support",
            no_support_count,
            1651,
            "PASS"
            if no_support_count == 1651
            else "FAIL",
            "Support coverage must reconcile with final dataset construction.",
        )
    
    # Infinite Values
    
    numeric_df = feature_df.select_dtypes(
        include=[np.number]
    )

    infinite_count = int(
        np.isinf(
            numeric_df.to_numpy()
        ).sum()
    )

    add_check(
        checks,
        "Infinite Numeric Values",
        "Data Quality",
        infinite_count,
        0,
        "PASS"
        if infinite_count == 0
        else "FAIL",
        "Feature engineering must not create infinite numeric values.",
    )
    
    # Required Engineered Features
    
    required_features = [
        "age_group",
        "signup_year",
        "signup_month",
        "signup_quarter",
        "annual_subscription_value",
        "monthly_charge_band",
        "plan_category",
        "contract_category",
        "churn_target",
        "payment_failure_flag",
        "payment_activity_segment",
        "payment_value_segment",
        "service_count",
        "service_adoption_rate",
        "service_adoption_segment",
        "support_usage_segment",
        "support_experience_segment",
        "support_risk_flag",
        "customer_engagement_score",
        "customer_engagement_level",
        "high_value_customer",
        "low_payment_success_flag",
        "support_experience_risk",
    ]

    missing_engineered_features = [
        feature
        for feature in required_features
        if feature not in feature_df.columns
    ]

    add_check(
        checks,
        "Required Engineered Features",
        "Feature Engineering",
        len(missing_engineered_features),
        0,
        "PASS"
        if len(missing_engineered_features) == 0
        else "FAIL",
        "All required analytical features should exist.",
    )
    
    # Final Missing Values
    
    total_missing = int(
        feature_df.isna()
        .sum()
        .sum()
    )

    add_check(
        checks,
        "Total Missing Values",
        "Information",
        total_missing,
        "Expected / Context Dependent",
        "INFO",
        "Missing values are reviewed but are not automatically failures.",
    )
    
    # Feature Dataset Column Count
    
    add_check(
        checks,
        "Final Feature Column Count",
        "Information",
        len(feature_df.columns),
        "> 86",
        "INFO",
        "Feature engineering should increase the analytical feature set.",
    )

    # Summary    

    validation_df = pd.DataFrame(
        checks
    )

    passed = int(
        (
            validation_df["Status"]
            == "PASS"
        ).sum()
    )

    failed = int(
        (
            validation_df["Status"]
            == "FAIL"
        ).sum()
    )

    info = int(
        (
            validation_df["Status"]
            == "INFO"
        ).sum()
    )

    print(
        f"\nTotal Checks  : {len(validation_df)}"
    )

    print(
        f"Passed Checks : {passed}"
    )

    print(
        f"Failed Checks : {failed}"
    )

    print(
        f"Info Checks   : {info}"
    )

    overall_status = (
        "PASS"
        if failed == 0
        else "FAIL"
    )

    print(
        f"\nOverall Feature Engineering "
        f"Validation : {overall_status}"
    )

    return (
        validation_df,
        overall_status,
        new_features,
    )


######   SAVE REPORT   ######

def save_report(
    source_df,
    feature_df,
    validation_df,
    new_features,
    overall_status,
):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Source Rows",
                "Source Columns",
                "Feature Dataset Rows",
                "Feature Dataset Columns",
                "New Features",
                "Total Missing Values",
                "Overall Validation Status",
            ],
            "Value": [
                len(source_df),
                len(source_df.columns),
                len(feature_df),
                len(feature_df.columns),
                len(new_features),
                int(
                    feature_df.isna()
                    .sum()
                    .sum()
                ),
                overall_status,
            ],
        }
    )

    new_feature_df = pd.DataFrame(
        {
            "Feature": new_features,
            "Data_Type": [
                str(
                    feature_df[column]
                    .dtype
                )
                for column in new_features
            ],
            "Missing_Count": [
                int(
                    feature_df[column]
                    .isna()
                    .sum()
                )
                for column in new_features
            ],
            "Unique_Count": [
                int(
                    feature_df[column]
                    .nunique(
                        dropna=True
                    )
                )
                for column in new_features
            ],
        }
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl",
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

        validation_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False,
        )

        new_feature_df.to_excel(
            writer,
            sheet_name="New_Features",
            index=False,
        )

    print(
        f"\nValidation Report:\n"
        f"{REPORT_FILE}"
    )


######   MAIN   ######

def main():

    source_df, feature_df = (
        load_datasets()
    )

    (
        validation_df,
        overall_status,
        new_features,
    ) = validate(
        source_df,
        feature_df,
    )

    save_report(
        source_df,
        feature_df,
        validation_df,
        new_features,
        overall_status,
    )

    print("FEATURE ENGINEERING VALIDATION COMPLETED")

    print(
        f"Source rows             : "
        f"{len(source_df):,}"
    )

    print(
        f"Feature dataset rows    : "
        f"{len(feature_df):,}"
    )

    print(
        f"Feature dataset columns : "
        f"{len(feature_df.columns):,}"
    )

    print(
        f"New features            : "
        f"{len(new_features):,}"
    )

    print(
        f"Overall validation      : "
        f"{overall_status}"
    )


if __name__ == "__main__":
    main()
