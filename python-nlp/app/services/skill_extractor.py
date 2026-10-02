import re
from typing import List, Set
from app.services.topic_extractor import TECH_TAXONOMY, get_spacy_nlp

# Patterns where the student states known skills / experience
KNOWN_PATTERNS = [
    # "I know X and Y", "I already know X", "I know HTML, CSS and basic JavaScript"
    r"(?:i\s+(?:already\s+)?know|knowing|i\'?ve\s+learned|i\s+have\s+learned|studied)\s+(?:basic\s+|some\s+|good\s+)?([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|want|trying|looking|and\s+want|and\s+i\s+want|while|not)|[\.\;]|$)",
    # "I have worked with X and Y", "worked on X", "experience with X"
    r"(?:i\s+have|i\'?ve)\s+(?:worked\s+with|worked\s+on|experience\s+with|used|hands-on\s+with)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|want|trying|looking|and\s+want)|[\.\;]|$)",
    # "build an AI chatbot using Python" / "using Python and Flask"
    r"(?:build|create|develop|code|work|make)\s+.*?\s+(?:using|with|in)\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|and\s+want|\.|\;)|$)",
    # "I have basic X knowledge", "I have Python knowledge"
    r"(?:i\s+have|having)\s+(?:basic\s+|a\s+good\s+|solid\s+)?([A-Za-z0-9\+\#\.\s\-]+?)\s+(?:knowledge|background|foundation|skills)(?:\s+(?:and|but|though|however|want)|[\.\;]|$)",
    # "I am familiar with X", "familiar with X"
    r"(?:i\s+am|i\'?m)?\s*familiar\s+with\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|and\s+want)|[\.\;]|$)",
    # "I understand X", "already understand X"
    r"(?:i\s+(?:already\s+)?understand)\s+(?:the\s+basics\s+of\s+)?([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|and\s+want)|[\.\;]|$)",
    # "comfortable with X"
    r"(?:i\s+am|i\'?m)?\s*comfortable\s+with\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|and\s+want)|[\.\;]|$)",
    # "I have built projects using X / with X"
    r"(?:built\s+projects\s+(?:using|with|in))\s+([A-Za-z0-9\+\#\.\s\-\,\/]+?)(?:\s+(?:but|though|however|yet|and\s+want)|[\.\;]|$)",
]

# Canonical normalization map specifically for skills
SKILL_SYNONYMS = {
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "basic ml": "Machine Learning",
    "basic machine learning": "Machine Learning",
    "dsa": "Data Structures and Algorithms",
    "data structures": "Data Structures and Algorithms",
    "algorithms": "Data Structures and Algorithms",
    "basic dsa": "Data Structures and Algorithms",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "basic javascript": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "python": "Python",
    "basic python": "Python",
    "cpp": "C++",
    "c plus plus": "C++",
    "k8s": "Kubernetes",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "arrays": "Arrays",
    "linked lists": "Linked Lists",
}

def extract_known_skills(query: str, target_goal: str = None) -> List[str]:
    """
    Extracts skills explicitly claimed as known/experienced by the student.
    Guarantees target goal (e.g. 'I want to learn Python') is NOT treated as known skill.
    """
    if not query:
        return []

    cleaned = query.strip()
    known_skills: List[str] = []
    captured_clauses: List[str] = []

    # 1. Regex clause matching
    for pattern in KNOWN_PATTERNS:
        matches = re.finditer(pattern, cleaned, re.IGNORECASE)
        for m in matches:
            clause = m.group(1).strip()
            captured_clauses.append(clause)

    sorted_tax = sorted(TECH_TAXONOMY.items(), key=lambda x: len(x[0]), reverse=True)
    target_lower = target_goal.lower() if target_goal else ""

    for clause in captured_clauses:
        items = re.split(r"\,|\band\b|\&", clause)
        for raw_item in items:
            item_clean = raw_item.strip()
            item_clean = re.sub(r"^(basic|some|good|solid|advance|advanced|the|an?)\s+", "", item_clean, flags=re.IGNORECASE).strip()
            if not item_clean or len(item_clean) < 2:
                continue

            item_lower = item_clean.lower()
            matched_canonical = None

            if item_lower in SKILL_SYNONYMS:
                matched_canonical = SKILL_SYNONYMS[item_lower]
            elif item_lower in TECH_TAXONOMY:
                matched_canonical = TECH_TAXONOMY[item_lower]
            else:
                for term, canonical in sorted_tax:
                    if re.search(r"\b" + re.escape(term) + r"\b", item_lower):
                        matched_canonical = canonical
                        break

            if matched_canonical:
                # Guard: Do not add if it matches the target goal directly unless the user clearly says they already know it
                if target_lower and matched_canonical.lower() == target_lower and not ("already know " + target_lower in query.lower()):
                    continue
                if matched_canonical not in known_skills:
                    known_skills.append(matched_canonical)
            elif len(item_clean) > 2 and item_lower not in ["basics", "concepts", "fundamentals", "code", "programming", "things", "stuff"]:
                cap_item = item_clean.title()
                if cap_item not in known_skills:
                    known_skills.append(cap_item)

    return list(dict.fromkeys(known_skills))
