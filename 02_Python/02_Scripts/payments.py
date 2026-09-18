"""
Payments Cleaning Pipeline
==========================

Project:
    Customer Churn & Retention Analysis

Purpose:
    Load raw Payments data,
    clean the data,
    save the cleaned Payments dataset,
    and generate a cleaning report.
"""

from pathlib import Path
import sys

import pandas as pd


# 1. PROJECT PATHS

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


# 2. CLEANER IMPORT

CLEANERS_PATH = (
    PYTHON_ROOT
    / "03_Cleaners"
)

sys.path.insert(
    0,
    str(CLEANERS_PATH)
)

from payments_cleaner import clean_payments


# 3. RAW DATA PATH

RAW_EXCEL_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "01_Raw"
    / "Customer_Churn_Retention_Raw_Data.xlsx"
)


# 4. OUTPUT PATHS

CLEANED_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

CLEANED_FILE = (
    CLEANED_FOLDER
    / "payments_cleaned.xlsx"
)

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "01_cleaning_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "payments_cleaning_report.xlsx"
)


# 5. LOAD PAYMENTS DATA

def load_payments():
    """
    Load the Payments sheet from the raw Excel workbook.
    """

    print("LOADING PAYMENTS DATA")
    print("\n")

    if not RAW_EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Raw Excel file not found:\n"
            f"{RAW_EXCEL_FILE}"
        )

    df = pd.read_excel(
        RAW_EXCEL_FILE,
        sheet_name="payments"
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    print()

    return df


# 6. SAVE CLEANED DATA

def save_cleaned_data(df):
    """
    Save cleaned Payments data.
    """

    CLEANED_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        CLEANED_FILE,
        index=False
    )

    print("CLEANED DATA SAVED")
    print("\n")

    print(
        CLEANED_FILE
    )

    print()


# 7. SAVE CLEANING REPORT

def save_cleaning_report(
    report,
    summary
):
    """
    Save cleaning issues and summary to Excel.
    """

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    report_df = pd.DataFrame(
        report
    )

    summary_df = pd.DataFrame(
        [
            summary
        ]
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        report_df.to_excel(
            writer,
            sheet_name="Cleaning_Issues",
            index=False
        )

    print("CLEANING REPORT SAVED")
    print("\n")

    print(
        REPORT_FILE
    )

    print()


# 8. DISPLAY SUMMARY

def display_summary(summary):
    """
    Display cleaning summary in terminal.
    """

    print("PAYMENTS CLEANING SUMMARY")
    print("\n")

    for key, value in summary.items():

        print(
            f"{key:<30}: {value}"
        )

    print()


# 9. MAIN FUNCTION

def main():

    print()
    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("PAYMENTS DATA CLEANING")
    print("\n")
    print()
   
    # Step 1: Load raw Payments    

    df = load_payments()

    original_rows = len(df)

    # Step 2: Clean Payments    

    (
        cleaned_df,
        report,
        summary
    ) = clean_payments(df)

    # Step 3: Save cleaned Payments    

    save_cleaned_data(
        cleaned_df
    )
   
    # Step 4: Save cleaning report    

    save_cleaning_report(
        report,
        summary
    )
    
    # Step 5: Display summary
    
    display_summary(
        summary
    )
    
    # Final output
    
    print("\n")
    print("PAYMENTS CLEANING COMPLETED")

    print(
        f"Original rows : {original_rows:,}"
    )

    print(
        f"Final rows    : {len(cleaned_df):,}"
    )

    print(
        f"Rows removed  : "
        f"{original_rows - len(cleaned_df):,}"
    )

    print()

    print(
        f"Cleaned file  : {CLEANED_FILE}"
    )

    print(
        f"Report file   : {REPORT_FILE}"
    )

    print()


# 10. PROGRAM ENTRY POINT


if __name__ == "__main__":
    main()