from fastapi import FastAPI,Request, UploadFile, File
from fastapi import Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import assemblyai as aai
import uuid
import os

app = FastAPI()

# Create folders if not exist
os.makedirs("static", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# BaseModel for API input
class TextInput(BaseModel):
    text: str

# Serve UI page
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Serve favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Text-to-Speech via API (for JS/AJAX)
@app.post("/generate-voice/")
async def generate_voice(request: Request):
    data = await request.json()
    text = data.get("text", "")
    language = data.get("voice", "en")  # you can improve this logic

    if not text:
        return JSONResponse({"error": "Text is empty"}, status_code=400)

    tts = gTTS(text, lang=language)
    filename = "sample.mp3"
    path = os.path.join("static", filename)
    tts.save(path)

    return {"audio_url": f"/static/{filename}"}

# Upload audio file
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join("static/uploads", filename)

        contents = await file.read()
        with open(path, "wb") as f:
            f.write(contents)

        return {
            "status": "success",
            "url": f"/static/uploads/{filename}",
            "name": file.filename,
            "type": file.content_type
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# HTML form text-to-speech
@app.post("/speak", response_class=HTMLResponse)
async def speak(text: str = Form(...)):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("static", filename)

    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        return f"""
        <h2>Voice Generated</h2>
        <audio controls autoplay>
            <source src="/static/{filename}" type="audio/mpeg">
        </audio>
        <br><a href="/">Go back</a>
        """
    except Exception as e:
        return f"<p>Error: {e}</p><br><a href='/'>Go back</a>"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup my AssemblyAI API key
aai.settings.api_key = "ab8793e1e8e74c7daa7285556d6aa34a"

@app.post("/transcribe/file")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_bytes)

    return {"transcription": transcript.text}

@app.post("/generate-voice/")
async def generate_voice(data: dict):
    text = data["text"]
    # Dummy URL for now, integrate TTS if needed
    return {"audio_url": "/sample-audio.mp3"}