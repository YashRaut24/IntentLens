from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=2, description="Natural-language student learning query")

class IntentDetail(BaseModel):
    name: str
    label: str
    confidence: int

class SemanticMatch(BaseModel):
    intent: str
    similarity: float

class GoalDetail(BaseModel):
    text: str
    topic: str

class StartingPointDetail(BaseModel):
    title: str
    reason: str

class KnowledgeStateItem(BaseModel):
    concept: str
    state: str  # "KNOWN", "EXPLICIT_GAP", "POTENTIAL_GAP", "TARGET", "RELATED"

class AnalyzeResponse(BaseModel):
    query: str
    text: Optional[str] = None
    is_unclear: bool = False
    message: Optional[str] = None
    goal: Optional[GoalDetail] = None
    known_skills: List[str] = []
    knownSkills: List[str] = []
    explicit_gaps: List[str] = []
    explicitGaps: List[str] = []
    potential_gaps: List[str] = []
    potentialGaps: List[str] = []
    learning_level: str = "UNKNOWN"
    learningLevel: str = "UNKNOWN"
    learning_context: str = "SKILL_DEVELOPMENT"
    learningContext: str = "SKILL_DEVELOPMENT"
    topics: List[str] = []
    related_concepts: List[str] = []
    keywords: List[str] = []
    prerequisites: List[str] = []
    knowledge_states: List[KnowledgeStateItem] = []
    knowledgeStates: List[KnowledgeStateItem] = []
    starting_point: Optional[StartingPointDetail] = None
    startingPoint: Optional[StartingPointDetail] = None
    intent: Optional[IntentDetail] = None
    semantic_match: Optional[SemanticMatch] = None
    confidence: int = 85
    confidence_label: str = "HIGH"
    explanation: str = ""
    metadata: Optional[Dict[str, Any]] = None

class IntentCatalogItem(BaseModel):
    name: str
    label: str
    description: str
    icon: Optional[str] = None
