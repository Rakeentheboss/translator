from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class translate(BaseModel):
    model: str
    prompt: str
    target_language: str
    target_display: str
    input_text: str
    Temperature: float
    Max_tokens: int

@app.post("/translate")
async def translate(request: translate):
    translated_text = f"Translated '{request.input_text}' to {request.target_language} using {request.model}."
    return {"translated_text": translated_text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)