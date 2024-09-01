from beanie import Document, Indexed
from pydantic import BaseModel, field_validator
from hashlib import md5
from typing import Annotated, Optional


class User(Document):
    email: Annotated[str, Indexed(unique=True)]
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    status: str = "active"
    email_verified: bool = False
    phone_number: str | None = None
    phone_number_verified: bool = False
    picture: str | None = None
    meta_data: dict = {}
    google_id: str | None = None
    refresh_token: str | None = None

    class Config:
        collection = "users"


class CreateUser(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

    @field_validator("password")
    def password_length(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return md5(value.encode()).hexdigest()


class UpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    meta_data: dict | None = {}
