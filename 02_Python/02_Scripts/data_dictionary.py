"""
CUSTOMER CHURN & RETENTION ANALYSIS
Data Dictionary Cleaning Pipeline

Purpose:
    Load the Data_Dictionary sheet from the raw workbook,
    clean it, and save the cleaned Data_Dictionary dataset
    and cleaning report.

Input:
    raw_data/Customer_Churn_Retention_Raw_Data.xlsx

Sheet:
    Data_Dictionary

Outputs:
    cleaned/data_dictionary_cleaned.xlsx
    outputs/cleaning_reports/data_dictionary_cleaning_report.xlsx
"""

from pathlib import Path
import sys
import pandas as pd


###### PROJECT PATHS   ######

# data_dictionary.py is located at:
#
# Customer_Churn/
#       Python/
#           02_Scripts/
#               data_dictionary.py
#
# Therefore:
# PYTHON_ROOT  → Customer_Churn/02_Python
# PROJECT_ROOT → Customer_Churn

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

###### CLEANER IMPORT PATH   ######

CLEANERS_PATH = PYTHON_ROOT / "03_Cleaners"

sys.path.insert(0, str(CLEANERS_PATH))


######   IMPORT DATA DICTIONARY CLEANER   ######

from data_dictionary_cleaner import (
    clean_data_dictionary
)


###### RAW DATA PATH   ######

RAW_EXCEL_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "01_Raw"
    / "Customer_Churn_Retention_Raw_Data.xlsx"
)


######   CLEANED DATA PATH   ######

CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

CLEANED_FILE = (
    CLEANED_DIR
    / "data_dictionary_cleaned.xlsx"
)


######   CLEANING REPORT PATH   ######

CLEANING_REPORT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "01_cleaning_reports"
)

CLEANING_REPORT_FILE = (
    CLEANING_REPORT_DIR
    / "data_dictionary_cleaning_report.xlsx"
)


######   SHEET NAME   ######

SHEET_NAME = "Data_Dictionary"

######   LOAD DATA   ######

def load_data_dictionary():
    """
    Load Data_Dictionary from raw Excel workbook.
    """

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("DATA DICTIONARY DATA CLEANING")
    print("\n")

    print("LOADING DATA DICTIONARY DATA")
    print("\n")

    print(
        f"\nRaw Excel File : {RAW_EXCEL_FILE}"
    )

    print(
        f"Sheet          : {SHEET_NAME}"
    )

    df = pd.read_excel(
        RAW_EXCEL_FILE,
        sheet_name=SHEET_NAME
    )

    print(
        f"\nRows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    print("\nColumns:")

    for column in df.columns:

        print(
            f"  - {column}"
        )

    return df


######   SAVE CLEANED DATA   ######

def save_cleaned_data(df):
    """
    Save cleaned Data_Dictionary data.
    """

    CLEANED_DIR.mkdir(
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


######   SAVE CLEANING REPORT   ######

def save_cleaning_report(
    summary,
    cleaning_issues
):
    """
    Save cleaning summary and issue details to Excel.
    """

    CLEANING_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    summary_df = pd.DataFrame(
        [
            {
                "Metric": key,
                "Value": value
            }
            for key, value in summary.items()
        ]
    )

    issues_df = pd.DataFrame(
        [
            {
                "Issue_Number": number,
                "Issue": issue
            }
            for number, issue in enumerate(
                cleaning_issues,
                start=1
            )
        ]
    )

    if issues_df.empty:

        issues_df = pd.DataFrame(
            columns=[
                "Issue_Number",
                "Issue"
            ]
        )

    with pd.ExcelWriter(
        CLEANING_REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Cleaning_Summary",
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
        CLEANING_REPORT_FILE
    )


######   MAIN   ######

def main():

    try:

        ###### Load

        df = load_data_dictionary()

        ###### Clean

        cleaned_df, summary, cleaning_issues = (
            clean_data_dictionary(df)
        )

        ###### Save cleaned data

        save_cleaned_data(
            cleaned_df
        )

        ###### Save report

        save_cleaning_report(
            summary,
            cleaning_issues
        )

        ######   Final output

        print("\n")
        print(
            "DATA DICTIONARY CLEANING COMPLETED"
        )
        print("\n")

    except FileNotFoundError as error:

        print("\nERROR: Required file not found.")
        print(error)

    except ValueError as error:

        print("\nERROR: Data Dictionary validation problem.")
        print(error)

    except Exception as error:

        print("\nERROR: Unexpected error occurred.")
        print(error)


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()