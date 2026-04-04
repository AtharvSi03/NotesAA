from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# Initialize app
app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Gemini setup
# Make sure GEMINI_API_KEY is set in your Render Environment Variables!
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


@app.get("/")
async def root():
    return {"message": "NotesAA backend is live 🚀"}


# 🔥 FIXED FILE + FORM ENDPOINT
@app.post("/generate")
async def generate_notes(
    owner: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(None),
    useOCR: str = Form("false")
):
    try:
        print(f"✅ Request from {owner}: {name} (File: {file.filename if file else 'None'})")

        content_to_send = []

        # 🧠 Handle File if it exists
        if file:
            # Read the raw bytes from the uploaded file
            file_bytes = await file.read()
            
            # Create the part object for the Gemini API
            file_part = {
                "mime_type": file.content_type,  # e.g., 'application/pdf' or 'image/png'
                "data": file_bytes
            }
            content_to_send.append(file_part)

        # 🧠 Create the Text Prompt
        prompt = f"""
        Create clean, well-structured study notes based on the provided content.

        Metadata:
        - Owner: {owner}
        - Title: {name}
        - Extra Description: {description}

        Instructions:
        - Use clear headings (Markdown ## and ###)
        - Use bullet points for readability
        - Keep paragraphs short
        - Organize by logical sections
        - If a file is provided, prioritize its specific contents.
        """
        content_to_send.append(prompt)

        # 🧠 Generate Content
        # We pass the list [file_part, prompt] so Gemini processes both
        response = model.generate_content(content_to_send)

        return {
            "generated_notes": getattr(response, "text", "⚠️ No response from AI")
        }

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        # If there's an error, return a 500 status or a clear error message
        return {"error": f"Internal Server Error: {str(e)}"}