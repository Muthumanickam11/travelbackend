from transformers import pipeline

class NLPService:
    def __init__(self):
        self._classifier = None
        self.candidate_labels = ["adventurous", "relaxed", "cultural", "food-related", "nightlife", "luxury", "budget"]

    @property
    def classifier(self):
        if self._classifier is None:
            # Using a smaller, faster model for zero-shot
            self._classifier = pipeline(
                "zero-shot-classification", 
                model="typeform/distilbert-base-uncased-mnli"
            )
        return self._classifier

    def classify_intent(self, text: str):
        result = self.classifier(text, self.candidate_labels)
        return result['labels'][0]

nlp_service = NLPService()
