from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   CLEANED CUSTOMER DATA   ######

CLEANED_CUSTOMERS_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "customers_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

VALIDATION_REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

VALIDATION_REPORT_FILE = (
    VALIDATION_REPORT_FOLDER
    / "customers_post_cleaning_validation.xlsx"
)


######   EXPECTED CUSTOMERS STRUCTURE   ######

EXPECTED_COLUMNS = [
    "customer_id",
    "gender",
    "age",
    "city",
    "state",
    "signup_date"
]

VALID_GENDER_VALUES = {
    "male",
    "female",
    "other",
    "unknown"
}


######   LOAD CLEANED CUSTOMERS   ######

def load_cleaned_customers():

    print("\nLoading cleaned Customers data...")

    if not CLEANED_CUSTOMERS_FILE.exists():

        raise FileNotFoundError(
            f"\nCleaned Customers file not found:\n"
            f"{CLEANED_CUSTOMERS_FILE}\n\n"
            f"Run the Customers cleaning pipeline first."
        )

    df = pd.read_excel(
        CLEANED_CUSTOMERS_FILE,
        sheet_name="Customers"
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df


######   1. COLUMN STRUCTURE VALIDATION   ######

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
            "All expected Customers columns are present"
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


######   2. CUSTOMER ID VALIDATION   ######

def validate_customer_id(df, report):

    print("\nSTEP 2 - Validating customer_id")
    
    # Missing Customer IDs
    
    missing_count = (
        df["customer_id"]
        .isna()
        .sum()
    )

    if missing_count == 0:

        status = "PASS"

        issue = (
            "No missing customer IDs"
        )

    else:

        status = "FAIL"

        issue = (
            "Missing customer IDs found"
        )

    report.append({
        "check": "Missing Customer IDs",
        "column": "customer_id",
        "status": status,
        "issue": issue,
        "records_affected": int(missing_count)
    })
    
    # Duplicate Customer IDs
    
    duplicate_count = (
        df["customer_id"]
        .duplicated()
        .sum()
    )

    if duplicate_count == 0:

        status = "PASS"

        issue = (
            "All customer IDs are unique"
        )

    else:

        status = "FAIL"

        issue = (
            "Duplicate customer IDs found"
        )

    report.append({
        "check": "Duplicate Customer IDs",
        "column": "customer_id",
        "status": status,
        "issue": issue,
        "records_affected": int(duplicate_count)
    })


######   3. GENDER VALIDATION   ######

def validate_gender(df, report):

    print("\nSTEP 3 - Validating gender")

    gender_values = (
        df["gender"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_mask = (
        ~gender_values.isin(
            VALID_GENDER_VALUES
        )
    )

    invalid_count = (
        invalid_mask.sum()
    )

    if invalid_count == 0:

        status = "PASS"

        issue = (
            "All gender values are standardized"
        )

    else:

        status = "FAIL"

        issue = (
            "Invalid gender categories found"
        )

    report.append({
        "check": "Gender Categories",
        "column": "gender",
        "status": status,
        "issue": issue,
        "records_affected": int(invalid_count)
    })


######   4. AGE VALIDATION   ######

def validate_age(df, report):

    print("\nSTEP 4 - Validating age")

    
    # Data Type
    
    numeric_check = (
        pd.api.types.is_numeric_dtype(
            df["age"]
        )
    )

    if numeric_check:

        status = "PASS"

        issue = (
            "Age column is numeric"
        )

    else:

        status = "FAIL"

        issue = (
            "Age column is not numeric"
        )

    report.append({
        "check": "Age Data Type",
        "column": "age",
        "status": status,
        "issue": issue,
        "records_affected": 0
    })

    # Missing Age
    
    missing_age = (
        df["age"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing Age",
        "column": "age",
        "status": (
            "PASS"
            if missing_age == 0
            else "INFO"
        ),
        "issue": (
            "No missing age values"
            if missing_age == 0
            else "Missing age values remain"
        ),
        "records_affected": int(missing_age)
    })
    
    # Invalid Age
    
    invalid_age = (
        (
            (df["age"] < 0) |
            (df["age"] > 120)
        )
        .fillna(False)
        .sum()
    )

    if invalid_age == 0:

        status = "PASS"

        issue = (
            "All age values are within valid range"
        )

    else:

        status = "FAIL"

        issue = (
            "Invalid age values found"
        )

    report.append({
        "check": "Age Range",
        "column": "age",
        "status": status,
        "issue": issue,
        "records_affected": int(invalid_age)
    })


######   5. CITY VALIDATION   ######

def validate_city(df, report):

    print("\nSTEP 5 - Validating city")

    
    # Missing City
    

    missing_city = (
        df["city"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing City",
        "column": "city",
        "status": (
            "PASS"
            if missing_city == 0
            else "INFO"
        ),
        "issue": (
            "No missing city values"
            if missing_city == 0
            else "Missing city values remain"
        ),
        "records_affected": int(missing_city)
    })

    # Leading / Trailing Whitespace

    whitespace_count = (
        df["city"]
        .dropna()
        .astype(str)
        .apply(
            lambda x: x != x.strip()
        )
        .sum()
    )

    if whitespace_count == 0:

        status = "PASS"

        issue = (
            "No leading or trailing whitespace"
        )

    else:

        status = "FAIL"

        issue = (
            "Leading or trailing whitespace found"
        )

    report.append({
        "check": "City Whitespace",
        "column": "city",
        "status": status,
        "issue": issue,
        "records_affected": int(whitespace_count)
    })


######   6. STATE VALIDATION   ######

def validate_state(df, report):

    print("\nSTEP 6 - Validating state")

    missing_state = (
        df["state"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing State",
        "column": "state",
        "status": (
            "PASS"
            if missing_state == 0
            else "INFO"
        ),
        "issue": (
            "No missing state values"
            if missing_state == 0
            else "Missing state values remain"
        ),
        "records_affected": int(missing_state)
    })

    whitespace_count = (
        df["state"]
        .dropna()
        .astype(str)
        .apply(
            lambda x: x != x.strip()
        )
        .sum()
    )

    if whitespace_count == 0:

        status = "PASS"

        issue = (
            "No leading or trailing whitespace"
        )

    else:

        status = "FAIL"

        issue = (
            "Leading or trailing whitespace found"
        )

    report.append({
        "check": "State Whitespace",
        "column": "state",
        "status": status,
        "issue": issue,
        "records_affected": int(whitespace_count)
    })


######   7. SIGNUP DATE VALIDATION   ######

def validate_signup_date(df, report):

    print("\nSTEP 7 - Validating signup_date")

    # Data Type    

    is_datetime = (
        pd.api.types.is_datetime64_any_dtype(
            df["signup_date"]
        )
    )

    if is_datetime:

        status = "PASS"

        issue = (
            "Signup date is stored as datetime"
        )

    else:

        status = "FAIL"

        issue = (
            "Signup date is not stored as datetime"
        )

    report.append({
        "check": "Signup Date Data Type",
        "column": "signup_date",
        "status": status,
        "issue": issue,
        "records_affected": 0
    })
    
    # Missing Signup Date
    
    missing_dates = (
        df["signup_date"]
        .isna()
        .sum()
    )

    report.append({
        "check": "Missing Signup Dates",
        "column": "signup_date",
        "status": (
            "PASS"
            if missing_dates == 0
            else "INFO"
        ),
        "issue": (
            "No missing signup dates"
            if missing_dates == 0
            else "Missing signup dates remain"
        ),
        "records_affected": int(missing_dates)
    })
    
    # Future Signup Date
    
    today = pd.Timestamp.today().normalize()

    future_dates = (
        (
            df["signup_date"] > today
        )
        .fillna(False)
        .sum()
    )

    if future_dates == 0:

        status = "PASS"

        issue = (
            "No future signup dates"
        )

    else:

        status = "FAIL"

        issue = (
            "Future signup dates found"
        )

    report.append({
        "check": "Future Signup Dates",
        "column": "signup_date",
        "status": status,
        "issue": issue,
        "records_affected": int(future_dates)
    })


######   8. DUPLICATE ROW VALIDATION   ######

def validate_duplicate_rows(df, report):

    print("\nSTEP 8 - Validating duplicate rows")

    duplicate_rows = (
        df.duplicated()
        .sum()
    )

    if duplicate_rows == 0:

        status = "PASS"

        issue = (
            "No exact duplicate rows"
        )

    else:

        status = "FAIL"

        issue = (
            "Exact duplicate rows found"
        )

    report.append({
        "check": "Duplicate Rows",
        "column": "ALL",
        "status": status,
        "issue": issue,
        "records_affected": int(duplicate_rows)
    })


######   9. TEXT QUALITY VALIDATION   ######

def validate_text_quality(df, report):

    print("\nSTEP 9 - Validating text quality")

    text_columns = [
        "gender",
        "city",
        "state"
    ]

    for column in text_columns:

        null_values = (
            df[column]
            .isna()
            .sum()
        )

        blank_values = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        report.append({
            "check": "Blank Text Values",
            "column": column,
            "status": (
                "PASS"
                if blank_values == 0
                else "INFO"
            ),
            "issue": (
                "No blank text values"
                if blank_values == 0
                else "Blank text values remain"
            ),
            "records_affected": int(
                blank_values
            )
        })


######   10. OVERALL DATA QUALITY SUMMARY   ######

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

        "Total_Checks": total_checks,

        "Passed_Checks": passed_checks,

        "Failed_Checks": failed_checks,

        "Info_Checks": info_checks
    }

    return summary


######   SAVE VALIDATION REPORT   ######

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

def run_customers_post_cleaning_validation():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("CUSTOMERS POST-CLEANING VALIDATION")
    print("\n")

    df = load_cleaned_customers()

    report = []

    validate_columns(
        df,
        report
    )

    validate_customer_id(
        df,
        report
    )

    validate_gender(
        df,
        report
    )

    validate_age(
        df,
        report
    )

    validate_city(
        df,
        report
    )

    validate_state(
        df,
        report
    )

    validate_signup_date(
        df,
        report
    )

    validate_duplicate_rows(
        df,
        report
    )

    validate_text_quality(
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

    print("POST-CLEANING VALIDATION SUMMARY")
    print("\n")

    for key, value in summary.items():

        print(
            f"{key:<30}: {value}"
        )

    print("\nPost-cleaning validation completed successfully.")


######   RUN   ######

if __name__ == "__main__":

    run_customers_post_cleaning_validation()