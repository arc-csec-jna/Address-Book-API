"""
Schema creation contract for User input and database response
"""

from pydantic import BaseModel,ConfigDict


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class AddressResponse(BaseModel):
    id:int
    name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float | None
    longitude: float | None

    model_config = ConfigDict(from_attributes=True)

class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None