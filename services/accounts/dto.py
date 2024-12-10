from pydantic import BaseModel, Field


class CreateModel(BaseModel):
    address: str = Field(max_length=50)


class ResponseCreatedModel(BaseModel):
    address: str = Field(max_length=50)  # Barbara Liskov rules
