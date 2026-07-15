from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, Note, User
from schemas import NoteCreate, UserCreate, UserLogin
from security import hash_password, verify_password
from jwt_handler import create_access_token

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


@app.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "Email already exists"
        }

    new_user = User(

    email=user.email,

    password=hash_password(user.password)

)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User Registered Successfully"
    }

@app.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        db.close()
        return {
            "message": "User not found"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):
        db.close()
        return {
            "message": "Incorrect Password"
        }

    token = create_access_token(
    {
        "user_id": db_user.id,
        "email": db_user.email
    }
)

    db.close()

    return {
    "access_token": token,
    "token_type": "bearer"
}