"""
Customer Churn & Retention Analysis
====================================

Data Transformation / Feature Engineering

Source Files:
    customers_cleaned.xlsx
    subscriptions_cleaned.xlsx

Purpose:
    Combine Customers and Subscriptions data and create
    analytical features required for:

        - Exploratory Data Analysis
        - Churn Analysis
        - Retention Analysis
        - SQL Analysis
        - Power BI Dashboard

Output:
    customer_subscription_analytical.xlsx

Important:
    This script does NOT modify the cleaned source files.
    It creates a separate analytical dataset.
"""

from pathlib import Path
import pandas as pd
import numpy as np

######   PROJECT PATHS   ######  

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

######   CLEANED DATA PATHS   ######

CLEANED_FOLDER = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
)

CUSTOMERS_FILE = (
    CLEANED_FOLDER
    / "customers_cleaned.xlsx"
)

SUBSCRIPTIONS_FILE = (
    CLEANED_FOLDER
    / "subscriptions_cleaned.xlsx"
)

######   TRANSFORMED DATA OUTPUT PATH   ######

OUTPUT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "06_aggregated_data"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER
    / "customer_subscription_analytical.xlsx"
)

######   CONFIGURATION   ######

# Reference date used for calculating tenure for active customers.
#
# Using today's date makes the dataset current when the script
# is executed.
#
# You can change this to a fixed date later if you want
# completely reproducible historical analysis.

AS_OF_DATE = pd.Timestamp.today().normalize()

######   EXPECTED COLUMNS   ######

EXPECTED_CUSTOMER_COLUMNS = [
    "customer_id",
    "gender",
    "age",
    "city",
    "state",
    "signup_date",
]

EXPECTED_SUBSCRIPTION_COLUMNS = [
    "customer_id",
    "subscription_id",
    "plan",
    "contract_type",
    "start_date",
    "end_date",
    "monthly_charge",
    "churn_status",
    "churn_date",
]

######   LOAD CLEANED DATA   ######

def load_cleaned_data():
    """
    Load cleaned Customers and Subscriptions datasets.
    """

    print("STEP 1 - LOADING CLEANED DATA")
    print("\n")

    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customers file not found:\n{CUSTOMERS_FILE}"
        )

    if not SUBSCRIPTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Subscriptions file not found:\n"
            f"{SUBSCRIPTIONS_FILE}"
        )

    customers_df = pd.read_excel(
        CUSTOMERS_FILE
    )

    subscriptions_df = pd.read_excel(
        SUBSCRIPTIONS_FILE
    )

    print(
        f"Customers rows        : "
        f"{len(customers_df):,}"
    )

    print(
        f"Customers columns     : "
        f"{len(customers_df.columns)}"
    )

    print(
        f"Subscriptions rows    : "
        f"{len(subscriptions_df):,}"
    )

    print(
        f"Subscriptions columns : "
        f"{len(subscriptions_df.columns)}"
    )

    print()

    return customers_df, subscriptions_df


######   VALIDATE EXPECTED COLUMNS   ######

def validate_columns(
    customers_df,
    subscriptions_df
):
    """
    Verify that the cleaned files contain the expected
    columns before transformation begins.
    """

    print("STEP 2 - VALIDATING SOURCE COLUMNS")
    print("\n")

    missing_customer_columns = [
        column
        for column in EXPECTED_CUSTOMER_COLUMNS
        if column not in customers_df.columns
    ]

    missing_subscription_columns = [
        column
        for column in EXPECTED_SUBSCRIPTION_COLUMNS
        if column not in subscriptions_df.columns
    ]

    if missing_customer_columns:
        raise ValueError(
            "Missing Customers columns:\n"
            + "\n".join(missing_customer_columns)
        )

    if missing_subscription_columns:
        raise ValueError(
            "Missing Subscriptions columns:\n"
            + "\n".join(missing_subscription_columns)
        )

    print("Customers columns     : PASS")
    print("Subscriptions columns : PASS")
    print()


######   STANDARDIZE DATA TYPES   ######

def standardize_data_types(
    customers_df,
    subscriptions_df
):
    """
    Ensure dates and numeric fields have appropriate
    pandas data types.
    """

    print("STEP 3 - STANDARDIZING DATA TYPES")
    print("\n")

    ######   Customer fields

    customers_df["customer_id"] = (
        customers_df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    customers_df["gender"] = (
        customers_df["gender"]
        .astype("string")
        .str.strip()
    )

    customers_df["city"] = (
        customers_df["city"]
        .astype("string")
        .str.strip()
    )

    customers_df["state"] = (
        customers_df["state"]
        .astype("string")
        .str.strip()
    )

    customers_df["age"] = pd.to_numeric(
        customers_df["age"],
        errors="coerce"
    )

    customers_df["signup_date"] = pd.to_datetime(
        customers_df["signup_date"],
        errors="coerce"
    )

    ######   Subscription fields

    subscriptions_df["customer_id"] = (
        subscriptions_df["customer_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    subscriptions_df["subscription_id"] = (
        subscriptions_df["subscription_id"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    subscriptions_df["plan"] = (
        subscriptions_df["plan"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    subscriptions_df["contract_type"] = (
        subscriptions_df["contract_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    subscriptions_df["churn_status"] = (
        subscriptions_df["churn_status"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    subscriptions_df["monthly_charge"] = (
        pd.to_numeric(
            subscriptions_df["monthly_charge"],
            errors="coerce"
        )
    )

    subscriptions_df["start_date"] = pd.to_datetime(
        subscriptions_df["start_date"],
        errors="coerce"
    )

    subscriptions_df["end_date"] = pd.to_datetime(
        subscriptions_df["end_date"],
        errors="coerce"
    )

    subscriptions_df["churn_date"] = pd.to_datetime(
        subscriptions_df["churn_date"],
        errors="coerce"
    )

    print("Data types standardized successfully.")
    print()


######   MERGE CUSTOMERS + SUBSCRIPTIONS   ######

def merge_customer_subscription_data(
    customers_df,
    subscriptions_df
):
    """
    Merge Customers and Subscriptions using customer_id.

    Because cross-sheet referential integrity has already
    passed, an INNER JOIN should retain all 20,000 customers.

    Validation:
        Customers       = 20,000
        Subscriptions   = 20,000
        Matching IDs    = 20,000
    """

    print("=" * 80)
    print("STEP 4 - MERGING CUSTOMERS + SUBSCRIPTIONS")
    print("=" * 80)

    analytical_df = customers_df.merge(
        subscriptions_df,
        on="customer_id",
        how="inner",
        validate="one_to_one"
    )

    print(
        f"Customers rows before merge     : "
        f"{len(customers_df):,}"
    )

    print(
        f"Subscriptions rows before merge : "
        f"{len(subscriptions_df):,}"
    )

    print(
        f"Rows after merge                : "
        f"{len(analytical_df):,}"
    )

    print(
        f"Columns after merge             : "
        f"{len(analytical_df.columns)}"
    )

    ######   Merge validation

    if len(analytical_df) != len(customers_df):
        raise ValueError(
            "Unexpected row count after merge. "
            "Check referential integrity."
        )

    if analytical_df["customer_id"].isna().any():
        raise ValueError(
            "Missing customer_id found after merge."
        )

    print("Merge validation                : PASS")
    print()

    return analytical_df


######   CREATE CHURN FLAGS   ######

def create_churn_features(
    analytical_df
):
    """
    Create binary churn indicators.

    is_churned:
        1 = customer churned
        0 = customer active

    is_active:
        1 = customer active
        0 = customer churned
    """

    print("=" * 80)
    print("STEP 5 - CREATING CHURN FEATURES")
    print("=" * 80)

    analytical_df["is_churned"] = (
        analytical_df["churn_status"]
        .eq("Churned")
        .astype(int)
    )

    analytical_df["is_active"] = (
        analytical_df["churn_status"]
        .eq("Active")
        .astype(int)
    )

    ######   Churn date available flag

    analytical_df["has_churn_date"] = (
        analytical_df["churn_date"]
        .notna()
        .astype(int)
    )

    ######   End date available flag

    analytical_df["has_end_date"] = (
        analytical_df["end_date"]
        .notna()
        .astype(int)
    )

    print(
        f"Churned customers : "
        f"{analytical_df['is_churned'].sum():,}"
    )

    print(
        f"Active customers  : "
        f"{analytical_df['is_active'].sum():,}"
    )

    print("Churn features created.")
    print()

    return analytical_df

######   CREATE TENURE FEATURES   ######

def create_tenure_features(
    analytical_df
):
    """
    Calculate customer/subscription tenure.

    For churned customers:
        start_date → churn_date

    For active customers:
        start_date → AS_OF_DATE

    Features:
        tenure_days
        tenure_months
        tenure_years
    """

    print("=" * 80)
    print("STEP 6 - CREATING TENURE FEATURES")
    print("=" * 80)

    ######   Determine end point for tenure calculation

    analytical_df["tenure_end_date"] = (
        analytical_df["churn_date"]
        .fillna(
            analytical_df["end_date"]
        )
        .fillna(
            AS_OF_DATE
        )
    )

    ######   Calculate tenure in days

    analytical_df["tenure_days"] = (
        analytical_df["tenure_end_date"]
        - analytical_df["start_date"]
    ).dt.days

    ######   Prevent negative tenure

    analytical_df.loc[
        analytical_df["tenure_days"] < 0,
        "tenure_days"
    ] = np.nan

    ######   Calculate tenure in months

    analytical_df["tenure_months"] = (
        analytical_df["tenure_days"] / 30.44
    ).round(1)

    ######   Calculate tenure in years

    analytical_df["tenure_years"] = (
        analytical_df["tenure_days"] / 365.25
    ).round(2)

    print(
        f"Reference date : "
        f"{AS_OF_DATE.strftime('%Y-%m-%d')}"
    )

    print(
        "Tenure features created:"
    )

    print(
        "    tenure_end_date"
    )

    print(
        "    tenure_days"
    )

    print(
        "    tenure_months"
    )

    print(
        "    tenure_years"
    )

    print()

    return analytical_df


######   CREATE CUSTOMER AGE FEATURES   ######

def create_age_features(
    analytical_df
):
    """
    Create age-related analytical features.

    age_group categories:

        Under 25
        25-34
        35-44
        45-54
        55+
    """

    print("=" * 80)
    print("STEP 7 - CREATING AGE FEATURES")
    print("=" * 80)

    analytical_df["age_group"] = pd.cut(
        analytical_df["age"],
        bins=[
            -np.inf,
            24,
            34,
            44,
            54,
            np.inf
        ],
        labels=[
            "Under 25",
            "25-34",
            "35-44",
            "45-54",
            "55+"
        ]
    )

    analytical_df["age_group"] = (
        analytical_df["age_group"]
        .astype("string")
    )

    print(
        "Created age_group."
    )

    print()

    return analytical_df


######   CREATE SIGNUP FEATURES   ######

def create_signup_features(
    analytical_df
):
    """
    Create calendar features from signup_date.
    """

    print("=" * 80)
    print("STEP 8 - CREATING SIGNUP FEATURES")
    print("=" * 80)

    analytical_df["signup_year"] = (
        analytical_df["signup_date"]
        .dt.year
    )

    analytical_df["signup_month"] = (
        analytical_df["signup_date"]
        .dt.month
    )

    analytical_df["signup_month_name"] = (
        analytical_df["signup_date"]
        .dt.month_name()
    )

    analytical_df["signup_quarter"] = (
        analytical_df["signup_date"]
        .dt.quarter
    )

    analytical_df["signup_year_month"] = (
        analytical_df["signup_date"]
        .dt.to_period("M")
        .astype("string")
    )

    print(
        "Created:"
    )

    print(
        "    signup_year"
    )

    print(
        "    signup_month"
    )

    print(
        "    signup_month_name"
    )

    print(
        "    signup_quarter"
    )

    print(
        "    signup_year_month"
    )

    print()

    return analytical_df


######   CREATE SUBSCRIPTION DATE FEATURES   ######

def create_subscription_date_features(
    analytical_df
):
    """
    Create calendar features from subscription start,
    end and churn dates.
    """

    print("=" * 80)
    print("STEP 9 - CREATING SUBSCRIPTION DATE FEATURES")
    print("=" * 80)

    ######   Start date

    analytical_df["start_year"] = (
        analytical_df["start_date"]
        .dt.year
    )

    analytical_df["start_month"] = (
        analytical_df["start_date"]
        .dt.month
    )

    analytical_df["start_quarter"] = (
        analytical_df["start_date"]
        .dt.quarter
    )

    ######   Churn date

    analytical_df["churn_year"] = (
        analytical_df["churn_date"]
        .dt.year
    )

    analytical_df["churn_month"] = (
        analytical_df["churn_date"]
        .dt.month
    )

    analytical_df["churn_quarter"] = (
        analytical_df["churn_date"]
        .dt.quarter
    )

    print(
        "Subscription date features created."
    )

    print()

    return analytical_df


######   CREATE TENURE SEGMENTS

def create_tenure_segments(
    analytical_df
):
    """
    Group customers into meaningful tenure segments.

    Categories:

        0-3 Months
        4-6 Months
        7-12 Months
        13-24 Months
        25+ Months
    """

    print("=" * 80)
    print("STEP 10 - CREATING TENURE SEGMENTS")
    print("=" * 80)

    analytical_df["tenure_segment"] = pd.cut(
        analytical_df["tenure_months"],
        bins=[
            -np.inf,
            3,
            6,
            12,
            24,
            np.inf
        ],
        labels=[
            "0-3 Months",
            "4-6 Months",
            "7-12 Months",
            "13-24 Months",
            "25+ Months"
        ]
    )

    analytical_df["tenure_segment"] = (
        analytical_df["tenure_segment"]
        .astype("string")
    )

    print(
        "Created tenure_segment."
    )

    print()

    return analytical_df


######   CREATE MONTHLY CHARGE FEATURES   ######

def create_charge_features(
    analytical_df
):
    """
    Create monthly charge bands and estimated annual charge.

    annual_charge:
        monthly_charge × 12
    """

    print("=" * 80)
    print("STEP 11 - CREATING CHARGE FEATURES")
    print("=" * 80)

    ######   Estimated annual charge

    analytical_df["estimated_annual_charge"] = (
        analytical_df["monthly_charge"] * 12
    ).round(2)

    # Monthly charge bands
    #
    # These bands are based on the actual charge values
    # using quartiles rather than arbitrary business limits.

    charge_q1 = (
        analytical_df["monthly_charge"]
        .quantile(0.25)
    )

    charge_q2 = (
        analytical_df["monthly_charge"]
        .quantile(0.50)
    )

    charge_q3 = (
        analytical_df["monthly_charge"]
        .quantile(0.75)
    )

    analytical_df["monthly_charge_band"] = pd.cut(
        analytical_df["monthly_charge"],
        bins=[
            -np.inf,
            charge_q1,
            charge_q2,
            charge_q3,
            np.inf
        ],
        labels=[
            "Low",
            "Medium",
            "High",
            "Very High"
        ],
        duplicates="drop"
    )

    analytical_df["monthly_charge_band"] = (
        analytical_df["monthly_charge_band"]
        .astype("string")
    )

    print(
        f"Charge Q1 : {charge_q1:.2f}"
    )

    print(
        f"Charge Q2 : {charge_q2:.2f}"
    )

    print(
        f"Charge Q3 : {charge_q3:.2f}"
    )

    print(
        "Created estimated_annual_charge."
    )

    print(
        "Created monthly_charge_band."
    )

    print()

    return analytical_df


######   CREATE PLAN FEATURES   ######

def create_plan_features(
    analytical_df
):
    """
    Create plan-level analytical flags.
    """

    print("=" * 80)
    print("STEP 12 - CREATING PLAN FEATURES")
    print("=" * 80)

    analytical_df["is_basic_plan"] = (
        analytical_df["plan"]
        .eq("Basic")
        .astype(int)
    )

    analytical_df["is_standard_plan"] = (
        analytical_df["plan"]
        .eq("Standard")
        .astype(int)
    )

    analytical_df["is_premium_plan"] = (
        analytical_df["plan"]
        .eq("Premium")
        .astype(int)
    )

    print(
        "Created plan indicator variables."
    )

    print()

    return analytical_df


######   CREATE CONTRACT FEATURES   ######

def create_contract_features(
    analytical_df
):
    """
    Create contract-level analytical flags.
    """

    print("=" * 80)
    print("STEP 13 - CREATING CONTRACT FEATURES")
    print("=" * 80)

    analytical_df["is_monthly_contract"] = (
        analytical_df["contract_type"]
        .eq("Monthly")
        .astype(int)
    )

    analytical_df["is_one_year_contract"] = (
        analytical_df["contract_type"]
        .eq("One Year")
        .astype(int)
    )

    analytical_df["is_two_year_contract"] = (
        analytical_df["contract_type"]
        .eq("Two Year")
        .astype(int)
    )

    print(
        "Created contract indicator variables."
    )

    print()

    return analytical_df


######   CREATE REVENUE FEATURES   ######

def create_revenue_features(
    analytical_df
):
    """
    Create simple revenue-related analytical features.

    Estimated lifetime revenue:
        monthly_charge × tenure_months

    This is an estimate and should be clearly labelled as such.
    """

    print("=" * 80)
    print("STEP 14 - CREATING REVENUE FEATURES")
    print("=" * 80)

    analytical_df["estimated_lifetime_revenue"] = (
        analytical_df["monthly_charge"]
        * analytical_df["tenure_months"]
    ).round(2)

    print(
        "Created estimated_lifetime_revenue."
    )

    print()

    return analytical_df

 
######   CREATE CHURN TIMING FEATURES   ######

def create_churn_timing_features(
    analytical_df
):
    """
    Create features useful for understanding when customers
    churn.

    churn_tenure_segment identifies the tenure period in which
    a churn occurred.
    """

    print("=" * 80)
    print("STEP 15 - CREATING CHURN TIMING FEATURES")
    print("=" * 80)

    analytical_df["churn_tenure_months"] = np.where(
        analytical_df["is_churned"] == 1,
        analytical_df["tenure_months"],
        np.nan
    )

    analytical_df["churn_tenure_segment"] = pd.cut(
        analytical_df["churn_tenure_months"],
        bins=[
            -np.inf,
            3,
            6,
            12,
            24,
            np.inf
        ],
        labels=[
            "0-3 Months",
            "4-6 Months",
            "7-12 Months",
            "13-24 Months",
            "25+ Months"
        ]
    )

    analytical_df["churn_tenure_segment"] = (
        analytical_df["churn_tenure_segment"]
        .astype("string")
    )

    print(
        "Created churn_tenure_months."
    )

    print(
        "Created churn_tenure_segment."
    )

    print()

    return analytical_df


######   CREATE DATA QUALITY FLAGS   ######

def create_data_quality_flags(
    analytical_df
):
    """
    Create analytical data-quality flags.

    These flags should help us identify unusual records
    without deleting them.
    """

    print("=" * 80)
    print("STEP 16 - CREATING DATA QUALITY FLAGS")
    print("=" * 80)

    ######   Invalid date sequence

    analytical_df["invalid_date_sequence"] = (
        (
            analytical_df["end_date"].notna()
            &
            (
                analytical_df["end_date"]
                < analytical_df["start_date"]
            )
        )
        |
        (
            analytical_df["churn_date"].notna()
            &
            (
                analytical_df["churn_date"]
                < analytical_df["start_date"]
            )
        )
    ).astype(int)

    ######   Active customer with churn date

    analytical_df["active_with_churn_date"] = (
        (
            analytical_df["is_active"] == 1
        )
        &
        (
            analytical_df["churn_date"].notna()
        )
    ).astype(int)

    ######   Churned customer without churn date

    analytical_df["churned_without_churn_date"] = (
        (
            analytical_df["is_churned"] == 1
        )
        &
        (
            analytical_df["churn_date"].isna()
        )
    ).astype(int)

    ######   Negative monthly charge

    analytical_df["negative_monthly_charge"] = (
        analytical_df["monthly_charge"] < 0
    ).astype(int)

    ######   Overall quality flag

    analytical_df["has_data_quality_issue"] = (
        (
            analytical_df["invalid_date_sequence"] == 1
        )
        |
        (
            analytical_df["active_with_churn_date"] == 1
        )
        |
        (
            analytical_df["churned_without_churn_date"] == 1
        )
        |
        (
            analytical_df["negative_monthly_charge"] == 1
        )
    ).astype(int)

    issue_count = (
        analytical_df["has_data_quality_issue"]
        .sum()
    )

    print(
        f"Records with data-quality flags : "
        f"{issue_count:,}"
    )

    print()

    return analytical_df


######   REORDER COLUMNS   ######

def reorder_columns(
    analytical_df
):
    """
    Arrange columns into logical business sections.

    This makes the final Excel dataset easier to understand.
    """

    print("=" * 80)
    print("STEP 17 - ORGANIZING ANALYTICAL COLUMNS")
    print("=" * 80)

    preferred_columns = [
        # Customer Information
        "customer_id",
        "gender",
        "age",
        "age_group",
        "city",
        "state",
        "signup_date",
        "signup_year",
        "signup_month",
        "signup_month_name",
        "signup_quarter",
        "signup_year_month",

        # Subscription Information
        "subscription_id",
        "plan",
        "contract_type",
        "start_date",
        "end_date",
        "monthly_charge",
        "estimated_annual_charge",
        "monthly_charge_band",

        # Churn Information
        "churn_status",
        "is_churned",
        "is_active",
        "churn_date",
        "has_churn_date",
        "has_end_date",

        # Tenure Information
        "tenure_end_date",
        "tenure_days",
        "tenure_months",
        "tenure_years",
        "tenure_segment",
        "churn_tenure_months",
        "churn_tenure_segment",

        # Subscription Date Features
        "start_year",
        "start_month",
        "start_quarter",
        "churn_year",
        "churn_month",
        "churn_quarter",

        # Plan Features
        "is_basic_plan",
        "is_standard_plan",
        "is_premium_plan",

        # Contract Features
        "is_monthly_contract",
        "is_one_year_contract",
        "is_two_year_contract",

        # Revenue Features
        "estimated_lifetime_revenue",

        # Data Quality
        "invalid_date_sequence",
        "active_with_churn_date",
        "churned_without_churn_date",
        "negative_monthly_charge",
        "has_data_quality_issue",
    ]

    # Keep only columns that actually exist.
    ordered_columns = [
        column
        for column in preferred_columns
        if column in analytical_df.columns
    ]

    # Add any remaining columns that were not explicitly listed.
    remaining_columns = [
        column
        for column in analytical_df.columns
        if column not in ordered_columns
    ]

    analytical_df = analytical_df[
        ordered_columns + remaining_columns
    ]

    print(
        f"Final analytical columns : "
        f"{len(analytical_df.columns)}"
    )

    print()

    return analytical_df


######   FINAL TRANSFORMATION VALIDATION   ######

def validate_transformed_data(
    analytical_df
):
    """
    Perform final checks after transformation.
    """

    print("=" * 80)
    print("STEP 18 - FINAL TRANSFORMATION VALIDATION")
    print("=" * 80)

    ######   Row count

    print(
        f"Rows                     : "
        f"{len(analytical_df):,}"
    )

    print(
        f"Columns                  : "
        f"{len(analytical_df.columns)}"
    )

    ######   Customer IDs

    missing_customer_ids = (
        analytical_df["customer_id"]
        .isna()
        .sum()
    )

    duplicate_customer_ids = (
        analytical_df["customer_id"]
        .duplicated()
        .sum()
    )

    print(
        f"Missing customer IDs     : "
        f"{missing_customer_ids:,}"
    )

    print(
        f"Duplicate customer IDs   : "
        f"{duplicate_customer_ids:,}"
    )

    ######   Churn status   ######

    invalid_churn_status = (
        ~analytical_df["churn_status"]
        .isin(["Active", "Churned"])
    ).sum()

    print(
        f"Invalid churn statuses   : "
        f"{invalid_churn_status:,}"
    )

    ######   Churn flag consistency

    churn_flag_mismatch = (
        analytical_df["is_churned"]
        + analytical_df["is_active"]
    )

    invalid_churn_flags = (
        churn_flag_mismatch != 1
    ).sum()

    print(
        f"Invalid churn flags      : "
        f"{invalid_churn_flags:,}"
    )

    ######   Negative tenure

    negative_tenure = (
        analytical_df["tenure_days"] < 0
    ).sum()

    print(
        f"Negative tenure records  : "
        f"{negative_tenure:,}"
    )

    ######   Duplicate subscription IDs

    duplicate_subscription_ids = (
        analytical_df["subscription_id"]
        .duplicated()
        .sum()
    )

    print(
        f"Duplicate subscription IDs: "
        f"{duplicate_subscription_ids:,}"
    )

    ######   Overall status

    validation_passed = (
        missing_customer_ids == 0
        and duplicate_customer_ids == 0
        and invalid_churn_status == 0
        and invalid_churn_flags == 0
        and negative_tenure == 0
        and duplicate_subscription_ids == 0
    )

    print()

    print(
        "Transformation validation : "
        + (
            "PASS"
            if validation_passed
            else "CHECK REQUIRED"
        )
    )

    print()

    if not validation_passed:
        raise ValueError(
            "Final transformation validation failed. "
            "Review the output above before continuing."
        )


######   CREATE TRANSFORMATION SUMMARY   ######

def create_transformation_summary(
    analytical_df
):
    """
    Create a summary table for the transformation process.
    """

    summary = pd.DataFrame(
        [
            {
                "Metric": "Rows",
                "Value": len(analytical_df)
            },
            {
                "Metric": "Columns",
                "Value": len(analytical_df.columns)
            },
            {
                "Metric": "Unique Customers",
                "Value": analytical_df[
                    "customer_id"
                ].nunique()
            },
            {
                "Metric": "Unique Subscriptions",
                "Value": analytical_df[
                    "subscription_id"
                ].nunique()
            },
            {
                "Metric": "Active Customers",
                "Value": analytical_df[
                    "is_active"
                ].sum()
            },
            {
                "Metric": "Churned Customers",
                "Value": analytical_df[
                    "is_churned"
                ].sum()
            },
            {
                "Metric": "Average Age",
                "Value": round(
                    analytical_df[
                        "age"
                    ].mean(),
                    2
                )
            },
            {
                "Metric": "Average Monthly Charge",
                "Value": round(
                    analytical_df[
                        "monthly_charge"
                    ].mean(),
                    2
                )
            },
            {
                "Metric": "Average Tenure Months",
                "Value": round(
                    analytical_df[
                        "tenure_months"
                    ].mean(),
                    2
                )
            },
            {
                "Metric": "Data Quality Issue Records",
                "Value": analytical_df[
                    "has_data_quality_issue"
                ].sum()
            },
            {
                "Metric": "As Of Date",
                "Value": AS_OF_DATE.strftime(
                    "%Y-%m-%d"
                )
            },
        ]
    )

    return summary


######   SAVE ANALYTICAL DATASET   ######

def save_output(
    analytical_df,
    summary_df
):
    """
    Save analytical dataset and transformation summary
    to an Excel workbook.
    """

    print("=" * 80)
    print("STEP 19 - SAVING TRANSFORMED DATA")
    print("=" * 80)

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        analytical_df.to_excel(
            writer,
            sheet_name="Analytical_Data",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Transformation_Summary",
            index=False
        )

    print(
        f"Analytical dataset saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()


######   MAIN FUNCTION    ######

def main():

    print()
    print("=" * 80)
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("DATA TRANSFORMATION / FEATURE ENGINEERING")
    print("=" * 80)
    print()

    # Load cleaned datasets

    customers_df, subscriptions_df = (
        load_cleaned_data()
    )

    # Validate expected columns

    validate_columns(
        customers_df,
        subscriptions_df
    )

    # Standardize data types

    standardize_data_types(
        customers_df,
        subscriptions_df
    )

    # Merge Customers + Subscriptions

    analytical_df = (
        merge_customer_subscription_data(
            customers_df,
            subscriptions_df
        )
    )

    # Churn features

    analytical_df = create_churn_features(
        analytical_df
    )

    # Tenure features

    analytical_df = create_tenure_features(
        analytical_df
    )

    # Age features

    analytical_df = create_age_features(
        analytical_df
    )

    # Signup features

    analytical_df = create_signup_features(
        analytical_df
    )

    # Subscription date features

    analytical_df = create_subscription_date_features(
        analytical_df
    )

    # Tenure segments

    analytical_df = create_tenure_segments(
        analytical_df
    )

    # Charge features

    analytical_df = create_charge_features(
        analytical_df
    )

    # Plan features

    analytical_df = create_plan_features(
        analytical_df
    )

    # Contract features

    analytical_df = create_contract_features(
        analytical_df
    )

    # Revenue features

    analytical_df = create_revenue_features(
        analytical_df
    )

    # Churn timing features

    analytical_df = create_churn_timing_features(
        analytical_df
    )

    # Data quality flags

    analytical_df = create_data_quality_flags(
        analytical_df
    )

    # Organize columns

    analytical_df = reorder_columns(
        analytical_df
    )

    # Final validation

    validate_transformed_data(
        analytical_df
    )

    # Transformation summary

    summary_df = (
        create_transformation_summary(
            analytical_df
        )
    )

    # Save output

    save_output(
        analytical_df,
        summary_df
    )

    # Final message

    print("=" * 80)
    print("DATA TRANSFORMATION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()

    print(
        f"Final rows    : "
        f"{len(analytical_df):,}"
    )

    print(
        f"Final columns : "
        f"{len(analytical_df.columns)}"
    )

    print(
        f"Output file   : "
        f"{OUTPUT_FILE}"
    )

    print()
    print("=" * 80)


######   PROGRAM ENTRY POINT   ######

if __name__ == "__main__":
    main()