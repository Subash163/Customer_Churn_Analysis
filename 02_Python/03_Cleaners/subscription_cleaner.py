import pandas as pd

from cleaning_utils import (
    standardize_column_names,
    strip_text_columns,
    convert_blank_to_na,
    add_cleaning_report
)

######   EXPECTED SUBSCRIPTION COLUMNS   ######

SUBSCRIPTION_COLUMNS = [
    "customer_id",
    "subscription_id",
    "plan",
    "contract_type",
    "start_date",
    "end_date",
    "monthly_charge",
    "churn_status",
    "churn_date"
]

# NUMERIC COLUMNS

SUBSCRIPTION_NUMERIC_COLUMNS = [
    "monthly_charge"
]

# DATE COLUMNS

SUBSCRIPTION_DATE_COLUMNS = [
    "start_date",
    "end_date",
    "churn_date"
]

# VALID CATEGORIES

VALID_PLAN_VALUES = {
    "basic",
    "standard",
    "premium"
}

VALID_CONTRACT_VALUES = {
    "monthly",
    "one year",
    "two year"
}

VALID_CHURN_STATUS_VALUES = {
    "active",
    "churned"
}

######   1. CLEAN CUSTOMER ID   ######

def clean_customer_id(df, report):

    print("\nSTEP 3 - Cleaning Customer ID")

    if "customer_id" not in df.columns:
        return df, report

    # Convert to string
    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Blank values
    blank_mask = (
        df["customer_id"]
        .isna()
        |
        df["customer_id"].eq("")
    )

    blank_count = blank_mask.sum()

    if blank_count > 0:

        add_cleaning_report(
            report=report,
            step="Customer ID Cleaning",
            column="customer_id",
            issue="Missing or blank customer ID",
            records_affected=int(blank_count),
            action="Retained as missing for investigation"
        )

    return df, report

######   2. CLEAN SUBSCRIPTION ID   ######

def clean_subscription_id(df, report):

    print("\nSTEP 4 - Cleaning Subscription ID")

    if "subscription_id" not in df.columns:
        return df, report

    df["subscription_id"] = (
        df["subscription_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    blank_mask = (
        df["subscription_id"]
        .isna()
        |
        df["subscription_id"].eq("")
    )

    blank_count = blank_mask.sum()

    if blank_count > 0:

        add_cleaning_report(
            report=report,
            step="Subscription ID Cleaning",
            column="subscription_id",
            issue="Missing or blank subscription ID",
            records_affected=int(blank_count),
            action="Retained as missing for investigation"
        )

    return df, report

######   3. CHECK DUPLICATE SUBSCRIPTION IDs   ######

def check_duplicate_subscription_ids(df, report):

    print("\nSTEP 5 - Checking duplicate Subscription IDs")

    if "subscription_id" not in df.columns:
        return df, report

    duplicate_mask = (
        df["subscription_id"].duplicated(
            keep=False
        )
        &
        df["subscription_id"].notna()
    )

    duplicate_count = duplicate_mask.sum()

    if duplicate_count > 0:

        add_cleaning_report(
            report=report,
            step="Duplicate Check",
            column="subscription_id",
            issue="Duplicate subscription IDs found",
            records_affected=int(duplicate_count),
            action="Duplicates retained for investigation"
        )

    return df, report

######   4. STANDARDIZE PLAN   ######

def standardize_plan(df, report):

    print("\nSTEP 6 - Standardizing Plan")

    if "plan" not in df.columns:
        return df, report

    before = (
        df["plan"]
        .copy()
    )

    df["plan"] = (
        df["plan"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Standard capitalization
    plan_mapping = {
        "basic": "Basic",
        "standard": "Standard",
        "premium": "Premium"
    }

    df["plan"] = (
        df["plan"]
        .replace(plan_mapping)
    )

    changed_count = (
        before.fillna("")
        .astype(str)
        .ne(
            df["plan"].fillna("").astype(str)
        )
        .sum()
    )

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Category Standardization",
            column="plan",
            issue="Inconsistent plan formatting",
            records_affected=int(changed_count),
            action="Trimmed whitespace and standardized plan names"
        )

    return df, report

######  5. STANDARDIZE CONTRACT TYPE   ######

def standardize_contract_type(df, report):

    print("\nSTEP 7 - Standardizing Contract Type")

    if "contract_type" not in df.columns:
        return df, report

    before = (
        df["contract_type"]
        .copy()
    )

    df["contract_type"] = (
        df["contract_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    contract_mapping = {
        "monthly": "Monthly",
        "one year": "One Year",
        "two year": "Two Year"
    }

    df["contract_type"] = (
        df["contract_type"]
        .replace(contract_mapping)
    )

    changed_count = (
        before.fillna("")
        .astype(str)
        .ne(
            df["contract_type"]
            .fillna("")
            .astype(str)
        )
        .sum()
    )

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Category Standardization",
            column="contract_type",
            issue="Inconsistent contract type formatting",
            records_affected=int(changed_count),
            action="Trimmed whitespace and standardized contract type"
        )

    return df, report

# 6. STANDARDIZE CHURN STATUS

def standardize_churn_status(df, report):

    print("\nSTEP 8 - Standardizing Churn Status")

    if "churn_status" not in df.columns:
        return df, report

    before = (
        df["churn_status"]
        .copy()
    )

    df["churn_status"] = (
        df["churn_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    status_mapping = {
        "active": "Active",
        "churned": "Churned"
    }

    df["churn_status"] = (
        df["churn_status"]
        .replace(status_mapping)
    )

    changed_count = (
        before.fillna("")
        .astype(str)
        .ne(
            df["churn_status"]
            .fillna("")
            .astype(str)
        )
        .sum()
    )

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Category Standardization",
            column="churn_status",
            issue="Inconsistent churn status formatting",
            records_affected=int(changed_count),
            action="Trimmed whitespace and standardized churn status"
        )

    return df, report

######   7. VALIDATE PLAN VALUES   ######

def validate_plan_values(df, report):

    print("\nSTEP 9 - Validating Plan values")

    if "plan" not in df.columns:
        return df, report

    normalized = (
        df["plan"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~normalized.isin(
            VALID_PLAN_VALUES
        )
    ).sum()

    if invalid_count > 0:

        add_cleaning_report(
            report=report,
            step="Business Rule Validation",
            column="plan",
            issue="Invalid plan category",
            records_affected=int(invalid_count),
            action="Retained for investigation"
        )

    return df, report

######   8. VALIDATE CONTRACT TYPE VALUES   ######

def validate_contract_values(df, report):

    print("\nSTEP 10 - Validating Contract Type values")

    if "contract_type" not in df.columns:
        return df, report

    normalized = (
        df["contract_type"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~normalized.isin(
            VALID_CONTRACT_VALUES
        )
    ).sum()

    if invalid_count > 0:

        add_cleaning_report(
            report=report,
            step="Business Rule Validation",
            column="contract_type",
            issue="Invalid contract type",
            records_affected=int(invalid_count),
            action="Retained for investigation"
        )

    return df, report

######   9. VALIDATE CHURN STATUS VALUES   ######

def validate_churn_status_values(df, report):

    print("\nSTEP 11 - Validating Churn Status values")

    if "churn_status" not in df.columns:
        return df, report

    normalized = (
        df["churn_status"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~normalized.isin(
            VALID_CHURN_STATUS_VALUES
        )
    ).sum()

    if invalid_count > 0:

        add_cleaning_report(
            report=report,
            step="Business Rule Validation",
            column="churn_status",
            issue="Invalid churn status",
            records_affected=int(invalid_count),
            action="Retained for investigation"
        )

    return df, report

######   10. CLEAN MONTHLY CHARGE   ######

def clean_monthly_charge(df, report):

    print("\nSTEP 12 - Cleaning Monthly Charge")

    if "monthly_charge" not in df.columns:
        return df, report

    df["monthly_charge"] = pd.to_numeric(
        df["monthly_charge"],
        errors="coerce"
    )

    negative_mask = (
        df["monthly_charge"] < 0
    )

    negative_count = (
        negative_mask.sum()
    )

    if negative_count > 0:

        df.loc[
            negative_mask,
            "monthly_charge"
        ] = pd.NA

        add_cleaning_report(
            report=report,
            step="Business Rule Cleaning",
            column="monthly_charge",
            issue="Negative monthly charge",
            records_affected=int(negative_count),
            action="Converted negative values to missing"
        )

    return df, report

######   11. CLEAN DATE COLUMNS   ######

def clean_subscription_dates(df, report):

    print("\nSTEP 13 - Converting Subscription Dates")

    date_columns = [
        column
        for column in SUBSCRIPTION_DATE_COLUMNS
        if column in df.columns
    ]

    for column in date_columns:

        before_invalid = (
            df[column].notna()
            &
            pd.to_datetime(
                df[column],
                errors="coerce"
            ).isna()
        ).sum()

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        if before_invalid > 0:

            add_cleaning_report(
                report=report,
                step="Date Cleaning",
                column=column,
                issue="Invalid date values",
                records_affected=int(
                    before_invalid
                ),
                action="Converted invalid dates to missing"
            )

    return df, report

######   12. VALIDATE DATE LOGIC   ######

def validate_date_logic(df, report):

    print("\nSTEP 14 - Validating Subscription Date Logic")

    # End Date Before Start Date   

    if (
        "start_date" in df.columns
        and
        "end_date" in df.columns
    ):

        invalid_end_dates = (
            (
                df["end_date"]
                <
                df["start_date"]
            )
            .fillna(False)
        )

        invalid_count = (
            invalid_end_dates.sum()
        )

        if invalid_count > 0:

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="end_date",
                issue="End date occurs before start date",
                records_affected=int(
                    invalid_count
                ),
                action="Retained for investigation"
            )

    # Churn Date Before Start Date
    
    if (
        "start_date" in df.columns
        and
        "churn_date" in df.columns
    ):

        invalid_churn_dates = (
            (
                df["churn_date"]
                <
                df["start_date"]
            )
            .fillna(False)
        )

        invalid_count = (
            invalid_churn_dates.sum()
        )

        if invalid_count > 0:

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="churn_date",
                issue="Churn date occurs before start date",
                records_affected=int(
                    invalid_count
                ),
                action="Retained for investigation"
            )

    # Churn Date and End Date Consistency    

    if (
        "churn_status" in df.columns
        and
        "churn_date" in df.columns
    ):

        churned_without_date = (
            (
                df["churn_status"]
                .eq("Churned")
            )
            &
            df["churn_date"].isna()
        )

        count = (
            churned_without_date.sum()
        )

        if count > 0:

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="churn_date",
                issue="Churned subscription has no churn date",
                records_affected=int(count),
                action="Retained for investigation"
            )

    # Active With Churn Date    

    if (
        "churn_status" in df.columns
        and
        "churn_date" in df.columns
    ):

        active_with_churn_date = (
            (
                df["churn_status"]
                .eq("Active")
            )
            &
            df["churn_date"].notna()
        )

        count = (
            active_with_churn_date.sum()
        )

        if count > 0:

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="churn_date",
                issue="Active subscription has a churn date",
                records_affected=int(count),
                action="Retained for investigation"
            )

    return df, report

######   13. FINAL TEXT CLEANUP   ######


def final_text_cleanup(df, report):

    print("\nSTEP 15 - Final text cleanup")

    text_columns = [
        "customer_id",
        "subscription_id",
        "plan",
        "contract_type",
        "churn_status"
    ]

    for column in text_columns:

        if column not in df.columns:
            continue

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df, report

######   14. FINALIZE DATA TYPES   ######

def finalize_data_types(df, report):

    print("\nSTEP 16 - Finalizing data types")

    # Customer ID
    if "customer_id" in df.columns:

        df["customer_id"] = (
            df["customer_id"]
            .astype("string")
        )

    # Subscription ID
    if "subscription_id" in df.columns:

        df["subscription_id"] = (
            df["subscription_id"]
            .astype("string")
        )

    # Monthly charge
    if "monthly_charge" in df.columns:

        df["monthly_charge"] = pd.to_numeric(
            df["monthly_charge"],
            errors="coerce"
        )

    # Dates
    for column in SUBSCRIPTION_DATE_COLUMNS:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df, report

######   15. GENERATE CLEANING SUMMARY   ######

def generate_subscription_summary(
    df,
    original_rows,
    duplicate_rows_removed
):

    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Original_Rows": original_rows,
        "Rows_Removed": (
            original_rows - len(df)
        ),
        "Total_Missing_Values": int(
            df.isna().sum().sum()
        ),
        "Duplicate_Rows": int(
            df.duplicated().sum()
        ),
        "Duplicate_Rows_Removed": int(
            duplicate_rows_removed
        ),
        "Missing_Customer_IDs": int(
            df["customer_id"].isna().sum()
        ),
        "Missing_Subscription_IDs": int(
            df["subscription_id"].isna().sum()
        ),
        "Duplicate_Customer_IDs": int(
            df["customer_id"].duplicated().sum()
        ),
        "Duplicate_Subscription_IDs": int(
            df["subscription_id"].duplicated().sum()
        )
    }

    return summary

######   MAIN SUBSCRIPTION CLEANING FUNCTION   ######

def clean_subscriptions(df):

    print("\n")
    print("SUBSCRIPTIONS SHEET - DATA CLEANING")
    print("\n")
    
    original_rows = len(df)

    print(
        f"\nOriginal rows    : {len(df):,}"
    )

    print(
        f"Original columns : {len(df.columns)}"
    )

    report = []

    # STEP 1    

    print("\nSTEP 1 - Standardizing column names")

    df = standardize_column_names(df)
    
    # STEP 2
    
    print("\nSTEP 2 - Cleaning text whitespace")

    df = strip_text_columns(df)

    df = convert_blank_to_na(df)
    
    # STEP 3
    
    df, report = clean_customer_id(
        df,
        report
    )
    
    # STEP 4
    
    df, report = clean_subscription_id(
        df,
        report
    )
    
    # STEP 5
    
    df, report = check_duplicate_subscription_ids(
        df,
        report
    )
    
    # STEP 6
    
    df, report = standardize_plan(
        df,
        report
    )
    
    # STEP 7
    
    df, report = standardize_contract_type(
        df,
        report
    )
    
    # STEP 8
    
    df, report = standardize_churn_status(
        df,
        report
    )
    
    # STEP 9
    
    df, report = validate_plan_values(
        df,
        report
    )
    
    # STEP 10
    
    df, report = validate_contract_values(
        df,
        report
    )
    
    # STEP 11
    
    df, report = validate_churn_status_values(
        df,
        report
    )
    
    # STEP 12
    
    df, report = clean_monthly_charge(
        df,
        report
    )
    
    # STEP 13
    
    df, report = clean_subscription_dates(
        df,
        report
    )
    
    # STEP 14

    df, report = validate_date_logic(
        df,
        report
    )
    
    # STEP 15
    
    df, report = final_text_cleanup(
        df,
        report
    )
    
    # STEP 16
    
    df, report = finalize_data_types(
        df,
        report
    )
    
    # FINAL SUMMARY
    
    summary = generate_subscription_summary(
        df,
        original_rows,
        duplicate_rows_removed=0
    )

    print("\n")
    print("SUBSCRIPTIONS CLEANING COMPLETED")
    print("\n") 

    print(
        f"\nOriginal rows : {original_rows:,}"
    )

    print(
        f"Final rows    : {len(df):,}"
    )

    print(
        f"Rows removed  : "
        f"{original_rows - len(df):,}"
    )

    print(
        f"Cleaning issues recorded : "
        f"{len(report)}"
    )

    return df, report, summary