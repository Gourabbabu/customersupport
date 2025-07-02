import asyncio
from tts import speak
from stt import listen
from agent_brain import get_response
from dotenv import load_dotenv

load_dotenv()

while True:
    query = listen()
    print("User said:", query)
    reply = get_response(query)
    print("AI:", reply)
    asyncio.run(speak(reply))
