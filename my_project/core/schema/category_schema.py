from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateCategory(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ReadCategory(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateCategory(BaseModel):
    id: UUID | None = None
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)
