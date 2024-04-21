from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from starlette import status
from sqlalchemy.orm import Session
from db import engine_s
from typing import Union, Annotated
from models.good import Tags, User, Classes, Main_User, New_Respons, Main_Classes

def get_session():
     with Session(engine_s) as session:
         try:
           yield session
         finally:
           session.close()



users_router = APIRouter(tags=[Tags.users], prefix='/api/users')
classes_router = APIRouter(tags=[Tags.classes], prefix='/api/classes')
info_router = APIRouter(tags=[Tags.info])


def coder_passwd(cod: str):
    return cod*2



@users_router.get("/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
def get_user_(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    else:
        return user


@users_router.get("/", response_model=Union[list[Main_User], New_Respons], tags=[Tags.users])
def get_user_db(DB: Session = Depends(get_session)):
    users = DB.query(User).all()
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users



@classes_router.get("/", response_model=Union[list[Main_Classes], New_Respons], tags=[Tags.classes])
def get_all_classes(DB: Session = Depends(get_session)):
    classes = DB.query(Classes).all()
    if not classes:
        return JSONResponse(status_code=404, content={"message": "Группы не найдены"})
    return classes


@users_router.post("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],
                DB: Session = Depends(get_session)):
    try:
      user = User(name=item.name, hashed_password=coder_passwd(item.name))
      user.class_id = item.class_id
      if user is None:
          raise HTTPException(status_code=404, detail="Объект не определен")
      DB.add(user)
      DB.commit()
      DB.refresh(user)
      return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")


@users_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user_(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")],
               DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = item.name
    user.class_id = item.class_id
    try:
        DB.commit()
        DB.refresh(user)  # сохраняем изменения
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user


@users_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
def delete_user(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(user)
        DB.commit()
    except HTTPException:
        JSONResponse(content={'message' : f'Ошибка'})
    return JSONResponse(content={'message' : f'Пользователь удалён {id}'})


@users_router.patch("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные по id")], id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    if item.name is not None:
        user.name = item.name
    if item.class_id is not None:
        user.class_id = item.class_id

    try:
        DB.commit()
        DB.refresh(user)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Произошла ошибка при обновлении пользователя: {str(e)}"})
    return user