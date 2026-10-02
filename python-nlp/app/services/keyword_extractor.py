import re
from typing import List

# Common English and conversational stopwords to filter out
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
    "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
    "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
    "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "tell", "give", "want", "please", "suggest", "explain"
}

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """
    Extracts salient keywords and key noun phrases using:
    - Compound noun and multi-word phrase detection
    - POS and linguistic stopword pruning
    - Salience ordering preserving semantic value
    """
    if not text:
        return []

    cleaned = text.strip()
    keywords: List[str] = []

    # Priority multi-word domain patterns to capture as cohesive key phrases
    domain_phrases = [
        "binary trees", "binary tree", "binary search tree", "binary search",
        "data structures", "dynamic programming", "machine learning", "deep learning",
        "neural networks", "system design", "operating systems", "computer networks",
        "object oriented", "relational databases", "database normalization",
        "cloud computing", "microservices architecture", "rest api", "full stack",
        "mern stack", "web development", "event loop", "asynchronous programming"
    ]

    lower_text = cleaned.lower()
    for phrase in domain_phrases:
        if phrase in lower_text:
            keywords.append(phrase)

    # Noun phrases / POS token extraction
    tokens = re.findall(r"[A-Za-z0-9#\+\.\-]+", cleaned)
    for tok in tokens:
        low = tok.lower()
        if low not in STOPWORDS and len(low) > 2:
            # Check if this token is already covered by a multi-word phrase
            already_covered = any(tok.lower() in kw.lower() for kw in keywords)
            if not already_covered and low not in [k.lower() for k in keywords]:
                keywords.append(tok)

    # Add meaningful action verbs if relevant (e.g. "practice", "learn", "compare", "debug")
    action_cues = ["practice", "learn", "compare", "difference", "debug", "error", "quiz", "summary", "revise"]
    for cue in action_cues:
        if cue in lower_text and cue not in [k.lower() for k in keywords]:
            keywords.append(cue)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for k in keywords:
        k_clean = k.strip().strip(".,;:?!'\"()[]{}")
        if k_clean and k_clean.lower() not in seen:
            seen.add(k_clean.lower())
            result.append(k_clean)

    return result[:max_keywords]
