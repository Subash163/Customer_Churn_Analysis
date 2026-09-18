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

# INPUT FILE

SUPPORT_TICKETS_FILE = (
    CLEANED_DIR
    / "support_tickets_cleaned.xlsx"
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

# OUTPUT FILES

OUTPUT_FILE = (
    AGGREGATED_DIR
    / "support_ticket_customer_level.xlsx"
)

REPORT_FILE = (
    AGGREGATED_DIR
    / "support_ticket_aggregation_report.xlsx"
)

# EXPECTED COLUMNS

EXPECTED_COLUMNS = [
    "ticket_id",
    "customer_id",
    "ticket_date",
    "issue_type",
    "resolution_time_hours",
    "satisfaction_score",
    "resolved",
]

# STANDARDIZE COLUMN NAMES

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

# CLEAN BASIC DATA TYPES

def clean_basic_types(df):
    """
    Standardize data types required for aggregation.
    """

    df = df.copy()

    
    # IDs
    

    df["ticket_id"] = (
        df["ticket_id"]
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
  
    # Date    

    df["ticket_date"] = pd.to_datetime(
        df["ticket_date"],
        errors="coerce"
    )
  
    # Numeric columns    

    df["resolution_time_hours"] = pd.to_numeric(
        df["resolution_time_hours"],
        errors="coerce"
    )

    df["satisfaction_score"] = pd.to_numeric(
        df["satisfaction_score"],
        errors="coerce"
    )
    
    # Text columns    

    df["issue_type"] = (
        df["issue_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    df["resolved"] = (
        df["resolved"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    return df

# LOAD SUPPORT TICKETS

def load_support_tickets():
    """
    Load cleaned Support Tickets dataset.
    """

    print("\n")
    print("SUPPORT TICKET AGGREGATION - DATA LOADING")
    print("\n")

    if not SUPPORT_TICKETS_FILE.exists():

        raise FileNotFoundError(
            "Support Tickets file not found:\n"
            f"{SUPPORT_TICKETS_FILE}"
        )

    df = pd.read_excel(
        SUPPORT_TICKETS_FILE
    )

    print(
        f"Support Ticket rows loaded    : "
        f"{len(df):,}"
    )

    print(
        f"Support Ticket columns loaded : "
        f"{len(df.columns)}"
    )

    return df

# VALIDATE SOURCE COLUMNS

def validate_source_columns(df):
    """
    Validate required Support Ticket columns.
    """

    actual_columns = set(df.columns)

    expected_columns = set(
        EXPECTED_COLUMNS
    )

    missing_columns = (
        expected_columns
        - actual_columns
    )

    unexpected_columns = (
        actual_columns
        - expected_columns
    )

    if missing_columns:

        raise ValueError(
            "Missing required Support Ticket columns:\n"
            + "\n".join(
                sorted(missing_columns)
            )
        )

    if unexpected_columns:

        print(
            "\nINFO: Unexpected columns found:\n"
            + "\n".join(
                sorted(unexpected_columns)
            )
        )

    return True

# SOURCE DATA QUALITY CHECKS

def create_source_checks(df):
    """
    Perform source-level validation before aggregation.
    """

    checks = []

    def add_check(
        check_name,
        category,
        actual_value,
        expected,
        status,
        description
    ):
        checks.append(
            {
                "Check_Name": check_name,
                "Category": category,
                "Actual_Value": actual_value,
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
        "PASS"
        if len(df) > 0
        else "FAIL",
        "Support Ticket dataset contains records."
    )
    
    # Ticket ID    

    missing_ticket_ids = (
        df["ticket_id"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Ticket IDs",
        "Ticket ID",
        missing_ticket_ids,
        0,
        "PASS"
        if missing_ticket_ids == 0
        else "FAIL",
        "Every ticket should have a ticket ID."
    )

    duplicate_ticket_ids = (
        df["ticket_id"]
        .duplicated()
        .sum()
    )

    add_check(
        "Duplicate Ticket IDs",
        "Ticket ID",
        duplicate_ticket_ids,
        0,
        "PASS"
        if duplicate_ticket_ids == 0
        else "FAIL",
        "Ticket IDs should uniquely identify ticket records."
    )
   
    # Customer ID    

    missing_customer_ids = (
        df["customer_id"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Customer IDs",
        "Customer ID",
        missing_customer_ids,
        0,
        "PASS"
        if missing_customer_ids == 0
        else "FAIL",
        "Every support ticket should belong to a customer."
    )

    # Ticket Date    

    missing_ticket_dates = (
        df["ticket_date"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Ticket Dates",
        "Ticket Date",
        missing_ticket_dates,
        0,
        "PASS"
        if missing_ticket_dates == 0
        else "FAIL",
        "Ticket date is required for support trend analysis."
    )
   
    # Issue Type    

    missing_issue_types = (
        df["issue_type"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Issue Types",
        "Issue Type",
        missing_issue_types,
        0,
        "PASS"
        if missing_issue_types == 0
        else "FAIL",
        "Issue type is required for issue-category analysis."
    )
   
    # Resolution Time    

    missing_resolution_time = (
        df["resolution_time_hours"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Resolution Time",
        "Resolution Time",
        missing_resolution_time,
        0,
        "PASS"
        if missing_resolution_time == 0
        else "FAIL",
        "Resolution time is required for support performance analysis."
    )

    negative_resolution_time = (
        df["resolution_time_hours"] < 0
    ).sum()

    add_check(
        "Negative Resolution Time",
        "Resolution Time",
        negative_resolution_time,
        0,
        "PASS"
        if negative_resolution_time == 0
        else "FAIL",
        "Resolution time cannot be negative."
    )
 
    # Satisfaction Score    

    missing_satisfaction = (
        df["satisfaction_score"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Satisfaction Scores",
        "Satisfaction",
        missing_satisfaction,
        0,
        "PASS"
        if missing_satisfaction == 0
        else "FAIL",
        "Satisfaction score is required for support experience analysis."
    )

    invalid_satisfaction = (
        (
            df["satisfaction_score"] < 1
        )
        |
        (
            df["satisfaction_score"] > 5
        )
    ).sum()

    add_check(
        "Invalid Satisfaction Scores",
        "Satisfaction",
        invalid_satisfaction,
        0,
        "PASS"
        if invalid_satisfaction == 0
        else "FAIL",
        "Satisfaction scores should be between 1 and 5."
    )

    # Resolved    

    missing_resolved = (
        df["resolved"]
        .isna()
        .sum()
    )

    add_check(
        "Missing Resolved Values",
        "Resolution Status",
        missing_resolved,
        0,
        "PASS"
        if missing_resolved == 0
        else "FAIL",
        "Every support ticket should have a resolution status."
    )

    unexpected_resolved = sorted(
        set(
            df["resolved"]
            .dropna()
            .unique()
        )
        - {"Yes", "No"}
    )

    add_check(
        "Unexpected Resolved Values",
        "Resolution Status",
        len(unexpected_resolved),
        0,
        "PASS"
        if len(unexpected_resolved) == 0
        else "FAIL",
        (
            "Allowed values are Yes and No. "
            f"Unexpected values: {unexpected_resolved}"
        )
    )
  
    # Issue Types    

    expected_issue_types = {
        "Account",
        "Billing",
        "General",
        "Performance",
        "Technical",
    }

    unexpected_issue_types = sorted(
        set(
            df["issue_type"]
            .dropna()
            .unique()
        )
        - expected_issue_types
    )

    add_check(
        "Unexpected Issue Types",
        "Issue Type",
        len(unexpected_issue_types),
        0,
        "PASS"
        if len(unexpected_issue_types) == 0
        else "FAIL",
        (
            "Unexpected issue types detected: "
            f"{unexpected_issue_types}"
        )
    )

    return pd.DataFrame(checks)

# CUSTOMER-LEVEL SUPPORT TICKET AGGREGATION

def aggregate_support_tickets(df):
    """
    Convert ticket-level data into one row per customer
    with at least one support ticket.
    """

    print("\n")
    print("SUPPORT TICKET CUSTOMER-LEVEL AGGREGATION")
    print("\n")

    tickets = df.copy()
 
    # Resolution flags    

    tickets["is_resolved"] = (
        tickets["resolved"]
        == "Yes"
    ).astype(int)

    tickets["is_unresolved"] = (
        tickets["resolved"]
        == "No"
    ).astype(int)

    # Basic customer-level aggregation    

    summary = (
        tickets
        .groupby(
            "customer_id",
            dropna=False
        )
        .agg(
            total_ticket_count=(
                "ticket_id",
                "count"
            ),

            resolved_ticket_count=(
                "is_resolved",
                "sum"
            ),

            unresolved_ticket_count=(
                "is_unresolved",
                "sum"
            ),

            average_resolution_time_hours=(
                "resolution_time_hours",
                "mean"
            ),

            minimum_resolution_time_hours=(
                "resolution_time_hours",
                "min"
            ),

            maximum_resolution_time_hours=(
                "resolution_time_hours",
                "max"
            ),

            average_satisfaction_score=(
                "satisfaction_score",
                "mean"
            ),

            minimum_satisfaction_score=(
                "satisfaction_score",
                "min"
            ),

            maximum_satisfaction_score=(
                "satisfaction_score",
                "max"
            ),

            first_ticket_date=(
                "ticket_date",
                "min"
            ),

            last_ticket_date=(
                "ticket_date",
                "max"
            ),
        )
        .reset_index()
    )
    
    # Resolution rates

    summary["ticket_resolution_rate"] = np.where(
        summary["total_ticket_count"] > 0,

        (
            summary["resolved_ticket_count"]
            /
            summary["total_ticket_count"]
        ) * 100,

        np.nan
    )

    summary["ticket_unresolved_rate"] = np.where(
        summary["total_ticket_count"] > 0,

        (
            summary["unresolved_ticket_count"]
            /
            summary["total_ticket_count"]
        ) * 100,

        np.nan
    )

    # Issue Type Counts
    
    issue_counts = pd.crosstab(
        tickets["customer_id"],
        tickets["issue_type"]
    )

    issue_counts.columns = [
        f"{str(column).lower()}_ticket_count"
        for column in issue_counts.columns
    ]

    issue_counts = (
        issue_counts
        .reset_index()
    )

    summary = summary.merge(
        issue_counts,
        on="customer_id",
        how="left"
    )

    # Ensure expected issue columns exist
    
    expected_issue_columns = [
        "account_ticket_count",
        "billing_ticket_count",
        "general_ticket_count",
        "performance_ticket_count",
        "technical_ticket_count",
    ]

    for column in expected_issue_columns:

        if column not in summary.columns:

            summary[column] = 0

    # Number of unique issue types
    
    issue_type_count = (
        tickets
        .groupby("customer_id")["issue_type"]
        .nunique()
        .rename(
            "unique_issue_types"
        )
    )

    summary = summary.merge(
        issue_type_count,
        on="customer_id",
        how="left"
    )

    # Dataset observation date
    
    dataset_observation_date = (
        tickets["ticket_date"].max()
    )

    summary["dataset_observation_date"] = (
        dataset_observation_date
    )

    # Days since last ticket    

    summary["days_since_last_ticket"] = (
        dataset_observation_date
        - summary["last_ticket_date"]
    ).dt.days
    
    # Ticket period    

    ticket_period_days = (
        summary["last_ticket_date"]
        - summary["first_ticket_date"]
    ).dt.days

    # Tickets per month    

    summary["tickets_per_month"] = np.where(
        ticket_period_days > 0,

        summary["total_ticket_count"]
        /
        (
            ticket_period_days
            / 30.44
        ),

        summary["total_ticket_count"]
    )

    # Support activity flag    

    summary["has_support_ticket"] = 1

    # Median-based high support usage flag    

    ticket_count_median = (
        summary["total_ticket_count"]
        .median()
    )

    summary["high_support_usage"] = np.where(
        summary["total_ticket_count"]
        > ticket_count_median,
        1,
        0
    )
    
    # Unresolved ticket flag

    summary["has_unresolved_ticket"] = (
        summary["unresolved_ticket_count"]
        > 0
    ).astype(int)
  
    # Low satisfaction flag

    summary["has_low_satisfaction"] = np.where(
        summary["average_satisfaction_score"] < 3,
        1,
        0
    )

    # Round numerical values

    decimal_columns = [
        "average_resolution_time_hours",
        "minimum_resolution_time_hours",
        "maximum_resolution_time_hours",
        "average_satisfaction_score",
        "minimum_satisfaction_score",
        "maximum_satisfaction_score",
        "ticket_resolution_rate",
        "ticket_unresolved_rate",
        "tickets_per_month",
    ]

    for column in decimal_columns:

        if column in summary.columns:

            summary[column] = (
                summary[column]
                .round(2)
            )

    # Sort by Customer ID   

    summary = (
        summary
        .sort_values(
            "customer_id"
        )
        .reset_index(drop=True)
    )

    print(
        f"Customer-level support rows : "
        f"{len(summary):,}"
    )

    print(
        f"Unique customers with tickets: "
        f"{summary['customer_id'].nunique():,}"
    )

    print(
        f"Customers with unresolved tickets: "
        f"{(
            summary['has_unresolved_ticket']
            == 1
        ).sum():,}"
    )

    return (
        summary,
        dataset_observation_date
    )

# AGGREGATION VALIDATION CHECKS

def create_aggregation_checks(
    tickets,
    customer_support,
    dataset_observation_date
):
    """
    Validate customer-level aggregation against
    original ticket-level data.
    """

    checks = []

    def add_check(
        check_name,
        category,
        actual_value,
        expected,
        status,
        description
    ):
        checks.append(
            {
                "Check_Name": check_name,
                "Category": category,
                "Actual_Value": actual_value,
                "Expected": expected,
                "Status": status,
                "Description": description,
            }
        )
   
    # One row per customer   

    customer_rows = len(
        customer_support
    )

    unique_customer_rows = (
        customer_support[
            "customer_id"
        ].nunique()
    )

    add_check(
        "One Row Per Customer",
        "Grain",
        customer_rows,
        unique_customer_rows,
        "PASS"
        if customer_rows == unique_customer_rows
        else "FAIL",
        (
            "Customer-level support dataset "
            "must contain one row per customer "
            "with support activity."
        )
    )
   
    # Ticket count reconciliation  

    source_ticket_count = len(
        tickets
    )

    aggregated_ticket_count = (
        customer_support[
            "total_ticket_count"
        ].sum()
    )

    add_check(
        "Ticket Count Reconciliation",
        "Reconciliation",
        aggregated_ticket_count,
        source_ticket_count,
        "PASS"
        if aggregated_ticket_count
        == source_ticket_count
        else "FAIL",
        (
            "Sum of customer ticket counts "
            "must equal source ticket records."
        )
    )
 
    # Resolved ticket reconciliation

    source_resolved_count = (
        tickets["resolved"]
        .eq("Yes")
        .sum()
    )

    aggregated_resolved_count = (
        customer_support[
            "resolved_ticket_count"
        ].sum()
    )

    add_check(
        "Resolved Ticket Count Reconciliation",
        "Reconciliation",
        aggregated_resolved_count,
        source_resolved_count,
        "PASS"
        if aggregated_resolved_count
        == source_resolved_count
        else "FAIL",
        (
            "Resolved ticket counts "
            "must reconcile with source."
        )
    )
  
    # Unresolved ticket reconciliation

    source_unresolved_count = (
        tickets["resolved"]
        .eq("No")
        .sum()
    )

    aggregated_unresolved_count = (
        customer_support[
            "unresolved_ticket_count"
        ].sum()
    )

    add_check(
        "Unresolved Ticket Count Reconciliation",
        "Reconciliation",
        aggregated_unresolved_count,
        source_unresolved_count,
        "PASS"
        if aggregated_unresolved_count
        == source_unresolved_count
        else "FAIL",
        (
            "Unresolved ticket counts "
            "must reconcile with source."
        )
    )
 
    # Issue type reconciliation

    issue_types = [
        "Account",
        "Billing",
        "General",
        "Performance",
        "Technical",
    ]

    for issue_type in issue_types:

        source_count = (
            tickets["issue_type"]
            .eq(issue_type)
            .sum()
        )

        column_name = (
            f"{issue_type.lower()}_ticket_count"
        )

        aggregated_count = (
            customer_support[
                column_name
            ].sum()
        )

        add_check(
            f"{issue_type} Ticket Count Reconciliation",
            "Issue Type",
            aggregated_count,
            source_count,
            "PASS"
            if aggregated_count
            == source_count
            else "FAIL",
            (
                f"{issue_type} ticket count "
                "must reconcile with source."
            )
        )
   
    # Customer coverage    

    source_customers = (
        tickets["customer_id"]
        .nunique()
    )

    aggregated_customers = (
        customer_support[
            "customer_id"
        ].nunique()
    )

    add_check(
        "Customer Coverage",
        "Coverage",
        aggregated_customers,
        source_customers,
        "PASS"
        if aggregated_customers
        == source_customers
        else "FAIL",
        (
            "Every customer with a ticket "
            "must appear in the aggregation."
        )
    )
 
    # Missing Customer IDs   

    missing_customer_ids = (
        customer_support[
            "customer_id"
        ]
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
        (
            "Customer-level aggregation "
            "must not contain missing IDs."
        )
    )
  
    # Duplicate customers
    
    duplicate_customers = (
        customer_support[
            "customer_id"
        ]
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
        (
            "There must be one support summary "
            "row per customer."
        )
    )
 
    # Last ticket date reconciliation 

    max_source_date = (
        tickets["ticket_date"].max()
    )

    max_aggregation_date = (
        customer_support[
            "last_ticket_date"
        ].max()
    )

    add_check(
        "Last Ticket Date Reconciliation",
        "Reconciliation",
        max_aggregation_date,
        max_source_date,
        "PASS"
        if max_aggregation_date
        == max_source_date
        else "FAIL",
        (
            "Maximum customer last-ticket date "
            "must match source maximum ticket date."
        )
    )
       
    # Average satisfaction reconciliation   

    source_average_satisfaction = (
        tickets[
            "satisfaction_score"
        ].mean()
    )

    weighted_average_satisfaction = (
        (
            customer_support[
                "average_satisfaction_score"
            ]
            *
            customer_support[
                "total_ticket_count"
            ]
        ).sum()
        /
        customer_support[
            "total_ticket_count"
        ].sum()
    )

    satisfaction_difference = abs(
        weighted_average_satisfaction
        - source_average_satisfaction
    )

    add_check(
        "Average Satisfaction Reconciliation",
        "Reconciliation",
        round(
            weighted_average_satisfaction,
            4
        ),
        round(
            source_average_satisfaction,
            4
        ),
        "PASS"
        if satisfaction_difference <= 0.01
        else "FAIL",
        (
            "Weighted customer-level average "
            "satisfaction should reconcile with "
            "the source average within a small "
            "rounding tolerance."
        )
    )

    # Observation date

    add_check(
        "Dataset Observation Date",
        "Metadata",
        dataset_observation_date,
        dataset_observation_date,
        "INFO",
        (
            "Observation date is based on the "
            "maximum ticket date in the cleaned "
            "Support Tickets dataset."
        )
    )

    return pd.DataFrame(
        checks
    )

# SUPPORT AGGREGATION SUMMARY

def create_support_summary(
    tickets,
    customer_support,
    dataset_observation_date
):
    """
    Create overall support aggregation summary.
    """

    source_ticket_count = len(
        tickets
    )

    source_customer_count = (
        tickets["customer_id"]
        .nunique()
    )

    resolved_count = (
        tickets["resolved"]
        .eq("Yes")
        .sum()
    )

    unresolved_count = (
        tickets["resolved"]
        .eq("No")
        .sum()
    )

    average_resolution_time = (
        tickets[
            "resolution_time_hours"
        ].mean()
    )

    average_satisfaction = (
        tickets[
            "satisfaction_score"
        ].mean()
    )

    customers_with_unresolved = (
        customer_support[
            "has_unresolved_ticket"
        ]
        .eq(1)
        .sum()
    )

    resolution_rate = (
        resolved_count
        / source_ticket_count
        * 100
    )

    summary = pd.DataFrame(
        {
            "Metric": [
                "Source Support Ticket Rows",
                "Source Unique Customers",
                "Customer-Level Rows",
                "Customer-Level Unique Customers",
                "Resolved Ticket Count",
                "Unresolved Ticket Count",
                "Resolution Rate (%)",
                "Average Resolution Time (Hours)",
                "Average Satisfaction Score",
                "Customers With Unresolved Tickets",
                "Unique Issue Types",
                "Dataset Observation Date",
            ],

            "Value": [
                source_ticket_count,

                source_customer_count,

                len(customer_support),

                customer_support[
                    "customer_id"
                ].nunique(),

                resolved_count,

                unresolved_count,

                round(
                    resolution_rate,
                    2
                ),

                round(
                    average_resolution_time,
                    2
                ),

                round(
                    average_satisfaction,
                    2
                ),

                customers_with_unresolved,

                tickets[
                    "issue_type"
                ].nunique(),

                dataset_observation_date,
            ],
        }
    )

    return summary

# ISSUE TYPE SUMMARY

def create_issue_type_summary(tickets):
    """
    Create issue type distribution and
    performance summary.
    """

    issue_summary = (
        tickets["issue_type"]
        .value_counts()
        .rename_axis(
            "Issue_Type"
        )
        .reset_index(
            name="Ticket_Count"
        )
    )

    issue_summary["Percentage"] = (
        issue_summary[
            "Ticket_Count"
        ]
        / len(tickets)
        * 100
    ).round(2)

    # Issue-level performance
    
    issue_resolution = (
        tickets
        .groupby(
            "issue_type"
        )
        .agg(
            Resolved_Tickets=(
                "resolved",
                lambda x:
                    (x == "Yes").sum()
            ),

            Unresolved_Tickets=(
                "resolved",
                lambda x:
                    (x == "No").sum()
            ),

            Average_Resolution_Hours=(
                "resolution_time_hours",
                "mean"
            ),

            Average_Satisfaction=(
                "satisfaction_score",
                "mean"
            ),
        )
        .reset_index()
        .rename(
            columns={
                "issue_type": "Issue_Type"
            }
        )
    )

    issue_summary = issue_summary.merge(
        issue_resolution,
        on="Issue_Type",
        how="left"
    )

    # Resolution rate

    issue_summary[
        "Resolution_Rate"
    ] = (
        issue_summary[
            "Resolved_Tickets"
        ]
        /
        issue_summary[
            "Ticket_Count"
        ]
        * 100
    ).round(2)

    issue_summary[
        "Average_Resolution_Hours"
    ] = (
        issue_summary[
            "Average_Resolution_Hours"
        ].round(2)
    )

    issue_summary[
        "Average_Satisfaction"
    ] = (
        issue_summary[
            "Average_Satisfaction"
        ].round(2)
    )

    return issue_summary

# RESOLUTION STATUS SUMMARY

def create_resolution_summary(tickets):
    """
    Create resolution status distribution.
    """

    resolution_summary = (
        tickets["resolved"]
        .value_counts()
        .rename_axis(
            "Resolved"
        )
        .reset_index(
            name="Ticket_Count"
        )
    )

    resolution_summary["Percentage"] = (
        resolution_summary[
            "Ticket_Count"
        ]
        / len(tickets)
        * 100
    ).round(2)

    return resolution_summary

# SAVE OUTPUTS

def save_outputs(
    customer_support,
    support_summary,
    source_checks,
    aggregation_checks,
    issue_summary,
    resolution_summary
):
    """
    Save customer-level support dataset
    and aggregation report.
    """

    print("\n")
    print("SAVING SUPPORT TICKET AGGREGATION OUTPUTS")
    print("\n")
 
    # Customer-level dataset

    customer_support.to_excel(
        OUTPUT_FILE,
        index=False
    )

    # Aggregation report

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        support_summary.to_excel(
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

        issue_summary.to_excel(
            writer,
            sheet_name="Issue_Type",
            index=False
        )

        resolution_summary.to_excel(
            writer,
            sheet_name="Resolution_Status",
            index=False
        )

    print(
        "Customer-Level Dataset:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        "\nAggregation Report:"
    )

    print(
        REPORT_FILE
    )

# MAIN

def main():

    print("\n")
    print("SUPPORT TICKET CUSTOMER-LEVEL AGGREGATION")
    print("\n")

    # STEP 1 - LOAD  

    tickets = load_support_tickets()
    
    # STEP 2 - STANDARDIZE COLUMN NAMES
    
    tickets = standardize_columns(
        tickets
    )
   
    # STEP 3 - VALIDATE STRUCTURE
    
    validate_source_columns(
        tickets
    )
  
    # STEP 4 - STANDARDIZE DATA TYPES

    tickets = clean_basic_types(
        tickets
    )
   
    # STEP 5 - SOURCE VALIDATION
    
    source_checks = create_source_checks(
        tickets
    )

    source_failures = (
        source_checks[
            "Status"
        ]
        == "FAIL"
    ).sum()

    if source_failures > 0:

        print("\n")
        print("SOURCE VALIDATION FAILED")
        print("\n")

        print(
            source_checks.loc[
                source_checks["Status"]
                == "FAIL"
            ][
                [
                    "Check_Name",
                    "Actual_Value",
                    "Expected",
                    "Description",
                ]
            ].to_string(
                index=False
            )
        )

        raise ValueError(
            "Support Ticket aggregation stopped "
            "because source validation failed."
        )
  
    # STEP 6 - AGGREGATE

    (
        customer_support,
        dataset_observation_date
    ) = aggregate_support_tickets(
        tickets
    )

    # STEP 7 - AGGREGATION VALIDATION 

    aggregation_checks = (
        create_aggregation_checks(
            tickets,
            customer_support,
            dataset_observation_date
        )
    )
   
    # STEP 8 - CREATE REPORT SUMMARIES
    
    support_summary = (
        create_support_summary(
            tickets,
            customer_support,
            dataset_observation_date
        )
    )

    issue_summary = (
        create_issue_type_summary(
            tickets
        )
    )

    resolution_summary = (
        create_resolution_summary(
            tickets
        )
    )
 
    # STEP 9 - SAVE OUTPUTS
    
    save_outputs(
        customer_support,
        support_summary,
        source_checks,
        aggregation_checks,
        issue_summary,
        resolution_summary
    )
  
    # STEP 10 - COMBINE ALL CHECKS   

    all_checks = pd.concat(
        [
            source_checks,
            aggregation_checks
        ],
        ignore_index=True
    )

    total_checks = len(
        all_checks
    )

    passed_checks = (
        all_checks["Status"]
        == "PASS"
    ).sum()

    failed_checks = (
        all_checks["Status"]
        == "FAIL"
    ).sum()

    info_checks = (
        all_checks["Status"]
        == "INFO"
    ).sum()
   
    # STEP 11 - FINAL OUTPUT   

    print("\n")
    print("SUPPORT TICKET AGGREGATION COMPLETED")
    print("\n")

    print(
        f"Ticket-level rows             : "
        f"{len(tickets):,}"
    )

    print(
        f"Customer-level rows           : "
        f"{len(customer_support):,}"
    )

    print(
        f"Unique customers with tickets : "
        f"{customer_support['customer_id'].nunique():,}"
    )

    print(
        f"Resolved tickets              : "
        f"{(
            tickets['resolved']
            .eq('Yes')
            .sum()
        ):,}"
    )

    print(
        f"Unresolved tickets            : "
        f"{(
            tickets['resolved']
            .eq('No')
            .sum()
        ):,}"
    )

    print(
        f"Average resolution time       : "
        f"{tickets['resolution_time_hours'].mean():.2f} hours"
    )

    print(
        f"Average satisfaction           : "
        f"{tickets['satisfaction_score'].mean():.2f}"
    )

    print(
        f"Total Checks                  : "
        f"{total_checks}"
    )

    print(
        f"Passed Checks                 : "
        f"{passed_checks}"
    )

    print(
        f"Failed Checks                 : "
        f"{failed_checks}"
    )

    print(
        f"Info Checks                   : "
        f"{info_checks}"
    )

    print(
        f"\nOverall Support Ticket "
        f"Aggregation                  : "
        f"{'PASS' if failed_checks == 0 else 'FAIL'}"
    )


# RUN SCRIPT

if __name__ == "__main__":
    main()