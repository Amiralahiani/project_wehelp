import secrets
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt
from backend.database.database import users_collection
from backend.database.models import UserRegister, UserLogin
from backend.config import JWT_SECRET, JWT_ALGORITHM

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(p):
    return pwd_context.hash(p)

def verify_password(p, h):
    return pwd_context.verify(p, h)

@router.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User exists")

    users_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })
    return {"msg": "User created"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": user.email}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}

# Utility endpoint: create a test user quickly
@router.post("/create-test-user")
def create_test_user():
    email = f"codex.user+{secrets.token_hex(4)}@example.com"
    password = f"Trustia!{secrets.token_hex(4)}"

    users_collection.insert_one({
        "email": email,
        "password": hash_password(password)
    })

    return {"email": email, "password": password}
