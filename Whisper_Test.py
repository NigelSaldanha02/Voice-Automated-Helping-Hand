import whisper
import speech_recognition as sr

# listening logic
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

with open("input.wav", "wb") as f:
    f.write(audio.get_wav_data())

model = whisper.load_model("tiny")
result = model.transcribe(audio)

print(result["text"])
