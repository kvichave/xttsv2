from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid
import os

app = FastAPI()

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name=MODEL_NAME, gpu=True)

# Global variable to cache speaker path
cached_speaker_path = None


@app.post("/set-speaker")
async def set_speaker(file: UploadFile = File(...)):
    global cached_speaker_path

    # Save uploaded file to a known location
    speaker_path = f"speaker_{uuid.uuid4().hex}.wav"
    with open(speaker_path, "wb") as f:
        f.write(await file.read())

    cached_speaker_path = speaker_path
    return {"message": "Speaker uploaded successfully."}


@app.post("/speak")
async def speak(text: str = Form(...), language: str = Form("en")):
    
    global cached_speaker_path

    if not cached_speaker_path or not os.path.exists(cached_speaker_path):
        raise HTTPException(status_code=400, detail="Speaker not set. Upload it to /set-speaker first.")

    output_path = f"output_{uuid.uuid4().hex}.wav"

    tts.tts_to_file(
        text=text,
        speaker_wav=cached_speaker_path,
        language=language,
        file_path=output_path
    )

    return FileResponse(output_path, media_type="audio/wav", filename="cloned_voice.wav")
