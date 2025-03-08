    """
    Description: This module contains the API endpoints for user signup and login.
    API endpoints: /signup, /login
    """

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


router = APIRouter()

# Pydantic model for user signup
class UserSignup(BaseModel):
    email: str
    password: str

# Pydantic model for user login
class UserLogin(BaseModel):
    email: str
    password: str
    
# Secret key to encode and decode JWT tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_db.get(email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup") # /signup endpoint
async def signup(user: UserSignup):
   
    if user.email in users_db:
        
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    users_db[user.email] = {
        "email": user.email,
        "password": hashed_password
    }
    
    return {"message": f"User: {user.email} signed up successfully "}

@router.post("/login") # login endpoint
async def login(user: UserLogin):
    if user.email not in users_db or not verify_password(user.password, users_db[user.email]["password"]):
        # logging.warning(f"Login attempt failed for email: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    

    return {"access_token": access_token, "token_type": "bearer"}