# IntentLens — Python NLP Microservice

The core machine learning and natural language processing microservice for **IntentLens**.

---

## 1. NLP Pipeline Overview

```
Raw Student Query
        ↓
Text Cleaning & Normalization (app/utils/text_preprocessor.py)
        ↓
Feature Extraction (Sublinear TF-IDF Unigrams + Bigrams)
        ↓
Supervised Intent Classification (Logistic Regression / Linear SVM)
        ↓
Topic & Relational Concept Extraction (spaCy + CS Taxonomy)
        ↓
Keyword N-gram Extraction (POS Filtering & Salience)
        ↓
Learning Level Detection (BEGINNER / INTERMEDIATE / ADVANCED / UNKNOWN)
        ↓
Semantic Similarity Validation (Sentence Transformers all-MiniLM-L6-v2)
        ↓
Calibrated Confidence Calculation (0-100 Score & HIGH/MED/LOW Label)
        ↓
Deterministic Natural Language Explanation Synthesis
        ↓
FastAPI JSON Response
```

---

## 2. Intent Taxonomy (12 Categories)

| Intent ID | Label | Description |
|---|---|---|
| `LEARNING_REQUEST` | Learning Request | Student seeks roadmaps or guidance to learn a topic. |
| `CONCEPT_EXPLANATION` | Concept Explanation | Student requests theoretical mechanisms or breakdowns. |
| `COMPARISON` | Technology Comparison | Student asks to compare two or more technologies/algorithms. |
| `PRACTICE_REQUEST` | Practice Request | Student wants coding exercises, challenges, or drills. |
| `RESOURCE_REQUEST` | Resource Request | Student seeks books, documentation, courses, or guides. |
| `PREREQUISITE_QUERY` | Prerequisite Query | Inquires about foundational skills needed before a topic. |
| `DEBUGGING_HELP` | Debugging Help | Student is struggling with code errors, exceptions, or bugs. |
| `REVISION_REQUEST` | Revision Request | Rapid refresher or cheat sheet before exams or interviews. |
| `CAREER_SKILL_QUERY` | Career Skill Query | Job role requirements, resume qualifications, interview prep. |
| `PROJECT_GUIDANCE` | Project Guidance | Capstone, resume, and portfolio project suggestions. |
| `ASSESSMENT_QUERY` | Assessment Query | Diagnostic quizzes, tests, and self-evaluation questions. |
| `SUMMARY_REQUEST` | Summary Request | Condensed high-level summary or key takeaways of a topic. |

---

## 3. Machine Learning Methodology & Training

The dataset (`data/intents.csv`) consists of **423 authentic student queries** distributed across the 12 intents (~35-40 examples each).

### Training Steps:
1. **Preprocessing**: Normalizes unicode, expands colloquial contractions (e.g. *don't* &rarr; *do not*), preserves domain tokens (`C++`, `.js`).
2. **TF-IDF Vectorizer**: Extracted unigram and bigram features with sublinear term-frequency scaling:
   - Vocabulary size: 2,879 features
   - Sublinear TF enabled
   - Strip accents: unicode
3. **Classifier**: Multiclass Logistic Regression with balanced class weights (`C=3.0`, `max_iter=1000`) providing calibrated posterior probabilities.
4. **Validation Metrics**:
   - **Accuracy**: 89.41%
   - **Precision**: 91.08%
   - **Recall**: 89.41%
   - **F1-Score**: 89.33%

Artifacts saved to `models/`:
- `intent_classifier.pkl`
- `tfidf_vectorizer.pkl`
- `label_encoder.pkl`

---

## 4. Setup & Running

```bash
# Navigate to NLP directory
cd python-nlp

# Create Python virtual environment
py -3.11 -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm

# Retrain model if needed
python training/train_model.py

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```
