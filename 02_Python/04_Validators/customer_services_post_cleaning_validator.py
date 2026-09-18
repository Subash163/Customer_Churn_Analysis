from pathlib import Path
import pandas as pd

######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   CLEANED CUSTOMER SERVICES DATA   ######

CLEANED_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "customer_services_cleaned.xlsx"
)

######   VALIDATION REPORT   ######

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "customer_services_post_cleaning_validation_report.xlsx"
)


######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "customer_id",
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
]

SERVICE_COLUMNS = [
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
]

VALID_SERVICE_VALUES = {
    "yes",
    "no",
}


######   LOAD CLEANED DATA   ######

def load_cleaned_customer_services():
    """
    Load cleaned Customer_Services data.
    """

    print("LOADING CLEANED CUSTOMER SERVICES DATA")
    print("\n")

    df = pd.read_excel(
        CLEANED_FILE
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df


######   CHECK COLUMNS   ######

def check_columns(df):

    results = []

    actual_columns = list(
        df.columns
    )

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    unexpected_columns = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    results.append({
        "Check": "Expected Columns Present",
        "Value": len(missing_columns) == 0,
        "Status": (
            "PASS"
            if len(missing_columns) == 0
            else "FAIL"
        ),
        "Details": (
            "All expected columns are present."
            if len(missing_columns) == 0
            else f"Missing columns: {missing_columns}"
        ),
    })

    results.append({
        "Check": "Unexpected Columns",
        "Value": len(unexpected_columns),
        "Status": "INFO",
        "Details": (
            "No unexpected columns."
            if len(unexpected_columns) == 0
            else f"Unexpected columns: {unexpected_columns}"
        ),
    })

    return results


######   CHECK MISSING VALUES   ######

def check_missing_values(df):

    results = []

    total_missing = int(
        df.isnull().sum().sum()
    )

    results.append({
        "Check": "Total Missing Values",
        "Value": total_missing,
        "Status": (
            "PASS"
            if total_missing == 0
            else "INFO"
        ),
        "Details": (
            "No missing values."
            if total_missing == 0
            else f"{total_missing:,} missing values found."
        ),
    })

    for column in EXPECTED_COLUMNS:

        missing_count = int(
            df[column].isnull().sum()
        )

        results.append({
            "Check": f"Missing Values - {column}",
            "Value": missing_count,
            "Status": (
                "PASS"
                if missing_count == 0
                else "INFO"
            ),
            "Details": (
                "No missing values."
                if missing_count == 0
                else f"{missing_count:,} missing values found."
            ),
        })

    return results


######   CHECK DUPLICATE ROWS   ######

def check_duplicate_rows(df):

    duplicate_rows = int(
        df.duplicated().sum()
    )

    return [{
        "Check": "Duplicate Rows",
        "Value": duplicate_rows,
        "Status": (
            "PASS"
            if duplicate_rows == 0
            else "FAIL"
        ),
        "Details": (
            "No duplicate rows."
            if duplicate_rows == 0
            else f"{duplicate_rows:,} duplicate rows found."
        ),
    }]


######   CHECK CUSTOMER IDs   ######

def check_customer_ids(df):

    results = []

    missing_ids = int(
        df["customer_id"].isnull().sum()
    )

    duplicate_ids = int(
        df["customer_id"].duplicated().sum()
    )

    blank_ids = int(
        df["customer_id"]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    unique_ids = int(
        df["customer_id"].nunique()
    )

    results.append({
        "Check": "Missing Customer IDs",
        "Value": missing_ids,
        "Status": (
            "PASS"
            if missing_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No missing Customer IDs."
            if missing_ids == 0
            else f"{missing_ids:,} missing Customer IDs found."
        ),
    })

    results.append({
        "Check": "Duplicate Customer IDs",
        "Value": duplicate_ids,
        "Status": (
            "PASS"
            if duplicate_ids == 0
            else "FAIL"
        ),
        "Details": (
            "Customer IDs are unique."
            if duplicate_ids == 0
            else f"{duplicate_ids:,} duplicate Customer IDs found."
        ),
    })

    results.append({
        "Check": "Blank Customer IDs",
        "Value": blank_ids,
        "Status": (
            "PASS"
            if blank_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No blank Customer IDs."
            if blank_ids == 0
            else f"{blank_ids:,} blank Customer IDs found."
        ),
    })

    results.append({
        "Check": "Unique Customer IDs",
        "Value": unique_ids,
        "Status": "INFO",
        "Details": "Number of unique customers in Customer_Services.",
    })

    return results


######   CHECK SERVICE VALUES   ######

def check_service_values(df):

    results = []

    for column in SERVICE_COLUMNS:

        values = set(
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
        )

        unexpected_values = (
            values - VALID_SERVICE_VALUES
        )

        results.append({
            "Check": f"Unexpected Values - {column}",
            "Value": len(unexpected_values),
            "Status": (
                "PASS"
                if len(unexpected_values) == 0
                else "FAIL"
            ),
            "Details": (
                "Only Yes/No values found."
                if len(unexpected_values) == 0
                else (
                    "Unexpected values: "
                    f"{sorted(unexpected_values)}"
                )
            ),
        })

    return results


######   CHECK SERVICE DISTRIBUTIONS   ######

def check_service_distributions(df):

    results = []

    for column in SERVICE_COLUMNS:

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

        missing_count = int(
            df[column].isnull().sum()
        )

        results.append({
            "Check": f"{column} - Yes Count",
            "Value": yes_count,
            "Status": "INFO",
            "Details": "Number of customers using the service.",
        })

        results.append({
            "Check": f"{column} - No Count",
            "Value": no_count,
            "Status": "INFO",
            "Details": "Number of customers not using the service.",
        })

        results.append({
            "Check": f"{column} - Missing Count",
            "Value": missing_count,
            "Status": (
                "PASS"
                if missing_count == 0
                else "INFO"
            ),
            "Details": (
                "No missing service values."
                if missing_count == 0
                else f"{missing_count:,} missing service values."
            ),
        })

    return results


######   CHECK DATA TYPES   ######

def check_data_types(df):

    results = []

    results.append({
        "Check": "Customer ID Data Type",
        "Value": str(
            df["customer_id"].dtype
        ),
        "Status": "INFO",
        "Details": "Expected string/object type.",
    })

    for column in SERVICE_COLUMNS:

        results.append({
            "Check": f"{column} Data Type",
            "Value": str(
                df[column].dtype
            ),
            "Status": "INFO",
            "Details": "Expected string/object type.",
        })

    return results


######   RUN VALIDATION   ######

def run_validation(df):

    results = []

    results.extend(
        check_columns(df)
    )

    results.extend(
        check_missing_values(df)
    )

    results.extend(
        check_duplicate_rows(df)
    )

    results.extend(
        check_customer_ids(df)
    )

    results.extend(
        check_service_values(df)
    )

    results.extend(
        check_service_distributions(df)
    )

    results.extend(
        check_data_types(df)
    )

    return pd.DataFrame(
        results
    )


######   CREATE SUMMARY   ######

def create_summary(
    df,
    validation_df
):

    passed = int(
        (
            validation_df["Status"]
            == "PASS"
        ).sum()
    )

    failed = int(
        (
            validation_df["Status"]
            == "FAIL"
        ).sum()
    )

    info = int(
        (
            validation_df["Status"]
            == "INFO"
        ).sum()
    )

    summary = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Total_Missing_Values",
            "Duplicate_Rows",
            "Missing_Customer_IDs",
            "Duplicate_Customer_IDs",
            "Unique_Customer_IDs",
            "Mobile_App_Missing",
            "Streaming_Missing",
            "Cloud_Storage_Missing",
            "Premium_Support_Missing",
            "Family_Plan_Missing",
            "Total_Checks",
            "Passed_Checks",
            "Failed_Checks",
            "Info_Checks",
        ],

        "Value": [
            len(df),
            len(df.columns),
            int(
                df.isnull().sum().sum()
            ),
            int(
                df.duplicated().sum()
            ),
            int(
                df["customer_id"].isnull().sum()
            ),
            int(
                df["customer_id"].duplicated().sum()
            ),
            int(
                df["customer_id"].nunique()
            ),
            int(
                df["mobile_app"].isnull().sum()
            ),
            int(
                df["streaming"].isnull().sum()
            ),
            int(
                df["cloud_storage"].isnull().sum()
            ),
            int(
                df["premium_support"].isnull().sum()
            ),
            int(
                df["family_plan"].isnull().sum()
            ),
            len(validation_df),
            passed,
            failed,
            info,
        ],
    })

    return summary


######   SAVE VALIDATION REPORT   ######

def save_validation_report(
    validation_df,
    summary
):

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        validation_df.to_excel(
            writer,
            sheet_name="Validation_Results",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

    print("VALIDATION REPORT SAVED")
    print("\n")

    print(
        REPORT_FILE
    )


######   DISPLAY RESULTS   ######

def display_results(
    validation_df,
    summary
):

    print("CUSTOMER SERVICES POST-CLEANING VALIDATION")
    print("\n")

    print(
        validation_df.to_string(
            index=False
        )
    )

    print("VALIDATION SUMMARY")
    print("\n")

    print(
        summary.to_string(
            index=False
        )
    )


######   MAIN   ######

def main():

    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("CUSTOMER SERVICES POST-CLEANING VALIDATION")
    print("\n")
    
    # Load cleaned data
    
    df = load_cleaned_customer_services()
    
    # Run validation
    
    validation_df = run_validation(
        df
    )
    
    # Create summary
    
    summary = create_summary(
        df,
        validation_df
    )
    
    # Display results
    
    display_results(
        validation_df,
        summary
    )
    
    # Save report
    
    save_validation_report(
        validation_df,
        summary
    )
    
    # Completion
    
    print(
        "CUSTOMER SERVICES POST-CLEANING "
        "VALIDATION COMPLETED"
    )


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()