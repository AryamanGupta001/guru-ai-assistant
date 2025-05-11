# modules/context/retrieval.py
# System for retrieving relevant context for the current conversation turn.

class ContextRetriever:
    def __init__(self, short_term_memory_provider, long_term_memory_provider=None):
        """
        Initializes the context retriever.
        :param short_term_memory_provider: An instance of ConversationHistory (or similar).
        :param long_term_memory_provider: An instance of LongTermMemory (or similar).
        """
        self.short_term_memory = short_term_memory_provider
        self.long_term_memory = long_term_memory_provider
        print("ContextRetriever initialized.")

    def retrieve_relevant_context(self, current_query, max_short_term_history=5, search_long_term=True):
        """
        Retrieves relevant context based on the current query.
        Combines short-term conversation history and potentially long-term facts.
        """
        context_parts = []

        # 1. Get recent conversation history
        history = self.short_term_memory.get_history()
        if history:
            # Take the last few items, or implement more sophisticated selection
            relevant_history = history[-max_short_term_history:]
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in relevant_history])
            context_parts.append(f"Recent Conversation:\n{history_str}")

        # 2. Search long-term memory if available and enabled
        if self.long_term_memory and search_long_term:
            related_facts = self.long_term_memory.search_related_facts(current_query, top_k=2)
            if related_facts:
                facts_str = "\n".join([f"- {fact['key']}: {fact['value']}" for fact in related_facts])
                context_parts.append(f"Relevant Information:\n{facts_str}")
        
        # 3. Summarize context if it's too long (placeholder)
        # combined_context = "\n\n".join(context_parts)
        # if len(combined_context) > 1000: # Arbitrary length
        #     # Potentially call an AI model to summarize
        #     combined_context = "Placeholder: Context summarized: " + combined_context[:200] + "..."
            
        return "\n\n".join(context_parts) if context_parts else None

if __name__ == '__main__':
    from .history import ConversationHistory
    from .memory import LongTermMemory

    # Sample setup
    conv_history = ConversationHistory(max_history_length=10)
    conv_history.add_message("user", "What is my name?")
    conv_history.add_message("assistant", "I don't know your name yet.")
    conv_history.add_message("user", "My name is Alex.")
    conv_history.add_message("assistant", "Nice to meet you, Alex!")

    lt_memory = LongTermMemory()
    lt_memory.store_fact("user_name", "Alex") # Storing it based on conversation
    lt_memory.store_fact("project_guru_goal", "Advanced conversational AI")

    retriever = ContextRetriever(short_term_memory_provider=conv_history, long_term_memory_provider=lt_memory)

    query1 = "What was the last thing I said?"
    context1 = retriever.retrieve_relevant_context(query1, search_long_term=False)
    print(f"--- Context for '{query1}' ---\n{context1}\n")

    query2 = "What is the goal of project GURU?"
    context2 = retriever.retrieve_relevant_context(query2)
    print(f"--- Context for '{query2}' ---\n{context2}\n")
    
    query3 = "Do you remember my name?"
    context3 = retriever.retrieve_relevant_context(query3)
    print(f"--- Context for '{query3}' ---\n{context3}\n")
