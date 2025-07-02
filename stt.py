import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return "Sorry, I didn't understand that."

def transcribe_wav(wav_path):
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio)
        except:
            return "Sorry, I didn't understand that."
