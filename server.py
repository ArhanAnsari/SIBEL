from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from main_without_gui import get_gemini_response, take_command, speak

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_query(request: QueryRequest):
    try:
        response = get_gemini_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/speak")
async def speak_text(text: str):
    speak(text)
    return {"message": "Speaking now"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
