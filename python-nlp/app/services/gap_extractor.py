import re
from typing import List
from app.services.topic_extractor import TECH_TAXONOMY

# Explicit weakness / struggle / lack of experience patterns
GAP_PATTERNS = [
    # "weak at statistics", "weak in math"
    r"(?:i\s+am|i\'?m|am)?\s*(?:weak\s+(?:at|in)|poor\s+at)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|and|so|though|however|to|because)|\.|\;|$)",
    # "struggle with dynamic programming", "struggling with recursion"
    r"(?:struggle|struggling)\s+with\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|and|so|though|however)|\.|\;|$)",
    # "not good at dynamic programming", "not great at DSA"
    r"(?:not\s+(?:good|great|confident|comfortable)\s+(?:at|with|in))\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|and|so|though|however)|\.|\;|$)",
    # "never worked with NLP", "never used Docker", "never studied deep learning"
    r"(?:never\s+(?:worked\s+with|used|studied|built|touched|coded\s+in|learned))\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:before|yet|but|and|so|though|however)|\.|\;|$)",
    # "don't understand recursion", "don't know calculus" (excluding orienting questions like "what I should learn")
    r"(?:don\'?t|do\s+not)\s+(?:understand|get)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:well|at\s+all|properly|but|and|so|though|however)|\.|\;|$)",
    # "no experience with X", "zero experience in X", "lack knowledge of X"
    r"(?:no|zero|little|lack\s+of)\s+(?:prior\s+)?(?:experience\s+with|experience\s+in|knowledge\s+of|background\s+in)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|and|so|though|however)|\.|\;|$)",
    # "know X but not Y"
    r"(?:but|however)\s+(?:not|not\s+with)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:yet|at\s+all|though)|\.|\;|$)"
]

# Canonical normalization specifically for gaps
GAP_SYNONYMS = {
    "stats": "Statistics",
    "statistics": "Statistics",
    "probability": "Probability",
    "prob and stats": "Statistics and Probability",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "dp": "Dynamic Programming",
    "dynamic programming": "Dynamic Programming",
    "recursion": "Recursion",
    "dsa": "Data Structures and Algorithms",
    "data structures": "Data Structures and Algorithms",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "math": "Mathematics",
    "calculus": "Calculus",
    "linear algebra": "Linear Algebra",
    "deep learning": "Deep Learning",
    "neural networks": "Neural Networks",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "system design": "System Design",
}

NON_GAP_PHRASES = {
    "what i should learn first",
    "where to start",
    "where to begin",
    "what to learn",
    "how to start",
    "how to learn",
    "what should i learn",
    "anything",
    "everything",
    "much",
    "it",
    "this",
    "that"
}

def extract_explicit_gaps(query: str) -> List[str]:
    """
    Detects explicitly stated weaknesses, struggles, or missing prior experience from student query.
    Filters out orientation phrases like 'don't know where to start'.
    """
    if not query:
        return []

    cleaned = query.strip()
    gaps: List[str] = []
    captured_clauses: List[str] = []

    for pat in GAP_PATTERNS:
        matches = re.finditer(pat, cleaned, re.IGNORECASE)
        for m in matches:
            clause = m.group(1).strip()
            captured_clauses.append(clause)

    sorted_tax = sorted(TECH_TAXONOMY.items(), key=lambda x: len(x[0]), reverse=True)

    for clause in captured_clauses:
        items = re.split(r"\,|\band\b|\&", clause)
        for raw_item in items:
            item_clean = raw_item.strip()
            item_clean = re.sub(r"^(basic|some|advance|advanced|the|any)\s+", "", item_clean, flags=re.IGNORECASE).strip()
            if not item_clean or len(item_clean) < 2:
                continue

            item_lower = item_clean.lower()

            # Ignore orientation questions
            if item_lower in NON_GAP_PHRASES or any(item_lower.startswith(w) for w in ["what ", "where ", "how ", "which "]):
                continue

            matched_canonical = None

            if item_lower in GAP_SYNONYMS:
                matched_canonical = GAP_SYNONYMS[item_lower]
            elif item_lower in TECH_TAXONOMY:
                matched_canonical = TECH_TAXONOMY[item_lower]
            else:
                for term, canonical in sorted_tax:
                    if re.search(r"\b" + re.escape(term) + r"\b", item_lower):
                        matched_canonical = canonical
                        break

            if matched_canonical:
                if matched_canonical not in gaps:
                    gaps.append(matched_canonical)
            elif len(item_clean) > 2 and item_lower not in ["it", "that", "this", "them", "anything", "much"]:
                cap_item = item_clean.title()
                if cap_item not in gaps:
                    gaps.append(cap_item)

    return list(dict.fromkeys(gaps))
