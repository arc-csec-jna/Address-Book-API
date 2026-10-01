"""
Schema creation contract for User input and database response
"""

from pydantic import BaseModel


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str