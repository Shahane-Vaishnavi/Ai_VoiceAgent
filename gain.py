from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os

app = FastAPI()

# Create static folder if not exists
os.makedirs("static", exist_ok=True)

# Input model
class TextInput(BaseModel):
    text: str

# Serve static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML UI
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")


# API endpoint for text-to-speech
@app.post("/generate-voice/")
async def generate_voice(data: TextInput):
    if not data.text.strip():
        return {"error": "Text input is empty."}

    filename = f"{uuid.uuid4().hex}.mp3"
    path = f"static/{filename}"

    tts = gTTS(data.text)
    tts.save(path)

    return {"audio_url": f"/static/{filename}"}
