from pathlib import Path
import sys
import pandas as pd

# PROJECT PATHS

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

# CLEANER IMPORT

CLEANERS_PATH = (
    PYTHON_ROOT
    / "03_Cleaners"
)

sys.path.insert(
    0,
    str(CLEANERS_PATH)
)

from support_tickets_cleaner import (
    clean_support_tickets
)

# RAW DATA PATH

RAW_EXCEL_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "01_Raw"
    / "Customer_Churn_Retention_Raw_Data.xlsx"
)

# CLEANED DATA PATH

CLEANED_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

CLEANED_FILE = (
    CLEANED_FOLDER
    / "support_tickets_cleaned.xlsx"
)

# CLEANING REPORT PATH

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "01_cleaning_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "support_tickets_cleaning_report.xlsx"
)

# LOAD SUPPORT TICKETS

def load_support_tickets():
    """
    Load Support_Tickets sheet from the raw Excel workbook.
    """

    print("\n")
    print("LOADING SUPPORT TICKETS DATA")
    print("\n")

    df = pd.read_excel(
        RAW_EXCEL_FILE,
        sheet_name="support_tickets"
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df

# SAVE CLEANED DATA

def save_cleaned_data(df):
    """
    Save cleaned Support_Tickets data.
    """

    CLEANED_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        CLEANED_FILE,
        index=False
    )

    print("\n")
    print("CLEANED DATA SAVED")
    print("\n")

    print(
        CLEANED_FILE
    )

# SAVE CLEANING REPORT

def save_cleaning_report(
    summary,
    report
):
    """
    Save cleaning summary and detailed cleaning issues.
    """

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    summary_df = pd.DataFrame(
        list(summary.items()),
        columns=[
            "Metric",
            "Value"
        ]
    )

    issues_df = pd.DataFrame(
        {
            "Issue": report
        }
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

        issues_df.to_excel(
            writer,
            sheet_name="Cleaning_Issues",
            index=False
        )

    print("\n")
    print("CLEANING REPORT SAVED")
    print("\n")

    print(
        REPORT_FILE
    )

# DISPLAY SUMMARY

def display_summary(summary):
    """
    Display cleaning summary in terminal.
    """

    print("\n")
    print("SUPPORT TICKETS CLEANING SUMMARY")
    print("\n")

    for metric, value in summary.items():

        print(
            f"{metric:<40}: {value}"
        )

# DISPLAY CLEANING ISSUES

def display_cleaning_issues(report):
    """
    Display detailed cleaning issues.
    """

    print("\n")
    print("CLEANING ISSUES")
    print("\n")

    if not report:

        print(
            "No cleaning issues detected."
        )

        return

    for number, issue in enumerate(
        report,
        start=1
    ):

        print(
            f"{number}. {issue}"
        )

# MAIN

def main():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("SUPPORT TICKETS DATA CLEANING")
    print("\n")
   
    # Load raw data    

    df = load_support_tickets()
    
    # Clean data
    
    (
        cleaned_df,
        summary,
        report
    ) = clean_support_tickets(
        df
    )
    
    # Save cleaned data
    
    save_cleaned_data(
        cleaned_df
    )
    
    # Save cleaning report
    
    save_cleaning_report(
        summary,
        report
    )
    
    # Display summary
    
    display_summary(
        summary
    )
    
    # Display cleaning issues
    
    display_cleaning_issues(
        report
    )
    
    # Completion message
    
    print("\n")
    print("SUPPORT TICKETS CLEANING COMPLETED")
    print("\n")

    print(
        f"Original rows : "
        f"{summary['Original_Rows']:,}"
    )

    print(
        f"Final rows    : "
        f"{summary['Rows']:,}"
    )

    print(
        f"Rows removed  : "
        f"{summary['Rows_Removed']:,}"
    )

    print(
        f"Cleaning issues : "
        f"{summary['Cleaning_Issues']}"
    )

    print(
        f"\nCleaned file  : "
        f"{CLEANED_FILE}"
    )

    print(
        f"Report file   : "
        f"{REPORT_FILE}"
    )


# SCRIPT ENTRY POINT

if __name__ == "__main__":
    main()