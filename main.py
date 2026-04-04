from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# Initialize app
app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")


@app.get("/")
async def root():
    return {"message": "NotesAA backend is live 🚀"}


# 🔥 FILE + FORM ENDPOINT
@app.post("/generate")
async def generate_notes(
    owner: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(None),
    useOCR: str = Form("false")
):
    try:
        print("✅ Request:", owner, name, description, file.filename if file else "No file")

        extracted_text = ""

        # 🧠 Read file if exists
        if file:
            contents = await file.read()

            # SIMPLE handling (no OCR yet)
            if file.filename.endswith(".txt"):
                extracted_text = contents.decode("utf-8", errors="ignore")

            else:
                extracted_text = f"[File uploaded: {file.filename}]"

        # 🧠 Prompt
        prompt = f"""
Create clean, well-structured study notes.

Owner: {owner}
Title: {name}
Description: {description}

File Content:
{extracted_text}

Format with:
- Clear headings
- Bullet points
- Short paragraphs
- Organized sections
"""

        response = model.generate_content(prompt)

        return {
            "generated_notes": getattr(response, "text", "⚠️ No response")
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}
