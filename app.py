from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ----- IMPORT YOUR MODULES -----
from modules.ai_core.gemini_client import GeminiClient
from modules.ai_core.processor import AIProcessor
from modules.ai_core.config import DEFAULT_MODEL_NAME, DEFAULT_GENERATION_CONFIG, DEFAULT_SAFETY_SETTINGS # Import AI core configs
from modules.context.history import ConversationHistory
# from modules.sentiment.analyzer import SentimentAnalyzer # Uncomment when ready
# from modules.sentiment.response_modifier import ResponseModifier # Uncomment when ready

app = Flask(__name__)

# ----- INITIALIZE YOUR MODULES -----
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("FATAL: GEMINI_API_KEY not found in .env file. Please set it.")
    
    gemini_client = GeminiClient(api_key=gemini_api_key, model_name=DEFAULT_MODEL_NAME)
    ai_processor = AIProcessor()
    conversation_history = ConversationHistory(max_history_length=10) # Manage history per session later
    # sentiment_analyzer = SentimentAnalyzer() # Uncomment when ready
    # response_modifier = ResponseModifier() # Uncomment when ready
    print("GURU core modules initialized successfully.")

except ValueError as ve:
    print(ve)
    # You might want to exit or disable AI features if critical components fail
    gemini_client = None 
except Exception as e:
    print(f"FATAL: Error initializing GURU components: {e}")
    gemini_client = None # Disable AI if initialization fails

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not gemini_client:
        return jsonify({'error': 'AI service is not available due to initialization issues.'}), 503

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # 1. Add user message to history
    conversation_history.add_message(role="user", content=user_message)

    # 2. Format the prompt (potentially with history)
    # For now, let's send just the user message, you can enhance this later
    # current_history_for_prompt = conversation_history.get_history()
    # formatted_prompt = ai_processor.format_prompt(user_message, conversation_history=current_history_for_prompt)
    # For Gemini, a simple list of content objects is often preferred for chat history
    
    # Construct messages list compatible with Gemini's generate_content if using multi-turn chat
    # For a single turn from user for now:
    current_prompt = user_message 
    
    # To use conversation history for multi-turn chat (more advanced):
    # messages_for_gemini = []
    # for entry in conversation_history.get_history():
    #     # Gemini API expects 'user' and 'model' roles for chat history
    #     role = entry['role'] if entry['role'] == 'user' else 'model' 
    #     messages_for_gemini.append({'role': role, 'parts': [{'text': entry['content']}]})
    # current_prompt = messages_for_gemini # Pass this to generate_response

    print(f"Sending to Gemini: {current_prompt}")

    # 3. Get response from Gemini
    ai_raw_response = gemini_client.generate_response(
        prompt=current_prompt, # Send the formatted prompt
        generation_config=DEFAULT_GENERATION_CONFIG,
        safety_settings=DEFAULT_SAFETY_SETTINGS
    )
    print(f"Raw response from Gemini: {ai_raw_response}")

    # 4. Parse the response (if needed)
    ai_final_response = ai_processor.parse_response(ai_raw_response)

    # 5. (Optional) Analyze sentiment of user_message and AI response
    # user_sentiment = sentiment_analyzer.analyze_sentiment(user_message)
    # ai_final_response = response_modifier.modify_response_based_on_sentiment(ai_final_response, user_sentiment)

    # 6. Add AI response to history
    conversation_history.add_message(role="model", content=ai_final_response) # Use 'model' for Gemini's role

    return jsonify({'reply': ai_final_response})

@app.route('/health')
def health_check():
    return jsonify({'status': 'GURU is healthy!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)