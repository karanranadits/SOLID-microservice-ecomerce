from pydantic import BaseModel
from typing import Optional

class AddressDTO(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class ProfileResponseDTO(BaseModel):
    username: str
    name: str
    address: AddressDTO

class UpdateProfileRequestDTO(BaseModel):
    name: str
    address: AddressDTO
