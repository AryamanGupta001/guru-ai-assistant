console.log("GURU main.js loaded.");

// Example: Basic chat interaction (very simplified)
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatOutput = document.getElementById('chat-output');

    if (chatForm) {
        chatForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const userMessage = messageInput.value.trim();
            if (!userMessage) return;

            appendMessage('You: ' + userMessage, chatOutput);
            messageInput.value = ''; // Clear input

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage }),
                });
                const data = await response.json();
                if (data.reply) {
                    appendMessage('GURU: ' + data.reply, chatOutput);
                } else if (data.error) {
                    appendMessage('Error: ' + data.error, chatOutput);
                }
            } catch (error) {
                console.error('Error sending message:', error);
                appendMessage('Error: Could not connect to GURU.', chatOutput);
            }
        });
    }
});

function appendMessage(message, outputElement) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    outputElement.appendChild(messageDiv);
    outputElement.scrollTop = outputElement.scrollHeight; // Scroll to bottom
}

// Add voice UI and animation JS file references or content as needed
// e.g., import './voice_ui.js';
// e.g., import './animation.js';
