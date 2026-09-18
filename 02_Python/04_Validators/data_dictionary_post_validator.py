"""
CUSTOMER CHURN & RETENTION ANALYSIS
Data Dictionary Post-Cleaning Validator

Purpose:
    Validate the cleaned Data_Dictionary dataset.

Input:
    cleaned/data_dictionary_cleaned.xlsx

Output:
    outputs/validation_reports/
        data_dictionary_post_cleaning_validation_report.xlsx
"""

from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED DATA DICTIONARY   ######

CLEANED_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "data_dictionary_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "data_dictionary_post_cleaning_validation_report.xlsx"
)


######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "table",
    "column",
    "description",
    "data_type",
    "notes",
]


######   VALIDATION STORAGE   ######

validation_results = []

def add_check(
    check,
    value,
    status,
    details
):
    """
    Add one validation check.
    """

    validation_results.append(
        {
            "Check": check,
            "Value": value,
            "Status": status,
            "Details": details,
        }
    )


######   LOAD CLEANED DATA   ######

def load_cleaned_data():
    """
    Load cleaned Data_Dictionary dataset.
    """
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("DATA DICTIONARY POST-CLEANING VALIDATION")
    print("\n")

    
    print("LOADING CLEANED DATA DICTIONARY")
    print("\n")

    print(
        f"\nFile : {CLEANED_FILE}"
    )

    df = pd.read_excel(
        CLEANED_FILE
    )

    print(
        f"\nRows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df


######   VALIDATE DATA DICTIONARY   ######

def validate_data_dictionary(df):
    """
    Perform post-cleaning validation.
    """

    print("DATA DICTIONARY POST-CLEANING VALIDATION")
    print("\n")

    
    # 1. EXPECTED COLUMNS
    

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

    expected_columns_present = (
        len(missing_columns) == 0
    )

    add_check(
        "Expected Columns Present",
        expected_columns_present,
        "PASS"
        if expected_columns_present
        else "FAIL",
        (
            "All expected Data_Dictionary columns are present."
            if expected_columns_present
            else (
                "Missing columns: "
                + ", ".join(missing_columns)
            )
        ),
    )
    
    # 2. UNEXPECTED COLUMNS
    
    add_check(
        "Unexpected Columns",
        len(unexpected_columns),
        "INFO"
        if len(unexpected_columns) == 0
        else "INFO",
        (
            "No unexpected columns."
            if len(unexpected_columns) == 0
            else (
                "Unexpected columns: "
                + ", ".join(unexpected_columns)
            )
        ),
    )
    
    # STOP IF REQUIRED COLUMNS ARE MISSING
    
    if missing_columns:

        return pd.DataFrame(
            validation_results
        )
    
    # 3. ROW COUNT
    
    row_count = len(df)

    add_check(
        "Total Rows",
        row_count,
        "INFO",
        "Number of Data_Dictionary records."
    )
    
    # 4. COLUMN COUNT
    
    column_count = len(df.columns)

    add_check(
        "Total Columns",
        column_count,
        "INFO",
        "Number of Data_Dictionary columns."
    )
    
    # 5. TOTAL MISSING VALUES
    
    total_missing = (
        df.isna()
        .sum()
        .sum()
    )

    add_check(
        "Total Missing Values",
        int(total_missing),
        "INFO"
        if total_missing > 0
        else "PASS",
        (
            "No missing values."
            if total_missing == 0
            else (
                f"{total_missing:,} missing values found. "
                "Review because some metadata fields may legitimately "
                "be optional."
            )
        ),
    )
    
    # 6. MISSING VALUES BY COLUMN
    
    for column in EXPECTED_COLUMNS:

        missing_count = (
            df[column]
            .isna()
            .sum()
        )

        if missing_count == 0:

            status = "PASS"

            details = "No missing values."

        else:

            status = "INFO"

            details = (
                f"{missing_count:,} missing values found."
            )

        add_check(
            f"Missing Values - {column}",
            int(missing_count),
            status,
            details,
        )
    
    # 7. BLANK TABLE NAMES
    
    blank_tables = (
        df["table"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    add_check(
        "Blank Table Names",
        int(blank_tables),
        "PASS"
        if blank_tables == 0
        else "FAIL",
        (
            "No blank Table names."
            if blank_tables == 0
            else f"{blank_tables:,} blank Table names found."
        ),
    )
    
    # 8. BLANK COLUMN NAMES
    
    blank_columns = (
        df["column"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    add_check(
        "Blank Column Names",
        int(blank_columns),
        "PASS"
        if blank_columns == 0
        else "FAIL",
        (
            "No blank Column names."
            if blank_columns == 0
            else f"{blank_columns:,} blank Column names found."
        ),
    )
    
    # 9. DUPLICATE ROWS
    
    duplicate_rows = (
        df.duplicated()
        .sum()
    )

    add_check(
        "Duplicate Rows",
        int(duplicate_rows),
        "PASS"
        if duplicate_rows == 0
        else "FAIL",
        (
            "No duplicate rows."
            if duplicate_rows == 0
            else f"{duplicate_rows:,} duplicate rows found."
        ),
    )
    
    # 10. DUPLICATE TABLE + COLUMN DEFINITIONS
    
    duplicate_definitions = (
        df.duplicated(
            subset=[
                "table",
                "column"
            ]
        )
        .sum()
    )

    add_check(
        "Duplicate Table + Column Definitions",
        int(duplicate_definitions),
        "PASS"
        if duplicate_definitions == 0
        else "FAIL",
        (
            "Each Table + Column combination has one definition."
            if duplicate_definitions == 0
            else (
                f"{duplicate_definitions:,} duplicate "
                "Table + Column definitions found."
            )
        ),
    )
    
    # 11. UNIQUE TABLE COUNT
    
    unique_tables = (
        df["table"]
        .dropna()
        .nunique()
    )

    add_check(
        "Unique Tables",
        int(unique_tables),
        "INFO",
        "Number of unique tables documented."
    )
    
    # 12. UNIQUE COLUMN COUNT
    
    unique_columns = (
        df["column"]
        .dropna()
        .nunique()
    )

    add_check(
        "Unique Columns",
        int(unique_columns),
        "INFO",
        "Number of unique column names documented."
    )
    
    # 13. MISSING DESCRIPTIONS
    
    missing_descriptions = (
        df["description"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Descriptions",
        int(missing_descriptions),
        "INFO"
        if missing_descriptions > 0
        else "PASS",
        (
            "All documented columns have descriptions."
            if missing_descriptions == 0
            else (
                f"{missing_descriptions:,} records have "
                "missing descriptions."
            )
        ),
    )
    
    # 14. MISSING DATA TYPES
    
    missing_data_types = (
        df["data_type"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Data Types",
        int(missing_data_types),
        "INFO"
        if missing_data_types > 0
        else "PASS",
        (
            "All documented columns have Data Types."
            if missing_data_types == 0
            else (
                f"{missing_data_types:,} records have "
                "missing Data Types."
            )
        ),
    )
    
    # 15. MISSING NOTES
    
    missing_notes = (
        df["notes"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Notes",
        int(missing_notes),
        "INFO"
        if missing_notes > 0
        else "PASS",
        (
            "No missing Notes."
            if missing_notes == 0
            else (
                f"{missing_notes:,} records have missing Notes. "
                "Notes may be optional metadata."
            )
        ),
    )
    
    # 16. TABLE NAME DATA TYPE
    
    table_dtype = str(
        df["table"].dtype
    )

    add_check(
        "Table Data Type",
        table_dtype,
        "INFO",
        "Table names should be stored as text."
    )
    
    # 17. COLUMN NAME DATA TYPE
    
    column_dtype = str(
        df["column"].dtype
    )

    add_check(
        "Column Data Type",
        column_dtype,
        "INFO",
        "Column names should be stored as text."
    )
    
    # 18. DESCRIPTION DATA TYPE
    
    description_dtype = str(
        df["description"].dtype
    )

    add_check(
        "Description Data Type",
        description_dtype,
        "INFO",
        "Descriptions should be stored as text."
    )
    
    # 19. DATA TYPE DATA TYPE
    
    data_type_dtype = str(
        df["data_type"].dtype
    )

    add_check(
        "Data Type Field Data Type",
        data_type_dtype,
        "INFO",
        "Data_Type values should be stored as text."
    )
    
    # 20. NOTES DATA TYPE
    
    notes_dtype = str(
        df["notes"].dtype
    )

    add_check(
        "Notes Data Type",
        notes_dtype,
        "INFO",
        "Notes should be stored as text."
    )
    
    # 21. TABLE NAME CASE CHECK
    
    non_lowercase_tables = (
        df["table"]
        .dropna()
        .astype(str)
        .ne(
            df["table"]
            .dropna()
            .astype(str)
            .str.lower()
        )
        .sum()
    )

    add_check(
        "Non-Lowercase Table Names",
        int(non_lowercase_tables),
        "PASS"
        if non_lowercase_tables == 0
        else "INFO",
        (
            "All Table names are lowercase."
            if non_lowercase_tables == 0
            else (
                f"{non_lowercase_tables:,} Table names "
                "are not lowercase."
            )
        ),
    )
    
    # 22. NON-LOWERCASE COLUMN NAMES
    
    non_lowercase_columns = (
        df["column"]
        .dropna()
        .astype(str)
        .ne(
            df["column"]
            .dropna()
            .astype(str)
            .str.lower()
        )
        .sum()
    )

    add_check(
        "Non-Lowercase Column Names",
        int(non_lowercase_columns),
        "PASS"
        if non_lowercase_columns == 0
        else "INFO",
        (
            "All Column names are lowercase."
            if non_lowercase_columns == 0
            else (
                f"{non_lowercase_columns:,} Column names "
                "are not lowercase."
            )
        ),
    )
    
    # 23. EMPTY DATA DICTIONARY
    
    empty_dictionary = (
        len(df) == 0
    )

    add_check(
        "Data Dictionary Contains Records",
        not empty_dictionary,
        "PASS"
        if not empty_dictionary
        else "FAIL",
        (
            "Data_Dictionary contains records."
            if not empty_dictionary
            else "Data_Dictionary contains no records."
        ),
    )
    
    # 24. OVERALL VALIDATION
    
    critical_failures = (
        missing_columns
        or blank_tables > 0
        or blank_columns > 0
        or duplicate_rows > 0
        or duplicate_definitions > 0
        or empty_dictionary
    )

    overall_status = (
        "FAIL"
        if critical_failures
        else "PASS"
    )

    add_check(
        "Overall Data Dictionary Validation",
        overall_status,
        overall_status,
        (
            "Data_Dictionary passed all critical "
            "post-cleaning validation checks."
            if overall_status == "PASS"
            else (
                "Data_Dictionary contains critical "
                "validation issues that require investigation."
            )
        ),
    )

    return pd.DataFrame(
        validation_results
    )


######   CREATE SUMMARY   ######

def create_validation_summary(validation_df):
    """
    Create validation summary.
    """

    total_checks = len(
        validation_df
    )

    passed_checks = (
        validation_df["Status"]
        .eq("PASS")
        .sum()
    )

    failed_checks = (
        validation_df["Status"]
        .eq("FAIL")
        .sum()
    )

    info_checks = (
        validation_df["Status"]
        .eq("INFO")
        .sum()
    )

    summary = pd.DataFrame(
        [
            {
                "Metric": "Rows",
                "Value": len(validation_df),
            },
            {
                "Metric": "Total Checks",
                "Value": total_checks,
            },
            {
                "Metric": "Passed Checks",
                "Value": passed_checks,
            },
            {
                "Metric": "Failed Checks",
                "Value": failed_checks,
            },
            {
                "Metric": "Info Checks",
                "Value": info_checks,
            },
        ]
    )

    return summary


######   PRINT RESULTS   ######

def print_results(
    validation_df,
    summary_df
):
    """
    Print validation results.
    """

    print("DATA DICTIONARY POST-CLEANING VALIDATION RESULTS")
    print("\n")

    print(
        validation_df[
            [
                "Check",
                "Value",
                "Status",
                "Details"
            ]
        ].to_string(
            index=False
        )
    )

    print("VALIDATION SUMMARY")
    print("\n")

    print(
        summary_df.to_string(
            index=False
        )
    )


######   SAVE VALIDATION REPORT   ######

def save_validation_report(
    validation_df,
    summary_df,
    df
):
    """
    Save validation report to Excel.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    
    # Create table summary
    
    table_summary = (
        df.groupby(
            "table",
            dropna=False
        )
        .size()
        .reset_index(
            name="Column_Count"
        )
    )
    
    # Create duplicate definition report
    
    duplicate_definitions = (
        df[
            df.duplicated(
                subset=[
                    "table",
                    "column"
                ],
                keep=False
            )
        ]
        .sort_values(
            [
                "table",
                "column"
            ]
        )
    )

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        validation_df.to_excel(
            writer,
            sheet_name="Validation_Details",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Validation_Summary",
            index=False
        )

        table_summary.to_excel(
            writer,
            sheet_name="Table_Summary",
            index=False
        )

        if len(duplicate_definitions) > 0:

            duplicate_definitions.to_excel(
                writer,
                sheet_name="Duplicate_Definitions",
                index=False
            )

        else:

            pd.DataFrame(
                {
                    "Message": [
                        "No duplicate Table + Column definitions found."
                    ]
                }
            ).to_excel(
                writer,
                sheet_name="Duplicate_Definitions",
                index=False
            )

    print("VALIDATION REPORT SAVED")
    print("\n")

    print(
        OUTPUT_FILE
    )


######   MAIN   ######

def main():

    try:

        # Load
        
        df = load_cleaned_data()

        # Validate        

        validation_df = validate_data_dictionary(
            df
        )
        
        # Summary

        summary_df = create_validation_summary(
            validation_df
        )
        
        # Print
        
        print_results(
            validation_df,
            summary_df
        )
        
        # Save
        
        save_validation_report(
            validation_df,
            summary_df,
            df
        )

        print("\n")
        print(
            "DATA DICTIONARY POST-CLEANING "
            "VALIDATION COMPLETED"
        )

    except FileNotFoundError as error:

        print("\nERROR: Cleaned Data_Dictionary file not found.")
        print(error)

    except Exception as error:

        print("\nERROR: Unexpected error occurred.")
        print(error)


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()