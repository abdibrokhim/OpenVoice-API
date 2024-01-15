from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from voice_over_service import create_custom_voice_over

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
async def voice_over_endpoint(query: str, speaker: str, reference_speaker: str):
    try:
        file_path = await create_custom_voice_over(text=query, speaker=speaker, reference_speaker=reference_speaker)
        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
