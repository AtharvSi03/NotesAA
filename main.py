from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Initialize FastAPI app
app = FastAPI()

# ✅ TEMP CORS (for debugging)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (TEMP)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set")

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
    return {"message": "NotesAA backend is live 🚀"}

# Generate notes route
@app.post("/generate")
async def generate_notes(data: NotesRequest):

    print("✅ Request received:", data)

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
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
        )

        print("✅ OpenAI raw response:", response)

        # ✅ SUPER SAFE extraction (no crashes)
        generated_text = ""

        if hasattr(response, "output") and response.output:
            for item in response.output:
                if hasattr(item, "content"):
                    for content in item.content:
                        if hasattr(content, "text"):
                            generated_text += content.text

        # fallback if empty
        if not generated_text:
            generated_text = "⚠️ No notes generated. Try again."

        return {
            "generated_notes": generated_text
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "error": str(e)
        }
