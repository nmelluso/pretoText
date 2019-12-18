from spacy import load
import subprocess

SPACY_SM = "spacy_small"
_SPACY_SM = "en_core_web_sm"

SPACY_MD = "spacy_medium"
_SPACY_MD = "en_core_web_md"

SPACY_LG = "spacy_large"
_SPACY_LG = "en_core_web_lg"

SPACY_VECS = "spacy_vectors"
_SPACY_VECS = "en_vectors_web_lg"

FASTTEXT = "fasttext"
_FASTTEXT = "en_ft_cc_300"


def load_model(model=SPACY_MD, disable=None):
    kwargs = {"name": _get_real_model(model)}
    if disable:
        kwargs["disable"] = disable
    return load(**kwargs)


# CLI


def download_model(model=SPACY_MD):
    if model == FASTTEXT:
        command = (
            "wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.vec.gz &&"
            "python -m spacy init-model en en_ft_cc_300 --vectors-loc cc.en.300.vec.gz"
        )
    else:
        command = "python -m spacy download %s" % _get_real_model(model)

    subprocess.check_call(command, shell=True)


# Private


def _get_real_model(model):
    if model == SPACY_SM:
        return _SPACY_SM
    elif model == SPACY_MD:
        return _SPACY_MD
    elif model == SPACY_LG:
        return _SPACY_LG
    elif model == FASTTEXT:
        return _FASTTEXT
    else:
        raise AttributeException("Invalid model for spaCy")
