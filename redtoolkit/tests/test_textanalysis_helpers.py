from nltk.corpus import wordnet as wn
from redtoolkit.textanalysis.helpers import converter
from redtoolkit.textanalysis.helpers import despacy
from redtoolkit.textanalysis.helpers import splitter
from redtoolkit.utils import spacy


def test_converter_any2wnpos():
    convert_table = {
        # WordNet POS tags
        wn.ADJ: wn.ADJ,
        wn.ADV: wn.ADV,
        wn.NOUN: wn.NOUN,
        wn.VERB: wn.VERB,
        # Universal POS tags
        "ADJ": wn.ADJ,
        "ADV": wn.ADV,
        "AUX": wn.VERB,
        "NOUN": wn.NOUN,
        "PRON": wn.NOUN,
        "PROPN": wn.NOUN,
        "VERB": wn.VERB,
        # Penn Treebank POS tags
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

    for anypos, wnpos in convert_table.items():
        assert converter.any2wnpos(anypos) == wnpos
    assert converter.any2wnpos("NOT A POS") == "NIL"


def test_converter_penn2unipos():
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
    for pennpos, unipos in convert_table.items():
        assert converter.penn2unipos(pennpos) == unipos
    assert converter.penn2unipos("NOT A POS") == "NIL"


nlp = spacy.load_model(spacy.SPACY_SM)


def test_despacy_get_attributes_as_dict():
    sample_doc = nlp("This is a sample sentence")
    for token in sample_doc:
        assert despacy.get_attributes_as_dict(token, ["text", "pos_", "tag_"]) == {
            "text": token.text,
            "pos_": token.pos_,
            "tag_": token.tag_,
        }


despacy_sample_doc_1 = nlp(
    " this is a tEst sent#ence \n\n used to verify the Function spacy_to_sent"
)


def test_despacy_get_clean_text():
    assert (
        despacy.get_clean_text(despacy_sample_doc_1)
        == "this is a test used to verify the function"
    )


def test_despacy_get_clean_text_filtered_by_pos():
    valid_postags = ["NOUN", "VERB", "PROPN"]
    clean_text_filtered = despacy.get_clean_text_filtered_by_pos(
        despacy_sample_doc_1, valid_postags
    )
    assert clean_text_filtered == "is test used verify function"


def test_despacy_get_clean_text_filtered_by_attributions():
    valid_postags = ["NOUN", "VERB", "PROPN"]
    not_valid_words = ["verify"]
    attributions = {"!text": not_valid_words, "pos_": valid_postags}
    clean_text_filtered = despacy.get_clean_text_filtered_by_attributions(
        despacy_sample_doc_1, attributions
    )
    assert clean_text_filtered == "is test used function"


def test_get_docs_clean_sentences_as_tuples():

    test_text_to_show_1 = """We can for example examine this small text, composed of long enough sentences. Where some important words are present, even though some word to ignore are present too and we will see how they are not considered. """

    test_text_to_show_2 = """We can also look at too short sentences. Or at sentences where a forbidden word is present so that they will be ignored even if long enough."""

    test_doc_to_show = [nlp(test_text_to_show_1), nlp(test_text_to_show_2)]

    sentences_tuples = despacy.get_docs_clean_sentences_as_tuples(
        test_doc_to_show,
        relevant_tags=["NOUN", "VERB"],
        word="forbidden",
        blacklist="ignore",
        min_length=10,
    )

    assert sentences_tuples == [
        (
            "we can for example examine this small text composed of long enough sentences",
            "can example examine text composed sentences",
        ),
        (
            "where some important words are present even though some word to ignore are present too and we will see how they are not considered",
            "words are word are will see are considered",
        ),
        ("we can also look at too short sentences", "can look sentences"),
    ]
