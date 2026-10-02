"""
IntentLens NLP Training Pipeline
Trains a supervised text classification model using TF-IDF + Logistic Regression / Calibrated Linear SVM.
Evaluates accuracy, precision, recall, F1, and saves model artifacts to models/.
"""

import os
import sys
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Add parent directory to sys.path to import app modules
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
sys.path.append(str(BASE_DIR))

from app.utils.text_preprocessor import clean_text
from training.generate_dataset import generate_csv

def train():
    data_path = BASE_DIR / "data" / "intents.csv"
    models_dir = BASE_DIR / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        print(f"[Training] Dataset not found at {data_path}, generating fresh dataset...")
        generate_csv(str(data_path))

    print(f"[Training] Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"[Training] Loaded {len(df)} samples across {df['intent'].nunique()} intents.")

    # 1. Clean texts
    print("[Training] Preprocessing query texts...")
    df["clean_text"] = df["text"].apply(clean_text)

    # 2. Encode labels
    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["intent"])

    # 3. Stratified train/test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.20,
        random_state=42,
        stratify=df["label"]
    )
    print(f"[Training] Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    # 4. Feature Extraction: TF-IDF
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=6000,
        strip_accents="unicode"
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"[Training] TF-IDF Vocabulary size: {len(vectorizer.vocabulary_)} features")

    # 5. Classifier Training (Logistic Regression with balanced weights for true probabilities)
    print("[Training] Fitting multiclass Logistic Regression classifier...")
    classifier = LogisticRegression(
        C=3.0,
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
    classifier.fit(X_train_vec, y_train)

    # 6. Evaluation
    y_pred = classifier.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    print("\n" + "=" * 60)
    print("           INTENTLENS MODEL EVALUATION METRICS")
    print("=" * 60)
    print(f"Accuracy  : {acc * 100:.2f}%")
    print(f"Precision : {prec * 100:.2f}%")
    print(f"Recall    : {rec * 100:.2f}%")
    print(f"F1-Score  : {f1 * 100:.2f}%")
    print("=" * 60)
    print("\nDetailed Classification Report:\n")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    ))
    print("=" * 60)

    # 7. Save model artifacts
    model_file = models_dir / "intent_classifier.pkl"
    vec_file = models_dir / "tfidf_vectorizer.pkl"
    le_file = models_dir / "label_encoder.pkl"

    joblib.dump(classifier, model_file)
    joblib.dump(vectorizer, vec_file)
    joblib.dump(label_encoder, le_file)

    print(f"[Training] Model saved to: {model_file}")
    print(f"[Training] Vectorizer saved to: {vec_file}")
    print(f"[Training] Label encoder saved to: {le_file}")
    print("[Training] Pipeline training complete successfully!")

if __name__ == "__main__":
    train()
