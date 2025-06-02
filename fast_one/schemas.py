from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


# class Message(BaseModel):
#     message: str


# class UserPublic(BaseModel):
#     id: int
#     username: str
#     email: EmailStr


# class UserSchema(UserPublic):
#     password: str


# class UserDB(UserSchema):
#     id: int


# class UserList(BaseModel):
#     users: list[UserPublic]
