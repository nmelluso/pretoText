from redtoolkit.scidata import graphs
import pandas as pd


def test_adjacency_graphs():

    test_data = [
        {"name": "val1", "val1": 0, "val2": 1, "val3": 1},
        {"name": "val2", "val1": 1, "val2": 0, "val3": 2},
        {"name": "val3", "val1": 1, "val2": 2, "val3": 0},
    ]

    expected_data = [
        {"a": "val1", "b": "val2", "w": 1},
        {"a": "val1", "b": "val3", "w": 1},
        {"a": "val2", "b": "val3", "w": 2},
    ]

    test_df = pd.DataFrame.from_records(test_data, index=["name"])
    expected_df = pd.DataFrame.from_records(expected_data)
    assert graphs.convert_df_to_adjacency_df(test_df).equals(expected_df)
