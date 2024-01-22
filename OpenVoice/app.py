from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from voice_over_service import create_custom_voice_over
# from whisper_api import whisper
from tempfile import NamedTemporaryFile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/api/v1/voice-over/")
async def voice_over_endpoint(query: str, speaker: str, language: str, reference_speaker: UploadFile = File(...)):
    try:
        # Save the file to a temporary file
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(reference_speaker.filename)[1]) as temp_file:
            contents = await reference_speaker.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Transcribe the file
        file_path = await create_custom_voice_over(text=query, speaker=speaker, reference_speaker=temp_file_path, language=language)
        
        # Optionally, delete the file after processing
        os.remove(temp_file_path)

        return {"file_path": file_path}
    except Exception as e:        
        # Cleanup if an error occurs
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/api/v1/transcribe/")
# async def transcribe_endpoint(file: UploadFile = File(...)):
#     try:
#         # Save the file to a temporary file
#         with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
#             contents = await file.read()
#             temp_file.write(contents)
#             temp_file_path = temp_file.name

#         # Transcribe the file
#         content = await whisper(temp_file_path)

#         # Optionally, delete the file after processing
#         os.remove(temp_file_path)

#         return {"content": content}
#     except Exception as e:
#         # Cleanup if an error occurs
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)
#         raise HTTPException(status_code=500, detail=str(e)) 

# if __name__ == "__main__":
#     uvicorn.run(app, port=8000)
