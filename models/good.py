from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, Identity, Sequence, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)
    class_id = Column(Integer, ForeignKey('classes.id'))
    user_class = relationship('Classes', back_populates='students')


class Tags(Enum):
    users = "users"
    classes = "classes"
    info = "info"
    good = "good"


class Classes(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String, nullable=False)
    students = relationship('User', back_populates='user_class')


class Main_User(BaseModel):
        id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
        name: Union[str, None] = None
        class_id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None


class Main_Classes(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    class_name: Union[str, None] = None


class Main_UserDB(Main_User):
    hashed_password: Annotated[Union[str, None], Field(max_length=200, min_length=6)] = None


class New_Respons(BaseModel):
    message: str