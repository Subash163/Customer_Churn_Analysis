"""
CUSTOMER CHURN & RETENTION ANALYSIS
Data Dictionary Cleaner

Purpose:
    Clean and standardize the Data_Dictionary sheet.

Important:
    Data_Dictionary is metadata/documentation.
    It should NOT be treated like an operational dataset.

Input:
    Raw Excel -> Data_Dictionary sheet

Output:
    Cleaned Data_Dictionary DataFrame
"""

import pandas as pd

######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "table",
    "column",
    "description",
    "data_type",
    "notes",
]

######   COLUMN STANDARDIZATION   ######

COLUMN_MAPPING = {
    "Table": "table",
    "Column": "column",
    "Description": "description",
    "Data_Type": "data_type",
    "Notes": "notes",
}

######   CLEAN DATA DICTIONARY   ######

def clean_data_dictionary(df):
    """
    Clean and standardize the Data_Dictionary dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw Data_Dictionary dataframe.

    Returns
    -------
    cleaned_df : pandas.DataFrame
        Cleaned dataframe.

    cleaning_report : dict
        Summary of cleaning operations.
    """

    print("DATA DICTIONARY CLEANING")
    print("\n")

    # COPY DATA    

    df = df.copy()

    original_rows = len(df)
    original_columns = len(df.columns)

    cleaning_issues = []
    
    # STANDARDIZE COLUMN NAMES
    
    df = df.rename(columns=COLUMN_MAPPING)
    
    # CHECK EXPECTED COLUMNS
    
    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required Data_Dictionary columns: "
            + ", ".join(missing_columns)
        )
    
    # KEEP EXPECTED COLUMNS
    
    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if unexpected_columns:

        cleaning_issues.append(
            f"Found unexpected columns: {', '.join(unexpected_columns)}."
        )

    df = df[EXPECTED_COLUMNS]
    
    # CLEAN STRING VALUES
    
    for column in EXPECTED_COLUMNS:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )
    
    # STANDARDIZE TABLE NAMES
    
    # Table names are metadata identifiers.
    # We standardize them to lowercase.

    df["table"] = (
        df["table"]
        .str.lower()
        .str.strip()
    )
    
    # STANDARDIZE COLUMN NAMES
    
    # Column names are technical field names.
    # We standardize them to lowercase.

    df["column"] = (
        df["column"]
        .str.lower()
        .str.strip()
    )
    
    # STANDARDIZE DATA TYPE
    
    # Data_Type is descriptive metadata.
    # We standardize whitespace but do not enforce a fixed category list.

    df["data_type"] = (
        df["data_type"]
        .str.strip()
    )
    
    # MISSING VALUE CHECKS
    
    for column in EXPECTED_COLUMNS:

        missing_count = df[column].isna().sum()

        if missing_count > 0:

            cleaning_issues.append(
                f"{column}: {missing_count:,} missing values found."
            )
    
    # BLANK VALUE CHECKS
    
    for column in EXPECTED_COLUMNS:

        blank_count = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if blank_count > 0:

            cleaning_issues.append(
                f"{column}: {blank_count:,} blank values found."
            )
    
    # REMOVE COMPLETELY EMPTY ROWS
    
    completely_empty_mask = df.isna().all(axis=1)

    completely_empty_rows = completely_empty_mask.sum()

    if completely_empty_rows > 0:

        df = df.loc[
            ~completely_empty_mask
        ].copy()

        cleaning_issues.append(
            f"Removed {completely_empty_rows:,} completely empty rows."
        )
    
    # REMOVE EXACT DUPLICATE ROWS
    
    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:

        df = df.drop_duplicates().copy()

        cleaning_issues.append(
            f"Removed {duplicate_rows:,} exact duplicate rows."
        )
    
    # CHECK DUPLICATE TABLE + COLUMN DEFINITIONS
    
    # A Data Dictionary should normally contain one definition
    # per table + column combination.

    duplicate_definition_mask = (
        df.duplicated(
            subset=["table", "column"],
            keep=False
        )
    )

    duplicate_definition_count = (
        duplicate_definition_mask.sum()
    )

    if duplicate_definition_count > 0:

        cleaning_issues.append(
            f"Found {duplicate_definition_count:,} records "
            "with duplicate Table + Column definitions."
        )
    
    # MISSING TABLE / COLUMN DEFINITIONS
    
    missing_table_count = df["table"].isna().sum()

    missing_column_count = df["column"].isna().sum()

    if missing_table_count > 0:

        cleaning_issues.append(
            f"Found {missing_table_count:,} rows with missing Table names."
        )

    if missing_column_count > 0:

        cleaning_issues.append(
            f"Found {missing_column_count:,} rows with missing Column names."
        )
    
    # CONVERT EMPTY STRINGS TO MISSING VALUES
    
    for column in EXPECTED_COLUMNS:

        df[column] = df[column].replace(
            "",
            pd.NA
        )
    
    # FINAL DATA TYPES
    
    for column in EXPECTED_COLUMNS:

        df[column] = df[column].astype("string")
    
    # SUMMARY
    
    final_rows = len(df)

    rows_removed = (
        original_rows
        - final_rows
    )

    total_missing_values = (
        df.isna().sum().sum()
    )

    summary = {
        "Rows": final_rows,
        "Columns": len(df.columns),
        "Original_Rows": original_rows,
        "Original_Columns": original_columns,
        "Rows_Removed": rows_removed,
        "Total_Missing_Values": int(total_missing_values),
        "Duplicate_Rows": int(df.duplicated().sum()),
        "Duplicate_Table_Column_Definitions": int(
            df.duplicated(
                subset=["table", "column"]
            ).sum()
        ),
        "Missing_Table_Names": int(
            df["table"].isna().sum()
        ),
        "Missing_Column_Names": int(
            df["column"].isna().sum()
        ),
        "Missing_Descriptions": int(
            df["description"].isna().sum()
        ),
        "Missing_Data_Types": int(
            df["data_type"].isna().sum()
        ),
        "Missing_Notes": int(
            df["notes"].isna().sum()
        ),
        "Unique_Tables": int(
            df["table"].dropna().nunique()
        ),
        "Unique_Columns": int(
            df["column"].dropna().nunique()
        ),
        "Cleaning_Issues": len(cleaning_issues),
    }
    
    # PRINT CLEANING SUMMARY
    
    print("DATA DICTIONARY CLEANING SUMMARY")
    print("\n")

    for key, value in summary.items():

        print(
            f"{key:<45}: {value}"
        )
    
    # PRINT CLEANING ISSUES
    
    print("CLEANING ISSUES")
    print("\n")

    if cleaning_issues:

        for number, issue in enumerate(
            cleaning_issues,
            start=1
        ):

            print(
                f"{number}. {issue}"
            )

    else:

        print("No cleaning issues found.")
    
    # RETURN
    
    return df, summary, cleaning_issues