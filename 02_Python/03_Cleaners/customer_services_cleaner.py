import pandas as pd

######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "customer_id",
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
]

######   VALID VALUES   ######

VALID_YES_NO_VALUES = {
    "yes",
    "no",
}

######   STANDARDIZE COLUMN NAMES   ######

def standardize_column_names(df):
    """
    Standardize column names into snake_case.

    Example:
        Customer_ID -> customer_id
        Mobile_App  -> mobile_app
    """

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

######   VALIDATE COLUMNS   ######

def validate_columns(df):
    """
    Validate that all expected Customer_Services columns exist.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing expected Customer_Services columns: "
            f"{missing_columns}"
        )

    return True

######   CLEAN CUSTOMER IDs   ######

def clean_customer_ids(df, report):
    """
    Clean Customer IDs.

    Rules:
    - Convert to string
    - Remove leading/trailing spaces
    - Convert to uppercase
    - Detect missing IDs
    - Detect duplicate IDs
    """

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    missing_ids = int(
        df["customer_id"].isna().sum()
    )

    if missing_ids > 0:

        report.append(
            f"Found {missing_ids:,} missing Customer IDs."
        )

    duplicate_ids = int(
        df["customer_id"].duplicated().sum()
    )

    if duplicate_ids > 0:

        report.append(
            f"Found {duplicate_ids:,} duplicate Customer IDs."
        )

    return df

######   CLEAN YES / NO SERVICE COLUMNS   ######

def clean_yes_no_column(df, column, report):
    """
    Standardize service columns to Yes / No.

    Accepted values:
        yes
        no

    Blank values remain missing.
    Unexpected values are retained but reported.
    """

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Count missing values    

    missing_count = int(
        df[column].isna().sum()
    )

    if missing_count > 0:

        report.append(
            f"{column}: {missing_count:,} missing values found."
        )

    # Detect unexpected values    

    non_null_values = set(
        df[column]
        .dropna()
        .unique()
    )

    unexpected_values = (
        non_null_values - VALID_YES_NO_VALUES
    )

    if unexpected_values:

        report.append(
            f"{column}: unexpected values found: "
            f"{sorted(unexpected_values)}"
        )
    
    # Standardize Yes / No
    
    value_mapping = {
        "yes": "Yes",
        "no": "No",
    }

    df[column] = df[column].map(
        value_mapping
    ).fillna(df[column])

    return df

######   CLEAN SERVICE COLUMNS   ######

def clean_service_columns(df, report):
    """
    Clean all service indicator columns.
    """

    service_columns = [
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    ]

    for column in service_columns:

        df = clean_yes_no_column(
            df,
            column,
            report
        )

    return df

######   REMOVE EXACT DUPLICATE ROWS   ######

def remove_duplicate_rows(df, report):
    """
    Remove exact duplicate records.
    """

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if duplicate_rows > 0:

        report.append(
            f"Removed {duplicate_rows:,} exact duplicate rows."
        )

        df = df.drop_duplicates(
            keep="first"
        ).copy()

    return df

######   REMOVE DUPLICATE CUSTOMER IDs   ######

def remove_duplicate_customer_ids(df, report):
    """
    Remove duplicate Customer ID records.

    The first occurrence is retained.

    This is appropriate if Customer_Services is intended
    to contain one service-profile record per customer.
    """

    duplicate_ids = int(
        df["customer_id"].duplicated().sum()
    )

    if duplicate_ids > 0:

        report.append(
            f"Removed {duplicate_ids:,} duplicate Customer ID records."
        )

        df = df.drop_duplicates(
            subset=["customer_id"],
            keep="first"
        ).copy()

    return df

######   FINAL TEXT CLEANUP   ######

def final_text_cleanup(df):
    """
    Final cleanup of string columns.
    """

    text_columns = [
        "customer_id",
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    return df

######   FINAL DATA TYPES   ######

def finalize_data_types(df):
    """
    Set final data types.
    """

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
    )

    service_columns = [
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    ]

    for column in service_columns:

        df[column] = (
            df[column]
            .astype("string")
        )

    return df

######   CREATE SUMMARY   ######

def create_summary(
    df,
    original_rows,
    rows_removed,
    report
):
    """
    Create cleaning summary.
    """

    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Original_Rows": original_rows,
        "Rows_Removed": rows_removed,
        "Total_Missing_Values": int(
            df.isnull().sum().sum()
        ),
        "Duplicate_Rows": int(
            df.duplicated().sum()
        ),
        "Missing_Customer_IDs": int(
            df["customer_id"].isnull().sum()
        ),
        "Duplicate_Customer_IDs": int(
            df["customer_id"].duplicated().sum()
        ),
        "Unique_Customer_IDs": int(
            df["customer_id"].nunique()
        ),
        "Cleaning_Issues": len(report),
    }

    # Service-level summaries    

    service_columns = [
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    ]

    for column in service_columns:

        yes_count = int(
            (
                df[column]
                .astype("string")
                .str.lower()
                == "yes"
            ).sum()
        )

        no_count = int(
            (
                df[column]
                .astype("string")
                .str.lower()
                == "no"
            ).sum()
        )

        summary[
            f"{column}_Yes_Count"
        ] = yes_count

        summary[
            f"{column}_No_Count"
        ] = no_count

    return summary

######   MAIN CLEANING FUNCTION   ######

def clean_customer_services(df):
    """
    Complete Customer_Services cleaning pipeline.

    Returns:
        cleaned_df
        summary
        cleaning_report
    """

    # Make a copy    

    df = df.copy()

    original_rows = len(df)

    report = []
    
    # Standardize columns

    df = standardize_column_names(df)
    
    # Validate columns
    
    validate_columns(df)
    
    # Keep only expected columns
    
    df = df[
        EXPECTED_COLUMNS
    ].copy()
    
    # Clean Customer IDs
    
    df = clean_customer_ids(
        df,
        report
    )
    
    # Clean service columns
    
    df = clean_service_columns(
        df,
        report
    )
    
    # Remove exact duplicates
    
    df = remove_duplicate_rows(
        df,
        report
    )
    
    # Remove duplicate Customer IDs

    df = remove_duplicate_customer_ids(
        df,
        report
    )
    
    # Final text cleanup
    
    df = final_text_cleanup(df)

    # Final data types
    
    df = finalize_data_types(df)
    
    # Calculate rows removed
    
    rows_removed = (
        original_rows - len(df)
    )
    
    # Create summary
    
    summary = create_summary(
        df=df,
        original_rows=original_rows,
        rows_removed=rows_removed,
        report=report
    )

    return df, summary, report