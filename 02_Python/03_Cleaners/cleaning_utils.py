# CUSTOMER CHURN & RETENTION ANALYSIS
# COMMON CLEANING UTILITIES

from pathlib import Path
import pandas as pd

###### 1. PROJECT PATHS   ######

# Python root directory
# 03_Cleaners -> 02_Python
PYTHON_ROOT = Path(__file__).resolve().parents[1]

# Project root directory
# 02_Python -> Customer_Churn
PROJECT_ROOT = PYTHON_ROOT.parent

######   2. DATA FOLDERS   ######

# Raw data folder
RAW_DATA_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "01_Raw"
)

# Cleaned data folder
CLEANED_DATA_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

######   3. OUTPUT FOLDERS   ######

OUTPUT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
)

# Validation reports
VALIDATION_REPORT_FOLDER = (
    OUTPUT_FOLDER
    / "09_validation_reports"
)

# Cleaning reports
CLEANING_REPORT_FOLDER = (
    OUTPUT_FOLDER
    / "01_cleaning_reports"
)

# EDA charts
CHART_FOLDER = (
    OUTPUT_FOLDER
    / "02_eda"
    / "charts"
)

# Summary / aggregated outputs
SUMMARY_FOLDER = (
    OUTPUT_FOLDER
    / "06_aggregated_data"
)

######   4. FILE PATHS   ######

RAW_EXCEL_FILE = (
    RAW_DATA_FOLDER
    / "Customer_Churn_Retention_Raw_Data.xlsx"
)

######   3. CREATE REQUIRED DIRECTORIES   ######

def create_project_directories():
    """
    Create all required project directories
    if they do not already exist.
    """

    folders = [
        RAW_DATA_FOLDER,
        CLEANED_DATA_FOLDER,
        OUTPUT_FOLDER,
        VALIDATION_REPORT_FOLDER,
        CLEANING_REPORT_FOLDER,
        CHART_FOLDER,
        SUMMARY_FOLDER
    ]

    for folder in folders:
        folder.mkdir(
            parents=True,
            exist_ok=True
        )

######   4. STANDARDIZE COLUMN NAMES   ######

def standardize_column_names(df):
    """
    Convert column names into consistent snake_case format.

    Example:

    Customer ID      -> customer_id
    Monthly Charges  -> monthly_charges
    Contract-Type    -> contract_type
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    return df

######   5. CLEAN TEXT WHITESPACE   ######

def strip_text_columns(df):
    """
    Remove leading and trailing whitespace
    from all text columns.
    """

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df

######   6. CONVERT BLANK STRINGS TO MISSING VALUES   ######

def convert_blank_to_na(df):
    """
    Convert blank strings and whitespace-only strings
    into pandas missing values.
    """

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        blank_mask = (
            df[column]
            .astype("string")
            .str.strip()
            .eq("")
        )

        df.loc[
            blank_mask,
            column
        ] = pd.NA

    return df

######   7. CONVERT NUMERIC COLUMNS   ######

def convert_numeric_columns(df, columns):
    """
    Convert specified columns to numeric.

    Invalid values are converted to NaN.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df

######   8. CONVERT DATE COLUMNS   ######

def convert_date_columns(df, columns):
    """
    Convert specified columns to datetime.

    Invalid dates are converted to NaT.
    """

    df = df.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df

######   9. REMOVE EXACT DUPLICATES   ######

def remove_exact_duplicates(df):
    """
    Remove completely identical rows.

    Returns:
        cleaned dataframe
        number of duplicates removed
    """

    df = df.copy()

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        df = df.drop_duplicates(
            keep="first"
        ).copy()

    return df, int(duplicate_count)

######   10. GENERATE MISSING VALUE SUMMARY   ######

def missing_value_summary(df):
    """
    Generate missing-value summary.
    """

    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing_Count": [
            df[column].isna().sum()
            for column in df.columns
        ]
    })

    summary["Missing_Percentage"] = (
        summary["Missing_Count"]
        / len(df)
        * 100
    ).round(2)

    return summary

######   11. GENERATE DATASET SUMMARY   ######

def dataset_summary(df):
    """
    Generate basic dataset summary.
    """

    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Total_Missing_Values": int(
            df.isna().sum().sum()
        ),
        "Duplicate_Rows": int(
            df.duplicated().sum()
        )
    }

    return summary

######   12. ADD CLEANING REPORT RECORD   ###### 

def add_cleaning_report(
    report,
    step,
    column,
    issue,
    records_affected,
    action
):
    """
    Add one cleaning activity to the report list.
    """

    report.append({
        "Step": step,
        "Column": column,
        "Issue": issue,
        "Records_Affected": int(records_affected),
        "Action_Taken": action
    })

    return report
 
######    13. SAVE DATAFRAME TO EXCEL   ###### 

def save_dataframe_to_excel(
    df,
    file_path,
    sheet_name="Sheet1"
):
    """
    Save DataFrame to an Excel file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        file_path,
        sheet_name=sheet_name,
        index=False
    )

######    14. SAVE CLEANING REPORT   ###### 

def save_cleaning_report(
    report,
    file_path
):
    """
    Save cleaning report to Excel.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if report:

        report_df = pd.DataFrame(report)

    else:

        report_df = pd.DataFrame({
            "Step": [],
            "Column": [],
            "Issue": [],
            "Records_Affected": [],
            "Action_Taken": []
        })

    report_df.to_excel(
        file_path,
        index=False
    )

    return report_df