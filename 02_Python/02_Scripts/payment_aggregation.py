from pathlib import Path
import pandas as pd
import numpy as np



# PROJECT PATHS


PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


# INPUT DIRECTORY


CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)


# OUTPUT DIRECTORY


AGGREGATED_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "06_aggregated_data"
)

AGGREGATED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# INPUT FILE


PAYMENTS_FILE = (
    CLEANED_DIR
    / "payments_cleaned.xlsx"
)


# OUTPUT FILES


OUTPUT_FILE = (
    AGGREGATED_DIR
    / "payment_customer_level.xlsx"
)

REPORT_FILE = (
    AGGREGATED_DIR
    / "payment_aggregation_report.xlsx"
)


# EXPECTED COLUMNS

EXPECTED_COLUMNS = [
    "payment_id",
    "customer_id",
    "payment_date",
    "amount",
    "payment_method",
    "payment_status",
]


# HELPER FUNCTIONS

def standardize_columns(df):
    """
    Standardize column names to lowercase snake_case.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


def clean_basic_types(df):
    """
    Standardize important data types used for aggregation.
    """

    df = df.copy()

    # IDs
    df["payment_id"] = (
        df["payment_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Dates
    df["payment_date"] = pd.to_datetime(
        df["payment_date"],
        errors="coerce"
    )

    # Amount
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Text fields
    df["payment_method"] = (
        df["payment_method"]
        .astype("string")
        .str.strip()
    )

    df["payment_status"] = (
        df["payment_status"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    return df



# LOAD DATA

def load_payments():
    """
    Load cleaned payment data.
    """
    print("\n")
    print("PAYMENT AGGREGATION - DATA LOADING")
    print("\n")

    if not PAYMENTS_FILE.exists():
        raise FileNotFoundError(
            f"Payments file not found:\n{PAYMENTS_FILE}"
        )

    df = pd.read_excel(PAYMENTS_FILE)

    print(f"Payments rows loaded    : {len(df):,}")
    print(f"Payments columns loaded : {len(df.columns)}")

    return df



# VALIDATE SOURCE STRUCTURE

def validate_source_columns(df):
    """
    Validate that the cleaned Payments dataset
    contains the expected columns.
    """

    actual_columns = set(df.columns)
    expected_columns = set(EXPECTED_COLUMNS)

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    if missing_columns:
        raise ValueError(
            "Missing required payment columns:\n"
            + "\n".join(sorted(missing_columns))
        )

    if unexpected_columns:
        print(
            "\nINFO: Unexpected columns found:\n"
            + "\n".join(sorted(unexpected_columns))
        )

    return True



# CREATE PAYMENT LEVEL QUALITY CHECKS

def create_source_checks(df):
    """
    Perform source-level checks before aggregation.
    """

    checks = []

    def add_check(
        check_name,
        category,
        value,
        expected,
        status,
        description
    ):
        checks.append(
            {
                "Check_Name": check_name,
                "Category": category,
                "Actual_Value": value,
                "Expected": expected,
                "Status": status,
                "Description": description,
            }
        )

    
    # Row count  

    add_check(
        "Source Row Count",
        "Source",
        len(df),
        "> 0",
        "PASS" if len(df) > 0 else "FAIL",
        "Payments source dataset contains records."
    )

    
    # Payment ID   

    missing_payment_ids = df["payment_id"].isna().sum()

    add_check(
        "Missing Payment IDs",
        "Payment ID",
        missing_payment_ids,
        0,
        "PASS" if missing_payment_ids == 0 else "FAIL",
        "Every payment should have a payment ID."
    )

    duplicate_payment_ids = df["payment_id"].duplicated().sum()

    add_check(
        "Duplicate Payment IDs",
        "Payment ID",
        duplicate_payment_ids,
        0,
        "PASS" if duplicate_payment_ids == 0 else "FAIL",
        "Payment IDs should uniquely identify payment records."
    )

    
    # Customer ID 

    missing_customer_ids = df["customer_id"].isna().sum()

    add_check(
        "Missing Customer IDs",
        "Customer ID",
        missing_customer_ids,
        0,
        "PASS" if missing_customer_ids == 0 else "FAIL",
        "Every payment should belong to a customer."
    )

    
    # Payment Date   

    missing_payment_dates = df["payment_date"].isna().sum()

    add_check(
        "Missing Payment Dates",
        "Payment Date",
        missing_payment_dates,
        0,
        "PASS" if missing_payment_dates == 0 else "FAIL",
        "Payment dates are required for payment behavior analysis."
    )

    
    # Amount   

    missing_amounts = df["amount"].isna().sum()

    add_check(
        "Missing Payment Amounts",
        "Amount",
        missing_amounts,
        0,
        "PASS" if missing_amounts == 0 else "FAIL",
        "Payment amount is required for revenue calculations."
    )

    negative_amounts = (df["amount"] < 0).sum()

    add_check(
        "Negative Payment Amounts",
        "Amount",
        negative_amounts,
        0,
        "PASS" if negative_amounts == 0 else "FAIL",
        "Negative payment amounts are invalid for this dataset."
    )

    
    # Status  

    unexpected_statuses = sorted(
        set(df["payment_status"].dropna().unique())
        - {"Successful", "Failed"}
    )

    add_check(
        "Unexpected Payment Statuses",
        "Payment Status",
        len(unexpected_statuses),
        0,
        "PASS" if len(unexpected_statuses) == 0 else "FAIL",
        (
            "Allowed statuses are Successful and Failed. "
            f"Unexpected values: {unexpected_statuses}"
        )
    )

    return pd.DataFrame(checks)



# AGGREGATE PAYMENT DATA

def aggregate_payment_data(df):
    """
    Convert payment-level data into one row per customer.
    """

    print("PAYMENT CUSTOMER-LEVEL AGGREGATION")

    
    # Work on a copy    

    payments = df.copy()
    
    # Status flags

    payments["is_successful"] = (
        payments["payment_status"]
        == "Successful"
    ).astype(int)

    payments["is_failed"] = (
        payments["payment_status"]
        == "Failed"
    ).astype(int)
 
    # Aggregate basic payment metrics    

    summary = (
        payments
        .groupby("customer_id", dropna=False)
        .agg(
            total_payment_count=(
                "payment_id",
                "count"
            ),

            successful_payment_count=(
                "is_successful",
                "sum"
            ),

            failed_payment_count=(
                "is_failed",
                "sum"
            ),

            total_payment_amount=(
                "amount",
                "sum"
            ),

            average_payment_amount=(
                "amount",
                "mean"
            ),

            minimum_payment_amount=(
                "amount",
                "min"
            ),

            maximum_payment_amount=(
                "amount",
                "max"
            ),

            first_payment_date=(
                "payment_date",
                "min"
            ),

            last_payment_date=(
                "payment_date",
                "max"
            ),
        )
        .reset_index()
    )
   
    # Successful / Failed payment amounts    

    successful_amounts = (
        payments.loc[
            payments["payment_status"] == "Successful"
        ]
        .groupby("customer_id")["amount"]
        .sum()
        .rename("successful_payment_amount")
    )

    failed_amounts = (
        payments.loc[
            payments["payment_status"] == "Failed"
        ]
        .groupby("customer_id")["amount"]
        .sum()
        .rename("failed_payment_amount")
    )

    summary = summary.merge(
        successful_amounts,
        on="customer_id",
        how="left"
    )

    summary = summary.merge(
        failed_amounts,
        on="customer_id",
        how="left"
    )

    # Replace missing amounts caused by no successful/failed
    # records with zero.

    summary["successful_payment_amount"] = (
        summary["successful_payment_amount"]
        .fillna(0)
    )

    summary["failed_payment_amount"] = (
        summary["failed_payment_amount"]
        .fillna(0)
    )
    
    # Payment success / failure rates    

    summary["payment_success_rate"] = np.where(
        summary["total_payment_count"] > 0,
        (
            summary["successful_payment_count"]
            / summary["total_payment_count"]
        ) * 100,
        np.nan
    )

    summary["payment_failure_rate"] = np.where(
        summary["total_payment_count"] > 0,
        (
            summary["failed_payment_count"]
            / summary["total_payment_count"]
        ) * 100,
        np.nan
    )
   
    # Payment method analysis    

    method_counts = (
        payments
        .groupby(
            ["customer_id", "payment_method"]
        )
        .size()
        .reset_index(name="method_count")
    )

    # Primary payment method = method with highest frequency
    method_counts = method_counts.sort_values(
        [
            "customer_id",
            "method_count",
            "payment_method"
        ],
        ascending=[True, False, True]
    )

    primary_methods = (
        method_counts
        .drop_duplicates("customer_id")
        [["customer_id", "payment_method"]]
        .rename(
            columns={
                "payment_method": "primary_payment_method"
            }
        )
    )

    summary = summary.merge(
        primary_methods,
        on="customer_id",
        how="left"
    )

    
    # Number of payment methods used   

    method_usage = (
        payments
        .groupby("customer_id")["payment_method"]
        .nunique()
        .rename("payment_methods_used")
    )

    summary = summary.merge(
        method_usage,
        on="customer_id",
        how="left"
    )
   
    # Payment method counts    

    payment_method_pivot = pd.crosstab(
        payments["customer_id"],
        payments["payment_method"]
    )

    payment_method_pivot.columns = [
        f"payment_method_{str(col).lower().replace(' ', '_')}_count"
        for col in payment_method_pivot.columns
    ]

    payment_method_pivot = (
        payment_method_pivot
        .reset_index()
    )

    summary = summary.merge(
        payment_method_pivot,
        on="customer_id",
        how="left"
    )
    
    # Last payment recency    

    dataset_observation_date = payments["payment_date"].max()

    summary["dataset_observation_date"] = (
        dataset_observation_date
    )

    summary["days_since_last_payment"] = (
        dataset_observation_date
        - summary["last_payment_date"]
    ).dt.days
    
    # Payment frequency    

    summary["payments_per_month"] = np.where(
        (
            summary["first_payment_date"].notna()
            &
            summary["last_payment_date"].notna()
        ),
        np.where(
            (
                summary["last_payment_date"]
                - summary["first_payment_date"]
            ).dt.days > 0,

            summary["total_payment_count"]
            /
            (
                (
                    summary["last_payment_date"]
                    - summary["first_payment_date"]
                ).dt.days
                / 30.44
            ),

            summary["total_payment_count"]
        ),
        np.nan
    )
   
    # Payment behavior flags    

    summary["has_failed_payment"] = (
        summary["failed_payment_count"] > 0
    ).astype(int)

    summary["has_successful_payment"] = (
        summary["successful_payment_count"] > 0
    ).astype(int)
   
    # Payment amount difference    

    summary["successful_vs_failed_amount_difference"] = (
        summary["successful_payment_amount"]
        - summary["failed_payment_amount"]
    )
    
    # Round numerical metrics    

    decimal_columns = [
        "total_payment_amount",
        "successful_payment_amount",
        "failed_payment_amount",
        "average_payment_amount",
        "minimum_payment_amount",
        "maximum_payment_amount",
        "payment_success_rate",
        "payment_failure_rate",
        "payments_per_month",
        "successful_vs_failed_amount_difference",
    ]

    for column in decimal_columns:
        if column in summary.columns:
            summary[column] = summary[column].round(2)
   
    # Sort    

    summary = summary.sort_values(
        "customer_id"
    ).reset_index(drop=True)

    print(
        f"Customer-level payment rows : "
        f"{len(summary):,}"
    )

    print(
        f"Unique customers             : "
        f"{summary['customer_id'].nunique():,}"
    )

    return summary, dataset_observation_date


# CREATE AGGREGATION VALIDATION CHECKS

def create_aggregation_checks(
    payments,
    customer_payment,
    dataset_observation_date
):
    """
    Validate the customer-level aggregation against
    the original payment-level dataset.
    """

    checks = []

    def add_check(
        check_name,
        category,
        actual,
        expected,
        status,
        description
    ):
        checks.append(
            {
                "Check_Name": check_name,
                "Category": category,
                "Actual_Value": actual,
                "Expected": expected,
                "Status": status,
                "Description": description,
            }
        )
    
    # Customer-level grain   

    unique_customers = (
        customer_payment["customer_id"]
        .nunique()
    )

    customer_rows = len(customer_payment)

    add_check(
        "One Row Per Customer",
        "Grain",
        customer_rows,
        unique_customers,
        "PASS"
        if customer_rows == unique_customers
        else "FAIL",
        "Customer-level dataset must contain exactly one row per customer."
    )
  
    # Total payment count reconciliation    

    source_payment_count = len(payments)

    aggregated_payment_count = (
        customer_payment["total_payment_count"]
        .sum()
    )

    add_check(
        "Payment Count Reconciliation",
        "Reconciliation",
        aggregated_payment_count,
        source_payment_count,
        "PASS"
        if aggregated_payment_count == source_payment_count
        else "FAIL",
        "Sum of customer payment counts must equal source payment rows."
    )
 
    # Total amount reconciliation    

    source_total_amount = payments["amount"].sum()

    aggregated_total_amount = (
        customer_payment["total_payment_amount"]
        .sum()
    )

    amount_difference = (
        aggregated_total_amount
        - source_total_amount
    )

    add_check(
        "Payment Amount Reconciliation",
        "Reconciliation",
        round(aggregated_total_amount, 2),
        round(source_total_amount, 2),
        "PASS"
        if abs(amount_difference) < 0.01
        else "FAIL",
        "Customer-level total payment amount must reconcile with source."
    )

    # Successful payment reconciliation    

    source_successful_count = (
        payments["payment_status"]
        .eq("Successful")
        .sum()
    )

    aggregated_successful_count = (
        customer_payment[
            "successful_payment_count"
        ]
        .sum()
    )

    add_check(
        "Successful Payment Count Reconciliation",
        "Reconciliation",
        aggregated_successful_count,
        source_successful_count,
        "PASS"
        if aggregated_successful_count == source_successful_count
        else "FAIL",
        "Successful payment counts must reconcile."
    )
    
    # Failed payment reconciliation

    source_failed_count = (
        payments["payment_status"]
        .eq("Failed")
        .sum()
    )

    aggregated_failed_count = (
        customer_payment[
            "failed_payment_count"
        ]
        .sum()
    )

    add_check(
        "Failed Payment Count Reconciliation",
        "Reconciliation",
        aggregated_failed_count,
        source_failed_count,
        "PASS"
        if aggregated_failed_count == source_failed_count
        else "FAIL",
        "Failed payment counts must reconcile."
    )
 
    # Customer coverage    

    source_customers = (
        payments["customer_id"]
        .nunique()
    )

    aggregated_customers = (
        customer_payment["customer_id"]
        .nunique()
    )

    add_check(
        "Customer Coverage",
        "Coverage",
        aggregated_customers,
        source_customers,
        "PASS"
        if aggregated_customers == source_customers
        else "FAIL",
        "All payment customers must appear in aggregation."
    )

    
    # Missing customer IDs in aggregation 

    missing_customer_ids = (
        customer_payment["customer_id"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Customer IDs in Aggregation",
        "Quality",
        missing_customer_ids,
        0,
        "PASS"
        if missing_customer_ids == 0
        else "FAIL",
        "Customer-level aggregation must not contain missing customer IDs."
    )

    
    # Duplicate customers
    
    duplicate_customers = (
        customer_payment["customer_id"]
        .duplicated()
        .sum()
    )

    add_check(
        "Duplicate Customer Rows",
        "Grain",
        duplicate_customers,
        0,
        "PASS"
        if duplicate_customers == 0
        else "FAIL",
        "There must be exactly one payment summary row per customer."
    )

    
    # Date reconciliation

    max_source_date = payments["payment_date"].max()

    max_aggregation_date = (
        customer_payment["last_payment_date"]
        .max()
    )

    add_check(
        "Last Payment Date Reconciliation",
        "Reconciliation",
        max_aggregation_date,
        max_source_date,
        "PASS"
        if max_aggregation_date == max_source_date
        else "FAIL",
        "Maximum last payment date must match source maximum date."
    )

    
    # Observation date 

    add_check(
        "Dataset Observation Date",
        "Metadata",
        dataset_observation_date,
        dataset_observation_date,
        "INFO",
        "Observation date is based on the maximum payment date in the cleaned payment dataset."
    )

    return pd.DataFrame(checks)



# CREATE SUMMARY REPORT

def create_summary_report(
    payments,
    customer_payment,
    source_checks,
    aggregation_checks,
    dataset_observation_date
):
    """
    Create detailed payment aggregation report.
    """

    source_payment_count = len(payments)

    source_customer_count = (
        payments["customer_id"].nunique()
    )

    total_payment_amount = (
        payments["amount"].sum()
    )

    successful_count = (
        payments["payment_status"]
        .eq("Successful")
        .sum()
    )

    failed_count = (
        payments["payment_status"]
        .eq("Failed")
        .sum()
    )

    successful_amount = (
        payments.loc[
            payments["payment_status"] == "Successful",
            "amount"
        ].sum()
    )

    failed_amount = (
        payments.loc[
            payments["payment_status"] == "Failed",
            "amount"
        ].sum()
    )

    summary = pd.DataFrame(
        {
            "Metric": [
                "Source Payment Rows",
                "Source Unique Customers",
                "Customer-Level Rows",
                "Customer-Level Unique Customers",
                "Total Payment Amount",
                "Successful Payment Count",
                "Failed Payment Count",
                "Successful Payment Amount",
                "Failed Payment Amount",
                "Average Payment Amount",
                "Minimum Payment Amount",
                "Maximum Payment Amount",
                "Average Payments per Customer",
                "Customers with Failed Payments",
                "Customers with Successful Payments",
                "Unique Payment Methods",
                "Dataset Observation Date",
            ],
            "Value": [
                source_payment_count,
                source_customer_count,
                len(customer_payment),
                customer_payment["customer_id"].nunique(),
                round(total_payment_amount, 2),
                successful_count,
                failed_count,
                round(successful_amount, 2),
                round(failed_amount, 2),
                round(payments["amount"].mean(), 2),
                round(payments["amount"].min(), 2),
                round(payments["amount"].max(), 2),
                round(
                    source_payment_count
                    / source_customer_count,
                    2
                ),
                int(
                    (
                        customer_payment[
                            "has_failed_payment"
                        ]
                        == 1
                    ).sum()
                ),
                int(
                    (
                        customer_payment[
                            "has_successful_payment"
                        ]
                        == 1
                    ).sum()
                ),
                payments["payment_method"].nunique(),
                dataset_observation_date,
            ],
        }
    )

    return summary


# CREATE PAYMENT STATUS SUMMARY

def create_status_summary(payments):
    """
    Create payment status distribution.
    """

    status_summary = (
        payments["payment_status"]
        .value_counts(dropna=False)
        .rename_axis("Payment_Status")
        .reset_index(name="Payment_Count")
    )

    status_summary["Percentage"] = (
        status_summary["Payment_Count"]
        / len(payments)
        * 100
    ).round(2)

    return status_summary


# CREATE PAYMENT METHOD SUMMARY

def create_method_summary(payments):
    """
    Create payment method distribution.
    """

    method_summary = (
        payments["payment_method"]
        .value_counts(dropna=False)
        .rename_axis("Payment_Method")
        .reset_index(name="Payment_Count")
    )

    method_summary["Percentage"] = (
        method_summary["Payment_Count"]
        / len(payments)
        * 100
    ).round(2)

    method_amount = (
        payments
        .groupby("payment_method")["amount"]
        .sum()
        .reset_index(
            name="Total_Amount"
        )
    )

    method_summary = method_summary.merge(
        method_amount,
        left_on="Payment_Method",
        right_on="payment_method",
        how="left"
    )

    method_summary = method_summary.drop(
        columns=["payment_method"]
    )

    method_summary["Total_Amount"] = (
        method_summary["Total_Amount"]
        .round(2)
    )

    return method_summary


# SAVE OUTPUTS

def save_outputs(
    customer_payment,
    summary,
    source_checks,
    aggregation_checks,
    status_summary,
    method_summary
):
    """
    Save customer-level payment dataset and
    aggregation report.
    """

    print("SAVING PAYMENT AGGREGATION OUTPUTS")

    # Customer-level dataset    

    customer_payment.to_excel(
        OUTPUT_FILE,
        index=False
    )
  
    # Combined report    

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary.to_excel(
            writer,
            sheet_name="Aggregation_Summary",
            index=False
        )

        source_checks.to_excel(
            writer,
            sheet_name="Source_Checks",
            index=False
        )

        aggregation_checks.to_excel(
            writer,
            sheet_name="Aggregation_Checks",
            index=False
        )

        status_summary.to_excel(
            writer,
            sheet_name="Payment_Status",
            index=False
        )

        method_summary.to_excel(
            writer,
            sheet_name="Payment_Method",
            index=False
        )

    print(
        f"Customer-Level Dataset:\n"
        f"{OUTPUT_FILE}"
    )

    print(
        f"\nAggregation Report:\n"
        f"{REPORT_FILE}"
    )


# MAIN

def main():

    print("PAYMENT CUSTOMER-LEVEL AGGREGATION")

    # 1. Load    

    payments = load_payments()
    
    # 2. Standardize columns

    payments = standardize_columns(
        payments
    )
    
    # 3. Validate columns

    validate_source_columns(
        payments
    )
   
    # 4. Clean basic types    

    payments = clean_basic_types(
        payments
    )
    
    # 5. Source checks

    source_checks = create_source_checks(
        payments
    )
    
    # Stop if source validation has failures    

    source_failures = (
        source_checks["Status"]
        == "FAIL"
    ).sum()

    if source_failures > 0:

        print("SOURCE VALIDATION FAILED")

        print(
            source_checks.loc[
                source_checks["Status"] == "FAIL"
            ][
                [
                    "Check_Name",
                    "Actual_Value",
                    "Expected",
                    "Description"
                ]
            ].to_string(index=False)
        )

        raise ValueError(
            "Payment aggregation stopped because "
            "source validation failed."
        )
   
    # 6. Aggregate    

    (
        customer_payment,
        dataset_observation_date
    ) = aggregate_payment_data(
        payments
    )
    
    # 7. Aggregation validation

    aggregation_checks = (
        create_aggregation_checks(
            payments,
            customer_payment,
            dataset_observation_date
        )
    )
   
    # 8. Create reports    

    summary = create_summary_report(
        payments,
        customer_payment,
        source_checks,
        aggregation_checks,
        dataset_observation_date
    )

    status_summary = create_status_summary(
        payments
    )

    method_summary = create_method_summary(
        payments
    )
   
    # 9. Save    

    save_outputs(
        customer_payment,
        summary,
        source_checks,
        aggregation_checks,
        status_summary,
        method_summary
    )
    
    # 10. Final result

    all_checks = pd.concat(
        [
            source_checks,
            aggregation_checks
        ],
        ignore_index=True
    )

    total_checks = len(all_checks)

    passed_checks = (
        all_checks["Status"] == "PASS"
    ).sum()

    failed_checks = (
        all_checks["Status"] == "FAIL"
    ).sum()

    info_checks = (
        all_checks["Status"] == "INFO"
    ).sum()

    print("PAYMENT AGGREGATION COMPLETED")

    print(
        f"Payment-level rows        : "
        f"{len(payments):,}"
    )

    print(
        f"Customer-level rows       : "
        f"{len(customer_payment):,}"
    )

    print(
        f"Unique customers          : "
        f"{customer_payment['customer_id'].nunique():,}"
    )

    print(
        f"Total payment amount      : "
        f"₹{payments['amount'].sum():,.2f}"
    )

    print(
        f"Successful payments       : "
        f"{(
            payments['payment_status']
            .eq('Successful')
            .sum()
        ):,}"
    )

    print(
        f"Failed payments           : "
        f"{(
            payments['payment_status']
            .eq('Failed')
            .sum()
        ):,}"
    )

    print(
        f"Total Checks              : "
        f"{total_checks}"
    )

    print(
        f"Passed Checks             : "
        f"{passed_checks}"
    )

    print(
        f"Failed Checks             : "
        f"{failed_checks}"
    )

    print(
        f"Info Checks               : "
        f"{info_checks}"
    )

    print(
        f"\nOverall Payment "
        f"Aggregation              : "
        f"{'PASS' if failed_checks == 0 else 'FAIL'}"
    )

# RUN


if __name__ == "__main__":
    main()