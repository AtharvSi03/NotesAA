from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesRequest(BaseModel):
    owner: str
    name: str
    description: str

@app.get("/")
async def root():
    return {"message": "Backend running on Render"}

@app.post("/generate")
async def generate_notes(data: NotesRequest):
    return {"message": "Received", "data": data}
