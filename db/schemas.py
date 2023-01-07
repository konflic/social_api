from typing import List, Optional
from fastapi import Query
from pydantic import EmailStr
from datetime import datetime
from pydantic import Required
from db import validators
from config import constants

from fastapi.exceptions import RequestValidationError, ValidationError

# from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator, Field


class Like(BaseModel):
    post_id: int = Query(default=Required, ge=constants.POST_ID_GE)
    dir: int = Field(
        default=Required, ge=constants.LIKE_MIN_VALUE, le=constants.LIKE_MAX_VALUE
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr = Field(default=Required)
    password: str = Field(default=Required, min_length=constants.MIN_LENGTH_PASSWORD)
    username: str = Field(
        default=Required,
        min_length=constants.MIN_LENGTH_USERNAME,
        max_length=constants.MAX_LENGTH_USERNAME,
    )

    _validator_password = validator("password", allow_reuse=True)(
        validators.validator_password
    )
    _validator_username = validator("username", allow_reuse=True)(
        validators.validator_name
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str = Field(
        default=Required,
        min_length=constants.MIN_LENGTH_POST_TITLE,
        max_length=constants.MAX_LENGTH_POST_TITLE,
    )
    content: str = Field(
        default=Required,
        min_length=constants.MIN_LENGTH_POST_CONTENT,
        max_length=constants.MAX_LENGTH_POST_CONTENT,
    )


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str = Field(
        None,
        min_length=constants.MIN_LENGTH_POST_TITLE,
        max_length=constants.MAX_LENGTH_POST_TITLE,
    )
    content: str = Field(
        None,
        min_length=constants.MIN_LENGTH_POST_CONTENT,
        max_length=constants.MAX_LENGTH_POST_CONTENT,
    )


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class EmailSchema(BaseModel):
    email: List[EmailStr]
