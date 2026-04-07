from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import google.generativeai as genai
import os

# Initialize app
app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://atharvsi03.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Gemini setup
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


@app.get("/")
async def root():
    return {"message": "NotesAA backend is live 🚀"}


# 🔥 MULTI-FILE SAFE VERSION
@app.post("/generate")
async def generate_notes(
    owner: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    files: List[UploadFile] = File(None),   # ✅ CHANGED
    useOCR: str = Form("false")
):
    try:
        print(f"✅ Request from {owner}: {name}")

        content_to_send = []

        # 🧠 Handle MULTIPLE files safely
        if files:
            for file in files:
                print(f"📄 File received: {file.filename}")

                file_bytes = await file.read()

                file_part = {
                    "mime_type": file.content_type,
                    "data": file_bytes
                }

                content_to_send.append(file_part)

        # 🧠 Prompt
        prompt = f"""
        Create clean, well-structured study notes based on the provided content.

        Metadata:
        - Owner: {owner}
        - Title: {name}
        - Extra Description: {description}

        Instructions:
        - Use clear headings
        - Use bullet points for readability
        - Keep paragraphs short
        - Organize by logical sections
        - If files are provided, combine and prioritize their contents
        - Do NOT use bold formatting anywhere
        - If something is important, put the "❗" emoji in front and at the back of the word

        """

        content_to_send.append(prompt)

        # 🧠 Generate
        response = model.generate_content(content_to_send)

        return {
            "generated_notes": getattr(response, "text", "⚠️ No response from AI")
        }

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"error": f"Internal Server Error: {str(e)}"}
