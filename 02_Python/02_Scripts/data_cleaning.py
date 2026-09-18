######   CUSTOMER CHURN & RETENTION ANALYSIS   ######
######   DATA CLEANING ORCHESTRATOR   ######

import pandas as pd
from pathlib import Path
import sys

###### PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

CLEANERS_PATH = PYTHON_ROOT / "03_Cleaners"

sys.path.insert(0, str(CLEANERS_PATH))


from cleaning_utils import (
    RAW_EXCEL_FILE,
    CLEANED_DATA_FOLDER,
    CLEANING_REPORT_FOLDER,
    create_project_directories,
    save_dataframe_to_excel,
    save_cleaning_report
)

from customer_cleaner import (
    clean_customers
)


######   1. RUN CUSTOMERS CLEANING   ######

def run_customers_cleaning():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("DATA CLEANING PIPELINE")

    ###### Create required folders

    create_project_directories()

    print("RAW EXCEL PATH:")
    print(RAW_EXCEL_FILE)
    print("FILE EXISTS:", RAW_EXCEL_FILE.exists())

    ###### Load Customers sheet

    print("\nLoading Customers sheet...")

    customers = pd.read_excel(
        RAW_EXCEL_FILE,
        sheet_name="customers"
    )

    print(
        f"Customers rows loaded : "
        f"{len(customers):,}"
    )

    print(
        f"Customers columns     : "
        f"{len(customers.columns):,}"
    )

    ###### Clean Customers sheet

    (
        cleaned_customers,
        cleaning_report,
        cleaning_summary
    ) = clean_customers(
        customers
    )

    ###### Save cleaned Customers data

    cleaned_customers_file = (
        CLEANED_DATA_FOLDER
        / "customers_cleaned.xlsx"
    )

    save_dataframe_to_excel(
        df=cleaned_customers,
        file_path=cleaned_customers_file,
        sheet_name="Customers"
    )

    ###### Save cleaning report

    cleaning_report_file = (
        CLEANING_REPORT_FOLDER
        / "customers_cleaning_report.xlsx"
    )

    save_cleaning_report(
        report=cleaning_report.to_dict(
            orient="records"
        ),
        file_path=cleaning_report_file
    )

    ###### Display final summary

    print("\n")
    print("CUSTOMERS CLEANING SUMMARY")
    print("\n")

    for key, value in cleaning_summary.items():

        print(
            f"{key:<30}: {value}"
        )

    print("\n")
    print(
        f"Cleaned Customers file:\n"
        f"{cleaned_customers_file}"
    )
    print("\n")

    print(
        f"\nCleaning report:\n"
        f"{cleaning_report_file}"
    )

    print("\nCustomers data cleaning completed successfully.")

    return (
        cleaned_customers,
        cleaning_report,
        cleaning_summary
    )


###### 2. MAIN   ######

if __name__ == "__main__":

    run_customers_cleaning()