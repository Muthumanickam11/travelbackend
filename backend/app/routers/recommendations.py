from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database
from ..services.ai_recommender import recommender_service
from ..services.ai_sentiment import sentiment_service
from ..services.ai_nlp import nlp_service
from pydantic import BaseModel
from typing import List

router = APIRouter(tags=["recommendations"])

class RecommendRequest(BaseModel):
    user_id: int
    location: str
    preferences: dict

class MoodRequest(BaseModel):
    user_id: int
    text: str

@router.post("/recommendations")
def get_recommendations(req: RecommendRequest, db: Session = Depends(database.get_db)):
    # 1. Fetch available events in the location
    events = db.query(models.Event).filter(models.Event.location.ilike(f"%{req.location}%")).all()
    # Convert ORM to dict for the service
    events_data = [{"id": e.id, "name": e.name, "category": e.category} for e in events]
    
    # 2. Get recommendations (default mood positive if not specified)
    mood = req.preferences.get("mood", "positive")
    recs = recommender_service.get_recommendations(req.preferences, events_data, mood)
    return recs

@router.post("/mood")
def analyze_mood(req: MoodRequest, db: Session = Depends(database.get_db)):
    # 1. Analyze sentiment
    sentiment = sentiment_service.analyze_mood(req.text)
    
    # 2. Extract intent (optional enhancement)
    intent = nlp_service.classify_intent(req.text)
    
    # 3. Get recommendations based on mood
    # For demo, we'll fetch some events
    events = db.query(models.Event).limit(10).all()
    events_data = [{"id": e.id, "name": e.name, "category": e.category} for e in events]
    
    recs = recommender_service.get_recommendations({"categories": [intent]}, events_data, sentiment)
    
    return {
        "sentiment": sentiment,
        "intent": intent,
        "recommendations": recs[:5]
    }
