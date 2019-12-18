from redtoolkit.textanalysis import extractors
from redtoolkit.utils import spacy
from spacy.pipeline import EntityRuler
import os


nlp = spacy.load_model(spacy.SPACY_SM)


def extract_functional_verbs(text):
    nlp.add_pipe(
        EntityRuler(nlp).from_disk(
            "%s/resources/functional.jsonl" % os.path.dirname(extractors.__file__)
        )
    )
    return [ent.text for ent in nlp(text).ents if ent.label_ == "FUNCTIONAL"]


def extract_soft_skills(text):
    nlp.add_pipe(
        EntityRuler(nlp).from_disk(
            "%s/resources/soft_skill.jsonl" % os.path.dirname(extractors.__file__)
        )
    )
    return [ent.text for ent in nlp(text).ents if ent.label_ == "SOFT SKILL"]
