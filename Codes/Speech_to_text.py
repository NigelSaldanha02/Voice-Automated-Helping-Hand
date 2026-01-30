import speech_recognition as sr

# listening logic
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, could not understand")

# keyword logic
classes = ["orange", "banana", "apple", "water bottle", "medicine", "remote", "cup", "glass"]

keyword = []

for object in classes:
    if object in text:
        keyword.append(object)

if keyword:        
     print("Object is present in classes")
else:
    print("No such object found")

# find keyword in camera logic
