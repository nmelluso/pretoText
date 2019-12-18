from nltk.corpus import wordnet as wn


# POS Tagging


def any2wnpos(postag):
    """
    Convert *Universal POS tags* or *Penn Treebank POS tags* to *WordNet POS tags* format.
    If the given POS tag is a *WordNet POS tag*, it is returned as is.
    If the given POS tag is unsupported, ``NIL`` is returned.
    
    Args:
        postag (str): 
            *Universal POS tag* or *Penn Treebank POS tag* to convert.
    
    Returns:
        str: 
            *WordNet POS tag*, or ``NIL`` if unsupported.
    """
    if postag in [wn.ADJ, wn.ADV, wn.NOUN, wn.VERB]:
        return postag

    convert_table = {
        "ADJ": wn.ADJ,
        "ADV": wn.ADV,
        "AUX": wn.VERB,
        "NOUN": wn.NOUN,
        "PRON": wn.NOUN,
        "PROPN": wn.NOUN,
        "VERB": wn.VERB,
        "AFX": wn.ADJ,
        "BES": wn.VERB,
        "EX": wn.ADV,
        "HVS": wn.VERB,
        "JJ": wn.ADJ,
        "JJR": wn.ADJ,
        "JJS": wn.ADJ,
        "MD": wn.VERB,
        "NN": wn.NOUN,
        "NNP": wn.NOUN,
        "NNPS": wn.NOUN,
        "NNS": wn.NOUN,
        "PDT": wn.ADJ,
        "PRP$": wn.ADJ,
        "RB": wn.ADV,
        "RBR": wn.ADV,
        "RBS": wn.ADV,
        "VB": wn.VERB,
        "VBD": wn.VERB,
        "VBG": wn.VERB,
        "VBN": wn.VERB,
        "VBP": wn.VERB,
        "VBZ": wn.VERB,
        "WDT": wn.ADJ,
        "WP": wn.NOUN,
        "WP$": wn.ADJ,
        "WRB": wn.ADV,
    }

    return _safe_convert_pos(postag, convert_table)


def penn2unipos(postag):
    """
    Convert *Penn Treebank POS tags* to *Universal POS tags* format.
    If the given POS tag is unsupported, ``NIL`` is returned.
    
    Args:
        postag (str): 
            *Penn Treebank POS tag* to convert.
    
    Returns:
        str: 
            *Universal POS tag*, or ``NIL`` if unsupported.
    """
    convert_table = {
        "-LRB-": "PUNCT",
        "-RRB-": "PUNCT",
        ",": "PUNCT",
        ":": "PUNCT",
        ".": "PUNCT",
        "''": "PUNCT",
        '""': "PUNCT",
        "``": "PUNCT",
        "#": "SYM",
        "$": "SYM",
        "ADD": "X",
        "AFX": "ADJ",
        "BES": "VERB",
        "CC": "CONJ",
        "CD": "NUM",
        "DT": "DET",
        "EX": "ADV",
        "FW": "X",
        "GW": "X",
        "HVS": "VERB",
        "HYPH": "PUNCT",
        "IN": "ADP",
        "JJ": "ADJ",
        "JJR": "ADJ",
        "JJS": "ADJ",
        "LS": "PUNCT",
        "MD": "VERB",
        "NFP": "PUNCT",
        "NN": "NOUN",
        "NNP": "PROPN",
        "NNPS": "PROPN",
        "NNS": "NOUN",
        "PDT": "ADJ",
        "POS": "PART",
        "PRP": "PRON",
        "PRP$": "ADJ",
        "RB": "ADV",
        "RBR": "ADV",
        "RBS": "ADV",
        "RP": "PART",
        "_SP": "SPACE",
        "SYM": "SYM",
        "TO": "PART",
        "UH": "INTJ",
        "VB": "VERB",
        "VBD": "VERB",
        "VBG": "VERB",
        "VBN": "VERB",
        "VBP": "VERB",
        "VBZ": "VERB",
        "WDT": "ADJ",
        "WP": "NOUN",
        "WP$": "ADJ",
        "WRB": "ADV",
        "XX": "X",
    }
    return _safe_convert_pos(postag, convert_table)


def _safe_convert_pos(postag, convert_table):
    try:
        return convert_table[postag]
    except KeyError:
        return "NIL"
