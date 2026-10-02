import re
from typing import Optional, Dict, Any
from app.services.topic_extractor import TECH_TAXONOMY, extract_topics_and_skills

GOAL_PATTERNS = [
    # "want to get into X", "want to learn X", "looking to learn X"
    r"(?:want to|looking to|trying to|hoping to|wish to|plan to|planning to)\s+(?:get into|learn|master|study|dive into|pick up|understand|explore)\s+([A-Za-z0-9\+\#\.\s\-]+?)(?:\s+(?:from|but|though|however|and|because|for|since|as|with|after)|\.|\,|$)",
    # "want to build X" / "want to create X"
    r"(?:want to|looking to|trying to|hoping to)\s+(?:build|create|develop|make)\s+(?:an?|the)?\s*([A-Za-z0-9\+\#\.\s\-]+?)(?:\s+(?:using|with|in|for|but|though)|\.|\,|$)",
    # "preparing for X", "prepping for X"
    r"(?:preparing for|prepping for|studying for|getting ready for)\s+(?:an?|the)?\s*([A-Za-z0-9\+\#\.\s\-]+?)(?:\s+(?:role|position|job|interview|exam|test|internship|and|but)|\.|\,|$)",
    # "start competitive programming", "start learning X"
    r"(?:start|begin)\s+([A-Za-z0-9\+\#\.\s\-]+?)(?:\s+(?:but|though|however|and|from)|\.|\,|$)",
    # "suggest a project using X" / "suggest a X project"
    r"(?:suggest|recommend)\s+(?:a|an)?\s*([A-Za-z0-9\+\#\.\s\-]+?)\s+project",
    # "how do I learn X" / "where do I begin with X"
    r"(?:how do i|how can i|where do i)\s+(?:start|begin|learn|master)\s+(?:with\s+)?([A-Za-z0-9\+\#\.\s\-]+?)(?:\s+(?:from|as|after|if)|\.|\?|$)",
]

GOAL_CANONICAL_MAP = {
    "llm": "LLMs",
    "llms": "LLMs",
    "large language models": "LLMs",
    "large language model": "LLMs",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "ai chatbot": "AI Chatbot",
    "chatbot": "AI Chatbot",
    "machine learning internship": "Machine Learning Internship Preparation",
    "ml internship": "Machine Learning Internship Preparation",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "competitive programming": "Competitive Programming",
    "cp": "Competitive Programming",
    "dsa": "Data Structures and Algorithms",
    "data structures": "Data Structures and Algorithms",
    "dynamic programming": "Dynamic Programming",
    "dp": "Dynamic Programming",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "docker": "Docker",
    "mern": "MERN Stack",
    "mern stack": "MERN Stack",
    "full stack": "Full Stack Web Development",
    "full-stack": "Full Stack Web Development",
    "backend": "Backend Development",
    "backend development": "Backend Development",
    "deep learning": "Deep Learning",
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "operating systems": "Operating Systems",
    "os": "Operating Systems",
    "computer networks": "Computer Networks",
    "dbms": "Database Management Systems",
}

def extract_learning_goal(query: str) -> Optional[Dict[str, str]]:
    """
    Extracts the student's core learning goal:
    Returns dict {"text": "...", "topic": "..."} or None if no valid goal is present.
    """
    if not query or len(query.strip()) < 5:
        return None

    cleaned = query.strip()
    lower = cleaned.lower()

    # Reject non-actionable or generic non-learning statements
    non_goals = ["i like technology", "hello", "hi there", "what is this", "test", "how are you", "i am fine"]
    if lower.rstrip(".!?") in non_goals:
        return None

    extracted_topic = None
    goal_raw_text = None

    # 1. Match specific linguistic patterns
    for pat in GOAL_PATTERNS:
        match = re.search(pat, cleaned, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            # Clean candidate string
            cand_clean = re.sub(r"^(a|an|the|to|some|basic|advanced)\s+", "", candidate, flags=re.IGNORECASE).strip()
            if len(cand_clean) > 1 and cand_clean.lower() not in ["it", "this", "that", "them", "code", "anything", "everything"]:
                # Check canonical map
                cand_lower = cand_clean.lower()
                for key, canonical in GOAL_CANONICAL_MAP.items():
                    if key == cand_lower or f" {key} " in f" {cand_lower} " or cand_lower.startswith(key):
                        extracted_topic = canonical
                        goal_raw_text = candidate
                        break
                if not extracted_topic:
                    # Check general tech taxonomy
                    for key, canonical in TECH_TAXONOMY.items():
                        if key == cand_lower or f" {key} " in f" {cand_lower} ":
                            extracted_topic = canonical
                            goal_raw_text = candidate
                            break

                if not extracted_topic and len(cand_clean) > 2:
                    extracted_topic = cand_clean.title()
                    goal_raw_text = candidate
                break

    # 2. If pattern extraction didn't catch, check topic extractor against query
    if not extracted_topic:
        extracted = extract_topics_and_skills(cleaned)
        topics = extracted.get("topics", [])
        if topics and topics[0] != "General Computer Science":
            extracted_topic = topics[0]
            goal_raw_text = topics[0]

    if not extracted_topic:
        return None

    # Format human-friendly display text
    if "internship" in lower or "job" in lower:
        display_text = f"{extracted_topic} Preparation" if not extracted_topic.endswith("Preparation") else extracted_topic
    elif "build" in lower or "project" in lower:
        display_text = f"Build {extracted_topic}"
    else:
        display_text = f"Learn {extracted_topic}"

    return {
        "text": display_text,
        "topic": extracted_topic
    }
