from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str 
    firstname: str 
    lastname: str
    is_active: bool | None 
    age: int | None = None

class UserRead(UserBase):
    pass

class UserCreate(UserBase):
    password: str


class UserPatch(UserBase):
    email: str | None
    firstname: str | None
    lastname: str | None

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
