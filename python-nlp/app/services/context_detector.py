import re

CONTEXT_RULES = [
    # EXAM_PREPARATION
    (
        r"\b(exam|test|midterm|final\s+exam|semester|viva|quiz|boards?)\b",
        "EXAM_PREPARATION"
    ),
    # INTERVIEW_PREPARATION
    (
        r"\b(interview|coding\s+round|technical\s+round|oa|online\s+assessment|mock\s+interview)\b",
        "INTERVIEW_PREPARATION"
    ),
    # CAREER_PREPARATION
    (
        r"\b(internship|job|career|placement|hiring|role|resume|cv|industry|junior\s+developer|fresher)\b",
        "CAREER_PREPARATION"
    ),
    # PROJECT_BUILDING
    (
        r"\b(build|building|create|creating|develop|developing|make|making|full[- ]stack\s+app|project|portfolio|capstone)\b",
        "PROJECT_BUILDING"
    ),
    # REVISION
    (
        r"\b(revise|revision|brush\s+up|refresher|revisit|recap|review|forgot)\b",
        "REVISION"
    ),
    # SKILL_DEVELOPMENT
    (
        r"\b(competitive\s+programming|cp|leetcode|codeforces|hackerrank|master|get\s+into|dive\s+into|level\s+up|practice)\b",
        "SKILL_DEVELOPMENT"
    ),
    # ACADEMIC_LEARNING
    (
        r"\b(syllabus|course|university|college|professor|lecture|assignment|homework|curriculum)\b",
        "ACADEMIC_LEARNING"
    ),
    # GENERAL_EXPLORATION
    (
        r"\b(explore|curious|learn|how\s+to|what\s+is|started|starting|understand)\b",
        "SKILL_DEVELOPMENT"  # default natural learning goal
    ),
]

def detect_learning_context(query: str) -> str:
    """
    Detects the student's learning context using linguistic cues and domain intent.
    Returns one of:
      ACADEMIC_LEARNING, SKILL_DEVELOPMENT, CAREER_PREPARATION, PROJECT_BUILDING,
      INTERVIEW_PREPARATION, REVISION, EXAM_PREPARATION, GENERAL_EXPLORATION, UNKNOWN
    """
    if not query or len(query.strip()) < 5:
        return "UNKNOWN"

    lower = query.lower()

    # Priority check: direct pattern matches
    for pattern, context in CONTEXT_RULES:
        if re.search(pattern, lower):
            return context

    return "GENERAL_EXPLORATION"
