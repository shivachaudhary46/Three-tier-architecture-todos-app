from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os 
from datetime import timedelta

from schemas import Token, UserRead, UserCreate
from database import get_db, User, hasher
from OAuth import authenticate_user, get_current_user, create_access_token

load_dotenv()
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE", 60))

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/token", response_model=Token)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    DB: Session = Depends(get_db)
):
    try:
        """
        Authenticate a user and return an access token.
        """
        user = authenticate_user(credentials.username, credentials.password, DB)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        access_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
        token = create_access_token(
            data={"sub": user.username},
            expire_time=access_time
        )

        return Token(access_token=token, token_type="bearer")
    
    except HTTPException:
        raise

    except Exception as e:
        print("Error", e)
        raise

@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    try: 
        """
        Return the currently authenticated user's information.
        """
        return current_user
    except: 
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.post("/", response_model=UserRead)
def add(user: UserCreate, db: Session = Depends(get_db)): 
    try: 
        db_user = User(
                username=user.username, 
                email=user.email, 
                password_hash=hasher.hash(user.password),
            )
        db.add(db_user)
        db.commit() 
        db.refresh(db_user)
        return db_user

    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))