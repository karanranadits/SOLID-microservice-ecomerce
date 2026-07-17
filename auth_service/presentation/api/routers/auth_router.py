from fastapi import APIRouter, Depends, HTTPException
from application.dtos.requests import UserCredentialsDTO
from application.dtos.responses import TokenResponseDTO
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.login_user import LoginUserUseCase
from presentation.api.dependencies import get_register_use_case, get_login_use_case, get_profile_use_case, update_profile_use_case, verify_token
from application.dtos.profile_dtos import ProfileResponseDTO, UpdateProfileRequestDTO, AddressDTO
from application.use_cases.manage_profile import GetProfileUseCase, UpdateProfileUseCase

router = APIRouter()

@router.post("/register", response_model=TokenResponseDTO)
def register(
    credentials: UserCredentialsDTO, 
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    try:
        token = use_case.execute(username=credentials.username, password=credentials.password)
        return TokenResponseDTO(access_token=token.access_token, token_type=token.token_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponseDTO)
def login(
    credentials: UserCredentialsDTO, 
    use_case: LoginUserUseCase = Depends(get_login_use_case)
):
    try:
        token = use_case.execute(username=credentials.username, password=credentials.password)
        return TokenResponseDTO(access_token=token.access_token, token_type=token.token_type)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/profile", response_model=ProfileResponseDTO)
def get_profile(
    username: str = Depends(verify_token),
    use_case: GetProfileUseCase = Depends(get_profile_use_case)
):
    try:
        profile = use_case.execute(username=username)
        return ProfileResponseDTO(
            username=profile.username,
            name=profile.name,
            address=AddressDTO(
                street=profile.address.street,
                city=profile.address.city,
                state=profile.address.state,
                zip_code=profile.address.zip_code,
                country=profile.address.country
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/profile", response_model=ProfileResponseDTO)
def update_profile(
    request: UpdateProfileRequestDTO,
    username: str = Depends(verify_token),
    use_case: UpdateProfileUseCase = Depends(update_profile_use_case)
):
    try:
        profile = use_case.execute(username=username, request=request)
        return ProfileResponseDTO(
            username=profile.username,
            name=profile.name,
            address=AddressDTO(
                street=profile.address.street,
                city=profile.address.city,
                state=profile.address.state,
                zip_code=profile.address.zip_code,
                country=profile.address.country
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

