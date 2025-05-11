# modules/context/memory.py
# For long-term storage and retrieval of important information.

class LongTermMemory:
    def __init__(self, storage_path="long_term_memory.db"):
        """
        Initializes long-term memory.
        Could use a simple file, a database (SQLite), or a vector DB.
        :param storage_path: Path to where memory is stored.
        """
        self.storage_path = storage_path
        self.memory_data = {} # Simplified in-memory storage for this example
        print(f"LongTermMemory initialized. Storage (simulated): {storage_path}")
        # self._load_memory() # In a real app

    def store_fact(self, key, value):
        """Stores an important fact or piece of information."""
        self.memory_data[key] = value
        print(f"Stored fact: '{key}' -> '{value}'")
        # self._save_memory() # In a real app

    def retrieve_fact(self, key):
        """Retrieves a fact by its key."""
        return self.memory_data.get(key)

    def search_related_facts(self, query_text, top_k=3):
        """
        Placeholder: Searches for facts related to a query.
        Would typically involve embedding and similarity search for a real implementation.
        """
        # Very naive keyword search for demonstration
        results = []
        for key, value in self.memory_data.items():
            if query_text.lower() in key.lower() or query_text.lower() in str(value).lower():
                results.append({"key": key, "value": value})
            if len(results) >= top_k:
                break
        return results

    def _load_memory(self):
        """Placeholder for loading memory from persistent storage."""
        # Example: if os.path.exists(self.storage_path): load data
        print(f"Attempting to load memory from {self.storage_path} (simulated).")
        pass

    def _save_memory(self):
        """Placeholder for saving memory to persistent storage."""
        # Example: with open(self.storage_path, 'w') as f: json.dump(self.memory_data, f)
        print(f"Attempting to save memory to {self.storage_path} (simulated).")
        pass

if __name__ == '__main__':
    ltm = LongTermMemory()
    ltm.store_fact("user_name", "Aryaman")
    ltm.store_fact("user_preference_topic", "AI technology")
    ltm.store_fact("important_meeting_date", "2024-12-25")
    
    print("Retrieved 'user_name':", ltm.retrieve_fact("user_name"))
    print("Search related to 'AI':", ltm.search_related_facts("AI"))
    print("Search related to 'meeting':", ltm.search_related_facts("meeting"))
