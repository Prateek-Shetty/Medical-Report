from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.user import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, request: Request):
    db = request.app.state.db
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed
    del user_dict["password"]
    await db.users.insert_one(user_dict)

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, request: Request):
    db = request.app.state.db
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": db_user["role"]})
    return {"access_token": token}
