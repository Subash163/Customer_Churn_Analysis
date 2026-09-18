# CUSTOMER CHURN & RETENTION ANALYSIS
# CUSTOMERS SHEET CLEANER

import numpy as np
import pandas as pd

from cleaning_utils import (
    standardize_column_names,
    strip_text_columns,
    convert_blank_to_na,
    convert_numeric_columns,
    convert_date_columns,
    remove_exact_duplicates,
    dataset_summary,
    add_cleaning_report
)

######   1. CUSTOMERS NUMERIC COLUMNS   ######


CUSTOMER_NUMERIC_COLUMNS = [
    "age"
]

######   2. CUSTOMERS DATE COLUMNS   ######

CUSTOMER_DATE_COLUMNS = [
    "signup_date"
]

######   3. CLEAN CUSTOMER ID   ######

def clean_customer_id(
    df,
    report
):
    """
    Clean Customer ID.

    Customer ID is treated as a required
    customer-level identifier.
    """

    if "customer_id" not in df.columns:

        return df, report

    # Convert to string
    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
    )

    # Convert blank IDs to missing
    blank_mask = (
        df["customer_id"]
        .eq("")
    )

    blank_count = blank_mask.sum()

    if blank_count > 0:

        df.loc[
            blank_mask,
            "customer_id"
        ] = pd.NA

        add_cleaning_report(
            report=report,
            step="Customer ID Cleaning",
            column="customer_id",
            issue="Blank Customer IDs",
            records_affected=blank_count,
            action="Converted blank Customer IDs to missing"
        )

    # Missing IDs
    missing_count = (
        df["customer_id"]
        .isna()
        .sum()
    )

    if missing_count > 0:

        add_cleaning_report(
            report=report,
            step="Customer ID Cleaning",
            column="customer_id",
            issue="Missing Customer IDs",
            records_affected=missing_count,
            action=(
                "Removed records because Customer ID "
                "is required to uniquely identify customers"
            )
        )

        df = df.dropna(
            subset=["customer_id"]
        ).copy()

    return df, report

######   4. CHECK DUPLICATE CUSTOMER IDs   ######

def check_duplicate_customer_ids(
    df,
    report
):
    """
    Check duplicate Customer IDs.

    We do not automatically delete them.
    """

    if "customer_id" not in df.columns:

        return df, report

    duplicate_mask = (
        df["customer_id"]
        .duplicated(
            keep=False
        )
    )

    duplicate_count = (
        duplicate_mask.sum()
    )

    unique_duplicate_ids = (
        df.loc[
            duplicate_mask,
            "customer_id"
        ]
        .nunique()
    )

    if duplicate_count > 0:

        add_cleaning_report(
            report=report,
            step="Customer ID Validation",
            column="customer_id",
            issue="Duplicate Customer IDs",
            records_affected=duplicate_count,
            action=(
                f"Flagged {unique_duplicate_ids} "
                "unique duplicated Customer IDs "
                "for investigation; records were not "
                "automatically removed"
            )
        )

    return df, report

######   5. STANDARDIZE GENDER   ######

def standardize_gender(
    df,
    report
):
    """
    Standardize gender values.
    """

    if "gender" not in df.columns:

        return df, report

    original = (
        df["gender"]
        .astype("string")
        .copy()
    )

    df["gender"] = (
        df["gender"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    gender_mapping = {

        "male": "Male",
        "m": "Male",
        "man": "Male",

        "female": "Female",
        "f": "Female",
        "woman": "Female",

        "other": "Other",
        "o": "Other",

        "non-binary": "Other",
        "nonbinary": "Other"
    }

    df["gender"] = (
        df["gender"]
        .replace(gender_mapping)
    )

    changed_count = (
        original.fillna("__NA__")
        .astype(str)
        !=
        df["gender"]
        .fillna("__NA__")
        .astype(str)
    ).sum()

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Categorical Standardization",
            column="gender",
            issue="Inconsistent gender values",
            records_affected=changed_count,
            action="Standardized gender values"
        )

    return df, report

######   6. STANDARDIZE MARITAL STATUS   ######

def standardize_marital_status(
    df,
    report
):
    """
    Standardize marital status.
    """

    if "marital_status" not in df.columns:

        return df, report

    original = (
        df["marital_status"]
        .astype("string")
        .copy()
    )

    df["marital_status"] = (
        df["marital_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    mapping = {

        "single": "Single",
        "s": "Single",

        "married": "Married",
        "m": "Married",

        "divorced": "Divorced",
        "d": "Divorced",

        "widowed": "Widowed",
        "w": "Widowed"
    }

    df["marital_status"] = (
        df["marital_status"]
        .replace(mapping)
    )

    changed_count = (
        original.fillna("__NA__")
        .astype(str)
        !=
        df["marital_status"]
        .fillna("__NA__")
        .astype(str)
    ).sum()

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Categorical Standardization",
            column="marital_status",
            issue="Inconsistent marital status values",
            records_affected=changed_count,
            action="Standardized marital status values"
        )

    return df, report

######   7. STANDARDIZE CITY   ######

def standardize_city(
    df,
    report
):
    """
    Standardize city names.
    """

    if "city" not in df.columns:

        return df, report

    original = (
        df["city"]
        .astype("string")
        .copy()
    )

    df["city"] = (
        df["city"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    changed_count = (
        original.fillna("__NA__")
        .astype(str)
        !=
        df["city"]
        .fillna("__NA__")
        .astype(str)
    ).sum()

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Text Standardization",
            column="city",
            issue="Inconsistent city formatting",
            records_affected=changed_count,
            action="Trimmed whitespace and standardized capitalization"
        )

    return df, report

######   8. STANDARDIZE STATE   ######

def standardize_state(
    df,
    report
):
    """
    Standardize state names.
    """

    if "state" not in df.columns:

        return df, report

    original = (
        df["state"]
        .astype("string")
        .copy()
    )

    df["state"] = (
        df["state"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    changed_count = (
        original.fillna("__NA__")
        .astype(str)
        !=
        df["state"]
        .fillna("__NA__")
        .astype(str)
    ).sum()

    if changed_count > 0:

        add_cleaning_report(
            report=report,
            step="Text Standardization",
            column="state",
            issue="Inconsistent state formatting",
            records_affected=changed_count,
            action="Trimmed whitespace and standardized capitalization"
        )

    return df, report

######   9. CLEAN AGE   ######

def clean_age(
    df,
    report
):
    """
    Apply reasonable business rules to Age.
    """

    if "age" not in df.columns:

        return df, report

    invalid_mask = (
        (df["age"] < 0)
        |
        (df["age"] > 120)
    )

    invalid_count = (
        invalid_mask.sum()
    )

    if invalid_count > 0:

        df.loc[
            invalid_mask,
            "age"
        ] = np.nan

        add_cleaning_report(
            report=report,
            step="Business Rule Cleaning",
            column="age",
            issue="Age outside valid range",
            records_affected=invalid_count,
            action="Converted invalid ages to missing"
        )

    return df, report

######   10. VALIDATE DATE LOGIC   ######

def validate_date_logic(
    df,
    report
):
    """
    Validate logical relationships between customer dates.
    """

    
    # Signup date should not be in the future
    

    if "signup_date" in df.columns:

        today = (
            pd.Timestamp
            .today()
            .normalize()
        )

        future_mask = (
            df["signup_date"] > today
        )

        future_count = (
            future_mask.sum()
        )

        if future_count > 0:

            df.loc[
                future_mask,
                "signup_date"
            ] = pd.NaT

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="signup_date",
                issue="Future signup date",
                records_affected=future_count,
                action="Converted future signup dates to missing"
            )

    
    # Churn date should not be before signup date
    

    if (
        "signup_date" in df.columns
        and
        "churn_date" in df.columns
    ):

        invalid_mask = (
            df["signup_date"].notna()
            &
            df["churn_date"].notna()
            &
            (
                df["churn_date"]
                <
                df["signup_date"]
            )
        )

        invalid_count = (
            invalid_mask.sum()
        )

        if invalid_count > 0:

            df.loc[
                invalid_mask,
                "churn_date"
            ] = pd.NaT

            add_cleaning_report(
                report=report,
                step="Date Business Rule",
                column="churn_date",
                issue="Churn date before signup date",
                records_affected=invalid_count,
                action="Converted invalid churn dates to missing"
            )

    return df, report



# 11. GENERATE CUSTOMER CLEANING SUMMARY


def generate_customer_summary(
    df,
    original_rows
):
    """
    Generate final customer cleaning summary.
    """

    summary = dataset_summary(df)

    summary["Original_Rows"] = original_rows

    summary["Rows_Removed"] = (
        original_rows -
        len(df)
    )

    summary["Missing_Customer_IDs"] = (
        df["customer_id"].isna().sum()
        if "customer_id" in df.columns
        else None
    )

    summary["Duplicate_Customer_IDs"] = (
        df["customer_id"].duplicated().sum()
        if "customer_id" in df.columns
        else None
    )

    return summary



# 12. MAIN CUSTOMERS CLEANING FUNCTION


def clean_customers(df):
    """
    Complete Customers sheet cleaning pipeline.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw Customers DataFrame.

    Returns
    -------
    cleaned_df : pandas.DataFrame
        Cleaned Customers DataFrame.

    cleaning_report : pandas.DataFrame
        Cleaning operations performed.

    cleaning_summary : dict
        Before/after summary.
    """

    print("\n")
    print("CUSTOMERS SHEET - DATA CLEANING")

    # Initial information
    
    df = df.copy()

    original_rows = len(df)
    original_columns = len(df.columns)

    print(
        f"\nOriginal rows    : {original_rows:,}"
    )

    print(
        f"Original columns : {original_columns:,}"
    )

    # Cleaning report
    report = []
    
    # STEP 1 - Column names

    print("\nSTEP 1 - Standardizing column names")

    df = standardize_column_names(df)

    # STEP 2 - Text cleaning    

    print("\nSTEP 2 - Cleaning text whitespace")

    df = strip_text_columns(df)

    df = convert_blank_to_na(df)

    # STEP 3 - Customer ID
    
    print("\nSTEP 3 - Cleaning Customer ID")

    df, report = clean_customer_id(
        df,
        report
    )
    
    # STEP 4 - Exact duplicates
    
    print("\nSTEP 4 - Removing exact duplicates")

    df, duplicate_count = (
        remove_exact_duplicates(df)
    )

    if duplicate_count > 0:

        add_cleaning_report(
            report=report,
            step="Duplicate Cleaning",
            column="All Columns",
            issue="Exact duplicate rows",
            records_affected=duplicate_count,
            action="Removed duplicate rows and kept first occurrence"
        )
    
    # STEP 5 - Duplicate Customer IDs
    
    print("\nSTEP 5 - Checking duplicate Customer IDs")

    df, report = (
        check_duplicate_customer_ids(
            df,
            report
        )
    )
    
    # STEP 6 - Numeric columns
    
    print("\nSTEP 6 - Converting numeric columns")

    df = convert_numeric_columns(
        df,
        CUSTOMER_NUMERIC_COLUMNS
    )

    
    # STEP 7 - Date columns
    
    print("\nSTEP 7 - Converting date columns")

    df = convert_date_columns(
        df,
        CUSTOMER_DATE_COLUMNS
    )
    
    # STEP 8 - Gender
    
    print("\nSTEP 8 - Standardizing gender")

    df, report = standardize_gender(
        df,
        report
    )
    
    # STEP 9 - Marital status
    
    print("\nSTEP 9 - Standardizing marital status")

    df, report = standardize_marital_status(
        df,
        report
    )
    
    # STEP 10 - City
    
    print("\nSTEP 10 - Standardizing city")

    df, report = standardize_city(
        df,
        report
    )
    
    # STEP 11 - State
    
    print("\nSTEP 11 - Standardizing state")

    df, report = standardize_state(
        df,
        report
    )
    
    # STEP 12 - Age
    
    print("\nSTEP 12 - Validating age")

    df, report = clean_age(
        df,
        report
    )
    
    # STEP 13 - Date logic
    
    print("\nSTEP 13 - Validating date logic")

    df, report = validate_date_logic(
        df,
        report
    )
    
    # STEP 14 - Final text cleanup
    
    print("\nSTEP 14 - Final text cleanup")

    df = strip_text_columns(df)

    df = convert_blank_to_na(df)
    
    # STEP 15 - Final data types
    
    print("\nSTEP 15 - Finalizing data types")

    object_columns = (
        df.select_dtypes(
            include=["object"]
        ).columns
    )

    for column in object_columns:

        df[column] = (
            df[column]
            .astype("string")
        )

    # Final summary    

    cleaning_summary = (
        generate_customer_summary(
            df,
            original_rows
        )
    )

    cleaning_report = pd.DataFrame(
        report
    )

    print("\n")
    print("CUSTOMERS CLEANING COMPLETED")
    print("\n")

    print(
        f"\nOriginal rows : "
        f"{original_rows:,}"
    )

    print(
        f"Final rows    : "
        f"{len(df):,}"
    )

    print(
        f"Rows removed  : "
        f"{original_rows - len(df):,}"
    )

    print(
        f"Cleaning issues recorded : "
        f"{len(report):,}"
    )

    return (
        df,
        cleaning_report,
        cleaning_summary
    )