# modules/ai_core/gemini_client.py
import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key=None, model_name="gemini-pro"):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or provided.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"GeminiClient initialized with model: {model_name}")

    def generate_chat_response(self, messages, generation_config=None, safety_settings=None):
        """
        Generates a chat response using a list of message history.
        :param messages: A list of message dicts, e.g.,
                         [{'role': 'user', 'parts': [{'text': 'Hello'}]},
                          {'role': 'model', 'parts': [{'text': 'Hi there!'}]}]
        """
        try:
            chat = self.model.start_chat(history=messages[:-1]) # History up to the last user message
            response = chat.send_message(
                messages[-1]['parts'][0]['text'], # Send only the latest user message content
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            # ... (rest of response parsing as before)
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
            # ... (error handling)
        except Exception as e:
            # ...
            return str(e)
        # Handle the case where the response is empty or blocked
    def generate_response(self, prompt, generation_config=None, safety_settings=None):
        """
        Generates a response from the Gemini model.
        :param prompt: The input prompt string.
        :param generation_config: Optional. A dictionary for generation configuration.
                                  e.g., {"temperature": 0.7, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
        :param safety_settings: Optional. A list of safety setting dictionaries.
                                e.g., [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]
        :return: The generated text response or an error message.
        """
        try:
            # Default config if none provided
            config = generation_config if generation_config else genai.types.GenerationConfig(
                candidate_count=1,
                # Add other defaults here if needed e.g. temperature=0.9
            )
            

            response = self.model.generate_content(
                prompt,
                generation_config=config,
                safety_settings=safety_settings
            )
            
            # Check for empty candidates or safety blocks
            if not response.candidates:
                if response.prompt_feedback.block_reason:
                    return f"Blocked due to: {response.prompt_feedback.block_reason_message}"
                return "No response generated. The prompt might have been blocked or resulted in empty candidates."

            # Accessing text, ensuring parts exist
            if response.candidates[0].content and response.candidates[0].content.parts:
                return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
            else:
                # Handle cases where the response might be blocked or empty in a different way
                finish_reason = response.candidates[0].finish_reason
                if finish_reason != 1 : # 1 usually means "STOP" (successful)
                     return f"Generation failed or was blocked. Finish Reason: {finish_reason.name}"
                return "Received an empty or non-text response part."

        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            return f"Error generating response: {str(e)}"

if __name__ == '__main__':
    # This is for basic testing of the client
    # Ensure your GEMINI_API_KEY is set in your .env file or environment
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env')) # Adjust path to .env

    try:
        client = GeminiClient()
        sample_prompt = "Hello Gemini, what can you do?"
        print(f"Sending prompt: {sample_prompt}")
        response_text = client.generate_response(sample_prompt)
        print(f"Gemini Response: {response_text}")
        
        sample_prompt_2 = "Write a short story about a friendly robot."
        print(f"Sending prompt: {sample_prompt_2}")
        response_text_2 = client.generate_response(sample_prompt_2, generation_config={"temperature": 0.8})
        print(f"Gemini Response 2: {response_text_2}")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
