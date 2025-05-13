# modules/ai_core/gemini_client.py
import os
import google.generativeai as genai
from .config import SYSTEM_INSTRUCTION_TEXT
import logging # Add logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key=None, model_name="gemini-2.0-flash", system_instruction=SYSTEM_INSTRUCTION_TEXT):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or provided.")
        
        genai.configure(api_key=api_key)
        
        self.model_name = model_name
        self.system_instruction_text = system_instruction # Store for potential use
        self.model_supports_system_instruction_directly = False

        try:
            self.model = genai.GenerativeModel(
                model_name,
                system_instruction=self.system_instruction_text
            )
            self.model_supports_system_instruction_directly = True
            logger.info(f"GeminiClient initialized model '{model_name}' directly WITH system instruction.")
        except (TypeError, ValueError) as e:
            logger.warning(f"Model '{model_name}' might not support 'system_instruction' parameter directly in constructor ({e}).")
            logger.info("Fetching available models for debugging...")
            self.list_available_models()  # Log available models
            self.model = genai.GenerativeModel(model_name)
            self.model_supports_system_instruction_directly = False

    def generate_response(self, prompt, generation_config=None, safety_settings=None, stream=False):
        final_prompt_for_api = prompt

        # If model doesn't support system_instruction directly and prompt is a list (chat history)
        # we should prepend the system instruction as the first message in the list.
        if not self.model_supports_system_instruction_directly and isinstance(prompt, list) and self.system_instruction_text:
            logger.info("Prepending system instruction to message list for model.")
            # Ensure system instruction isn't already there to avoid duplication
            is_system_instruction_present = any(
                part.get('text', '').strip() == self.system_instruction_text.strip()
                for msg in prompt 
                if msg.get('role') == 'user' or msg.get('role') == 'system' # Check user or potential system role
                for part in msg.get('parts', [])
            )
            if not is_system_instruction_present:
                # Gemini often expects system-like prompts to be from 'user' if no 'system' role is supported in contents
                # Or, for models that do support it in contents, 'system' role.
                # For safety, let's check model documentation or experiment. For now, 'user' is a common fallback.
                final_prompt_for_api = [
                    {'role': 'user', 'parts': [{'text': f"[SYSTEM GUIDANCE]:\n{self.system_instruction_text}"}]}
                ] + prompt
        elif not self.model_supports_system_instruction_directly and isinstance(prompt, str) and self.system_instruction_text:
            logger.info("Prepending system instruction to string prompt for model.")
            final_prompt_for_api = f"[SYSTEM GUIDANCE]:\n{self.system_instruction_text}\n\nUser: {prompt}\nAssistant:"

        try:
            logger.info(f"Sending to Gemini Model ({self.model_name}): stream_enabled={stream}")
            logger.debug(f"Final prompt for API: {final_prompt_for_api}") # Can be very verbose

            response_iterable = self.model.generate_content(
                final_prompt_for_api,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=stream
            )
            
            if stream:
                logger.info("Streaming response from Gemini...")
                # It's crucial to iterate through the stream here to catch immediate errors
                try:
                    for chunk in response_iterable:
                        yield chunk
                except Exception as stream_e:
                    logger.error(f"Error DURING Gemini stream iteration: {stream_e}")
                    yield f"Error_Stream_Iteration: {str(stream_e)}" # Yield an error string
                return # End of generator for stream=True

            # Non-streaming path (remains largely the same)
            logger.info("Received non-streaming response from Gemini.")
            # response_iterable is now a single GenerateContentResponse object
            response_obj = response_iterable 

            if not response_obj.candidates:
                block_reason_msg = "Unknown reason."
                if response_obj.prompt_feedback and response_obj.prompt_feedback.block_reason:
                    block_reason_msg = f"{response_obj.prompt_feedback.block_reason.name} - {response_obj.prompt_feedback.block_reason_message}"
                logger.warning(f"No candidates in response. Blocked due to: {block_reason_msg}")
                yield f"Error: Blocked due to: {block_reason_msg}"
            
            full_text = "".join(part.text for part in response_obj.candidates[0].content.parts if hasattr(part, 'text'))
            if not full_text:
                finish_reason = response_obj.candidates[0].finish_reason
                logger.warning(f"Empty text from Gemini. Finish Reason: {finish_reason.name if finish_reason else 'N/A'}")
                if finish_reason != 1: # 1 usually means "STOP"
                     return f"Generation failed or was blocked. Finish Reason: {finish_reason.name if finish_reason else 'N/A'}"
                return "Received an empty or non-text response."
            return full_text

        except ValueError as ve: # e.g. API key issue
            logger.error(f"ValueError during Gemini API call: {ve}")
            if stream: yield f"Error_API_Config: {str(ve)}"
            else: return f"Error_API_Config: {str(ve)}"
        except Exception as e:
            logger.error(f"Unexpected error during Gemini API call: {e}")
            if stream: yield f"Error_API_Call: {str(e)}" # Yield an error chunk
            else: return f"Error_API_Call: {str(e)}"

    # Add this function to the GeminiClient class or as a standalone utility
    def list_available_models():
        try:
            from google.generativeai import models
            available_models = models.list_models()
            logger.info("Available models:")
            for model in available_models:
                logger.info(f"Model ID: {model.model_id}, Supported Methods: {model.supported_generation_methods}")
            return available_models
        except Exception as e:
            logger.error(f"Error fetching available models: {e}")
            return []

# ... (rest of the file, including if __name__ == '__main__')
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

        # Example usage of streaming response
        user_message = "Tell me a joke."
        response_stream = client.generate_response(
            prompt=user_message,
            generation_config={"temperature": 0.7},
            safety_settings=None,  # TEMPORARY DEBUG
            stream=True
        )
        print("Streaming response:")
        for chunk in response_stream:
            print(chunk)

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
