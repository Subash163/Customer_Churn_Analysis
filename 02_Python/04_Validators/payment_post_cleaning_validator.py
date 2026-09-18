from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED PAYMENTS DATA   ######

CLEANED_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "payments_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "payments_post_cleaning_validation_report.xlsx"
)


######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "payment_id",
    "customer_id",
    "payment_date",
    "amount",
    "payment_method",
    "payment_status",
]


######   VALIDATION FUNCTIONS   ######

def load_cleaned_payments():
    """Load cleaned Payments data."""

    print("LOADING CLEANED PAYMENTS DATA")
    print("\n")

    df = pd.read_excel(CLEANED_FILE)

    print(f"Rows loaded    : {len(df):,}")
    print(f"Columns loaded : {len(df.columns)}")

    return df


def check_columns(df):
    """Check whether expected columns exist."""

    results = []

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

    results.append({
        "Check": "Expected Columns Present",
        "Value": len(missing_columns) == 0,
        "Status": "PASS" if len(missing_columns) == 0 else "FAIL",
        "Details": (
            "All expected columns are present."
            if len(missing_columns) == 0
            else f"Missing columns: {missing_columns}"
        ),
    })

    results.append({
        "Check": "Unexpected Columns",
        "Value": len(unexpected_columns),
        "Status": "INFO" if len(unexpected_columns) == 0 else "INFO",
        "Details": (
            "No unexpected columns."
            if len(unexpected_columns) == 0
            else f"Unexpected columns: {unexpected_columns}"
        ),
    })

    return results


def check_missing_values(df):
    """Check missing values."""

    results = []

    total_missing = int(df.isnull().sum().sum())

    results.append({
        "Check": "Total Missing Values",
        "Value": total_missing,
        "Status": "PASS" if total_missing == 0 else "INFO",
        "Details": (
            "No missing values found."
            if total_missing == 0
            else "Missing values exist and require review."
        ),
    })

    for column in EXPECTED_COLUMNS:

        missing_count = int(df[column].isnull().sum())

        results.append({
            "Check": f"Missing Values - {column}",
            "Value": missing_count,
            "Status": "PASS" if missing_count == 0 else "INFO",
            "Details": (
                "No missing values."
                if missing_count == 0
                else f"{missing_count:,} missing values found."
            ),
        })

    return results


def check_duplicate_rows(df):
    """Check exact duplicate rows."""

    duplicate_rows = int(df.duplicated().sum())

    return [{
        "Check": "Duplicate Rows",
        "Value": duplicate_rows,
        "Status": "PASS" if duplicate_rows == 0 else "FAIL",
        "Details": (
            "No duplicate rows."
            if duplicate_rows == 0
            else f"{duplicate_rows:,} duplicate rows found."
        ),
    }]


def check_payment_ids(df):
    """Validate Payment IDs."""

    results = []

    duplicate_payment_ids = int(
        df["payment_id"].duplicated().sum()
    )

    results.append({
        "Check": "Duplicate Payment IDs",
        "Value": duplicate_payment_ids,
        "Status": (
            "PASS"
            if duplicate_payment_ids == 0
            else "FAIL"
        ),
        "Details": (
            "Payment IDs are unique."
            if duplicate_payment_ids == 0
            else f"{duplicate_payment_ids:,} duplicate Payment IDs found."
        ),
    })

    blank_payment_ids = int(
        df["payment_id"].astype("string").str.strip().eq("").sum()
    )

    results.append({
        "Check": "Blank Payment IDs",
        "Value": blank_payment_ids,
        "Status": (
            "PASS"
            if blank_payment_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No blank Payment IDs."
            if blank_payment_ids == 0
            else f"{blank_payment_ids:,} blank Payment IDs found."
        ),
    })

    return results


def check_customer_ids(df):
    """Validate Customer IDs."""

    results = []

    missing_customer_ids = int(
        df["customer_id"].isnull().sum()
    )

    duplicate_customer_ids = int(
        df["customer_id"].nunique()
    )

    results.append({
        "Check": "Missing Customer IDs",
        "Value": missing_customer_ids,
        "Status": (
            "PASS"
            if missing_customer_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No missing Customer IDs."
            if missing_customer_ids == 0
            else f"{missing_customer_ids:,} missing Customer IDs found."
        ),
    })

    results.append({
        "Check": "Unique Customers in Payments",
        "Value": duplicate_customer_ids,
        "Status": "INFO",
        "Details": "Number of unique customers represented in Payments.",
    })

    return results


def check_dates(df):
    """Validate Payment Date."""

    results = []

    invalid_dates = int(
        df["payment_date"].isnull().sum()
    )

    results.append({
        "Check": "Invalid Payment Dates",
        "Value": invalid_dates,
        "Status": (
            "PASS"
            if invalid_dates == 0
            else "FAIL"
        ),
        "Details": (
            "All Payment Dates are valid."
            if invalid_dates == 0
            else f"{invalid_dates:,} invalid Payment Dates found."
        ),
    })

    future_dates = int(
        (df["payment_date"] > pd.Timestamp.now()).sum()
    )

    results.append({
        "Check": "Future Payment Dates",
        "Value": future_dates,
        "Status": (
            "PASS"
            if future_dates == 0
            else "INFO"
        ),
        "Details": (
            "No future Payment Dates."
            if future_dates == 0
            else f"{future_dates:,} future Payment Dates found."
        ),
    })

    return results


def check_amounts(df):
    """Validate Payment Amount."""

    results = []

    invalid_amounts = int(
        df["amount"].isnull().sum()
    )

    negative_amounts = int(
        (df["amount"] < 0).sum()
    )

    zero_amounts = int(
        (df["amount"] == 0).sum()
    )

    results.append({
        "Check": "Invalid Payment Amounts",
        "Value": invalid_amounts,
        "Status": (
            "PASS"
            if invalid_amounts == 0
            else "FAIL"
        ),
        "Details": (
            "No invalid Payment Amounts."
            if invalid_amounts == 0
            else f"{invalid_amounts:,} invalid amounts found."
        ),
    })

    results.append({
        "Check": "Negative Payment Amounts",
        "Value": negative_amounts,
        "Status": (
            "PASS"
            if negative_amounts == 0
            else "FAIL"
        ),
        "Details": (
            "No negative Payment Amounts."
            if negative_amounts == 0
            else f"{negative_amounts:,} negative amounts found."
        ),
    })

    results.append({
        "Check": "Zero Payment Amounts",
        "Value": zero_amounts,
        "Status": "INFO",
        "Details": (
            "No zero-value payments."
            if zero_amounts == 0
            else f"{zero_amounts:,} zero-value payments found."
        ),
    })

    return results


def check_categorical_columns(df):
    """Validate payment method and status."""

    results = []

    payment_methods = sorted(
        df["payment_method"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    payment_statuses = sorted(
        df["payment_status"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    results.append({
        "Check": "Payment Methods",
        "Value": ", ".join(payment_methods),
        "Status": "INFO",
        "Details": "Unique Payment Method categories.",
    })

    results.append({
        "Check": "Payment Statuses",
        "Value": ", ".join(payment_statuses),
        "Status": "INFO",
        "Details": "Unique Payment Status categories.",
    })

    return results


def check_data_types(df):
    """Validate important data types."""

    results = []

    results.append({
        "Check": "Payment ID Data Type",
        "Value": str(df["payment_id"].dtype),
        "Status": "INFO",
        "Details": "Expected string/object type.",
    })

    results.append({
        "Check": "Customer ID Data Type",
        "Value": str(df["customer_id"].dtype),
        "Status": "INFO",
        "Details": "Expected string/object type.",
    })

    results.append({
        "Check": "Payment Date Data Type",
        "Value": str(df["payment_date"].dtype),
        "Status": (
            "PASS"
            if pd.api.types.is_datetime64_any_dtype(
                df["payment_date"]
            )
            else "FAIL"
        ),
        "Details": "Payment Date should be datetime.",
    })

    results.append({
        "Check": "Amount Data Type",
        "Value": str(df["amount"].dtype),
        "Status": (
            "PASS"
            if pd.api.types.is_numeric_dtype(
                df["amount"]
            )
            else "FAIL"
        ),
        "Details": "Amount should be numeric.",
    })

    return results


######   RUN VALIDATION   ######

def run_validation(df):

    results = []

    results.extend(check_columns(df))
    results.extend(check_missing_values(df))
    results.extend(check_duplicate_rows(df))
    results.extend(check_payment_ids(df))
    results.extend(check_customer_ids(df))
    results.extend(check_dates(df))
    results.extend(check_amounts(df))
    results.extend(check_categorical_columns(df))
    results.extend(check_data_types(df))

    validation_df = pd.DataFrame(results)

    return validation_df


######   SUMMARY   ######

def create_summary(validation_df, df):

    passed = int(
        (validation_df["Status"] == "PASS").sum()
    )

    failed = int(
        (validation_df["Status"] == "FAIL").sum()
    )

    info = int(
        (validation_df["Status"] == "INFO").sum()
    )

    summary = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Total_Missing_Values",
            "Duplicate_Rows",
            "Missing_Payment_IDs",
            "Duplicate_Payment_IDs",
            "Missing_Customer_IDs",
            "Unique_Payment_IDs",
            "Unique_Customer_IDs",
            "Missing_Payment_Dates",
            "Missing_Amounts",
            "Negative_Amounts",
            "Total_Checks",
            "Passed_Checks",
            "Failed_Checks",
            "Info_Checks",
        ],
        "Value": [
            len(df),
            len(df.columns),
            int(df.isnull().sum().sum()),
            int(df.duplicated().sum()),
            int(df["payment_id"].isnull().sum()),
            int(df["payment_id"].duplicated().sum()),
            int(df["customer_id"].isnull().sum()),
            int(df["payment_id"].nunique()),
            int(df["customer_id"].nunique()),
            int(df["payment_date"].isnull().sum()),
            int(df["amount"].isnull().sum()),
            int((df["amount"] < 0).sum()),
            len(validation_df),
            passed,
            failed,
            info,
        ],
    })

    return summary


######   SAVE REPORT   ######

def save_validation_report(validation_df, summary):

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:

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

    print(REPORT_FILE)


######   DISPLAY RESULTS   ######

def display_results(validation_df, summary):

    print("PAYMENTS POST-CLEANING VALIDATION")
    print("\n")

    print(validation_df.to_string(index=False))

    print("VALIDATION SUMMARY")
    print("\n")

    print(summary.to_string(index=False))


######   MAIN   ######

def main():

    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("PAYMENTS POST-CLEANING VALIDATION")
    print("\n")

    df = load_cleaned_payments()

    validation_df = run_validation(df)

    summary = create_summary(
        validation_df,
        df
    )

    display_results(
        validation_df,
        summary
    )

    save_validation_report(
        validation_df,
        summary
    )

    print("PAYMENTS POST-CLEANING VALIDATION COMPLETED")
    print("\n")


if __name__ == "__main__":
    main()