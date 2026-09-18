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


######   CLEANED CUSTOMER SERVICES DATA   ######

CUSTOMER_SERVICES_FILE = (
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
    / "customers_customer_services_referential_integrity.xlsx"
)


######   COLUMN NAMES   ######

CUSTOMER_ID_COLUMN = "customer_id"

######   LOAD DATA   ######

def load_data():
    """
    Load cleaned Customers and Customer_Services data.
    """

    print("LOADING CLEANED DATA")
    print("\n")

    customers = pd.read_excel(
        CUSTOMERS_FILE
    )

    customer_services = pd.read_excel(
        CUSTOMER_SERVICES_FILE
    )

    print(
        f"Customers rows               : "
        f"{len(customers):,}"
    )

    print(
        f"Customers columns            : "
        f"{len(customers.columns)}"
    )

    print(
        f"Customer_Services rows       : "
        f"{len(customer_services):,}"
    )

    print(
        f"Customer_Services columns    : "
        f"{len(customer_services.columns)}"
    )

    return customers, customer_services



######   CHECK REQUIRED COLUMNS   ######

def check_required_columns(
    customers,
    customer_services
):
    """
    Check whether customer_id exists in both datasets.
    """

    customer_column_exists = (
        CUSTOMER_ID_COLUMN
        in customers.columns
    )

    services_customer_column_exists = (
        CUSTOMER_ID_COLUMN
        in customer_services.columns
    )

    print("COLUMN EXISTENCE CHECK")
    print("\n")

    print(
        f"Customers 'customer_id' exists          : "
        f"{customer_column_exists}"
    )

    print(
        f"Customer_Services 'customer_id' exists  : "
        f"{services_customer_column_exists}"
    )

    if not customer_column_exists:

        raise ValueError(
            "Customers file does not contain "
            "'customer_id'."
        )

    if not services_customer_column_exists:

        raise ValueError(
            "Customer_Services file does not contain "
            "'customer_id'."
        )


######   STANDARDIZE CUSTOMER IDs   ######

def standardize_customer_ids(
    customers,
    customer_services
):
    """
    Standardize Customer IDs before comparison.
    """

    customers = customers.copy()

    customer_services = (
        customer_services.copy()
    )

    customers[CUSTOMER_ID_COLUMN] = (
        customers[CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    customer_services[CUSTOMER_ID_COLUMN] = (
        customer_services[CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return customers, customer_services


######   RUN REFERENTIAL INTEGRITY CHECKS   ######

def run_referential_integrity_checks(
    customers,
    customer_services
):
    """
    Perform Customers ↔ Customer_Services
    referential integrity checks.
    """

    results = []
    
    # Create Customer ID sets
    
    customer_ids = set(
        customers[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    service_customer_ids = set(
        customer_services[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )
    
    # Matching IDs
    
    matching_customer_ids = (
        customer_ids
        .intersection(
            service_customer_ids
        )
    )
    
    # Orphan IDs
    
    orphan_customer_ids = (
        service_customer_ids
        - customer_ids
    )
    
    # Customers without service records
    
    customers_without_services = (
        customer_ids
        - service_customer_ids
    )

    # 1. Customers - Missing Customer IDs    

    missing_customer_ids = int(
        customers[CUSTOMER_ID_COLUMN]
        .isna()
        .sum()
    )

    results.append({
        "Check": "Customers - Missing Customer IDs",
        "Value": missing_customer_ids,
        "Status": (
            "PASS"
            if missing_customer_ids == 0
            else "FAIL"
        ),
    })

    # 2. Customers - Duplicate Customer IDs
    
    duplicate_customer_ids = int(
        customers[CUSTOMER_ID_COLUMN]
        .duplicated()
        .sum()
    )

    results.append({
        "Check": "Customers - Duplicate Customer IDs",
        "Value": duplicate_customer_ids,
        "Status": (
            "PASS"
            if duplicate_customer_ids == 0
            else "FAIL"
        ),
    })
    
    # 3. Customer_Services - Missing Customer IDs
    
    missing_service_customer_ids = int(
        customer_services[CUSTOMER_ID_COLUMN]
        .isna()
        .sum()
    )

    results.append({
        "Check": (
            "Customer_Services - Missing Customer IDs"
        ),
        "Value": missing_service_customer_ids,
        "Status": (
            "PASS"
            if missing_service_customer_ids == 0
            else "FAIL"
        ),
    })
    
    # 4. Customer_Services - Duplicate Customer IDs
    
    duplicate_service_customer_ids = int(
        customer_services[CUSTOMER_ID_COLUMN]
        .duplicated()
        .sum()
    )

    results.append({
        "Check": (
            "Customer_Services - Duplicate Customer IDs"
        ),
        "Value": duplicate_service_customer_ids,
        "Status": (
            "PASS"
            if duplicate_service_customer_ids == 0
            else "FAIL"
        ),
    })
    
    # 5. Orphan Customer IDs
    
    orphan_count = len(
        orphan_customer_ids
    )

    results.append({
        "Check": (
            "Customer_Services - Orphan Customer IDs"
        ),
        "Value": orphan_count,
        "Status": (
            "PASS"
            if orphan_count == 0
            else "FAIL"
        ),
    })
    
    # 6. Customers Without Customer_Services
    
    customers_without_services_count = len(
        customers_without_services
    )

    results.append({
        "Check": "Customers - Without Customer_Services",
        "Value": customers_without_services_count,
        "Status": "INFO",
    })
    
    # 7. Customer ID Overlap
    
    results.append({
        "Check": "Customer ID Overlap",
        "Value": len(matching_customer_ids),
        "Status": "INFO",
    })
    
    # 8. Customers Row Count
    
    results.append({
        "Check": "Customers Row Count",
        "Value": len(customers),
        "Status": "INFO",
    })
    
    # 9. Customer_Services Row Count
    
    results.append({
        "Check": "Customer_Services Row Count",
        "Value": len(customer_services),
        "Status": "INFO",
    })
    
    # 10. Unique Customers in Customers
    
    unique_customers = int(
        customers[CUSTOMER_ID_COLUMN]
        .nunique()
    )

    results.append({
        "Check": "Unique Customers in Customers",
        "Value": unique_customers,
        "Status": "INFO",
    })
    
    # 11. Unique Customers in Customer_Services
    
    unique_service_customers = int(
        customer_services[CUSTOMER_ID_COLUMN]
        .nunique()
    )

    results.append({
        "Check": (
            "Unique Customers in Customer_Services"
        ),
        "Value": unique_service_customers,
        "Status": "INFO",
    })
    
    # 12. Unique Customer Count Difference
    
    unique_customer_count_difference = (
        unique_customers
        - unique_service_customers
    )

    results.append({
        "Check": "Unique Customer Count Difference",
        "Value": unique_customer_count_difference,
        "Status": "INFO",
    })
    
    # 13. Customer Row Count Difference
    
    row_count_difference = (
        len(customers)
        - len(customer_services)
    )

    results.append({
        "Check": (
            "Customers vs Customer_Services "
            "Row Difference"
        ),
        "Value": row_count_difference,
        "Status": "INFO",
    })
    
    # 14. Customers with Multiple Service Records
    
    service_counts = (
        customer_services
        .groupby(CUSTOMER_ID_COLUMN)
        .size()
    )

    customers_with_multiple_services = int(
        (service_counts > 1).sum()
    )

    results.append({
        "Check": (
            "Customers with Multiple "
            "Customer_Services Records"
        ),
        "Value": customers_with_multiple_services,
        "Status": "INFO",
    })
    
    # 15. Customers with Exactly One Service Record
    
    customers_with_one_service = int(
        (service_counts == 1).sum()
    )

    results.append({
        "Check": (
            "Customers with Exactly One "
            "Customer_Services Record"
        ),
        "Value": customers_with_one_service,
        "Status": "INFO",
    })
    
    # 16. Customer_Services Records Without Customer
    
    results.append({
        "Check": (
            "Customer_Services Records "
            "Without Customer"
        ),
        "Value": orphan_count,
        "Status": "INFO",
    })
    
    # 17. Minimum Service Records per Customer
    
    if len(service_counts) > 0:

        minimum_services = int(
            service_counts.min()
        )

    else:

        minimum_services = 0

    results.append({
        "Check": (
            "Minimum Customer_Services "
            "Records per Customer"
        ),
        "Value": minimum_services,
        "Status": "INFO",
    })
    
    # 18. Maximum Service Records per Customer
    
    if len(service_counts) > 0:

        maximum_services = int(
            service_counts.max()
        )

    else:

        maximum_services = 0

    results.append({
        "Check": (
            "Maximum Customer_Services "
            "Records per Customer"
        ),
        "Value": maximum_services,
        "Status": "INFO",
    })
    
    # 19. Average Service Records per Customer
    
    if len(service_counts) > 0:

        average_services = round(
            service_counts.mean(),
            2
        )

    else:

        average_services = 0

    results.append({
        "Check": (
            "Average Customer_Services "
            "Records per Customer"
        ),
        "Value": average_services,
        "Status": "INFO",
    })
    
    # 20. Relationship Type
    
    if (
        unique_customers == unique_service_customers
        and duplicate_customer_ids == 0
        and duplicate_service_customer_ids == 0
        and orphan_count == 0
        and customers_without_services_count == 0
    ):

        relationship = "One-to-One"

    elif maximum_services > 1:

        relationship = "One-to-Many"

    else:

        relationship = "Not Determined"

    results.append({
        "Check": (
            "Customers to Customer_Services "
            "Relationship"
        ),
        "Value": relationship,
        "Status": "INFO",
    })

    return pd.DataFrame(
        results
    )


######   CREATE SUMMARY   ######

def create_summary(
    customers,
    customer_services
):
    """
    Create referential integrity summary.
    """

    customer_ids = set(
        customers[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    service_customer_ids = set(
        customer_services[CUSTOMER_ID_COLUMN]
        .dropna()
        .unique()
    )

    matching_customer_ids = (
        customer_ids
        .intersection(
            service_customer_ids
        )
    )

    orphan_customer_ids = (
        service_customer_ids
        - customer_ids
    )

    customers_without_services = (
        customer_ids
        - service_customer_ids
    )
    
    # Coverage calculations
    
    if len(customer_ids) > 0:

        customer_coverage = round(
            (
                len(matching_customer_ids)
                / len(customer_ids)
            ) * 100,
            2
        )

    else:

        customer_coverage = 0

    if len(service_customer_ids) > 0:

        service_coverage = round(
            (
                len(matching_customer_ids)
                / len(service_customer_ids)
            ) * 100,
            2
        )

    else:

        service_coverage = 0
    
    # Service record counts
    
    service_counts = (
        customer_services
        .groupby(CUSTOMER_ID_COLUMN)
        .size()
    )

    if len(service_counts) > 0:

        maximum_services = int(
            service_counts.max()
        )

        minimum_services = int(
            service_counts.min()
        )

        average_services = round(
            service_counts.mean(),
            2
        )

    else:

        maximum_services = 0
        minimum_services = 0
        average_services = 0
    
    # Relationship
    
    if (
        len(customers) == len(customer_services)
        and len(customer_ids)
        == len(service_customer_ids)
        and len(orphan_customer_ids) == 0
        and len(customers_without_services) == 0
        and customers[CUSTOMER_ID_COLUMN]
        .duplicated()
        .sum() == 0
        and customer_services[CUSTOMER_ID_COLUMN]
        .duplicated()
        .sum() == 0
    ):

        relationship = "One-to-One"

    elif maximum_services > 1:

        relationship = "One-to-Many"

    else:

        relationship = "Not Determined"
    
    # Overall integrity
    
    overall_status = (
        "PASS"
        if (
            customers[CUSTOMER_ID_COLUMN]
            .isna()
            .sum() == 0
            and
            customers[CUSTOMER_ID_COLUMN]
            .duplicated()
            .sum() == 0
            and
            customer_services[CUSTOMER_ID_COLUMN]
            .isna()
            .sum() == 0
            and
            customer_services[CUSTOMER_ID_COLUMN]
            .duplicated()
            .sum() == 0
            and
            len(orphan_customer_ids) == 0
        )
        else "FAIL"
    )
    
    # Summary dataframe
    
    summary = pd.DataFrame({
        "Metric": [
            "Total Customers",
            "Total Customer_Services Records",
            "Unique Customer IDs",
            "Unique Customer IDs in Customer_Services",
            "Matching Customer IDs",
            "Customers Without Customer_Services",
            "Orphan Customer_Services Customer IDs",
            "Customer Coverage Percentage",
            "Customer_Services Coverage Percentage",
            "Customers with Multiple Service Records",
            "Minimum Service Records per Customer",
            "Maximum Service Records per Customer",
            "Average Service Records per Customer",
            "Relationship",
            "Overall Referential Integrity",
        ],

        "Value": [
            len(customers),
            len(customer_services),
            len(customer_ids),
            len(service_customer_ids),
            len(matching_customer_ids),
            len(customers_without_services),
            len(orphan_customer_ids),
            customer_coverage,
            service_coverage,
            int(
                (
                    service_counts > 1
                ).sum()
            ),
            minimum_services,
            maximum_services,
            average_services,
            relationship,
            overall_status,
        ],
    })

    return summary


######   SAVE REPORT   ######

def save_report(
    validation_results,
    summary
):
    """
    Save validation results and summary
    to an Excel workbook.
    """

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

    print("REFERENTIAL INTEGRITY REPORT SAVED")
    print("\n")

    print(
        REPORT_FILE
    )


######   DISPLAY RESULTS   ######

def display_results(
    validation_results,
    summary
):
    """
    Display validation results in terminal.
    """

    print(
        "CUSTOMERS ↔ CUSTOMER_SERVICES "
        "REFERENTIAL INTEGRITY"
    )
    print("\n")

    print(
        validation_results.to_string(
            index=False
        )
    )

    print("SUMMARY")
    print("\n")

    print(
        summary.to_string(
            index=False
        )
    )


######   MAIN   ######

def main():

    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print(
        "CUSTOMERS ↔ CUSTOMER_SERVICES "
        "REFERENTIAL INTEGRITY VALIDATION"
    )
    print("\n")

    # Load data    

    customers, customer_services = (
        load_data()
    )
    
    # Check required columns
    
    check_required_columns(
        customers,
        customer_services
    )
    
    # Standardize Customer IDs
    
    customers, customer_services = (
        standardize_customer_ids(
            customers,
            customer_services
        )
    )
    
    # Run validation
    
    validation_results = (
        run_referential_integrity_checks(
            customers,
            customer_services
        )
    )
    
    # Create summary
    
    summary = create_summary(
        customers,
        customer_services
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
        "CUSTOMERS ↔ CUSTOMER_SERVICES "
        "REFERENTIAL INTEGRITY VALIDATION COMPLETED"
    )


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()