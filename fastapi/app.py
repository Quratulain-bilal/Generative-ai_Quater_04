from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Notes API", description="Simple CRUD Notes Application")

# In-memory database
notes_db: Dict[int, str] = {
    1: "First note",
    2: "Second note",
    3: "Third note",
    4: "Fourth note",
    5: "Fifth note"
}

# Note model
class Note(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    text: str

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Notes API! Visit /docs for Swagger UI"}

# Add new note
@app.post("/notes/", response_model=Note)
def add_note(note: Note):
    new_id = max(notes_db.keys()) + 1 if notes_db else 1
    notes_db[new_id] = note.text
    return {"text": note.text}

# Get all notes
@app.get("/notes/")
def get_all_notes():
    return notes_db

# Get single note
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": note_id, "text": notes_db[note_id]}

# Update note
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    notes_db[note_id] = note.text
    return {"message": "Note updated", "id": note_id, "text": note.text}

# Delete note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    deleted_text = notes_db.pop(note_id)
    return {"message": "Note deleted", "id": note_id, "deleted_text": deleted_text}