import re
from typing import Tuple

# Cue patterns for each learning level
BEGINNER_PATTERNS = [
    r"\b(beginner|beginners|newbie|novice|starter|freshman|starting out)\b",
    r"\b(from scratch|from the beginning|from zero|ground up|introduction|introductory|101)\b",
    r"\b(new to|start learning|how to start|where to begin|never worked with|never used|never coded|no prior knowledge|absolute beginner)\b",
    r"\b(easy|simple|elementary|foundational|basic understanding)\b",
    r"\bdon\'?t know.*very well\b",
    r"\bnever heard of\b",
]

INTERMEDIATE_PATTERNS = [
    r"\b(intermediate|moderate|next level|beyond basics|deepen|solidify)\b",
    r"\b(already know (basic|the basics)|know the basics|comfortable with|familiar with|have used before)\b",
    r"\b(understand.*but.*struggle with|i understand.*can you explain)\b",
    r"\b(transition from|bridge the gap|real world application|practical usage)\b",
    r"\b(medium level|mid level|best practices|clean code)\b",
    r"\b(internship|job|preparing for|competitive programming|cp)\b",
    r"\bi\s+know\s+[a-z0-9\+\#\.\s\-]+\s+and\b",
    r"\b(basic\s+machine\s+learning|basic\s+ml|basic\s+dsa|basic\s+javascript|basic\s+python)\b",
]

ADVANCED_PATTERNS = [
    r"\b(advanced|expert|mastery|deep dive|internals|under the hood|low level)\b",
    r"\b(production grade|enterprise|high performance|scalability|scale|sharding)\b",
    r"\b(concurrency|multithreading|asynchronous internals|memory management|distributed)\b",
    r"\b(advanced patterns|design patterns|micro-architectures|compiler optimization)\b",
    r"\b(benchmark|profiling|latency optimization|fault tolerance|raft consensus)\b",
]

def detect_learning_level(text: str) -> Tuple[str, float]:
    """
    Detects the student's proficiency or targeted learning level:
    Returns (level, confidence_score) where level in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'UNKNOWN']
    """
    if not text:
        return "UNKNOWN", 0.50

    lower = text.lower()

    # Score matches by regex hit count and priority
    adv_matches = sum(1 for p in ADVANCED_PATTERNS if re.search(p, lower))
    int_matches = sum(1 for p in INTERMEDIATE_PATTERNS if re.search(p, lower))
    beg_matches = sum(1 for p in BEGINNER_PATTERNS if re.search(p, lower))

    # Priority check: explicit advance
    if adv_matches > 0 and adv_matches >= int_matches and adv_matches >= beg_matches:
        return "ADVANCED", min(0.75 + (adv_matches * 0.08), 0.96)

    # Intermediate check
    if int_matches > 0 and int_matches >= beg_matches:
        return "INTERMEDIATE", min(0.72 + (int_matches * 0.08), 0.94)

    # Beginner check
    if beg_matches > 0:
        return "BEGINNER", min(0.78 + (beg_matches * 0.07), 0.97)

    # Contextual check: "I know X and Y" implies intermediate knowledge
    if re.search(r"i\s+(?:know|understand|worked\s+with)\s+.*?\s+(?:and|,)", lower):
        return "INTERMEDIATE", 0.80

    # Default to BEGINNER if asking "want to learn X" or "start X"
    if re.search(r"\b(want to learn|want to get into|start)\b", lower):
        return "BEGINNER", 0.70

    return "UNKNOWN", 0.50
