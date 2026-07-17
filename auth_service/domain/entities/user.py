from pydantic import BaseModel
from typing import Optional
from domain.entities.profile import Profile

class User(BaseModel):
    username: str
    password_hash: str
    profile: Profile = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.profile is None:
            self.profile = Profile(username=self.username)
