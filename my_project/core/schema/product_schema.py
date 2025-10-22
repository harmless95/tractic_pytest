from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .category_schema import CreateCategory, ReadCategory, UpdateCategory


class CreateProduct(BaseModel):
    name: str
    price: Decimal
    category: Optional[CreateCategory]

    model_config = ConfigDict(from_attributes=True)


class ReadProduct(BaseModel):
    id: UUID
    name: str
    price: Decimal
    category: Optional[ReadCategory]

    model_config = ConfigDict(from_attributes=True)


class UpdateProduct(BaseModel):
    id: UUID | None = None
    name: str | None = None
    price: Decimal | None = None
    category: Optional[UpdateCategory] | None = None

    model_config = ConfigDict(from_attributes=True)
