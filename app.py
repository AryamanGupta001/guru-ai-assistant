from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import modules (placeholders for now)
# from modules.ai_core.gemini_client import GeminiClient
# from modules.context.history import ConversationHistory

app = Flask(__name__)

# Access API key (example)
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     print("GEMINI_API_KEY not found in .env file")
    # Handle missing API key (e.g., raise an error or use a default)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Placeholder: Process message and get AI response
    # ai_response = f"GURU echoes: {user_message}"
    # In a real app, you'd interact with your AI core and context modules here.
    ai_response = "Placeholder AI response."
    
    return jsonify({'reply': ai_response})

@app.route('/health')
def health_check():
    return jsonify({'status': 'GURU is healthy!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
