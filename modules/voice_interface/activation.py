# modules/voice_interface/activation.py
# Handles wake word detection system.

class WakeWordDetector:
    def __init__(self, wake_word="hey guru", library_choice="porcupine_or_custom"):
        """
        Initializes the wake word detector.
        :param wake_word: The phrase to listen for.
        :param library_choice: Specifies the underlying detection engine (e.g., Porcupine, Snowboy, custom).
        """
        self.wake_word = wake_word.lower()
        self.library = library_choice
        self._is_listening = False
        print(f"WakeWordDetector initialized for '{self.wake_word}' (simulating: {self.library}).")

    def start_listening(self, on_wake_word_detected_callback):
        """
        Starts listening for the wake word in the audio stream.
        :param on_wake_word_detected_callback: Function to call when wake word is detected.
        """
        if self._is_listening:
            print("Already listening for wake word.")
            return

        self._is_listening = True
        print(f"Starting to listen for wake word '{self.wake_word}'...")
        
        # Placeholder for actual wake word detection logic loop
        # In a real system, this would involve:
        # 1. Capturing audio frames continuously.
        # 2. Feeding frames to the chosen wake word engine (e.g., Porcupine).
        # 3. If the engine detects the wake word, call `on_wake_word_detected_callback()`.
        # This often runs in a separate thread or process.

        # Simulating detection for demonstration
        # import time
        # import threading
        # def simulate():
        #     time.sleep(5) # Simulate some listening time
        #     if self._is_listening:
        #         print(f"Wake word '{self.wake_word}' detected (simulated)!")
        #         on_wake_word_detected_callback()
        # threading.Thread(target=simulate, daemon=True).start()
        
        print(f"(Simulated) To test, manually call `on_wake_word_detected_callback` or integrate a real engine.")


    def stop_listening(self):
        """Stops listening for the wake word."""
        if not self._is_listening:
            print("Not currently listening for wake word.")
            return
        self._is_listening = False
        print("Stopped listening for wake word.")

    def is_listening(self):
        return self._is_listening

# Example callback function
def handle_wake_word():
    print("CALLBACK: Wake word detected! GURU is now active.")
    # Trigger main speech recognition or other actions here

if __name__ == '__main__':
    detector = WakeWordDetector(wake_word="Hey GURU")
    
    if not detector.is_listening():
        detector.start_listening(on_wake_word_detected_callback=handle_wake_word)
    
    print("Wake word detector is running (simulated). Check console for simulated detection or manually trigger callback.")
    # To simulate detection if not using threading in the example:
    # if detector.is_listening():
    #     print("\nSimulating manual trigger of wake word detection...")
    #     handle_wake_word() # Manually call for testing
    
    # To stop:
    # detector.stop_listening()
    # print(f"Detector listening status: {detector.is_listening()}")
    
    # Keep the script running for a bit if using a threaded simulation
    import time
    try:
        for i in range(10):
            if not detector.is_listening(): break
            print(f"Still listening... ({i+1}/10)")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if detector.is_listening():
            detector.stop_listening()
