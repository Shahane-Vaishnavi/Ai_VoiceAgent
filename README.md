# AI Voice Agent 🎙️

An evolving AI voice agent built to handle text-to-speech, speech-to-text, and smart voice switching, with more powerful features coming soon.

## Features

- **Text-to-Speech (TTS)**: Convert text into natural-sounding speech using Google Text-to-Speech (gTTS)
- **Speech-to-Text (STT)**: Transcribe audio recordings using AssemblyAI
- **Audio Recording**: Record audio directly from your browser
- **Real-time Transcription**: Get instant transcriptions of your recorded audio
- **Modern UI**: Beautiful, responsive interface with gradient backgrounds and smooth animations

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Speech-to-Text**: AssemblyAI API
- **Server**: Uvicorn

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn gtts assemblyai python-multipart
   ```

   Or create a `requirements.txt` file with:
   ```
   fastapi==0.116.1
   uvicorn==0.35.0
   gTTS==2.5.4
   assemblyai==0.42.1
   python-multipart
   ```

   Then install:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up AssemblyAI API Key**:
   - Get your API key from [AssemblyAI](https://www.assemblyai.com/)
   - Update the API key in `gain.py` (line 104) or use environment variables

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn gain:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure

```
Ai_VoiceAgent/
├── gain.py              # FastAPI backend server
├── index.html           # Main HTML file
├── static/
│   ├── styles.css       # CSS styles
│   ├── script.js        # JavaScript functionality
│   ├── uploads/         # Uploaded audio files
│   └── favicon.ico      # Site favicon
└── README.md            # This file
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `POST /generate-voice/` - Generates audio from text (TTS)
- `POST /upload` - Uploads audio files
- `POST /transcribe/file` - Transcribes uploaded audio files
- `POST /speak` - Alternative TTS endpoint (form-based)

## Usage

### Text-to-Speech
1. Enter text in the textarea
2. Click "🎙️ Speak Now"
3. The generated audio will play automatically

### Speech-to-Text
1. Click "Start Recording" to begin recording audio
2. Speak into your microphone
3. Click "Stop Recording" when finished
4. The audio will be uploaded and transcribed automatically
5. View the transcription below the audio player

## Browser Compatibility

- Requires a modern browser with MediaRecorder API support
- Chrome, Firefox, Edge, and Safari (latest versions) are supported
- Microphone permissions are required for recording functionality

## Development

The server runs with auto-reload enabled, so changes to Python files will automatically restart the server. For frontend changes, refresh your browser.

## Future Features

- Multiple voice options and languages
- Voice cloning capabilities
- Real-time voice switching
- Enhanced transcription accuracy
- Audio file format conversion
- Voice command recognition

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Note**: Make sure to keep your API keys secure. Consider using environment variables for production deployments.
