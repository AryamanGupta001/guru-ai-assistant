# modules/sentiment/response_modifier.py
# Adapts AI responses based on detected sentiment.

class ResponseModifier:
    def __init__(self):
        print("ResponseModifier initialized.")

    def modify_response_based_on_sentiment(self, original_response, user_sentiment):
        """
        Modifies the AI's response tone or content based on user's sentiment.
        :param original_response: The AI's initially generated response.
        :param user_sentiment: A sentiment analysis result (e.g., output from SentimentAnalyzer).
                               Example: {'label': 'negative', 'score': -0.8}
        :return: A modified response string.
        """
        modified_response = original_response

        if not user_sentiment or 'label' not in user_sentiment:
            return original_response # No sentiment data to act upon

        sentiment_label = user_sentiment.get('label', 'neutral').lower()

        if sentiment_label == "negative":
            # Example: Add an empathetic phrase if user is negative
            empathetic_phrases = [
                "I understand this might be frustrating. ",
                "I'm sorry to hear that. ",
                "Let's try to sort this out. "
            ]
            import random
            modified_response = random.choice(empathetic_phrases) + original_response
        elif sentiment_label == "positive":
            # Example: Add an encouraging phrase if user is positive
            positive_phrases = [
                "Great to hear! ",
                "That's wonderful! ",
                "Awesome! "
            ]
            import random
            modified_response = random.choice(positive_phrases) + original_response
        # Could add more complex logic for "neutral" or other nuances

        return modified_response

if __name__ == '__main__':
    modifier = ResponseModifier()
    
    original_resp = "I can help you with that task."
    
    neg_sentiment = {'label': 'negative', 'score': -0.7}
    modified_neg = modifier.modify_response_based_on_sentiment(original_resp, neg_sentiment)
    print(f"Original: {original_resp}\nUser Sentiment: Negative\nModified: {modified_neg}\n")

    pos_sentiment = {'label': 'positive', 'score': 0.8}
    modified_pos = modifier.modify_response_based_on_sentiment(original_resp, pos_sentiment)
    print(f"Original: {original_resp}\nUser Sentiment: Positive\nModified: {modified_pos}\n")

    neutral_sentiment = {'label': 'neutral', 'score': 0.1}
    modified_neutral = modifier.modify_response_based_on_sentiment(original_resp, neutral_sentiment)
    print(f"Original: {original_resp}\nUser Sentiment: Neutral\nModified: {modified_neutral}\n")
