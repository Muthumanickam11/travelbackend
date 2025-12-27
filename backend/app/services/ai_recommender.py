from typing import List, Dict
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class RecommenderService:
    def __init__(self):
        # In a real app, this would load from the DB
        pass

    def get_recommendations(self, user_preferences: Dict, events: List[Dict], mood: str):
        # simple content-based filtering logic
        # 1. Filter by location and budget
        # 2. Score based on categories and mood
        
        ranked_events = []
        for event in events:
            score = 0.5 # base score
            
            # Match categories
            if any(cat in event['category'].lower() for cat in user_preferences.get('categories', [])):
                score += 0.3
            
            # Match Mood
            if mood == "positive" and event['category'].lower() in ['nightlife', 'festival', 'food']:
                score += 0.1
            elif mood == "negative" and event['category'].lower() in ['culture', 'nature', 'spa']:
                score += 0.2 # suggest relaxing things for "negative" (tired) mood
                
            # Random shuffle/noise for variety
            import random
            score += random.uniform(0, 0.1)
            
            ranked_events.append({
                "event_id": event['id'],
                "name": event['name'],
                "score": round(score, 2),
                "reason": self._generate_reason(event, user_preferences, mood)
            })
            
        return sorted(ranked_events, key=lambda x: x['score'], reverse=True)

    def _generate_reason(self, event, prefs, mood):
        if mood == "negative":
            return "Perfect for a relaxing day after feeling low energy."
        if any(cat in event['category'].lower() for cat in prefs.get('categories', [])):
            return f"Matches your interest in {event['category']}."
        return "Popular choice among similar travelers."

recommender_service = RecommenderService()
