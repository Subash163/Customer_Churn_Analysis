"""
CUSTOMER CHURN & RETENTION ANALYSIS
Customers ↔ Support Tickets Referential Integrity Validator

Purpose:
    Validate the referential integrity between:
        Customers
        Support_Tickets

Expected Relationship:
    One Customer → Many Support Tickets

Input Files:
    cleaned/customers_cleaned.xlsx
    cleaned/support_tickets_cleaned.xlsx

Output:
    outputs/validation_reports/
        customers_support_tickets_referential_integrity.xlsx
"""

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


######   CLEANED SUPPORT TICKETS DATA   ######

SUPPORT_TICKETS_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "support_tickets_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "customers_support_tickets_referential_integrity.xlsx"
)

######   EXPECTED COLUMNS   ######

CUSTOMER_KEY = "customer_id"
TICKET_KEY = "ticket_id"


# VALIDATION RESULT STORAGE

validation_results = []

def add_check(check, value, status, details):
    """
    Add one validation check to the results list.
    """

    validation_results.append(
        {
            "Check": check,
            "Value": value,
            "Status": status,
            "Details": details,
        }
    )


######   LOAD DATA   ######

def load_data():
    """
    Load cleaned Customers and Support_Tickets datasets.
    """

    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("CUSTOMERS ↔ SUPPORT TICKETS REFERENTIAL INTEGRITY VALIDATION")
    print("\n")

    print("LOADING CLEANED DATA")
    print("\n")

    print(f"\nCustomers file       : {CUSTOMERS_FILE}")
    print(f"Support Tickets file : {SUPPORT_TICKETS_FILE}")

    customers = pd.read_excel(CUSTOMERS_FILE)
    support_tickets = pd.read_excel(SUPPORT_TICKETS_FILE)

    print("\nCustomers")
    print(f"Rows    : {len(customers):,}")
    print(f"Columns : {len(customers.columns)}")

    print("\nSupport Tickets")
    print(f"Rows    : {len(support_tickets):,}")
    print(f"Columns : {len(support_tickets.columns)}")

    return customers, support_tickets


######   STANDARDIZE KEY COLUMNS   ######

def standardize_keys(customers, support_tickets):
    """
    Standardize Customer IDs before comparison.
    """

    customers[CUSTOMER_KEY] = (
        customers[CUSTOMER_KEY]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    support_tickets[CUSTOMER_KEY] = (
        support_tickets[CUSTOMER_KEY]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    if TICKET_KEY in support_tickets.columns:
        support_tickets[TICKET_KEY] = (
            support_tickets[TICKET_KEY]
            .astype("string")
            .str.strip()
            .str.upper()
        )

    return customers, support_tickets


######   MAIN REFERENTIAL INTEGRITY VALIDATION   ######

def validate_referential_integrity(customers, support_tickets):
    """
    Perform Customers ↔ Support_Tickets referential integrity checks.
    """

    print("CUSTOMERS ↔ SUPPORT TICKETS REFERENTIAL INTEGRITY VALIDATION")
    print("\n")
    
    # 1. ROW COUNTS
    
    customer_rows = len(customers)
    ticket_rows = len(support_tickets)

    add_check(
        "Customers Row Count",
        customer_rows,
        "INFO",
        "Total number of customer records."
    )

    add_check(
        "Support Tickets Row Count",
        ticket_rows,
        "INFO",
        "Total number of support ticket records."
    )
    
    # 2. CHECK REQUIRED CUSTOMER KEY
    
    customers_has_key = CUSTOMER_KEY in customers.columns
    tickets_have_customer_key = CUSTOMER_KEY in support_tickets.columns
    tickets_have_ticket_key = TICKET_KEY in support_tickets.columns

    add_check(
        "Customers Customer_ID Column Present",
        customers_has_key,
        "PASS" if customers_has_key else "FAIL",
        (
            "Customer_ID column is present in Customers."
            if customers_has_key
            else "Customer_ID column is missing from Customers."
        ),
    )

    add_check(
        "Support Tickets Customer_ID Column Present",
        tickets_have_customer_key,
        "PASS" if tickets_have_customer_key else "FAIL",
        (
            "Customer_ID column is present in Support_Tickets."
            if tickets_have_customer_key
            else "Customer_ID column is missing from Support_Tickets."
        ),
    )

    add_check(
        "Support Tickets Ticket_ID Column Present",
        tickets_have_ticket_key,
        "PASS" if tickets_have_ticket_key else "FAIL",
        (
            "Ticket_ID column is present in Support_Tickets."
            if tickets_have_ticket_key
            else "Ticket_ID column is missing from Support_Tickets."
        ),
    )

    # Stop if required keys are missing
    if not customers_has_key or not tickets_have_customer_key:
        print("\nRequired Customer_ID column is missing.")
        return pd.DataFrame(validation_results), None
    
    # 3. MISSING CUSTOMER IDs IN CUSTOMERS
    
    missing_customer_ids_customers = customers[CUSTOMER_KEY].isna().sum()

    add_check(
        "Missing Customer IDs in Customers",
        int(missing_customer_ids_customers),
        "PASS" if missing_customer_ids_customers == 0 else "FAIL",
        (
            "No missing Customer IDs in Customers."
            if missing_customer_ids_customers == 0
            else f"{missing_customer_ids_customers:,} Customers have missing Customer IDs."
        ),
    )
    
    # 4. DUPLICATE CUSTOMER IDs IN CUSTOMERS
    
    duplicate_customer_ids = (
        customers[CUSTOMER_KEY]
        .dropna()
        .duplicated()
        .sum()
    )

    add_check(
        "Duplicate Customer IDs in Customers",
        int(duplicate_customer_ids),
        "PASS" if duplicate_customer_ids == 0 else "FAIL",
        (
            "Customer IDs are unique in Customers."
            if duplicate_customer_ids == 0
            else f"{duplicate_customer_ids:,} duplicate Customer ID records found."
        ),
    )
    
    # 5. MISSING CUSTOMER IDs IN SUPPORT TICKETS
    
    missing_customer_ids_tickets = (
        support_tickets[CUSTOMER_KEY]
        .isna()
        .sum()
    )

    add_check(
        "Missing Customer IDs in Support Tickets",
        int(missing_customer_ids_tickets),
        "PASS" if missing_customer_ids_tickets == 0 else "FAIL",
        (
            "No missing Customer IDs in Support_Tickets."
            if missing_customer_ids_tickets == 0
            else f"{missing_customer_ids_tickets:,} Support Tickets have missing Customer IDs."
        ),
    )
    
    # 6. BLANK CUSTOMER IDs IN SUPPORT TICKETS
    
    blank_customer_ids_tickets = (
        support_tickets[CUSTOMER_KEY]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    add_check(
        "Blank Customer IDs in Support Tickets",
        int(blank_customer_ids_tickets),
        "PASS" if blank_customer_ids_tickets == 0 else "FAIL",
        (
            "No blank Customer IDs in Support_Tickets."
            if blank_customer_ids_tickets == 0
            else f"{blank_customer_ids_tickets:,} blank Customer IDs found."
        ),
    )
    
    # 7. DUPLICATE TICKET IDs
    
    duplicate_ticket_ids = 0

    if tickets_have_ticket_key:

        duplicate_ticket_ids = (
            support_tickets[TICKET_KEY]
            .dropna()
            .duplicated()
            .sum()
        )

    add_check(
        "Duplicate Ticket IDs in Support Tickets",
        int(duplicate_ticket_ids),
        "PASS" if duplicate_ticket_ids == 0 else "FAIL",
        (
            "Ticket IDs are unique in Support_Tickets."
            if duplicate_ticket_ids == 0
            else f"{duplicate_ticket_ids:,} duplicate Ticket ID records found."
        ),
    )
    
    # 8. UNIQUE CUSTOMER IDs IN CUSTOMERS
    
    unique_customers = (
        customers[CUSTOMER_KEY]
        .dropna()
        .nunique()
    )

    add_check(
        "Unique Customers in Customers",
        int(unique_customers),
        "INFO",
        "Number of unique Customer IDs in Customers."
    )
    
    # 9. UNIQUE CUSTOMERS WITH SUPPORT TICKETS
    
    unique_ticket_customers = (
        support_tickets[CUSTOMER_KEY]
        .dropna()
        .nunique()
    )

    add_check(
        "Unique Customers in Support Tickets",
        int(unique_ticket_customers),
        "INFO",
        "Number of unique customers with at least one support ticket."
    )
    
    # 10. CUSTOMER ID OVERLAP
    
    customer_id_set = set(
        customers[CUSTOMER_KEY]
        .dropna()
    )

    ticket_customer_id_set = set(
        support_tickets[CUSTOMER_KEY]
        .dropna()
    )

    matching_customer_ids = (
        customer_id_set
        .intersection(ticket_customer_id_set)
    )

    matching_customer_count = len(matching_customer_ids)

    add_check(
        "Customer ID Overlap",
        int(matching_customer_count),
        "INFO",
        "Number of Customer IDs appearing in both datasets."
    )
    
    # 11. ORPHAN SUPPORT TICKETS
    
    orphan_mask = (
        support_tickets[CUSTOMER_KEY].notna()
        & ~support_tickets[CUSTOMER_KEY].isin(customer_id_set)
    )

    orphan_tickets = support_tickets.loc[orphan_mask].copy()

    orphan_ticket_count = len(orphan_tickets)

    add_check(
        "Orphan Support Tickets",
        int(orphan_ticket_count),
        "PASS" if orphan_ticket_count == 0 else "FAIL",
        (
            "All Support Tickets reference valid Customer IDs."
            if orphan_ticket_count == 0
            else f"{orphan_ticket_count:,} Support Tickets reference Customer IDs not found in Customers."
        ),
    )
    
    # 12. CUSTOMERS WITHOUT SUPPORT TICKETS
    
    customers_without_tickets_mask = (
        ~customers[CUSTOMER_KEY].isin(ticket_customer_id_set)
    )

    customers_without_tickets = customers.loc[
        customers_without_tickets_mask
    ].copy()

    customers_without_ticket_count = len(
        customers_without_tickets
    )

    add_check(
        "Customers Without Support Tickets",
        int(customers_without_ticket_count),
        "INFO",
        (
            "Number of customers without any Support Ticket records. "
            "This is not considered a referential integrity failure."
        ),
    )
    
    # 13. UNIQUE CUSTOMER COUNT DIFFERENCE
    
    unique_customer_count_difference = (
        unique_customers
        - unique_ticket_customers
    )

    add_check(
        "Unique Customer Count Difference",
        int(unique_customer_count_difference),
        "INFO",
        (
            "Difference between unique Customers and unique customers "
            "with Support Tickets."
        ),
    )
    
    # 14. ROW COUNT DIFFERENCE
    
    rows_difference = customer_rows - ticket_rows

    add_check(
        "Rows Difference",
        int(rows_difference),
        "INFO",
        (
            "Difference between Customers rows and Support Tickets rows. "
            "Different row counts are expected because one customer can "
            "have multiple support tickets."
        ),
    )
    
    # 15. SUPPORT TICKETS PER CUSTOMER
    
    ticket_counts = (
        support_tickets
        .dropna(subset=[CUSTOMER_KEY])
        .groupby(CUSTOMER_KEY)
        .size()
    )

    if len(ticket_counts) > 0:

        customers_with_multiple_tickets = (
            ticket_counts > 1
        ).sum()

        customers_with_one_ticket = (
            ticket_counts == 1
        ).sum()

        minimum_tickets = ticket_counts.min()
        maximum_tickets = ticket_counts.max()
        average_tickets = ticket_counts.mean()

    else:

        customers_with_multiple_tickets = 0
        customers_with_one_ticket = 0
        minimum_tickets = 0
        maximum_tickets = 0
        average_tickets = 0
    
    # 16. CUSTOMERS WITH MULTIPLE SUPPORT TICKETS
    
    add_check(
        "Customers with Multiple Support Tickets",
        int(customers_with_multiple_tickets),
        "INFO",
        "Customers having more than one Support Ticket."
    )
    
    # 17. CUSTOMERS WITH EXACTLY ONE SUPPORT TICKET
    
    add_check(
        "Customers with Exactly One Support Ticket",
        int(customers_with_one_ticket),
        "INFO",
        "Customers having exactly one Support Ticket."
    )
    
    # 18. CUSTOMERS WITH NO SUPPORT TICKETS
    
    customers_with_no_tickets = (
        unique_customers
        - unique_ticket_customers
    )

    add_check(
        "Customers with No Support Tickets",
        int(customers_with_no_tickets),
        "INFO",
        "Customers who do not have any Support Ticket records."
    )
    
    # 19. TICKETS WITHOUT CUSTOMER
    
    tickets_without_customer = (
        support_tickets[CUSTOMER_KEY]
        .isna()
        .sum()
    )

    add_check(
        "Support Tickets Without Customer",
        int(tickets_without_customer),
        "PASS" if tickets_without_customer == 0 else "FAIL",
        (
            "Every Support Ticket has a Customer ID."
            if tickets_without_customer == 0
            else f"{tickets_without_customer:,} Support Tickets have no Customer ID."
        ),
    )
    
    # 20. MINIMUM TICKETS PER CUSTOMER
    
    add_check(
        "Minimum Support Tickets per Customer",
        float(minimum_tickets),
        "INFO",
        "Minimum number of Support Tickets among customers with tickets."
    )
    
    # 21. MAXIMUM TICKETS PER CUSTOMER
    
    add_check(
        "Maximum Support Tickets per Customer",
        int(maximum_tickets),
        "INFO",
        "Maximum number of Support Tickets for a single customer."
    )
    
    # 22. AVERAGE TICKETS PER CUSTOMER
    
    add_check(
        "Average Support Tickets per Customer",
        round(float(average_tickets), 2),
        "INFO",
        (
            "Average number of Support Tickets per customer "
            "among customers who have at least one ticket."
        ),
    )
    
    # 23. CUSTOMER COVERAGE
    
    if unique_customers > 0:

        customer_coverage = (
            unique_ticket_customers
            / unique_customers
            * 100
        )

    else:
        customer_coverage = 0

    add_check(
        "Customer Support Ticket Coverage (%)",
        round(float(customer_coverage), 2),
        "INFO",
        (
            "Percentage of Customers who have at least one "
            "Support Ticket."
        ),
    )
    
    # 24. TICKET CUSTOMER COVERAGE
    
    if ticket_rows > 0:

        matched_ticket_rows = (
            support_tickets[CUSTOMER_KEY]
            .isin(customer_id_set)
            .sum()
        )

        ticket_customer_coverage = (
            matched_ticket_rows
            / ticket_rows
            * 100
        )

    else:

        matched_ticket_rows = 0
        ticket_customer_coverage = 0

    add_check(
        "Support Ticket Customer Coverage (%)",
        round(float(ticket_customer_coverage), 2),
        "INFO",
        (
            "Percentage of Support Ticket records whose Customer IDs "
            "exist in Customers."
        ),
    )
    
    # 25. RELATIONSHIP TYPE
    
    if (
        duplicate_customer_ids == 0
        and maximum_tickets > 1
    ):

        relationship = "One-to-Many"

        relationship_details = (
            "One Customer can have multiple Support Tickets."
        )

    elif (
        duplicate_customer_ids == 0
        and maximum_tickets == 1
    ):

        relationship = "One-to-One"

        relationship_details = (
            "Each Customer has at most one Support Ticket."
        )

    else:

        relationship = "Unable to Determine"

        relationship_details = (
            "Relationship requires further investigation."
        )

    add_check(
        "Customers to Support Tickets Relationship",
        relationship,
        "INFO",
        relationship_details,
    )
    
    # 26. ORPHAN CUSTOMER IDs
    
    orphan_customer_ids = sorted(
        ticket_customer_id_set
        - customer_id_set
    )

    add_check(
        "Orphan Customer ID Count",
        len(orphan_customer_ids),
        "PASS" if len(orphan_customer_ids) == 0 else "FAIL",
        (
            "No orphan Customer IDs found."
            if len(orphan_customer_ids) == 0
            else f"{len(orphan_customer_ids):,} orphan Customer IDs found."
        ),
    )
    
    # 27. MATCHED SUPPORT TICKET RECORDS
    
    add_check(
        "Matched Support Ticket Records",
        int(matched_ticket_rows),
        "INFO",
        "Number of Support Ticket records linked to valid Customers."
    )
    
    # 28. RECORDS WITHOUT CUSTOMER
    
    records_without_customer = (
        support_tickets[CUSTOMER_KEY]
        .isna()
        .sum()
    )

    add_check(
        "Records Without Customer",
        int(records_without_customer),
        "PASS" if records_without_customer == 0 else "FAIL",
        (
            "All Support Ticket records contain Customer IDs."
            if records_without_customer == 0
            else f"{records_without_customer:,} records have no Customer ID."
        ),
    )
    
    # 29. OVERALL REFERENTIAL INTEGRITY
    
    referential_integrity_pass = (
        missing_customer_ids_customers == 0
        and duplicate_customer_ids == 0
        and missing_customer_ids_tickets == 0
        and blank_customer_ids_tickets == 0
        and duplicate_ticket_ids == 0
        and orphan_ticket_count == 0
        and tickets_without_customer == 0
    )

    overall_status = (
        "PASS"
        if referential_integrity_pass
        else "FAIL"
    )

    overall_details = (
        "Customers and Support_Tickets maintain valid referential integrity."
        if referential_integrity_pass
        else "Referential integrity issues require investigation."
    )

    add_check(
        "Overall Referential Integrity",
        overall_status,
        overall_status,
        overall_details,
    )
    
    # RETURN RESULTS
    
    validation_df = pd.DataFrame(validation_results)

    return (
        validation_df,
        {
            "orphan_tickets": orphan_tickets,
            "customers_without_tickets": customers_without_tickets,
            "ticket_counts": ticket_counts.reset_index(
                name="Support_Ticket_Count"
            ),
        },
    )


######   VALIDATION SUMMARY   ######

def create_validation_summary(validation_df):
    """
    Create high-level validation summary.
    """

    passed_checks = (
        validation_df["Status"]
        .eq("PASS")
        .sum()
    )

    failed_checks = (
        validation_df["Status"]
        .eq("FAIL")
        .sum()
    )

    info_checks = (
        validation_df["Status"]
        .eq("INFO")
        .sum()
    )

    total_checks = len(validation_df)

    summary = pd.DataFrame(
        [
            {
                "Metric": "Total Checks",
                "Value": total_checks,
            },
            {
                "Metric": "Passed Checks",
                "Value": passed_checks,
            },
            {
                "Metric": "Failed Checks",
                "Value": failed_checks,
            },
            {
                "Metric": "Info Checks",
                "Value": info_checks,
            },
        ]
    )

    return summary


######   PRINT RESULTS   ######

def print_results(validation_df, summary_df):
    """
    Print validation results to terminal.
    """
    print("\n")
    print("REFERENTIAL INTEGRITY VALIDATION RESULTS")
    print("\n")

    print(
        validation_df[
            ["Check", "Value", "Status", "Details"]
        ].to_string(index=False)
    )

    print("\n")
    print("VALIDATION SUMMARY")
    print("\n")

    print(
        summary_df.to_string(index=False)
    )


######   SAVE EXCEL REPORT   

def save_validation_report(
    validation_df,
    summary_df,
    additional_data,
):
    """
    Save validation results to Excel.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    orphan_tickets = additional_data["orphan_tickets"]

    customers_without_tickets = (
        additional_data["customers_without_tickets"]
    )

    ticket_counts = additional_data["ticket_counts"]

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        # Main validation details
        validation_df.to_excel(
            writer,
            sheet_name="Validation_Details",
            index=False
        )

        # Summary
        summary_df.to_excel(
            writer,
            sheet_name="Validation_Summary",
            index=False
        )

        # Orphan tickets
        if len(orphan_tickets) > 0:

            orphan_tickets.to_excel(
                writer,
                sheet_name="Orphan_Tickets",
                index=False
            )

        else:

            pd.DataFrame(
                {
                    "Message": [
                        "No orphan Support Tickets found."
                    ]
                }
            ).to_excel(
                writer,
                sheet_name="Orphan_Tickets",
                index=False
            )

        # Customers without tickets
        if len(customers_without_tickets) > 0:

            customers_without_tickets.to_excel(
                writer,
                sheet_name="Customers_Without_Tickets",
                index=False
            )

        else:

            pd.DataFrame(
                {
                    "Message": [
                        "All customers have at least one Support Ticket."
                    ]
                }
            ).to_excel(
                writer,
                sheet_name="Customers_Without_Tickets",
                index=False
            )

        # Ticket count per customer
        ticket_counts.to_excel(
            writer,
            sheet_name="Tickets_Per_Customer",
            index=False
        )

    print("\n")
    print("VALIDATION REPORT SAVED")
    print("\n")

    print(OUTPUT_FILE)


######   MAIN   ######

def main():

    try:
        
        # Load
        
        customers, support_tickets = load_data()
        
        # Validate required columns before standardization
        
        required_customer_columns = {
            CUSTOMER_KEY
        }

        required_ticket_columns = {
            CUSTOMER_KEY,
            TICKET_KEY
        }

        missing_customer_columns = (
            required_customer_columns
            - set(customers.columns)
        )

        missing_ticket_columns = (
            required_ticket_columns
            - set(support_tickets.columns)
        )

        if missing_customer_columns:

            raise ValueError(
                "Missing required columns in Customers: "
                + ", ".join(
                    sorted(missing_customer_columns)
                )
            )

        if missing_ticket_columns:

            raise ValueError(
                "Missing required columns in Support_Tickets: "
                + ", ".join(
                    sorted(missing_ticket_columns)
                )
            )
        
        # Standardize keys
        
        customers, support_tickets = standardize_keys(
            customers,
            support_tickets
        )
        
        # Validate
        
        validation_df, additional_data = (
            validate_referential_integrity(
                customers,
                support_tickets
            )
        )
        
        # Summary
        
        summary_df = create_validation_summary(
            validation_df
        )
        
        # Print
        
        print_results(
            validation_df,
            summary_df
        )
        
        # Save report
        
        save_validation_report(
            validation_df,
            summary_df,
            additional_data
        )

        print("\n")
        print(
            "CUSTOMERS ↔ SUPPORT TICKETS "
            "REFERENTIAL INTEGRITY VALIDATION COMPLETED"
        )
        print("\n")

    except FileNotFoundError as error:

        print("\nERROR: Required file not found.")
        print(error)

    except ValueError as error:

        print("\nERROR: Validation configuration problem.")
        print(error)

    except Exception as error:

        print("\nERROR: Unexpected error occurred.")
        print(error)


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()