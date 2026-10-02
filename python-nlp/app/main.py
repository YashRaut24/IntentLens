from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analyze import router as analyze_router
from app.services.intent_classifier import intent_classifier_service
from app.services.semantic_similarity import semantic_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models and sentence transformers
    print("[IntentLens NLP] Service initializing ML models...")
    intent_classifier_service.load_models()
    semantic_engine.initialize()
    print("[IntentLens NLP] All NLP engines warmed up and ready.")
    yield
    print("[IntentLens NLP] Service shutting down.")

app = FastAPI(
    title="IntentLens NLP Intelligence Service",
    description="Student Learning Intent Classification, Topic Extraction & Intent Analytics API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(analyze_router)

@app.get("/")
def root():
    return {
        "service": "IntentLens NLP Intelligence Service",
        "status": "online",
        "docs_url": "/docs",
        "endpoints": [
            "POST /api/analyze",
            "GET /api/intents",
            "GET /api/health"
        ]
    }
