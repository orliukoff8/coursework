import os
import wave
import json

from pathlib import Path

import time

import uvicorn

from fastapi import FastAPI, UploadFile

from vosk import Model, KaldiRecognizer

app = FastAPI()


chunk = 4096

model = Model("vosk-model-small-en-us-0.15")

samples_dir = Path('samples')
transcriptions_dir = Path('transcriptions')

if not samples_dir.exists():
    os.mkdir(samples_dir)

if not transcriptions_dir.exists():
    os.mkdir(transcriptions_dir)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, name: str):
    start_time = time.time()
    content = await file.read()
    local_filename = samples_dir / file.filename
    with open(str(local_filename), 'wb') as f:
        f.write(content)

    wf = wave.open(str(local_filename), 'rb')

    recognizer = KaldiRecognizer(model, wf.getframerate())

    # # Read data in chunks
    data = wf.readframes(chunk)

    while data:
        recognizer.AcceptWaveform(data)
        data = wf.readframes(chunk)

    final_result = json.loads(recognizer.FinalResult())
    print(final_result['text'])
    with open(transcriptions_dir / file.filename, 'a') as f:
        f.write(final_result['text'] + '\n')

    print("Transcription complete. Output written to transcribed_text.txt.")
    print(f'Processing took: {time.time() - start_time} seconds')
    return final_result


if __name__ == "__main__":
    uvicorn.run(app)
