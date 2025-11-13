# src/scoring.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def jd_resume_similarity_score(jd_text, resume_text):
    vect = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
    X = vect.fit_transform([jd_text, resume_text])
    sim = cosine_similarity(X[0:1], X[1:2])[0][0]
    return float(sim)

def skill_coverage_score(required_skills, resume_skills):
    required_set = set([s.lower() for s in required_skills])
    resume_set = set([s.lower() for s in resume_skills])
    if not required_set:
        return 0.0
    matched = len(required_set & resume_set)
    return matched / len(required_set)

def combined_match_score(jd_text, resume_text, required_skills, resume_skills, weights=(0.6, 0.4)):
    """
    weights: (jd_similarity_weight, skill_coverage_weight)
    returns float 0..1
    """
    sim = jd_resume_similarity_score(jd_text, resume_text)
    scov = skill_coverage_score(required_skills, resume_skills)
    score = weights[0]*sim + weights[1]*scov
    return score, sim, scov
