import os
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib

from app.config import (
    CLASSIFIER_MODEL_PATH,
    TFIDF_VECTORIZER_PATH,
    LABEL_ENCODER_PATH,
    INTENT_METADATA,
)
from app.utils.text_preprocessor import clean_text

class IntentClassifierService:
    def __init__(self):
        self.classifier = None
        self.vectorizer = None
        self.label_encoder = None
        self._is_loaded = False

    def load_models(self, force_reload: bool = False):
        if self._is_loaded and not force_reload:
            return

        if not CLASSIFIER_MODEL_PATH.exists() or not TFIDF_VECTORIZER_PATH.exists() or not LABEL_ENCODER_PATH.exists():
            print("[Classifier] Models not found on disk. Training will be required.")
            return

        try:
            self.classifier = joblib.load(CLASSIFIER_MODEL_PATH)
            self.vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
            self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
            self._is_loaded = True
            print("[Classifier] Successfully loaded TF-IDF Vectorizer and Intent Classifier.")
        except Exception as e:
            print(f"[Classifier] Error loading models: {e}")
            self._is_loaded = False

    def is_ready(self) -> bool:
        return self._is_loaded and self.classifier is not None

    def predict(self, raw_text: str) -> Dict[str, Any]:
        """
        Classifies the student query text.
        Returns:
            {
                "name": "LEARNING_REQUEST",
                "label": "Learning Request",
                "description": "...",
                "probability": 0.94,
                "all_probabilities": { "LEARNING_REQUEST": 0.94, ... }
            }
        """
        if not self._is_loaded:
            self.load_models()

        if not self._is_loaded:
            raise RuntimeError("Model artifacts are not loaded. Run train_model.py first.")

        cleaned = clean_text(raw_text)
        features = self.vectorizer.transform([cleaned])

        probabilities = self.classifier.predict_proba(features)[0]
        max_idx = int(probabilities.argmax())
        max_prob = float(probabilities[max_idx])

        intent_name = self.label_encoder.inverse_transform([max_idx])[0]
        meta = INTENT_METADATA.get(intent_name, {
            "label": intent_name.replace("_", " ").title(),
            "description": "Student intent detected by classifier."
        })

        all_probs = {}
        for idx, prob in enumerate(probabilities):
            cls_name = self.label_encoder.inverse_transform([idx])[0]
            all_probs[cls_name] = round(float(prob), 4)

        return {
            "name": intent_name,
            "label": meta["label"],
            "description": meta["description"],
            "probability": max_prob,
            "all_probabilities": all_probs,
        }

intent_classifier_service = IntentClassifierService()
