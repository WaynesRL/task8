# Импорт модулей
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Хранение пользователей (список)
users = []
user_id_counter = 1

# Создание моделей данных пользователей
class UserIn(BaseModel):
    name: str
    email: EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

# CRUD

# CREATE - создание пользователя
@app.post("/users")
def create_user(user: UserIn):
    global user_id_counter

    for u in users:
        if u.email == user.email:
            raise HTTPException(400, "Пользователь с таким email уже существует")

    new_user = User(
        id=user_id_counter,
        name=user.name,
        email=user.email,
    )
        
    users.append(new_user)
    user_id_counter += 1

    return JSONResponse(content={"message": "Пользователь добавлен"}, status_code=201)

# READ - прочитать всех пользователей
@app.get("/users")
def get_all_users():
    return JSONResponse(content=[u.model_dump() for u in users], status_code=200)

# READ - прочитать пользователя по id
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return JSONResponse(content=user.model_dump(), status_code=200)
    raise HTTPException(404, "Пользователь не найден")


# UPDATE - обновление данных пользователя
@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserIn):
    for i, user in enumerate(users):
        if user.id == user_id:
            for u in users:
                if u.email == data.email and u.id != user_id:
                    raise HTTPException(400, "Пользователь с таким email уже существует")

            updated = User(id=user_id, name=data.name, email=data.email)   # id сохраняем!
            users[i] = updated
            return JSONResponse(content=updated.model_dump(), status_code=200)
    raise HTTPException(404, "Пользователь не найден")

# DELETE - удаление пользователя
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return JSONResponse(content={"message": "Пользователь удален"}, status_code=200)
    raise HTTPException(404, "Пользователь не найден")
