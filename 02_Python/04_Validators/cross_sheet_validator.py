"""
Cross-Sheet Referential Integrity Validator

Project:
Customer Churn & Retention Analysis

Purpose:
Validate the relationship between the Customers and
Subscriptions sheets after data cleaning.

Checks:
1. Customers customer_id is not missing
2. Customers customer_id is unique
3. Subscriptions customer_id is not missing
4. Every subscription customer exists in Customers
5. Every customer has a subscription
6. Customer ID overlap between sheets
7. Subscription count per customer
8. Relationship type between Customers and Subscriptions
9. Overall referential integrity status

Output:
outputs/validation_reports/
customers_subscriptions_referential_integrity.xlsx
"""

from pathlib import Path
import pandas as pd

######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   CLEANED DATA   ######

CLEANED_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)


######   INPUT FILES   ######

CUSTOMERS_FILE = (
    CLEANED_FOLDER
    / "customers_cleaned.xlsx"
)

SUBSCRIPTIONS_FILE = (
    CLEANED_FOLDER
    / "subscriptions_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "customers_subscriptions_referential_integrity.xlsx"
)


###### 2. EXPECTED COLUMNS   ######

CUSTOMER_ID_COLUMN = "customer_id"


######   3. LOAD CLEANED DATA   ######

def load_cleaned_data():
    """
    Load cleaned Customers and Subscriptions data.
    """

    print("LOADING CLEANED DATA")
    print("\n")

    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customers cleaned file not found:\n{CUSTOMERS_FILE}"
        )

    if not SUBSCRIPTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Subscriptions cleaned file not found:\n"
            f"{SUBSCRIPTIONS_FILE}"
        )

    customers_df = pd.read_excel(CUSTOMERS_FILE)

    subscriptions_df = pd.read_excel(SUBSCRIPTIONS_FILE)

    print(f"Customers rows       : {len(customers_df)}")
    print(f"Customers columns    : {len(customers_df.columns)}")

    print(f"Subscriptions rows   : {len(subscriptions_df)}")
    print(f"Subscriptions columns: {len(subscriptions_df.columns)}")

    print()

    return customers_df, subscriptions_df


######   4. VALIDATE REQUIRED COLUMNS   ######

def validate_required_columns(customers_df, subscriptions_df):
    """
    Check whether customer_id exists in both datasets.
    """

    print("CHECKING REQUIRED COLUMNS")
    print("\n")

    customers_has_id = CUSTOMER_ID_COLUMN in customers_df.columns
    subscriptions_has_id = CUSTOMER_ID_COLUMN in subscriptions_df.columns

    print(
        f"Customers '{CUSTOMER_ID_COLUMN}' exists     : "
        f"{customers_has_id}"
    )

    print(
        f"Subscriptions '{CUSTOMER_ID_COLUMN}' exists : "
        f"{subscriptions_has_id}"
    )

    if not customers_has_id:
        raise ValueError(
            f"'{CUSTOMER_ID_COLUMN}' column is missing "
            f"from Customers sheet."
        )

    if not subscriptions_has_id:
        raise ValueError(
            f"'{CUSTOMER_ID_COLUMN}' column is missing "
            f"from Subscriptions sheet."
        )

    print("Required column check completed.")
    print()


######   5. CLEAN CUSTOMER IDs   ######

def standardize_customer_ids(customers_df, subscriptions_df):
    """
    Standardize customer IDs before comparing the two sheets.

    Example:
        ' C00001 ' -> 'C00001'
    """

    customers_df[CUSTOMER_ID_COLUMN] = (
        customers_df[CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    subscriptions_df[CUSTOMER_ID_COLUMN] = (
        subscriptions_df[CUSTOMER_ID_COLUMN]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return customers_df, subscriptions_df


######   6. CHECK MISSING CUSTOMER IDs   ######

def check_missing_customer_ids(customers_df, subscriptions_df):
    """
    Check missing customer IDs in both sheets.
    """

    customer_missing = (
        customers_df[CUSTOMER_ID_COLUMN]
        .isna()
        .sum()
    )

    subscription_missing = (
        subscriptions_df[CUSTOMER_ID_COLUMN]
        .isna()
        .sum()
    )

    results = [
        {
            "Check": "Customers - Missing Customer IDs",
            "Value": customer_missing,
            "Status": "PASS" if customer_missing == 0 else "FAIL",
            "Description": (
                "Every customer record should have a customer ID."
            )
        },
        {
            "Check": "Subscriptions - Missing Customer IDs",
            "Value": subscription_missing,
            "Status": (
                "PASS"
                if subscription_missing == 0
                else "FAIL"
            ),
            "Description": (
                "Every subscription should be linked "
                "to a customer."
            )
        }
    ]

    return results


######   7. CHECK DUPLICATE CUSTOMER IDs   ######

def check_duplicate_customer_ids(customers_df, subscriptions_df):
    """
    Check duplicate customer IDs in both sheets.

    Customers:
        Expected to be unique.

    Subscriptions:
        Duplicate customer IDs would indicate
        multiple subscriptions for a customer.
    """

    customer_duplicate_count = (
        customers_df[CUSTOMER_ID_COLUMN]
        .dropna()
        .duplicated()
        .sum()
    )

    subscription_duplicate_count = (
        subscriptions_df[CUSTOMER_ID_COLUMN]
        .dropna()
        .duplicated()
        .sum()
    )

    results = [
        {
            "Check": "Customers - Duplicate Customer IDs",
            "Value": customer_duplicate_count,
            "Status": (
                "PASS"
                if customer_duplicate_count == 0
                else "FAIL"
            ),
            "Description": (
                "Customer ID should uniquely identify "
                "each customer."
            )
        },
        {
            "Check": "Subscriptions - Duplicate Customer IDs",
            "Value": subscription_duplicate_count,
            "Status": "INFO",
            "Description": (
                "Duplicate customer IDs are allowed only if "
                "customers can have multiple subscriptions."
            )
        }
    ]

    return results


######   8. CREATE CUSTOMER ID SETS   ######

def create_customer_id_sets(customers_df, subscriptions_df):
    """
    Create sets of valid customer IDs.

    Sets make it easy to identify:
        - orphan subscription records
        - customers without subscriptions
        - common customers
    """

    customer_ids = set(
        customers_df[CUSTOMER_ID_COLUMN]
        .dropna()
    )

    subscription_customer_ids = set(
        subscriptions_df[CUSTOMER_ID_COLUMN]
        .dropna()
    )

    return customer_ids, subscription_customer_ids


######   9. CHECK ORPHAN SUBSCRIPTIONS   ######

def check_orphan_subscriptions(
    customer_ids,
    subscription_customer_ids
):
    """
    Identify subscriptions whose customer_id does not
    exist in the Customers sheet.

    Example:

    Customers:
        C00001
        C00002
        C00003

    Subscriptions:
        C00001
        C00002
        C99999

    C99999 is an orphan subscription.
    """

    orphan_customer_ids = (
        subscription_customer_ids
        - customer_ids
    )

    orphan_count = len(orphan_customer_ids)

    result = {
        "Check": (
            "Subscriptions - Orphan Customer IDs"
        ),
        "Value": orphan_count,
        "Status": (
            "PASS"
            if orphan_count == 0
            else "FAIL"
        ),
        "Description": (
            "Every subscription customer_id must exist "
            "in the Customers sheet."
        )
    }

    return result, orphan_customer_ids


###### 10. CHECK CUSTOMERS WITHOUT SUBSCRIPTIONS   ######

def check_customers_without_subscriptions(
    customer_ids,
    subscription_customer_ids
):
    """
    Identify customers who do not have a subscription.
    """

    customers_without_subscription = (
        customer_ids
        - subscription_customer_ids
    )

    count = len(customers_without_subscription)

    result = {
        "Check": (
            "Customers - Without Subscription"
        ),
        "Value": count,
        "Status": "INFO",
        "Description": (
            "Customers without subscriptions may be valid "
            "depending on the business process."
        )
    }

    return result, customers_without_subscription


######   11. CHECK CUSTOMER ID OVERLAP   ######

def check_customer_overlap(
    customer_ids,
    subscription_customer_ids
):
    """
    Calculate how many customer IDs appear in both sheets.
    """

    common_customer_ids = (
        customer_ids
        & subscription_customer_ids
    )

    overlap_count = len(common_customer_ids)

    total_customers = len(customer_ids)

    if total_customers > 0:
        overlap_percentage = (
            overlap_count / total_customers
        ) * 100
    else:
        overlap_percentage = 0

    result = {
        "Check": "Customer ID Overlap",
        "Value": overlap_count,
        "Status": "INFO",
        "Description": (
            f"{overlap_percentage:.2f}% of Customers "
            f"have a matching customer_id in Subscriptions."
        )
    }

    return result

######   12. CHECK ROW COUNTS   ######

def check_row_counts(customers_df, subscriptions_df):
    """
    Compare total rows between Customers and Subscriptions.
    """

    customer_rows = len(customers_df)

    subscription_rows = len(subscriptions_df)

    difference = (
        customer_rows
        - subscription_rows
    )

    results = [
        {
            "Check": "Customers Row Count",
            "Value": customer_rows,
            "Status": "INFO",
            "Description": (
                "Total number of cleaned customer records."
            )
        },
        {
            "Check": "Subscriptions Row Count",
            "Value": subscription_rows,
            "Status": "INFO",
            "Description": (
                "Total number of cleaned subscription records."
            )
        },
        {
            "Check": "Customer vs Subscription Row Difference",
            "Value": difference,
            "Status": "INFO",
            "Description": (
                "A difference does not automatically indicate "
                "a data-quality issue."
            )
        }
    ]

    return results


######   13. CHECK UNIQUE CUSTOMER COUNTS   ######

def check_unique_customer_counts(
    customer_ids,
    subscription_customer_ids
):
    """
    Compare unique customer counts.
    """

    customer_unique_count = len(customer_ids)

    subscription_unique_count = (
        len(subscription_customer_ids)
    )

    results = [
        {
            "Check": "Unique Customers in Customers",
            "Value": customer_unique_count,
            "Status": "INFO",
            "Description": (
                "Number of unique customer IDs in Customers."
            )
        },
        {
            "Check": (
                "Unique Customers in Subscriptions"
            ),
            "Value": subscription_unique_count,
            "Status": "INFO",
            "Description": (
                "Number of unique customer IDs represented "
                "in Subscriptions."
            )
        }
    ]

    return results


######   14. CHECK RELATIONSHIP TYPE   ######

def determine_relationship(
    customers_df,
    subscriptions_df
):
    """
    Determine the relationship between Customers
    and Subscriptions.

    Possible relationships:

        One-to-One
        One-to-Many
        Many-to-Many
        Unknown

    Expected project relationship:

        Customers 1 ---- 1 Subscriptions

    if each customer has exactly one subscription.
    """

    customer_ids = (
        customers_df[CUSTOMER_ID_COLUMN]
        .dropna()
    )

    subscription_ids = (
        subscriptions_df[CUSTOMER_ID_COLUMN]
        .dropna()
    )

    customer_count = len(
        customer_ids
    )

    subscription_row_count = len(
        subscription_ids
    )

    unique_customer_count = (
        customer_ids.nunique()
    )

    unique_subscription_customer_count = (
        subscription_ids.nunique()
    )

    if (
        subscription_row_count
        == unique_subscription_customer_count
        and
        customer_count
        == unique_customer_count
        and
        customer_count
        == unique_subscription_customer_count
    ):
        relationship = "One-to-One"

    elif (
        subscription_row_count
        > unique_subscription_customer_count
    ):
        relationship = "One-to-Many"

    else:
        relationship = "Unknown"

    result = {
        "Check": "Customers to Subscriptions Relationship",
        "Value": relationship,
        "Status": "INFO",
        "Description": (
            "Relationship determined using customer_id "
            "uniqueness and subscription counts."
        )
    }

    return result


######   15. SUBSCRIPTION COUNT PER CUSTOMER   ######

def calculate_subscription_counts(subscriptions_df):
    """
    Calculate the number of subscriptions per customer.
    """

    subscription_counts = (
        subscriptions_df
        .dropna(subset=[CUSTOMER_ID_COLUMN])
        .groupby(CUSTOMER_ID_COLUMN)
        .size()
        .reset_index(name="subscription_count")
    )

    return subscription_counts


######   16. CHECK MULTIPLE SUBSCRIPTIONS   ######

def check_multiple_subscriptions(
    subscription_counts
):
    """
    Identify customers with more than one subscription.
    """

    multiple_subscription_customers = (
        subscription_counts[
            subscription_counts["subscription_count"] > 1
        ]
        .copy()
    )

    count = len(
        multiple_subscription_customers
    )

    result = {
        "Check": (
            "Customers with Multiple Subscriptions"
        ),
        "Value": count,
        "Status": "INFO",
        "Description": (
            "Multiple subscriptions may indicate a "
            "one-to-many relationship."
        )
    }

    return (
        result,
        multiple_subscription_customers
    )

  
######   17. CREATE ID DETAIL TABLES   ######

def create_id_detail_tables(
    orphan_customer_ids,
    customers_without_subscription,
    subscription_counts
):
    """
    Create detailed tables for IDs that require investigation.
    """

    orphan_df = pd.DataFrame(
        sorted(orphan_customer_ids),
        columns=[CUSTOMER_ID_COLUMN]
    )

    customers_without_subscription_df = pd.DataFrame(
        sorted(customers_without_subscription),
        columns=[CUSTOMER_ID_COLUMN]
    )

    return (
        orphan_df,
        customers_without_subscription_df,
        subscription_counts
    )


######    18. CREATE SUMMARY   ######

def create_summary(
    customers_df,
    subscriptions_df,
    customer_ids,
    subscription_customer_ids,
    orphan_customer_ids,
    customers_without_subscription,
    relationship
):
    """
    Create overall referential integrity summary.
    """

    total_customers = len(
        customers_df
    )

    total_subscriptions = len(
        subscriptions_df
    )

    unique_customers = len(
        customer_ids
    )

    unique_subscription_customers = len(
        subscription_customer_ids
    )

    orphan_count = len(
        orphan_customer_ids
    )

    customers_without_subscription_count = len(
        customers_without_subscription
    )

    common_customer_count = len(
        customer_ids
        & subscription_customer_ids
    )

    if total_customers > 0:
        customer_coverage_percentage = (
            common_customer_count
            / total_customers
        ) * 100
    else:
        customer_coverage_percentage = 0

    if total_subscriptions > 0:
        subscription_coverage_percentage = (
            common_customer_count
            / unique_subscription_customers
        ) * 100
    else:
        subscription_coverage_percentage = 0

    overall_status = (
        "PASS"
        if orphan_count == 0
        else "FAIL"
    )

    summary = pd.DataFrame(
        [
            {
                "Metric": "Total Customers",
                "Value": total_customers
            },
            {
                "Metric": "Total Subscriptions",
                "Value": total_subscriptions
            },
            {
                "Metric": "Unique Customer IDs",
                "Value": unique_customers
            },
            {
                "Metric": (
                    "Unique Customer IDs in Subscriptions"
                ),
                "Value": unique_subscription_customers
            },
            {
                "Metric": "Matching Customer IDs",
                "Value": common_customer_count
            },
            {
                "Metric": (
                    "Customers Without Subscription"
                ),
                "Value": customers_without_subscription_count
            },
            {
                "Metric": "Orphan Subscription Customers",
                "Value": orphan_count
            },
            {
                "Metric": (
                    "Customer Coverage Percentage"
                ),
                "Value": round(
                    customer_coverage_percentage,
                    2
                )
            },
            {
                "Metric": (
                    "Subscription Customer Coverage Percentage"
                ),
                "Value": round(
                    subscription_coverage_percentage,
                    2
                )
            },
            {
                "Metric": "Relationship",
                "Value": relationship
            },
            {
                "Metric": "Overall Referential Integrity",
                "Value": overall_status
            }
        ]
    )

    return summary


######   19. SAVE EXCEL REPORT   ######

def save_report(
    summary_df,
    validation_results_df,
    orphan_df,
    customers_without_subscription_df,
    subscription_counts_df,
    multiple_subscription_df
):
    """
    Save all validation results into a single Excel workbook.
    """

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        validation_results_df.to_excel(
            writer,
            sheet_name="Validation_Results",
            index=False
        )

        orphan_df.to_excel(
            writer,
            sheet_name="Orphan_Subscriptions",
            index=False
        )

        customers_without_subscription_df.to_excel(
            writer,
            sheet_name="Customers_No_Subscription",
            index=False
        )

        subscription_counts_df.to_excel(
            writer,
            sheet_name="Subscription_Counts",
            index=False
        )

        multiple_subscription_df.to_excel(
            writer,
            sheet_name="Multiple_Subscriptions",
            index=False
        )

    print()
    print("REPORT SAVED")
    print("\n")
    print(REPORT_FILE)


######    20. MAIN FUNCTION   ######

def main():

    print()
    print("CROSS-SHEET REFERENTIAL INTEGRITY VALIDATION")
    print("Customers ↔ Subscriptions")
    print("\n")
    print()
    
    # Step 1: Load data
    
    customers_df, subscriptions_df = (
        load_cleaned_data()
    )
    
    # Step 2: Validate required columns
    
    validate_required_columns(
        customers_df,
        subscriptions_df
    )
    
    # Step 3: Standardize IDs
    
    customers_df, subscriptions_df = (
        standardize_customer_ids(
            customers_df,
            subscriptions_df
        )
    )
    
    # Step 4: Create validation result list
    
    validation_results = []
    
    # Step 5: Missing ID checks
    
    validation_results.extend(
        check_missing_customer_ids(
            customers_df,
            subscriptions_df
        )
    )
    
    # Step 6: Duplicate ID checks
    
    validation_results.extend(
        check_duplicate_customer_ids(
            customers_df,
            subscriptions_df
        )
    )
    
    # Step 7: Create ID sets
    
    (
        customer_ids,
        subscription_customer_ids
    ) = create_customer_id_sets(
        customers_df,
        subscriptions_df
    )
    
    # Step 8: Check orphan subscriptions
    
    (
        orphan_result,
        orphan_customer_ids
    ) = check_orphan_subscriptions(
        customer_ids,
        subscription_customer_ids
    )

    validation_results.append(
        orphan_result
    )
    
    # Step 9: Check customers without subscriptions
    
    (
        no_subscription_result,
        customers_without_subscription
    ) = check_customers_without_subscriptions(
        customer_ids,
        subscription_customer_ids
    )

    validation_results.append(
        no_subscription_result
    )
    
    # Step 10: Customer overlap
    
    validation_results.append(
        check_customer_overlap(
            customer_ids,
            subscription_customer_ids
        )
    )
    
    # Step 11: Row count checks
    
    validation_results.extend(
        check_row_counts(
            customers_df,
            subscriptions_df
        )
    )
    
    # Step 12: Unique customer counts
    
    validation_results.extend(
        check_unique_customer_counts(
            customer_ids,
            subscription_customer_ids
        )
    )
    
    # Step 13: Determine relationship
    
    relationship_result = (
        determine_relationship(
            customers_df,
            subscriptions_df
        )
    )

    validation_results.append(
        relationship_result
    )

    relationship = relationship_result["Value"]
    
    # Step 14: Subscription count per customer
    
    subscription_counts_df = (
        calculate_subscription_counts(
            subscriptions_df
        )
    )
    
    # Step 15: Multiple subscriptions
    
    (
        multiple_subscription_result,
        multiple_subscription_df
    ) = check_multiple_subscriptions(
        subscription_counts_df
    )

    validation_results.append(
        multiple_subscription_result
    )
    
    # Step 16: Create detail tables
    
    (
        orphan_df,
        customers_without_subscription_df,
        subscription_counts_df
    ) = create_id_detail_tables(
        orphan_customer_ids,
        customers_without_subscription,
        subscription_counts_df
    )
    
    # Step 17: Create summary
    
    summary_df = create_summary(
        customers_df,
        subscriptions_df,
        customer_ids,
        subscription_customer_ids,
        orphan_customer_ids,
        customers_without_subscription,
        relationship
    )
    
    # Step 18: Convert validation results to DataFrame
    
    validation_results_df = pd.DataFrame(
        validation_results
    )
    
    # Step 19: Display results
    
    print()
    print("VALIDATION RESULTS")
    print("\n")
    print(
        validation_results_df[
            [
                "Check",
                "Value",
                "Status"
            ]
        ].to_string(index=False)
    )

    print()
    print("SUMMARY")
    print("\n")

    print(
        summary_df.to_string(index=False)
    )
    
    # Step 20: Save report
    
    save_report(
        summary_df,
        validation_results_df,
        orphan_df,
        customers_without_subscription_df,
        subscription_counts_df,
        multiple_subscription_df
    )

    print()
    print("CROSS-SHEET VALIDATION COMPLETED")


######   PROGRAM ENTRY POINT   ######

if __name__ == "__main__":
    main()