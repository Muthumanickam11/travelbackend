from fastapi import FastAPI
from .routers import auth, events, itinerary, recommendations
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database sync failed: {e}. Ensure DATABASE_URL is correct.")

app = FastAPI(title="AI Cultural Immersion Travel Planner API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(itinerary.router)
app.include_router(recommendations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Cultural Immersion Travel Planner API!"}
