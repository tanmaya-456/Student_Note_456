from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import engine, SessionLocal
from models import Base, Note, User
from schemas import NoteCreate, UserCreate
from security import hash_password, verify_password
from jwt_handler import create_access_token, verify_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- Authentication --------------------

def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload


# -------------------- Notes --------------------

@app.post("/notes")
def create_note(
    note: NoteCreate,
    payload: dict = Depends(get_current_user)
):

    db = SessionLocal()

    new_note = Note(
        title=note.title,
        note=note.note,
        user_id=payload["user_id"]
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    db.close()

    return {
        "message": "Saved Successfully"
    }


@app.get("/notes")
def get_notes(
    payload: dict = Depends(get_current_user)
):

    db = SessionLocal()

    notes = db.query(Note).filter(
        Note.user_id == payload["user_id"]
    ).all()

    db.close()

    return notes


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    payload: dict = Depends(get_current_user)
):

    db = SessionLocal()

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == payload["user_id"]
    ).first()

    if not note:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()
    db.close()

    return {
        "message": "Deleted Successfully"
    }


# -------------------- Register --------------------

@app.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

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


# -------------------- Login --------------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        db.close()

        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        db.close()

        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

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