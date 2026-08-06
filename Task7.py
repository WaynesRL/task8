# Импорт модулей
import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone

app = FastAPI()

# БД
users = []
user_id_counter = 1

secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
algorithm = "HS256"
token_expire_minutes = 30

security = HTTPBearer()

# Модели
# Я не хеширую пароль, но в проде так делать нельзя!!!
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Вспомогательные функции 
def public(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email}

# Вспомогательные функции для JWT
def create_access_token(user: User) -> str:
    to_encode = {
        "sub": str(user.id),  # по стандарту sub — строка
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_expire_minutes),
    }
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, secret_key, algorithms=[algorithm])
        user_id = int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Токен истёк")
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(401, "Неверный токен")

    for u in users:
        if u.id == user_id:
            return u

# Регистрация пользователя
@app.post("/register")
def create_user(user: UserRegister):
    global user_id_counter

    for u in users:
        if u.email == user.email:
            raise HTTPException(400, "Пользователь с таким email уже существует")

    new_user = User(
        id=user_id_counter,
        name=user.name,
        email=user.email,
        password=user.password,
    )

    users.append(new_user)
    user_id_counter += 1

    return JSONResponse(content={"status": "Пользователь добавлен"}, status_code=201)

# Аутентификация пользователя, создание access токена
@app.post("/login")
def login(credentials: UserLogin):
    user = None
    for u in users:
        if u.email == credentials.email and u.password == credentials.password:
            user = u
            break

    if user is None:
        raise HTTPException(401, "Неверный email или пароль")

    access_token = create_access_token(user)

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=200
    )

# Защищенный маршрут: получить текущего пользователя
@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return JSONResponse(
        content={"id": current_user.id, "name": current_user.name, "email": current_user.email},
        status_code=200
    )

# Защищенный маршрут: получить всех пользователей
@app.get("/users", dependencies=[Depends(get_current_user)])
def get_users():
    return JSONResponse(
        content=[{"id": u.id, "name": u.name, "email": u.email} for u in users],
        status_code=200
    )
