from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/itinerary", tags=["itinerary"])

class ItineraryCreate(BaseModel):
    user_id: int
    events: List[int]
    notes: str = ""

@router.post("/")
def save_itinerary(itinerary: ItineraryCreate, db: Session = Depends(database.get_db)):
    new_itinerary = models.Itinerary(
        user_id=itinerary.user_id,
        events_json={"event_ids": itinerary.events, "notes": itinerary.notes}
    )
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return {"message": "Itinerary saved successfully", "itinerary_id": new_itinerary.id}

@router.get("/{user_id}")
def get_itineraries(user_id: int, db: Session = Depends(database.get_db)):
    itineraries = db.query(models.Itinerary).filter(models.Itinerary.user_id == user_id).all()
    # In a real app, you'd join with Events to get names
    return itineraries
