from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    preferences = Column(JSON, default={})

    itineraries = relationship("Itinerary", back_populates="owner")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    category = Column(String)
    date = Column(DateTime)
    cost = Column(Float)
    metadata_info = Column(JSON, name="metadata") 

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    events_json = Column(JSON, name="events") # Store list of event IDs and notes
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="itineraries")
