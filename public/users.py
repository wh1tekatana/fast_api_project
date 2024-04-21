import uuid
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse , FileResponse
from models.good import Main_User,Main_UserDB, New_Respons
import hashlib
from typing import Union, Annotated

users_router = APIRouter()


def coder_pwrd(cod: str):
    result = cod * 2


user_list = [Main_UserDB(name='Kaplunov', id=1, password='*************'),
             Main_UserDB(name='Petrov', id=2, password='************')]
def find_user(id: int) -> Union[Main_UserDB,None]:
    for user in user_list:
        if user.id == id:
            return user
    return None


@users_router.get("/api/users",response_model=Union[list[Main_User],None])
def get_users():
    '''
    Документация APIRouter принадлежит пакету FastAPI и тд...
    '''
    return user_list

@users_router.get("/api/users/{id}",response_model=Union[Main_User,New_Respons])
def get_user(id: int):
    user = find_user(id)
    print(user)

    if user == None:
        return New_Respons(message = "Пользователь не найден")

    return user


@users_router.post("/api/users",response_model=Union[Main_User,New_Respons])
def create_user(item: Annotated[Main_User,Body(embed=True,description="Новый пользователь")]):
    user = Main_UserDB(name=item.name,id=item.id,password=coder_pwrd(item.name))
    user_list.append(user)
    return user



@users_router.put("/api/users/",response_model=Union[Main_User,New_Respons])
def edit_person(item: Annotated[Main_User,Body(embed=True,description="Изменение данных пользователя по id")]):
    user = find_user(item.id)
    if user ==None:
        return New_Respons(message="Пользователь не найден")
    user.id = item.id
    user.name = item.name
    return user



@users_router.delete("/api/users/{id}",response_model=Union[list[Main_User],None])
def delete_person(id: int):

    user = find_user(id)

    if user == None:
        return New_Respons(message = "Пользователь не найден")
    user_list.remove(user)

    return user_list