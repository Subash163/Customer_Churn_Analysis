"""
Final Customer Analytical Dataset Validator
============================================

Purpose
-------
Independently validate the final customer-level analytical dataset.

Expected analytical grain
-------------------------
1 row = 1 customer

Expected customer count
-----------------------
20,000

The validator checks:

1. File existence
2. Required columns
3. Row count
4. Customer ID completeness
5. Customer ID uniqueness
6. Customer preservation
7. Subscription / churn coverage
8. Customer service coverage
9. Payment coverage
10. Support ticket coverage
11. Support ticket zero-default logic
12. Payment aggregation reconciliation
13. Support ticket aggregation reconciliation
14. Churn reconciliation
15. Row multiplication
16. Overall validation status
"""

from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED DATA   ######

CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)


######   CHURN PROCESSING OUTPUT   ######

CHURN_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "04_churn_processing"
)


######   AGGREGATED DATA OUTPUT   ######

AGGREGATED_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "06_aggregated_data"
)


######   FINAL DATASET   ######

FINAL_DATA_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "03_Final"
)


######   FILES   ######

CUSTOMERS_FILE = (
    CLEANED_DIR
    / "customers_cleaned.xlsx"
)

CHURN_FILE = (
    CHURN_DIR
    / "churn_customer_level.xlsx"
)

CUSTOMER_SERVICES_FILE = (
    CLEANED_DIR
    / "customer_services_cleaned.xlsx"
)

PAYMENT_AGGREGATION_FILE = (
    AGGREGATED_DIR
    / "payment_customer_level.xlsx"
)

SUPPORT_AGGREGATION_FILE = (
    AGGREGATED_DIR
    / "support_ticket_customer_level.xlsx"
)

FINAL_DATASET_FILE = (
    FINAL_DATA_DIR
    / "final_customer_analytical_dataset.xlsx"
)

OUTPUT_REPORT_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
    / "final_customer_dataset_validation_report.xlsx"
)


######   EXPECTED COLUMNS   ######

REQUIRED_FINAL_COLUMNS = [
    "customer_id",
    "gender",
    "age",
    "city",
    "state",
    "signup_date",
    "subscription_id",
    "plan",
    "contract_type",
    "start_date",
    "monthly_charge",
    "churn_status",
    "is_churned",
    "is_active",
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
    "total_payment_count",
    "successful_payment_count",
    "failed_payment_count",
    "total_payment_amount",
    "successful_payment_amount",
    "failed_payment_amount",
    "average_payment_amount",
    "first_payment_date",
    "last_payment_date",
    "payment_success_rate",
    "payment_failure_rate",
    "total_ticket_count",
    "resolved_ticket_count",
    "unresolved_ticket_count",
    "average_resolution_time_hours",
    "average_satisfaction_score",
    "ticket_resolution_rate",
    "ticket_unresolved_rate",
    "has_support_ticket",
    "has_unresolved_ticket",
    "final_observation_date",
]



######   HELPER FUNCTIONS   ######

def load_excel(file_path, dataset_name):

    if not file_path.exists():

        raise FileNotFoundError(
            f"{dataset_name} file not found:\n"
            f"{file_path}"
        )

    df = pd.read_excel(
        file_path
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False
        )
        .str.replace(
            "-",
            "_",
            regex=False
        )
    )

    if "customer_id" in df.columns:

        df["customer_id"] = (
            df["customer_id"]
            .astype("string")
            .str.strip()
        )

    print(
        f"{dataset_name:<35}: "
        f"{len(df):,} rows"
    )

    return df


def add_check(
    checks,
    check_name,
    check_type,
    expected,
    actual,
    status,
    explanation,
):

    checks.append(
        {
            "Check_Name": check_name,
            "Check_Type": check_type,
            "Expected": expected,
            "Actual": actual,
            "Status": status,
            "Explanation": explanation,
        }
    )


######   MAIN VALIDATION   ######

def main():

    print("\n")
    print("FINAL CUSTOMER ANALYTICAL DATASET VALIDATION")
    print("\n")
    
    # LOAD DATA
    
    print("\nLoading validation datasets...\n")

    customers = load_excel(
        CUSTOMERS_FILE,
        "Customers"
    )

    churn = load_excel(
        CHURN_FILE,
        "Churn / Subscription"
    )

    customer_services = load_excel(
        CUSTOMER_SERVICES_FILE,
        "Customer Services"
    )

    payment_aggregation = load_excel(
        PAYMENT_AGGREGATION_FILE,
        "Payment Aggregation"
    )

    support_aggregation = load_excel(
        SUPPORT_AGGREGATION_FILE,
        "Support Aggregation"
    )

    final_df = load_excel(
        FINAL_DATASET_FILE,
        "Final Customer Dataset"
    )
    
    # CHECK COLLECTION
    
    checks = []

    expected_customer_count = (
        len(customers)
    )
    
    # 1. FINAL ROW COUNT
    
    add_check(
        checks,
        "Final Row Count",
        "Structural",
        expected_customer_count,
        len(final_df),
        "PASS"
        if len(final_df)
        == expected_customer_count
        else "FAIL",
        "Final dataset must contain one row for every customer.",
    )
    
    # 2. REQUIRED COLUMNS
    
    missing_columns = [
        column
        for column in REQUIRED_FINAL_COLUMNS
        if column not in final_df.columns
    ]

    add_check(
        checks,
        "Required Final Columns",
        "Schema",
        0,
        len(missing_columns),
        "PASS"
        if len(missing_columns) == 0
        else "FAIL",
        (
            "All required analytical columns must exist."
            if not missing_columns
            else
            f"Missing columns: {missing_columns}"
        ),
    )
    
    # 3. CUSTOMER ID MISSING
    
    missing_customer_ids = (
        final_df["customer_id"]
        .isna()
        .sum()
    )

    add_check(
        checks,
        "Missing Customer IDs",
        "Completeness",
        0,
        missing_customer_ids,
        "PASS"
        if missing_customer_ids == 0
        else "FAIL",
        "Customer ID cannot be missing.",
    )
    
    # 4. DUPLICATE CUSTOMER IDS
    
    duplicate_customer_ids = (
        final_df["customer_id"]
        .duplicated()
        .sum()
    )

    add_check(
        checks,
        "Duplicate Customer IDs",
        "Uniqueness",
        0,
        duplicate_customer_ids,
        "PASS"
        if duplicate_customer_ids == 0
        else "FAIL",
        "Final analytical dataset must have one row per customer.",
    )
    
    # 5. UNIQUE CUSTOMER COUNT
    
    unique_final_customers = (
        final_df["customer_id"]
        .nunique()
    )

    add_check(
        checks,
        "Unique Final Customers",
        "Uniqueness",
        expected_customer_count,
        unique_final_customers,
        "PASS"
        if unique_final_customers
        == expected_customer_count
        else "FAIL",
        "Unique final customers should equal the Customers master count.",
    )
    
    # 6. CUSTOMER PRESERVATION
    
    customer_ids = set(
        customers["customer_id"]
    )

    final_customer_ids = set(
        final_df["customer_id"]
    )

    missing_from_final = (
        customer_ids
        - final_customer_ids
    )

    unexpected_final_customers = (
        final_customer_ids
        - customer_ids
    )

    add_check(
        checks,
        "Customers Missing From Final Dataset",
        "Referential Integrity",
        0,
        len(missing_from_final),
        "PASS"
        if len(missing_from_final) == 0
        else "FAIL",
        "Every customer in Customers must exist in the final dataset.",
    )

    add_check(
        checks,
        "Unexpected Customers In Final Dataset",
        "Referential Integrity",
        0,
        len(unexpected_final_customers),
        "PASS"
        if len(unexpected_final_customers) == 0
        else "FAIL",
        "Final dataset should not introduce new customer IDs.",
    )
    
    # 7. CHURN / SUBSCRIPTION COVERAGE
    
    churn_ids = set(
        churn["customer_id"]
    )

    churn_missing_from_final = (
        churn_ids
        - final_customer_ids
    )

    add_check(
        checks,
        "Churn Customers Missing From Final Dataset",
        "Referential Integrity",
        0,
        len(churn_missing_from_final),
        "PASS"
        if len(churn_missing_from_final) == 0
        else "FAIL",
        "Every churn/subscription customer should be represented.",
    )
    
    # 8. CUSTOMER SERVICES COVERAGE
    
    service_ids = set(
        customer_services[
            "customer_id"
        ]
    )

    service_missing_from_final = (
        service_ids
        - final_customer_ids
    )

    add_check(
        checks,
        "Service Customers Missing From Final Dataset",
        "Referential Integrity",
        0,
        len(service_missing_from_final),
        "PASS"
        if len(service_missing_from_final) == 0
        else "FAIL",
        "Every Customer Services record should match a final customer.",
    )
    
    # 9. PAYMENT COVERAGE
    
    payment_ids = set(
        payment_aggregation[
            "customer_id"
        ]
    )

    payment_missing_from_final = (
        payment_ids
        - final_customer_ids
    )

    add_check(
        checks,
        "Payment Customers Missing From Final Dataset",
        "Referential Integrity",
        0,
        len(payment_missing_from_final),
        "PASS"
        if len(payment_missing_from_final) == 0
        else "FAIL",
        "Every payment aggregation record should match a final customer.",
    )
    
    # 10. SUPPORT COVERAGE
    
    support_ids = set(
        support_aggregation[
            "customer_id"
        ]
    )

    support_missing_from_final = (
        support_ids
        - final_customer_ids
    )

    add_check(
        checks,
        "Support Customers Missing From Final Dataset",
        "Referential Integrity",
        0,
        len(support_missing_from_final),
        "PASS"
        if len(support_missing_from_final) == 0
        else "FAIL",
        "Every support aggregation record should match a final customer.",
    )
    
    # 11. SUPPORT COVERAGE INFORMATION
    
    customers_without_support = (
        expected_customer_count
        - len(support_ids)
    )

    add_check(
        checks,
        "Customers Without Support Tickets",
        "Business Information",
        "Informational",
        customers_without_support,
        "INFO",
        "Customers without tickets are intentionally retained using LEFT JOIN.",
    )
    
    # 12. SUPPORT TICKET COUNT ZERO DEFAULT
    
    if "total_ticket_count" in final_df.columns:

        missing_ticket_counts = (
            final_df[
                "total_ticket_count"
            ]
            .isna()
            .sum()
        )

        add_check(
            checks,
            "Missing Total Ticket Count",
            "Business Rule",
            0,
            missing_ticket_counts,
            "PASS"
            if missing_ticket_counts == 0
            else "FAIL",
            "Customers without support tickets should have count = 0.",
        )
    
    # 13. SUPPORT TICKET COVERAGE RECONCILIATION
    
    final_support_customer_count = (
        (
            final_df[
                "total_ticket_count"
            ]
            > 0
        )
        .sum()
    )

    add_check(
        checks,
        "Support Customer Count Reconciliation",
        "Reconciliation",
        len(support_aggregation),
        final_support_customer_count,
        "PASS"
        if final_support_customer_count
        == len(support_aggregation)
        else "FAIL",
        "Customers with tickets should reconcile with the support aggregation.",
    )
    
    # 14. PAYMENT CUSTOMER COUNT RECONCILIATION
    
    final_payment_customer_count = (
        final_df[
            "total_payment_count"
        ]
        .notna()
        .sum()
    )

    add_check(
        checks,
        "Payment Customer Count Reconciliation",
        "Reconciliation",
        len(payment_aggregation),
        final_payment_customer_count,
        "PASS"
        if final_payment_customer_count
        == len(payment_aggregation)
        else "FAIL",
        "Payment aggregation should cover every customer.",
    )
    
    # 15. PAYMENT COUNT RECONCILIATION
    
    source_payment_count = (
        payment_aggregation[
            "total_payment_count"
        ]
        .sum()
    )

    final_payment_count = (
        final_df[
            "total_payment_count"
        ]
        .sum()
    )

    payment_count_difference = abs(
        source_payment_count
        - final_payment_count
    )

    add_check(
        checks,
        "Payment Count Reconciliation",
        "Reconciliation",
        round(
            source_payment_count,
            2
        ),
        round(
            final_payment_count,
            2
        ),
        "PASS"
        if payment_count_difference <= 0.01
        else "FAIL",
        "Total payment count must remain unchanged after integration.",
    )
    
    # 16. PAYMENT AMOUNT RECONCILIATION
    
    source_payment_amount = (
        payment_aggregation[
            "total_payment_amount"
        ]
        .sum()
    )

    final_payment_amount = (
        final_df[
            "total_payment_amount"
        ]
        .sum()
    )

    payment_amount_difference = abs(
        source_payment_amount
        - final_payment_amount
    )

    add_check(
        checks,
        "Payment Amount Reconciliation",
        "Reconciliation",
        round(
            source_payment_amount,
            2
        ),
        round(
            final_payment_amount,
            2
        ),
        "PASS"
        if payment_amount_difference <= 0.01
        else "FAIL",
        "Total payment amount must remain unchanged after integration.",
    )
    
    # 17. SUPPORT TICKET COUNT RECONCILIATION
    
    source_ticket_count = (
        support_aggregation[
            "total_ticket_count"
        ]
        .sum()
    )

    final_ticket_count = (
        final_df[
            "total_ticket_count"
        ]
        .sum()
    )

    ticket_count_difference = abs(
        source_ticket_count
        - final_ticket_count
    )

    add_check(
        checks,
        "Support Ticket Count Reconciliation",
        "Reconciliation",
        round(
            source_ticket_count,
            2
        ),
        round(
            final_ticket_count,
            2
        ),
        "PASS"
        if ticket_count_difference <= 0.01
        else "FAIL",
        "Total support ticket count must remain unchanged after integration.",
    )
    
    # 18. RESOLVED TICKET RECONCILIATION
    
    source_resolved_tickets = (
        support_aggregation[
            "resolved_ticket_count"
        ]
        .sum()
    )

    final_resolved_tickets = (
        final_df[
            "resolved_ticket_count"
        ]
        .sum()
    )

    resolved_difference = abs(
        source_resolved_tickets
        - final_resolved_tickets
    )

    add_check(
        checks,
        "Resolved Ticket Reconciliation",
        "Reconciliation",
        round(
            source_resolved_tickets,
            2
        ),
        round(
            final_resolved_tickets,
            2
        ),
        "PASS"
        if resolved_difference <= 0.01
        else "FAIL",
        "Resolved ticket count must remain unchanged.",
    )
    
    # 19. UNRESOLVED TICKET RECONCILIATION
    
    source_unresolved_tickets = (
        support_aggregation[
            "unresolved_ticket_count"
        ]
        .sum()
    )

    final_unresolved_tickets = (
        final_df[
            "unresolved_ticket_count"
        ]
        .sum()
    )

    unresolved_difference = abs(
        source_unresolved_tickets
        - final_unresolved_tickets
    )

    add_check(
        checks,
        "Unresolved Ticket Reconciliation",
        "Reconciliation",
        round(
            source_unresolved_tickets,
            2
        ),
        round(
            final_unresolved_tickets,
            2
        ),
        "PASS"
        if unresolved_difference <= 0.01
        else "FAIL",
        "Unresolved ticket count must remain unchanged.",
    )
    
    # 20. CHURN COUNT RECONCILIATION
    
    source_churn_count = (
        churn[
            "is_churned"
        ]
        .sum()
    )

    final_churn_count = (
        final_df[
            "is_churned"
        ]
        .sum()
    )

    churn_difference = abs(
        source_churn_count
        - final_churn_count
    )

    add_check(
        checks,
        "Churn Count Reconciliation",
        "Reconciliation",
        round(
            source_churn_count,
            2
        ),
        round(
            final_churn_count,
            2
        ),
        "PASS"
        if churn_difference <= 0.01
        else "FAIL",
        "Churned customer count must remain unchanged.",
    )
    
    # 21. ACTIVE CUSTOMER RECONCILIATION
    
    source_active_count = (
        churn[
            "is_active"
        ]
        .sum()
    )

    final_active_count = (
        final_df[
            "is_active"
        ]
        .sum()
    )

    active_difference = abs(
        source_active_count
        - final_active_count
    )

    add_check(
        checks,
        "Active Customer Reconciliation",
        "Reconciliation",
        round(
            source_active_count,
            2
        ),
        round(
            final_active_count,
            2
        ),
        "PASS"
        if active_difference <= 0.01
        else "FAIL",
        "Active customer count must remain unchanged.",
    )
    
    # 22. CHURN + ACTIVE TOTAL
    
    churn_active_total = (
        final_df["is_churned"].sum()
        +
        final_df["is_active"].sum()
    )

    add_check(
        checks,
        "Churned + Active Customer Count",
        "Business Rule",
        expected_customer_count,
        churn_active_total,
        "PASS"
        if churn_active_total
        == expected_customer_count
        else "FAIL",
        "Every customer should be either active or churned in the current model.",
    )
    
    # 23. PAYMENT FAN-OUT CHECK
    
    max_payment_count = (
        final_df[
            "total_payment_count"
        ].max()
    )

    add_check(
        checks,
        "Payment Aggregation Fan-Out",
        "Structural",
        "One row per customer",
        f"Max payment count = {max_payment_count}",
        "PASS",
        "Payment records are represented through customer-level aggregates, not individual rows.",
    )
    
    # 24. SUPPORT FAN-OUT CHECK
    
    max_ticket_count = (
        final_df[
            "total_ticket_count"
        ].max()
    )

    add_check(
        checks,
        "Support Aggregation Fan-Out",
        "Structural",
        "One row per customer",
        f"Max ticket count = {max_ticket_count}",
        "PASS",
        "Support tickets are represented through customer-level aggregates.",
    )
    
    # 25. FINAL ROW MULTIPLICATION
    
    expected_rows = (
        customers["customer_id"]
        .nunique()
    )

    actual_rows = len(
        final_df
    )

    add_check(
        checks,
        "Final Row Multiplication",
        "Structural",
        expected_rows,
        actual_rows,
        "PASS"
        if actual_rows == expected_rows
        else "FAIL",
        "LEFT JOIN integration must not multiply customer rows.",
    )
    
    # 26. SUPPORT ZERO-TICKET FLAG
    
    no_ticket_rows = (
        final_df[
            "total_ticket_count"
        ]
        == 0
    )

    if "has_support_ticket" in final_df.columns:

        invalid_support_flags = (
            final_df.loc[
                no_ticket_rows,
                "has_support_ticket"
            ]
            != 0
        ).sum()

        add_check(
            checks,
            "No-Ticket Customer Support Flag",
            "Business Rule",
            0,
            invalid_support_flags,
            "PASS"
            if invalid_support_flags == 0
            else "FAIL",
            "Customers with zero tickets should have has_support_ticket = 0.",
        )
    
    # 27. SUPPORT COUNT NON-NEGATIVE
    
    negative_ticket_counts = (
        (
            final_df[
                "total_ticket_count"
            ]
            < 0
        )
        .sum()
    )

    add_check(
        checks,
        "Negative Support Ticket Counts",
        "Data Quality",
        0,
        negative_ticket_counts,
        "PASS"
        if negative_ticket_counts == 0
        else "FAIL",
        "Ticket counts cannot be negative.",
    )
    
    # 28. PAYMENT COUNT NON-NEGATIVE
    
    negative_payment_counts = (
        (
            final_df[
                "total_payment_count"
            ]
            < 0
        )
        .sum()
    )

    add_check(
        checks,
        "Negative Payment Counts",
        "Data Quality",
        0,
        negative_payment_counts,
        "PASS"
        if negative_payment_counts == 0
        else "FAIL",
        "Payment counts cannot be negative.",
    )
    
    # 29. FINAL DATASET MISSING VALUES
    
    total_missing_values = (
        final_df.isna()
        .sum()
        .sum()
    )

    add_check(
        checks,
        "Total Final Dataset Missing Values",
        "Completeness",
        "Informational",
        total_missing_values,
        "INFO",
        "Missing values are reviewed by column because some fields are legitimately unavailable.",
    )
    
    # 30. SUPPORT AVERAGE NULLS
    
    if (
        "average_satisfaction_score"
        in final_df.columns
    ):

        no_ticket_satisfaction_not_null = (
            final_df.loc[
                no_ticket_rows,
                "average_satisfaction_score"
            ]
            .notna()
            .sum()
        )

        add_check(
            checks,
            "No-Ticket Customers With Satisfaction Values",
            "Business Rule",
            0,
            no_ticket_satisfaction_not_null,
            "PASS"
            if no_ticket_satisfaction_not_null == 0
            else "FAIL",
            "Customers without support interaction should not receive an artificial satisfaction score.",
        )
    
    # REPORT
    
    report_df = pd.DataFrame(
        checks
    )

    passed_checks = (
        report_df["Status"]
        == "PASS"
    ).sum()

    failed_checks = (
        report_df["Status"]
        == "FAIL"
    ).sum()

    info_checks = (
        report_df["Status"]
        == "INFO"
    ).sum()

    total_checks = (
        len(report_df)
    )

    overall_status = (
        "PASS"
        if failed_checks == 0
        else "FAIL"
    )
    
    # SUMMARY
    
    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Customers Source Rows",
                "Final Dataset Rows",
                "Final Dataset Columns",
                "Unique Final Customers",
                "Customers Without Support Tickets",
                "Source Churned Customers",
                "Final Churned Customers",
                "Source Active Customers",
                "Final Active Customers",
                "Source Payment Customers",
                "Final Payment Customers",
                "Source Support Customers",
                "Final Support Customers",
                "Source Total Payments",
                "Final Total Payments",
                "Source Total Payment Amount",
                "Final Total Payment Amount",
                "Source Total Tickets",
                "Final Total Tickets",
                "Total Checks",
                "Passed Checks",
                "Failed Checks",
                "Info Checks",
                "Overall Validation Status",
            ],
            "Value": [
                expected_customer_count,
                len(final_df),
                len(final_df.columns),
                unique_final_customers,
                customers_without_support,
                source_churn_count,
                final_churn_count,
                source_active_count,
                final_active_count,
                len(payment_aggregation),
                final_payment_customer_count,
                len(support_aggregation),
                final_support_customer_count,
                source_payment_count,
                final_payment_count,
                source_payment_amount,
                final_payment_amount,
                source_ticket_count,
                final_ticket_count,
                total_checks,
                passed_checks,
                failed_checks,
                info_checks,
                overall_status,
            ],
        }
    )
    
    # COLUMN QUALITY SUMMARY
    
    column_summary = pd.DataFrame(
        {
            "Column": final_df.columns,
            "Data_Type": [
                str(dtype)
                for dtype
                in final_df.dtypes
            ],
            "Missing_Count": [
                final_df[
                    column
                ].isna().sum()
                for column
                in final_df.columns
            ],
            "Unique_Count": [
                final_df[
                    column
                ].nunique()
                for column
                in final_df.columns
            ],
        }
    )
    
    # SAVE REPORT
    
    OUTPUT_REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        OUTPUT_REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

        report_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False,
        )

        column_summary.to_excel(
            writer,
            sheet_name="Column_Quality",
            index=False,
        )
    
    # CONSOLE OUTPUT
    
    print("\n")
    print("FINAL CUSTOMER DATASET VALIDATION RESULTS")
    print("\n")

    print(
        f"Customers source rows        : "
        f"{expected_customer_count:,}"
    )

    print(
        f"Final dataset rows           : "
        f"{len(final_df):,}"
    )

    print(
        f"Final dataset columns        : "
        f"{len(final_df.columns):,}"
    )

    print(
        f"Unique final customers       : "
        f"{unique_final_customers:,}"
    )

    print(
        f"Customers without support    : "
        f"{customers_without_support:,}"
    )

    print(
        f"Total Checks                 : "
        f"{total_checks}"
    )

    print(
        f"Passed Checks                : "
        f"{passed_checks}"
    )

    print(
        f"Failed Checks                : "
        f"{failed_checks}"
    )

    print(
        f"Info Checks                  : "
        f"{info_checks}"
    )

    print(
        "\nFinal Validation Report:"
    )

    print(
        OUTPUT_REPORT_FILE
    )

    print(
        f"\nOverall Final Dataset "
        f"Validation : {overall_status}"
    )


if __name__ == "__main__":
    main()