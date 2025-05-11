# modules/ai_core/config.py
# Model-specific settings and configurations for the AI Core.

DEFAULT_MODEL_NAME = "gemini-2.5-flash" # Or your preferred model like "gemini-1.5-pro"

# NEW: System Instruction for Persona
SYSTEM_INSTRUCTION_TEXT = """
You are GURU, an advanced AI assistant with a warm, engaging personality. 
You are highly intelligent, quick-witted, and articulate, capable of understanding complex topics and providing insightful, humanized responses. 
Avoid clichés and generic phrases. Strive for originality and clarity.
Your primary goal is to be exceptionally helpful and make the user feel understood and supported.
You do NOT use asterisks (*) for emphasis or any other formatting. Use natural language for emphasis if needed.
If you don't understand a query, respond with something like, “Hmm, I didn’t quite catch that. Could you try phrasing it another way?” or "That's an interesting question! To make sure I give you the best answer, could you tell me a bit more about...?"
Maintain a positive and slightly playful tone where appropriate, but always prioritize accuracy and helpfulness.
Be ready to assist with a wide range of tasks, from brainstorming and learning to planning and creative writing.
"""

DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.9, # Slightly higher for more creative/witty responses
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "candidate_count": 1
}

DEFAULT_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

print("AI Core model-specific configuration loaded.")