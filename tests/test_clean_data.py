import pandas as pd


from src.clean_data import (
    calculate_financials,
    load_data,
    normalize_customer_names,
    normalize_region_and_category,
    normalize_emails,
    reject_missing_quantities,
    remove_exact_duplicates,
)


def test_calculate_financials():

    input_data = pd.DataFrame(
        {"Quantity": [2], "Unit Price": [10.0], "Unit Cost": [6.0]}
    )

    result = calculate_financials(input_data)

    assert result.loc[0, "Revenue"] == 20.0
    assert result.loc[0, "Total Cost"] == 12.0
    assert result.loc[0, "Profit"] == 8.0


def test_remove_exact_duplicates():
    input_data = pd.DataFrame(
        {
            "Order ID": ["ORD-001", "ORD-001", "ORD-002"],
            "Product": ["Laptop", "Laptop", "Mouse"],
        }
    )

    cleaned_data, duplicate_count = remove_exact_duplicates(input_data)

    assert duplicate_count == 1
    assert len(cleaned_data) == 2

    assert cleaned_data["Order ID"].tolist() == ["ORD-001", "ORD-002"]


def test_load_data(tmp_path):
    expected_data = pd.DataFrame(
        {
            "Order ID": ["ORD-001", "ORD-002"],
            "Quantity": [2, 3],
        }
    )
    csv_path = tmp_path / "sample.csv"

    expected_data.to_csv(csv_path, index=False)
    actual_data = load_data(csv_path)

    pd.testing.assert_frame_equal(actual_data, expected_data)


def test_reject_missing_quantities():
    input_data = pd.DataFrame(
        {
            "Order ID": ["ORD-001", "ORD-002"],
            "Quantity": [2, None],
        }
    )

    accepted_data, rejected_data = reject_missing_quantities(input_data)

    assert accepted_data["Order ID"].tolist() == ["ORD-001"]
    assert rejected_data["Order ID"].tolist() == ["ORD-002"]
    assert rejected_data["Rejection Reason"].tolist() == ["Missing Quantity"]


def test_normalize_emails():
    input_data = pd.DataFrame(
        {
            "Email": [
                "  ARZU@EXAMPLE.COM  ",
                "user@example.com",
                None,
            ]
        }
    )

    result, changed_count = normalize_emails(input_data)

    assert result["Email"].tolist() == [
        "arzu@example.com",
        "user@example.com",
        None,
    ]
    assert changed_count == 1


def test_normalize_customer_names():
    input_data = pd.DataFrame(
        {
            "Customer Name": [
                "  aRZu asGarov  ",
                "John Smith",
                None,
            ]
        }
    )

    result, changed_count = normalize_customer_names(input_data)

    assert result["Customer Name"].tolist() == [
        "Arzu Asgarov",
        "John Smith",
        None,
    ]
    assert changed_count == 1
