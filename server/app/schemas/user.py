from pydantic import BaseModel, Field


class AdminUserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=128)
    role: str = Field(default="user")


class UserRoleUpdate(BaseModel):
    role: str