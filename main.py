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
  files: List[UploadFile] = File(None),
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
    - Description: {description}

    Instructions:

    - Get straight to the point
    - Use clear headings for every section
    - Use bullet points to improve readability
    - Keep paragraphs short and concise
    - Organize content in a logical flow
    - If multiple files are provided, combine them and prioritize the most relevant information
    - Avoid unnecessary explanations or filler text
    - If you have to bold something put "<b>" at the front and "</b>" at the back of the word
    - If you have to italicize something put "<i>" at the front and "</i" at the back of the word
    - If you have to underline something put "<u">" at the front and "</u>" at the back of the word
    - Maintain clarity over complexity
    - Focus on delivering useful, actionable information
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
