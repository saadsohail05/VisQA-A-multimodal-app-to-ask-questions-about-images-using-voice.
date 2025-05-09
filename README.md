# VisQA: A Multimodal App to Ask Questions About Images Using Voice

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Demo Video](https://img.shields.io/badge/Demo-Watch%20Video-red)](https://drive.google.com/file/d/1f7SY8nOdlaNxwcduqBFKfpWe5x9tqKto/view?usp=sharing)

VisQA is a multimodal application that allows users to ask questions about images using voice commands. The app leverages advanced AI technologies for speech recognition, visual understanding, and text-to-speech synthesis to create a seamless interactive experience.

## Features

- **Voice-Based Querying**: Ask questions about images through an intuitive voice interface
- **Automatic Speech Recognition (ASR)**: Converts voice questions to text using Groq's Whisper Large V3 model
- **Visual Understanding**: Analyzes images and responds to queries using NVIDIA's Kosmos-2 visual language model
- **Text-to-Speech (TTS)**: Converts text answers back to speech for fully voice-based interaction
- **User-Friendly Interface**: Simple three-step process with clear visual guidance
- **Edit Transcriptions**: Option to edit transcribed text for improved accuracy

## How It Works

1. **Upload an Image**: Start by uploading an image you want to ask questions about
2. **Record Your Question**: Use the built-in audio recorder to ask a question about the image
3. **Get Answer**: The application analyzes your image and question, then provides both text and audio responses

## Tech Stack

- **Frontend**: Streamlit
- **Audio Recording**: Streamlit-AudioRec
- **Speech-to-Text**: Groq API (Whisper Large V3)
- **Visual Question Answering**: NVIDIA API (Kosmos-2 VLM)
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Image Processing**: Pillow

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/VisQA.git
   cd VisQA
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   NVIDIA_API_KEY=your_nvidia_api_key
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Follow the on-screen instructions to use the application:
   - Upload an image
   - Record your question about the image
   - Click the "Ask Question" button to get your answer

## Project Structure

```
VisQA/
├── app.py             # Main Streamlit application
├── asr.py             # Speech-to-text functionality
├── qa.py              # Image analysis and question answering
├── tts.py             # Text-to-speech functionality
├── requirements.txt   # Project dependencies
├── temp_files/        # Temporary storage for uploaded files (auto-created)
└── README.md          # Project documentation
```

## Requirements

- Python 3.9+
- API keys for Groq and NVIDIA services
- Internet connection for API calls

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Groq](https://groq.com/) for the Whisper ASR API
- [NVIDIA](https://www.nvidia.com/) for the Kosmos-2 VLM API
- [Streamlit](https://streamlit.io/) for the web application framework
- [Google Text-to-Speech](https://cloud.google.com/text-to-speech) for the TTS functionality

---
