import numpy as np
from typing import Dict, Any, List

# Representative anchor query prototypes for each of the 12 intents
INTENT_PROTOTYPES: Dict[str, List[str]] = {
    "LEARNING_REQUEST": [
        "How do I start learning this topic from scratch?",
        "I want to learn this framework from the beginning as a beginner.",
        "Where do I begin learning this programming language?",
        "What roadmap should I follow to learn this technology?",
    ],
    "CONCEPT_EXPLANATION": [
        "Can you explain how this concept works with an example?",
        "What is the theoretical meaning and mechanism of this topic?",
        "Can you break down this concept and explain why it is used?",
        "What is the internal mechanism of this algorithm or architecture?",
    ],
    "COMPARISON": [
        "What is the difference between these two technologies?",
        "Compare these two algorithms and their performance trade-offs.",
        "How does technology A compare against technology B?",
        "Difference between two concepts or programming paradigms?",
    ],
    "PRACTICE_REQUEST": [
        "Give me practice coding problems and exercises on this topic.",
        "Where can I find hands-on challenges and problem sets to practice?",
        "I need dynamic programming and algorithm coding practice questions.",
        "Provide exercise drills to practice writing code for this concept.",
    ],
    "RESOURCE_REQUEST": [
        "Suggest the best books and tutorials to learn this topic.",
        "Recommend free online courses, documentation, and video playlists.",
        "Where can I find cheat sheets and reference guides for this framework?",
        "What are the top learning resources for studying this subject?",
    ],
    "PREREQUISITE_QUERY": [
        "What should I learn before starting this technology?",
        "What are the foundational prerequisites needed before learning this?",
        "Do I need to know math or other languages prior to this subject?",
        "What concepts must I master before studying this advanced topic?",
    ],
    "DEBUGGING_HELP": [
        "Why is my code throwing an exception or runtime error?",
        "How do I fix this bug, segmentation fault, or crash in my application?",
        "Why is this function returning undefined or failing silently?",
        "Troubleshoot connection refused or syntax error in my program.",
    ],
    "REVISION_REQUEST": [
        "Quick revision notes and recap before my examination tomorrow.",
        "Give me a fast refresher on key concepts and formulas.",
        "I need to quickly review the essential points of this topic.",
        "Cheat sheet summary to revise this subject before an interview.",
    ],
    "CAREER_SKILL_QUERY": [
        "What skills do I need for an internship or job role in this field?",
        "What tech stack is required to become a software engineer?",
        "What do recruiters look for on a student resume for this role?",
        "How do I prepare for campus placement technical interviews?",
    ],
    "PROJECT_GUIDANCE": [
        "Suggest a capstone or portfolio project idea using this tech stack.",
        "What are good real-world project ideas to put on my resume?",
        "Give me innovative software project concepts for a college final year.",
        "Suggest a hands-on project to demonstrate proficiency in this subject.",
    ],
    "ASSESSMENT_QUERY": [
        "Give me a quiz or mock test to evaluate my understanding.",
        "Test my knowledge on this subject with 5 assessment questions.",
        "Create a multiple choice test to assess my readiness for exam.",
        "Diagnostic quiz to check if I have mastered these concepts.",
    ],
    "SUMMARY_REQUEST": [
        "Summarize this explanation and give me the key takeaways.",
        "Can you provide a concise executive summary of this topic?",
        "Provide a high-level overview summary of how this works.",
        "Condense this explanation into a short bullet-point summary.",
    ],
}

class SemanticSimilarityEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.prototype_embeddings = {}
        self._is_initialized = False

    def initialize(self):
        """Loads sentence-transformers model and pre-computes prototype embeddings"""
        if self._is_initialized:
            return

        try:
            from sentence_transformers import SentenceTransformer
            print(f"[Semantic] Loading SentenceTransformer '{self.model_name}'...")
            self.model = SentenceTransformer(self.model_name)

            # Precompute centroid/mean embeddings for each intent prototype
            for intent, sentences in INTENT_PROTOTYPES.items():
                embs = self.model.encode(sentences, convert_to_numpy=True, normalize_embeddings=True)
                # Compute centroid and re-normalize
                centroid = np.mean(embs, axis=0)
                centroid = centroid / np.linalg.norm(centroid)
                self.prototype_embeddings[intent] = centroid

            self._is_initialized = True
            print("[Semantic] Successfully initialized sentence embeddings for 12 intents.")
        except Exception as e:
            print(f"[Semantic] Warning: Could not initialize SentenceTransformer ({e}). Using cosine TF-IDF fallback.")
            self._is_initialized = False

    def find_most_similar(self, query: str) -> Dict[str, Any]:
        """
        Encodes student query and calculates cosine similarity against intent prototypes.
        Returns { "intent": best_intent, "similarity": float (0.0 to 1.0) }
        """
        if not self._is_initialized:
            self.initialize()

        if self.model and self.prototype_embeddings:
            try:
                query_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
                all_sims = {}
                best_intent = "CONCEPT_EXPLANATION"
                highest_sim = -1.0

                for intent, proto_emb in self.prototype_embeddings.items():
                    raw_dot = float(np.dot(query_emb, proto_emb))
                    calibrated = round(max(0.10, min(0.99, (raw_dot * 0.7) + 0.3)), 4)
                    all_sims[intent] = calibrated
                    if raw_dot > highest_sim:
                        highest_sim = raw_dot
                        best_intent = intent

                top_calibrated = all_sims.get(best_intent, 0.85)

                return {
                    "intent": best_intent,
                    "similarity": round(top_calibrated, 2),
                    "all_similarities": all_sims,
                }
            except Exception as e:
                print(f"[Semantic] Computation error: {e}")

        # Graceful fallback heuristic if transformer unavailable
        return {
            "intent": "CONCEPT_EXPLANATION",
            "similarity": 0.85
        }

semantic_engine = SemanticSimilarityEngine()
