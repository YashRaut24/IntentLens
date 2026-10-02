from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from app.schemas.analysis_schema import (
    AnalyzeRequest,
    AnalyzeResponse,
    IntentDetail,
    SemanticMatch,
    GoalDetail,
    StartingPointDetail,
    KnowledgeStateItem,
    IntentCatalogItem
)
from app.config import INTENT_METADATA
from app.services.intent_classifier import intent_classifier_service
from app.services.semantic_similarity import semantic_engine
from app.services.topic_extractor import extract_topics_and_skills
from app.services.keyword_extractor import extract_keywords
from app.services.learning_level_detector import detect_learning_level
from app.services.goal_extractor import extract_learning_goal
from app.services.skill_extractor import extract_known_skills
from app.services.gap_extractor import extract_explicit_gaps
from app.services.context_detector import detect_learning_context
from app.services.prerequisite_matcher import match_prerequisites_and_states
from app.services.starting_point_generator import generate_starting_point

router = APIRouter(prefix="/api", tags=["NLP Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_student_query(payload: AnalyzeRequest):
    query_text = payload.text.strip()
    if len(query_text) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student query is too short. Please describe what you want to learn."
        )

    # 1. Internal Intent Classification & Semantic Support
    try:
        clf_result = intent_classifier_service.predict(query_text)
    except Exception as e:
        print(f"[AnalyzeRoute] Classifier warning: {e}")
        clf_result = {"intent": "LEARNING_REQUEST", "probability": 0.85, "all_probabilities": {}}

    semantic_result = semantic_engine.find_most_similar(query_text)
    semantic_intent = semantic_result["intent"]
    semantic_sim = semantic_result["similarity"]
    all_sem_sims = semantic_result.get("all_similarities", {})
    all_clf_probs = clf_result.get("all_probabilities", {})

    combined_scores = {}
    lower_q = query_text.lower()

    for intent_key in INTENT_METADATA.keys():
        prob = all_clf_probs.get(intent_key, 0.0)
        sim = all_sem_sims.get(intent_key, 0.5)
        combined_scores[intent_key] = (0.55 * prob) + (0.45 * sim)

    best_intent_name = max(combined_scores.items(), key=lambda x: x[1])[0]
    best_meta = INTENT_METADATA.get(best_intent_name, {
        "label": best_intent_name.replace("_", " ").title(),
        "description": "Student intent detected by ensemble NLP."
    })

    top_clf_prob = all_clf_probs.get(best_intent_name, clf_result["probability"])
    blended = (0.60 * top_clf_prob) + (0.40 * semantic_sim)
    if best_intent_name == semantic_intent:
        blended = min(0.98, blended * 1.1)
    final_confidence_int = int(round(blended * 100))
    final_confidence_int = max(60, min(97, final_confidence_int))

    # 2. Extract Learning Goal
    goal_dict = extract_learning_goal(query_text)

    # Handle Unclear / Non-actionable queries (e.g. "I like technology.")
    if not goal_dict:
        # Check if there are explicit gaps or known skills to salvage
        preliminary_skills = extract_known_skills(query_text)
        preliminary_gaps = extract_explicit_gaps(query_text)
        if not preliminary_skills and not preliminary_gaps:
            return AnalyzeResponse(
                query=query_text,
                text=query_text,
                is_unclear=True,
                message="We couldn't identify a clear learning goal. Try describing what you want to learn, what you already know, or what you're struggling with.",
                confidence=40,
                confidence_label="LOW",
                explanation="The system could not detect an actionable target technology, skill gap, or academic topic in the provided statement."
            )
        else:
            goal_topic = preliminary_gaps[0] if preliminary_gaps else preliminary_skills[0]
            goal_dict = {"text": f"Learn {goal_topic}", "topic": goal_topic}

    goal_topic = goal_dict["topic"]

    # 3. Extract Known Skills (ensuring goal is not marked as known unless explicitly stated)
    known_skills = extract_known_skills(query_text, target_goal=goal_topic)

    # 4. Extract Explicit Gaps / Weaknesses
    explicit_gaps = extract_explicit_gaps(query_text)

    # 5. Detect Learning Level
    learning_level, _ = detect_learning_level(query_text)

    # 6. Detect Learning Context
    learning_context = detect_learning_context(query_text)

    # 7. Prerequisite Matching and Knowledge States
    prereq_result = match_prerequisites_and_states(goal_topic, known_skills, explicit_gaps)
    prerequisites = prereq_result["prerequisites"]
    potential_gaps = prereq_result["potential_gaps"]
    raw_knowledge_states = prereq_result["knowledge_states"]
    knowledge_state_items = [
        KnowledgeStateItem(concept=ks["concept"], state=ks["state"])
        for ks in raw_knowledge_states
    ]

    # 8. Starting Point & Pedagogical Reason Generation
    starting_point_dict = generate_starting_point(
        goal_topic=goal_topic,
        known_skills=known_skills,
        explicit_gaps=explicit_gaps,
        potential_gaps=potential_gaps,
        learning_level=learning_level,
        prerequisites=prerequisites,
        context=learning_context
    )

    # 9. Topic and Keyword Extraction
    extracted_topics = [goal_topic]
    for s in known_skills:
        if s not in extracted_topics:
            extracted_topics.append(s)
    keywords = extract_keywords(query_text, max_keywords=5)

    # Formulate clear pedagogical explanation
    explanation = starting_point_dict["reason"]

    confidence_label = "HIGH" if final_confidence_int >= 80 else ("MEDIUM" if final_confidence_int >= 65 else "LOW")

    return AnalyzeResponse(
        query=query_text,
        text=query_text,
        is_unclear=False,
        goal=GoalDetail(text=goal_dict["text"], topic=goal_topic),
        known_skills=known_skills,
        knownSkills=known_skills,
        explicit_gaps=explicit_gaps,
        explicitGaps=explicit_gaps,
        potential_gaps=potential_gaps,
        potentialGaps=potential_gaps,
        learning_level=learning_level,
        learningLevel=learning_level,
        learning_context=learning_context,
        learningContext=learning_context,
        topics=extracted_topics,
        related_concepts=prerequisites[:3],
        keywords=keywords,
        prerequisites=prerequisites,
        knowledge_states=knowledge_state_items,
        knowledgeStates=knowledge_state_items,
        starting_point=StartingPointDetail(
            title=starting_point_dict["title"],
            reason=starting_point_dict["reason"]
        ),
        startingPoint=StartingPointDetail(
            title=starting_point_dict["title"],
            reason=starting_point_dict["reason"]
        ),
        intent=IntentDetail(
            name=best_intent_name,
            label=best_meta["label"],
            confidence=final_confidence_int
        ),
        semantic_match=SemanticMatch(
            intent=semantic_intent,
            similarity=semantic_sim
        ),
        confidence=final_confidence_int,
        confidence_label=confidence_label,
        explanation=explanation,
        metadata={
            "classifier_raw_prob": round(top_clf_prob, 4),
            "all_probabilities": all_clf_probs,
            "semantic_intent_match": (best_intent_name == semantic_intent)
        }
    )

@router.get("/intents", response_model=List[IntentCatalogItem])
async def get_intent_catalog():
    catalog = []
    for name, meta in INTENT_METADATA.items():
        catalog.append(
            IntentCatalogItem(
                name=name,
                label=meta["label"],
                description=meta["description"],
                icon=meta.get("icon", "Tag")
            )
        )
    return catalog

@router.get("/health")
async def health_check():
    is_ready = intent_classifier_service.is_ready()
    return {
        "status": "healthy" if is_ready else "degraded",
        "service": "IntentLens NLP Intelligence Service",
        "version": "2.0.0",
        "models_loaded": is_ready,
        "semantic_engine_ready": semantic_engine._is_initialized,
    }
