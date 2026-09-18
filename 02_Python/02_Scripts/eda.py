from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

######    SUPPRESS NON-CRITICAL WARNINGS

warnings.filterwarnings("ignore")


###### PROJECT PATHS

# eda.py is located at:
#
# Customer_Churn/
#   02_Python/
#        02_Scripts/
#            eda.py

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   INPUT DATA PATH

INPUT_FILE = (
    PYTHON_ROOT
    / "06_Outputs"
    / "03_feature_engineering"
    / "customer_analytical_features.xlsx"
)


######   EDA OUTPUT PATHS

OUTPUT_DIR = (
    PYTHON_ROOT
    / "06_Outputs"
    / "02_eda"
)

CHART_DIR = OUTPUT_DIR / "charts"


######   COLUMN CLASSIFICATION   ######

# Exact 119-column classification supplied for this project.

CATEGORIES = {
    "Customer": [
        "customer_id",
        "gender",
        "age",
        "city",
        "state",
        "signup_date",
        "age_group",
        "signup_year",
        "signup_month",
        "signup_month_name",
        "signup_quarter",
        "signup_year_month",
    ],
    "Subscription": [
        "subscription_id",
        "plan",
        "contract_type",
        "start_date",
        "end_date",
        "monthly_charge",
        "annual_subscription_value",
        "monthly_charge_band",
        "plan_category",
        "contract_category",
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
        "tenure_days",
        "tenure_months",
        "tenure_years",
        "tenure_segment",
        "churn_year",
        "churn_month",
        "churn_month_name",
        "churn_quarter",
        "churn_year_month",
        "churn_timing_segment",
        "churn_data_quality_flag",
        "churn_target",
        "churn_year_engineered",
        "churn_month_engineered",
        "churn_month_name_engineered",
        "churn_quarter_engineered",
        "churn_year_month_engineered",
        "tenure_at_churn_months",
        "tenure_at_churn_years",
        "tenure_segment_engineered",
    ],
    "Customer Services": [
        "mobile_app",
        "streaming",
        "cloud_storage",
        "premium_support",
        "family_plan",
        "service_count",
        "service_adoption_rate",
        "service_adoption_segment",
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
        "days_since_last_payment",
        "payment_success_rate",
        "payment_failure_rate",
        "payment_methods_used",
        "primary_payment_method",
        "payments_per_month",
        "has_failed_payment",
        "has_successful_payment",
        "successful_vs_failed_amount_difference",
        "payment_failure_flag",
        "payment_activity_segment",
        "payment_value_segment",
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
        "days_since_last_ticket",
        "tickets_per_month",
        "has_support_ticket",
        "high_support_usage",
        "has_unresolved_ticket",
        "has_low_satisfaction",
        "support_usage_segment",
        "support_experience_segment",
        "support_risk_flag",
    ],
    "Engagement / Business": [
        "customer_engagement_score",
        "customer_engagement_level",
        "high_value_customer",
        "low_payment_success_flag",
        "support_experience_risk",
    ],
    "Observation / Technical": [
        "final_observation_date",
        "observation_date",
        "dataset_observation_date_x",
        "dataset_observation_date_y",
    ],
}


######   EXCLUDED COLUMNS   ######

# For explanatory EDA, exclude identifiers, technical date duplicates,
# and direct churn/leakage fields.

EXCLUDED = {
    "customer_id",
    "subscription_id",
    "final_observation_date",
    "observation_date",
    "dataset_observation_date_x",
    "dataset_observation_date_y",
    "churn_target",
    "churn_status",
    "churn_date",
    "is_churned",
    "is_active",
    "has_churn_date",
    "has_end_date",
    "end_date",
    "churn_year",
    "churn_month",
    "churn_month_name",
    "churn_quarter",
    "churn_year_month",
    "churn_year_engineered",
    "churn_month_engineered",
    "churn_month_name_engineered",
    "churn_quarter_engineered",
    "churn_year_month_engineered",
    "churn_timing_segment",
    "churn_data_quality_flag",
    "tenure_days_at_churn",
    "tenure_months_at_churn",
    "tenure_years_at_churn",
    "tenure_at_churn_months",
    "tenure_at_churn_years",
    "tenure_segment_engineered",
}


######    STANDARDIZE COLUMN NAMES   ######

def std(df):
    """Standardize DataFrame column names."""

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False,
        )
        .str.replace(
            "-",
            "_",
            regex=False,
        )
    )

    return df


######   SAVE DATAFRAMES TO EXCEL   ######

def save_xlsx(path, sheets):
    """Save multiple DataFrames to separate Excel sheets."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:

        for name, data in sheets.items():

            if data is not None:

                data.to_excel(
                    writer,
                    sheet_name=str(name)[:31],
                    index=False,
                )


######   DATASET PROFILE   ######

def profile(df):
    """Create a column-level dataset profile."""

    lookup = {
        column: category
        for category, columns in CATEGORIES.items()
        for column in columns
    }

    rows = []

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_numeric_dtype(series):

            data_type = "Numeric"

        elif pd.api.types.is_datetime64_any_dtype(series):

            data_type = "Date"

        else:

            data_type = "Categorical/Text"

        rows.append(
            {
                "Column": column,
                "Category": lookup.get(
                    column,
                    "Other / Review",
                ),
                "Data_Type": str(
                    series.dtype
                ),
                "EDA_Type": data_type,
                "Rows": len(df),
                "Missing_Count": int(
                    series.isna().sum()
                ),
                "Missing_Percent": round(
                    series.isna().mean() * 100,
                    2,
                ),
                "Unique_Count": int(
                    series.nunique(
                        dropna=True
                    )
                ),
            }
        )

    return pd.DataFrame(rows)


######   NUMERICAL SUMMARY   ######

def num_summary(df):
    """Create summary statistics for numerical columns."""

    rows = []

    for column in df.select_dtypes(
        include=np.number
    ):

        series = df[column]

        rows.append(
            {
                "Column": column,
                "Count": int(
                    series.count()
                ),
                "Missing": int(
                    series.isna().sum()
                ),
                "Mean": series.mean(),
                "Median": series.median(),
                "Std": series.std(),
                "Min": series.min(),
                "Q1": series.quantile(0.25),
                "Q3": series.quantile(0.75),
                "Max": series.max(),
                "Zero_Count": int(
                    (series == 0).sum()
                ),
                "Negative_Count": int(
                    (series < 0).sum()
                ),
            }
        )

    return pd.DataFrame(rows)


######   CATEGORICAL SUMMARY   ######

def cat_summary(df):
    """Create frequency summaries for categorical/text columns."""

    rows = []

    for column in df.select_dtypes(
        include=[
            "object",
            "category",
            "string",
        ]
    ):

        value_counts = (
            df[column]
            .value_counts(
                dropna=False
            )
        )

        for value, count in value_counts.items():

            rows.append(
                {
                    "Column": column,
                    "Value": (
                        "<MISSING>"
                        if pd.isna(value)
                        else str(value)
                    ),
                    "Count": int(count),
                    "Percentage": round(
                        count / len(df) * 100,
                        2,
                    ),
                }
            )

    return pd.DataFrame(rows)


######   CHURN BY CATEGORICAL VARIABLE   ######

def churn_cat(df, column):
    """Calculate customer count and churn rate by category."""

    data = df[
        [
            column,
            "churn_target",
        ]
    ].copy()

    data[column] = data[column].fillna(
        "<MISSING>"
    )

    result = (
        data
        .groupby(
            column,
            dropna=False,
        )
        .agg(
            Customers=(
                "churn_target",
                "size",
            ),
            Churned=(
                "churn_target",
                "sum",
            ),
        )
        .reset_index()
    )

    result["Active"] = (
        result["Customers"]
        - result["Churned"]
    )

    result["Churn_Rate_Percent"] = (
        result["Churned"]
        / result["Customers"]
        * 100
    ).round(2)

    return result.sort_values(
        "Churn_Rate_Percent",
        ascending=False,
    )


######    MAIN EDA WORKFLOW   ######

def main():

    ######   Create output directories

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    ######   Display project header

    print("CUSTOMER CHURN & RETENTION")
    print("EXPLORATORY DATA ANALYSIS")
    print("\n")

    ######   Validate input file

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    ######   Load analytical dataset

    df = std(
        pd.read_excel(
            INPUT_FILE
        )
    )

    ######   Convert date columns

    for column in df.columns:

        if (
            column.endswith("_date")
            or column in [
                "signup_date",
                "start_date",
                "end_date",
                "first_payment_date",
                "last_payment_date",
                "first_ticket_date",
                "last_ticket_date",
                "final_observation_date",
                "observation_date",
                "dataset_observation_date_x",
                "dataset_observation_date_y",
            ]
        ):

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    ######   Display dataset size

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns):,}"
    )

    ######   Generate dataset profiles

    profile_df = profile(df)
    numerical_df = num_summary(df)
    categorical_df = cat_summary(df)

    profile_df.to_excel(
        OUTPUT_DIR / "column_profile.xlsx",
        index=False,
    )

    numerical_df.to_excel(
        OUTPUT_DIR / "numerical_analysis.xlsx",
        index=False,
    )

    categorical_df.to_excel(
        OUTPUT_DIR / "categorical_analysis.xlsx",
        index=False,
    )

    ######   Churn analysis

    churn = {}

    churn["Overall_Churn"] = pd.DataFrame(
        [
            {
                "Customers": len(df),
                "Churned_Customers": int(
                    df.churn_target.sum()
                ),
                "Active_Customers": int(
                    (df.churn_target == 0).sum()
                ),
                "Churn_Rate_Percent": round(
                    df.churn_target.mean() * 100,
                    2,
                ),
            }
        ]
    )

    churn_columns = [
        "gender",
        "age_group",
        "state",
        "plan",
        "contract_type",
        "monthly_charge_band",
        "plan_category",
        "contract_category",
        "tenure_segment",
        "churn_timing_segment",
        "payment_activity_segment",
        "payment_value_segment",
        "service_adoption_segment",
        "support_usage_segment",
        "support_experience_segment",
        "customer_engagement_level",
        "primary_payment_method",
    ]

    for column in churn_columns:

        if column in df:

            result = churn_cat(
                df,
                column,
            )

            churn[
                "Churn_by_"
                + column[:20]
            ] = result

            chart_data = (
                result
                .head(15)
                .sort_values(
                    "Churn_Rate_Percent"
                )
            )

            plt.figure(
                figsize=(10, 6)
            )

            plt.barh(
                chart_data[column].astype(str),
                chart_data[
                    "Churn_Rate_Percent"
                ],
            )

            plt.xlabel(
                "Churn Rate (%)"
            )

            plt.title(
                "Churn Rate by "
                + column
            )

            plt.tight_layout()

            plt.savefig(
                CHART_DIR
                / f"churn_by_{column}.png",
                dpi=150,
            )

            plt.close()

    save_xlsx(
        OUTPUT_DIR / "churn_analysis.xlsx",
        churn,
    )

    ######   Segment analysis

    segment_analysis = {}

    segment_columns = [
        "age_group",
        "monthly_charge_band",
        "tenure_segment",
        "payment_activity_segment",
        "payment_value_segment",
        "service_adoption_segment",
        "support_usage_segment",
        "support_experience_segment",
        "customer_engagement_level",
    ]

    for column in segment_columns:

        if column in df:

            result = (
                df
                .groupby(
                    column,
                    dropna=False,
                )
                .agg(
                    Customers=(
                        "customer_id",
                        "nunique",
                    ),
                    Churned=(
                        "churn_target",
                        "sum",
                    ),
                    Average_Monthly_Charge=(
                        "monthly_charge",
                        "mean",
                    ),
                    Average_Payment_Success_Rate=(
                        "payment_success_rate",
                        "mean",
                    ),
                    Average_Service_Adoption=(
                        "service_adoption_rate",
                        "mean",
                    ),
                    Average_Tickets=(
                        "total_ticket_count",
                        "mean",
                    ),
                )
                .reset_index()
            )

            result["Churn_Rate_Percent"] = (
                result["Churned"]
                / result["Customers"]
                * 100
            ).round(2)

            segment_analysis[
                "Segment_"
                + column[:22]
            ] = result

    save_xlsx(
        OUTPUT_DIR / "segment_analysis.xlsx",
        segment_analysis,
    )

    ######   Correlation analysis

    correlation_columns = [
        "age",
        "monthly_charge",
        "annual_subscription_value",
        "tenure_days",
        "tenure_months",
        "total_payment_count",
        "successful_payment_count",
        "failed_payment_count",
        "total_payment_amount",
        "successful_payment_amount",
        "failed_payment_amount",
        "average_payment_amount",
        "payments_per_month",
        "payment_success_rate",
        "payment_failure_rate",
        "service_count",
        "service_adoption_rate",
        "total_ticket_count",
        "resolved_ticket_count",
        "unresolved_ticket_count",
        "average_resolution_time_hours",
        "average_satisfaction_score",
        "ticket_resolution_rate",
        "tickets_per_month",
        "unique_issue_types",
        "customer_engagement_score",
        "churn_target",
    ]

    available_correlation_columns = [
        column
        for column in correlation_columns
        if column in df
    ]

    correlation = (
        df[
            available_correlation_columns
        ]
        .corr(
            numeric_only=True
        )
    )

    pairs = []

    for index, feature_1 in enumerate(
        correlation.columns
    ):

        for feature_2 in correlation.columns[
            index + 1:
        ]:

            correlation_value = float(
                correlation.loc[
                    feature_1,
                    feature_2,
                ]
            )

            pairs.append(
                {
                    "Feature_1": feature_1,
                    "Feature_2": feature_2,
                    "Correlation": round(
                        correlation_value,
                        4,
                    ),
                    "Absolute_Correlation": round(
                        abs(correlation_value),
                        4,
                    ),
                }
            )

    if pairs:

        pairs_df = (
            pd.DataFrame(pairs)
            .sort_values(
                "Absolute_Correlation",
                ascending=False,
            )
        )

    else:

        pairs_df = pd.DataFrame(
            columns=[
                "Feature_1",
                "Feature_2",
                "Correlation",
                "Absolute_Correlation",
            ]
        )

    churn_relationships = pairs_df[
        (
            pairs_df["Feature_1"]
            == "churn_target"
        )
        |
        (
            pairs_df["Feature_2"]
            == "churn_target"
        )
    ]

    save_xlsx(
        OUTPUT_DIR / "correlation_analysis.xlsx",
        {
            "Correlation_Matrix": (
                correlation
                .reset_index()
                .rename(
                    columns={
                        "index": "Feature"
                    }
                )
            ),
            "Correlation_Pairs": pairs_df,
            "Churn_Relationships": (
                churn_relationships
            ),
        },
    )

    ######   Correlation heatmap

    if not correlation.empty:

        plt.figure(
            figsize=(14, 11)
        )

        plt.imshow(
            correlation.values,
            aspect="auto",
        )

        plt.colorbar(
            label="Correlation"
        )

        plt.xticks(
            range(
                len(correlation.columns)
            ),
            correlation.columns,
            rotation=90,
            fontsize=7,
        )

        plt.yticks(
            range(
                len(correlation)
            ),
            correlation.index,
            fontsize=7,
        )

        plt.title(
            "Numerical Feature Correlation Matrix"
        )

        plt.tight_layout()

        plt.savefig(
            CHART_DIR
            / "correlation_heatmap.png",
            dpi=150,
        )

        plt.close()

    ######   Numerical distribution charts

    distribution_columns = [
        "age",
        "monthly_charge",
        "service_count",
        "total_payment_count",
        "total_ticket_count",
        "customer_engagement_score",
    ]

    for column in distribution_columns:

        if column in df:

            values = (
                pd.to_numeric(
                    df[column],
                    errors="coerce",
                )
                .dropna()
            )

            if len(values):

                plt.figure(
                    figsize=(10, 6)
                )

                plt.hist(
                    values,
                    bins=30,
                )

                plt.title(
                    column
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
                    + " Distribution"
                )

                plt.xlabel(
                    column
                )

                plt.ylabel(
                    "Customers"
                )

                plt.tight_layout()

                plt.savefig(
                    CHART_DIR
                    / f"{column}_distribution.png",
                    dpi=150,
                )

                plt.close()

    ######   EDA summary

    summary = pd.DataFrame(
        [
            {
                "Rows": len(df),
                "Columns": len(df.columns),
                "Unique_Customers": (
                    df.customer_id.nunique()
                ),
                "Duplicate_Customer_IDs": int(
                    df.customer_id.duplicated().sum()
                ),
                "Total_Missing_Values": int(
                    df.isna().sum().sum()
                ),
                "Numeric_Columns": len(
                    df.select_dtypes(
                        include=np.number
                    ).columns
                ),
                "Categorical_Text_Columns": len(
                    df.select_dtypes(
                        include=[
                            "object",
                            "category",
                            "string",
                        ]
                    ).columns
                ),
                "Date_Columns": len(
                    df.select_dtypes(
                        include=[
                            "datetime",
                            "datetimetz",
                        ]
                    ).columns
                ),
                "Churned_Customers": int(
                    df.churn_target.sum()
                ),
                "Active_Customers": int(
                    (df.churn_target == 0).sum()
                ),
                "Churn_Rate_Percent": round(
                    df.churn_target.mean() * 100,
                    2,
                ),
            }
        ]
    )

    ######   Category and missing-value summaries

    category_summary = (
        profile_df
        .groupby("Category")
        .agg(
            Columns=(
                "Column",
                "count",
            ),
            Missing_Values=(
                "Missing_Count",
                "sum",
            ),
        )
        .reset_index()
    )

    missing_columns = (
        profile_df[
            profile_df["Missing_Count"] > 0
        ]
        .sort_values(
            "Missing_Count",
            ascending=False,
        )
    )

    save_xlsx(
        OUTPUT_DIR / "eda_summary_report.xlsx",
        {
            "EDA_Summary": summary,
            "Missing_Columns": missing_columns,
            "Category_Summary": category_summary,
        },
    )

    ######   EDA completion report

    completed_areas = [
        "Dataset Profile",
        "Numerical Analysis",
        "Categorical Analysis",
        "Churn Analysis",
        "Segment Analysis",
        "Correlation Analysis",
        "Visualization",
    ]

    save_xlsx(
        OUTPUT_DIR / "eda_report.xlsx",
        {
            "EDA_Report": pd.DataFrame(
                [
                    {
                        "EDA_Area": area,
                        "Status": "COMPLETED",
                    }
                    for area in completed_areas
                ]
            ),
            "Excluded_Columns": pd.DataFrame(
                {
                    "Column": sorted(
                        EXCLUDED
                    )
                }
            ),
        },
    )

    ######   Final output

    print(
        "\nEDA COMPLETED"
    )

    print(
        f"Rows analyzed        : "
        f"{len(df):,}"
    )

    print(
        f"Columns analyzed     : "
        f"{len(df.columns):,}"
    )

    print(
        f"Churn rate           : "
        f"{df.churn_target.mean() * 100:.2f}%"
    )

    print(
        f"Charts directory     : "
        f"{CHART_DIR}"
    )



######   SCRIPT ENTRY POINT    ######

if __name__ == "__main__":
    main()