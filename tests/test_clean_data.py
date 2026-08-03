import pandas as pd


from src.clean_data import calculate_financials, remove_exact_duplicates

def test_calculate_financials():

    input_data = pd.DataFrame(
        {
            "Quantity":[2],
            "Unit Price": [10.0],
            "Unit Cost":[6.0]
        }
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