from transformers import pipeline

class SentimentAnalysisTool:
    """
    Tool to analyze sentiment of financial text (news headlines, tweets).
    """

    def __init__(self):
        """
        Load transformer-based sentiment analysis model (FinBERT).
        """
        self.model = pipeline("text-classification", model="ProsusAI/finbert")

    def analyze_sentiment(self, text):
        """
        Analyzes sentiment of the given text.
        :param text: Financial news headline or tweet.
        :return: Sentiment classification (Positive, Negative, Neutral) with score.
        """
        try:
            result = self.model(text)[0]  # Get first prediction
            return {
                "text": text,
                "sentiment": result["label"],
                "confidence": round(result["score"], 2)
            }
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
