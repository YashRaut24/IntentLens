import json
import os
import re
from typing import Dict, Any, List

PREREQ_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prerequisites.json")

def load_prerequisites_dataset() -> Dict[str, List[str]]:
    """Loads prerequisite reference dataset."""
    try:
        with open(PREREQ_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[PrereqMatcher] Warning: Could not load prerequisites.json ({e})")
        return {}

PREREQUISITE_DATA = load_prerequisites_dataset()

# Map common goal variations to prerequisite dictionary keys
GOAL_KEY_MAP = {
    "llm": "LLMs",
    "llms": "LLMs",
    "large language models": "LLMs",
    "large language model": "LLMs",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "ai chatbot": "AI Chatbot",
    "chatbot": "AI Chatbot",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "machine learning internship preparation": "Machine Learning Internship",
    "machine learning internship": "Machine Learning Internship",
    "competitive programming": "Competitive Programming",
    "cp": "Competitive Programming",
    "dsa": "Competitive Programming",
    "data structures and algorithms": "Competitive Programming",
    "dynamic programming": "Competitive Programming",
    "deep learning": "Deep Learning",
    "kubernetes": "Kubernetes",
    "docker": "Docker",
    "backend development": "Backend Development",
    "backend developer": "Backend Development",
    "mern stack": "MERN Stack",
    "mern": "MERN Stack",
    "full stack web development": "MERN Stack",
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "computer vision": "Computer Vision",
    "system design": "System Design",
    "operating systems": "Operating Systems",
    "computer networks": "Computer Networks",
    "database management systems": "Database Management Systems",
}

def match_prerequisites_and_states(
    goal_topic: str,
    known_skills: List[str],
    explicit_gaps: List[str]
) -> Dict[str, Any]:
    """
    NLP prerequisite and lightweight knowledge state engine.
    States:
      - KNOWN: Concept explicitly claimed as known by student
      - EXPLICIT_GAP: Stated weakness or lack of experience
      - POTENTIAL_GAP: Prerequisite concept not mentioned as known or weak
      - TARGET: Target learning goal
    """
    if not goal_topic:
        return {
            "prerequisites": [],
            "potential_gaps": [],
            "knowledge_states": []
        }

    # Find matching prerequisites key
    topic_lower = goal_topic.lower().strip()
    target_key = GOAL_KEY_MAP.get(topic_lower)

    if not target_key:
        for k in PREREQUISITE_DATA.keys():
            if k.lower() in topic_lower or topic_lower in k.lower():
                target_key = k
                break

    prereq_list = PREREQUISITE_DATA.get(target_key, []) if target_key else []

    # If still not found, provide intelligent fallback domain prerequisites
    if not prereq_list:
        if "web" in topic_lower or "frontend" in topic_lower:
            prereq_list = ["HTML", "CSS", "JavaScript", "DOM Manipulation"]
        elif "ai" in topic_lower or "data" in topic_lower:
            prereq_list = ["Python", "Linear Algebra", "Statistics", "Data Structures"]
        else:
            prereq_list = ["Programming Fundamentals", "Logic Building", "Core Concepts"]

    known_lower = {s.lower(): s for s in known_skills}
    gap_lower = {g.lower(): g for g in explicit_gaps}

    def is_known(concept: str) -> bool:
        c_low = concept.lower()
        if c_low in known_lower:
            return True
        for k in known_lower:
            if k in c_low or c_low in k:
                return True
        return False

    def is_explicit_gap(concept: str) -> bool:
        c_low = concept.lower()
        if c_low in gap_lower:
            return True
        for g in gap_lower:
            if g in c_low or c_low in g:
                return True
        return False

    knowledge_states: List[Dict[str, str]] = []
    potential_gaps: List[str] = []
    seen_concepts = set()

    # 1. Add known skills first
    for skill in known_skills:
        if skill.lower() not in seen_concepts and skill.lower() != topic_lower:
            knowledge_states.append({"concept": skill, "state": "KNOWN"})
            seen_concepts.add(skill.lower())

    # 2. Add explicit gaps
    for gap in explicit_gaps:
        if gap.lower() not in seen_concepts and gap.lower() != topic_lower:
            knowledge_states.append({"concept": gap, "state": "EXPLICIT_GAP"})
            seen_concepts.add(gap.lower())

    # 3. Classify prerequisite concepts
    for concept in prereq_list:
        c_low = concept.lower()
        if c_low == topic_lower:
            continue
        if c_low in seen_concepts:
            continue

        if is_known(concept):
            knowledge_states.append({"concept": concept, "state": "KNOWN"})
            seen_concepts.add(c_low)
        elif is_explicit_gap(concept):
            knowledge_states.append({"concept": concept, "state": "EXPLICIT_GAP"})
            seen_concepts.add(c_low)
        else:
            knowledge_states.append({"concept": concept, "state": "POTENTIAL_GAP"})
            potential_gaps.append(concept)
            seen_concepts.add(c_low)

    # 4. Add target goal
    knowledge_states.append({"concept": goal_topic, "state": "TARGET"})

    return {
        "prerequisites": prereq_list,
        "potential_gaps": potential_gaps,
        "knowledge_states": knowledge_states
    }
