from pathlib import Path
import pandas as pd


######   PROJECT PATHS   ######

PYTHON_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PYTHON_ROOT.parent


######   CLEANED SUPPORT TICKETS DATA   ######

CLEANED_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "02_Cleaned"
    / "Excel"
    / "support_tickets_cleaned.xlsx"
)


######   VALIDATION REPORT   ######

REPORT_FOLDER = (
    PYTHON_ROOT
    / "06_Outputs"
    / "09_validation_reports"
)

REPORT_FILE = (
    REPORT_FOLDER
    / "support_tickets_post_cleaning_validation_report.xlsx"
)


######   EXPECTED COLUMNS   ######

EXPECTED_COLUMNS = [
    "ticket_id",
    "customer_id",
    "ticket_date",
    "issue_type",
    "resolution_time_hours",
    "satisfaction_score",
    "resolved",
]


SERVICE_STATUS_VALUES = {
    "yes",
    "no",
}


######   LOAD CLEANED DATA   ######

def load_cleaned_support_tickets():
    """
    Load cleaned Support_Tickets data.
    """

    print("\n")
    print("LOADING CLEANED SUPPORT TICKETS DATA")

    df = pd.read_excel(
        CLEANED_FILE
    )

    print(
        f"Rows loaded    : {len(df):,}"
    )

    print(
        f"Columns loaded : {len(df.columns)}"
    )

    return df


######   CHECK COLUMNS   ######

def check_columns(df):

    results = []

    actual_columns = list(
        df.columns
    )

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    unexpected_columns = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    results.append({
        "Check": "Expected Columns Present",
        "Value": len(missing_columns) == 0,
        "Status": (
            "PASS"
            if len(missing_columns) == 0
            else "FAIL"
        ),
        "Details": (
            "All expected columns are present."
            if len(missing_columns) == 0
            else f"Missing columns: {missing_columns}"
        ),
    })

    results.append({
        "Check": "Unexpected Columns",
        "Value": len(unexpected_columns),
        "Status": "INFO",
        "Details": (
            "No unexpected columns."
            if len(unexpected_columns) == 0
            else f"Unexpected columns: {unexpected_columns}"
        ),
    })

    return results


######   CHECK MISSING VALUES   ######

def check_missing_values(df):

    results = []

    total_missing = int(
        df.isnull().sum().sum()
    )

    results.append({
        "Check": "Total Missing Values",
        "Value": total_missing,
        "Status": (
            "PASS"
            if total_missing == 0
            else "INFO"
        ),
        "Details": (
            "No missing values."
            if total_missing == 0
            else f"{total_missing:,} missing values found."
        ),
    })

    for column in EXPECTED_COLUMNS:

        missing_count = int(
            df[column].isnull().sum()
        )

        results.append({
            "Check": f"Missing Values - {column}",
            "Value": missing_count,
            "Status": (
                "PASS"
                if missing_count == 0
                else "INFO"
            ),
            "Details": (
                "No missing values."
                if missing_count == 0
                else f"{missing_count:,} missing values found."
            ),
        })

    return results


######   CHECK DUPLICATE ROWS   ######

def check_duplicate_rows(df):

    duplicate_rows = int(
        df.duplicated().sum()
    )

    return [{
        "Check": "Duplicate Rows",
        "Value": duplicate_rows,
        "Status": (
            "PASS"
            if duplicate_rows == 0
            else "FAIL"
        ),
        "Details": (
            "No duplicate rows."
            if duplicate_rows == 0
            else f"{duplicate_rows:,} duplicate rows found."
        ),
    }]


######   CHECK TICKET IDs   ######

def check_ticket_ids(df):

    results = []

    missing_ids = int(
        df["ticket_id"].isnull().sum()
    )

    duplicate_ids = int(
        df["ticket_id"].duplicated().sum()
    )

    blank_ids = int(
        df["ticket_id"]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    unique_ids = int(
        df["ticket_id"].nunique()
    )

    results.append({
        "Check": "Missing Ticket IDs",
        "Value": missing_ids,
        "Status": (
            "PASS"
            if missing_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No missing Ticket IDs."
            if missing_ids == 0
            else f"{missing_ids:,} missing Ticket IDs found."
        ),
    })

    results.append({
        "Check": "Duplicate Ticket IDs",
        "Value": duplicate_ids,
        "Status": (
            "PASS"
            if duplicate_ids == 0
            else "FAIL"
        ),
        "Details": (
            "Ticket IDs are unique."
            if duplicate_ids == 0
            else f"{duplicate_ids:,} duplicate Ticket IDs found."
        ),
    })

    results.append({
        "Check": "Blank Ticket IDs",
        "Value": blank_ids,
        "Status": (
            "PASS"
            if blank_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No blank Ticket IDs."
            if blank_ids == 0
            else f"{blank_ids:,} blank Ticket IDs found."
        ),
    })

    results.append({
        "Check": "Unique Ticket IDs",
        "Value": unique_ids,
        "Status": "INFO",
        "Details": "Number of unique tickets.",
    })

    return results


######   CHECK CUSTOMER IDS   ######

def check_customer_ids(df):

    results = []

    missing_ids = int(
        df["customer_id"].isnull().sum()
    )

    blank_ids = int(
        df["customer_id"]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    unique_customers = int(
        df["customer_id"].nunique()
    )

    results.append({
        "Check": "Missing Customer IDs",
        "Value": missing_ids,
        "Status": (
            "PASS"
            if missing_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No missing Customer IDs."
            if missing_ids == 0
            else f"{missing_ids:,} missing Customer IDs found."
        ),
    })

    results.append({
        "Check": "Blank Customer IDs",
        "Value": blank_ids,
        "Status": (
            "PASS"
            if blank_ids == 0
            else "FAIL"
        ),
        "Details": (
            "No blank Customer IDs."
            if blank_ids == 0
            else f"{blank_ids:,} blank Customer IDs found."
        ),
    })

    results.append({
        "Check": "Unique Customers in Support Tickets",
        "Value": unique_customers,
        "Status": "INFO",
        "Details": (
            "Number of unique customers "
            "with support tickets."
        ),
    })

    return results


######   CHECK DATES   ######

def check_dates(df):

    results = []

    invalid_dates = int(
        df["ticket_date"].isnull().sum()
    )

    future_dates = int(
        (
            df["ticket_date"]
            > pd.Timestamp.now()
        ).sum()
    )

    results.append({
        "Check": "Invalid Ticket Dates",
        "Value": invalid_dates,
        "Status": (
            "PASS"
            if invalid_dates == 0
            else "FAIL"
        ),
        "Details": (
            "All Ticket Dates are valid."
            if invalid_dates == 0
            else f"{invalid_dates:,} invalid Ticket Dates found."
        ),
    })

    results.append({
        "Check": "Future Ticket Dates",
        "Value": future_dates,
        "Status": (
            "PASS"
            if future_dates == 0
            else "INFO"
        ),
        "Details": (
            "No future Ticket Dates."
            if future_dates == 0
            else f"{future_dates:,} future Ticket Dates found."
        ),
    })

    return results


######   CHECK RESOLUTION TIME   ######

def check_resolution_time(df):

    results = []

    invalid_values = int(
        df["resolution_time_hours"].isnull().sum()
    )

    negative_values = int(
        (
            df["resolution_time_hours"]
            < 0
        ).sum()
    )

    zero_values = int(
        (
            df["resolution_time_hours"]
            == 0
        ).sum()
    )

    results.append({
        "Check": "Invalid Resolution Time",
        "Value": invalid_values,
        "Status": (
            "PASS"
            if invalid_values == 0
            else "INFO"
        ),
        "Details": (
            "No missing or invalid Resolution Time values."
            if invalid_values == 0
            else f"{invalid_values:,} missing Resolution Time values."
        ),
    })

    results.append({
        "Check": "Negative Resolution Time",
        "Value": negative_values,
        "Status": (
            "PASS"
            if negative_values == 0
            else "FAIL"
        ),
        "Details": (
            "No negative Resolution Time values."
            if negative_values == 0
            else f"{negative_values:,} negative values found."
        ),
    })

    results.append({
        "Check": "Zero Resolution Time",
        "Value": zero_values,
        "Status": "INFO",
        "Details": (
            "Number of tickets with zero-hour resolution."
        ),
    })

    return results


######   CHECK SATISFACTION SCORE   ######

def check_satisfaction_score(df):

    results = []

    missing_scores = int(
        df["satisfaction_score"].isnull().sum()
    )

    below_minimum = int(
        (
            df["satisfaction_score"] < 1
        )
        .fillna(False)
        .sum()
    )

    above_maximum = int(
        (
            df["satisfaction_score"] > 5
        )
        .fillna(False)
        .sum()
    )

    invalid_scores = (
        below_minimum
        + above_maximum
    )

    results.append({
        "Check": "Missing Satisfaction Scores",
        "Value": missing_scores,
        "Status": (
            "PASS"
            if missing_scores == 0
            else "INFO"
        ),
        "Details": (
            "No missing Satisfaction Scores."
            if missing_scores == 0
            else f"{missing_scores:,} missing Satisfaction Scores."
        ),
    })

    results.append({
        "Check": "Invalid Satisfaction Scores",
        "Value": invalid_scores,
        "Status": (
            "PASS"
            if invalid_scores == 0
            else "FAIL"
        ),
        "Details": (
            "All Satisfaction Scores are within 1-5."
            if invalid_scores == 0
            else (
                f"{invalid_scores:,} scores outside "
                "the 1-5 range."
            )
        ),
    })

    results.append({
        "Check": "Average Satisfaction Score",
        "Value": round(
            df["satisfaction_score"].mean(),
            2
        ),
        "Status": "INFO",
        "Details": "Average customer satisfaction score.",
    })

    return results


######   CHECK RESOLVED VALUES   ######

def check_resolved(df):

    results = []

    values = set(
        df["resolved"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .unique()
    )

    unexpected_values = (
        values
        - SERVICE_STATUS_VALUES
    )

    results.append({
        "Check": "Unexpected Resolved Values",
        "Value": len(unexpected_values),
        "Status": (
            "PASS"
            if len(unexpected_values) == 0
            else "FAIL"
        ),
        "Details": (
            "Only Yes/No values found."
            if len(unexpected_values) == 0
            else f"Unexpected values: {sorted(unexpected_values)}"
        ),
    })

    yes_count = int(
        (
            df["resolved"]
            .astype("string")
            .str.lower()
            == "yes"
        ).sum()
    )

    no_count = int(
        (
            df["resolved"]
            .astype("string")
            .str.lower()
            == "no"
        ).sum()
    )

    results.append({
        "Check": "Resolved Yes Count",
        "Value": yes_count,
        "Status": "INFO",
        "Details": "Number of resolved tickets.",
    })

    results.append({
        "Check": "Resolved No Count",
        "Value": no_count,
        "Status": "INFO",
        "Details": "Number of unresolved tickets.",
    })

    return results


######   CHECK ISSUE TYPES   ######

def check_issue_types(df):

    issue_types = sorted(
        df["issue_type"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    return [{
        "Check": "Issue Types",
        "Value": ", ".join(issue_types),
        "Status": "INFO",
        "Details": "Unique Support Ticket Issue Types.",
    }]


######   CHECK DATA TYPES   ######

def check_data_types(df):

    results = []

    results.append({
        "Check": "Ticket ID Data Type",
        "Value": str(
            df["ticket_id"].dtype
        ),
        "Status": "INFO",
        "Details": "Expected string/object type.",
    })

    results.append({
        "Check": "Customer ID Data Type",
        "Value": str(
            df["customer_id"].dtype
        ),
        "Status": "INFO",
        "Details": "Expected string/object type.",
    })

    results.append({
        "Check": "Ticket Date Data Type",
        "Value": str(
            df["ticket_date"].dtype
        ),
        "Status": (
            "PASS"
            if pd.api.types.is_datetime64_any_dtype(
                df["ticket_date"]
            )
            else "FAIL"
        ),
        "Details": "Ticket Date should be datetime.",
    })

    results.append({
        "Check": "Resolution Time Data Type",
        "Value": str(
            df["resolution_time_hours"].dtype
        ),
        "Status": (
            "PASS"
            if pd.api.types.is_numeric_dtype(
                df["resolution_time_hours"]
            )
            else "FAIL"
        ),
        "Details": "Resolution Time should be numeric.",
    })

    results.append({
        "Check": "Satisfaction Score Data Type",
        "Value": str(
            df["satisfaction_score"].dtype
        ),
        "Status": (
            "PASS"
            if pd.api.types.is_numeric_dtype(
                df["satisfaction_score"]
            )
            else "FAIL"
        ),
        "Details": "Satisfaction Score should be numeric.",
    })

    return results


######   RUN VALIDATION   ######

def run_validation(df):

    results = []

    results.extend(
        check_columns(df)
    )

    results.extend(
        check_missing_values(df)
    )

    results.extend(
        check_duplicate_rows(df)
    )

    results.extend(
        check_ticket_ids(df)
    )

    results.extend(
        check_customer_ids(df)
    )

    results.extend(
        check_dates(df)
    )

    results.extend(
        check_resolution_time(df)
    )

    results.extend(
        check_satisfaction_score(df)
    )

    results.extend(
        check_resolved(df)
    )

    results.extend(
        check_issue_types(df)
    )

    results.extend(
        check_data_types(df)
    )

    return pd.DataFrame(
        results
    )


######   CREATE SUMMARY   ######

def create_summary(
    df,
    validation_df
):

    passed = int(
        (
            validation_df["Status"]
            == "PASS"
        ).sum()
    )

    failed = int(
        (
            validation_df["Status"]
            == "FAIL"
        ).sum()
    )

    info = int(
        (
            validation_df["Status"]
            == "INFO"
        ).sum()
    )

    summary = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Total_Missing_Values",
            "Duplicate_Rows",
            "Missing_Ticket_IDs",
            "Duplicate_Ticket_IDs",
            "Unique_Ticket_IDs",
            "Missing_Customer_IDs",
            "Unique_Customer_IDs",
            "Missing_Ticket_Dates",
            "Missing_Issue_Types",
            "Missing_Resolution_Time",
            "Negative_Resolution_Time",
            "Missing_Satisfaction_Scores",
            "Invalid_Satisfaction_Scores",
            "Missing_Resolved",
            "Resolved_Yes_Count",
            "Resolved_No_Count",
            "Average_Resolution_Time_Hours",
            "Average_Satisfaction_Score",
            "Total_Checks",
            "Passed_Checks",
            "Failed_Checks",
            "Info_Checks",
        ],

        "Value": [
            len(df),

            len(df.columns),

            int(
                df.isnull().sum().sum()
            ),

            int(
                df.duplicated().sum()
            ),

            int(
                df["ticket_id"].isnull().sum()
            ),

            int(
                df["ticket_id"].duplicated().sum()
            ),

            int(
                df["ticket_id"].nunique()
            ),

            int(
                df["customer_id"].isnull().sum()
            ),

            int(
                df["customer_id"].nunique()
            ),

            int(
                df["ticket_date"].isnull().sum()
            ),

            int(
                df["issue_type"].isnull().sum()
            ),

            int(
                df["resolution_time_hours"].isnull().sum()
            ),

            int(
                (
                    df["resolution_time_hours"]
                    < 0
                ).sum()
            ),

            int(
                df["satisfaction_score"].isnull().sum()
            ),

            int(
                (
                    (
                        df["satisfaction_score"] < 1
                    )
                    |
                    (
                        df["satisfaction_score"] > 5
                    )
                )
                .fillna(False)
                .sum()
            ),

            int(
                df["resolved"].isnull().sum()
            ),

            int(
                (
                    df["resolved"]
                    .astype("string")
                    .str.lower()
                    == "yes"
                ).sum()
            ),

            int(
                (
                    df["resolved"]
                    .astype("string")
                    .str.lower()
                    == "no"
                ).sum()
            ),

            round(
                df["resolution_time_hours"].mean(),
                2
            ),

            round(
                df["satisfaction_score"].mean(),
                2
            ),

            len(validation_df),

            passed,

            failed,

            info,
        ],
    })

    return summary


######   SAVE VALIDATION REPORT   ######

def save_validation_report(
    validation_df,
    summary
):

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with pd.ExcelWriter(
        REPORT_FILE,
        engine="openpyxl"
    ) as writer:

        validation_df.to_excel(
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
    print("VALIDATION REPORT SAVED")

    print(
        REPORT_FILE
    )


######   DISPLAY RESULTS   ######

def display_results(
    validation_df,
    summary
):

    print("\n")
    print("SUPPORT TICKETS POST-CLEANING VALIDATION")

    print(
        validation_df.to_string(
            index=False
        )
    )

    print("\n")
    print("VALIDATION SUMMARY")

    print(
        summary.to_string(
            index=False
        )
    )


######   MAIN   ######

def main():

    print("\n")
    print("CUSTOMER CHURN & RETENTION ANALYSIS")
    print("SUPPORT TICKETS POST-CLEANING VALIDATION")
    
    # Load cleaned data
    
    df = load_cleaned_support_tickets()
    
    # Run validation
    
    validation_df = run_validation(
        df
    )
    
    # Create summary
    
    summary = create_summary(
        df,
        validation_df
    )
    
    # Display results
    
    display_results(
        validation_df,
        summary
    )
    
    # Save report
    
    save_validation_report(
        validation_df,
        summary
    )
    
    # Completion message
    
    print("\n")
    print(
        "SUPPORT TICKETS POST-CLEANING "
        "VALIDATION COMPLETED"
    )


######   SCRIPT ENTRY POINT   ######

if __name__ == "__main__":
    main()