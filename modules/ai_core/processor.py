# modules/ai_core/processor.py
# Handles request/response formatting and any additional NLP beyond Gemini.

class AIProcessor:
    def __init__(self):
        print("AIProcessor initialized.")

    def format_prompt(self, user_query, conversation_history=None, context_data=None, system_instruction=None):
        # ... (keep existing logic, or adjust if system_instruction is prepended here for certain models)
        prompt = user_query # Base
        
        # This is a simplified history injection. For Gemini chat models, 
        # you'd typically build a list of {'role': 'user'/'model', 'parts': [{'text': ...}]}
        if conversation_history:
            history_str = "\\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-5:]]) # Last 5 turns
            prompt = f"Conversation History:\\n{history_str}\\n\\nUser: {user_query}"
        
        if context_data:
            prompt += f"\\n\\nRelevant Information: {context_data}"
        
        # If the model expects system instruction as part of the main prompt:
        # if system_instruction:
        #     prompt = f"{system_instruction}\\n\\n{prompt}"
            
        return prompt

    def parse_response(self, ai_raw_response):
        cleaned_response = ai_raw_response.strip()
        # Fallback to remove asterisks if the model still uses them despite instructions
        cleaned_response = cleaned_response.replace('*', '')
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
