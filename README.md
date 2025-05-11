# GURU - Advanced Conversational AI Assistant

![GURU AI Assistant](https://img.shields.io/badge/AI%20Assistant-GURU-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

GURU is a sophisticated voice-activated AI assistant leveraging Google's Gemini API to deliver natural, context-aware conversations with sentiment analysis capabilities.

## 📋 Features

- **Natural Language Understanding**: Powered by the Gemini API for human-like comprehension
- **Contextual Memory**: Maintains conversation history for coherent multi-turn exchanges
- **Voice Activation**: Hands-free interaction through voice commands
- **Multi-Modal Interface**: Both text and voice interaction options
- **Sentiment Analysis**: Tailors responses based on detected emotional tone
- **Responsive Web Interface**: Clean, accessible design that works across devices

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI/ML**: Google Gemini API
- **Speech Processing**: Web Speech API (or alternative libraries)
- **Sentiment Analysis**: TextBlob/NLTK/Custom implementation

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Modern web browser supporting the Web Speech API

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/guru-ai-assistant.git
   cd guru-ai-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file to add your Gemini API key and other configurations
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
guru-ai-assistant/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── static/                 # Frontend assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Images and icons
├── templates/              # HTML templates
├── modules/
│   ├── ai_core/            # Gemini API integration & NLP logic
│   ├── voice_interface/    # Speech recognition and synthesis
│   ├── sentiment/          # Sentiment analysis engine
│   └── context/            # Conversation context management
└── tests/                  # Test suite
```

## 🧩 Component Details

### Core AI Module

The heart of GURU, responsible for understanding user queries and generating appropriate responses.

- **Gemini API Client**: Handles API communication, request formatting, and response parsing
- **NLP Processor**: Additional language processing beyond Gemini's capabilities
- **Response Generator**: Constructs contextually appropriate answers

### Voice Interface

Enables hands-free interaction with the assistant.

- **Speech Recognition**: Converts spoken words to text
- **Text-to-Speech**: Converts response text to natural speech
- **Wake Word Detection**: Listens for activation phrases (e.g., "Hey GURU")

### Web Application

A Flask-based interface allowing both text and voice interactions.

- **Responsive UI**: Adapts seamlessly to different screen sizes
- **Real-time Processing**: Asynchronous handling of requests
- **Session Management**: Maintains user sessions securely

### Sentiment Analysis

Detects emotional context to personalize interactions.

- **Emotion Classification**: Identifies user sentiment (positive, negative, neutral)
- **Response Modulation**: Adjusts tone and content based on detected emotions
- **Feedback Loop**: Learns from user reactions over time

### Integration Layer

Connects all components into a cohesive system.

- **Module Communication**: Standardized interfaces between components
- **State Management**: Maintains application state across requests
- **Configuration System**: Centralizes settings and customizations

## 🛣️ Development Roadmap

1. **Phase 1: Core Setup**
   - Establish Flask application structure
   - Implement basic Gemini API integration
   - Create minimalistic UI for text interactions

2. **Phase 2: Voice Capabilities**
   - Add speech recognition
   - Implement text-to-speech output
   - Develop wake word detection

3. **Phase 3: Context & Intelligence**
   - Build conversation context management
   - Enhance response quality with additional processing
   - Implement sentiment analysis

4. **Phase 4: UI Enhancement**
   - Develop responsive design
   - Add visual feedback for voice interactions
   - Implement accessibility features

5. **Phase 5: Testing & Refinement**
   - Comprehensive testing across devices
   - Performance optimization
   - User experience improvements

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact

Aryaman Gupta - [aryamangupta353@gmail.com]

Project Link: [https://github.com/aryamangupta001/guru-ai-assistant](https://github.com/aryamangupta001/guru-ai-assistant)
