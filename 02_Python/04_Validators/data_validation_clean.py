"""
Customer Churn & Retention Analysis
Data Validation Script

Purpose:
    Validate the raw Customer Churn & Retention workbook before cleaning
    and downstream analysis.

Expected project structure:
    Customer_Churn/
         01_Data/
            01_Raw/
               Customer_Churn_Retention_Raw_Data.xlsx
         02_Python/
             04_Validators/
                 data_validation_clean.py

The script performs:
    - Workbook and sheet validation
    - Missing-value analysis
    - Duplicate analysis
    - Customers validation
    - Subscriptions validation
    - Payments validation
    - Customer Services validation
    - Support Tickets validation
    - Data Dictionary validation
    - Referential-integrity checks
    - Date/business-rule checks
"""

from pathlib import Path
import pandas as pd

### 1. LOAD RAW DATA

######   PROJECT PATHS   ######

PYTHON_ROOT = (Path(__file__).resolve().parents[1])
PROJECT_ROOT = (PYTHON_ROOT.parent)

######   RAW DATA FILE   ######

FILE_PATH = (
    PROJECT_ROOT
    / "01_Data"
    / "01_Raw"
    / "Customer_Churn_Retention_Raw_Data.xlsx"
)

EXPECTED_SHEETS = {
    "customers",
    "subscriptions",
    "payments",
    "customer_services",
    "support_tickets",
    "Data_Dictionary",
}


def load_raw_data(file_path: Path) -> dict[str, pd.DataFrame]:
    """Load all expected sheets from the raw Excel workbook."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data file was not found:\n{file_path}\n"
            "Check that the file is located in 01_Data/01_Raw."
        )

    excel_file = pd.ExcelFile(file_path)
    available_sheets = set(excel_file.sheet_names)

    print("=" * 70)
    print("WORKBOOK VALIDATION")
    print("=" * 70)
    print("Workbook:", file_path)
    print("Available sheets:", excel_file.sheet_names)

    missing_sheets = EXPECTED_SHEETS - available_sheets
    if missing_sheets:
        raise ValueError(
            f"Missing expected sheets: {sorted(missing_sheets)}"
        )

    data = {
        "customers": pd.read_excel(excel_file, sheet_name="customers"),
        "subscriptions": pd.read_excel(
            excel_file, sheet_name="subscriptions"
        ),
        "payments": pd.read_excel(excel_file, sheet_name="payments"),
        "customer_services": pd.read_excel(
            excel_file, sheet_name="customer_services"
        ),
        "support_tickets": pd.read_excel(
            excel_file, sheet_name="support_tickets"
        ),
        "data_dictionary": pd.read_excel(
            excel_file, sheet_name="Data_Dictionary"
        ),
    }

    return data

######   2. GENERAL VALIDATION HELPERS   ######

def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing count and percentage for every column."""
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df) * 100).round(2)

    return (
        pd.DataFrame(
            {
                "Missing_Count": missing_count,
                "Missing_Percentage": missing_percentage,
            }
        )
        .sort_values("Missing_Count", ascending=False)
    )


def print_section(title: str) -> None:
    """Print a consistent section heading."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_duplicate_summary(data: dict[str, pd.DataFrame]) -> None:
    """Print exact duplicate-row counts for all loaded tables."""
    print_section("DUPLICATE RECORD ANALYSIS")

    for name, df in data.items():
        print(f"{name}: {df.duplicated().sum()} duplicate rows")


######   3. CUSTOMERS VALIDATION   ######

def validate_customers(
    customers: pd.DataFrame,
    customer_ids: set,
) -> None:
    """Validate the Customers table."""
    print_section("CUSTOMERS DATA VALIDATION")

    print("Shape:", customers.shape)
    print("\nColumns:")
    print(customers.columns.tolist())

    print("\nMissing Values:")
    print(missing_value_summary(customers))

    print("\nGender Distribution:")
    print(customers["Gender"].value_counts(dropna=False))

    print("\nCity Distribution:")
    print(customers["City"].value_counts(dropna=False))

    print("\nState Distribution:")
    print(customers["State"].value_counts(dropna=False))

    print("\nCustomer_ID:")
    print("Missing:", customers["Customer_ID"].isnull().sum())
    print("Unique:", customers["Customer_ID"].nunique())
    print("Duplicate:", customers["Customer_ID"].duplicated().sum())

    print("\nAge:")
    print(customers["Age"].describe())

    invalid_age = customers[
        (customers["Age"] < 18) | (customers["Age"] > 75)
    ]
    print("Age outside 18-75:", len(invalid_age))

    customers["Signup_Date"] = pd.to_datetime(
        customers["Signup_Date"], errors="coerce"
    )

    print("\nSignup_Date:")
    print("Data Type:", customers["Signup_Date"].dtype)
    print("Missing:", customers["Signup_Date"].isnull().sum())
    print("Minimum:", customers["Signup_Date"].min())
    print("Maximum:", customers["Signup_Date"].max())

    out_of_period = customers[
        (customers["Signup_Date"] < "2023-01-01")
        | (customers["Signup_Date"] > "2025-12-31")
    ]
    print("Outside 2023-2025:", len(out_of_period))

    city_missing_state_available = customers[
        customers["City"].isnull() & customers["State"].notnull()
    ]
    print(
        "\nCity missing but State available:",
        len(city_missing_state_available),
    )

    city_state_both_missing = customers[
        customers["City"].isnull() & customers["State"].isnull()
    ]
    print("Both City and State missing:", len(city_state_both_missing))

    city_state_duplicates = (
        customers[["City", "State"]]
        .drop_duplicates()
        .sort_values(["State", "City"])
    )
    print("\nUnique City-State combinations:")
    print(city_state_duplicates.head(20))

    print("\nExact duplicate rows:")
    print(customers[customers.duplicated()].head(20))


######   4. SUBSCRIPTIONS VALIDATION   ######

def validate_subscriptions(
    subscriptions: pd.DataFrame,
    customers: pd.DataFrame,
    customer_ids: set,
) -> None:
    """Validate the Subscriptions table."""
    print_section("SUBSCRIPTIONS DATA VALIDATION")

    print("Shape:", subscriptions.shape)
    print("\nColumns:")
    print(subscriptions.columns.tolist())

    print("\nMissing Values:")
    print(missing_value_summary(subscriptions))

    subscriptions["Start_Date"] = pd.to_datetime(
        subscriptions["Start_Date"], errors="coerce"
    )
    subscriptions["End_Date"] = pd.to_datetime(
        subscriptions["End_Date"], errors="coerce"
    )
    subscriptions["Churn_Date"] = pd.to_datetime(
        subscriptions["Churn_Date"], errors="coerce"
    )

    print("\nCustomer_ID:")
    print("Missing:", subscriptions["Customer_ID"].isnull().sum())
    print("Unique:", subscriptions["Customer_ID"].nunique())
    print("Duplicate:", subscriptions["Customer_ID"].duplicated().sum())

    print("\nSubscription_ID:")
    print("Missing:", subscriptions["Subscription_ID"].isnull().sum())
    print("Unique:", subscriptions["Subscription_ID"].nunique())
    print(
        "Duplicate:",
        subscriptions["Subscription_ID"].duplicated().sum(),
    )

    print("\nPlan:")
    print(subscriptions["Plan"].value_counts(dropna=False))

    print("\nContract_Type:")
    print(subscriptions["Contract_Type"].value_counts(dropna=False))

    print("\nStart_Date:")
    print("Missing:", subscriptions["Start_Date"].isnull().sum())
    print("Minimum:", subscriptions["Start_Date"].min())
    print("Maximum:", subscriptions["Start_Date"].max())

    print("\nEnd_Date:")
    print("Missing:", subscriptions["End_Date"].isnull().sum())
    print("Minimum:", subscriptions["End_Date"].min())
    print("Maximum:", subscriptions["End_Date"].max())

    print("\nMonthly_Charge:")
    print(subscriptions["Monthly_Charge"].describe())
    print("Minimum:", subscriptions["Monthly_Charge"].min())
    print("Maximum:", subscriptions["Monthly_Charge"].max())
    print(
        "Non-positive charges:",
        (subscriptions["Monthly_Charge"] <= 0).sum(),
    )

    print("\nChurn_Status:")
    print(subscriptions["Churn_Status"].value_counts(dropna=False))
    print(
        "Missing:",
        subscriptions["Churn_Status"].isnull().sum(),
    )

    print("\nChurn_Date:")
    print("Missing:", subscriptions["Churn_Date"].isnull().sum())
    print("Minimum:", subscriptions["Churn_Date"].min())
    print("Maximum:", subscriptions["Churn_Date"].max())

    active_with_churn_date = subscriptions[
        (subscriptions["Churn_Status"] == "Active")
        & subscriptions["Churn_Date"].notnull()
    ]
    churned_without_churn_date = subscriptions[
        (subscriptions["Churn_Status"] == "Churned")
        & subscriptions["Churn_Date"].isnull()
    ]

    print(
        "\nActive subscriptions with Churn_Date:",
        len(active_with_churn_date),
    )
    print(
        "Churned subscriptions without Churn_Date:",
        len(churned_without_churn_date),
    )

    invalid_end_dates = subscriptions[
        subscriptions["End_Date"] < subscriptions["Start_Date"]
    ]
    print(
        "End_Date before Start_Date:",
        len(invalid_end_dates),
    )

    invalid_churn_start = subscriptions[
        subscriptions["Churn_Date"] < subscriptions["Start_Date"]
    ]
    print(
        "Churn_Date before Start_Date:",
        len(invalid_churn_start),
    )

    invalid_churn_end = subscriptions[
        subscriptions["Churn_Date"].notnull()
        & subscriptions["End_Date"].notnull()
        & (subscriptions["Churn_Date"] > subscriptions["End_Date"])
    ]
    print(
        "Churn_Date after End_Date:",
        len(invalid_churn_end),
    )

    orphan_subscriptions = subscriptions[
        subscriptions["Customer_ID"].notnull()
        & ~subscriptions["Customer_ID"].isin(customer_ids)
    ]
    print(
        "Subscriptions without matching customer:",
        len(orphan_subscriptions),
    )

    customer_signup_dates = customers[
        ["Customer_ID", "Signup_Date"]
    ].copy()

    subscription_validation = subscriptions.merge(
        customer_signup_dates,
        on="Customer_ID",
        how="left",
        suffixes=("", "_Customer"),
    )

    subscription_before_signup = subscription_validation[
        subscription_validation["Start_Date"]
        < subscription_validation["Signup_Date"]
    ]
    print(
        "Subscription Start_Date before Customer Signup_Date:",
        len(subscription_before_signup),
    )

    print("\nMonthly charge by Plan:")
    print(subscriptions.groupby("Plan")["Monthly_Charge"].describe())

    print("\nContract Type vs Churn Status:")
    print(
        pd.crosstab(
            subscriptions["Contract_Type"],
            subscriptions["Churn_Status"],
            dropna=False,
        )
    )

######   5. PAYMENTS VALIDATION   ######

def validate_payments(
    payments: pd.DataFrame,
    customers: pd.DataFrame,
    customer_ids: set,
) -> None:
    """Validate the Payments table."""
    print_section("PAYMENTS DATA VALIDATION")

    print("Shape:", payments.shape)
    print("\nColumns:")
    print(payments.columns.tolist())

    print("\nMissing Values:")
    print(missing_value_summary(payments))

    print("\nPayment_ID:")
    print("Missing:", payments["Payment_ID"].isnull().sum())
    print("Unique:", payments["Payment_ID"].nunique())
    print("Duplicate:", payments["Payment_ID"].duplicated().sum())

    print("\nCustomer_ID:")
    print("Missing:", payments["Customer_ID"].isnull().sum())
    print("Unique Customers:", payments["Customer_ID"].nunique())

    print("\nPayments per Customer:")
    print(payments.groupby("Customer_ID")["Payment_ID"].count().describe())

    payments["Payment_Date"] = pd.to_datetime(
        payments["Payment_Date"], errors="coerce"
    )

    print("\nPayment_Date:")
    print("Data Type:", payments["Payment_Date"].dtype)
    print("Missing:", payments["Payment_Date"].isnull().sum())
    print("Minimum:", payments["Payment_Date"].min())
    print("Maximum:", payments["Payment_Date"].max())

    out_of_period = payments[
        (payments["Payment_Date"] < "2023-01-01")
        | (payments["Payment_Date"] > "2025-12-31")
    ]
    print("Outside 2023-2025:", len(out_of_period))

    print("\nAmount:")
    print(payments["Amount"].describe())
    print("Minimum:", payments["Amount"].min())
    print("Maximum:", payments["Amount"].max())
    print("Non-positive amounts:", (payments["Amount"] <= 0).sum())
    print("Missing Amount:", payments["Amount"].isnull().sum())

    print("\nPayment Method:")
    print(payments["Payment_Method"].value_counts(dropna=False))

    print("\nPayment Status:")
    print(payments["Payment_Status"].value_counts(dropna=False))
    print(
        "Missing Payment_Status:",
        payments["Payment_Status"].isnull().sum(),
    )

    print("\nPayment Status vs Amount:")
    print(payments.groupby("Payment_Status")["Amount"].describe())

    orphan_payments = payments[
        payments["Customer_ID"].notnull()
        & ~payments["Customer_ID"].isin(customer_ids)
    ]
    print(
        "\nPayments without matching customer:",
        len(orphan_payments),
    )

    print("\nDuplicate payment transactions:")
    print("Exact duplicate rows:", payments.duplicated().sum())

    duplicate_payment_ids = payments[
        payments["Payment_ID"].duplicated(keep=False)
    ].sort_values("Payment_ID")
    print(
        "Rows with duplicated Payment_ID:",
        len(duplicate_payment_ids),
    )

    print("\nPayment amount by method:")
    print(payments.groupby("Payment_Method")["Amount"].describe())

    print("\nPayment Status Distribution (%):")
    print(
        payments["Payment_Status"]
        .value_counts(normalize=True, dropna=False)
        .mul(100)
        .round(2)
    )


######   6. CUSTOMER SERVICES VALIDATION   ######

def validate_customer_services(
    customer_services: pd.DataFrame,
    customers: pd.DataFrame,
    customer_ids: set,
) -> None:
    """Validate the Customer Services table."""
    print_section("CUSTOMER SERVICES DATA VALIDATION")

    print("Shape:", customer_services.shape)
    print("\nColumns:")
    print(customer_services.columns.tolist())

    print("\nMissing Values:")
    print(missing_value_summary(customer_services))

    print("\nCustomer_ID:")
    print(
        "Missing:",
        customer_services["Customer_ID"].isnull().sum(),
    )
    print(
        "Unique:",
        customer_services["Customer_ID"].nunique(),
    )
    print(
        "Duplicate:",
        customer_services["Customer_ID"].duplicated().sum(),
    )

    service_columns = [
        "Internet_Service",
        "Streaming_Service",
        "Cloud_Storage",
        "Device_Protection",
    ]

    for column in service_columns:
        print(f"\n{column}:")
        print(customer_services[column].value_counts(dropna=False))

    print("\nExact duplicate rows:")
    print(customer_services[customer_services.duplicated()].head(20))

    orphan_services = customer_services[
        customer_services["Customer_ID"].notnull()
        & ~customer_services["Customer_ID"].isin(customer_ids)
    ]
    print(
        "Service records without matching customer:",
        len(orphan_services),
    )

    customer_service_ids = set(
        customer_services["Customer_ID"].dropna()
    )
    customer_ids_without_service = (
        customer_ids - customer_service_ids
    )
    service_ids_without_customer = (
        customer_service_ids - customer_ids
    )

    print(
        "Customers without service record:",
        len(customer_ids_without_service),
    )
    print(
        "Service records without customer record:",
        len(service_ids_without_customer),
    )

    print("\nMost common service combinations:")
    print(
        customer_services.groupby(
            service_columns,
            dropna=False,
        )
        .size()
        .sort_values(ascending=False)
        .head(20)
    )


######   7. SUPPORT TICKETS VALIDATION   ######

def validate_support_tickets(
    support_tickets: pd.DataFrame,
    customers: pd.DataFrame,
    customer_ids: set,
) -> None:
    """Validate the Support Tickets table."""
    print_section("SUPPORT TICKETS DATA VALIDATION")

    print("Shape:", support_tickets.shape)
    print("\nColumns:")
    print(support_tickets.columns.tolist())

    print("\nMissing Values:")
    print(missing_value_summary(support_tickets))

    print("\nTicket_ID:")
    print("Missing:", support_tickets["Ticket_ID"].isnull().sum())
    print("Unique:", support_tickets["Ticket_ID"].nunique())
    print(
        "Duplicate:",
        support_tickets["Ticket_ID"].duplicated().sum(),
    )

    duplicate_ticket_ids = support_tickets[
        support_tickets["Ticket_ID"].duplicated(keep=False)
    ].sort_values("Ticket_ID")
    print(
        "Rows with duplicated Ticket_ID:",
        len(duplicate_ticket_ids),
    )

    print("\nCustomer_ID:")
    print("Missing:", support_tickets["Customer_ID"].isnull().sum())
    print("Unique Customers:", support_tickets["Customer_ID"].nunique())

    print("\nTicket Count per Customer:")
    ticket_counts = support_tickets.groupby("Customer_ID")[
        "Ticket_ID"
    ].count()
    print(ticket_counts.describe())
    print("\nCustomers with most tickets:")
    print(ticket_counts.sort_values(ascending=False).head(10))

    support_tickets["Ticket_Date"] = pd.to_datetime(
        support_tickets["Ticket_Date"], errors="coerce"
    )

    print("\nTicket_Date:")
    print("Data Type:", support_tickets["Ticket_Date"].dtype)
    print("Missing:", support_tickets["Ticket_Date"].isnull().sum())
    print("Minimum:", support_tickets["Ticket_Date"].min())
    print("Maximum:", support_tickets["Ticket_Date"].max())

    out_of_period = support_tickets[
        (support_tickets["Ticket_Date"] < "2023-01-01")
        | (support_tickets["Ticket_Date"] > "2025-12-31")
    ]
    print("Outside 2023-2025:", len(out_of_period))

    print("\nIssue_Type:")
    print(support_tickets["Issue_Type"].value_counts(dropna=False))

    print("\nPriority:")
    print(support_tickets["Priority"].value_counts(dropna=False))

    print("\nResolved:")
    print(support_tickets["Resolved"].value_counts(dropna=False))
    print(
        "Missing Resolved:",
        support_tickets["Resolved"].isnull().sum(),
    )

    print("\nSatisfaction_Score:")
    print(support_tickets["Satisfaction_Score"].describe())
    print(
        "Minimum:",
        support_tickets["Satisfaction_Score"].min(),
    )
    print(
        "Maximum:",
        support_tickets["Satisfaction_Score"].max(),
    )
    print(
        "Missing:",
        support_tickets["Satisfaction_Score"].isnull().sum(),
    )

    invalid_satisfaction = support_tickets[
        (support_tickets["Satisfaction_Score"] < 1)
        | (support_tickets["Satisfaction_Score"] > 5)
    ]
    print(
        "Invalid Satisfaction Scores:",
        len(invalid_satisfaction),
    )

    print("\nResolution Time:")
    if "Resolution_Time_Hours" in support_tickets.columns:
        print(
            support_tickets["Resolution_Time_Hours"].describe()
        )
        print(
            "Non-positive Resolution_Time_Hours:",
            (
                support_tickets["Resolution_Time_Hours"] <= 0
            ).sum(),
        )

    print("\nExact duplicate rows:")
    print("Duplicate rows:", support_tickets.duplicated().sum())

    orphan_tickets = support_tickets[
        support_tickets["Customer_ID"].notnull()
        & ~support_tickets["Customer_ID"].isin(customer_ids)
    ]
    print(
        "Tickets without matching customer:",
        len(orphan_tickets),
    )

    customer_signup_dates = customers[
        ["Customer_ID", "Signup_Date"]
    ].copy()

    ticket_validation = support_tickets.merge(
        customer_signup_dates,
        on="Customer_ID",
        how="left",
        suffixes=("", "_Customer"),
    )

    tickets_before_signup = ticket_validation[
        ticket_validation["Ticket_Date"]
        < ticket_validation["Signup_Date"]
    ]
    print(
        "Tickets before Customer Signup_Date:",
        len(tickets_before_signup),
    )

    print("\nSatisfaction Score by Resolution:")
    print(
        support_tickets.groupby("Resolved")[
            "Satisfaction_Score"
        ].describe()
    )

    print("\nSatisfaction Score by Priority:")
    print(
        support_tickets.groupby("Priority")[
            "Satisfaction_Score"
        ].describe()
    )

    print("\nIssue Type vs Resolution:")
    print(
        pd.crosstab(
            support_tickets["Issue_Type"],
            support_tickets["Resolved"],
            dropna=False,
        )
    )

    print("\nResolution Distribution (%):")
    print(
        support_tickets["Resolved"]
        .value_counts(normalize=True, dropna=False)
        .mul(100)
        .round(2)
    )


######   8. DATA DICTIONARY VALIDATION   ######

def validate_data_dictionary(
    data_dictionary: pd.DataFrame,
    customers: pd.DataFrame,
    subscriptions: pd.DataFrame,
    payments: pd.DataFrame,
    customer_services: pd.DataFrame,
    support_tickets: pd.DataFrame,
) -> None:
    """Validate the Data Dictionary against operational tables."""
    print_section("DATA DICTIONARY VALIDATION")

    dictionary = data_dictionary

    print("Number of Rows:", dictionary.shape[0])
    print("Number of Columns:", dictionary.shape[1])

    print("\nColumn Names:")
    print(dictionary.columns.tolist())

    required_dictionary_columns = {
        "Table_Name",
        "Column_Name",
        "Data_Type",
        "Description",
    }
    missing_dictionary_columns = (
        required_dictionary_columns - set(dictionary.columns)
    )

    if missing_dictionary_columns:
        raise ValueError(
            "Data Dictionary is missing required columns: "
            f"{sorted(missing_dictionary_columns)}"
        )

    print("\nTable Name Distribution:")
    print(dictionary["Table_Name"].value_counts(dropna=False))
    print(
        "Missing Table_Name:",
        dictionary["Table_Name"].isnull().sum(),
    )

    print(
        "\nMissing Column_Name:",
        dictionary["Column_Name"].isnull().sum(),
    )

    print("\nColumn Name Distribution:")
    print(dictionary["Column_Name"].value_counts(dropna=False))

    print("\nData Type Distribution:")
    print(dictionary["Data_Type"].value_counts(dropna=False))
    print(
        "Missing Data_Type:",
        dictionary["Data_Type"].isnull().sum(),
    )

    print(
        "\nMissing Description:",
        dictionary["Description"].isnull().sum(),
    )
    print(
        "Blank Description:",
        dictionary["Description"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum(),
    )

    print("\nExact duplicate rows:", dictionary.duplicated().sum())

    duplicate_table_column = dictionary[
        ["Table_Name", "Column_Name"]
    ].duplicated()
    print(
        "Duplicate Table-Column combinations:",
        duplicate_table_column.sum(),
    )

    print("\nRows with Missing Table or Column:")
    print(
        dictionary[
            dictionary["Table_Name"].isnull()
            | dictionary["Column_Name"].isnull()
        ]
    )

    expected_tables = {
        "Customers",
        "Subscriptions",
        "Payments",
        "Customer Services",
        "Support Tickets",
    }

    documented_tables = set(
        dictionary["Table_Name"].dropna().unique()
    )

    print("\nExpected Tables Missing from Dictionary:")
    print(expected_tables - documented_tables)

    print("\nUnexpected Tables in Dictionary:")
    print(documented_tables - expected_tables)

    actual_columns = {
        "Customers": set(customers.columns),
        "Subscriptions": set(subscriptions.columns),
        "Payments": set(payments.columns),
        "Customer Services": set(customer_services.columns),
        "Support Tickets": set(support_tickets.columns),
    }

    missing_documentation = {}
    extra_documentation = {}
    column_comparison = []

    for table, columns in actual_columns.items():
        documented_columns = set(
            dictionary.loc[
                dictionary["Table_Name"] == table,
                "Column_Name",
            ].dropna()
        )

        missing_columns = columns - documented_columns
        extra_columns = documented_columns - columns

        if missing_columns:
            missing_documentation[table] = missing_columns

        if extra_columns:
            extra_documentation[table] = extra_columns

        column_comparison.append(
            {
                "Table": table,
                "Actual_Columns": len(columns),
                "Documented_Columns": len(documented_columns),
                "Missing_Documentation": len(missing_columns),
                "Extra_Documentation": len(extra_columns),
            }
        )

    print("\nMissing Column Documentation:")
    print(missing_documentation)

    print("\nDocumentation for Nonexistent Columns:")
    print(extra_documentation)

    print("\nActual vs Documented Column Comparison:")
    print(pd.DataFrame(column_comparison))

    print("\nUnique Documented Columns per Table:")
    print(
        dictionary.groupby("Table_Name")["Column_Name"].nunique()
    )

    print("\nDocumented Data Types:")
    print(
        dictionary[
            ["Table_Name", "Column_Name", "Data_Type"]
        ]
    )


######   9. MAIN   ######

def main() -> None:
    """Run the complete data validation workflow."""
    data = load_raw_data(FILE_PATH)

    customers = data["customers"]
    subscriptions = data["subscriptions"]
    payments = data["payments"]
    customer_services = data["customer_services"]
    support_tickets = data["support_tickets"]
    data_dictionary = data["data_dictionary"]

    print_section("DATASET DIMENSIONS")
    for name, df in data.items():
        print(f"{name}: {df.shape}")

    print_section("MISSING VALUE ANALYSIS")
    for name, df in data.items():
        print(f"\n--- {name} ---")
        print(missing_value_summary(df))

    print_duplicate_summary(data)

    customer_ids = set(customers["Customer_ID"].dropna())

    validate_customers(customers, customer_ids)
    validate_subscriptions(
        subscriptions,
        customers,
        customer_ids,
    )
    validate_payments(
        payments,
        customers,
        customer_ids,
    )
    validate_customer_services(
        customer_services,
        customers,
        customer_ids,
    )
    validate_support_tickets(
        support_tickets,
        customers,
        customer_ids,
    )
    validate_data_dictionary(
        data_dictionary,
        customers,
        subscriptions,
        payments,
        customer_services,
        support_tickets,
    )

    print_section("DATA VALIDATION COMPLETED")
    print("All validation sections executed successfully.")


if __name__ == "__main__":
    main()
