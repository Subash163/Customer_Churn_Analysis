"""
Customer Churn & Retention Analysis
Feature Engineering

Purpose
-------
Transform the validated final customer analytical dataset
into a business-ready feature dataset for EDA, churn analysis,
customer segmentation, SQL analysis, and Power BI.

Analytical Grain
----------------
1 row = 1 customer

Input
-----
outputs/final_data/final_customer_analytical_dataset.xlsx

Output
------
outputs/feature_engineering/customer_analytical_features.xlsx
outputs/feature_engineering/feature_engineering_report.xlsx
outputs/feature_engineering/final_dataset_column_inventory.xlsx
"""

from pathlib import Path
import numpy as np
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "03_Final"
    / "final_customer_analytical_dataset.xlsx"
)

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "03_feature_engineering"
)

FEATURE_OUTPUT_FILE = (
    OUTPUT_DIR
    / "customer_analytical_features.xlsx"
)

REPORT_OUTPUT_FILE = (
    OUTPUT_DIR
    / "feature_engineering_report.xlsx"
)

COLUMN_INVENTORY_FILE = (
    OUTPUT_DIR
    / "final_dataset_column_inventory.xlsx"
)

######   UTILITY FUNCTIONS   ######

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


def add_check(checks, check_name, category, actual_value,
              expected_value, status, description):
    """
    Add a validation / feature engineering check.
    """

    checks.append(
        {
            "Check_Name": check_name,
            "Category": category,
            "Actual_Value": actual_value,
            "Expected_Value": expected_value,
            "Status": status,
            "Description": description,
        }
    )


def safe_divide(numerator, denominator):
    """
    Safely divide two pandas Series.

    Returns NaN where denominator is zero or missing.
    """

    denominator = denominator.replace(0, np.nan)

    return numerator / denominator


def classify_monthly_charge(series):
    """
    Create a business-friendly monthly charge segmentation
    using quartiles.

    The thresholds are calculated from the actual dataset.
    """

    q1 = series.quantile(0.25)
    q2 = series.quantile(0.50)
    q3 = series.quantile(0.75)

    def classify(value):

        if pd.isna(value):
            return np.nan

        if value <= q1:
            return "Low"

        if value <= q2:
            return "Medium-Low"

        if value <= q3:
            return "Medium-High"

        return "High"

    return series.apply(classify)


######   LOAD DATA   ######

def load_final_dataset():

    print("CUSTOMER CHURN & RETENTION")
    print("FEATURE ENGINEERING")
    print("\n")

    print("\nLoading final customer analytical dataset...")

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"\nInput file not found:\n{INPUT_FILE}\n\n"
            "Run the final customer dataset construction first."
        )

    df = pd.read_excel(INPUT_FILE)

    df = standardize_columns(df)

    print(f"Rows loaded    : {len(df):,}")
    print(f"Columns loaded : {len(df.columns):,}")

    return df


######   INSPECT AND CATEGORIZE 86 COLUMNS   ######

def create_column_inventory(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("FINAL DATASET COLUMN INVENTORY")
    print("\n")

    column_groups = {

        "Customer": [
            "customer_id",
            "gender",
            "age",
            "city",
            "state",
            "signup_date",
        ],

        "Subscription": [
            "subscription_id",
            "plan",
            "contract_type",
            "start_date",
            "end_date",
            "monthly_charge",
        ],

        "Churn": [
            "churn_status",
            "churn_date",
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
        ],

        "Customer Services": [
            "mobile_app",
            "streaming",
            "cloud_storage",
            "premium_support",
            "family_plan",
        ],

        "Payments": [
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
        ],

        "Support Tickets": [
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
        ],
    }

    inventory = []

    assigned_columns = set()

    for category, columns in column_groups.items():

        for column in columns:

            if column in df.columns:

                inventory.append(
                    {
                        "Column": column,
                        "Category": category,
                        "Data_Type": str(df[column].dtype),
                        "Missing_Count": int(df[column].isna().sum()),
                        "Unique_Count": int(df[column].nunique(dropna=True)),
                        "Used_For_Feature_Engineering": "Yes",
                    }
                )

                assigned_columns.add(column)

    # Identify columns that exist in the actual final dataset
    # but were not included in the predefined analytical groups.

    for column in df.columns:

        if column not in assigned_columns:

            inventory.append(
                {
                    "Column": column,
                    "Category": "Other / Review",
                    "Data_Type": str(df[column].dtype),
                    "Missing_Count": int(df[column].isna().sum()),
                    "Unique_Count": int(df[column].nunique(dropna=True)),
                    "Used_For_Feature_Engineering": "Review",
                }
            )

    inventory_df = pd.DataFrame(inventory)

    inventory_df.to_excel(
        COLUMN_INVENTORY_FILE,
        index=False,
    )

    print(
        f"\nColumn inventory saved:\n"
        f"{COLUMN_INVENTORY_FILE}"
    )

    print("\nColumn categories:")

    category_summary = (
        inventory_df["Category"]
        .value_counts()
        .sort_index()
    )

    for category, count in category_summary.items():

        print(f"{category:<25}: {count}")

    print(
        f"\nActual columns inspected : {len(df.columns):,}"
    )

    print(
        f"Columns categorized       : "
        f"{len(inventory_df):,}"
    )

    return inventory_df


######   PREPARE DATA TYPES   ######

def prepare_data_types(df):

    date_columns = [
        "signup_date",
        "start_date",
        "end_date",
        "churn_date",
        "first_payment_date",
        "last_payment_date",
        "first_ticket_date",
        "last_ticket_date",
        "observation_date",
        "dataset_observation_date",
    ]

    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    numeric_columns = [
        "age",
        "monthly_charge",
        "tenure_days",
        "tenure_months",
        "tenure_years",
        "tenure_days_at_churn",
        "tenure_months_at_churn",
        "tenure_years_at_churn",
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

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df


######   CUSTOMER FEATURE ENGINEERING   ######

def create_customer_features(df):

    print("\nCreating customer features...")

    ######   Age Group

    if "age" in df.columns:

        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 24, 34, 44, 54, 64, np.inf],
            labels=[
                "18-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65+",
            ],
            include_lowest=True,
        )

    ######   Signup Date Features

    if "signup_date" in df.columns:

        df["signup_year"] = df["signup_date"].dt.year

        df["signup_month"] = df["signup_date"].dt.month

        df["signup_month_name"] = (
            df["signup_date"]
            .dt.month_name()
        )

        df["signup_quarter"] = (
            "Q"
            + df["signup_date"]
            .dt.quarter
            .astype("Int64")
            .astype(str)
        )

        df["signup_year_month"] = (
            df["signup_date"]
            .dt.to_period("M")
            .astype(str)
        )

    return df


######   SUBSCRIPTION FEATURE ENGINEERING   ######

def create_subscription_features(df):

    print("Creating subscription features...")

    ######   Annual Subscription Value

    if "monthly_charge" in df.columns:

        df["annual_subscription_value"] = (
            df["monthly_charge"] * 12
        )

        df["monthly_charge_band"] = (
            classify_monthly_charge(
                df["monthly_charge"]
            )
        )

    ######   Plan Category

    if "plan" in df.columns:

        df["plan_category"] = (
            df["plan"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    ######   Contract Category

    if "contract_type" in df.columns:

        df["contract_category"] = (
            df["contract_type"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    return df


######   CHURN FEATURE ENGINEERING   ######

def create_churn_features(df):

    print("Creating churn features...")

    ######   Binary Churn Target

    if "churn_status" in df.columns:

        df["churn_target"] = (
            df["churn_status"]
            .astype("string")
            .str.strip()
            .str.lower()
            .eq("churned")
            .astype("Int64")
        )

    elif "is_churned" in df.columns:

        df["churn_target"] = (
            pd.to_numeric(
                df["is_churned"],
                errors="coerce",
            )
            .astype("Int64")
        )

    ######   Churn Date Features

    if "churn_date" in df.columns:

        df["churn_year_engineered"] = (
            df["churn_date"].dt.year
        )

        df["churn_month_engineered"] = (
            df["churn_date"].dt.month
        )

        df["churn_month_name_engineered"] = (
            df["churn_date"].dt.month_name()
        )

        df["churn_quarter_engineered"] = (
            "Q"
            + df["churn_date"]
            .dt.quarter
            .astype("Int64")
            .astype(str)
        )

        df["churn_year_month_engineered"] = (
            df["churn_date"]
            .dt.to_period("M")
            .astype(str)
        )

    ######   Tenure at Churn

    if "tenure_months_at_churn" in df.columns:

        df["tenure_at_churn_months"] = (
            df["tenure_months_at_churn"]
        )

    elif {
        "start_date",
        "churn_date",
    }.issubset(df.columns):

        df["tenure_at_churn_months"] = (
            (
                df["churn_date"]
                - df["start_date"]
            ).dt.days / 30.4375
        )

    if "tenure_at_churn_months" in df.columns:

        df["tenure_at_churn_years"] = (
            df["tenure_at_churn_months"] / 12
        )

    #######   Tenure Segment

    tenure_source = None

    if "tenure_months" in df.columns:

        tenure_source = df["tenure_months"]

    elif "tenure_at_churn_months" in df.columns:

        tenure_source = df["tenure_at_churn_months"]

    if tenure_source is not None:

        def tenure_segment(value):

            if pd.isna(value):
                return np.nan

            if value < 6:
                return "0-6 Months"

            if value < 12:
                return "6-12 Months"

            if value < 24:
                return "1-2 Years"

            if value < 36:
                return "2-3 Years"

            return "3+ Years"

        df["tenure_segment_engineered"] = (
            tenure_source.apply(tenure_segment)
        )

    return df

######   PAYMENT FEATURE ENGINEERING   ######

def create_payment_features(df):

    print("Creating payment features...")

    ######   Payment Failure Flag

    if "failed_payment_count" in df.columns:

        df["payment_failure_flag"] = (
            df["failed_payment_count"]
            .fillna(0)
            .gt(0)
            .astype(int)
        )

    elif "has_failed_payment" in df.columns:

        df["payment_failure_flag"] = (
            pd.to_numeric(
                df["has_failed_payment"],
                errors="coerce",
            )
            .fillna(0)
            .gt(0)
            .astype(int)
        )

    ######   Payment Activity Segment

    if "total_payment_count" in df.columns:

        def payment_activity(value):

            if pd.isna(value):
                return np.nan

            if value == 0:
                return "No Payment Activity"

            if value <= 6:
                return "Low"

            if value <= 18:
                return "Medium"

            return "High"

        df["payment_activity_segment"] = (
            df["total_payment_count"]
            .apply(payment_activity)
        )

    ######   Payment Value Segment

    if "total_payment_amount" in df.columns:

        total_amount = df["total_payment_amount"]

        q1 = total_amount.quantile(0.25)
        q2 = total_amount.quantile(0.50)
        q3 = total_amount.quantile(0.75)

        def payment_value(value):

            if pd.isna(value):
                return np.nan

            if value <= q1:
                return "Low"

            if value <= q2:
                return "Medium-Low"

            if value <= q3:
                return "Medium-High"

            return "High"

        df["payment_value_segment"] = (
            total_amount.apply(payment_value)
        )

    return df


######   CUSTOMER SERVICE FEATURE ENGINEERING   ######

def create_service_features(df):

    print("Creating customer service features...")

    service_columns = [
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
    ]

    available_services = [
        column
        for column in service_columns
        if column in df.columns
    ]

    if available_services:

        service_binary = pd.DataFrame(index=df.index)

        for column in available_services:

            service_binary[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .str.lower()
                .map(
                    {
                        "yes": 1,
                        "no": 0,
                    }
                )
            )

        # Count only confirmed Yes values.
        df["service_count"] = (
            service_binary.sum(axis=1, min_count=1)
        )

        # Denominator = services with known Yes/No status.
        known_service_count = (
            service_binary.notna().sum(axis=1)
        )

        df["service_adoption_rate"] = safe_divide(
            df["service_count"],
            known_service_count,
        )

        def service_segment(value):

            if pd.isna(value):
                return np.nan

            if value == 0:
                return "No Services"

            if value <= 0.40:
                return "Low Adoption"

            if value <= 0.75:
                return "Medium Adoption"

            return "High Adoption"

        df["service_adoption_segment"] = (
            df["service_adoption_rate"]
            .apply(service_segment)
        )

    return df


######   SUPPORT FEATURE ENGINEERING   ######

def create_support_features(df):

    print("Creating support features...")

    ######   Support Usage Segment

    if "total_ticket_count" in df.columns:

        def support_usage(value):

            if pd.isna(value) or value == 0:
                return "No Support Usage"

            if value <= 2:
                return "Low"

            if value <= 5:
                return "Medium"

            return "High"

        df["support_usage_segment"] = (
            df["total_ticket_count"]
            .apply(support_usage)
        )

    ######   Support Experience Segment

    if "average_satisfaction_score" in df.columns:

        def support_experience(value):

            if pd.isna(value):
                return "No Support Interaction"

            if value < 3:
                return "Poor"

            if value < 4:
                return "Average"

            if value < 4.5:
                return "Good"

            return "Excellent"

        df["support_experience_segment"] = (
            df["average_satisfaction_score"]
            .apply(support_experience)
        )

    # Support Risk Flag
    #
    # Descriptive flag only.
    # This is NOT a predictive churn model.

    risk_conditions = []

    if "has_unresolved_ticket" in df.columns:

        unresolved = (
            pd.to_numeric(
                df["has_unresolved_ticket"],
                errors="coerce",
            )
            .fillna(0)
            .gt(0)
        )

        risk_conditions.append(unresolved)

    if "has_low_satisfaction" in df.columns:

        low_satisfaction = (
            pd.to_numeric(
                df["has_low_satisfaction"],
                errors="coerce",
            )
            .fillna(0)
            .gt(0)
        )

        risk_conditions.append(low_satisfaction)

    if risk_conditions:

        combined_risk = risk_conditions[0]

        for condition in risk_conditions[1:]:

            combined_risk = (
                combined_risk | condition
            )

        df["support_risk_flag"] = (
            combined_risk.astype(int)
        )

    return df


######   CUSTOMER ENGAGEMENT   ######

def create_engagement_features(df):

    print("Creating customer engagement features...")

    engagement_score = pd.Series(
        0,
        index=df.index,
        dtype="int64",
    )

    components = 0

    # Successful payment activity
    if "has_successful_payment" in df.columns:

        engagement_score += (
            pd.to_numeric(
                df["has_successful_payment"],
                errors="coerce",
            )
            .fillna(0)
            .gt(0)
            .astype(int)
        )

        components += 1

    # Service adoption
    if "service_count" in df.columns:

        engagement_score += (
            df["service_count"]
            .fillna(0)
            .gt(0)
            .astype(int)
        )

        components += 1

    # Support interaction
    if "has_support_ticket" in df.columns:

        engagement_score += (
            pd.to_numeric(
                df["has_support_ticket"],
                errors="coerce",
            )
            .fillna(0)
            .gt(0)
            .astype(int)
        )

        components += 1

    if components > 0:

        df["customer_engagement_score"] = (
            engagement_score
        )

        def engagement_level(value):

            if value == 0:
                return "Low"

            if value == 1:
                return "Moderate"

            if value == 2:
                return "Engaged"

            return "Highly Engaged"

        df["customer_engagement_level"] = (
            df["customer_engagement_score"]
            .apply(engagement_level)
        )

    return df


######   BUSINESS FLAGS   ######

def create_business_flags(df):

    print("Creating business analytical flags...")

    ######   High Value Customer

    if "monthly_charge" in df.columns:

        median_charge = (
            df["monthly_charge"]
            .median()
        )

        df["high_value_customer"] = (
            df["monthly_charge"]
            .ge(median_charge)
            .astype(int)
        )

    ######   Low Payment Success

    if "payment_success_rate" in df.columns:

        df["low_payment_success_flag"] = (
            df["payment_success_rate"]
            .lt(0.90)
            .fillna(False)
            .astype(int)
        )

    ######   Customer Support Experience Risk

    if "average_satisfaction_score" in df.columns:

        df["support_experience_risk"] = (
            df["average_satisfaction_score"]
            .lt(3)
            .fillna(False)
            .astype(int)
        )

    return df


######   FEATURE ENGINEERING VALIDATION   ######

def validate_feature_engineering(
    original_df,
    feature_df,
):

    print("FEATURE ENGINEERING VALIDATION")
    

    checks = []

    ######   Row Count

    add_check(
        checks,
        "Row Count Preserved",
        "Structure",
        len(feature_df),
        len(original_df),
        "PASS"
        if len(feature_df) == len(original_df)
        else "FAIL",
        "Feature engineering must not change analytical grain.",
    )

    ######   Customer ID

    if "customer_id" in feature_df.columns:

        missing_customer_ids = (
            feature_df["customer_id"]
            .isna()
            .sum()
        )

        duplicate_customer_ids = (
            feature_df["customer_id"]
            .duplicated()
            .sum()
        )

        add_check(
            checks,
            "Missing Customer IDs",
            "Key Integrity",
            int(missing_customer_ids),
            0,
            "PASS"
            if missing_customer_ids == 0
            else "FAIL",
            "Every analytical row must have a customer ID.",
        )

        add_check(
            checks,
            "Duplicate Customer IDs",
            "Key Integrity",
            int(duplicate_customer_ids),
            0,
            "PASS"
            if duplicate_customer_ids == 0
            else "FAIL",
            "Analytical grain must remain one row per customer.",
        )

    ######   Churn Target

    if "churn_target" in feature_df.columns:

        target_values = set(
            feature_df["churn_target"]
            .dropna()
            .astype(int)
            .unique()
        )

        invalid_target_values = (
            target_values - {0, 1}
        )

        add_check(
            checks,
            "Churn Target Values",
            "Churn Target",
            sorted(target_values),
            [0, 1],
            "PASS"
            if not invalid_target_values
            else "FAIL",
            "Churn target must contain only 0 and 1.",
        )

        churn_count = int(
            feature_df["churn_target"]
            .sum()
        )

        add_check(
            checks,
            "Churn Target Count",
            "Churn Target",
            churn_count,
            "4,463",
            "INFO",
            "Expected churn count based on validated source data.",
        )

    ######   Annual Subscription Value

    if {
        "monthly_charge",
        "annual_subscription_value",
    }.issubset(feature_df.columns):

        expected_annual = (
            feature_df["monthly_charge"] * 12
        )

        differences = (
            feature_df["annual_subscription_value"]
            - expected_annual
        ).abs()

        max_difference = (
            differences.max()
            if len(differences)
            else 0
        )

        add_check(
            checks,
            "Annual Subscription Value Calculation",
            "Calculation",
            round(float(max_difference), 6),
            0,
            "PASS"
            if max_difference <= 0.000001
            else "FAIL",
            "Annual value must equal monthly charge multiplied by 12.",
        )

    ######   Payment Failure Flag

    if {
        "failed_payment_count",
        "payment_failure_flag",
    }.issubset(feature_df.columns):

        expected_flag = (
            feature_df["failed_payment_count"]
            .fillna(0)
            .gt(0)
            .astype(int)
        )

        mismatches = (
            feature_df["payment_failure_flag"]
            != expected_flag
        ).sum()

        add_check(
            checks,
            "Payment Failure Flag",
            "Calculation",
            int(mismatches),
            0,
            "PASS"
            if mismatches == 0
            else "FAIL",
            "Payment failure flag must reflect failed payment count.",
        )

    ######   Support Risk Flag

    if "support_risk_flag" in feature_df.columns:

        invalid_support_flags = (
            ~feature_df["support_risk_flag"]
            .isin([0, 1])
        ).sum()

        add_check(
            checks,
            "Support Risk Flag Values",
            "Business Flag",
            int(invalid_support_flags),
            0,
            "PASS"
            if invalid_support_flags == 0
            else "FAIL",
            "Support risk flag must contain only 0 or 1.",
        )

    ######   No Support Customers

    if {
        "total_ticket_count",
        "average_satisfaction_score",
    }.issubset(feature_df.columns):

        no_support = (
            feature_df["total_ticket_count"]
            .fillna(0)
            .eq(0)
        )

        satisfaction_for_no_support = (
            feature_df.loc[
                no_support,
                "average_satisfaction_score"
            ]
            .notna()
            .sum()
        )

        add_check(
            checks,
            "No-Support Customers Satisfaction",
            "Missingness",
            int(satisfaction_for_no_support),
            0,
            "PASS"
            if satisfaction_for_no_support == 0
            else "FAIL",
            "Customers without support interactions should not have "
            "support satisfaction values.",
        )

    ######   Feature Count

    new_columns = [
        column
        for column in feature_df.columns
        if column not in original_df.columns
    ]

    add_check(
        checks,
        "New Feature Count",
        "Feature Engineering",
        len(new_columns),
        "> 0",
        "PASS"
        if len(new_columns) > 0
        else "FAIL",
        "Feature engineering should create new analytical columns.",
    )

    ######   Infinite Values

    numeric_df = feature_df.select_dtypes(
        include=np.number
    )

    numeric_array = numeric_df.to_numpy(
        dtype="float64"
    )

    infinite_values = int(
        np.isinf(numeric_array).sum()
    )

    add_check(
        checks,
        "Infinite numeric values",
        "Data Quality",
        infinite_values,
        0,
        "PASS" if infinite_values == 0 else "FAIL",
        f"Number of infinite numeric values: {infinite_values}",
    )

    add_check(
        checks,
        "Infinite Numeric Values",
        "Data Quality",
        infinite_values,
        0,
        "PASS"
        if infinite_values == 0
        else "FAIL",
        "Feature engineering should not create infinite numeric values.",
    )

    ######   Result

    validation_df = pd.DataFrame(checks)

    passed = int(
        (validation_df["Status"] == "PASS").sum()
    )

    failed = int(
        (validation_df["Status"] == "FAIL").sum()
    )

    info = int(
        (validation_df["Status"] == "INFO").sum()
    )

    print(f"\nTotal Checks  : {len(validation_df)}")
    print(f"Passed Checks : {passed}")
    print(f"Failed Checks : {failed}")
    print(f"Info Checks   : {info}")

    if failed == 0:

        overall_status = "PASS"

    else:

        overall_status = "FAIL"

    print(
        f"\nOverall Feature Engineering : "
        f"{overall_status}"
    )

    return validation_df, overall_status


######   SAVE OUTPUTS   ######

def save_outputs(
    original_df,
    feature_df,
    inventory_df,
    validation_df,
    overall_status,
):

    print("SAVING FEATURE ENGINEERING OUTPUTS")
    print("\n")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    ######   Feature Dataset

    feature_df.to_excel(
        FEATURE_OUTPUT_FILE,
        index=False,
    )

    ######   Report Summary

    new_columns = [
        column
        for column in feature_df.columns
        if column not in original_df.columns
    ]

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Original Rows",
                "Original Columns",
                "Final Rows",
                "Final Columns",
                "New Features Created",
                "Original Missing Values",
                "Final Missing Values",
                "Overall Feature Engineering Status",
            ],
            "Value": [
                len(original_df),
                len(original_df.columns),
                len(feature_df),
                len(feature_df.columns),
                len(new_columns),
                int(original_df.isna().sum().sum()),
                int(feature_df.isna().sum().sum()),
                overall_status,
            ],
        }
    )

    ######   New Feature Inventory

    feature_inventory_df = pd.DataFrame(
        {
            "New_Feature": new_columns,
            "Data_Type": [
                str(feature_df[column].dtype)
                for column in new_columns
            ],
            "Missing_Count": [
                int(feature_df[column].isna().sum())
                for column in new_columns
            ],
            "Unique_Count": [
                int(feature_df[column].nunique(dropna=True))
                for column in new_columns
            ],
        }
    )

    ######   Save Excel Report

    with pd.ExcelWriter(
        REPORT_OUTPUT_FILE,
        engine="openpyxl",
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

        validation_df.to_excel(
            writer,
            sheet_name="Validation_Checks",
            index=False,
        )

        feature_inventory_df.to_excel(
            writer,
            sheet_name="New_Features",
            index=False,
        )

        inventory_df.to_excel(
            writer,
            sheet_name="Column_Inventory",
            index=False,
        )

    print(
        f"\nFeature Dataset:\n"
        f"{FEATURE_OUTPUT_FILE}"
    )

    print(
        f"\nFeature Engineering Report:\n"
        f"{REPORT_OUTPUT_FILE}"
    )

    print(
        f"\nColumn Inventory:\n"
        f"{COLUMN_INVENTORY_FILE}"
    )


######   MAIN PIPELINE   ######

def main():

    ######   1. Load

    original_df = load_final_dataset()

    # Keep an untouched copy for comparison.
    df = original_df.copy()

    ######   2. Inspect 86 columns

    inventory_df = create_column_inventory(df)

    ######   3. Prepare data types

    df = prepare_data_types(df)

    ######   4. Feature Engineering

    df = create_customer_features(df)

    df = create_subscription_features(df)

    df = create_churn_features(df)

    df = create_payment_features(df)

    df = create_service_features(df)

    df = create_support_features(df)

    df = create_engagement_features(df)

    df = create_business_flags(df)

    # 5. Validation

    validation_df, overall_status = (
        validate_feature_engineering(
            original_df,
            df,
        )
    )

    # 6. Save
    # 

    save_outputs(
        original_df,
        df,
        inventory_df,
        validation_df,
        overall_status,
    )
 
    ######   7. Final Console Summary

    new_columns = [
        column
        for column in df.columns
        if column not in original_df.columns
    ]

    print("\n")
    print("FEATURE ENGINEERING COMPLETED")
    print("\n")

    print(
        f"Original rows          : "
        f"{len(original_df):,}"
    )

    print(
        f"Final rows             : "
        f"{len(df):,}"
    )

    print(
        f"Original columns       : "
        f"{len(original_df.columns):,}"
    )

    print(
        f"Final columns          : "
        f"{len(df.columns):,}"
    )

    print(
        f"New features created   : "
        f"{len(new_columns):,}"
    )

    print(
        f"Overall status         : "
        f"{overall_status}"
    )


if __name__ == "__main__":
    main()
