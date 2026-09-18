from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    address: str


class UserUpdateDTO(BaseModel):
    name: str
    email: EmailStr
    address: str


class UserResponseDTO(BaseModel):
    id: int|None
    name: str
    email: EmailStr
    address: str