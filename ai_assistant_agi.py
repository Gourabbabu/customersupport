#!/usr/bin/env python3
import sys
import os
from agent_brain import get_response
from stt import transcribe_wav
from tts import synthesize_to_wav
import uuid

def agi_write(cmd):
    sys.stdout.write(cmd + '\n')
    sys.stdout.flush()

def agi_read():
    return sys.stdin.readline().strip()

def main():
    greeting_wav = "/tmp/greeting.wav"
    synthesize_to_wav("Hello, you are connected to the AI assistant. Please state your query after the beep.", greeting_wav)
    agi_write(f'EXEC Playback {greeting_wav}')
    agi_read()

    record_wav = f"/tmp/recording_{uuid.uuid4()}.wav"
    agi_write(f'RECORD FILE {record_wav[:-4]} wav "#" 10000 0 s=1')
    agi_read()

    transcript = transcribe_wav(record_wav)
    response = get_response(transcript)
    response_wav = f"/tmp/response_{uuid.uuid4()}.wav"
    synthesize_to_wav(response, response_wav)
    agi_write(f'EXEC Playback {response_wav}')
    agi_read()
    agi_write('HANGUP')

if __name__ == "__main__":
    main() 