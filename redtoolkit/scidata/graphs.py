import networkx as nx
import pandas as pd


__all__ = [
    "convert_df_to_graph",
    "convert_adjacency_graph_to_df",
    "convert_df_to_adjacency_df",
]


def convert_df_to_graph(df, asymmetric=False):
    """
    Turn a :class:`pandas.DataFrame` into a :class:`networkx.Graph`.
    
    Args:
        df (pandas.DataFrame): 
            The :class:`DataFrame` to build the graph from.
        asymmetric (bool, optional): 
            Determines whether the output is a symmetric or asymmetric one. 
            Defaults to False.
    
    Returns:
        networkx.Graph: 
            The :class:`Graph` inferred from the :class:`DataFrame`.
    """
    return (nx.DiGraph if asymmetric else nx.Graph)(df)


def convert_adjacency_graph_to_df(graph):
    """
    Turn a :class:`networkx.Graph` into a :class:`pandas.DataFrame` where the first
    two columns hold all the nodes, and the third one the weight of the graph.
    
    Args:
        graph (networkx.Graph): 
            The :class:`Graph` to derive the :class:`pandas.DataFrame` from.
    
    Returns:
        pandas.DataFrame: 
            The :class:`DataFrame` as described in the function with columns = ["a", "b", "w"]
    """
    return pd.DataFrame(
        [[a, b, data["weight"]] for a, b, data in graph.edges(data=True)],
        columns=["a", "b", "w"],
    )


def convert_df_to_adjacency_df(df, asymmetric=False):
    """
    Turns a :class:`pandas.DataFrame` holding pairs of elements into one representing an adjacency matrix.
    
    Args:
        df (pandas.DataFrame): 
            The :class:`DataFrame` of pairs to work with.
        asymmetric (bool, optional): 
            The type of adjacency matrix to infer. 
            Defaults to False.
    
    Returns:
        pandas.DataFrame: 
            The adjacency :class:`DataFrame`.
    """
    return convert_adjacency_graph_to_df(convert_df_to_graph(df, asymmetric))
