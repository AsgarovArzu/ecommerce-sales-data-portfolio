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


def reject_missing_quantities(data):
    result = data.copy()
    rejected_data = result.loc[result["Quantity"].isna()].copy()
    rejected_data["Rejection Reason"] = "Missing Quantity"
    accepted_data = result.loc[result["Quantity"].notna()].copy()
    return accepted_data, rejected_data


def normalize_emails(data):
    result = data.copy()

    changed_count = (
        result["Email"].notna()
        & (result["Email"] != result["Email"].str.strip().str.lower())
    ).sum()

    result["Email"] = result["Email"].str.strip().str.lower()

    return result, changed_count


def normalize_customer_names(data):
    result = data.copy()

    changed_count = (
        result["Customer Name"].notna()
        & (result["Customer Name"] != result["Customer Name"].str.strip().str.title())
    ).sum()

    result["Customer Name"] = result["Customer Name"].str.strip().str.title()

    return result, changed_count


def calculate_financials(data):
    result = data.copy()

    result["Revenue"] = (result["Quantity"] * result["Unit Price"]).round(2)

    result["Total Cost"] = (result["Quantity"] * result["Unit Cost"]).round(2)

    result["Profit"] = (result["Revenue"] - result["Total Cost"]).round(2)

    return result


def main():
    file_path = project_root / "data" / "raw_ecommerce_sales.csv"
    df = load_data(file_path)
    missing_values = df.isna().sum()

    clean_df = df.copy()
    clean_df["Order Date"] = pd.to_datetime(
        clean_df["Order Date"],
        errors="coerce",
    )
    invalid_dates = clean_df["Order Date"].isna().sum()
    clean_df, exact_duplicate_count = remove_exact_duplicates(clean_df)
    remaining_duplicate_ids = clean_df.duplicated(subset=["Order ID"]).sum()

    clean_df["Region"] = clean_df["Region"].str.strip().str.title()
    clean_df["Category"] = clean_df["Category"].str.strip()

    clean_df, email_needs_cleaning = normalize_emails(clean_df)

    remaining_email_issues = (
        clean_df["Email"].notna()
        & (clean_df["Email"] != clean_df["Email"].str.strip().str.lower())
    ).sum()

    clean_df, rejected_df = reject_missing_quantities(clean_df)

    non_integer_quantities = (clean_df["Quantity"] % 1 != 0).sum()
    clean_df["Quantity"] = clean_df["Quantity"].astype("int64")

    clean_df, customer_name_needs_cleaning = normalize_customer_names(clean_df)

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
    cost_above_price = (clean_df["Unit Cost"] > clean_df["Unit Price"]).sum()

    assert invalid_dates == 0
    assert remaining_duplicate_ids == 0
    assert remaining_email_issues == 0
    assert non_integer_quantities == 0
    assert remaining_customer_name_issues == 0
    assert invalid_quantities == 0
    assert invalid_unit_prices == 0
    assert invalid_unit_costs == 0
    assert cost_above_price == 0

    clean_df = calculate_financials(clean_df)

    input_row_count = len(df)
    accounted_row_count = len(clean_df) + len(rejected_df) + exact_duplicate_count
    rows_reconciled = input_row_count == accounted_row_count
    assert rows_reconciled

    quality_report = {
        "Input rows": input_row_count,
        "Exact duplicates removed": exact_duplicate_count,
        "Missing emails found": int(missing_values["Email"]),
        "Missing quantities rejected": len(rejected_df),
        "Emails normalized": int(email_needs_cleaning),
        "Customer names normalized": int(customer_name_needs_cleaning),
        "Accepted rows": len(clean_df),
        "Accounted rows": accounted_row_count,
        "Rows reconciled": rows_reconciled,
    }

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

    saved_clean_df = pd.read_csv(clean_output_path)
    saved_rejected_df = pd.read_csv(rejected_output_path)

    assert len(saved_clean_df) == len(clean_df)
    assert len(saved_rejected_df) == len(rejected_df)
    assert saved_clean_df["Order ID"].duplicated().sum() == 0

    print("\nData quality summary:")
    for metric, value in quality_report.items():
        print(f"- {metric}: {value}")

    print("\nOutput validation passed.")


if __name__ == "__main__":
    main()
