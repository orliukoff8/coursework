from vosk import Model, KaldiRecognizer
import wave
import json

wf = wave.open('output1.wav', 'rb')

chunk = 4096

model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, wf.getframerate())

# # Read data in chunks
data = wf.readframes(chunk)

while data:
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
    data = wf.readframes(chunk)
    # transcribed_text_list.append(result['text'])
final_result = json.loads(recognizer.FinalResult())
print(final_result['text'])
with open('results.txt', 'a') as f:
    f.write(final_result['text'] + '\n')

print("Transcription complete. Output written to transcribed_text.txt.")
