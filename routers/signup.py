from fastapi import APIRouter, status, HTTPException, Depends, Body
from utils.crypt import hash
from db import models, schemas, database
from sqlalchemy.orm import Session
from pydantic import Required

router = APIRouter(tags=["Signup"])


@router.post("/signup")
async def signup(
    user: schemas.UserCreate = Body(default=Required),
    db: Session = Depends(database.get_db),
):
    try:
        user_email_exists = (
            db.query(models.User).filter(models.User.email == user.email).first()
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while creating the user",
        )
    if user_email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this email is already exist",
        )
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while creating the user",
        )
    return new_user
