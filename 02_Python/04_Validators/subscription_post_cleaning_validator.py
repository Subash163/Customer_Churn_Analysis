from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED SUBSCRIPTIONS DATA   ######

CLEANED_SUBSCRIPTIONS_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "subscriptions_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

VALIDATION_REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

VALIDATION_REPORT_FILE = (
    VALIDATION_REPORT_FOLDER
    / "subscriptions_post_cleaning_validation.xlsx"
)

######   EXPECTED STRUCTURE   ######

EXPECTED_COLUMNS = [
    "customer_id",
    "subscription_id",
    "plan",
    "contract_type",
    "start_date",
    "end_date",
    "monthly_charge",
    "churn_status",
    "churn_date"
]


VALID_PLANS = {
    "basic",
    "standard",
    "premium"
}


VALID_CONTRACT_TYPES = {
    "monthly",
    "one year",
    "two year"
}


VALID_CHURN_STATUS = {
    "active",
    "churned"
}


######   LOAD CLEANED DATA   ######

def load_cleaned_subscriptions():

    print("\nLoading cleaned Subscriptions data...")

    if not CLEANED_SUBSCRIPTIONS_FILE.exists():

        raise FileNotFoundError(
            f"\nCleaned Subscriptions file not found:\n"
            f"{CLEANED_SUBSCRIPTIONS_FILE}\n\n"
            f"Run the Subscriptions cleaning pipeline first."
        )

    df = pd.read_excel(
        CLEANED_SUBSCRIPTIONS_FILE,
        sheet_name="Subscriptions"
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df


######   1. COLUMN STRUCTURE   ######

def validate_columns(df, report):

    print("\nSTEP 1 - Validating column structure")

    actual_columns = list(df.columns)

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

    if not missing_columns and not unexpected_columns:

        status = "PASS"

        issue = (
            "All expected Subscriptions columns are present"
        )

    else:

        status = "FAIL"

        issue = (
            f"Missing columns: {missing_columns}; "
            f"Unexpected columns: {unexpected_columns}"
        )

    report.append({
        "check": "Column Structure",
        "column": "ALL",
        "status": status,
        "issue": issue,
        "records_affected": 0
    })


######   2. CUSTOMER ID   ######

def validate_customer_id(df, report):

    print("\nSTEP 2 - Validating customer_id")

    missing_count = (
        df["customer_id"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing Customer IDs",
        "column": "customer_id",
        "status": (
            "PASS"
            if missing_count == 0
            else "FAIL"
        ),
        "issue": (
            "No missing customer IDs"
            if missing_count == 0
            else "Missing customer IDs found"
        ),
        "records_affected": int(missing_count)
    })

    duplicate_count = (
        df["customer_id"]
        .duplicated()
        .sum()
    )

    report.append({
        "check": "Duplicate Customer IDs",
        "column": "customer_id",
        "status": (
            "PASS"
            if duplicate_count == 0
            else "INFO"
        ),
        "issue": (
            "Each customer has one subscription record"
            if duplicate_count == 0
            else "Multiple subscription records found for customers"
        ),
        "records_affected": int(duplicate_count)
    })


######   3. SUBSCRIPTION ID   ######

def validate_subscription_id(df, report):

    print("\nSTEP 3 - Validating subscription_id")

    missing_count = (
        df["subscription_id"]
        .isna()
        .sum()
    )

    duplicate_count = (
        df["subscription_id"]
        .duplicated()
        .sum()
    )

    report.append({
        "check": "Missing Subscription IDs",
        "column": "subscription_id",
        "status": (
            "PASS"
            if missing_count == 0
            else "FAIL"
        ),
        "issue": (
            "No missing subscription IDs"
            if missing_count == 0
            else "Missing subscription IDs found"
        ),
        "records_affected": int(missing_count)
    })

    report.append({
        "check": "Duplicate Subscription IDs",
        "column": "subscription_id",
        "status": (
            "PASS"
            if duplicate_count == 0
            else "FAIL"
        ),
        "issue": (
            "All subscription IDs are unique"
            if duplicate_count == 0
            else "Duplicate subscription IDs found"
        ),
        "records_affected": int(duplicate_count)
    })


######   4. PLAN   ######

def validate_plan(df, report):

    print("\nSTEP 4 - Validating Plan")

    values = (
        df["plan"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~values.isin(VALID_PLANS)
    ).sum()

    missing_count = (
        df["plan"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Plan Categories",
        "column": "plan",
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        ),
        "issue": (
            "All plan values are valid"
            if invalid_count == 0
            else "Invalid plan values found"
        ),
        "records_affected": int(invalid_count)
    })

    report.append({
        "check": "Missing Plan",
        "column": "plan",
        "status": (
            "PASS"
            if missing_count == 0
            else "INFO"
        ),
        "issue": (
            "No missing plan values"
            if missing_count == 0
            else "Missing plan values remain"
        ),
        "records_affected": int(missing_count)
    })


######   5. CONTRACT TYPE   ######

def validate_contract_type(df, report):

    print("\nSTEP 5 - Validating Contract Type")

    values = (
        df["contract_type"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~values.isin(
            VALID_CONTRACT_TYPES
        )
    ).sum()

    missing_count = (
        df["contract_type"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Contract Type Categories",
        "column": "contract_type",
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        ),
        "issue": (
            "All contract types are valid"
            if invalid_count == 0
            else "Invalid contract types found"
        ),
        "records_affected": int(invalid_count)
    })

    report.append({
        "check": "Missing Contract Type",
        "column": "contract_type",
        "status": (
            "PASS"
            if missing_count == 0
            else "INFO"
        ),
        "issue": (
            "No missing contract types"
            if missing_count == 0
            else "Missing contract types remain"
        ),
        "records_affected": int(missing_count)
    })


######   6. MONTHLY CHARGE   ######

def validate_monthly_charge(df, report):

    print("\nSTEP 6 - Validating Monthly Charge")

    # Data type
    numeric = pd.api.types.is_numeric_dtype(
        df["monthly_charge"]
    )

    report.append({
        "check": "Monthly Charge Data Type",
        "column": "monthly_charge",
        "status": (
            "PASS"
            if numeric
            else "FAIL"
        ),
        "issue": (
            "Monthly charge is numeric"
            if numeric
            else "Monthly charge is not numeric"
        ),
        "records_affected": 0
    })

    # Missing
    missing_count = (
        df["monthly_charge"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing Monthly Charge",
        "column": "monthly_charge",
        "status": (
            "PASS"
            if missing_count == 0
            else "INFO"
        ),
        "issue": (
            "No missing monthly charges"
            if missing_count == 0
            else "Missing monthly charges remain"
        ),
        "records_affected": int(missing_count)
    })

    # Negative
    negative_count = (
        (
            df["monthly_charge"] < 0
        )
        .fillna(False)
        .sum()
    )

    report.append({
        "check": "Negative Monthly Charge",
        "column": "monthly_charge",
        "status": (
            "PASS"
            if negative_count == 0
            else "FAIL"
        ),
        "issue": (
            "No negative monthly charges"
            if negative_count == 0
            else "Negative monthly charges found"
        ),
        "records_affected": int(negative_count)
    })


######   7. DATE DATA TYPES   ######

def validate_date_types(df, report):

    print("\nSTEP 7 - Validating date data types")

    date_columns = [
        "start_date",
        "end_date",
        "churn_date"
    ]

    for column in date_columns:

        is_datetime = (
            pd.api.types.is_datetime64_any_dtype(
                df[column]
            )
        )

        report.append({
            "check": "Date Data Type",
            "column": column,
            "status": (
                "PASS"
                if is_datetime
                else "FAIL"
            ),
            "issue": (
                f"{column} is datetime"
                if is_datetime
                else f"{column} is not datetime"
            ),
            "records_affected": 0
        })


######   8. START DATE   ######

def validate_start_date(df, report):

    print("\nSTEP 8 - Validating Start Date")

    missing_count = (
        df["start_date"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing Start Date",
        "column": "start_date",
        "status": (
            "PASS"
            if missing_count == 0
            else "FAIL"
        ),
        "issue": (
            "No missing start dates"
            if missing_count == 0
            else "Missing start dates found"
        ),
        "records_affected": int(missing_count)
    })

    today = pd.Timestamp.today().normalize()

    future_count = (
        (
            df["start_date"] > today
        )
        .fillna(False)
        .sum()
    )

    report.append({
        "check": "Future Start Date",
        "column": "start_date",
        "status": (
            "PASS"
            if future_count == 0
            else "FAIL"
        ),
        "issue": (
            "No future subscription start dates"
            if future_count == 0
            else "Future subscription start dates found"
        ),
        "records_affected": int(future_count)
    })


######   9. END DATE / START DATE LOGIC   ######

def validate_end_date_logic(df, report):

    print("\nSTEP 9 - Validating End Date Logic")

    invalid_count = (
        (
            df["end_date"]
            <
            df["start_date"]
        )
        .fillna(False)
        .sum()
    )

    report.append({
        "check": "End Date After Start Date",
        "column": "end_date",
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        ),
        "issue": (
            "All end dates are on or after start dates"
            if invalid_count == 0
            else "End dates before start dates found"
        ),
        "records_affected": int(invalid_count)
    })


######   10. CHURN STATUS   ######

def validate_churn_status(df, report):

    print("\nSTEP 10 - Validating Churn Status")

    values = (
        df["churn_status"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_count = (
        ~values.isin(
            VALID_CHURN_STATUS
        )
    ).sum()

    report.append({
        "check": "Churn Status Categories",
        "column": "churn_status",
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        ),
        "issue": (
            "All churn status values are valid"
            if invalid_count == 0
            else "Invalid churn status values found"
        ),
        "records_affected": int(invalid_count)
    })


######   11. CHURN DATE LOGIC   ######

def validate_churn_date_logic(df, report):

    print("\nSTEP 11 - Validating Churn Date Logic")
    
    # Active + Churn Date
    
    active_with_churn_date = (
        (
            df["churn_status"]
            .eq("Active")
        )
        &
        df["churn_date"].notna()
    )

    active_count = (
        active_with_churn_date.sum()
    )

    report.append({
        "check": "Active With Churn Date",
        "column": "churn_date",
        "status": (
            "PASS"
            if active_count == 0
            else "FAIL"
        ),
        "issue": (
            "Active subscriptions have no churn date"
            if active_count == 0
            else "Active subscriptions have churn dates"
        ),
        "records_affected": int(active_count)
    })
    
    # Churned Without Churn Date
    
    churned_without_date = (
        (
            df["churn_status"]
            .eq("Churned")
        )
        &
        df["churn_date"].isna()
    )

    churned_count = (
        churned_without_date.sum()
    )

    report.append({
        "check": "Churned Without Churn Date",
        "column": "churn_date",
        "status": (
            "PASS"
            if churned_count == 0
            else "FAIL"
        ),
        "issue": (
            "All churned subscriptions have churn dates"
            if churned_count == 0
            else "Churned subscriptions missing churn dates"
        ),
        "records_affected": int(churned_count)
    })
    
    # Churn Date Before Start Date
    
    invalid_dates = (
        (
            df["churn_date"]
            <
            df["start_date"]
        )
        .fillna(False)
        .sum()
    )

    report.append({
        "check": "Churn Date After Start Date",
        "column": "churn_date",
        "status": (
            "PASS"
            if invalid_dates == 0
            else "FAIL"
        ),
        "issue": (
            "All churn dates are on or after start dates"
            if invalid_dates == 0
            else "Churn dates before start dates found"
        ),
        "records_affected": int(invalid_dates)
    })


######   12. EXPECTED NULL ANALYSIS   ######

def validate_expected_missing_values(df, report):

    print("\nSTEP 12 - Validating Expected Missing Values")

    # Active subscriptions should normally have
    # no End Date and no Churn Date.

    active_count = (
        df["churn_status"]
        .eq("Active")
    ).sum()

    active_missing_end = (
        (
            df["churn_status"]
            .eq("Active")
        )
        &
        df["end_date"].isna()
    ).sum()

    active_missing_churn = (
        (
            df["churn_status"]
            .eq("Active")
        )
        &
        df["churn_date"].isna()
    ).sum()

    report.append({
        "check": "Expected Active End Dates",
        "column": "end_date",
        "status": "INFO",
        "issue": (
            "Active subscriptions without end dates: "
            f"{active_missing_end} of {active_count}"
        ),
        "records_affected": int(
            active_missing_end
        )
    })

    report.append({
        "check": "Expected Active Churn Dates",
        "column": "churn_date",
        "status": "INFO",
        "issue": (
            "Active subscriptions without churn dates: "
            f"{active_missing_churn} of {active_count}"
        ),
        "records_affected": int(
            active_missing_churn
        )
    })


######   13. DUPLICATE ROWS   ######

def validate_duplicate_rows(df, report):

    print("\nSTEP 13 - Validating duplicate rows")

    duplicate_count = (
        df.duplicated()
        .sum()
    )

    report.append({
        "check": "Duplicate Rows",
        "column": "ALL",
        "status": (
            "PASS"
            if duplicate_count == 0
            else "FAIL"
        ),
        "issue": (
            "No exact duplicate rows"
            if duplicate_count == 0
            else "Exact duplicate rows found"
        ),
        "records_affected": int(
            duplicate_count
        )
    })


######   14. TEXT WHITESPACE   ######

def validate_text_whitespace(df, report):

    print("\nSTEP 14 - Validating text whitespace")

    text_columns = [
        "customer_id",
        "subscription_id",
        "plan",
        "contract_type",
        "churn_status"
    ]

    for column in text_columns:

        whitespace_count = (
            df[column]
            .dropna()
            .astype(str)
            .apply(
                lambda x: x != x.strip()
            )
            .sum()
        )

        report.append({
            "check": "Text Whitespace",
            "column": column,
            "status": (
                "PASS"
                if whitespace_count == 0
                else "FAIL"
            ),
            "issue": (
                "No leading/trailing whitespace"
                if whitespace_count == 0
                else "Leading/trailing whitespace found"
            ),
            "records_affected": int(
                whitespace_count
            )
        })


######   15. GENERATE SUMMARY   ######

def generate_summary(df, report):

    total_checks = len(report)

    passed_checks = sum(
        1
        for item in report
        if item["status"] == "PASS"
    )

    failed_checks = sum(
        1
        for item in report
        if item["status"] == "FAIL"
    )

    info_checks = sum(
        1
        for item in report
        if item["status"] == "INFO"
    )

    summary = {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Total_Missing_Values": int(
            df.isna().sum().sum()
        ),

        "Duplicate_Rows": int(
            df.duplicated().sum()
        ),

        "Missing_Customer_IDs": int(
            df["customer_id"].isna().sum()
        ),

        "Duplicate_Customer_IDs": int(
            df["customer_id"].duplicated().sum()
        ),

        "Missing_Subscription_IDs": int(
            df["subscription_id"].isna().sum()
        ),

        "Duplicate_Subscription_IDs": int(
            df["subscription_id"].duplicated().sum()
        ),

        "Total_Checks": total_checks,

        "Passed_Checks": passed_checks,

        "Failed_Checks": failed_checks,

        "Info_Checks": info_checks
    }

    return summary


######   SAVE REPORT   ######

def save_validation_report(report, summary):

    VALIDATION_REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    report_df = pd.DataFrame(report)

    summary_df = pd.DataFrame(
        [summary]
    )

    with pd.ExcelWriter(
        VALIDATION_REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        report_df.to_excel(
            writer,
            sheet_name="Validation_Details",
            index=False
        )

    print(
        "\nValidation report saved:"
    )

    print(
        VALIDATION_REPORT_FILE
    )



######   MAIN PIPELINE   ######

def run_subscriptions_post_cleaning_validation():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("SUBSCRIPTIONS POST-CLEANING VALIDATION")
    print("\n")

    df = load_cleaned_subscriptions()

    report = []

    validate_columns(
        df,
        report
    )

    validate_customer_id(
        df,
        report
    )

    validate_subscription_id(
        df,
        report
    )

    validate_plan(
        df,
        report
    )

    validate_contract_type(
        df,
        report
    )

    validate_monthly_charge(
        df,
        report
    )

    validate_date_types(
        df,
        report
    )

    validate_start_date(
        df,
        report
    )

    validate_end_date_logic(
        df,
        report
    )

    validate_churn_status(
        df,
        report
    )

    validate_churn_date_logic(
        df,
        report
    )

    validate_expected_missing_values(
        df,
        report
    )

    validate_duplicate_rows(
        df,
        report
    )

    validate_text_whitespace(
        df,
        report
    )

    summary = generate_summary(
        df,
        report
    )

    save_validation_report(
        report,
        summary
    )
    
    # DISPLAY SUMMARY
    
    print("\n")
    print("SUBSCRIPTIONS POST-CLEANING VALIDATION SUMMARY")
    print("\n")
    for key, value in summary.items():

        print(
            f"{key:<35}: {value}"
        )

    print(
        "\nSubscriptions post-cleaning "
        "validation completed successfully."
    )


######   RUN   ######

if __name__ == "__main__":

    run_subscriptions_post_cleaning_validation()