from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# ✅ TEMP CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Request model
class NotesRequest(BaseModel):
    owner: str
    name: str
    description: str

# Root route
@app.get("/")
async def root():
    return {"message": "NotesAA backend is live 🚀"}

# ✅ Gemini-powered route
@app.post("/generate")
async def generate_notes(data: NotesRequest):

    print("✅ Request received:", data)

    try:
        prompt = f"""
Create clean, well-structured study notes.

Owner: {data.owner}
Title: {data.name}
Description: {data.description}

Format with:
- Clear headings
- Bullet points
- Short paragraphs
- Organized sections
"""

        response = model.generate_content(prompt)

        return {
            "generated_notes": response.text
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "error": str(e)
        }
