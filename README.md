# IntentLens — Natural Language Learning Goal & Skill Gap Analyzer

> **Academic NLP Mini-Project | Semester 7 | Natural Language Processing**  
> An NLP intelligence pipeline that turns natural-language student learning goals into structured knowledge: what you want to learn, what you already know, what foundations you may be missing, and exactly where you should start.

---

## 1. Project Overview

**IntentLens** is an NLP-driven learning intelligence system that answers a fundamental question in educational NLP:

> *"Given the way a student naturally describes what they want to learn, can NLP extract their learning goal, current knowledge, weaknesses, learning level, and relevant prerequisites to identify where they should start?"*

Instead of merely telling the student *"Your intent is LEARNING_REQUEST"*, IntentLens uses supervised intent classification and dense sentence embeddings internally as supporting signals, while presenting the student with an actionable, structured learning profile:

1. **YOUR LEARNING GOAL** (e.g., `LLMs`, `React`, `AI Chatbot`)
2. **WHAT YOU ALREADY KNOW** (e.g., `✓ Python`, `✓ Machine Learning`)
3. **EXPLICITLY MENTIONED GAPS** (e.g., `• Statistics`, `• Dynamic Programming`)
4. **RELEVANT PREREQUISITES & POTENTIAL GAPS** (e.g., `• Neural Networks`, `• Transformers`)
5. **YOUR RECOMMENDED STARTING POINT** (e.g., `Deep Learning Fundamentals`)
6. **PEDAGOGICAL REASONING** (Explaining *WHY* this starting point builds on what they already know)
7. **LEARNING CONTEXT & LEVEL** (`Skill Development`, `Career Preparation`, `Intermediate`, etc.)

---

## 2. Problem Statement

When students seek guidance, they formulate holistic, compound natural-language queries:

> *"I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first."*  
> *"I'm preparing for a machine learning internship. I know Python and sklearn but I'm weak at statistics."*  
> *"I want to learn React. I already know HTML, CSS and basic JavaScript."*

Traditional search engines perform naive keyword matches, missing the distinction between what is already known and what is missing. Meanwhile, basic text classifiers classify the sentence as a generic `LEARNING_REQUEST`, offering zero guidance on prerequisites or starting points.

**IntentLens** bridges this gap using pure NLP: extracting target goals, validating claimed competencies, isolating explicit weaknesses, mapping prerequisite dependencies, and synthesizing a justified starting point.

---

## 3. Motivation

Students often fail to progress in self-directed learning because:
1. They skip essential prerequisites and get stuck on advanced material.
2. They repeat concepts they already know because generic courses force them to start from zero.
3. They cannot identify the specific missing link between their current knowledge and their goal.

IntentLens applies NLP techniques to remove friction from self-directed learning.

---

## 4. Key Objectives

- **Goal Extraction**: Isolate target technologies, frameworks, and career objectives using linguistic dependency analysis and domain taxonomies.
- **Competency Separation**: Differentiate claimed knowledge (`KNOWN`) from target goals (`TARGET`) and stated struggles (`EXPLICIT_GAP`).
- **Cautious Prerequisite Inference**: Never assume a student definitely does not know a concept simply because it was unmentioned; instead, flag it as a `POTENTIAL_GAP`.
- **Pedagogical Starting Point**: Generate an immediate foundation with a contextual explanation.
- **Pure Local NLP**: Run 100% locally on standard CPU hardware with spaCy, scikit-learn, and Sentence-Transformers (`all-MiniLM-L6-v2`) without third-party LLM APIs.

---

## 5. Key Features

- **Linguistic Goal Extraction**: Identifies the primary objective even in compound sentences.
- **Known vs. Gap Extractor**: Recognizes positive affirmations ("I know Python") vs. negative struggle assertions ("weak at statistics", "never worked with NLP").
- **5-State Knowledge Mapping**: `KNOWN`, `EXPLICIT_GAP`, `POTENTIAL_GAP`, `TARGET`, `RELATED`.
- **Learning Level Classifier**: Detects `BEGINNER`, `INTERMEDIATE`, `ADVANCED`, or `UNKNOWN`.
- **Learning Context Classifier**: Detects `CAREER_PREPARATION`, `PROJECT_BUILDING`, `SKILL_DEVELOPMENT`, `EXAM_PREPARATION`, `REVISION`, `INTERVIEW_PREPARATION`.
- **Visual Progression Flow**: Interactive node relationship from known skills through potential gaps to target goal.
- **Graceful Unclear Query Fallback**: Non-actionable input (e.g. *"I like technology."*) prompts the student for clarification without fabricating data.

---

## 6. NLP Pipeline

```
Student's Natural Language Learning Query
                    ↓
          Text Preprocessing
                    ↓
     Internal Intent Classification (TF-IDF + Logistic Regression)
                    ↓
    Semantic Sentence Embeddings (all-MiniLM-L6-v2)
                    ↓
       Extract Learning Goal (Linguistic Patterns & spaCy)
                    ↓
       Extract Known Skills (Competency Cue Extraction)
                    ↓
       Extract Weak / Missing Skills (Struggle Cue Extraction)
                    ↓
       Detect Learning Level & Learning Context
                    ↓
     Prerequisite Cross-Referencing & Knowledge States
                    ↓
       Generate Useful Learning Starting Point + Reason
                    ↓
       Structured Educational Profile & Visual Flow
```

---

## 7. System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   React.js Frontend                    │
│      (Vite • Warm Dark Editorial UI • Vanilla CSS)     │
└───────────────────────────┬────────────────────────────┘
                            │ REST JSON
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Node.js Express API                  │
│       (MongoDB History Storage • Gateway Controller)   │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP Proxy / Internal API
                            ▼
┌────────────────────────────────────────────────────────┐
│               Python 3.11 FastAPI Engine               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Goal Extractor (Linguistic patterns & POS)       │  │
│  │ Skill Extractor (Known competencies)             │  │
│  │ Gap Extractor (Stated weaknesses & struggles)    │  │
│  │ Prerequisite Matcher (Knowledge state mapping)   │  │
│  │ Starting Point Generator (Pedagogical rules)     │  │
│  │ Level & Context Detectors                        │  │
│  │ Sentence-Transformers (all-MiniLM-L6-v2)         │  │
│  │ Intent Classifier (TF-IDF + Logistic Regression) │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 8. Intent Classification (Internal Component)

Intent classification runs internally to provide contextual signals:

- `LEARNING_REQUEST`: Roadmap and starting guidance
- `PREREQUISITE_QUERY`: Foundational dependencies
- `CONCEPT_EXPLANATION`: Theoretical clarification
- `COMPARISON`: Technology trade-offs
- `PRACTICE_REQUEST`: Hands-on coding exercises
- `RESOURCE_REQUEST`: Curated books, docs, and courses
- `DEBUGGING_HELP`: Error and runtime crash resolution
- `REVISION_REQUEST`: Exam and interview recaps
- `CAREER_SKILL_QUERY`: Job requirements and placement preparation
- `PROJECT_GUIDANCE`: Portfolio and capstone architecture
- `ASSESSMENT_QUERY`: Self-quizzes and diagnostics
- `SUMMARY_REQUEST`: Condensed takeaways

---

## 9. Learning Goal Extraction

- **Module**: `python-nlp/app/services/goal_extractor.py`
- **Methodology**: Pattern matching over verb-noun phrases (`"want to get into X"`, `"want to learn X"`, `"preparing for X"`, `"build an X"`) combined with canonical taxonomy normalization.
- **Safety**: Rejects generic, non-actionable queries (e.g., *"I like technology."*) returning `is_unclear: true`.

---

## 10. Known Skill Extraction

- **Module**: `python-nlp/app/services/skill_extractor.py`
- **Methodology**: Isolates explicit competence statements:
  - `"I know Python and basic ML"` &rarr; `["Python", "Machine Learning"]`
  - `"I have worked with React and Node"` &rarr; `["React", "Node.js"]`
  - `"built ... using Python"` &rarr; `["Python"]`
- **Guard**: Ensures the target goal (e.g., *"I want to learn React"*) is never classified as a known skill.

---

## 11. Skill Gap Extraction

- **Module**: `python-nlp/app/services/gap_extractor.py`
- **Methodology**: Detects explicit struggle and weakness markers:
  - `"weak at statistics"` &rarr; `["Statistics"]`
  - `"struggle with dynamic programming"` &rarr; `["Dynamic Programming"]`
  - `"never worked with NLP"` &rarr; `["NLP"]`
- **Filters**: Excludes conversational orientation phrases (e.g., *"don't know where to start"*).

---

## 12. Learning Level Detection

- **Module**: `python-nlp/app/services/learning_level_detector.py`
- **Levels**: `BEGINNER`, `INTERMEDIATE`, `ADVANCED`, `UNKNOWN`.
- **Heuristics**: Evaluates experience markers (`"from scratch"`, `"comfortable with"`, `"mastery"`), context (e.g., multiple known skills implies intermediate), and target scope.

---

## 13. Learning Context Detection

- **Module**: `python-nlp/app/services/context_detector.py`
- **Categories**:
  - `CAREER_PREPARATION` (internship, job, hiring)
  - `PROJECT_BUILDING` (build, create, develop)
  - `SKILL_DEVELOPMENT` (master, competitive programming, learn)
  - `EXAM_PREPARATION` (exam, test, semester)
  - `INTERVIEW_PREPARATION` (interview, technical round)
  - `REVISION` (revise, refresher, recap)

---

## 14. Semantic Similarity Engine

- **Module**: `python-nlp/app/services/semantic_similarity.py`
- **Model**: `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Role**: Computes dense 384-dimensional cosine similarity to validate intent prototypes and concept semantics without exact keyword overlap.

---

## 15. Prerequisite Matching

- **Module**: `python-nlp/app/services/prerequisite_matcher.py`
- **Reference**: `python-nlp/data/prerequisites.json`
- **Matching**: Cross-references extracted goals with domain dependencies and categorizes each prerequisite:
  - If found in `known_skills` &rarr; `KNOWN` (Covered)
  - If found in `explicit_gaps` &rarr; `EXPLICIT_GAP` (Stated Gap)
  - Otherwise &rarr; `POTENTIAL_GAP` (Unmentioned Prerequisite)

---

## 16. Starting Point Generation

- **Module**: `python-nlp/app/services/starting_point_generator.py`
- **Logic**:
  1. If an explicit weakness was stated (e.g., weak in statistics for ML internship), that gap is prioritized as the immediate starting point.
  2. If prerequisite gaps exist between known skills and the goal (e.g., Python/ML known, goal is LLMs), the bridging foundation (Deep Learning) is recommended.
  3. If all foundational web basics are covered (HTML/CSS/JS), the framework fundamentals (React) are recommended directly.
  4. Generates an academic reason explaining *WHY* this starting point fits the student.

---

## 17. Knowledge State Representation

| Concept | State | Meaning |
|---|---|---|
| Python | `KNOWN` | Explicitly stated as known by student |
| Machine Learning | `KNOWN` | Explicitly stated as known by student |
| Deep Learning | `POTENTIAL_GAP` | Prerequisite not mentioned in query |
| Transformers | `POTENTIAL_GAP` | Prerequisite not mentioned in query |
| LLMs | `TARGET` | Primary learning goal |

---

## 18. Datasets

1. **`python-nlp/data/intents.csv`**: 423 curated student queries across 12 intent categories used for supervised classification.
2. **`python-nlp/data/learning_queries.csv`**: 80+ comprehensive student learning queries annotated with goal, known skills, explicit gaps, learning level, and learning context.
3. **`python-nlp/data/prerequisites.json`**: Reference prerequisite maps for core computer science domains (LLMs, React, ML, CP, MERN, Kubernetes, Docker, Backend).

---

## 19. Model Training & Evaluation

The supervised intent model was trained using TF-IDF N-grams (1-2) with Logistic Regression:

```
============================================================
           INTENTLENS MODEL EVALUATION METRICS
============================================================
Accuracy  : 89.41%
Precision : 91.08%
Recall    : 89.41%
F1-Score  : 89.33%
============================================================

Detailed Classification Report:

                     precision    recall  f1-score   support

   ASSESSMENT_QUERY       0.70      1.00      0.82         7
 CAREER_SKILL_QUERY       0.88      1.00      0.93         7
         COMPARISON       0.78      1.00      0.88         7
CONCEPT_EXPLANATION       1.00      0.71      0.83         7
     DEBUGGING_HELP       1.00      0.86      0.92         7
   LEARNING_REQUEST       0.89      1.00      0.94         8
   PRACTICE_REQUEST       1.00      1.00      1.00         7
 PREREQUISITE_QUERY       0.86      0.86      0.86         7
   PROJECT_GUIDANCE       1.00      1.00      1.00         7
   RESOURCE_REQUEST       1.00      0.71      0.83         7
   REVISION_REQUEST       0.83      0.71      0.77         7
    SUMMARY_REQUEST       1.00      0.86      0.92         7

           accuracy                           0.89        85
          macro avg       0.91      0.89      0.89        85
       weighted avg       0.91      0.89      0.89        85
```

---

## 20. Installation & Running Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.10 or 3.11)
- MongoDB running on `mongodb://127.0.0.1:27017`

### 1. Python NLP Engine
```bash
cd python-nlp
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python training/train_model.py
uvicorn app.main:app --reload --port 8000
```

### 2. Node.js Express Gateway
```bash
cd server
npm install
npm run dev
```

### 3. React Frontend Client
```bash
cd client
npm install
npm run dev
```
Access the application at `http://localhost:5173`.

---

## 21. API Documentation

### POST `/api/analysis` (Express Gateway) / POST `/api/analyze` (Python FastAPI)

**Sample Request**:
```json
{
  "query": "I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first."
}
```

**Sample Response**:
```json
{
  "success": true,
  "data": {
    "query": "I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first.",
    "isUnclear": false,
    "goal": {
      "text": "Learn LLMs",
      "topic": "LLMs"
    },
    "knownSkills": ["Python", "Machine Learning"],
    "explicitGaps": [],
    "potentialGaps": ["Neural Networks", "Deep Learning", "Attention Mechanism", "Transformers"],
    "learningLevel": "INTERMEDIATE",
    "learningContext": "SKILL_DEVELOPMENT",
    "startingPoint": {
      "title": "Deep Learning Fundamentals",
      "reason": "Your query indicates that you already have Python, Machine Learning foundations. Deep learning and neural networks are relevant prerequisite bridges before moving directly into modern attention mechanisms, transformers, and LLM architectures."
    },
    "confidence": 88
  }
}
```

---

## 22. Verification Test Cases

| Test | Input Query | Extracted Goal | Known Skills | Stated Gaps | Starting Point |
|---|---|---|---|---|---|
| **1** | *"I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first."* | `LLMs` | Python, Machine Learning | None | `Deep Learning Fundamentals` |
| **2** | *"I want to learn React. I already know HTML, CSS and basic JavaScript."* | `React` | HTML, CSS, JavaScript | None | `React Fundamentals` |
| **3** | *"I want to build an AI chatbot using Python, but I've never worked with NLP."* | `AI Chatbot` | Python | NLP | `NLP Fundamentals` |
| **4** | *"I'm preparing for a machine learning internship. I know Python and sklearn but I'm weak at statistics."* | `Machine Learning` | Python, scikit-learn | Statistics | `Statistics and Probability for Machine Learning` |
| **5** | *"I know Java and basic DSA. I want to start competitive programming but I'm not good at dynamic programming."* | `Competitive Programming` | Java, DSA | Dynamic Programming | `Dynamic Programming Fundamentals` |
| **6** | *"I like technology."* | *None* | None | None | Prompt for clear learning goal |

---

## 23. Limitations & Future Scope

- **Domain Scope**: Vocabulary is tailored for computer science, software engineering, and data science domains.
- **Phrasing Sensitivity**: Highly fragmented or sarcastic queries may require further conversational clarification.
- **Future Integration with Cognivue**: IntentLens provides the upstream NLP understanding layer to extract structured learner profiles before knowledge graphs, mastery modeling, and cognitive frontier sequencing take over in larger learning platforms.
