from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, Note
from schemas import NoteCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/notes")
def create_note(note: NoteCreate):

    db = SessionLocal()

    new_note = Note(

        title=note.title,

        note=note.note

    )

    db.add(new_note)

    db.commit()

    db.refresh(new_note)

    db.close()

    return {

        "message": "Saved Successfully"

    }

@app.get("/notes")
def get_notes():

    db = SessionLocal()

    notes = db.query(Note).all()

    db.close()

    return notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):

    db = SessionLocal()

    note = db.query(Note).filter(Note.id == note_id).first()

    if note:

        db.delete(note)

        db.commit()

    db.close()

    return {
        "message": "Deleted Successfully"
    }