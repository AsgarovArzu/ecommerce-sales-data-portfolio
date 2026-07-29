from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parent.parent

def load_data(csv_path):
    data = pd.read_csv(csv_path)
    return data

def remove_exact_duplicates(data):
    duplicate_count = data.duplicated().sum()
    cleaned_data = data.drop_duplicates().copy()

    return cleaned_data, duplicate_count

def calculate_financials(data):
    result = data.copy()

    result["Revenue"] = (
        result["Quantity"] * result["Unit Price"]
    ).round(2)

    result["Total Cost"] = (
        result["Quantity"] * result["Unit Cost"]
    ).round(2)

    result["Profit"] = (
        result["Revenue"] - result["Total Cost"]
    ).round(2)

    return result


file_path = project_root / "data" / "raw_ecommerce_sales.csv"
df = load_data(file_path)

duplicate_count = df.duplicated(subset=["Order ID"]).sum()

clean_df = df.copy()
clean_df["Order Date"] = pd.to_datetime(
    clean_df["Order Date"],
    errors="coerce"
)

# print(df.head())
# print("\nDataset dimensions:")
# print(df.shape)
# print("\nColumn names:")
# print(df.columns.tolist())


# print("\nDuplicate Order IDs:")
# print(duplicate_count)

missing_values = df.isna().sum()

# print("\nMissing values by column:")
# print(missing_values)


missing_email_rows = df.loc[
    df["Email"].isna(),
    ["Order ID", "Customer Name", "Email"]
]

missing_quantity_rows = df.loc[
    df["Quantity"].isna(),
    ["Order ID", "Product", "Quantity", "Unit Price"]
]

invalid_dates = clean_df["Order Date"].isna().sum()


duplicate_rows = clean_df.loc[
    clean_df.duplicated(subset=["Order ID"], keep=False)
].sort_values("Order ID")



clean_df, exact_duplicate_count = remove_exact_duplicates(clean_df)


remaining_duplicate_ids = clean_df.duplicated(
    subset=["Order ID"]
).sum()


clean_df["Region"] = (
    clean_df["Region"]
    .str.strip()
    .str.title()
)

clean_df["Category"] = clean_df["Category"].str.strip()


email_needs_cleaning = (
    clean_df["Email"].notna()
    & (
        clean_df["Email"]
        != clean_df["Email"].str.strip().str.lower()
    )
).sum()


clean_df["Email"] = (
    clean_df["Email"]
    .str.strip()
    .str.lower()
)

remaining_email_issues = (
    clean_df["Email"].notna()
    & (
        clean_df["Email"]
        != clean_df["Email"].str.strip().str.lower()
    )
).sum()


rejected_df = clean_df.loc[
    clean_df["Quantity"].isna()
].copy()

rejected_df["Rejection Reason"] = "Missing Quantity"

clean_df = clean_df.loc[
    clean_df["Quantity"].notna()
].copy()


non_integer_quantities = (
    clean_df["Quantity"] % 1 != 0
).sum()


clean_df["Quantity"] = clean_df["Quantity"].astype("int64")


customer_name_needs_cleaning = (
    clean_df["Customer Name"].notna()
    & (
        clean_df["Customer Name"]
        != clean_df["Customer Name"].str.strip().str.title()
    )
).sum()



clean_df["Customer Name"] = (
    clean_df["Customer Name"]
    .str.strip()
    .str.title()
)

remaining_customer_name_issues = (
    clean_df["Customer Name"].notna()
    & (
        clean_df["Customer Name"]
        != clean_df["Customer Name"].str.strip().str.title()
    )
).sum() 


invalid_quantities = (clean_df["Quantity"] <= 0).sum()



invalid_unit_prices = (clean_df["Unit Price"] <= 0).sum()


invalid_unit_costs = (clean_df["Unit Cost"] < 0).sum()

cost_above_price = (
    clean_df["Unit Cost"] > clean_df["Unit Price"]
).sum()

clean_df = calculate_financials(clean_df)

input_row_count = len(df)

accounted_row_count = (
    len(clean_df)
    + len(rejected_df)
    + exact_duplicate_count
)

rows_reconciled = input_row_count == accounted_row_count

# print("\nInput rows:")
# print(input_row_count)

# print("\nAccounted rows:")
# print(accounted_row_count)

# print("\nRows reconciled:")
# print(rows_reconciled)

output_dir = project_root / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

clean_output_path = output_dir / "clean_ecommerce_sales.csv"
rejected_output_path = output_dir / "rejected_records.csv"

clean_df.to_csv(
    clean_output_path,
    index=False,
    date_format="%Y-%m-%d",
)

rejected_df.to_csv(
    rejected_output_path,
    index=False,
    date_format="%Y-%m-%d",
)
# print("\nFiles created:")
# print(clean_output_path)
# print(rejected_output_path)

saved_clean_df = pd.read_csv(clean_output_path)
saved_rejected_df = pd.read_csv(rejected_output_path)

assert len(saved_clean_df) == len(clean_df)
assert len(saved_rejected_df) == len(rejected_df)
assert saved_clean_df["Order ID"].duplicated().sum() == 0

print("\nOutput validation passed.")