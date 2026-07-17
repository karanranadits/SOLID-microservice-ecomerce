from application.interfaces.user_repository import UserRepository
from domain.entities.profile import Profile, Address
from application.dtos.profile_dtos import UpdateProfileRequestDTO
from typing import Optional

class GetProfileUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str) -> Optional[Profile]:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        return user.profile

class UpdateProfileUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, request: UpdateProfileRequestDTO) -> Profile:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        
        address = Address(
            street=request.address.street,
            city=request.address.city,
            state=request.address.state,
            zip_code=request.address.zip_code,
            country=request.address.country
        )
        
        user.profile.name = request.name
        user.profile.address = address
        
        self.user_repo.save(user)
        return user.profile
