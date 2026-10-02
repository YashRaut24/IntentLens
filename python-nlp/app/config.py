import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DATASET_PATH = DATA_DIR / "intents.csv"

CLASSIFIER_MODEL_PATH = MODELS_DIR / "intent_classifier.pkl"
TFIDF_VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.pkl"

# Model hyperparameters
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"

# Intent Taxonomy Catalog
INTENT_METADATA = {
    "LEARNING_REQUEST": {
        "label": "Learning Request",
        "description": "Student is seeking guidance or a roadmap to start learning a new topic, framework, or technology.",
        "icon": "Compass",
    },
    "CONCEPT_EXPLANATION": {
        "label": "Concept Explanation",
        "description": "Student is requesting a detailed breakdown or theoretical clarification of a specific concept.",
        "icon": "BookOpen",
    },
    "COMPARISON": {
        "label": "Technology / Concept Comparison",
        "description": "Student is asking to contrast two or more technologies, algorithms, or approaches.",
        "icon": "GitCompare",
    },
    "PRACTICE_REQUEST": {
        "label": "Practice & Exercises Request",
        "description": "Student wants coding challenges, exercises, or problem sets to build practical mastery.",
        "icon": "Code2",
    },
    "RESOURCE_REQUEST": {
        "label": "Learning Resources Request",
        "description": "Student seeks curated books, tutorials, documentation, courses, or reference materials.",
        "icon": "Bookmark",
    },
    "PREREQUISITE_QUERY": {
        "label": "Prerequisite Query",
        "description": "Student inquires about foundational knowledge or prior skills needed before tackling a subject.",
        "icon": "Layers",
    },
    "DEBUGGING_HELP": {
        "label": "Debugging & Error Help",
        "description": "Student is struggling with code errors, exceptions, crashes, or unintended runtime behavior.",
        "icon": "Bug",
    },
    "REVISION_REQUEST": {
        "label": "Revision & Quick Recap",
        "description": "Student desires a rapid refresher, summary cheat sheet, or quick review before an exam or interview.",
        "icon": "RotateCcw",
    },
    "CAREER_SKILL_QUERY": {
        "label": "Career & Industry Skills Query",
        "description": "Student asks about industry role requirements, resume qualifications, interview prep, or job skills.",
        "icon": "Briefcase",
    },
    "PROJECT_GUIDANCE": {
        "label": "Project Ideas & Guidance",
        "description": "Student seeks practical capstone, resume, or portfolio project ideas and architectural advice.",
        "icon": "Lightbulb",
    },
    "ASSESSMENT_QUERY": {
        "label": "Assessment & Self-Test",
        "description": "Student wants to evaluate their knowledge through quizzes, mock exams, or diagnostic questions.",
        "icon": "CheckSquare",
    },
    "SUMMARY_REQUEST": {
        "label": "Content Summarization Request",
        "description": "Student requests a condensed, high-level summary or key takeaways of an explanation or topic.",
        "icon": "FileText",
    },
}
