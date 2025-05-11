# modules/context/history.py
# Manages conversation history for short-term context.

class ConversationHistory:
    def __init__(self, max_history_length=10):
        """
        Initializes conversation history.
        :param max_history_length: Maximum number of turns to keep in history.
        """
        self.history = []
        self.max_history_length = max_history_length
        print(f"ConversationHistory initialized with max length: {max_history_length}")

    def add_message(self, role, content):
        """
        Adds a message to the history.
        :param role: 'user' or 'assistant' (or 'model' for Gemini)
        :param content: The message text.
        """
        if role not in ['user', 'assistant', 'model']:
            raise ValueError("Role must be 'user', 'assistant', or 'model'.")
        
        self.history.append({"role": role, "content": content})
        self._trim_history()

    def get_history(self):
        """Returns the current conversation history."""
        return list(self.history) # Return a copy

    def _trim_history(self):
        """Ensures history does not exceed max_history_length."""
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]
    
    def clear_history(self):
        """Clears the conversation history."""
        self.history = []
        print("Conversation history cleared.")

    # --- Context Window Management & Summarization (Placeholders) ---
    def get_context_window(self, max_tokens=1000):
        """
        Placeholder: Returns a part of the history that fits within a token limit.
        Actual implementation would need a tokenizer.
        """
        # This is a very naive implementation based on message count.
        # A real version needs token counting.
        return self.get_history() 

    def summarize_conversation(self):
        """
        Placeholder: Summarizes older parts of the conversation.
        This could involve calling an AI model.
        """
        if len(self.history) > 5: # Arbitrary threshold
            return "Placeholder: Conversation is getting long, summary might be needed."
        return None

if __name__ == '__main__':
    hist = ConversationHistory(max_history_length=3)
    hist.add_message("user", "Hello GURU")
    hist.add_message("assistant", "Hi there! How can I help?")
    hist.add_message("user", "Tell me a joke.")
    print("History (1):", hist.get_history())
    hist.add_message("assistant", "Why did the scarecrow win an award? Because he was outstanding in his field!")
    print("History (2) (trimmed):", hist.get_history())
    summary_needed = hist.summarize_conversation()
    if summary_needed:
        print(summary_needed)
    hist.clear_history()
    print("History (3) (cleared):", hist.get_history())
