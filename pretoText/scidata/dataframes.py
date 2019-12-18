from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import sklearn


__all__ = [
    "column_vertical_shift",
    "sparse_matrix_from_text",
    "spread_col",
    "target_column",
    "target_values_vec",
]


def column_vertical_shift(df, col_name, shift_len, absolute_value=False):
    """
    Adds a column to the :class:`pandas.DataFrame` which is an old one shifted by a signed shift forward or backward,
    if the absolute value parameter is set to True the new column is the sum of the shift backward and
    forward of length ``shift_len`` where all nonzero values are replaced by the value one.
    
    Args:
        df (pandas.DataFrame): 
            Source :class:`pandas.DataFrame` to modify.
        col_name (str): 
            Name of the column to shift.
        shift_len (int): 
            Length of the shift.
        absolute_value (bool, optional): 
            If set to True acts as in the description.
            Defaults to False.

    .. highlight:: python
    .. code-block:: python

        >>> test_df = pandas.DataFrame(list(range(6)), columns=['col']) 
        >>> test_df
        ====  =====
          ..    col
        ====  =====
           0      0
           1      1
           2      2
           3      3
           4      4
           5      5
           6      6
        ====  =====

        >>> column_vertical_shift(test_df, 'col', 2)
        >>> test_df
        ====  =====  =======
          ..    col    col_2
        ====  =====  =======
           0      0        2
           1      1        3
           2      2        4
           3      3        5
           4      4        0
           5      5        0     
        ====  =====  =======

    """
    bool_to_float = df[col_name]
    shifted = bool_to_float.shift(periods=-shift_len, fill_value=0.0)
    if not absolute_value:
        df[col_name + "_" + str(shift_len)] = shifted
    else:
        oppos_shifted = bool_to_float.shift(periods=shift_len, fill_value=0.0)
        abs_shifted = shifted.add(oppos_shifted)
        df[col_name + "_abs_" + str(abs(shift_len))] = abs_shifted.replace(2.0, 1.0)


# TODO - move to its right functional module
def sparse_matrix_from_text(doc_list):
    """
    Turns an input list of strings, into a bag of words representation stored in a sparse matrix.
    
    Args:
        doc_list (list): 
            list of strings.
    
    Returns:
        tuple: 
            A pair composed by ``scipy.sparse.csr_matrix`` in the first entry and a ``sklearn.CountVectorizer`` in the second one.
    """
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(doc_list)

    return X, vectorizer


def spread_col(df, col_name):
    """
    Adds a number of columns equal to the number of unique values in the ``col_name`` column.
    Each of these new columns has a ``1`` if the same row has that value in ``col_name`` and a ``0`` otherwise.

    Args:
        df (pandas.DataFrame): 
            Source :class:`pandas.DataFrame` to work with.
        col_name (str): 
            Name of the column to spread.
    
    Returns:
        pandas.DataFrame: 
            Spreaded :class:`pandas.DataFrame`.

    .. highlight:: python
    .. code-block:: python

        >>> test_df = pandas.DataFrame(["si", "no", "si", "no", "si", "si"], columns=['col'])
        >>> test_df
        ====  =====
          ..  col  
        ====  =====
           0  si   
           1  no   
           2  si   
           3  no   
           4  si   
           5  si   
        ====  =====

        >>> test_df = spread_col(test_df)
        >>> test_df
        ====  =====  ====  ====
          ..  col      no    si
        ====  =====  ====  ====
           0  si        0     1
           1  no        1     0
           2  si        0     1
           3  no        1     0
           4  si        0     1
           5  si        0     1
        ====  =====  ====  ====

    """
    df[col_name] = pd.Categorical(df[col_name])
    df_dummies = pd.get_dummies(df[col_name], dtype="float64")
    output = pd.concat([df, df_dummies], axis=1)
    return output


def target_column(df, col_name, targets):
    """
    Creates a new column named ``target``, where at its *n-th* position there is a ``1`` in case a
    value from ``targets`` is present at the *n-th* position of the column specified, ``0`` otherwise.
    
    Args:
        df (pandas.DataFrame): 
            Source :class:`pandas.DataFrame` to add the column to.
        col_name (str): 
            Name of the column to parse.
        targets (list): 
            List of target values that can match.
    
    .. highlight:: python
    .. code-block:: python

        >>> test_df=pd.DataFrame(
            [["word"+str(i),"number"+str(i)]for i in range(5)],
            columns=["word","number"])
        >>> test_df
        ====  ======  ========
          ..  word    number
        ====  ======  ========
           0  word0   number0
           1  word1   number1
           2  word2   number2
           3  word3   number3
           4  word4   number4
        ====  ======  ========
        >>> target_column(test_df,"word",["word1","word2"])
        >>> test_df
        ====  ======  ========  ========
          ..  word    number      target
        ====  ======  ========  ========
           0  word0   number0          0
           1  word1   number1          1
           2  word2   number2          0
           3  word3   number3          0
           4  word4   number4          1
        ====  ======  ========  ========
        
    """
    target_col = [int(i in targets) for i in df[col_name]]
    df["target"] = pd.Series(target_col)


def target_values_vec(doc_list, targets):
    """
    Given an iterable of strings returns a ``numpy.array`` of the same length as the input one,
    where at the n-th position there is a one in case a word from target is present
    in the n-th element of the iterable and zero otherwise.
    
    Args:
        doc_list (iterable): 
            Iterable of strings.
        targets (list): 
            List of the words that generate a one in the output.
    
    Returns:
        ``numpy.array``: 
            Array built as in the description.
    """

    if not isinstance(targets, list):
        raise ValueError("Targets must be a list")

    test_presence = lambda x: len(set(targets).intersection(x.split(" "))) > 0
    target = np.array([int(is_target) for is_target in map(test_presence, doc_list)])

    return target
