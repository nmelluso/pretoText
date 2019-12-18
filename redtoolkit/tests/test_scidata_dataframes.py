from redtoolkit.scidata import dataframes
import numpy as np
import pandas as pd
import spacy


sentences = [
    "there are many target",
    "targets are what we investigate",
    "dogs are animals",
    "the number of bees on earth is 74",
    "",
    "sometimes a string is empty and therefore not a target",
    "there are also weird symbols @@",
]


names1 = ["word1", "word2", "word3", "word4", "word5", "word6", "word7"]
names2 = [1, 2, 3, 4, 5, 6, 7]
test_df = pd.DataFrame(
    list(zip(names1, names2, sentences)), columns=["col1", "col2", "sentences"]
)


def test_column_vertical_shift():

    df = test_df.copy()
    dataframes.column_vertical_shift(df, "col2", 3)

    assert list(df["col2_3"]) == [4, 5, 6, 7, 0, 0, 0]


def test_sparse_matrix_from_text():

    test_text = [
        "this sentence is red",
        "sentence is this blue",
        "this is sentence yellow",
    ]
    sent_to_transform = "this sentence is green"
    test_sparse = dataframes.sparse_matrix_from_text(test_text)

    assert (
        (test_sparse[0][1, :].todense() == np.array([1, 1, 0, 1, 1, 0])).all() == True
        and (
            test_sparse[1].transform([sent_to_transform]).todense()
            == np.array([0, 1, 0, 1, 1, 0])
        ).all()
        == True
    )


def test_spread_col():

    df = test_df.copy()
    spread_df = dataframes.spread_col(df, "col1")

    assert list(spread_df["word4"]) == [0, 0, 0, 1, 0, 0, 0]


def test_target_column():

    df = test_df.copy()
    dataframes.target_column(df, "col1", ["word2", "word4"])

    assert list(df["target"]) == [0, 1, 0, 1, 0, 0, 0]


def test_target_values_vec():

    df = test_df.copy()
    target_values = dataframes.target_values_vec(df["sentences"], ["target"])

    assert list(target_values) == [1, 0, 0, 0, 0, 1, 0]
