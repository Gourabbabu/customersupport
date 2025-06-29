import asyncio
from tts import speak
from stt import listen
from agent_brain import get_response

while True:
    query = listen()
    print("User said:", query)
    reply = get_response(query)
    print("AI:", reply)
    asyncio.run(speak(reply))
