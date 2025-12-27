from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentService:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_mood(self, text: str):
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"

sentiment_service = SentimentService()
