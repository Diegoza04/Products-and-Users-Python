from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0)
    is_active: bool = Field(default=True, alias="isActive")
    image: str | None = Field(default=None, max_length=255)


class ProductUpdate(ProductCreate):
    pass