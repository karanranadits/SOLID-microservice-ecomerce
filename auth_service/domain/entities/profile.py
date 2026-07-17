from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = ""

class Profile(BaseModel):
    username: str
    name: str = ""
    address: Address = Address()
