from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..auth import create_access_token, verify_password
from ..crud import get_user_by_phone_number, get_user_by_username
from ..database import SessionLocal
from ..schemas import Token, TokenData
from jose import JWTError, jwt

from app import crud


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_phone_number(db, form_data.username)
    if db_user is None:
        db_user = get_user_by_username(db, form_data.username)  # Fallback to username login
    
    if db_user is None or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}



SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the actual JWT token string
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user