"""
Payment Cleaner
===============

Project:
Customer Churn & Retention Analysis

Purpose:
    Clean and standardize the Payments sheet.

Expected columns:
    Payment_ID
    Customer_ID
    Payment_Date
    Amount
    Payment_Method
    Payment_Status

The Payments cleaner is intentionally self-contained.
It does not depend on helper functions from cleaning_utils.py.
"""

import pandas as pd

######   1. EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "payment_id",
    "customer_id",
    "payment_date",
    "amount",
    "payment_method",
    "payment_status",
]

######   2. VALID PAYMENT METHODS   ######

VALID_PAYMENT_METHODS = {
    "upi",
    "wallet",
    "debit card",
    "credit card",
    "net banking",
    "cash",
}

######   3. VALID PAYMENT STATUSES   ######

VALID_PAYMENT_STATUSES = {
    "successful",
    "failed",
    "pending",
    "refunded",
}

######   4. STANDARDIZE COLUMN NAMES   ######

def standardize_column_names(df):
    """
    Convert Excel column names into standardized snake_case.

    Example:

        Payment_ID      -> payment_id
        Customer_ID     -> customer_id
        Payment_Date    -> payment_date
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df

######   5. VALIDATE COLUMNS   ######

def validate_columns(df):
    """
    Check whether all expected Payments columns exist.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing Payments columns:\n"
            + "\n".join(missing_columns)
        )

######   6. CLEAN PAYMENT ID   ######

def clean_payment_ids(df, report):
    """
    Clean Payment_ID.

    Rules:
        - Convert to string
        - Strip whitespace
        - Convert to uppercase
        - Identify missing IDs
        - Identify duplicate IDs
    """

    df["payment_id"] = (
        df["payment_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Missing IDs    

    missing_count = (
        df["payment_id"]
        .isna()
        .sum()
    )

    if missing_count > 0:

        report.append(
            {
                "Column": "payment_id",
                "Issue": "Missing Payment ID",
                "Count": int(missing_count),
                "Action": (
                    "Retained as missing for review."
                )
            }
        )
    
    # Duplicate IDs
    
    duplicate_count = (
        df["payment_id"]
        .dropna()
        .duplicated()
        .sum()
    )

    if duplicate_count > 0:

        report.append(
            {
                "Column": "payment_id",
                "Issue": "Duplicate Payment ID",
                "Count": int(duplicate_count),
                "Action": (
                    "Duplicate IDs will be removed "
                    "after exact duplicate checking."
                )
            }
        )

    return df

######   7. CLEAN CUSTOMER ID   ######

def clean_customer_ids(df, report):
    """
    Clean Customer_ID.

    Customer_ID will later be used for referential
    integrity validation with Customers.
    """

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Missing Customer IDs    

    missing_count = (
        df["customer_id"]
        .isna()
        .sum()
    )

    if missing_count > 0:

        report.append(
            {
                "Column": "customer_id",
                "Issue": "Missing Customer ID",
                "Count": int(missing_count),
                "Action": (
                    "Retained as missing for review."
                )
            }
        )

    return df

######   8. CLEAN PAYMENT DATE   ######

def clean_payment_date(df, report):
    """
    Convert Payment_Date to datetime.

    Invalid dates become NaT.
    """

    original_missing = (
        df["payment_date"]
        .isna()
        .sum()
    )

    df["payment_date"] = pd.to_datetime(
        df["payment_date"],
        errors="coerce"
    )

    final_missing = (
        df["payment_date"]
        .isna()
        .sum()
    )

    invalid_date_count = (
        final_missing
        - original_missing
    )

    if invalid_date_count > 0:

        report.append(
            {
                "Column": "payment_date",
                "Issue": "Invalid Payment Date",
                "Count": int(invalid_date_count),
                "Action": (
                    "Invalid dates converted to missing."
                )
            }
        )
    
    # Future payment dates
    
    today = pd.Timestamp.today().normalize()

    future_count = (
        df["payment_date"] > today
    ).sum()

    if future_count > 0:

        report.append(
            {
                "Column": "payment_date",
                "Issue": "Future Payment Date",
                "Count": int(future_count),
                "Action": (
                    "Future dates retained for investigation."
                )
            }
        )

    return df

######   9. CLEAN PAYMENT AMOUNT   ######

def clean_payment_amount(df, report):
    """
    Convert Amount to numeric.

    Rules:
        - Invalid values become NaN
        - Negative amounts become NaN
    """

    original_missing = (
        df["amount"]
        .isna()
        .sum()
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    final_missing = (
        df["amount"]
        .isna()
        .sum()
    )

    invalid_amount_count = (
        final_missing
        - original_missing
    )

    if invalid_amount_count > 0:

        report.append(
            {
                "Column": "amount",
                "Issue": "Invalid Payment Amount",
                "Count": int(invalid_amount_count),
                "Action": (
                    "Invalid values converted to missing."
                )
            }
        )
    
    # Negative amounts
    
    negative_count = (
        df["amount"] < 0
    ).sum()

    if negative_count > 0:

        df.loc[
            df["amount"] < 0,
            "amount"
        ] = pd.NA

        report.append(
            {
                "Column": "amount",
                "Issue": "Negative Payment Amount",
                "Count": int(negative_count),
                "Action": (
                    "Negative amounts converted to missing."
                )
            }
        )

    return df

######   10. CLEAN PAYMENT METHOD   ######

def clean_payment_method(df, report):
    """
    Standardize Payment_Method.
    """

    df["payment_method"] = (
        df["payment_method"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Find unexpected categories    

    actual_values = set(
        df["payment_method"]
        .dropna()
        .unique()
    )

    unexpected_values = (
        actual_values
        - VALID_PAYMENT_METHODS
    )

    if unexpected_values:

        report.append(
            {
                "Column": "payment_method",
                "Issue": "Unexpected Payment Method",
                "Count": len(unexpected_values),
                "Action": (
                    "Unexpected categories retained "
                    "for investigation."
                )
            }
        )
    
    # Standardize known categories
    
    payment_method_mapping = {
        "upi": "UPI",
        "wallet": "Wallet",
        "debit card": "Debit Card",
        "credit card": "Credit Card",
        "net banking": "Net Banking",
        "cash": "Cash",
    }

    df["payment_method"] = (
        df["payment_method"]
        .map(payment_method_mapping)
        .fillna(
            df["payment_method"]
        )
    )

    return df

######   11. CLEAN PAYMENT STATUS   ######

def clean_payment_status(df, report):
    """
    Standardize Payment_Status.
    """

    df["payment_status"] = (
        df["payment_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    
    # Find unexpected statuses
    
    actual_values = set(
        df["payment_status"]
        .dropna()
        .unique()
    )

    unexpected_values = (
        actual_values
        - VALID_PAYMENT_STATUSES
    )

    if unexpected_values:

        report.append(
            {
                "Column": "payment_status",
                "Issue": "Unexpected Payment Status",
                "Count": len(unexpected_values),
                "Action": (
                    "Unexpected statuses retained "
                    "for investigation."
                )
            }
        )
    
    # Standardize known statuses
    
    status_mapping = {
        "successful": "Successful",
        "failed": "Failed",
        "pending": "Pending",
        "refunded": "Refunded",
    }

    df["payment_status"] = (
        df["payment_status"]
        .map(status_mapping)
        .fillna(
            df["payment_status"]
        )
    )

    return df

######   12. REMOVE EXACT DUPLICATE ROWS   ######

def remove_duplicate_rows(df, report):
    """
    Remove completely identical payment records.
    """

    duplicate_count = (
        df.duplicated()
        .sum()
    )

    if duplicate_count > 0:

        df = df.drop_duplicates(
            keep="first"
        )

        report.append(
            {
                "Column": "All Columns",
                "Issue": "Duplicate Payment Rows",
                "Count": int(duplicate_count),
                "Action": (
                    "Exact duplicate rows removed."
                )
            }
        )

    return df

######   13. REMOVE DUPLICATE PAYMENT IDs   ######

def remove_duplicate_payment_ids(
    df,
    report
):
    """
    Payment_ID should uniquely identify a payment.

    Keep the first occurrence of a duplicate Payment_ID.
    """

    duplicate_mask = (
        df["payment_id"]
        .notna()
        &
        df["payment_id"]
        .duplicated(
            keep="first"
        )
    )

    duplicate_count = (
        duplicate_mask.sum()
    )

    if duplicate_count > 0:

        df = df.loc[
            ~duplicate_mask
        ].copy()

        report.append(
            {
                "Column": "payment_id",
                "Issue": "Duplicate Payment IDs Removed",
                "Count": int(duplicate_count),
                "Action": (
                    "First occurrence retained."
                )
            }
        )

    return df

######   14. FINAL TEXT CLEANUP   ######

def final_text_cleanup(df):
    """
    Remove unnecessary whitespace from text columns.
    """

    text_columns = [
        "payment_id",
        "customer_id",
        "payment_method",
        "payment_status",
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df

######   15. FINAL DATA TYPES   ######

def finalize_data_types(df):
    """
    Apply final data types.
    """

    df["payment_id"] = (
        df["payment_id"]
        .astype("string")
    )

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
    )

    df["payment_date"] = pd.to_datetime(
        df["payment_date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["payment_method"] = (
        df["payment_method"]
        .astype("string")
    )

    df["payment_status"] = (
        df["payment_status"]
        .astype("string")
    )

    return df

######   16. CREATE SUMMARY   ######

def create_summary(
    df,
    original_rows,
    rows_removed,
    report
):
    """
    Create Payments cleaning summary.
    """

    summary = {
        "Rows": len(df),

        "Columns": len(df.columns),

        "Original_Rows": original_rows,

        "Rows_Removed": rows_removed,

        "Total_Missing_Values": int(
            df.isna().sum().sum()
        ),

        "Duplicate_Rows": int(
            df.duplicated().sum()
        ),

        "Missing_Payment_IDs": int(
            df["payment_id"]
            .isna()
            .sum()
        ),

        "Duplicate_Payment_IDs": int(
            df["payment_id"]
            .duplicated()
            .sum()
        ),

        "Missing_Customer_IDs": int(
            df["customer_id"]
            .isna()
            .sum()
        ),

        "Unique_Payment_IDs": int(
            df["payment_id"]
            .nunique()
        ),

        "Unique_Customer_IDs": int(
            df["customer_id"]
            .nunique()
        ),

        "Missing_Payment_Dates": int(
            df["payment_date"]
            .isna()
            .sum()
        ),

        "Missing_Amounts": int(
            df["amount"]
            .isna()
            .sum()
        ),

        "Negative_Amounts": int(
            (df["amount"] < 0)
            .sum()
        ),

        "Cleaning_Issues": len(report),
    }

    return summary

######   17. MAIN CLEANING FUNCTION   ######

def clean_payments(df):
    """
    Complete Payments cleaning pipeline.

    Returns:
        cleaned_df
        report
        summary
    """
    # Make a copy so the original DataFrame is not modified.
    df = df.copy()

    report = []

    original_rows = len(df)

    # Step 1: Standardize column names
    
    df = standardize_column_names(
        df
    )
    
    # Step 2: Validate columns    

    validate_columns(
        df
    )
    
    # Step 3: Clean Payment IDs
    
    df = clean_payment_ids(
        df,
        report
    )
    
    # Step 4: Clean Customer IDs
    
    df = clean_customer_ids(
        df,
        report
    )
    
    # Step 5: Clean Payment Date
    
    df = clean_payment_date(
        df,
        report
    )
    
    # Step 6: Clean Amount
    
    df = clean_payment_amount(
        df,
        report
    )

    # Step 7: Clean Payment Method
    
    df = clean_payment_method(
        df,
        report
    )
    
    # Step 8: Clean Payment Status
    
    df = clean_payment_status(
        df,
        report
    )
    
    # Step 9: Remove exact duplicate rows
    
    df = remove_duplicate_rows(
        df,
        report
    )
    
    # Step 10: Remove duplicate Payment IDs
    
    df = remove_duplicate_payment_ids(
        df,
        report
    )
    
    # Step 11: Final text cleanup
    
    df = final_text_cleanup(
        df
    )
    
    # Step 12: Final data types
    
    df = finalize_data_types(
        df
    )
    
    # Step 13: Rows removed
    
    rows_removed = (
        original_rows
        - len(df)
    )
    
    # Step 14: Create summary
    
    summary = create_summary(
        df,
        original_rows,
        rows_removed,
        report
    )

    return (
        df,
        report,
        summary
    )