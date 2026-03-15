from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Initialize FastAPI
app = FastAPI()

# Enable CORS (lock this later to your domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class NotesRequest(BaseModel):
    owner: str
    name: str
    description: str

# Root route (health check)
@app.get("/")
async def root():
    return {"message": "NotesAA backend is live 🚀"}

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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate professional academic study notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        generated_text = response.choices[0].message.content

        return {
            "generated_notes": generated_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }