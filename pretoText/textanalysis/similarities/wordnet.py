from collections import defaultdict
from functools import partial
from nltk.corpus import wordnet as wn
from redtoolkit.scidata import graphs
from redtoolkit.utils import importers
from redtoolkit.utils import parallelism
import pandas as pd
import re


__all__ = ["ranking_by_wordnet_from_gsheet", "ranking_by_wordnet_from_df"]


def ranking_by_wordnet_from_gsheet(
    gsheet_id,
    parallelisation=parallelism.SOFT,
    column=None,
    sheet_name=None,
    limit=None,
    save_csv=None,
):
    """
    Perform a ranking by distance between each element in the given *gsheet*.
    This distance is calculated by considering the number of common synonyms taken from *WordNet*.
    If no ``column`` of the gsheet is specified, elements are taken from the first one.
    If no ``sheet name`` inside the gsheet is specified, only the first one is considered.

    Args:
        gsheet_id (str): 
            The ID of the *gsheet*.
        parallelisation (int, optional): 
            The level of parallelisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to parallelism.SOFT.
        column (str, optional): 
            The column of the gsheet where to take elements from. 
            Defaults to None.
        sheet_name (str, optional): 
            The name of the sheet where to take elements from. 
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
    return ranking_by_wordnet_from_df(
        importers.get_df_from_gsheet(gsheet_id, sheet_name=sheet_name),
        parallelisation=parallelisation,
        column=column,
        limit=limit,
        save_csv=save_csv,
    )


def ranking_by_wordnet_from_df(
    df, parallelisation=parallelism.SOFT, column=None, limit=None, save_csv=None
):
    """
    Perform a ranking by distance between each element in the given :class:`pandas.DataFrame`.
    This distance is calculated by considering the number of common synonyms taken from *WordNet*.
    If no ``column`` of the gsheet is specified, elements are taken from the first one.
    If no ``sheet name`` inside the gsheet is specified, only the first one is considered.

    Args:
        df (pandas.DataFrame): 
            The :class:`pandas.DataFrame` which to perform ranking to.
        parallelisation (int, optional): 
            The level of parallelisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to parallelism.SOFT.
        column (str, optional): 
            The column of the :class:`pandas.DataFrame` where to take elements from. 
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

    items = [r[1].lower() for r in df.itertuples()]

    if parallelisation == parallelism.WorkerLevel.HARD:
        # force wordnet to be loaded for multiprocessing
        wn.ensure_loaded()

    task = partial(_iteration_task, items=items)
    results = parallelism.perform_job(items, task, level=parallelisation)

    df = graphs.convert_df_to_adjacency_df(pd.concat(results, sort=True))

    df.sort_values(by="w", ascending=False, inplace=True)

    if save_csv:
        df.to_csv(save_csv)

    return df


def _iteration_task(item, items):

    a_syns = []

    for word in re.split(r" ", item.lower()):
        try:
            syns = wn.synsets(word)
        except:
            continue

        a_syns.append(set(syns))

    row = defaultdict(int)
    for b in items:

        if b == item:
            continue

        row[b] = 0

        for syns in a_syns:
            for word in re.split(r" ", b.lower()):
                try:
                    b_syns = wn.synsets(word)
                except:
                    continue

                row[b] += len(syns.intersection(set(b_syns)))

    return pd.DataFrame(row, index=[item])
