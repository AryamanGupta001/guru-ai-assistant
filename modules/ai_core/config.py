# modules/ai_core/config.py
# Model-specific settings and configurations for the AI Core.

# Example: Gemini Model settings
# These could be defaults if not overridden by dynamic requests
DEFAULT_MODEL_NAME = "gemini-1.5-flash" # Or "gemini-pro", "gemini-1.0-pro", etc.

DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 32, # Adjust based on model and desired output
    "max_output_tokens": 1024, # Or 2048, 8192 depending on model
    "candidate_count": 1
}

# Example: Safety settings
# See Google AI documentation for categories and thresholds
# HARM_CATEGORY_UNSPECIFIED, HARM_CATEGORY_DEROGATORY, HARM_CATEGORY_TOXICITY, 
# HARM_CATEGORY_VIOLENCE, HARM_CATEGORY_SEXUAL, HARM_CATEGORY_MEDICAL, HARM_CATEGORY_DANGEROUS
DEFAULT_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# You might also include things like:
# - Prompt engineering templates or prefixes/suffixes
# - Retry mechanism settings (max_retries, delay_factor)
# - Logging levels specific to AI interactions

print("AI Core model-specific configuration loaded.")
