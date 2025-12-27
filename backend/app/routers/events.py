from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, database
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])

class EventSchema(BaseModel):
    id: int
    name: str
    location: str
    category: str
    date: datetime
    cost: float
    metadata: dict

    model_config = {"from_attributes": True}

@router.get("/", response_model=List[EventSchema])
def get_events(
    location: Optional[str] = None, 
    date: Optional[str] = None, 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Event)
    if location:
        query = query.filter(models.Event.location.ilike(f"%{location}%"))
    # In a real app, you'd parse the date string and filter
    return query.all()

@router.post("/")
def add_event(event: EventSchema, db: Session = Depends(database.get_db)):
    # Map 'metadata' from schema to 'metadata_info' in model
    event_data = event.model_dump()
    metadata = event_data.pop("metadata")
    db_event = models.Event(**event_data, metadata_info=metadata)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
