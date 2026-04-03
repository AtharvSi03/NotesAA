from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Initialize app
app = FastAPI()

# CORS configuration (SAFE VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow everything TEMP
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check API key properly
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Request model
class NotesRequest(BaseModel):
    owner: str
    name: str
    description: str

# Root route
@app.get("/")
async def root():
    return {"message": "NotesAA backend is live"}

# Generate notes route
@app.post("/generate")
async def generate_notes(data: NotesRequest):

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

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "You generate professional academic study notes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        # Safe extraction
        generated_text = response.output_text

        return {
            "generated_notes": generated_text
        }

    except Exception as e:
        print("❌ ERROR:", e)  # shows in Render logs
        return {
            "error": str(e)
        }
