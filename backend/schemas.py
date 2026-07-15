from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    email: EmailStr

    password: str


class NoteCreate(BaseModel):

    title: str

    note: str