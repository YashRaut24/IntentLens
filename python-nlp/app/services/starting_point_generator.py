from typing import Dict, List, Optional

def generate_starting_point(
    goal_topic: str,
    known_skills: List[str],
    explicit_gaps: List[str],
    potential_gaps: List[str],
    learning_level: str,
    prerequisites: List[str],
    context: str = "SKILL_DEVELOPMENT"
) -> Dict[str, str]:
    """
    NLP & pedagogical rule-driven starting point generator.
    Produces:
      {
        "title": "Starting Point Title",
        "reason": "Pedagogical explanation of why this starting point fits the learner"
      }
    """
    known_str = ", ".join(known_skills) if known_skills else None
    topic_clean = goal_topic.strip() if goal_topic else "your learning goal"
    topic_lower = topic_clean.lower()

    # Rule 1: Explicit gap stated by user is the highest-priority starting point
    if explicit_gaps:
        primary_gap = explicit_gaps[0]
        title = f"{primary_gap} Fundamentals"
        if "statistic" in primary_gap.lower() or "prob" in primary_gap.lower():
            title = "Statistics and Probability for Machine Learning"
        elif "dynamic programming" in primary_gap.lower():
            title = "Dynamic Programming Fundamentals"
        elif "nlp" in primary_gap.lower() or "natural language" in primary_gap.lower():
            title = "NLP Fundamentals"

        if known_skills:
            reason = (
                f"You already mention {known_str} as known foundations. "
                f"The explicitly stated weakness is {primary_gap}, so the system identifies {primary_gap} "
                f"as the immediate, high-priority learning gap before progressing further in {topic_clean}."
            )
        else:
            reason = (
                f"You explicitly identified {primary_gap} as an area of weakness or unfamiliarity. "
                f"Mastering the fundamentals of {primary_gap} will directly remove your roadblock toward {topic_clean}."
            )
        return {"title": title, "reason": reason}

    # Rule 2: LLMs with Python/ML known
    if "llm" in topic_lower or "large language" in topic_lower:
        has_ml = any("machine learning" in s.lower() or "ml" in s.lower() for s in known_skills)
        has_dl = any("deep learning" in s.lower() or "neural" in s.lower() for s in known_skills)
        if has_ml and not has_dl:
            return {
                "title": "Deep Learning Fundamentals",
                "reason": (
                    f"Your query indicates that you already have {known_str} foundations. "
                    f"Deep learning and neural networks are relevant prerequisite bridges "
                    f"before moving directly into modern attention mechanisms, transformers, and LLM architectures."
                )
            }
        elif not has_ml and not has_dl:
            return {
                "title": "Machine Learning & Neural Network Foundations",
                "reason": (
                    f"Understanding LLMs requires familiarity with neural architectures. "
                    f"Starting with ML fundamentals and neural networks provides the conceptual foundation needed for transformer models."
                )
            }

    # Rule 3: Web Development / React with HTML/CSS/JS known
    if "react" in topic_lower:
        has_js = any("javascript" in s.lower() or "js" in s.lower() for s in known_skills)
        if has_js:
            return {
                "title": "React Fundamentals",
                "reason": (
                    f"You already have relevant foundations in {known_str}. "
                    f"Since core JavaScript concepts are covered, you do not need to restart from basic web development "
                    f"and can proceed directly to React components, JSX, props, and state management."
                )
            }

    # Rule 4: Competitive Programming with basic DSA known
    if "competitive programming" in topic_lower or "cp" in topic_lower:
        return {
            "title": "Algorithm Design & Dynamic Programming",
            "reason": (
                f"With {known_str if known_skills else 'programming'} as your base, "
                f"focusing on algorithmic paradigms (recursion, memoization, and dynamic programming) "
                f"will give you the problem-solving leverage needed for competitive programming contests."
            )
        }

    # Rule 5: If potential prerequisite gaps exist, recommend the earliest foundational missing prerequisite
    if potential_gaps:
        first_prereq = potential_gaps[0]
        # Skip generic items like "Programming Fundamentals" if user already has programming skills
        if ("programming" in first_prereq.lower() or "fundamentals" in first_prereq.lower()) and known_skills:
            first_prereq = potential_gaps[1] if len(potential_gaps) > 1 else first_prereq

        title = f"{first_prereq} Foundations"
        reason = (
            f"To achieve your goal in {topic_clean}, {first_prereq} is a key prerequisite concept "
            f"not explicitly mentioned in your current knowledge base. Starting here establishes the necessary scaffolding."
        )
        if known_skills:
            reason = f"Building upon your existing knowledge of {known_str}, {reason}"
        return {"title": title, "reason": reason}

    # Rule 6: Default fallback
    return {
        "title": f"{topic_clean} Core Fundamentals",
        "reason": (
            f"Based on your query, you are ready to explore {topic_clean} directly. "
            f"Focusing on core syntax, architectural patterns, and practical hands-on examples will accelerate your progress."
        )
    }
