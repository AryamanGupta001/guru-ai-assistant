# modules/ai_core/gemini_client.py
import os
import google.generativeai as genai
from .config import SYSTEM_INSTRUCTION_TEXT # Import the persona

class GeminiClient:
    def __init__(self, api_key=None, model_name="gemini-pro", system_instruction=SYSTEM_INSTRUCTION_TEXT): # Add system_instruction
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or provided.")
        
        genai.configure(api_key=api_key)
        # Pass system_instruction if the model supports it (e.g., gemini-1.5-pro)
        # For older models or if passing differently, you might need to include it in the 'prompt' to generate_content
        try:
            self.model = genai.GenerativeModel(
                model_name,
                system_instruction=system_instruction # Pass it here
            )
            print(f"GeminiClient initialized with model: {model_name} and system instruction.")
        except Exception as e: # Catch potential errors if model doesn't support system_instruction directly
            print(f"Warning: Could not set system_instruction directly for model {model_name} ({e}). Will try prepending to prompt if necessary.")
            self.model = genai.GenerativeModel(model_name)
            self.system_instruction_fallback = system_instruction # Store for fallback

    def generate_response(self, prompt, generation_config=None, safety_settings=None, stream=False): # Added stream
        try:
            final_prompt = prompt
            # Fallback if system_instruction wasn't set in __init__ (older models)
            # This is a simple prepend; more sophisticated structuring might be needed for chat models
            if hasattr(self, 'system_instruction_fallback') and self.system_instruction_fallback:
                 if isinstance(prompt, str):
                    final_prompt = f"{self.system_instruction_fallback}\n\nUser: {prompt}\nAssistant:"
                 # If prompt is a list of messages for chat, prepend system message differently
                 # elif isinstance(prompt, list):
                 #     # This needs careful construction based on Gemini's chat message format
                 #     pass


            response = self.model.generate_content(
                final_prompt, # Use the potentially modified prompt
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=stream # Enable streaming
            )
            
            if stream:
                return response # Return the generator object for streaming

            # ... (rest of your existing non-streaming response parsing logic)
            if not response.candidates:
                if response.prompt_feedback.block_reason:
                    return f"Blocked due to: {response.prompt_feedback.block_reason_message}"
                return "No response generated. The prompt might have been blocked or resulted in empty candidates."

            if response.candidates[0].content and response.candidates[0].content.parts:
                return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
            else:
                finish_reason = response.candidates[0].finish_reason
                if finish_reason != 1 : 
                     return f"Generation failed or was blocked. Finish Reason: {finish_reason.name}"
                return "Received an empty or non-text response part."

        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            # If streaming, we can't return an error string like this easily.
            # The Flask route will need to handle stream errors.
            if stream:
                yield f"Error: {str(e)}" # Yield an error chunk
            else:
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
