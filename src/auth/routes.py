from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.auth.schema import CreateUserModel, LoginModel
from src.rag_db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService



auth_router = APIRouter(prefix="/auth", tags=["auth"])
service = UserService()


@auth_router.post("/CreateUser")
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)) -> CreateUserModel: 
    email = user_data.email
    user_exists = await service.user_exist(email, session)

    if user_exists :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="User already exist")
    
    new_user = await service.create_account(user_data, session)

    return new_user 

@auth_router.post("/Login")
async def login(login_data: LoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await service.get_user_by_email(email, session)

    if not user or not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {"message": "Login successful"}