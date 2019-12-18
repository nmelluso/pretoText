from functools import partial
from redtoolkit.scidata import graphs
from redtoolkit.utils import importers
from redtoolkit.utils import parallelism
from redtoolkit.utils import spacy
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


__all__ = ["ranking_by_embeddings_from_gsheet", "ranking_by_embeddings_from_df"]


def ranking_by_embeddings_from_gsheet(
    gsheet_id,
    model=spacy.SPACY_MD,
    parallelisation=parallelism.SOFT,
    column=None,
    sheet_name=None,
    limit=None,
    save_csv=None,
):
    """
    Perform a ranking by distance between each element in the given *gsheet*.
    This distance is calculated by considering the *cosine similarity*.
    If no ``column`` of the *gsheet* is specified, elements are taken from the first one.
    If no ``sheet name`` inside the *gsheet* is specified, only the first one is considered.

    Args:
        gsheet_id (str): 
            The ID of the *gsheet*.
        model (str, optional): 
            The *spaCy* model which to get word embeddings from. Defaults to *spacy_medium*.
        parallelisation (int, optional): 
            The level of parallelisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to parallelism.SOFT.
        column (str, optional): 
            The column of the *gsheet* where to take elements from. 
            Defaults to None.
        sheet_name (str, optional): 
            The name of the *sheet* where to take elements from. 
            Defaults to None.
        limit (int, optional): 
            If specified, only first *limit* elements are ranked. 
            Defaults to None.
        save_csv (str, optional): 
            If specified, the ranking is saved in that CSV file. 
            Defaults to None.

    Returns:
        :class:`pandas.DataFrame`: 
            The first two columns specify the elements compared and the third one has their similarity score.

    """
    return ranking_by_embeddings_from_df(
        importers.get_df_from_gsheet(gsheet_id, sheet_name=sheet_name),
        model=model,
        parallelisation=parallelisation,
        column=column,
        limit=limit,
        save_csv=save_csv,
    )


def ranking_by_embeddings_from_df(
    df,
    model=spacy.SPACY_MD,
    parallelisation=parallelism.SOFT,
    column=None,
    limit=None,
    save_csv=None,
):
    """
    Perform a ranking by distance between each element in the given :class:`pandas.DataFrame`.
    This distance is calculated by considering the *cosine similarity*.
    If no ``column`` of the :class:`pandas.DataFrame` is specified, elements are taken from the first one.

    Args:
        df (pandas.DataFrame):
             The :class:`pandas.DataFrame` which to perform ranking to.
        model (str, optional): 
            The *spaCy* model which to get word embeddings from. 
            Defaults to *spacy_medium*.
        parallelisation (int, optional): 
            The level of parallelisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to parallelism.SOFT.
        column (str, optional): 
            The column of the dataframe where to take elements from. 
            Defaults to None.
        limit (int, optional): 
            If specified, only first *limit* elements are ranked. 
            Defaults to None.
        save_csv (str, optional): 
            If specified, the ranking is saved in that CSV file. 
            Defaults to None.

    Returns:
        :class:`pandas.DataFrame`: 
            The first two columns specify the elements compared and the third one has their similarity score.
    """
    if column is not None:
        df = pd.DataFrame(df[column])

    if limit is not None:
        df = df.head(limit)

    items = [el[1].lower() for el in df.itertuples() if isinstance(el[1], str)]

    nlp = spacy.load_model(model)

    texts = []
    vecs = []

    for item in nlp.pipe(items):
        texts.append(item.text)
        vecs.append(item.vector)

    # working on sparse matrixes is WAY faster
    # than performing similarity on single pairs
    # even if on multiprocessing
    a_sparse = sparse.csr_matrix(np.array(vecs))
    similarities_sparse = cosine_similarity(a_sparse, dense_output=True)
    df = pd.DataFrame(similarities_sparse, index=texts, columns=texts)
    adj_df = graphs.convert_df_to_adjacency_df(df)

    adj_df.sort_values(by="w", ascending=False, inplace=True)

    if save_csv:
        adj_df.to_csv(save_csv)

    return adj_df
