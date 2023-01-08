import psycopg2
from fastapi import APIRouter, status, Response, HTTPException, Depends
from oauth2 import create_access_token
from utils.crypt import verify
from db import models, schemas, database
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=schemas.TokenResponse)
def login(
        respone: Response,
        user_credentails: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db),
):
    try:
        user = (
            db.query(models.User)
            .filter(models.User.username == user_credentails.username)
            .first()
        )
    except psycopg2.DatabaseError as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error '{error}' occurred while connecting to the database",
        )
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify(user_credentails.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
        }
    )
    respone.set_cookie(key="token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}
