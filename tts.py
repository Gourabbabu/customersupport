import asyncio
from edge_tts import Communicate
from pydub import AudioSegment
from pydub.playback import play
import os
import uuid

async def speak(text):
    try:
        filename = f"voice_{uuid.uuid4()}.mp3"
        communicate = Communicate(text, voice="en-IN-PrabhatNeural")
        await communicate.save(filename)

        audio = AudioSegment.from_file(filename, format="mp3")
        play(audio)
        os.remove(filename)
    except Exception as e:
        print(f"TTS error: {e}")
