"""
Final Customer Analytical Dataset
=================================

Purpose
-------
Build the final customer-level analytical dataset by combining:

1. Customers
2. Subscription + Churn data
3. Customer Services
4. Payment customer-level aggregation
5. Support Ticket customer-level aggregation

Final analytical grain
----------------------
1 row = 1 customer

Master table
------------
Customers

Join strategy
-------------
Customers
    LEFT JOIN Churn / Subscription
    LEFT JOIN Customer Services
    LEFT JOIN Payment Aggregation
    LEFT JOIN Support Ticket Aggregation

Important
---------
Payments and Support Tickets have already been aggregated
to customer level before this integration.

Therefore, the final dataset remains:

    1 row = 1 customer

Customers without support tickets are intentionally retained.
For such customers:

    total_ticket_count = 0
    resolved_ticket_count = 0
    unresolved_ticket_count = 0

Interaction-based support metrics remain missing because
there was no support interaction.

Output
------
outputs/final_data/
    final_customer_analytical_dataset.xlsx
    final_customer_dataset_report.xlsx
"""

from pathlib import Path
import pandas as pd



######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   DATA DIRECTORIES

CLEANED_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

CHURN_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "04_churn_processing"
)

AGGREGATED_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "06_aggregated_data"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "01_Data"
    / "03_Final"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

######   INPUT FILES

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


######   OUTPUT FILES

FINAL_DATASET_FILE = (
    OUTPUT_DIR
    / "final_customer_analytical_dataset.xlsx"
)

FINAL_REPORT_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "06_aggregated_data"
    / "final_customer_dataset_report.xlsx"
)


######   EXPECTED COLUMNS

CUSTOMER_COLUMNS = [
    "customer_id",
    "gender",
    "age",
    "city",
    "state",
    "signup_date",
]


CHURN_COLUMNS = [
    "customer_id",
    "subscription_id",
    "churn_status",
    "churn_date",
    "start_date",
    "end_date",
    "monthly_charge",
    "is_churned",
    "is_active",
    "has_churn_date",
    "has_end_date",
    "tenure_days_at_churn",
    "tenure_months_at_churn",
    "tenure_years_at_churn",
    "observation_date",
    "tenure_days",
    "tenure_months",
    "tenure_years",
    "churn_year",
    "churn_month",
    "churn_month_name",
    "churn_quarter",
    "churn_year_month",
    "tenure_segment",
    "churn_timing_segment",
    "churn_data_quality_flag",
    "plan",
    "contract_type",
]


SERVICE_COLUMNS = [
    "customer_id",
    "mobile_app",
    "streaming",
    "cloud_storage",
    "premium_support",
    "family_plan",
]

# IMPORTANT
# These are the payment columns actually required for the
# current final integration.
#
# We are NOT requiring:
#
# credit_card_payment_count
# debit_card_payment_count
# net_banking_payment_count
# upi_payment_count
# wallet_payment_count
#
# because the current payment aggregation output contains
# 27 columns and does not contain those five columns.
#
# Payment-method analysis can be handled later during
# Feature Engineering / EDA.

PAYMENT_COLUMNS = [
    "customer_id",
    "total_payment_count",
    "successful_payment_count",
    "failed_payment_count",
    "total_payment_amount",
    "successful_payment_amount",
    "failed_payment_amount",
    "average_payment_amount",
    "minimum_payment_amount",
    "maximum_payment_amount",
    "first_payment_date",
    "last_payment_date",
    "dataset_observation_date",
    "days_since_last_payment",
    "payment_success_rate",
    "payment_failure_rate",
    "payment_methods_used",
    "primary_payment_method",
    "payments_per_month",
    "has_failed_payment",
    "has_successful_payment",
    "successful_vs_failed_amount_difference",
]


SUPPORT_COLUMNS = [
    "customer_id",
    "total_ticket_count",
    "resolved_ticket_count",
    "unresolved_ticket_count",
    "average_resolution_time_hours",
    "minimum_resolution_time_hours",
    "maximum_resolution_time_hours",
    "average_satisfaction_score",
    "minimum_satisfaction_score",
    "maximum_satisfaction_score",
    "ticket_resolution_rate",
    "ticket_unresolved_rate",
    "account_ticket_count",
    "billing_ticket_count",
    "general_ticket_count",
    "performance_ticket_count",
    "technical_ticket_count",
    "unique_issue_types",
    "first_ticket_date",
    "last_ticket_date",
    "dataset_observation_date",
    "days_since_last_ticket",
    "tickets_per_month",
    "has_support_ticket",
    "high_support_usage",
    "has_unresolved_ticket",
    "has_low_satisfaction",
]


######   HELPER FUNCTIONS   ######

def load_excel_file(file_path, dataset_name):
    """
    Load an Excel file and display basic information.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"{dataset_name} file not found:\n"
            f"{file_path}"
        )

    df = pd.read_excel(file_path)

    print(
        f"{dataset_name} rows loaded    : "
        f"{len(df):,}"
    )

    print(
        f"{dataset_name} columns loaded : "
        f"{len(df.columns):,}"
    )

    return df


def standardize_columns(df):
    """
    Standardize column names.
    """

    df = df.copy()

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

    return df


def validate_required_columns(
    df,
    expected_columns,
    dataset_name
):
    """
    Validate required columns.
    """

    missing_columns = [
        column
        for column in expected_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"\n{dataset_name} is missing required columns:\n"
            f"{missing_columns}\n\n"
            f"Available columns are:\n"
            f"{list(df.columns)}"
        )


def prepare_customer_id(df):
    """
    Standardize customer_id.
    """

    df = df.copy()

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
    )

    return df


def check_unique_customer_id(
    df,
    dataset_name
):
    """
    Verify one row per customer.
    """

    duplicate_count = (
        df["customer_id"]
        .duplicated()
        .sum()
    )

    if duplicate_count > 0:

        raise ValueError(
            f"{dataset_name} contains "
            f"{duplicate_count:,} duplicate customer IDs."
            f"\nOne row per customer is required."
        )



######   LOAD ALL DATASETS   ######


def load_all_datasets():

    print("\n")
    print("LOADING DATASETS")
    print("\n")

    customers = load_excel_file(
        CUSTOMERS_FILE,
        "Customers"
    )

    churn = load_excel_file(
        CHURN_FILE,
        "Churn / Subscription"
    )

    customer_services = load_excel_file(
        CUSTOMER_SERVICES_FILE,
        "Customer Services"
    )

    payment_aggregation = load_excel_file(
        PAYMENT_AGGREGATION_FILE,
        "Payment Aggregation"
    )

    support_aggregation = load_excel_file(
        SUPPORT_AGGREGATION_FILE,
        "Support Ticket Aggregation"
    )

    ######   Standardize column names
    
    customers = standardize_columns(
        customers
    )

    churn = standardize_columns(
        churn
    )

    customer_services = standardize_columns(
        customer_services
    )

    payment_aggregation = standardize_columns(
        payment_aggregation
    )

    support_aggregation = standardize_columns(
        support_aggregation
    )

    
    ######   Validate required columns

    validate_required_columns(
        customers,
        CUSTOMER_COLUMNS,
        "Customers"
    )

    validate_required_columns(
        churn,
        CHURN_COLUMNS,
        "Churn / Subscription"
    )

    validate_required_columns(
        customer_services,
        SERVICE_COLUMNS,
        "Customer Services"
    )

    validate_required_columns(
        payment_aggregation,
        PAYMENT_COLUMNS,
        "Payment Aggregation"
    )

    validate_required_columns(
        support_aggregation,
        SUPPORT_COLUMNS,
        "Support Ticket Aggregation"
    )

    
    ######   Prepare customer IDs

    customers = prepare_customer_id(
        customers
    )

    churn = prepare_customer_id(
        churn
    )

    customer_services = prepare_customer_id(
        customer_services
    )

    payment_aggregation = prepare_customer_id(
        payment_aggregation
    )

    support_aggregation = prepare_customer_id(
        support_aggregation
    )

    
    # Verify one row per customer
    

    check_unique_customer_id(
        customers,
        "Customers"
    )

    check_unique_customer_id(
        churn,
        "Churn / Subscription"
    )

    check_unique_customer_id(
        customer_services,
        "Customer Services"
    )

    check_unique_customer_id(
        payment_aggregation,
        "Payment Aggregation"
    )

    check_unique_customer_id(
        support_aggregation,
        "Support Ticket Aggregation"
    )

    return (
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    )


######   SELECT REQUIRED COLUMNS   ######

def prepare_datasets(
    customers,
    churn,
    customer_services,
    payment_aggregation,
    support_aggregation,
):

    customers = customers[
        CUSTOMER_COLUMNS
    ].copy()

    churn = churn[
        CHURN_COLUMNS
    ].copy()

    customer_services = customer_services[
        SERVICE_COLUMNS
    ].copy()

    payment_aggregation = payment_aggregation[
        PAYMENT_COLUMNS
    ].copy()

    support_aggregation = support_aggregation[
        SUPPORT_COLUMNS
    ].copy()

    return (
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    )



######   BUILD FINAL DATASET   ######


def build_final_dataset(
    customers,
    churn,
    customer_services,
    payment_aggregation,
    support_aggregation,
):

    print("\n")
    print("BUILDING FINAL CUSTOMER ANALYTICAL DATASET")
    print("\n")

    print(
        "\nFinal analytical grain:"
    )

    print(
        "1 row = 1 customer"
    )


    # MASTER TABLE

    final_df = customers.copy()

    print(
        f"\nStarting Customers rows : "
        f"{len(final_df):,}"
    )

    # Customers + Churn

    final_df = final_df.merge(
        churn,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    print(
        f"After Churn merge       : "
        f"{len(final_df):,}"
    )

    # + Customer Services

    final_df = final_df.merge(
        customer_services,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    print(
        f"After Services merge    : "
        f"{len(final_df):,}"
    )

    # + Payment Aggregation

    final_df = final_df.merge(
        payment_aggregation,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    print(
        f"After Payment merge     : "
        f"{len(final_df):,}"
    )

    # + Support Aggregation

    final_df = final_df.merge(
        support_aggregation,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    print(
        f"After Support merge     : "
        f"{len(final_df):,}"
    )

    return final_df


######   HANDLE CUSTOMERS WITHOUT SUPPORT TICKETS   ######

def handle_missing_support_activity(
    final_df
):

    final_df = final_df.copy()

    print(
        "\nHandling customers without support tickets..."
    )
    
    # Count fields

    support_count_columns = [
        "total_ticket_count",
        "resolved_ticket_count",
        "unresolved_ticket_count",
        "account_ticket_count",
        "billing_ticket_count",
        "general_ticket_count",
        "performance_ticket_count",
        "technical_ticket_count",
    ]
    
    # Flag fields

    support_flag_columns = [
        "has_support_ticket",
        "high_support_usage",
        "has_unresolved_ticket",
        "has_low_satisfaction",
    ]

    # Rate fields

    support_rate_columns = [
        "ticket_resolution_rate",
        "ticket_unresolved_rate",
    ]

    # Customers with no support aggregation record
    
    no_support_mask = (
        final_df[
            "total_ticket_count"
        ]
        .isna()
    )

    no_support_count = (
        no_support_mask.sum()
    )

    print(
        f"Customers without support tickets : "
        f"{no_support_count:,}"
    )
   
    # Count fields → 0

    for column in support_count_columns:

        if column in final_df.columns:

            final_df.loc[
                no_support_mask,
                column
            ] = 0

    # Flags → 0

    for column in support_flag_columns:

        if column in final_df.columns:

            final_df.loc[
                no_support_mask,
                column
            ] = 0
    
    # Rates → 0    

    for column in support_rate_columns:

        if column in final_df.columns:

            final_df.loc[
                no_support_mask,
                column
            ] = 0

    
    # IMPORTANT
    # Do NOT fill:
    #
    # average_resolution_time_hours
    # minimum_resolution_time_hours
    # maximum_resolution_time_hours
    # average_satisfaction_score
    # minimum_satisfaction_score
    # maximum_satisfaction_score
    #
    # These remain NaN because there was no support
    # interaction.
    

    return final_df


######   CREATE FINAL OBSERVATION DATE   ######


def create_final_observation_date(
    final_df
):

    final_df = final_df.copy()

    date_columns = [
        "signup_date",
        "start_date",
        "end_date",
        "churn_date",
        "last_payment_date",
        "last_ticket_date",
    ]

    available_date_series = []

    for column in date_columns:

        if column in final_df.columns:

            final_df[column] = pd.to_datetime(
                final_df[column],
                errors="coerce"
            )

            available_date_series.append(
                final_df[column]
            )

    if available_date_series:

        final_df[
            "final_observation_date"
        ] = pd.concat(
            available_date_series,
            axis=1
        ).max(
            axis=1
        )

    else:

        final_df[
            "final_observation_date"
        ] = pd.NaT

    return final_df



######   FINAL DATA TYPES   ######


def finalize_data_types(
    final_df
):

    final_df = final_df.copy()

    # Customer ID    

    final_df["customer_id"] = (
        final_df["customer_id"]
        .astype("string")
        .str.strip()
    )

    # Date columns    

    date_columns = [
        "signup_date",
        "churn_date",
        "start_date",
        "end_date",
        "observation_date",
        "first_payment_date",
        "last_payment_date",
        "dataset_observation_date",
        "first_ticket_date",
        "last_ticket_date",
        "final_observation_date",
    ]

    for column in date_columns:

        if column in final_df.columns:

            final_df[column] = pd.to_datetime(
                final_df[column],
                errors="coerce"
            )
    
    # Numeric columns

    numeric_columns = [
        "age",
        "monthly_charge",

        "tenure_days_at_churn",
        "tenure_months_at_churn",
        "tenure_years_at_churn",
        "tenure_days",
        "tenure_months",
        "tenure_years",

        "total_payment_count",
        "successful_payment_count",
        "failed_payment_count",
        "total_payment_amount",
        "successful_payment_amount",
        "failed_payment_amount",
        "average_payment_amount",
        "minimum_payment_amount",
        "maximum_payment_amount",
        "days_since_last_payment",
        "payment_success_rate",
        "payment_failure_rate",
        "payments_per_month",
        "successful_vs_failed_amount_difference",

        "total_ticket_count",
        "resolved_ticket_count",
        "unresolved_ticket_count",
        "average_resolution_time_hours",
        "minimum_resolution_time_hours",
        "maximum_resolution_time_hours",
        "average_satisfaction_score",
        "minimum_satisfaction_score",
        "maximum_satisfaction_score",
        "ticket_resolution_rate",
        "ticket_unresolved_rate",
        "account_ticket_count",
        "billing_ticket_count",
        "general_ticket_count",
        "performance_ticket_count",
        "technical_ticket_count",
        "unique_issue_types",
        "days_since_last_ticket",
        "tickets_per_month",
    ]

    for column in numeric_columns:

        if column in final_df.columns:

            final_df[column] = pd.to_numeric(
                final_df[column],
                errors="coerce"
            )

    return final_df


######   COLUMN ORDER   ######

def order_final_columns(
    final_df
):

    preferred_order = [

        # CUSTOMER        

        "customer_id",
        "gender",
        "age",
        "city",
        "state",
        "signup_date",
       
        # SUBSCRIPTION / CHURN        

        "subscription_id",
        "plan",
        "contract_type",
        "start_date",
        "end_date",
        "monthly_charge",
        "churn_status",
        "churn_date",
        "is_churned",
        "is_active",
        "has_churn_date",
        "has_end_date",
        
        # TENURE        

        "tenure_days_at_churn",
        "tenure_months_at_churn",
        "tenure_years_at_churn",
        "tenure_days",
        "tenure_months",
        "tenure_years",
        "tenure_segment",
    
        # CHURN TIMING        

        "churn_year",
        "churn_month",
        "churn_month_name",
        "churn_quarter",
        "churn_year_month",
        "churn_timing_segment",
        "churn_data_quality_flag",
       
        # CUSTOMER SERVICES        

        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
      
        # PAYMENT        

        "total_payment_count",
        "successful_payment_count",
        "failed_payment_count",
        "total_payment_amount",
        "successful_payment_amount",
        "failed_payment_amount",
        "average_payment_amount",
        "minimum_payment_amount",
        "maximum_payment_amount",
        "first_payment_date",
        "last_payment_date",
        "dataset_observation_date",
        "days_since_last_payment",
        "payment_success_rate",
        "payment_failure_rate",
        "payment_methods_used",
        "primary_payment_method",
        "payments_per_month",
        "has_failed_payment",
        "has_successful_payment",
        "successful_vs_failed_amount_difference",
      
        # SUPPORT     

        "total_ticket_count",
        "resolved_ticket_count",
        "unresolved_ticket_count",
        "average_resolution_time_hours",
        "minimum_resolution_time_hours",
        "maximum_resolution_time_hours",
        "average_satisfaction_score",
        "minimum_satisfaction_score",
        "maximum_satisfaction_score",
        "ticket_resolution_rate",
        "ticket_unresolved_rate",
        "account_ticket_count",
        "billing_ticket_count",
        "general_ticket_count",
        "performance_ticket_count",
        "technical_ticket_count",
        "unique_issue_types",
        "first_ticket_date",
        "last_ticket_date",
        "days_since_last_ticket",
        "tickets_per_month",
        "has_support_ticket",
        "high_support_usage",
        "has_unresolved_ticket",
        "has_low_satisfaction",
      
        # FINAL OBSERVATION DATE        

        "final_observation_date",
    ]

    existing_columns = [
        column
        for column in preferred_order
        if column in final_df.columns
    ]

    remaining_columns = [
        column
        for column in final_df.columns
        if column not in existing_columns
    ]

    return final_df[
        existing_columns
        + remaining_columns
    ]

######   CREATE REPORT   ######

def create_final_report(
    customers,
    churn,
    customer_services,
    payment_aggregation,
    support_aggregation,
    final_df,
):

    report_rows = []

    expected_customer_count = len(
        customers
    )

    # 1. ROW COUNT    

    report_rows.append(
        {
            "Check_Name": "Final Row Count",
            "Check_Type": "Structural",
            "Expected": expected_customer_count,
            "Actual": len(final_df),
            "Status": (
                "PASS"
                if len(final_df)
                == expected_customer_count
                else "FAIL"
            ),
            "Explanation":
                "Final dataset should preserve every customer."
        }
    )

    # 2. COLUMN COUNT    

    report_rows.append(
        {
            "Check_Name": "Final Column Count",
            "Check_Type": "Structural",
            "Expected": "> 0",
            "Actual": len(final_df.columns),
            "Status": (
                "PASS"
                if len(final_df.columns) > 0
                else "FAIL"
            ),
            "Explanation":
                "Final dataset must contain analytical columns."
        }
    )
 
    # 3. MISSING CUSTOMER IDS    

    missing_customer_ids = (
        final_df[
            "customer_id"
        ]
        .isna()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Missing Customer IDs",
            "Check_Type":
                "Completeness",
            "Expected":
                0,
            "Actual":
                missing_customer_ids,
            "Status":
                (
                    "PASS"
                    if missing_customer_ids == 0
                    else "FAIL"
                ),
            "Explanation":
                "Customer ID is the analytical primary key."
        }
    )

    # 4. DUPLICATE CUSTOMER IDS    

    duplicate_customer_ids = (
        final_df[
            "customer_id"
        ]
        .duplicated()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Duplicate Customer IDs",
            "Check_Type":
                "Uniqueness",
            "Expected":
                0,
            "Actual":
                duplicate_customer_ids,
            "Status":
                (
                    "PASS"
                    if duplicate_customer_ids == 0
                    else "FAIL"
                ),
            "Explanation":
                "Final dataset must have one row per customer."
        }
    )

    # 5. CUSTOMER PRESERVATION

    customer_ids = set(
        customers[
            "customer_id"
        ]
    )

    final_customer_ids = set(
        final_df[
            "customer_id"
        ]
    )

    missing_from_final = (
        customer_ids
        - final_customer_ids
    )

    unexpected_final_customers = (
        final_customer_ids
        - customer_ids
    )

    report_rows.append(
        {
            "Check_Name":
                "Customers Missing From Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(missing_from_final),
            "Status":
                (
                    "PASS"
                    if len(missing_from_final) == 0
                    else "FAIL"
                ),
            "Explanation":
                "No customer from Customers should be lost."
        }
    )

    report_rows.append(
        {
            "Check_Name":
                "Unexpected Customers In Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(unexpected_final_customers),
            "Status":
                (
                    "PASS"
                    if len(unexpected_final_customers) == 0
                    else "FAIL"
                ),
            "Explanation":
                "Final dataset should not introduce new customer IDs."
        }
    )

    # 6. CHURN COVERAGE

    churn_ids = set(
        churn[
            "customer_id"
        ]
    )

    churn_missing = (
        churn_ids
        - final_customer_ids
    )

    report_rows.append(
        {
            "Check_Name":
                "Churn Customers Missing From Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(churn_missing),
            "Status":
                (
                    "PASS"
                    if len(churn_missing) == 0
                    else "FAIL"
                ),
            "Explanation":
                "All churn/subscription customers should be represented."
        }
    )

    # 7. CUSTOMER SERVICES COVERAGE

    service_ids = set(
        customer_services[
            "customer_id"
        ]
    )

    service_missing = (
        service_ids
        - final_customer_ids
    )

    report_rows.append(
        {
            "Check_Name":
                "Service Customers Missing From Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(service_missing),
            "Status":
                (
                    "PASS"
                    if len(service_missing) == 0
                    else "FAIL"
                ),
            "Explanation":
                "Every Customer Services record should match a customer."
        }
    )

    # 8. PAYMENT COVERAGE   

    payment_ids = set(
        payment_aggregation[
            "customer_id"
        ]
    )

    payment_missing = (
        payment_ids
        - final_customer_ids
    )

    report_rows.append(
        {
            "Check_Name":
                "Payment Customers Missing From Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(payment_missing),
            "Status":
                (
                    "PASS"
                    if len(payment_missing) == 0
                    else "FAIL"
                ),
            "Explanation":
                "Every payment aggregation record should match a customer."
        }
    )

    # 9. SUPPORT COVERAGE

    support_ids = set(
        support_aggregation[
            "customer_id"
        ]
    )

    support_missing = (
        support_ids
        - final_customer_ids
    )

    report_rows.append(
        {
            "Check_Name":
                "Support Customers Missing From Final Dataset",
            "Check_Type":
                "Referential Integrity",
            "Expected":
                0,
            "Actual":
                len(support_missing),
            "Status":
                (
                    "PASS"
                    if len(support_missing) == 0
                    else "FAIL"
                ),
            "Explanation":
                "Every support aggregation record should match a customer."
        }
    )
    
    # 10. CUSTOMERS WITHOUT SUPPORT    

    customers_without_support = (
        expected_customer_count
        - len(support_ids)
    )

    report_rows.append(
        {
            "Check_Name":
                "Customers Without Support Tickets",
            "Check_Type":
                "Business Information",
            "Expected":
                "Informational",
            "Actual":
                customers_without_support,
            "Status":
                "INFO",
            "Explanation":
                "Customers without tickets are intentionally retained."
        }
    )
    
    # 11. SUPPORT COUNT DEFAULT    

    missing_ticket_counts = (
        final_df[
            "total_ticket_count"
        ]
        .isna()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Missing Total Ticket Count After Merge",
            "Check_Type":
                "Business Rule",
            "Expected":
                0,
            "Actual":
                missing_ticket_counts,
            "Status":
                (
                    "PASS"
                    if missing_ticket_counts == 0
                    else "FAIL"
                ),
            "Explanation":
                "Customers without tickets should have count = 0."
        }
    )
    
    # 12. SUPPORT CUSTOMER RECONCILIATION    

    final_support_customer_count = (
        (
            final_df[
                "total_ticket_count"
            ]
            > 0
        )
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Support Customer Count Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                len(support_aggregation),
            "Actual":
                final_support_customer_count,
            "Status":
                (
                    "PASS"
                    if final_support_customer_count
                    == len(support_aggregation)
                    else "FAIL"
                ),
            "Explanation":
                "Customers with tickets should reconcile with support aggregation."
        }
    )
    
    # 13. PAYMENT CUSTOMER RECONCILIATION    

    final_payment_customer_count = (
        final_df[
            "total_payment_count"
        ]
        .notna()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Payment Customer Count Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                len(payment_aggregation),
            "Actual":
                final_payment_customer_count,
            "Status":
                (
                    "PASS"
                    if final_payment_customer_count
                    == len(payment_aggregation)
                    else "FAIL"
                ),
            "Explanation":
                "Payment aggregation should cover every customer."
        }
    )
    
    # 14. PAYMENT COUNT RECONCILIATION    

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

    payment_difference = abs(
        source_payment_count
        - final_payment_count
    )

    report_rows.append(
        {
            "Check_Name":
                "Payment Count Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_payment_count,
                    2
                ),
            "Actual":
                round(
                    final_payment_count,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if payment_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Total payment count must remain unchanged."
        }
    )
   
    # 15. PAYMENT AMOUNT RECONCILIATION    

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

    report_rows.append(
        {
            "Check_Name":
                "Payment Amount Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_payment_amount,
                    2
                ),
            "Actual":
                round(
                    final_payment_amount,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if payment_amount_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Total payment amount must remain unchanged."
        }
    )
    
    # 16. SUPPORT TICKET RECONCILIATION    

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

    ticket_difference = abs(
        source_ticket_count
        - final_ticket_count
    )

    report_rows.append(
        {
            "Check_Name":
                "Support Ticket Count Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_ticket_count,
                    2
                ),
            "Actual":
                round(
                    final_ticket_count,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if ticket_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Total support tickets must remain unchanged."
        }
    )
    
    # 17. RESOLVED TICKET RECONCILIATION    

    source_resolved = (
        support_aggregation[
            "resolved_ticket_count"
        ]
        .sum()
    )

    final_resolved = (
        final_df[
            "resolved_ticket_count"
        ]
        .sum()
    )

    resolved_difference = abs(
        source_resolved
        - final_resolved
    )

    report_rows.append(
        {
            "Check_Name":
                "Resolved Ticket Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_resolved,
                    2
                ),
            "Actual":
                round(
                    final_resolved,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if resolved_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Resolved ticket count must remain unchanged."
        }
    )

    
    # 18. UNRESOLVED TICKET RECONCILIATION    

    source_unresolved = (
        support_aggregation[
            "unresolved_ticket_count"
        ]
        .sum()
    )

    final_unresolved = (
        final_df[
            "unresolved_ticket_count"
        ]
        .sum()
    )

    unresolved_difference = abs(
        source_unresolved
        - final_unresolved
    )

    report_rows.append(
        {
            "Check_Name":
                "Unresolved Ticket Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_unresolved,
                    2
                ),
            "Actual":
                round(
                    final_unresolved,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if unresolved_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Unresolved ticket count must remain unchanged."
        }
    )
    
    # 19. CHURN RECONCILIATION    

    source_churn = (
        churn[
            "is_churned"
        ]
        .sum()
    )

    final_churn = (
        final_df[
            "is_churned"
        ]
        .sum()
    )

    churn_difference = abs(
        source_churn
        - final_churn
    )

    report_rows.append(
        {
            "Check_Name":
                "Churn Count Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_churn,
                    2
                ),
            "Actual":
                round(
                    final_churn,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if churn_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Churned customer count must remain unchanged."
        }
    )
    
    # 20. ACTIVE RECONCILIATION    

    source_active = (
        churn[
            "is_active"
        ].sum()
    )

    final_active = (
        final_df[
            "is_active"
        ].sum()
    )

    active_difference = abs(
        source_active
        - final_active
    )

    report_rows.append(
        {
            "Check_Name":
                "Active Customer Reconciliation",
            "Check_Type":
                "Reconciliation",
            "Expected":
                round(
                    source_active,
                    2
                ),
            "Actual":
                round(
                    final_active,
                    2
                ),
            "Status":
                (
                    "PASS"
                    if active_difference <= 0.01
                    else "FAIL"
                ),
            "Explanation":
                "Active customer count must remain unchanged."
        }
    )
    
    # 21. ACTIVE + CHURNED    

    active_churn_total = (
        final_active
        + final_churn
    )

    report_rows.append(
        {
            "Check_Name":
                "Active + Churned Customer Count",
            "Check_Type":
                "Business Rule",
            "Expected":
                expected_customer_count,
            "Actual":
                active_churn_total,
            "Status":
                (
                    "PASS"
                    if active_churn_total
                    == expected_customer_count
                    else "FAIL"
                ),
            "Explanation":
                "Every customer should be active or churned."
        }
    )
    
    # 22. NEGATIVE PAYMENT COUNT    

    negative_payment_counts = (
        (
            final_df[
                "total_payment_count"
            ]
            < 0
        )
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Negative Payment Counts",
            "Check_Type":
                "Data Quality",
            "Expected":
                0,
            "Actual":
                negative_payment_counts,
            "Status":
                (
                    "PASS"
                    if negative_payment_counts == 0
                    else "FAIL"
                ),
            "Explanation":
                "Payment counts cannot be negative."
        }
    )
    
    # 23. NEGATIVE TICKET COUNT    

    negative_ticket_counts = (
        (
            final_df[
                "total_ticket_count"
            ]
            < 0
        )
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Negative Support Ticket Counts",
            "Check_Type":
                "Data Quality",
            "Expected":
                0,
            "Actual":
                negative_ticket_counts,
            "Status":
                (
                    "PASS"
                    if negative_ticket_counts == 0
                    else "FAIL"
                ),
            "Explanation":
                "Support ticket counts cannot be negative."
        }
    )
    
    # 24. FINAL ROW MULTIPLICATION    

    expected_rows = (
        customers[
            "customer_id"
        ].nunique()
    )

    actual_rows = len(
        final_df
    )

    report_rows.append(
        {
            "Check_Name":
                "Final Row Multiplication",
            "Check_Type":
                "Structural",
            "Expected":
                expected_rows,
            "Actual":
                actual_rows,
            "Status":
                (
                    "PASS"
                    if expected_rows
                    == actual_rows
                    else "FAIL"
                ),
            "Explanation":
                "Joins must not multiply customer rows."
        }
    )
    
    # 25. NO-TICKET SUPPORT FLAG    

    no_ticket_mask = (
        final_df[
            "total_ticket_count"
        ]
        == 0
    )

    invalid_support_flags = (
        final_df.loc[
            no_ticket_mask,
            "has_support_ticket"
        ]
        != 0
    ).sum()

    report_rows.append(
        {
            "Check_Name":
                "No-Ticket Customer Support Flag",
            "Check_Type":
                "Business Rule",
            "Expected":
                0,
            "Actual":
                invalid_support_flags,
            "Status":
                (
                    "PASS"
                    if invalid_support_flags == 0
                    else "FAIL"
                ),
            "Explanation":
                "Customers with zero tickets should have has_support_ticket = 0."
        }
    )
    
    # 26. NO-TICKET SATISFACTION    

    no_ticket_satisfaction_values = (
        final_df.loc[
            no_ticket_mask,
            "average_satisfaction_score"
        ]
        .notna()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "No-Ticket Customers With Satisfaction Values",
            "Check_Type":
                "Business Rule",
            "Expected":
                0,
            "Actual":
                no_ticket_satisfaction_values,
            "Status":
                (
                    "PASS"
                    if no_ticket_satisfaction_values == 0
                    else "FAIL"
                ),
            "Explanation":
                "Customers without support interactions should not receive artificial satisfaction scores."
        }
    )
    
    # 27. TOTAL MISSING VALUES    

    total_missing_values = (
        final_df
        .isna()
        .sum()
        .sum()
    )

    report_rows.append(
        {
            "Check_Name":
                "Total Final Dataset Missing Values",
            "Check_Type":
                "Completeness",
            "Expected":
                "Informational",
            "Actual":
                total_missing_values,
            "Status":
                "INFO",
            "Explanation":
                "Missing values must be interpreted by business meaning."
        }
    )
    
    # FINAL REPORT    

    report_df = pd.DataFrame(
        report_rows
    )

    passed_checks = (
        report_df[
            "Status"
        ]
        == "PASS"
    ).sum()

    failed_checks = (
        report_df[
            "Status"
        ]
        == "FAIL"
    ).sum()

    info_checks = (
        report_df[
            "Status"
        ]
        == "INFO"
    ).sum()

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
                final_df[
                    "customer_id"
                ].nunique(),
                customers_without_support,
                source_churn,
                final_churn,
                source_active,
                final_active,
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
                len(report_df),
                passed_checks,
                failed_checks,
                info_checks,
                overall_status,
            ],
        }
    )
    
    # COLUMN QUALITY    

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

    return (
        report_df,
        summary_df,
        column_summary,
    )


######   SAVE OUTPUTS   ######


def save_outputs(
    final_df,
    report_df,
    summary_df,
    column_summary,
):

    print("\n")
    print("SAVING FINAL CUSTOMER DATASET")
    print("\n")

    final_df.to_excel(
        FINAL_DATASET_FILE,
        index=False
    )

    with pd.ExcelWriter(
        FINAL_REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        report_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False
        )

        column_summary.to_excel(
            writer,
            sheet_name="Column_Quality",
            index=False
        )

    print(
        "\nFinal Customer Analytical Dataset:"
    )

    print(
        FINAL_DATASET_FILE
    )

    print(
        "\nFinal Dataset Report:"
    )

    print(
        FINAL_REPORT_FILE
    )


######   MAIN   ######

def main():

    print("\n")
    print("FINAL CUSTOMER ANALYTICAL DATASET")

    
    # LOAD
    

    (
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    ) = load_all_datasets()

    
    # PREPARE
    

    (
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    ) = prepare_datasets(
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    )

    
    # BUILD
    

    final_df = build_final_dataset(
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
    )

    
    # SUPPORT NO-ACTIVITY HANDLING
    

    final_df = handle_missing_support_activity(
        final_df
    )

    
    # FINAL OBSERVATION DATE
    

    final_df = create_final_observation_date(
        final_df
    )

    
    # DATA TYPES
    

    final_df = finalize_data_types(
        final_df
    )

    
    # COLUMN ORDER
    

    final_df = order_final_columns(
        final_df
    )

    
    # REPORT
    

    (
        report_df,
        summary_df,
        column_summary,
    ) = create_final_report(
        customers,
        churn,
        customer_services,
        payment_aggregation,
        support_aggregation,
        final_df,
    )

    
    # SAVE
    

    save_outputs(
        final_df,
        report_df,
        summary_df,
        column_summary,
    )

    
    # CONSOLE SUMMARY
    

    passed_checks = (
        report_df[
            "Status"
        ]
        == "PASS"
    ).sum()

    failed_checks = (
        report_df[
            "Status"
        ]
        == "FAIL"
    ).sum()

    info_checks = (
        report_df[
            "Status"
        ]
        == "INFO"
    ).sum()

    overall_status = (
        "PASS"
        if failed_checks == 0
        else "FAIL"
    )

    print("\n")
    print("FINAL CUSTOMER DATASET COMPLETED")
    print("\n")

    print(
        f"Customers source rows       : "
        f"{len(customers):,}"
    )

    print(
        f"Final analytical rows       : "
        f"{len(final_df):,}"
    )

    print(
        f"Final analytical columns    : "
        f"{len(final_df.columns):,}"
    )

    print(
        f"Unique customers            : "
        f"{final_df['customer_id'].nunique():,}"
    )

    print(
        f"Duplicate customer IDs      : "
        f"{final_df['customer_id'].duplicated().sum():,}"
    )

    print(
        f"Total missing values        : "
        f"{final_df.isna().sum().sum():,}"
    )

    print(
        f"Passed Checks               : "
        f"{passed_checks}"
    )

    print(
        f"Failed Checks               : "
        f"{failed_checks}"
    )

    print(
        f"Info Checks                 : "
        f"{info_checks}"
    )

    print(
        f"Overall Final Dataset       : "
        f"{overall_status}"
    )


if __name__ == "__main__":
    main()