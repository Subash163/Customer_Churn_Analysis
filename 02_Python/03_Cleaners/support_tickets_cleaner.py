import pandas as pd

######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "ticket_id",
    "customer_id",
    "ticket_date",
    "issue_type",
    "resolution_time_hours",
    "satisfaction_score",
    "resolved",
]

# VALID YES / NO VALUES

VALID_YES_NO_VALUES = {
    "yes",
    "no",
}

######   STANDARDIZE COLUMN NAMES   ######

def standardize_column_names(df):
    """
    Standardize column names into snake_case.

    Example:
        Ticket_ID -> ticket_id
        Resolution_Time_Hours -> resolution_time_hours
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
    Validate that all expected Support_Tickets columns exist.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing expected Support_Tickets columns: "
            f"{missing_columns}"
        )

    return True

######   CLEAN TICKET IDs   ######

def clean_ticket_ids(df, report):
    """
    Clean Ticket IDs.

    Rules:
    - Convert to string
    - Strip whitespace
    - Convert to uppercase
    - Report missing IDs
    - Report duplicate IDs
    """

    df["ticket_id"] = (
        df["ticket_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    missing_ids = int(
        df["ticket_id"].isna().sum()
    )

    if missing_ids > 0:

        report.append(
            f"Found {missing_ids:,} missing Ticket IDs."
        )

    blank_ids = int(
        df["ticket_id"]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    if blank_ids > 0:

        report.append(
            f"Found {blank_ids:,} blank Ticket IDs."
        )

    duplicate_ids = int(
        df["ticket_id"].duplicated().sum()
    )

    if duplicate_ids > 0:

        report.append(
            f"Found {duplicate_ids:,} duplicate Ticket IDs."
        )

    return df

######   CLEAN CUSTOMER IDs   ######

def clean_customer_ids(df, report):
    """
    Clean Customer IDs.

    Rules:
    - Convert to string
    - Strip whitespace
    - Convert to uppercase
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

    blank_ids = int(
        df["customer_id"]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    if blank_ids > 0:

        report.append(
            f"Found {blank_ids:,} blank Customer IDs."
        )

    return df

######   CLEAN TICKET DATE   ######

def clean_ticket_date(df, report):
    """
    Convert Ticket_Date to datetime.

    Invalid dates become missing and are reported.
    Future dates are reported but retained.
    """

    original_missing = int(
        df["ticket_date"].isna().sum()
    )

    df["ticket_date"] = pd.to_datetime(
        df["ticket_date"],
        errors="coerce"
    )

    invalid_dates = int(
        df["ticket_date"].isna().sum()
    ) - original_missing

    if invalid_dates > 0:

        report.append(
            f"Found {invalid_dates:,} invalid Ticket Dates."
        )

    future_dates = int(
        (
            df["ticket_date"]
            > pd.Timestamp.now()
        ).sum()
    )

    if future_dates > 0:

        report.append(
            f"Found {future_dates:,} future Ticket Dates."
        )

    return df

######   CLEAN ISSUE TYPE   ######

def clean_issue_type(df, report):
    """
    Standardize Issue_Type text.

    Does not restrict Issue_Type to a hard-coded
    category list because the full dataset may contain
    legitimate categories not present in the sample.
    """

    df["issue_type"] = (
        df["issue_type"]
        .astype("string")
        .str.strip()
    )

    missing_issue_types = int(
        df["issue_type"].isna().sum()
    )

    if missing_issue_types > 0:

        report.append(
            f"Found {missing_issue_types:,} missing Issue Types."
        )

    # Standardize capitalization.
    df["issue_type"] = (
        df["issue_type"]
        .str.title()
    )

    return df

######   CLEAN RESOLUTION TIME   ######

def clean_resolution_time(df, report):
    """
    Convert Resolution_Time_Hours to numeric.

    Negative values are treated as invalid and
    converted to missing.
    """

    df["resolution_time_hours"] = pd.to_numeric(
        df["resolution_time_hours"],
        errors="coerce"
    )

    invalid_values = int(
        df["resolution_time_hours"].isna().sum()
    )

    if invalid_values > 0:

        report.append(
            f"Found {invalid_values:,} invalid or missing "
            "Resolution Time values."
        )

    negative_values = int(
        (
            df["resolution_time_hours"]
            < 0
        ).sum()
    )

    if negative_values > 0:

        report.append(
            f"Found {negative_values:,} negative "
            "Resolution Time values."
        )

        df.loc[
            df["resolution_time_hours"] < 0,
            "resolution_time_hours"
        ] = pd.NA

    return df

######   CLEAN SATISFACTION SCORE   ######

def clean_satisfaction_score(df, report):
    """
    Convert Satisfaction_Score to numeric.

    Expected business range:
        1 = lowest satisfaction
        5 = highest satisfaction

    Values outside 1-5 are converted to missing
    and reported.
    """

    df["satisfaction_score"] = pd.to_numeric(
        df["satisfaction_score"],
        errors="coerce"
    )

    invalid_numeric = int(
        df["satisfaction_score"].isna().sum()
    )

    if invalid_numeric > 0:

        report.append(
            f"Found {invalid_numeric:,} invalid or missing "
            "Satisfaction Score values."
        )

    out_of_range = int(
        (
            (
                df["satisfaction_score"] < 1
            )
            |
            (
                df["satisfaction_score"] > 5
            )
        )
        .fillna(False)
        .sum()
    )

    if out_of_range > 0:

        report.append(
            f"Found {out_of_range:,} Satisfaction Scores "
            "outside the valid 1-5 range."
        )

        df.loc[
            (
                df["satisfaction_score"] < 1
            )
            |
            (
                df["satisfaction_score"] > 5
            ),
            "satisfaction_score"
        ] = pd.NA

    return df

######   CLEAN RESOLVED STATUS   ######

def clean_resolved(df, report):
    """
    Standardize Resolved values to Yes / No.

    Accepted values:
        Yes
        No

    Unexpected values are retained and reported.
    """

    df["resolved"] = (
        df["resolved"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    missing_values = int(
        df["resolved"].isna().sum()
    )

    if missing_values > 0:

        report.append(
            f"Found {missing_values:,} missing Resolved values."
        )

    non_null_values = set(
        df["resolved"]
        .dropna()
        .unique()
    )

    unexpected_values = (
        non_null_values
        - VALID_YES_NO_VALUES
    )

    if unexpected_values:

        report.append(
            "Resolved contains unexpected values: "
            f"{sorted(unexpected_values)}"
        )

    value_mapping = {
        "yes": "Yes",
        "no": "No",
    }

    df["resolved"] = (
        df["resolved"]
        .map(value_mapping)
        .fillna(df["resolved"])
    )

    return df

######   REMOVE EXACT DUPLICATE ROWS   ######

def remove_duplicate_rows(df, report):
    """
    Remove exact duplicate rows.

    The first occurrence is retained.
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

######   REMOVE DUPLICATE TICKET IDs   ######

def remove_duplicate_ticket_ids(df, report):
    """
    Remove duplicate Ticket ID records.

    The first occurrence is retained.
    """

    duplicate_ids = int(
        df["ticket_id"].duplicated().sum()
    )

    if duplicate_ids > 0:

        report.append(
            f"Removed {duplicate_ids:,} duplicate Ticket ID records."
        )

        df = df.drop_duplicates(
            subset=["ticket_id"],
            keep="first"
        ).copy()

    return df

######   FINAL TEXT CLEANUP   ######

def final_text_cleanup(df):
    """
    Final cleanup of text columns.
    """

    text_columns = [
        "ticket_id",
        "customer_id",
        "issue_type",
        "resolved",
    ]

    for column in text_columns:

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

    df["ticket_id"] = (
        df["ticket_id"]
        .astype("string")
    )

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
    )

    df["ticket_date"] = pd.to_datetime(
        df["ticket_date"],
        errors="coerce"
    )

    df["issue_type"] = (
        df["issue_type"]
        .astype("string")
    )

    df["resolution_time_hours"] = pd.to_numeric(
        df["resolution_time_hours"],
        errors="coerce"
    )

    df["satisfaction_score"] = pd.to_numeric(
        df["satisfaction_score"],
        errors="coerce"
    )

    df["resolved"] = (
        df["resolved"]
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

        "Missing_Ticket_IDs": int(
            df["ticket_id"].isnull().sum()
        ),

        "Duplicate_Ticket_IDs": int(
            df["ticket_id"].duplicated().sum()
        ),

        "Missing_Customer_IDs": int(
            df["customer_id"].isnull().sum()
        ),

        "Unique_Ticket_IDs": int(
            df["ticket_id"].nunique()
        ),

        "Unique_Customer_IDs": int(
            df["customer_id"].nunique()
        ),

        "Missing_Ticket_Dates": int(
            df["ticket_date"].isnull().sum()
        ),

        "Missing_Issue_Types": int(
            df["issue_type"].isnull().sum()
        ),

        "Missing_Resolution_Time": int(
            df["resolution_time_hours"].isnull().sum()
        ),

        "Negative_Resolution_Time": int(
            (
                df["resolution_time_hours"] < 0
            ).sum()
        ),

        "Missing_Satisfaction_Score": int(
            df["satisfaction_score"].isnull().sum()
        ),

        "Invalid_Satisfaction_Score": int(
            (
                (
                    df["satisfaction_score"] < 1
                )
                |
                (
                    df["satisfaction_score"] > 5
                )
            )
            .fillna(False)
            .sum()
        ),

        "Missing_Resolved": int(
            df["resolved"].isnull().sum()
        ),

        "Cleaning_Issues": len(report),
    }

    # Resolved distribution
    
    summary["Resolved_Yes_Count"] = int(
        (
            df["resolved"]
            .astype("string")
            .str.lower()
            == "yes"
        ).sum()
    )

    summary["Resolved_No_Count"] = int(
        (
            df["resolved"]
            .astype("string")
            .str.lower()
            == "no"
        ).sum()
    )

    # Average resolution time    

    summary["Average_Resolution_Time_Hours"] = round(
        df["resolution_time_hours"]
        .mean(),
        2
    )

    # Average satisfaction score    

    summary["Average_Satisfaction_Score"] = round(
        df["satisfaction_score"]
        .mean(),
        2
    )

    return summary

######   MAIN CLEANING FUNCTION   ######

def clean_support_tickets(df):
    """
    Complete Support_Tickets cleaning pipeline.

    Returns:
        cleaned_df
        summary
        cleaning_report
    """

    df = df.copy()

    original_rows = len(df)

    report = []

    # Standardize column names    

    df = standardize_column_names(
        df
    )
    
    # Validate expected columns
    
    validate_columns(
        df
    )
    
    # Keep only expected columns
    
    df = df[
        EXPECTED_COLUMNS
    ].copy()
    
    # Clean Ticket IDs
    
    df = clean_ticket_ids(
        df,
        report
    )
    
    # Clean Customer IDs
    
    df = clean_customer_ids(
        df,
        report
    )
    
    # Clean Ticket Date
    
    df = clean_ticket_date(
        df,
        report
    )
    
    # Clean Issue Type
    
    df = clean_issue_type(
        df,
        report
    )
    
    # Clean Resolution Time
    
    df = clean_resolution_time(
        df,
        report
    )
    
    # Clean Satisfaction Score
    
    df = clean_satisfaction_score(
        df,
        report
    )
    
    # Clean Resolved
    
    df = clean_resolved(
        df,
        report
    )
    
    # Remove exact duplicate rows
    
    df = remove_duplicate_rows(
        df,
        report
    )
    
    # Remove duplicate Ticket IDs
    
    df = remove_duplicate_ticket_ids(
        df,
        report
    )
    
    # Final text cleanup
    
    df = final_text_cleanup(
        df
    )
    
    # Final data types
    
    df = finalize_data_types(
        df
    )
    
    # Rows removed
    
    rows_removed = (
        original_rows
        - len(df)
    )
    
    # Create summary
    
    summary = create_summary(
        df=df,
        original_rows=original_rows,
        rows_removed=rows_removed,
        report=report
    )

    return (
        df,
        summary,
        report
    )