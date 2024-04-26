from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserDisplay(UserBase):
    id: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
