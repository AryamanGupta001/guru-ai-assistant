# app.py
from flask import Flask, render_template, request, jsonify, Response, stream_with_context # Added Response, stream_with_context
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

from modules.ai_core.gemini_client import GeminiClient
from modules.ai_core.processor import AIProcessor
from modules.ai_core.config import (
    DEFAULT_MODEL_NAME,
    DEFAULT_GENERATION_CONFIG,
    DEFAULT_SAFETY_SETTINGS,
    SYSTEM_INSTRUCTION_TEXT # Import the system instruction
)
from modules.context.history import ConversationHistory

app = Flask(__name__)

# --- INITIAL WELCOME MESSAGE ---
GURU_WELCOME_MESSAGE = "Hello there! I'm GURU, your witty and insightful AI assistant. How can I illuminate your day or help you conquer your to-do list?"

try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("FATAL: GEMINI_API_KEY not found in .env file. Please set it.")
    
    gemini_client = GeminiClient(
        api_key=gemini_api_key,
        model_name=DEFAULT_MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION_TEXT
    )
    ai_processor = AIProcessor()
    conversation_history = ConversationHistory(max_history_length=10)
    logger.info("GURU core modules initialized successfully with persona.")
except ValueError as ve:
    logger.error(ve)
    gemini_client = None
except Exception as e:
    logger.critical(f"FATAL: Error initializing GURU components: {e}")
    gemini_client = None

@app.route('/')
def index():
    # Pass the initial welcome message to the template
    return render_template('index.html', initial_message=GURU_WELCOME_MESSAGE)

@app.route('/api/chat', methods=['POST'])
def chat():
    if not gemini_client:
        return jsonify({'error': 'AI service is not available due to initialization issues.'}), 503

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    conversation_history.add_message(role="user", content=user_message)

    def generate_stream():
        try:
            logger.info(f"DEBUG: Sending prompt: '{user_message}'")
            response_stream = gemini_client.generate_response(
                prompt=user_message,
                generation_config=DEFAULT_GENERATION_CONFIG,
                safety_settings=DEFAULT_SAFETY_SETTINGS,
                stream=True
            )

            full_ai_response_for_history = ""
            for chunk in response_stream:
                # Handle chunk based on its structure
                if isinstance(chunk, str):
                    # If the chunk is a plain string
                    processed_chunk = ai_processor.parse_response(chunk)
                    full_ai_response_for_history += processed_chunk
                    yield processed_chunk
                elif hasattr(chunk, 'text') and chunk.text:
                    # If the chunk has a 'text' attribute
                    processed_chunk = ai_processor.parse_response(chunk.text)
                    full_ai_response_for_history += processed_chunk
                    yield processed_chunk
                else:
                    # Log unexpected chunk structure and skip
                    logger.warning(f"Unexpected chunk structure: {chunk}")
                    logger.debug(f"Chunk details: {chunk.__dict__ if hasattr(chunk, '__dict__') else str(chunk)}")
                    continue

            if full_ai_response_for_history:
                conversation_history.add_message(role="model", content=full_ai_response_for_history)
            else:
                yield "Sorry, I couldn't generate a response this time. Please try again."

        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {e}", exc_info=True)
            yield f"Error: Could not stream AI response. {str(e)}"

    return Response(stream_with_context(generate_stream()), mimetype='text/event-stream')

@app.route('/health')
def health_check():
    return jsonify({'status': 'GURU is healthy!'}), 200

if __name__ == '__main__':
    port = os.getenv("PORT")
    if not port or not port.isdigit():
        raise ValueError("FATAL: Invalid or missing PORT in environment variables.")
    port = int(port)
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true", host='0.0.0.0', port=port)