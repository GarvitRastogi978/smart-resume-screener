# src/matcher.py
from src.nlp_utils import nlp, build_skill_phrase_matcher
from rapidfuzz import fuzz, process

def extract_skills_with_matcher(text, matcher, skills_list):
    """
    Returns matched skills (set) using spaCy PhraseMatcher.
    Also uses fuzzy fallback for single tokens.
    """
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        span = doc[start:end].text.strip()
        found.add(span.lower())
    # Normalize using skills_list canonical lowercases
    skills_map = {s.lower(): s for s in skills_list}
    canonical_found = {skills_map.get(s, s) for s in found}

    # Fuzzy fallback: check tokens/ngrams vs skills list with threshold
    text_lower = text.lower()
    fuzzy_choices = process.extract(
        query=text_lower, choices=skills_list, scorer=fuzz.partial_ratio, limit=20
    )
    # fuzzy_choices is list of (choice, score, index) — but because query huge, not ideal;
    # Instead do fuzzy on smaller candidates: tokens/phrases, or skip if phrase matcher already found good
    fuzzy_matches = set()
    for choice, score, _ in fuzzy_choices:
        if score > 85:
            fuzzy_matches.add(choice)
    # Merge sets
    return set([s for s in canonical_found]) | fuzzy_matches
