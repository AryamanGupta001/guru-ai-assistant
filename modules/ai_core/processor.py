# modules/ai_core/processor.py
# Handles request/response formatting and any additional NLP beyond Gemini.

class AIProcessor:
    def __init__(self):
        print("AIProcessor initialized.")

    def format_prompt(self, user_query, conversation_history=None, context_data=None):
        """
        Formats the user query and any relevant context into a suitable prompt
        for the AI model.
        """
        prompt = user_query
        if conversation_history:
            # Example: Prepend some history (simplified)
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-3:]]) # Last 3 turns
            prompt = f"Conversation History:\n{history_str}\n\nUser: {user_query}"
        
        if context_data:
            # Example: Add retrieved context
            prompt += f"\n\nRelevant Information: {context_data}"
            
        return prompt

    def parse_response(self, ai_raw_response):
        """
        Parses the raw response from the AI model into a user-friendly format.
        Can also handle extracting structured data if the model is prompted for it.
        """
        # For now, assuming ai_raw_response is a simple string
        cleaned_response = ai_raw_response.strip()
        return cleaned_response

if __name__ == '__main__':
    processor = AIProcessor()
    
    # Test prompt formatting
    test_query = "What's the weather like today?"
    test_history = [
        {"role": "user", "content": "Hello GURU"},
        {"role": "assistant", "content": "Hello! How can I help you?"}
    ]
    formatted = processor.format_prompt(test_query, conversation_history=test_history)
    print("Formatted Prompt:\n", formatted)

    # Test response parsing
    raw_resp = "   The weather is sunny.  \n"
    parsed = processor.parse_response(raw_resp)
    print("\nParsed Response:", parsed)
