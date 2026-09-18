import pandas as pd
from pathlib import Path
import sys

# PROJECT PATHS

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

# CLEANER IMPORTS

CLEANERS_PATH = (
    PYTHON_ROOT
    / "03_Cleaners"
)

sys.path.insert(
    0,
    str(CLEANERS_PATH)
)

from cleaning_utils import (
    RAW_EXCEL_FILE,
    CLEANED_DATA_FOLDER,
    CLEANING_REPORT_FOLDER,
    create_project_directories,
    save_dataframe_to_excel,
    save_cleaning_report,
)

from subscription_cleaner import (
    clean_subscriptions
)

# SUBSCRIPTIONS CLEANING PIPELINE

def run_subscriptions_cleaning():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("SUBSCRIPTIONS DATA CLEANING PIPELINE")
    print("\n")
    
    # CREATE REQUIRED DIRECTORIES    

    create_project_directories()
    
    # LOAD SUBSCRIPTIONS SHEET
    
    print("\nLoading Subscriptions sheet...")
    subscriptions = pd.read_excel(
        RAW_EXCEL_FILE,
        sheet_name="subscriptions"
    )

    print(
        f"Subscriptions rows loaded : "
        f"{len(subscriptions):,}"
    )

    print(
        f"Subscriptions columns     : "
        f"{len(subscriptions.columns)}"
    )
    
    # CLEAN SUBSCRIPTIONS  

    (
        cleaned_subscriptions,
        cleaning_report,
        cleaning_summary
    ) = clean_subscriptions(
        subscriptions
    )
   
    # SAVE CLEANED DATA
    
    cleaned_file = (
        CLEANED_DATA_FOLDER
        / "subscriptions_cleaned.xlsx"
    )

    save_dataframe_to_excel(
        cleaned_subscriptions,
        cleaned_file,
        sheet_name="Subscriptions"
    )
    
    # SAVE CLEANING REPORT   

    cleaning_report_file = (
        CLEANING_REPORT_FOLDER
        / "subscriptions_cleaning_report.xlsx"
    )

    save_cleaning_report(
        cleaning_report,
        cleaning_report_file
    )
  
    # DISPLAY SUMMARY    

    print("\n")
    print("SUBSCRIPTIONS CLEANING SUMMARY")
    print("\n")

    for key, value in cleaning_summary.items():

        print(
            f"{key:<35}: {value}"
        )

    print("\n")
    print("Cleaned Subscriptions file:")
    print(cleaned_file)

    print("\n")
    print("Cleaning report:")
    print(cleaning_report_file)

    print(
        "\nSubscriptions data cleaning "
        "completed successfully."
    )

    return (
        cleaned_subscriptions,
        cleaning_report,
        cleaning_summary
    )

# RUN PIPELINE

if __name__ == "__main__":

    run_subscriptions_cleaning()