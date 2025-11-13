# src/nlp_utils.py
import spacy
from spacy.matcher import PhraseMatcher
from pathlib import Path

nlp = spacy.load("en_core_web_sm", disable=["parser"])  # faster

def preprocess_text(text):
    doc = nlp(text)
    tokens = []
    for t in doc:
        if not t.is_stop and not t.is_punct and t.is_alpha:
            tokens.append(t.lemma_.lower())
    return " ".join(tokens)

def build_skill_phrase_matcher(skills_list, attr="LOWER"):
    """
    skills_list: iterable of skill strings
    returns: a PhraseMatcher bound to the nlp pipeline
    """
    matcher = PhraseMatcher(nlp.vocab, attr=attr)
    patterns = [nlp.make_doc(s) for s in skills_list]
    matcher.add("SKILLS", patterns)
    return matcher
