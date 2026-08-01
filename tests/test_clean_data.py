import pandas as pd
# import pytest
from src.clean_data import calculate_financials

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