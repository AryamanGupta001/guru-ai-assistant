console.log("GURU main.js loaded.");

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatOutput = document.getElementById('chat-output');

    // Display initial GURU message
    if (initialGuruMessage && chatOutput.children.length === 0) { // Check if chat is empty
        appendMessage('GURU: ' + initialGuruMessage, chatOutput, 'guru-message');
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const userMessage = messageInput.value.trim();
            if (!userMessage) return;

            appendMessage('You: ' + userMessage, chatOutput, 'user-message');
            messageInput.value = ''; 

            let guruMessageDiv = null; // To hold the streaming AI response

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage }),
                });

                if (!response.ok) {
                    // Handle HTTP errors from the Flask server
                    const errorData = await response.json().catch(() => ({ error: "Unknown server error" }));
                    appendMessage('Error: ' + (errorData.error || `Server error ${response.status}`), chatOutput, 'error-message');
                    return;
                }
                
                // Handle streaming response
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let firstChunk = true;

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;

                    const chunkText = decoder.decode(value, { stream: true });
                    
                    if (chunkText.toLowerCase().startsWith("error:")) {
                        if (guruMessageDiv) { // If we started displaying something
                            guruMessageDiv.textContent += " " + chunkText; // Append error to existing div
                        } else {
                            appendMessage(chunkText, chatOutput, 'error-message');
                        }
                        return; // Stop processing on error
                    }

                    if (firstChunk) {
                        guruMessageDiv = appendMessage('GURU: ' + chunkText, chatOutput, 'guru-message', true);
                        firstChunk = false;
                    } else if (guruMessageDiv) {
                        guruMessageDiv.textContent += chunkText;
                        chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll as content streams
                    }
                }

            } catch (error) {
                console.error('Error sending/receiving message:', error);
                if (guruMessageDiv) {
                     guruMessageDiv.textContent += ' (Error: Stream interrupted)';
                } else {
                    appendMessage('Error: Could not connect to GURU or stream interrupted.', chatOutput, 'error-message');
                }
            }
        });
    }
});

// Modified appendMessage to return the new div for streaming and add CSS classes
function appendMessage(message, outputElement, messageClass = '', returnDiv = false) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    if (messageClass) {
        messageDiv.classList.add(messageClass);
    }
    outputElement.appendChild(messageDiv);
    outputElement.scrollTop = outputElement.scrollHeight;
    if (returnDiv) {
        return messageDiv;
    }
}
// Add voice UI and animation JS file references or content as needed
// e.g., import './voice_ui.js';
// e.g., import './animation.js';
