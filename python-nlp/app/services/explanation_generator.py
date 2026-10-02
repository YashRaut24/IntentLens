from typing import List, Optional

def generate_explanation(
    intent_name: str,
    topics: List[str],
    related_concepts: List[str],
    learning_level: str,
    confidence: int,
    query_text: str = ""
) -> str:
    """
    Generates a clear, natural-language explanation of the detected learning intent,
    synthesizing extracted topics, related concepts, and proficiency levels
    without relying on any external LLM APIs.
    """
    topic_str = " and ".join(topics) if topics else "the specified subject"
    has_related = bool(related_concepts)
    related_str = " and ".join(related_concepts) if has_related else ""
    level_suffix = f" at a {learning_level.lower()} level" if learning_level != "UNKNOWN" else ""

    templates = {
        "LEARNING_REQUEST": (
            f"The student is requesting a structured learning roadmap for {topic_str}{level_suffix}"
            + (f", noting prior familiarity or context with {related_str}." if has_related else ".")
        ),
        "CONCEPT_EXPLANATION": (
            f"The query asks for a conceptual breakdown and theoretical explanation of {topic_str}"
            + (f", contrasting or building upon {related_str}." if has_related else ".")
        ),
        "COMPARISON": (
            f"The query asks to compare and analyze architectural or functional differences between {topic_str}"
            + (f" in relation to {related_str}." if has_related else ".")
        ),
        "PRACTICE_REQUEST": (
            f"The student is seeking hands-on coding problems, exercises, or algorithm challenges to practice {topic_str}{level_suffix}."
        ),
        "RESOURCE_REQUEST": (
            f"The student is asking for curated learning materials, textbooks, documentation, or tutorials for {topic_str}."
        ),
        "PREREQUISITE_QUERY": (
            f"The query asks which foundational concepts, tools, or skills should be mastered before learning {topic_str}."
        ),
        "DEBUGGING_HELP": (
            f"The student is encountering an error, runtime failure, or unexpected behavior in their code involving {topic_str} and requires troubleshooting assistance."
        ),
        "REVISION_REQUEST": (
            f"The query is a quick revision or exam recap request to review the core mechanisms and key points of {topic_str}."
        ),
        "CAREER_SKILL_QUERY": (
            f"The query investigates industry requirements, resume qualifications, or essential technical skills for career roles related to {topic_str}."
        ),
        "PROJECT_GUIDANCE": (
            f"The student is seeking practical capstone or portfolio project ideas and implementation guidance utilizing {topic_str}."
        ),
        "ASSESSMENT_QUERY": (
            f"The student wants to self-assess and test their comprehension of {topic_str} through quizzes or diagnostic questions."
        ),
        "SUMMARY_REQUEST": (
            f"The query requests a concise, high-level summary condensing the key takeaways of {topic_str}."
        ),
    }

    explanation = templates.get(
        intent_name,
        f"The system detected a {intent_name.replace('_', ' ').lower()} regarding {topic_str} with {confidence}% confidence."
    )

    return explanation
