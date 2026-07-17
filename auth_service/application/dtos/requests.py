from pydantic import BaseModel

class UserCredentialsDTO(BaseModel):
    username: str
    password: str
