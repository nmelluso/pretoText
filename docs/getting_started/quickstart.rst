Quickstart
==========

Examples from inside a project
------------------------------

::

    from pretoText.textanalysis import similarities

    df_sim_wn = similarities.wordnet.ranking_by_wordnet_from_gsheet(
        gsheet_id,
        parallelisation=2,
        sorting=True,
        column="a_column",
        sheet_name="a_sheet_name"
    )


Examples from a CLI
-------------------

If using pipenv, ``pipenv run`` must precede the command or ``pipenv shell`` must be called in order to activate the environment.

::

    python pretoText ranking_by_wordnet_from_gsheet gsheet_id --parallelisation=2 --sorting=True --column=a_column --sheet_name=a_sheet_name