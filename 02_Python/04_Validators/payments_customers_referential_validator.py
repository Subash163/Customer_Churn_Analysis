from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED CUSTOMER DATA   ######

CUSTOMERS_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "customers_cleaned.xlsx"
)


######   CLEANED PAYMENTS DATA   ######

PAYMENTS_FILE = (
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
    / "customers_payments_referential_integrity.xlsx"
)


######   EXPECTED COLUMNS   ######

CUSTOMER_ID_COLUMN = "customer_id"
PAYMENT_CUSTOMER_ID_COLUMN = "customer_id"


######   LOAD DATA   ######

def load_data():
    """
    Load cleaned Customers and Payments data.
    """

    print("\n")
    print("LOADING CLEANED DATA")
    print("\n")

    customers = pd.read_excel(CUSTOMERS_FILE)

    payments = pd.read_excel(PAYMENTS_FILE)

    print(f"Customers rows        : {len(customers):,}")
    print(f"Customers columns     : {len(customers.columns)}")
    print(f"Payments rows         : {len(payments):,}")
    print(f"Payments columns      : {len(payments.columns)}")

    return customers, payments


######   STANDARDIZE CUSTOMER IDS   ######

def standardize_customer_ids(customers, payments):
    """
    Standardize Customer IDs before comparison.
    """

    customers[CUSTOMER_ID_COLUMN] = (
        customers[CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    payments[PAYMENT_CUSTOMER_ID_COLUMN] = (
        payments[PAYMENT_CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return customers, payments


######   CHECK REQUIRED COLUMNS   ######

def check_required_columns(customers, payments):

    customer_column_exists = (
        CUSTOMER_ID_COLUMN in customers.columns
    )

    payment_column_exists = (
        PAYMENT_CUSTOMER_ID_COLUMN in payments.columns
    )

    print("\n")
    print("COLUMN EXISTENCE CHECK")
    print("\n")

    print(
        f"Customers 'customer_id' exists : "
        f"{customer_column_exists}"
    )

    print(
        f"Payments 'customer_id' exists   : "
        f"{payment_column_exists}"
    )

    if not customer_column_exists:
        raise ValueError(
            "Customers file does not contain 'customer_id'."
        )

    if not payment_column_exists:
        raise ValueError(
            "Payments file does not contain 'customer_id'."
        )


######   REFERENTIAL INTEGRITY VALIDATION   ######

def run_referential_integrity_checks(customers, payments):

    results = []

    customer_ids = set(
        customers[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    payment_customer_ids = set(
        payments[PAYMENT_CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    # 1. Missing Customer IDs in Customers    

    missing_customer_ids = int(
        customers[CUSTOMER_ID_COLUMN].isna().sum()
    )

    results.append({
        "Check": "Customers - Missing Customer IDs",
        "Value": missing_customer_ids,
        "Status": (
            "PASS"
            if missing_customer_ids == 0
            else "FAIL"
        )
    })
    
    # 2. Duplicate Customer IDs in Customers
    
    duplicate_customer_ids = int(
        customers[CUSTOMER_ID_COLUMN].duplicated().sum()
    )

    results.append({
        "Check": "Customers - Duplicate Customer IDs",
        "Value": duplicate_customer_ids,
        "Status": (
            "PASS"
            if duplicate_customer_ids == 0
            else "FAIL"
        )
    })
    
    # 3. Missing Customer IDs in Payments
    
    missing_payment_customer_ids = int(
        payments[PAYMENT_CUSTOMER_ID_COLUMN].isna().sum()
    )

    results.append({
        "Check": "Payments - Missing Customer IDs",
        "Value": missing_payment_customer_ids,
        "Status": (
            "PASS"
            if missing_payment_customer_ids == 0
            else "FAIL"
        )
    })
    
    # 4. Orphan Customer IDs in Payments
    
    orphan_customer_ids = (
        payment_customer_ids - customer_ids
    )

    orphan_count = len(orphan_customer_ids)

    results.append({
        "Check": "Payments - Orphan Customer IDs",
        "Value": orphan_count,
        "Status": (
            "PASS"
            if orphan_count == 0
            else "FAIL"
        )
    })
    
    # 5. Customer ID Overlap
    
    matching_customer_ids = (
        customer_ids.intersection(payment_customer_ids)
    )

    matching_count = len(matching_customer_ids)

    results.append({
        "Check": "Customer ID Overlap",
        "Value": matching_count,
        "Status": "INFO"
    })
    
    # 6. Customers Without Payments
    
    customers_without_payments = (
        customer_ids - payment_customer_ids
    )

    customers_without_payment_count = (
        len(customers_without_payments)
    )

    results.append({
        "Check": "Customers - Without Payments",
        "Value": customers_without_payment_count,
        "Status": "INFO"
    })
    
    # 7. Customers Row Count
    
    results.append({
        "Check": "Customers Row Count",
        "Value": len(customers),
        "Status": "INFO"
    })
    
    # 8. Payments Row Count
    
    results.append({
        "Check": "Payments Row Count",
        "Value": len(payments),
        "Status": "INFO"
    })
    
    # 9. Unique Customers in Customers

    unique_customers = customers[
        CUSTOMER_ID_COLUMN
    ].nunique()

    results.append({
        "Check": "Unique Customers in Customers",
        "Value": unique_customers,
        "Status": "INFO"
    })
    
    # 10. Unique Customers in Payments
    
    unique_payment_customers = payments[
        PAYMENT_CUSTOMER_ID_COLUMN
    ].nunique()

    results.append({
        "Check": "Unique Customers in Payments",
        "Value": unique_payment_customers,
        "Status": "INFO"
    })
    
    # 11. Customer Row vs Payment Customer Difference
    
    customer_count_difference = (
        unique_customers - unique_payment_customers
    )

    results.append({
        "Check": "Unique Customer Count Difference",
        "Value": customer_count_difference,
        "Status": "INFO"
    })
    
    # 12. Customers with Multiple Payments
    
    payment_counts = (
        payments
        .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
        .size()
    )

    customers_with_multiple_payments = int(
        (payment_counts > 1).sum()
    )

    results.append({
        "Check": "Customers with Multiple Payments",
        "Value": customers_with_multiple_payments,
        "Status": "INFO"
    })
    
    # 13. Customers with Exactly One Payment
    
    customers_with_one_payment = int(
        (payment_counts == 1).sum()
    )

    results.append({
        "Check": "Customers with Exactly One Payment",
        "Value": customers_with_one_payment,
        "Status": "INFO"
    })
    
    # 14. Customers with No Payment Records
    
    results.append({
        "Check": "Customers with No Payment Records",
        "Value": customers_without_payment_count,
        "Status": "INFO"
    })
    
    # 15. Minimum Payments per Customer
    
    if len(payment_counts) > 0:

        minimum_payments = int(
            payment_counts.min()
        )

    else:

        minimum_payments = 0

    results.append({
        "Check": "Minimum Payments per Customer",
        "Value": minimum_payments,
        "Status": "INFO"
    })
    
    # 16. Maximum Payments per Customer
    
    if len(payment_counts) > 0:

        maximum_payments = int(
            payment_counts.max()
        )

    else:

        maximum_payments = 0

    results.append({
        "Check": "Maximum Payments per Customer",
        "Value": maximum_payments,
        "Status": "INFO"
    })
    
    # 17. Average Payments per Customer
    
    if len(payment_counts) > 0:

        average_payments = round(
            payment_counts.mean(),
            2
        )

    else:

        average_payments = 0

    results.append({
        "Check": "Average Payments per Customer",
        "Value": average_payments,
        "Status": "INFO"
    })
    
    # 18. Payment-to-Customer Relationship
    
    if (
        len(payment_counts) > 0
        and maximum_payments > 1
    ):

        relationship = "Many-to-One"

    elif (
        len(payment_counts) > 0
        and maximum_payments == 1
    ):

        relationship = "One-to-One"

    else:

        relationship = "No Payment Records"

    results.append({
        "Check": "Customers to Payments Relationship",
        "Value": relationship,
        "Status": "INFO"
    })

    return pd.DataFrame(results)


######   SUMMARY   ######

def create_summary(customers, payments):

    customer_ids = set(
        customers[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    payment_customer_ids = set(
        payments[PAYMENT_CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    matching_customer_ids = (
        customer_ids.intersection(payment_customer_ids)
    )

    customers_without_payments = (
        customer_ids - payment_customer_ids
    )

    orphan_customer_ids = (
        payment_customer_ids - customer_ids
    )

    # Coverage calculations    

    if len(customer_ids) > 0:

        customer_payment_coverage = round(
            (
                len(matching_customer_ids)
                / len(customer_ids)
            ) * 100,
            2
        )

    else:

        customer_payment_coverage = 0

    if len(payment_customer_ids) > 0:

        payment_customer_coverage = round(
            (
                len(matching_customer_ids)
                / len(payment_customer_ids)
            ) * 100,
            2
        )

    else:

        payment_customer_coverage = 0
    
    # Overall status
    
    overall_status = (
        "PASS"
        if (
            customers[CUSTOMER_ID_COLUMN].isna().sum() == 0
            and customers[CUSTOMER_ID_COLUMN].duplicated().sum() == 0
            and payments[PAYMENT_CUSTOMER_ID_COLUMN].isna().sum() == 0
            and len(orphan_customer_ids) == 0
        )
        else "FAIL"
    )
    
    # Summary dataframe
    
    summary = pd.DataFrame({
        "Metric": [
            "Total Customers",
            "Total Payments",
            "Unique Customer IDs",
            "Unique Customer IDs in Payments",
            "Matching Customer IDs",
            "Customers Without Payments",
            "Orphan Payment Customer IDs",
            "Customer Payment Coverage Percentage",
            "Payment Customer Coverage Percentage",
            "Customers with Multiple Payments",
            "Minimum Payments per Customer",
            "Maximum Payments per Customer",
            "Average Payments per Customer",
            "Relationship",
            "Overall Referential Integrity",
        ],

        "Value": [
            len(customers),
            len(payments),
            len(customer_ids),
            len(payment_customer_ids),
            len(matching_customer_ids),
            len(customers_without_payments),
            len(orphan_customer_ids),
            customer_payment_coverage,
            payment_customer_coverage,
            int(
                (
                    payments
                    .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
                    .size()
                    > 1
                ).sum()
            ),
            (
                int(
                    payments
                    .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
                    .size()
                    .min()
                )
                if len(payments) > 0
                else 0
            ),
            (
                int(
                    payments
                    .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
                    .size()
                    .max()
                )
                if len(payments) > 0
                else 0
            ),
            (
                round(
                    payments
                    .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
                    .size()
                    .mean(),
                    2
                )
                if len(payments) > 0
                else 0
            ),
            (
                "Many-to-One"
                if (
                    len(payments) > 0
                    and payments
                    .groupby(PAYMENT_CUSTOMER_ID_COLUMN)
                    .size()
                    .max() > 1
                )
                else "One-to-One"
            ),
            overall_status,
        ]
    })

    return summary


######   SAVE REPORT   ######

def save_report(validation_results, summary):

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        validation_results.to_excel(
            writer,
            sheet_name="Validation_Results",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

    print("\n")
    print("REFERENTIAL INTEGRITY REPORT SAVED")
    print("\n")

    print(REPORT_FILE)


######   DISPLAY RESULTS   ######

def display_results(validation_results, summary):

    print("\n")
    print("PAYMENTS ↔ CUSTOMERS REFERENTIAL INTEGRITY")
    print("\n")

    print(
        validation_results.to_string(
            index=False
        )
    )

    print("\n")
    print("SUMMARY")
    print("\n")

    print(
        summary.to_string(
            index=False
        )
    )


######   MAIN   ######

def main():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("PAYMENTS ↔ CUSTOMERS REFERENTIAL INTEGRITY VALIDATION")
    print("\n")
    
    # Load data
    
    customers, payments = load_data()
    
    # Check required columns
    
    check_required_columns(
        customers,
        payments
    )
    
    # Standardize IDs
    
    customers, payments = standardize_customer_ids(
        customers,
        payments
    )

    # Run referential integrity checks    

    validation_results = run_referential_integrity_checks(
        customers,
        payments
    )
    
    # Create summary
    
    summary = create_summary(
        customers,
        payments
    )
    
    # Display results
    
    display_results(
        validation_results,
        summary
    )
    
    # Save report
    
    save_report(
        validation_results,
        summary
    )

    print("\n")
    print(
        "PAYMENTS ↔ CUSTOMERS REFERENTIAL "
        "INTEGRITY VALIDATION COMPLETED"
    )
    print("\n")


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()