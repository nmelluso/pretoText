import pandas as pd


def get_df_from_gsheet(gsheet_id, sheet_name=None):
    """
    Import a *gsheet* by ID as a :class:`DataFrame`.
    
    Args:
        gsheet_id (str): 
            The ID of the *gsheet*.
        sheet_name (str, optional): 
            name of the *sheet* where to take elements from. 
            Defaults to None.
    
    Returns:
        pandas.DataFrame: 
            a :class:`DataFrame` containing all imported data from the *gsheet*.
    """

    export_url = (
        "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv" % gsheet_id
    )

    if sheet_name is not None:
        export_url += "&sheet=%s" % sheet_name

    return pd.read_csv(export_url)
