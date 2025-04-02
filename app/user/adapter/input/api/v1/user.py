from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.container import Container
from app.user.adapter.input.api.v1.request import CreateUserRequest, LoginRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import CreateUserResponseDTO, GetUserListResponseDTO, LoginResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.exceptions.base import CustomException
from core.fastapi.dependencies import IsAdmin, PermissionDependency
from fastapi import status

user_router = APIRouter()


@user_router.get(
    "",
    response_model=list[GetUserListResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
@inject
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    return await usecase.get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
@inject
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    command = CreateUserCommand(**request.model_dump())
    await usecase.create_user(command=command)
    return command


@user_router.post(
    "/login"
)
@inject
async def login(
    request: LoginRequest,
    response: Response,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    token: LoginResponseDTO = await usecase.login(nickname=request.nickname, password=request.password)
    response.set_cookie("refresh_token", token.refresh_token, httponly=True)
    response.set_cookie("token", token.token)


