from openai import OpenAI
import os
import requests
from fastapi import UploadFile
import io
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def whisper(file: UploadFile):
    try:
        with open(file, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        print('transcript: ', transcript)
        return transcript["content"]['text']
    except Exception as e:
        # Handle exceptions or errors here
        return {"error": str(e)}

